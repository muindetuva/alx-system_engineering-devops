#!/bin/bash
# Inspect and stop a running container; pass its name as the first argument.
set -e

CONTAINER_NAME="${1:-docker-basics-app}"

docker ps
docker ps -a
docker exec -it "$CONTAINER_NAME" bash
docker logs "$CONTAINER_NAME"
docker logs -f "$CONTAINER_NAME"
docker stop "$CONTAINER_NAME"
