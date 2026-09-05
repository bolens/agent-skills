---
name: network-exposure-verification
description: Verify intended service reachability and isolation across host firewalls, Docker publishing, IPv4/IPv6, DNS, TLS, and LAN/WAN or VPN client paths. Use for exposure audits and network-policy verification, not broad external scanning or application authorization testing.
---

# Network exposure verification

Define which client should reach which service before testing or changing rules. A listener, firewall listing, DNS answer, or successful localhost request establishes only one part of the path.

## Establish the policy and target

Identify the owned hosts/services and authorized probe endpoints. Build a small allow/deny matrix: source client/network, destination name/address, protocol, port, address family, and expected result. Inspect canonical firewall, Compose, proxy, VPN, and DDNS configuration relevant to that matrix. Do not infer that every discovered host is in scope.

Keep default audit work read-only. A request to verify exposure does not authorize firewall changes, public DNS updates, router changes, service restarts, or scanning unrelated addresses. Existing authorization for a specific repair carries forward. Keep credentials and private topology out of shared output.

## Trace and measure

Read [paths and probes](references/paths-and-probes.md) when Docker, IPv6, split DNS, TLS termination, or remote access complicates the path. Compare configured intent with live listeners, routing, published ports, active firewall backend/rules, and proxy endpoints. Inspect the system's actual iptables/nftables/UFW arrangement rather than assuming a universal chain.

Docker-published traffic can bypass UFW's ordinary input/output filtering. Verify the real ingress path for the installed backend and network mode. Do not disable Docker's firewall management or flush rules as an audit shortcut. [Docker firewall behavior](https://docs.docker.com/engine/network/packet-filtering-firewalls/).

Probe a bounded set of explicit endpoints from the relevant available clients. Verify both expected access and expected denial, IPv4 and IPv6 when present, and VPN connected/disconnected states when requested. Identify the responder using TLS and application evidence so an unrelated service is not counted as success. Record timestamp, source vantage point, resolved address, protocol, and outcome.

For repairs, preserve the existing administrative path and prepare a tested recovery route and bounded rollback before applying potentially disconnecting changes. Apply only the authorized policy change. Recheck both intended access and denial from the same clients. Do not flush the firewall or remove protections to make a test pass.

Use [homelab-stack-triage](../homelab-stack-triage/SKILL.md) for service/dependency failures and [web-security](../web-security/SKILL.md) for application identity/authorization. Report verified policy cells, contradictory evidence, and unavailable vantage points. Do not call WAN isolation proven from a LAN-only check.
