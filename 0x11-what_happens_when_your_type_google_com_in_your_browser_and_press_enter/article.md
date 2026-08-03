# What Happens When You Type `https://www.google.com` and Press Enter?

A page appearing in a browser looks immediate, but it is the result of several
network and server-side systems cooperating. The path begins with a name and
ends with pixels, after DNS resolution, a TCP connection, a TLS handshake,
security checks, request routing, application work, and usually data access.

## 1. The browser prepares the request

The browser parses the URL into a scheme (`https`), host (`www.google.com`),
and default port (`443`). It may first consult its HTTP cache, service workers,
HSTS rules, and an existing connection pool. If a fresh network request is
needed, the browser must discover an IP address for the host.

## 2. The DNS request finds an IP address

DNS translates the human-readable hostname into an IP address. The browser
and operating system check their DNS caches first. On a miss, the machine asks
its configured recursive resolver, commonly supplied by a router, ISP, or
public DNS provider.

If the resolver also lacks a cached answer, it follows the DNS hierarchy: a
root name server points it to the `.com` top-level-domain servers, and a `.com`
server points it to Google's authoritative name servers. The authoritative
server returns an `A` record for IPv4, an `AAAA` record for IPv6, or possibly a
chain involving a `CNAME`. Each answer has a TTL that controls caching. The
resolver returns a suitable server IP address to the client.

## 3. TCP/IP carries packets to the server

IP is responsible for addressing and routing packets across networks. The
client selects a route to the returned server IP, resolves the local next-hop
MAC address when necessary, and sends packets through routers toward the
destination.

For HTTPS over HTTP/1.1 or HTTP/2, the browser normally establishes a TCP
connection to server port 443. TCP's three-way handshake exchanges `SYN`,
`SYN-ACK`, and `ACK` packets. It creates an ordered, reliable byte stream and
handles lost packets, flow control, and congestion control. A modern service
may instead negotiate HTTP/3, which uses QUIC over UDP, but the same high-level
request path still needs secure transport and server routing.

## 4. The firewall evaluates the connection

Firewalls can exist on the client, network edge, cloud platform, load
balancer, and destination host. Rules inspect properties such as source and
destination address, protocol, connection state, and destination port. The
public edge should allow legitimate HTTPS traffic on TCP port 443 while
rejecting disallowed traffic. Web application firewalls may later inspect the
HTTP request itself for malicious patterns, abuse, or policy violations.

## 5. HTTPS and SSL/TLS secure the session

Before sending private HTTP data, the browser and server perform a TLS
handshake. Although people still say "SSL," current HTTPS uses TLS. The server
presents a certificate containing its identity and public key information.
The browser checks the hostname, validity period, signature chain, and trust
anchor, and may check revocation information.

The peers negotiate a protocol version and cipher suite, establish shared
session keys, and confirm that the handshake was not altered. Public-key
cryptography authenticates and helps establish secrets; efficient symmetric
encryption then protects application data. TLS provides confidentiality and
integrity between the browser and the TLS endpoint. ALPN commonly selects
HTTP/2 or HTTP/1.1 during this process.

## 6. The browser sends the HTTP request

The encrypted channel carries a request resembling `GET / HTTP/2`, together
with headers such as `Host`, accepted content types, language preferences,
cookies, and user-agent information. The server side decrypts it at the TLS
endpoint and passes the request through the serving stack.

## 7. The load balancer chooses a healthy backend

A large site exposes multiple servers behind one public address. A load
balancer accepts the client connection, may terminate TLS, applies routing and
health information, and selects a healthy backend. Its algorithm might use
round robin, least connections, geographic proximity, latency, consistent
hashing, or weighted capacity. It can also provide failover and keep unhealthy
instances out of rotation.

The load balancer forwards the request to a web server, sometimes over a new
encrypted internal connection. Request metadata such as the original client
IP and protocol may travel in trusted forwarding headers.

## 8. The web server handles HTTP concerns

A web server such as Nginx or Apache parses HTTP, enforces size and timeout
limits, serves static assets, performs compression, and applies routing rules.
It may return a cached resource immediately. Dynamic requests are proxied to
an application server, often through HTTP or a language-specific gateway.

## 9. The application server runs product logic

The application server executes the code that understands the requested
resource. It validates input, authenticates the user when relevant, applies
authorization and business rules, calls internal services, and builds the
response. Application instances are commonly kept stateless so the load
balancer can send successive requests to different healthy workers.

## 10. The database supplies persistent data

If the response depends on stored information, the application queries a
database. A connection pool avoids opening a new database connection for every
request. The database parses and plans the query, uses indexes to locate rows,
and coordinates concurrent access and transactions. Replicas, distributed
caches, and sharding may reduce latency or spread load, but the application
must still handle stale data and failures correctly.

The database returns rows to the application server, which converts them into
HTML, JSON, or another representation. The result travels back through the web
server and load balancer, is encrypted by TLS, divided into transport packets,
and routed over IP to the browser.

## 11. The browser renders the result

The browser validates and decrypts received records, processes the HTTP
response, and follows caching and security headers. For HTML it builds a DOM;
CSS becomes a CSSOM; JavaScript may update both. The rendering engine creates
the render tree, calculates layout, paints layers, and composites them on the
screen. References to CSS, JavaScript, fonts, and images cause additional
requests that repeat much of the same network path, often reusing an existing
secure connection.

The short action of pressing Enter therefore crosses several boundaries: DNS
answers *where*, IP and TCP carry bytes reliably, the firewall decides what is
allowed, TLS protects the exchange, the load balancer selects capacity, the
web and application servers execute the request, and the database supplies
persistent state before the browser can finally draw the page.
