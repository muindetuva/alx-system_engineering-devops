# Reverse Proxy Design for auth-service

## Forward Proxy vs Reverse Proxy

A forward proxy acts for clients: it sends their outbound requests and hides
the clients from destination servers. A reverse proxy acts for servers: users
connect to the proxy, which selects and contacts an internal backend while
hiding that backend's topology and implementation from clients.

## Why auth-service Is Never Exposed Directly

The Gunicorn-managed `auth-service` process should be reachable only through
the host's private interface and firewall policy, not directly from the
internet. Nginx provides one hardened public entry point for TLS termination,
request size and timeout policy, access logs, static files, and future rate
limiting or caching without changing application code. It then proxies valid
requests to `127.0.0.1:8000`.

Although the required Gunicorn command binds `0.0.0.0:8000`, the VPS firewall
must deny public access to that port. A loopback-only bind would provide an
additional defense where the deployment architecture permits it.

## What Breaks Without It

If port 8000 is publicly exposed, a client can bypass Nginx and reach Gunicorn
without centralized TLS, limits, and proxy logging. An attacker could send
credentials over an unencrypted connection or avoid a rate limit configured at
Nginx, defeating the security boundary expected by the deployment.
