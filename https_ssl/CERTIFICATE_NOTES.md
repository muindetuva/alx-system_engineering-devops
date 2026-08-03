# TLS Certificate Trust for auth-service

## Certificate Fields

1. **Subject:** identifies the certificate holder, including the DNS names the
   certificate is valid for, such as `auth.example.com`.
2. **Issuer:** identifies the Certificate Authority (CA) that signed and issued
   the certificate.
3. **Public key:** lets clients establish encrypted sessions and verify proofs
   made by the server's corresponding private key.
4. **Validity period:** gives the `not before` and `not after` timestamps during
   which the certificate may be trusted.
5. **Digital signature:** the issuer's signature binds the subject, public key,
   validity period, and other certificate data so tampering can be detected.

## Chain of Trust

A browser trusts a small set of root CA certificates distributed with its
operating system or trust store. The root CA signs an intermediate CA
certificate, and the intermediate signs the server certificate presented by
`auth-service`. The server sends its certificate and intermediate chain; the
browser verifies each signature until it reaches a trusted root.

Intermediate CAs protect the root because the root private key can remain
offline. If an intermediate is compromised, it can be revoked and replaced
without replacing the root certificate in every browser and operating system.

## Self-Signed vs CA-Issued

For local `auth-service` development, a self-signed certificate is appropriate
because developers control the machine and can explicitly trust the generated
certificate. Browsers will warn until that trust is configured, which is
expected because no independent CA has vouched for it.

For a real production deployment, `auth-service` needs a CA-issued certificate
whose subject covers its public domain. A publicly trusted CA such as Let's
Encrypt lets ordinary clients validate the service without manually installing
a local certificate and supports a renewable, auditable trust chain.
