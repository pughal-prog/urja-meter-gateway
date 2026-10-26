"""Simulation server for the legacy Urja Meter Ops web portal.

Exhibits realistic legacy portal behaviors and quirks:
- Session cookie authentication (`urja_session`)
- Legacy field naming (`MTR_ID`, `MTR_SERIAL`, `DEVICE_STATUS`, `LAT`, `LNG`, etc.)
- Non-standard date format without timezone offset (`YYYY-MM-DD HH:MM:SS`)
- Abbreviated status codes ('ACTV', 'INAC', 'FLT', 'DISC')
- Coordinates returned as strings or floats
- Energy readings in watt-hours (Wh) requiring conversion to kWh
- Network hierarchy topology with orphan node and duplicate item quirks
- Polite rate limiting (429 when client bursts > 10 req/sec)
- Bulk export endpoint (`/api/export/meters.csv`)
"""

import csv
import io
import time
import uuid
from typing import Any

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

app = FastAPI(title="Urja Meter Ops (Legacy Portal Simulator)")

# In-memory session store: session_id -> {created_at, last_used, request_count}
SESSIONS: dict[str, dict[str, Any]] = {}
SESSION_EXPIRY_SECONDS = 900  # 15 minutes
MAX_REQUESTS_PER_SESSION = 50  # Forces re-auth simulation after 50 calls

# Rate limiter tracking: IP -> list of timestamps
REQUEST_TIMES: list[float] = []
BURST_LIMIT = 10

# Mock Seed Data: Substations -> Feeders -> Transformers -> Meters
MOCK_METERS = [
    {
        "MTR_ID": "URJA-MTR-1001",
        "MTR_SERIAL": "SN-2024-8891",
        "DEVICE_STATUS": "ACTV",
        "LAT": "13.0827",
        "LNG": "80.2707",
        "SITE_ADDR": "Plot 12, Anna Salai",
        "CITY": "Chennai",
        "SUBSTATION_NAME": "Central Substation 230kV",
        "FEEDER_CODE": "FDR-CHN-01",
        "TRANSFORMER_ID": "XFR-101",
        "COMM_TIMESTAMP": "2026-10-25 10:15:00",
        "INST_DT": "2024-01-15 09:00:00",
    },
    {
        "MTR_ID": "URJA-MTR-1002",
        "MTR_SERIAL": "SN-2024-8892",
        "DEVICE_STATUS": "ACTV",
        "LAT": 13.0835,
        "LNG": 80.2715,
        "SITE_ADDR": "Building 4, TTK Road",
        "CITY": "Chennai",
        "SUBSTATION_NAME": "Central Substation 230kV",
        "FEEDER_CODE": "FDR-CHN-01",
        "TRANSFORMER_ID": "XFR-101",
        "COMM_TIMESTAMP": "2026-10-25 10:14:30",
        "INST_DT": "2024-01-20 11:30:00",
    },
    {
        "MTR_ID": "URJA-MTR-1003",
        "MTR_SERIAL": "SN-2024-8893",
        "DEVICE_STATUS": "FLT",
        "LAT": "13.0841",
        "LNG": "80.2730",
        "SITE_ADDR": "Shop 7, Mount Road",
        "CITY": "Chennai",
        "SUBSTATION_NAME": "Central Substation 230kV",
        "FEEDER_CODE": "FDR-CHN-02",
        "TRANSFORMER_ID": "XFR-102",
        "COMM_TIMESTAMP": "2026-10-24 18:00:00",
        "INST_DT": "2024-02-10 14:00:00",
    },
    {
        "MTR_ID": "URJA-MTR-1004",
        "MTR_SERIAL": "SN-2024-8894",
        "DEVICE_STATUS": "INAC",
        "LAT": 13.0850,
        "LNG": 80.2742,
        "SITE_ADDR": "Substation Quarters B3",
        "CITY": "Chennai",
        "SUBSTATION_NAME": "Central Substation 230kV",
        "FEEDER_CODE": "FDR-CHN-02",
        "TRANSFORMER_ID": "XFR-102",
        "COMM_TIMESTAMP": None,
        "INST_DT": "2024-03-01 10:00:00",
    },
    {
        "MTR_ID": "URJA-MTR-1005",
        "MTR_SERIAL": "SN-2024-8895",
        "DEVICE_STATUS": "DISC",
        "LAT": "13.0862",
        "LNG": "80.2755",
        "SITE_ADDR": "Warehouse 9, North Sector",
        "CITY": "Chennai",
        "SUBSTATION_NAME": "North Hub Substation 110kV",
        "FEEDER_CODE": "FDR-CHN-03",
        "TRANSFORMER_ID": "XFR-103",
        "COMM_TIMESTAMP": "2026-10-25 09:45:00",
        "INST_DT": "2024-03-12 16:20:00",
    },
    {
        "MTR_ID": "URJA-MTR-1006",
        "MTR_SERIAL": "SN-2024-8896",
        "DEVICE_STATUS": "ACTV",
        "LAT": 13.0875,
        "LNG": 80.2768,
        "SITE_ADDR": "Tech Park Tower A",
        "CITY": "Chennai",
        "SUBSTATION_NAME": "North Hub Substation 110kV",
        "FEEDER_CODE": "FDR-CHN-03",
        "TRANSFORMER_ID": "XFR-103",
        "COMM_TIMESTAMP": "2026-10-25 10:20:00",
        "INST_DT": "2024-04-05 10:00:00",
    },
]

