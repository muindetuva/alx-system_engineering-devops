# auth-service Security Group Rules

## Inbound Rules

```text
ALLOW TCP 22 from 203.0.113.0/24
ALLOW TCP 80 from 0.0.0.0/0
ALLOW TCP 443 from 0.0.0.0/0
```

There is never a rule for port 8000. That is `auth-service`'s own Gunicorn port,
and it must not be reachable from outside the security group. Gunicorn binds to
`127.0.0.1:8000`, and only Nginx proxies to it locally.

Likewise, there is no allow rule for TCP 5432; any hypothetical database on the
host remains private.

## Reconciling with UFW

These cloud rules match the final active rules established by `ufw_setup.sh`:
both layers allow TCP 80 and 443 from any source, restrict TCP 22 to
`203.0.113.0/24`, and expose neither TCP 8000 nor TCP 5432. The UFW script first
adds broad SSH access as a lockout-prevention bootstrap, adds the trusted-range
rule, and removes the broad rule before enabling the firewall. Therefore the
effective SSH restriction is the same at both layers rather than conflicting.

## Debugging Order

When a permitted connection does not work, check the security group first
because it is the upstream filter: a rejected packet never reaches the server
or UFW. After confirming the provider rule's protocol, port, and source, check
UFW on the VPS, then confirm that the expected process is listening on the
right address and port. This order follows the actual packet path and avoids
debugging an application that never received the connection.
