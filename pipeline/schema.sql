-- Requires the pgvector extension. You already enabled it manually via
-- the Neon SQL editor, but this line makes the dependency explicit and
-- keeps the script idempotent if run against a fresh database.
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS knowledge_chunks (
    -- Generated in Python as uuid5(source_url + chunk_index), not by
    -- Postgres. This makes re-running the ingest script safe: the same
    -- chunk always produces the same id, so re-ingestion becomes an
    -- upsert instead of a duplicate insert.
    id              uuid PRIMARY KEY,

    content         text NOT NULL,

    -- Dimension is fixed by the embedding model (all-MiniLM-L6-v2, ADR-0006).
    -- Changing models later requires a migration, not a config change.
    embedding       vector(384) NOT NULL,

    source_url      text NOT NULL,
    source_title    text NOT NULL,
    entity          text,

    -- The critical column. Every retrieval query filters on this
    -- BEFORE ranking by vector distance (PROJECT.md section 11, layer 1).
    reveal_episode  int NOT NULL,

    confidence      text NOT NULL DEFAULT 'auto',
    created_at      timestamptz NOT NULL DEFAULT now()
);

-- Approximate nearest-neighbor search on the embedding column.
-- Cosine distance because sentence-transformers models are trained
-- and evaluated on cosine similarity.
CREATE INDEX IF NOT EXISTS knowledge_chunks_embedding_idx
    ON knowledge_chunks
    USING hnsw (embedding vector_cosine_ops);

-- Plain B-tree for the reveal_episode <= user_episode filter.
-- Separate from the vector index on purpose: different access method,
-- different query shape (equality/range vs. distance ranking).
CREATE INDEX IF NOT EXISTS knowledge_chunks_reveal_episode_idx
    ON knowledge_chunks (reveal_episode);