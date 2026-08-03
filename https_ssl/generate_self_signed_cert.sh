#!/bin/bash

set -euo pipefail

openssl req -x509 \
  -newkey rsa:4096 \
  -keyout key.pem \
  -out cert.pem \
  -days 365 \
  -nodes \
  -subj "/CN=localhost"

openssl x509 -in cert.pem -noout -subject -issuer
