# Deployment Plan for auth-service

## Deployment Target Decision

`auth-service` will target a VPS for this exercise. A PaaS would offer greater
convenience by managing the operating system, process lifecycle, routing, and
TLS, but the VPS provides the control needed to practise systemd, Nginx, and
certificate management directly. That control also makes network policy and
deployment behavior explicit, which is valuable for an authentication service.

The trade-off is operational responsibility: the team owns patching,
monitoring, capacity, backups, recovery, and every security configuration on
the host. A production team without that capacity should choose a PaaS instead.

## What a VPS Would Require

A VPS places these concerns directly on the team:

- firewall rules that expose only SSH, HTTP, and HTTPS while protecting port
  8000 from direct internet access;
- HTTPS/TLS termination, certificate issuance, and automatic renewal;
- Nginx reverse-proxy configuration and security headers;
- Gunicorn worker sizing and systemd process supervision;
- operating-system and dependency security updates;
- deployment of new code, migrations, health checks, monitoring, and rollback.

A PaaS normally handles the public load balancer, firewall defaults, TLS
certificates, process restarts, health routing, deployment mechanism, and much
of the host patching. The application team still owns secure code, secrets,
data migrations, observability, and recovery decisions.

## A Migration Scenario

If traffic grows enough to require autoscaling across several regions while
keeping token verification available during a host failure, migrate from the
single VPS to managed containers. A platform such as a managed Kubernetes or
container service can run multiple replicas, perform health-aware rolling
updates, distribute secrets, and route traffic across healthy instances.
