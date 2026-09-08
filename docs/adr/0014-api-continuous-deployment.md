# API continuous deployment mechanism

## 1. Status: Accepted

## 2. Context

The web app (Vercel) already redeploys automatically on every push to `main` via Vercel's native Git integration — no action from this repo is needed. The API has no equivalent: it runs on an Oracle Cloud VM (ADR-0007, Ampere A1, ARM64) and every deploy so far has been manual (SSH in, pull, rebuild by hand), with no record of the process in the repo. `docker-compose.yml` at the repo root is dev-only (bind mounts, `npm run dev`) and is not meant for production use. CI already exists for the API (`.github/workflows/api.yml`: lint + test on every push/PR touching `apps/api/**`); CD needs to build on top of that without duplicating it.

## 3. Decision

Add a `deploy` job to the API workflow that runs only on push to `main` after the existing lint-and-test job succeeds. It connects to the Oracle VM over SSH and rebuilds the API's container **on the server itself** (`git pull` + `docker compose -f docker-compose.prod.yml up -d --build`), using a new production compose file (no bind mounts, no dev server flags). SSH connection details (host, user, private key) are stored as GitHub Actions secrets, never committed.

## 4. Alternatives considered

Build the image in GitHub Actions (x86_64 runners) and push it to a registry (GHCR), with the VM pulling the pre-built image — rejected for now: the Oracle VM is ARM64, so this would require a multi-arch `buildx` build plus registry authentication on the server, adding real infrastructure (a registry, its credentials, a second network hop) for a single-server deployment where the benefit — an immutable, pre-built artifact and instant rollback by tag — doesn't yet justify the complexity. A polling/webhook agent on the server (e.g. Watchtower) that pulls updates independently of GitHub Actions — rejected because it decouples "tests passed" from "deploy happened," reintroducing the risk of deploying code that never ran through CI.

## 5. Consequences

Every deploy rebuilds the Docker image directly on the free-tier VM (2 OCPU / 12GB RAM), consuming its resources during the build instead of shipping a pre-built artifact — acceptable at this scale, but worth revisiting (via the GHCR alternative above) if build times or resource contention become a problem, or if instant rollback-by-tag becomes valuable. A new `docker-compose.prod.yml` needs to be authored and kept in sync with the dev compose file's service definitions. The SSH private key granting deploy access now lives as a GitHub secret, which is a new credential surface to protect (repo secret access = deploy access to the production VM).

There is no automated rollback: if a deploy ships a broken build, recovering means SSHing in and manually running `git checkout <previous-commit> && docker compose -f docker-compose.prod.yml up -d --build`. Acceptable for now given the low deploy frequency of a solo project; a tagged-image + rollback-command extension is a reasonable future addition if that changes.

### Rollout notes (implementation, September 8th 2026)

The VM had no git history of its own — every previous deploy had been a manual file copy (`~/api`, populated via `scp`/Finder, no `.git`), so `git pull` had nothing to build on. Fixed by cloning the repo fresh into `~/the-coordinate-ai` using a dedicated read-only **GitHub Deploy Key** (SSH, "Allow write access" left unchecked — the server only ever needs to read, never push), separate from the `ORACLE_SSH_KEY` secret that lets GitHub Actions *into* the VM. Two distinct keys, two distinct trust directions.

The first real deploy run failed (`error: The following untracked working tree files would be overwritten by merge: docker-compose.prod.yml`) because that file had been `scp`'d onto the VM by hand during testing, before it existed in git history — `git pull` refused to clobber an untracked file it didn't create. Fixed by deleting the untracked copy (verified byte-identical to the committed version first) and re-running the job. Lesson for next time: don't hand-place files that a later commit is going to introduce — let `git pull` be the only thing that writes into that clone.

Also surfaced, out of scope for this ADR but worth a future look: `lint-and-test` took ~10 minutes because `uv sync` resolves a full CUDA build of `torch` (~2GB of `nvidia-*` packages) on a GitHub-hosted runner that has no GPU. A CPU-only torch pin in `apps/api/pyproject.toml` would likely cut CI time significantly.

## 6. Date

September 8th, 2026.

## 7. Author

Iván Palacios Martínez
