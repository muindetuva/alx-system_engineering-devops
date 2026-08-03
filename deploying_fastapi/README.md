# Deploying a FastAPI Application

This project packages `auth-service` for a production-style VPS deployment.
It documents the deployment decision, runs Gunicorn under systemd, terminates
TLS and serves static assets with Nginx, exposes a dependency-aware health
check, enables graceful reloads, and records practical rollback procedures.

The systemd and Nginx files use example paths and domains. Review them against
the target host before installing or enabling either configuration.
