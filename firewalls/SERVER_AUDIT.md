# Server Listening-Port Audit

## Listening Ports

Run the following command on the VPS to inspect TCP and UDP listeners together
with their owning processes:

```bash
sudo ss -tulnp
```

Representative output for the deployed server is:

| Protocol | Local address | Port | Process | Purpose |
|---|---|---:|---|---|
| TCP | `0.0.0.0` | 22 | `sshd` | Restricted administration |
| TCP | `0.0.0.0` | 80 | `nginx` | HTTP-to-HTTPS redirect |
| TCP | `0.0.0.0` | 443 | `nginx` | Public HTTPS entry point |
| TCP | `127.0.0.1` | 8000 | `gunicorn` | Internal `auth-service` |

Gunicorn is bound to `127.0.0.1:8000` only, never `0.0.0.0:8000`.

## Decision Per Port

- **Port 22 — leave open with a narrow rule.** `sshd` is needed for
  administration, but UFW and the security group admit only the trusted
  `203.0.113.0/24` range. Key-based login and disabled root login add a separate
  authentication layer.
- **Port 80 — leave open with a narrow service purpose.** Nginx needs this
  public listener only to redirect requests to HTTPS. No application data is
  served over cleartext HTTP.
- **Port 443 — leave open publicly.** This is the intended public interface.
  Nginx terminates TLS and forwards approved requests to the internal service.
- **Port 8000 — bind internal and firewall.** Gunicorn binds to `127.0.0.1`
  rather than `0.0.0.0` so an external interface cannot accept connections even
  if a firewall rule is later misconfigured. UFW also provides no allow rule
  for port 8000. Nginx reaches it over loopback.

These decisions apply the three-way framework: stop unnecessary services
entirely, bind internal services privately plus firewall them, and leave only
necessary public services open under the narrowest practical rule.

## What Would Get Closed

If the audit found an abandoned development server listening on `0.0.0.0:3000`,
the correct response would be to identify and disable its systemd unit, stop
the process, and remove its startup configuration. Merely adding a deny rule
would leave vulnerable and unmaintained software running locally. A follow-up
`sudo ss -tulnp` must confirm that the listener disappeared entirely.
