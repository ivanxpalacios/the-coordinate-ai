# Hosting platform selection (D-03)

## 1. Status: Proposed

## 2. Context

Phase 6 needs a place to run the FastAPI app (which hosts the local embedding model chosen in D-02, ADR-0006) and a Postgres database with pgvector for `knowledge_chunks`. The constraints are the same as D-01/D-02: $0 monthly cost, the R-03 cold-start risk, and the <3s p90 latency target — plus a new one from D-02: the container running the API needs enough RAM headroom for `all-MiniLM-L6-v2`'s runtime overhead, not just the model weights.

## 3. Decision

Compute: **Oracle Cloud "Always Free"** (Ampere A1, 2 OCPU / 12GB RAM as of the June 2026 tier reduction), always-on with no scale-to-zero. Database: **Neon** for managed Postgres with pgvector, accepting its autosuspend-after-5-minutes-idle behavior given its fast resume (~1-3s median).

## 4. Alternatives considered

Render and Koyeb — rejected as the primary compute host: both cap free instances at 512MB RAM, tight against the embedding runtime overhead flagged in D-02, and both spin down on idle (15-60s cold start on Render), conflicting with R-03 and the latency target. Railway and Fly.io — rejected outright: neither offers a genuine free tier as of 2026 (Railway requires payment after a one-time credit; Fly.io only offers a 7-day trial). Supabase — rejected for the database role: its free project pauses after 7 days of inactivity, a real risk for a low-traffic portfolio app, versus Neon's much shorter idle-to-suspend window and faster resume. Render's free Postgres — rejected: it is deleted entirely after ~44 days, unsuitable for data meant to persist.

## 5. Consequences

Oracle requires a credit card on file for a $1 identity hold (no recurring charge), and ARM instance capacity has been reported as frequently unavailable in US regions — provisioning in EU or APAC is more reliable and should be preferred. Splitting compute (Oracle) and database (Neon) across two providers means two dashboards/accounts to manage instead of one platform, and their network distance affects the latency budget — the Oracle region and the Neon region should be chosen close to each other. Neon's idle autosuspend still adds up to ~1-3s to the first request after a quiet period, even though compute itself stays always-on.

Oracle's stock Ubuntu images ship with `iptables` preconfigured to accept only inbound SSH (port 22) and reject everything else by default, independently of and in addition to the cloud-level firewall (Network Security Groups / Security Lists). Opening a port in the NSG is not sufficient to expose a service — a matching `iptables` rule must also be added inside the instance itself (and persisted with `netfilter-persistent`, or it reverts on reboot). This is not prominently documented in the Oracle console, and the failure mode ("connection refused") is indistinguishable from a port simply not being open at the NSG level, which cost debugging time during Phase 6 deployment.

## 6. Date

August 29th, 2026.

## 7. Author

Iván Palacios Martínez
