#!/bin/bash
# Build the optimized image and connect it to a host-run PostgreSQL service.

docker build -f Dockerfile.multistage -t fastapi-containerized .
docker run -p 8000:8000 -e DATABASE_URL="postgresql://user:pass@host.docker.internal:5432/appdb" fastapi-containerized
