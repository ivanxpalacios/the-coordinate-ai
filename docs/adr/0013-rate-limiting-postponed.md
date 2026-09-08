# Per-user rate limiting postponed (RF-12)

## 1. Status: Accepted

## 2. Context

RF-12 (PROJECT.md, section 6.1) calls for rate limiting per user and globally, mitigating R-07 (PROJECT.md, section 12: "abuse of the API exhausts the free quota"). Access to the product is invite-only, gated behind a shared access code validated at registration (ADR-0011), and current traffic is low. A concrete design was discussed during Phase 4 closeout: an in-memory counter keyed by `user_id`, off by default.

## 3. Decision

Per-user rate limiting is postponed. The access-code gate (ADR-0011) stands as the primary mitigation for R-07 for now: it controls *who* can generate traffic, even though it does not cap *how much* traffic any single admitted user generates.

## 4. Alternatives considered

Implementing the in-memory counter now — rejected: beyond being extra work for a risk that's currently low given the small number of invited users, an in-memory counter is process-local and doesn't survive a restart or scale across multiple instances. Building it now would mean rebuilding it later if the hosting setup changes, for a problem that isn't pressing yet. Global-only rate limiting (no per-user dimension) — rejected: it wouldn't stop a single invited user from exhausting the quota alone, which is the more likely failure mode given the small invite pool. A Redis-backed limiter — rejected: unjustified infrastructure and cost for a $0/month, low-traffic portfolio project.

## 5. Consequences

R-07 remains partially open: if the access code leaks beyond its intended recipients, or traffic grows sustained, a single user or a handful of users could exhaust the Groq free-tier quota with no per-user cap in place. This decision should be revisited if either of those two triggers occurs — the access code is shared beyond its intended scope, or traffic grows sustained — at which point the in-memory design (or a durable alternative, if the hosting setup has changed by then) should be implemented.

## 6. Date

September 8th, 2026.

## 7. Author

Iván Palacios Martínez
