#!/bin/bash

# Configure the host firewall for the Nginx-fronted auth-service deployment.

sudo ufw default deny incoming
sudo ufw default allow outgoing

# Bootstrap SSH access before enabling the default-deny policy.
sudo ufw allow 22/tcp

# Public Nginx entry points.
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Defense in depth for a hypothetical local PostgreSQL service.
sudo ufw deny 5432/tcp

# Restrict ongoing SSH access, then remove the broad bootstrap rule.
sudo ufw allow from 203.0.113.0/24 to any port 22
sudo ufw --force delete allow 22/tcp

sudo ufw enable
sudo ufw status verbose
