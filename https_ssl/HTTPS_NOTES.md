# HTTPS Protection for auth-service

## What an Attacker Sees

When a client sends credentials to the `auth-service` `/token` endpoint over
plain HTTP, an attacker sharing the same coffee-shop Wi-Fi can capture the TCP
traffic and read the HTTP method, path, headers, username, password, and token
response. Encoding credentials does not encrypt them; for example, Basic Auth
is only Base64 and can be decoded immediately.

With HTTPS, TLS encrypts the HTTP request and response before they cross the
network. The observer can still infer connection metadata such as server IP,
port, timing, and approximate traffic size, but cannot read the credentials,
token, headers, path, or response body. TLS also authenticates the server and
detects modification of traffic in transit.

## What HTTPS Does Not Protect

1. **A compromised server:** malware or unsafe server logs can read plaintext
   credentials after TLS termination.
2. **A compromised client device:** a keylogger, malicious extension, or stolen
   session can access data before it is encrypted or after it is decrypted.
3. **Application-level security failures:** HTTPS does not replace password
   hashing, input validation, authorization checks, safe token handling, or
   protection against vulnerabilities in `auth-service`.

## The Protocol Stack

For an HTTPS request, IP routes packets and TCP provides the reliable byte
stream. TLS sits above TCP and performs the handshake, authenticates the
certificate, derives session keys, and creates an encrypted channel. HTTP sits
above TLS, so the `/token` request and its response travel as encrypted TLS
records. At Nginx, TLS is terminated and the decrypted HTTP request is proxied
to `auth-service`; the internal proxy hop is therefore HTTP even though the
original client connection was HTTPS.
