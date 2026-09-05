# Paths and probes

## Follow the actual path

Trace client resolver, A/AAAA answer, route/VPN, gateway/NAT, host firewall, container publishing, reverse proxy, and application only where present. Test direct and proxied paths separately when both are intended. NAT loopback may differ from external access. A VPN client is not automatically an external WAN vantage point.

Inspect listeners on loopback versus wildcard/specific interfaces. Treat IPv6 independently from IPv4 NAT assumptions. For Docker, inspect network mode, host bind address, published ports, and the installed firewall backend. An `expose` declaration or internal container port is not the same as host publication. [Compose networking](https://docs.docker.com/compose/how-tos/networking/).

For DNS/DDNS, compare authoritative records with answers from the client resolver and account for TTL/caching. A successful provider API update does not prove propagation to that client, correct routing, or service reachability. For HTTPS, preserve the intended hostname/SNI when testing a chosen address. Record certificate hostname, chain validation, and expiry independently from application status. An insecure TLS probe can diagnose connectivity but cannot prove valid HTTPS.

## Interpret results narrowly

Use available tools such as `ss`, `ip`, DNS clients, and bounded `curl` or connection probes. Prefer explicit connect/total timeouts and a small retry budget. Do not scan a subnet when named endpoints answer the question. Avoid state-changing HTTP routes for readiness checks.

A timeout is ambiguous: routing, filtering, unavailable service, or an unusable test client may cause it. Establish a positive control and correlate rules/logs where needed before attributing denial to a firewall. A TCP connection proves a transport path, not successful authentication or application health. UDP requires protocol-specific evidence; silence alone does not distinguish open from filtered.

When the necessary external client, router access, or IPv6 path is unavailable, leave those matrix cells unverified. Do not silently substitute localhost or a different network. Separate observation from any proposed change.
