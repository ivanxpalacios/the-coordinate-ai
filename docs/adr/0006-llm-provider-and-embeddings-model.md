# LLM provider and embeddings model selection (D-01, D-02)

## 1. Status: Proposed

## 2. Context

Phase 6 of the data pipeline (embeddings and ingestion) requires two decisions that were left open in PROJECT.md's section 15: D-01 (LLM provider for chat/generation) and D-02 (embeddings, local vs. API). Both are constrained by the project's stated goals: $0 monthly cost (section 14), the R-02 risk of free tiers changing or disappearing, the R-03 risk of cold-start degrading UX on free hosting, and a <3s p90 latency target for the first token.

## 3. Decision

D-01: **Groq**, using its free tier (no credit card, Llama 3.3 70B at 30 RPM / 1,000 RPD / 12K TPM, native fast streaming on LPU hardware). D-02: **local embeddings first**, using `sentence-transformers/all-MiniLM-L6-v2`, wrapped behind an interface so the provider can later be swapped for an API-based embedding model for evaluation.

## 4. Alternatives considered

For D-01: Gemini — rejected as primary despite a larger context window and stronger proprietary model quality, because its free tier has been cut twice within a year (Dec 2025 quota reduction, Apr 2026 removal of Pro from the free tier), directly conflicting with the project's stability priority. OpenRouter — rejected as primary due to a thin daily cap (50 req/day at $0). Qwen3 (via Alibaba's DashScope or OpenRouter) — rejected: competitive model quality, but DashScope's recurring free tier was discontinued in Apr 2026 (replaced by a one-time grant) and requires Chinese phone verification even on the international edition, while its OpenRouter free variant inherits the same thin limits as other `:free` models there. Mistral and Cohere — rejected as too limited for daily use (~2 RPM and 1,000 calls/month respectively).

For D-02: API-first embeddings — rejected because query-time embedding would become a runtime dependency on every chat request, not just at ingestion, reintroducing the exact free-tier-availability risk (R-02) that Groq was chosen to avoid, and adding network latency to the retrieval path. A hardcoded single embedding provider — rejected because Phase 6 explicitly needs to evaluate API options later per the user's request, and the swap needs to be a deliberate, documented process (re-embedding + dimension migration) rather than an untested assumption.

## 5. Consequences

Groq's free tier gives generous headroom for a hobby-scale app (1,000 requests/day) without card requirements, but its catalog is limited to open-weight models — solid for RAG-constrained generation, not frontier-level reasoning. Local embeddings remove the query-time external dependency, which directly mitigates R-02, but the model must run inside the API's container process, so its RAM footprint needs to be validated once D-03 (hosting platform) is decided — a firm constraint has not been set yet. Because pgvector fixes the embedding column's dimension, switching to an API-based embedding model later is not a drop-in swap: it requires re-embedding every existing chunk and migrating the `knowledge_chunks` table, not just changing a config value.

## 6. Date

August 29th, 2026.

## 7. Author

Iván Palacios Martínez
