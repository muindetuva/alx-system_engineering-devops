#!/bin/bash
# Build the Gunicorn image and demonstrate both environment mechanisms.

docker build -f Dockerfile.gunicorn -t fastapi-containerized .
docker run -e DATABASE_URL="postgresql://user:pass@db-host:5432/appdb" -e DEBUG="false" fastapi-containerized
docker run --env-file .env.production.example fastapi-containerized
