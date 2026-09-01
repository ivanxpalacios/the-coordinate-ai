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

## 8. Amendment (2026-09-01): Llama 3.3 70B removed from Groq's catalog

While testing `services/llm.py` (apps/api) end-to-end against the real Groq API, the model named in this ADR's Decision — `llama-3.3-70b-versatile` — returned `404 model_not_found`. Querying Groq's `/models` endpoint directly confirmed it is no longer listed, active or otherwise. This is R-02 materializing in practice, not just as a documented risk: the specific model backing D-01 disappeared from the provider's catalog roughly three days after this ADR was written, without the provider itself changing.

The active catalog at the time of this amendment includes, among text-generation-capable models: `openai/gpt-oss-120b`, `openai/gpt-oss-20b`, `openai/gpt-oss-safeguard-20b` (safety/moderation-oriented, not general-purpose), `qwen/qwen3.8-27b`, `qwen/qwen3.6-27b`, `allam-2-7b` (small, Arabic-focused), and `groq/compound` / `groq/compound-mini` (Groq's own tool-using agentic models, not a plain chat completion model).

Decision: replace the default model with `openai/gpt-oss-120b`. Reasoning: it is the largest general-purpose model in the current free-tier catalog, keeping the same "largest available open-weight model" intent that originally motivated picking Llama 3.3 70B over smaller alternatives. `openai/gpt-oss-20b` was considered as a lower-latency alternative but rejected for now, since RNF-01 (first token under 3s p90) has not yet been measured against either model — this can be revisited once real latency data exists. `groq/compound` was rejected because its agentic/tool-use behavior is out of scope for a RAG system that already does its own retrieval; introducing another layer of implicit tool-calling would complicate reasoning about what the model is doing with the retrieved context.

This amendment does not change D-01 itself (Groq remains the provider) — only the specific model configured, which is why it is recorded here as an amendment rather than reopening the decision. Given this is the second time a provider's catalog shifted underneath a written decision (see the Gemini free-tier cuts already cited in section 4), the model should be treated as inherently more volatile than the provider choice: `groq_model` is already exposed as its own configurable setting in `apps/api/src/config.py` (not hardcoded) specifically so this class of change stays a one-line config update rather than a code change.
