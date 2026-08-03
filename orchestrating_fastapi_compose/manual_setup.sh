#!/bin/bash
# Starts a manually networked FastAPI, Postgres, and Redis stack.

docker network create my-app-network

docker run -d \
  --name my-postgres \
  --network my-app-network \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=appdb \
  -v postgres-data:/var/lib/postgresql/data \
  postgres:16

docker run -d \
  --name my-redis \
  --network my-app-network \
  redis:7

docker run -d \
  --name my-api \
  --network my-app-network \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://postgres:secret@my-postgres:5432/appdb \
  -e REDIS_URL=redis://my-redis:6379/0 \
  my-fastapi-app:latest
