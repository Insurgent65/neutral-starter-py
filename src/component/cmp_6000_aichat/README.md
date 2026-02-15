# cmp_6000_aichat

AI chat component integrated with `ai_backend_0yt2sa`.

## Current Security Status

Implemented:

- Session gating in UI using `HAS_SESSION`.
- Session enforcement in API endpoints (`/api/chat`, `/api/profiles`).
- Generic HTTP 500 responses without internal exception leakage.
- Markdown rendering with HTML sanitization to reduce XSS risk.
- Automated tests for:
  - Unauthorized access (`401`) when session is missing.
  - Generic `500` error behavior without leaking exception details.

## Pending Hardening

- Add rate limiting/abuse controls for chat endpoints.
- Expand tests to cover throttling behavior and additional security edge cases.