# Topology Hierarchy with realistic legacy quirks:
# - Root: Substation
# - Feeder -> Transformer -> Meter
# - Quirk 1: XFR-999 is an orphan node (parent FDR-UNKNOWN doesn't exist)
# - Quirk 2: MTR-1001 appears twice under XFR-101 (duplicate child entry)
MOCK_TOPOLOGY_RAW = [
    {"NODE_ID": "SUB-01", "NAME": "Central Substation 230kV", "TYPE": "substation", "PARENT_ID": None},
    {"NODE_ID": "SUB-02", "NAME": "North Hub Substation 110kV", "TYPE": "substation", "PARENT_ID": None},
    {"NODE_ID": "FDR-CHN-01", "NAME": "Feeder Central South", "TYPE": "feeder", "PARENT_ID": "SUB-01"},
    {"NODE_ID": "FDR-CHN-02", "NAME": "Feeder Central North", "TYPE": "feeder", "PARENT_ID": "SUB-01"},
    {"NODE_ID": "FDR-CHN-03", "NAME": "Feeder North Industrial", "TYPE": "feeder", "PARENT_ID": "SUB-02"},
    {"NODE_ID": "XFR-101", "NAME": "Transformer T-101 (Anna Salai)", "TYPE": "transformer", "PARENT_ID": "FDR-CHN-01"},
    {"NODE_ID": "XFR-102", "NAME": "Transformer T-102 (Mount Road)", "TYPE": "transformer", "PARENT_ID": "FDR-CHN-02"},
    {"NODE_ID": "XFR-103", "NAME": "Transformer T-103 (Tech Park)", "TYPE": "transformer", "PARENT_ID": "FDR-CHN-03"},
    {"NODE_ID": "XFR-999", "NAME": "Transformer T-999 (Unmapped Feeder)", "TYPE": "transformer", "PARENT_ID": "FDR-GHOST"},  # Orphan
    {"NODE_ID": "URJA-MTR-1001", "NAME": "Meter SN-2024-8891", "TYPE": "meter", "PARENT_ID": "XFR-101"},
    {"NODE_ID": "URJA-MTR-1001", "NAME": "Meter SN-2024-8891 (DUP)", "TYPE": "meter", "PARENT_ID": "XFR-101"},  # Duplicate
    {"NODE_ID": "URJA-MTR-1002", "NAME": "Meter SN-2024-8892", "TYPE": "meter", "PARENT_ID": "XFR-101"},
    {"NODE_ID": "URJA-MTR-1003", "NAME": "Meter SN-2024-8893", "TYPE": "meter", "PARENT_ID": "XFR-102"},
    {"NODE_ID": "URJA-MTR-1004", "NAME": "Meter SN-2024-8894", "TYPE": "meter", "PARENT_ID": "XFR-102"},
    {"NODE_ID": "URJA-MTR-1005", "NAME": "Meter SN-2024-8895", "TYPE": "meter", "PARENT_ID": "XFR-103"},
    {"NODE_ID": "URJA-MTR-1006", "NAME": "Meter SN-2024-8896", "TYPE": "meter", "PARENT_ID": "XFR-103"},
]


class LoginPayload(BaseModel):
    username: str
    password: str


def check_auth(request: Request) -> str:
    """Validate session cookie."""
    # Check rate limit
    now = time.time()
    REQUEST_TIMES.append(now)
    # Prune timestamps older than 1 second
    while REQUEST_TIMES and REQUEST_TIMES[0] < now - 1.0:
        REQUEST_TIMES.pop(0)
    if len(REQUEST_TIMES) > BURST_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded: Urja Portal max burst is 10 requests/sec",
        )

    session_cookie = request.cookies.get("urja_session")
    if not session_cookie or session_cookie not in SESSIONS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired session")

    session = SESSIONS[session_cookie]
    if now - session["last_used"] > SESSION_EXPIRY_SECONDS:
        del SESSIONS[session_cookie]
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired")

    session["request_count"] += 1
    session["last_used"] = now
    if session["request_count"] > MAX_REQUESTS_PER_SESSION:
        del SESSIONS[session_cookie]
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session rotated")

    return session_cookie


