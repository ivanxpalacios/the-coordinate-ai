# Chat requires authentication; demo mode dropped from MVP

## 1. Status: Accepted

## 2. Context

RF-06 (PROJECT.md, section 6.1, "Should") allowed a visitor to try the chat without an account, in some limited form. Once registration became invite-only gated behind an access code (ADR-0011), the two decisions were in tension: the point of gating registration is controlling who can use the product, but an ungated demo chat would let anyone bypass that control anyway and use the RAG pipeline — and its free-tier LLM/embedding quota — without ever touching the gate.

## 3. Decision

The chat route (`/`, `apps/web/src/routes/Chat.tsx`) is wrapped in `RequireAuth` (`apps/web/src/features/auth/RequireAuth.tsx`), which reads the session from `AuthContext` and redirects to `/login` when there isn't one. `/about` stays public — it's the page recruiters land on to evaluate the project (PROJECT.md, section 5) and carries no usage cost. There is no limited/anonymous chat mode; every chat interaction requires a logged-in account.

## 4. Alternatives considered

Keeping a rate-limited anonymous demo alongside the gated full chat — rejected because it reopens the exact door the access-code gate (ADR-0011) was built to close: anyone could use the underlying free-tier quota without an invite, just through a side entrance. Gating only specific actions (e.g. allow read-only browsing, require login to send a message) — rejected as unnecessary complexity; the chat has no content to browse without sending a message, so a partial gate would add code for a state that doesn't meaningfully exist.

## 5. Consequences

RF-06 is dropped from MVP scope (PROJECT.md, section 6.1, marked accordingly) — recruiters must have an account to try the chat itself, not just read about it on `/about`. This raises the friction for the "90-second evaluation" persona (PROJECT.md, section 5): getting an access code and registering is now a precondition for ML/RAG a recruiter would want to try live. If that friction turns out to hurt the portfolio goal in practice, a scoped anonymous demo can be reintroduced later with its own rate limiting, separate from the invite gate.

## 6. Date

September 7th, 2026.

## 7. Author

Iván Palacios Martínez
