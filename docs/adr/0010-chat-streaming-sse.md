# Streaming chat responses over Server-Sent Events (SSE)

## 1. Status: Accepted

## 2. Context

`POST /chat` waited for the full Groq completion before returning a `ChatResponse` JSON body. This meant the user saw a loading state for however long generation took (several seconds), instead of seeing the answer build up token by token — the experience described in RF-08 (PROJECT.md section 6.2) and expected from comparable chat products. Retrieval (embedding → vector search → cross-encoder rerank, ADR-0009) already finishes before generation starts, so the sources are known before the LLM is even called — nothing about retrieval needed to change.

## 3. Decision

`services/llm.py` gained `stream_complete()`, an async generator that calls Groq's `chat.completions.create(..., stream=True)` and yields each content delta as it arrives, instead of the blocking `complete()` (kept as-is, unused elsewhere but not removed). `routers/chat.py` now returns a `StreamingResponse` (`media_type="text/event-stream"`) instead of a `ChatResponse`. The generator emits three JSON-tagged event types over SSE: `{"type": "sources", "sources": [...]}` first (since sources are already known), then one `{"type": "token", "content": "..."}` per delta, and `{"type": "done"}` at the end. If Groq raises `LlmError` mid-stream, an `{"type": "error", "message": "..."}` event is emitted instead of an HTTP error status, since the 200 response headers are already committed by the time streaming starts.

## 4. Alternatives considered

WebSockets — rejected because the chat only needs unidirectional server→client push; WebSockets add protocol upgrade handling and bidirectional complexity with no corresponding benefit here. Plain text deltas instead of JSON-tagged events — rejected because the frontend needs to distinguish "this is a source" from "this is an answer token" from "this is the end," and plain text can't carry that without fragile heuristics (e.g. sniffing content). Keeping `ChatResponse`/non-streaming as the only contract and adding streaming later — rejected because it would mean redesigning the frontend's chat state handling twice instead of once.

## 5. Consequences

`/chat`'s response is no longer validated by FastAPI's `response_model` — a `StreamingResponse` body bypasses Pydantic validation, so the shape of each event is enforced only by the code in `_stream_chat`, not the framework. Swagger's `/docs` can no longer render a useful schema or a live demo of this endpoint (it waits for the connection to close before showing anything) — testing requires `curl -N` or an actual SSE-aware client. `models.chat.ChatResponse` is now unused (left in place, commented, in case a non-streaming variant returns). The frontend (Fase 3) must implement an SSE/`fetch` stream reader instead of a simple `await response.json()`.

## 6. Date

September 4th, 2026.

## 7. Author

Iván Palacios Martínez
