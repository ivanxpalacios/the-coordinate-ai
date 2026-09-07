# Two-stage retrieval: vector search + cross-encoder reranking

## 1. Status: Accepted

## 2. Context

With single-stage retrieval (pure vector similarity, k=10), a recall problem was detected: for questions like "Who is the Female Titan?" with `user_episode=25`, the chunk that actually resolves the identity (episode 23, Armin revealing Annie is the Female Titan) did not even make the top-20 results, because the episode 17 chunk — dense in the literal phrase "Female Titan" — ranked higher on pure lexical/semantic similarity. This was not a bug in the anti-spoiler filter (layer 1, PROJECT.md section 11) — that filter worked correctly; it was a **recall/ranking** problem in the bi-encoder stage. See ADR-0006 section 9 for the embeddings model swap that was tried first and reduced but did not close this gap.

## 3. Decision

Two-stage retrieval. Stage 1 (cheap, wide): `services/retrieval.py` still does vector search against pgvector, but now returns 25 candidates (`RETRIEVE_K`) instead of the final k. Stage 2 (precise, narrow): `services/reranking.py` reorders those 25 with a cross-encoder (`cross-encoder/ms-marco-MiniLM-L-6-v2`, via `sentence-transformers`, no new dependency) that scores `(question, passage)` pairs directly instead of comparing precomputed vectors, and the final k chunks that reach the LLM are cut from that reordered list. Both routers that call retrieval (`chat.py`, `search.py`) orchestrate the two stages themselves; `retrieval.py` stays a pure data-access layer.

## 4. Alternatives considered

Just raising the bi-encoder's k (e.g. to 20) without reranking — rejected because it doesn't address the root cause (the ranking itself, not the candidate count) and feeds more irrelevant noise into the LLM's context. Swapping the embeddings model — already done (see ADR-0006 section 9) and it did improve ranking (the correct chunk moved from outside the top-20 to rank 6), but was insufficient alone at k=5. Orchestrating both stages inside `retrieval.py` instead of in the routers — rejected because it would mix the data-access layer (pgvector) with the ML layer (cross-encoder) in the same file.

## 5. Consequences

Every question now pays for a second inference pass (cross-encoder over 25 pairs) — slower than a single vector comparison, but bounded and cheap on CPU. `RETRIEVE_K=25` is a chosen value, not one measured rigorously; if the correct chunk is later found to still fall outside that top-25 for some questions, raising it is the first lever to try. `services/reranking.py` is a second model to keep loaded in memory alongside the embeddings model.

## 6. Date

September 4th, 2026.

## 7. Author

Iván Palacios Martínez
