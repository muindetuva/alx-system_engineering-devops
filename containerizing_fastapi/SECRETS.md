# Secrets in Containerized Applications

## The `ENV` / `ARG` risk

A real secret supplied through Dockerfile `ENV` or build `ARG` is recorded in
the image build metadata or layer history. Replacing the value later does not
erase the earlier layer, and anyone able to inspect the image can use
`docker history` to recover clues or values. Dockerfiles must therefore contain
only non-sensitive defaults and names, never credentials.

## Source-control risk

An example environment file with obvious placeholders is safe documentation,
but the real `--env-file` containing production secrets must never be
committed. Add real files such as `.env` and `.env.production` to `.gitignore`,
keep the placeholder `.env.production.example`, and rotate a credential
immediately if it is ever published.

## Safer production alternatives

Use a dedicated secrets manager such as Docker Secrets, HashiCorp Vault, AWS
Secrets Manager, or an equivalent platform service. The deployment platform
should inject a short-lived secret at runtime, restrict which workload can read
it, provide audit logs, and support rotation without rebuilding the image.
