# Architecture Decision Records (ADRs)

This document tracks key engineering decisions, their context, alternatives considered, and rationale.

---

## ADR-001: Anti-Corruption Layer Architecture
- **Date**: 2026-10-25
- **Status**: Accepted
- **Context**: The Urja Meter Ops legacy portal was not designed as an API and may have quirks, inconsistent keys, and unconventional session mechanisms.
- **Decision**: Isolate all portal-specific communication (HTTP client, authentication, retry logic, HTML/JSON parsing) strictly within `src/urja_api/portal/`. Domain models and API routes must never reference portal-specific types or headers.
- **Consequences**: Easy to maintain; portal layout or session changes will only require updating parsers or client auth without affecting downstream API consumers.

---

## ADR-002: Technology Stack Selection
- **Date**: 2026-10-25
- **Status**: Accepted
- **Context**: Need a fast, typed, maintainable backend service with automated documentation and robust HTTP client capabilities.
- **Decision**: Use Python 3.12+, FastAPI, httpx for async HTTP communication, Pydantic v2 for data validation, and pytest + respx for testing.
- **Consequences**: Native async support, high performance, automatic OpenAPI generation, and fast deterministic testing without hitting the live portal during CI.
