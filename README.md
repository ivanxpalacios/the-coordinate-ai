# The Coordinate AI

> Fanmade, non-commercial project. Not affiliated with, sponsored by, or endorsed by Hajime Isayama, Kodansha, MAPPA, or Wit Studio. *Attack on Titan* (進撃の巨人) is their property.

## What is this

An AI assistant that answers questions about the *Attack on Titan* universe — but only with information the user should already know based on the episode they've seen so far. No spoilers past your declared progress.

Full product and technical planning lives in [PROJECT.md](./PROJECT.md).

## Architecture

```
Frontend (Vite + React + TS)  →  API (FastAPI)  →  Supabase (Auth + Postgres + pgvector)
                                       │
                                       └──  LLM provider (free tier)

Offline: ETL pipeline (scrape → clean → chunk → label → embed → ingest)
```

See [PROJECT.md §8](./PROJECT.md#8-arquitectura) for the full diagram and stack rationale.

## Stack

| Layer | Technology |
|---|---|
| Frontend | Vite, React, TypeScript, React Router, Tailwind CSS |
| Backend | FastAPI, Python 3.12, Pydantic |
| Database / Vector store | Supabase (Postgres + pgvector) |
| Auth | Supabase Auth |
| Containers | Docker, Docker Compose |
| CI/CD | GitHub Actions |

## Running locally

Not yet available — Docker Compose setup is in progress. This section will be updated once it's functional.

## Project status

Early planning / Foundations phase. See the [roadmap in PROJECT.md](./PROJECT.md#13-roadmap) for current progress.

## Licensing

This project mixes assets with different rights, licensed separately rather than under one blanket license:

- **Code**: [MIT](./LICENSE).
- **Wiki-derived content** (`data/episodes.json` and future knowledge chunks): CC BY-SA, inherited from the source wiki, with per-fragment attribution (`source_url`, `source_title`).
- **Franchise images**: no license of their own; used under fair use (low resolution, attribution, non-commercial/illustrative purpose).

Rationale documented in [docs/adr/0001-licences.md](./docs/adr/0001-licences.md).
# the-coordinate-ai
