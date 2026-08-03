#!/bin/bash
# Build and run a live-mounted local development container.
set -e

docker build -t docker-basics-app .
docker run -p 8000:8000 -v $(pwd):/app docker-basics-app