@app.post("/api/login")
async def login(payload: LoginPayload, response: Response):
    """Authenticate and issue session cookie."""
    if payload.username == "demo_user" and payload.password == "demo_password":
        session_id = f"urja_sess_{uuid.uuid4().hex}"
        SESSIONS[session_id] = {
            "created_at": time.time(),
            "last_used": time.time(),
            "request_count": 0,
        }
        response.set_cookie(
            key="urja_session",
            value=session_id,
            httponly=True,
            path="/",
        )
        return {
            "status": "SUCCESS",
            "message": "Authenticated successfully",
            "user": payload.username,
            "session_id": session_id,
        }
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad credentials")


@app.post("/api/logout")
async def logout(request: Request, response: Response):
    """Invalidate session."""
    cookie = request.cookies.get("urja_session")
    if cookie and cookie in SESSIONS:
        del SESSIONS[cookie]
    response.delete_cookie("urja_session")
    return {"status": "SUCCESS", "message": "Logged out"}


@app.get("/api/meters/search")
async def search_meters(
    request: Request,
    q: str | None = None,
    status_filter: str | None = None,
    start: int = 0,
    limit: int = 20,
):
    """List meters with legacy pagination and filters."""
    check_auth(request)
    results = MOCK_METERS

    if q:
        query_lower = q.lower()
        results = [
            m for m in results
            if query_lower in m["MTR_ID"].lower()
            or query_lower in m["MTR_SERIAL"].lower()
            or query_lower in m["SITE_ADDR"].lower()
        ]

    if status_filter:
        results = [m for m in results if m["DEVICE_STATUS"] == status_filter.upper()]

    total = len(results)
    paginated = results[start : start + limit]

    return {
        "RESULT_STATUS": "OK",
        "START_OFFSET": start,
        "PAGE_SIZE": limit,
        "TOTAL_COUNT": total,
        "METERS": paginated,
    }


@app.get("/api/meters/{meter_id}")
async def get_meter(meter_id: str, request: Request):
    """Get single meter details."""
    check_auth(request)
    for m in MOCK_METERS:
        if m["MTR_ID"] == meter_id or m["MTR_SERIAL"] == meter_id:
            return {"RESULT_STATUS": "OK", "METER": m}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meter not found")


@app.get("/api/meters/{meter_id}/readings")
async def get_meter_readings(
    meter_id: str,
    request: Request,
    from_date: str | None = None,
    to_date: str | None = None,
):
    """Get meter time-series readings in Wh (Watt-hours) and electrical stats."""
    check_auth(request)
    # Verify meter exists
    found = any(m["MTR_ID"] == meter_id for m in MOCK_METERS)
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meter not found")

    # Generate synthetic 24-hour readings for testing
    readings = []
    base_wh = 1250000.0  # 1250 kWh in Wh
    for hour in range(24):
        timestamp_str = f"2026-10-24 {hour:02d}:00:00"
        energy_wh = base_wh + (hour * 2400.0)  # ~2.4 kWh per hour in Wh
        readings.append({
            "TS": timestamp_str,
            "ENERGY_WH": round(energy_wh, 2),
            "VOLTAGE_V": round(230.0 + (hour % 5 - 2) * 1.5, 1),
            "CURRENT_A": round(10.5 + (hour % 4) * 0.8, 2),
            "POWER_FACTOR": 0.95,
        })

    return {
        "RESULT_STATUS": "OK",
        "MTR_ID": meter_id,
        "UNIT": "Wh",
        "READINGS_COUNT": len(readings),
        "READINGS": readings,
    }


@app.get("/api/topology/tree")
async def get_topology(request: Request):
    """Get raw distribution hierarchy topology."""
    check_auth(request)
    return {
        "RESULT_STATUS": "OK",
        "TIMESTAMP": "2026-10-25 10:00:00",
        "NODES": MOCK_TOPOLOGY_RAW,
    }


@app.get("/api/export/meters.csv")
async def export_meters_csv(request: Request):
    """Bulk CSV download of all meters."""
    check_auth(request)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(MOCK_METERS[0].keys()))
    writer.writeheader()
    for m in MOCK_METERS:
        writer.writerow(m)
    return PlainTextResponse(content=output.getvalue(), media_type="text/csv")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
