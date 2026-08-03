# Containerizing FastAPI with Docker

This project moves a minimal FastAPI service from a single Uvicorn process to
a production-shaped container. It demonstrates Gunicorn-managed Uvicorn
workers, environment-driven configuration, secret-handling guidance,
multi-stage image construction, port publication, and reaching a database on
the Docker host.

## Files

- `Dockerfile` is the single-process Uvicorn baseline.
- `Dockerfile.gunicorn` uses four Uvicorn workers managed by Gunicorn.
- `Dockerfile.multistage` discards compiler packages and exposes port 8000.
- `.env.production.example` documents required configuration without secrets.
- `scripts/run_with_env.sh` compares `-e` flags with `--env-file`.
- `scripts/run_networked.sh` publishes port 8000 and uses
  `host.docker.internal` for the host PostgreSQL service.
- `SECRETS.md` and `MULTISTAGE_NOTES.md` explain the design and risks.

## Build and run

```bash
docker build -f Dockerfile.multistage -t fastapi-containerized .
docker run -p 8000:8000 --env-file .env.production fastapi-containerized
```

Create `.env.production` from the example and replace every placeholder. Never
commit that real file.
