# Invite-only registration via a backend-mediated access gate

## 1. Status: Accepted

## 2. Context

RF-01 originally allowed anyone to register with just email and password. The intended audience for this portfolio project is narrower: people the author trusts, and recruiters evaluating it — not the open internet. Access needed to be restricted at the point of account creation, without adding friction for the two intended audiences, and without depending on outbound email (already ruled out for account confirmation, to avoid Supabase's free-tier email rate limit).

The frontend talks to Supabase directly for auth (no backend involvement in a normal signup), which put the access-code check at a fork: either it lives in client-side JavaScript, or the backend has to mediate account creation itself.

## 3. Decision

Registration goes through the backend: `POST /auth/register` (`apps/api/src/routers/auth.py`) compares the submitted access code against `REGISTRATION_ACCESS_CODE` (a server-only environment variable) using `secrets.compare_digest`, then calls Supabase's Admin API (`services/supabase_admin.py`) to create the user directly, authenticated with `SUPABASE_SECRET_KEY` (Supabase's service-role-equivalent key, which bypasses Row Level Security and is never sent to the client). The account is created with `email_confirm: true`, so it's immediately usable — sidestepping Supabase's confirmation-email flow entirely, at the code level rather than a dashboard toggle. Login is unaffected: the frontend still calls `supabase.auth.signInWithPassword` directly, since only account *creation* needs gating.

## 4. Alternatives considered

Client-side gate (comparing the code against a `VITE_...` value in the frontend) — rejected as insufficient once the goal moved from "keep out casual/accidental sign-ups" to "keep out anyone without the code": any value shipped in a JS bundle can be extracted by inspecting network requests or the built bundle, so it would have been security theater rather than a real gate. Supabase's native invite flow (disable public sign-up, invite each trusted person from the dashboard) — rejected to avoid a per-person manual dashboard step and to keep the flow inside the project's own UI, and because invite emails would still route through the same rate-limited free-tier email sender the confirmation-email decision was trying to avoid entirely. `supabase-py` (official SDK) instead of a direct `httpx` call — rejected for a single REST call; the SDK bundles more clients (Postgrest, Realtime) than this endpoint needs.

## 5. Consequences

`SUPABASE_SECRET_KEY` — the highest-privilege credential in the project's Supabase account — now lives in the API's runtime, expanding the blast radius of a backend compromise; it must never reach the frontend or a versioned file. The access code is a shared secret with no per-person revocation: if it leaks, the fix is rotating `REGISTRATION_ACCESS_CODE`, which invalidates it for everyone, not just the leaker. There's no self-serve password reset via email (consistent with the earlier no-outbound-email decision) — a forgotten password currently has no recovery path and would need one added deliberately if it becomes a real problem. RF-01 (PROJECT.md, section 6.1) no longer describes open registration; it's amended to reflect the access-code requirement.

## 6. Date

September 7th, 2026.

## 7. Author

Iván Palacios Martínez
