from lib import *

THEORY("Where load balancing happens", """
<table>
<tr><th>Layer</th><th>Example</th><th>Decides by</th></tr>
<tr><td>DNS / global</td><td>geo-DNS, anycast</td><td>user location, region health</td></tr>
<tr><td>Edge</td><td>CDN</td><td>cache key, edge location</td></tr>
<tr><td>L4</td><td>network load balancer</td><td>IP and port</td></tr>
<tr><td>L7</td><td>nginx, Envoy, API gateway</td><td>path, headers, cookies</td></tr>
<tr><td>Client-side</td><td>service mesh, gRPC</td><td>service discovery + algorithm</td></tr>
</table>
""")

THEORY("Single points of failure", """
<p>A load balancer itself can fail, so run it in pairs (active-passive with a floating IP) or as a managed service spread across zones. Check every box in your diagram: if it has only one copy, it's a single point of failure — say how you'd remove it.</p>
""")

FAQ("Why should application servers be stateless?", "<p>So any server can handle any request: the balancer can spread load freely, servers can be added or removed at any time, and a crash doesn't lose user sessions. State lives in databases, caches or tokens.</p>")
FAQ("What problem does consistent hashing solve?", "<p>With hash mod N, changing N remaps almost every key. Consistent hashing remaps only about 1/N of keys when a node is added or removed, and virtual nodes keep the load balanced.</p>")
FAQ("L4 vs L7 load balancing?", "<p>L4 works on connections (IP, port) — fast and simple. L7 understands HTTP, so it can route by path or header, terminate TLS, retry, cache and rate-limit, at higher cost per request.</p>")
FAQ("How does a CDN help?", "<p>It serves cached content from locations close to users, cutting latency and origin load; it also absorbs traffic spikes and some attacks.</p>")
FAQ("What is connection draining?", "<p>Stopping new traffic to a server while letting in-flight requests finish before removing it, so deploys and scale-in don't fail live requests.</p>")
FAQ("How do you avoid autoscaling oscillation?", "<p>Scale out quickly but scale in slowly with cooldowns, use a target with headroom, and smooth the metric over a window.</p>")
