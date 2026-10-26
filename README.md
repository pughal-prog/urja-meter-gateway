# Urja Meter Gateway

A clean, documented REST API gateway built in front of the legacy "Urja Meter Ops" web portal (a smart-meter lookup portal with no native API).

---

## 1. Overview & Motivation
- **What**: Wraps the legacy Urja Meter Ops web portal with a modern, resource-oriented RESTful API.
- **Why**: Provides programmatic, typed, and structured access to smart-meter lookups, readings, consumption metrics, and grid hierarchy without direct brittle browser interaction.
- **Anti-Corruption Layer**: Isolates portal quirks, session lifecycles, and formatting oddities inside `src/urja_api/portal/` so external consumers interact exclusively with standard ISO-8601 UTC timestamps, explicit units, and clean schemas.

---

## 2. Quickstart & Installation

### Prerequisites
- Python 3.12+ (tested on Python 3.12 & 3.13)
- `pip` or `uv`

### Setup
```bash
# Clone and enter directory
git clone https://github.com/pughal-prog/urja-meter-gateway.git
cd urja-meter-gateway

# Configure environment variables
cp .env.example .env
# Edit .env with your portal credentials

# Install dependencies in editable mode with development tools
make install
```

### Running Locally
```bash
# Start the development server
make run
```
The API is available at `http://127.0.0.1:8000`. Interactive documentation is available at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI Schema: `http://127.0.0.1:8000/openapi.json`

---

## 3. Sample Requests & Responses

*(To be populated as endpoints and response shapes are verified)*

---

## 4. Key Design Decisions & Trade-offs
- **Anti-Corruption Architecture**: Legacy portal interaction is strictly contained in `src/urja_api/portal/`. Domain models and routes have zero awareness of portal session headers or HTML quirks.
- **Read-Only & Polite Rate Limiting**: The client enforces client-side rate limiting to avoid burdening the legacy portal.
- **Session Lifecycle & Re-Auth**: Authentication state is maintained and automatically refreshed upon session expiry or 401 detection.
- **See also**: [docs/decisions.md](docs/decisions.md) for Architecture Decision Records (ADRs).

---

## 5. Assumptions & Constraints
- The portal is read-only; no mutating actions or write-backs to smart meters are performed.
- All portal knowledge is derived exclusively from verified network activity and inspectable requests.
- Credentials are provided via environment variables.

---

## 6. Intentionally Skipped & Next Steps
- *To be detailed during progressive implementation.*

---

## 7. Documentation Links
- [PROTOCOL.md](PROTOCOL.md): Verified portal behavior, authentication flows, endpoint schemas, quirks, and open questions.
- [docs/investigation-log.md](docs/investigation-log.md): Running chronological log of exploration, findings, and tests.
- [openapi.json](openapi.json): Committed OpenAPI 3.1 specification.

---

## 8. Reflection
*(See [REFLECTION.md](REFLECTION.md) or final submission reflection)*
