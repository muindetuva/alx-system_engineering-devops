# HTTPS and SSL for FastAPI

This project documents and demonstrates HTTPS protection for an authentication
service. It includes TLS and certificate notes, local self-signed certificate
generation, a production Certbot workflow, Nginx TLS termination with an HTTP
to HTTPS redirect, and FastAPI handling of the `X-Forwarded-Proto` header.

The shell scripts describe commands intended for an Ubuntu deployment host.
They should be reviewed and updated with the real production domain before
being executed.
