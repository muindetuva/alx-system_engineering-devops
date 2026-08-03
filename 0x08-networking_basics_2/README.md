# Networking Basics 2

This project practices local name resolution, discovering active IPv4
addresses, and opening a simple TCP listener for network troubleshooting.

### 0-change_your_home_IP
A Bash script that configures an Ubuntu server with the below requirements.

- `localhost` resolves to `127.0.0.2`.
- `facebook.com` resolves to `8.8.8.8`.

The script changes `/etc/hosts` and therefore must be run with sufficient
permissions. Restore `localhost` to `127.0.0.1` after the exercise on any
machine you intend to keep using.

### 1-show_attached_IPs
A Bash script that displays all active IPv4 addresses on the machine where it
is executed, including the loopback interface when active.

### 100-port_listening_on_localhost
A Bash script that listens on port `98` with Netcat. Connect from a second
terminal to verify that text sent over the socket is printed by the listener.
