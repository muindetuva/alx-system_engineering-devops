# Orchestrating FastAPI Applications with Docker Compose

This project contrasts the commands required to operate a manually networked
FastAPI, Postgres, and Redis stack with a declarative Docker Compose setup.

The base Compose file contains shared application, database, cache, and
persistent-volume configuration. Docker Compose's default network lets the API
reach Postgres as `db` and Redis as `cache`. The automatically merged override
file adds a source bind mount and Uvicorn live reload for local development.
The production file instead runs four Uvicorn workers under Gunicorn and does
not mount host source code.

## Commands

- Development: `docker compose up --build`
- Production: `docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build`
- Manual baseline: build `my-fastapi-app:latest`, then run `./manual_setup.sh`
