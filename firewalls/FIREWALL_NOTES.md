# Firewall Design for auth-service

## Filtering by Port, Protocol, and Source

A network firewall decides whether to pass traffic using three principal
criteria:

- **Port:** The destination port identifies the service being addressed. This
  deployment allows HTTPS on TCP port 443 and HTTP on TCP port 80 only so Nginx
  can redirect clients to HTTPS. It never permits Gunicorn's port 8000 from an
  external network.
- **Protocol:** A rule distinguishes TCP from UDP and other IP protocols. HTTPS,
  HTTP, and SSH use TCP here, so allowing TCP 443 does not automatically permit
  unrelated UDP traffic on port 443.
- **Source:** A rule can admit all internet clients or only a trusted network.
  TCP 443 is allowed from any source (`0.0.0.0/0`), while TCP 22 is restricted
  to the administrator range `203.0.113.0/24`.

`auth-service` itself listens on `127.0.0.1:8000`. There is no inbound firewall
rule for port 8000, so external clients must enter through the Nginx proxy on
443 instead of contacting Gunicorn directly.

## Where Firewalls Sit in the Protocol Stack

A traditional packet-filtering firewall works primarily at Layers 3 and 4. It
can inspect IP addresses, transport protocols, and port numbers and may track
connection state. It does not understand Layer 7 application meaning: a
network rule allowing TCP 443 cannot tell whether the encrypted HTTPS request
contains a legitimate login, an injection attempt, or a stolen token.

## Network-Level vs Application-Level Firewalls

A network-level firewall such as UFW/netfilter filters IP packets and transport
connections before they reach a listening process. For example, UFW can permit
TCP 443 but reject TCP 5432.

An application-level firewall or web application firewall understands HTTP and
application patterns after the connection is accepted and TLS is terminated.
For example, an Nginx WAF can block a request matching an injection rule while
allowing other requests on the same TCP 443 connection.

## Defense in Depth

A correctly configured firewall reduces the reachable attack surface, but it
does not make reachable code trustworthy. Malicious traffic sent as valid HTTPS
still passes through port 443. `auth-service` must therefore keep its password
hashing, input validation, authentication, authorization, secure cookie, and
rate-limiting controls. The network firewall, Nginx policy, operating-system
hardening, and application controls protect different failure modes; none is a
replacement for the others.
