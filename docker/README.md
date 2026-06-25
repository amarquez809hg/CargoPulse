# Cargo Pulse — Docker

## Quick start (local)

```bash
cd docker
cp .env.example .env    # edit SECRET_KEY + POSTGRES_PASSWORD for real deploys
./run.sh                # Postgres + Gunicorn → http://127.0.0.1:8000/
```

Dev with live code reload:

```bash
./run-dev.sh
```

## GCP VM

See [docs/DEPLOY_GCP.md](../docs/DEPLOY_GCP.md) for full VM setup, nginx, and HTTPS.

## Stack

| Service | Image | Port |
|---------|-------|------|
| `web` | Custom Django + Gunicorn | 8000 (host) |
| `db` | postgres:16-alpine | internal |

On start, `entrypoint.sh` runs migrations and `collectstatic`.
