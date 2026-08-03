# Cloud Security Groups and Host Firewalls

## What a Security Group Is

A cloud security group is a virtual firewall enforced by the provider's network
infrastructure before a packet reaches the VPS. Its rules are configured in the
provider console, API, or infrastructure-as-code and are independent of the
guest operating system.

UFW is enforced inside the VPS by the Linux netfilter stack and is configured
with commands or host configuration. An administrator with root access can
change or disable UFW. The server has no comparable control over the provider's
security group, so those upstream restrictions survive even when the server
itself is compromised.

## Where It Sits in the Traffic Path

Inbound traffic follows this order:

`internet -> security group -> server's network interface -> UFW -> application`

The security group evaluates source, protocol, and destination port before the
packet reaches the server's network interface. Traffic blocked by the security
group never reaches UFW at all. Traffic the security group permits must still
pass UFW before Nginx or another process can receive it.

## Why This Matters If the Server Is Compromised

An attacker who gains root access could flush UFW rules, start a new listener,
or change local configuration. The attacker still cannot bypass the security
group because it is enforced on provider-owned infrastructure outside the VPS.
If the group exposes only TCP 22 from a trusted range and TCP 80/443 publicly,
an attacker's new service on port 8000 remains unreachable from the internet
even after UFW is disabled entirely.
