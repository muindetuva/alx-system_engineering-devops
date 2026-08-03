#!/bin/bash

set -euo pipefail

sudo apt update
sudo apt install certbot -y
sudo certbot certonly --standalone -d auth.example.com

# Certificate: /etc/letsencrypt/live/auth.example.com/fullchain.pem
# Key: /etc/letsencrypt/live/auth.example.com/privkey.pem

sudo certbot renew --dry-run
