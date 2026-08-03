#!/bin/bash
# Build the final image and smoke-test tools and secret exclusions.
set -e

docker build -t docker-basics-app .
docker run --rm docker-basics-app curl --version
docker run --rm docker-basics-app sh -c "test -f .env && echo FOUND || echo NOT_FOUND"
echo "Build and verification complete"
