# Urja Meter Ops Portal Protocol Specification

This document details how the legacy Urja Meter Ops portal operates under the hood, based on verified inspection facts from browser DevTools, network captures, and manual probes.

> **Status**: DRAFT / SKELETON (Phase 0). All sections below will be populated during Phase 1 investigation.

---

## 1. Portal Architecture Overview
- **Portal Base URL**: (Configured via `PORTAL_BASE_URL`)
- **Technology Stack**: *(Pending investigation: Server platform, session mechanism, rendering type)*
- **Data Transport Format**: *(Pending investigation: JSON, HTML scraping, XML, or hybrid)*

---

## 2. Authentication & Session Management
- **Login Endpoint**: *(Method, URL, payload structure)*
- **Credentials Handling**: *(Form-encoded vs JSON, username/password fields)*
- **Session Tokens / Cookies**: *(Cookie names, token headers, CSRF tokens)*
- **Session Expiry & Lifecycle**: *(Timeout duration, refresh behavior, idle vs hard expiry)*
- **Error Responses**: *(HTTP status code and response body when unauthorized)*

---

## 3. Endpoints & Data Exchange
### 3.1 Meter Search & Listing
- **Endpoint**: *(TBD)*
- **Method**: `GET` / `POST`
- **Query Parameters / Payload**:
- **Pagination**: *(Page number vs offset/limit, page size limits)*
- **Filtering & Sorting**:
- **Response Shape**:

### 3.2 Meter Detail & Location
- **Endpoint**: *(TBD)*
- **Identifiers**: *(Meter serial number, internal ID, MAC address)*
- **Response Shape**:

### 3.3 Consumption & Time-Series Readings
- **Endpoint**: *(TBD)*
- **Date/Time Parameters**: *(Format, timezone, range limits)*
- **Granularity**: *(Hourly, daily, monthly)*
- **Response Shape**:

### 3.4 Grid Hierarchy & Topology (Extension)
- **Endpoint**: *(TBD)*
- **Structure**: *(Parent-child relations, substation -> feeder -> transformer -> meter)*

---

## 4. Surprises & Quirks
*Document all anomalies, non-standard behaviors, and edge cases discovered during investigation.*
- *(To be added as discovered)*

---

## 5. Open Questions & Unverified Hypotheses
- [ ] What is the exact idle session timeout?
- [ ] Is there an undocumented bulk export (CSV/XLSX) endpoint?
- [ ] How does the portal respond when rate limits are exceeded?
- [ ] Are date/time values localized or in UTC?
