# Docker Basics

This project packages a small FastAPI application in a reproducible Docker
image. It demonstrates image and container concepts, Dockerfile construction,
`ENTRYPOINT` and `CMD`, bind-mounted development, container debugging,
layer-efficient package installation, and secure build-context exclusions.

## Build and run

```bash
docker build -t docker-basics-app .
docker run --rm -p 8000:8000 docker-basics-app
```

The API is then available at `http://localhost:8000`, with a health endpoint at
`/health`. Use `scripts/dev_run.sh` for a bind-mounted development workflow and
`scripts/build_and_verify.sh` for the final image checks.
