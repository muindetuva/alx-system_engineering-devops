# Firewalls

This project documents and implements layered network protection for the
deployed `auth-service`. It combines a default-deny UFW policy, a listening-port
audit, SSH hardening, and matching cloud security-group rules while keeping
Nginx public and Gunicorn private.
