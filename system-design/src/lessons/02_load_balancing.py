from lib import *
import bisect
import zlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LESSON("Basics", "Why load balancers exist", """
<p>One server has limits (CPU, memory, connections) and fails sometimes. A <b>load balancer</b> sits in front of many identical servers, spreads requests across them, and stops sending traffic to servers that fail health checks. This only works if servers are <b>stateless</b>: no user session kept in a server's memory — put sessions in a shared store (Redis, a database) or a signed cookie.</p>
<table>
<tr><th>Algorithm</th><th>How</th><th>Good for</th></tr>
<tr><td>Round robin</td><td>next server in turn</td><td>similar servers, similar requests</td></tr>
<tr><td>Weighted round robin</td><td>more turns for bigger servers</td><td>mixed server sizes, canaries</td></tr>
<tr><td>Least connections</td><td>fewest active requests</td><td>long or uneven requests</td></tr>
<tr><td>Power of two choices</td><td>sample two, pick the less loaded</td><td>large fleets, near-optimal and cheap</td></tr>
<tr><td>Hashing (IP / key)</td><td>same client → same server</td><td>caches, sticky needs</td></tr>
</table>
""", practice=["Round Robin", "Weighted Round Robin", "Least Connections", "Power of Two Choices", "What Sticky Sessions Cost You"])

LESSON("Core", "Layer 4 vs layer 7, and health checks", """
<p>An <b>L4</b> balancer routes TCP/UDP connections by IP and port — fast and protocol-agnostic. An <b>L7</b> balancer understands HTTP: it can route by path or header (<code>/api/v2/*</code> → new service), terminate TLS, retry, and rate-limit. Most web systems use L7 (nginx, Envoy, cloud application load balancers), often behind an L4 layer.</p>
<p><b>Health checks</b> probe each server; mark it down after several consecutive failures and back up after several passes (hysteresis), so a single blip doesn't make it flap in and out. When removing a server, <b>drain</b> it first: stop new requests and let in-flight ones finish.</p>
""", practice=["Route by Path (Layer 7)", "Health Checks With Hysteresis", "Fail Over to a Healthy Server", "Drain Connections Before Removing a Server"])

LESSON("Core", "Consistent hashing", """
<p>Caches and sharded stores need the same key to land on the same node. <code>hash(key) % N</code> works until N changes — then almost every key moves, and the cache empties. <b>Consistent hashing</b> places nodes on a ring of hash values; a key belongs to the first node clockwise from its hash. Adding or removing a node only moves the keys in that node's arc — about 1/N of them.</p>
<p>With only a few points, arcs are uneven; giving every node many <b>virtual nodes</b> (100+ points on the ring) evens out the load and lets bigger machines take more points. Used by Cassandra, DynamoDB, Memcached clients and many load balancers.</p>
""", practice=["Sticky Routing by Client IP", "Consistent Hashing Lookup", "Why Consistent Hashing Moves Fewer Keys"])


@LD
def ring_picture():
    import math
    servers = ["cache-a", "cache-b", "cache-c"]
    fig, ax = plt.subplots(figsize=(3.6, 3.6))
    ax.add_patch(plt.Circle((0, 0), 1, fill=False, color="#94a3b8"))
    colors = {"cache-a": "#0f766e", "cache-b": "#b45309", "cache-c": "#7c3aed"}
    for s in servers:
        for i in range(8):
            angle = zlib.crc32(f"{s}#{i}".encode()) / 2 ** 32 * 2 * math.pi
            ax.plot(math.cos(angle), math.sin(angle), "o", color=colors[s])
    for k in ["user:1", "user:2", "photo:9", "cart:7"]:
        angle = zlib.crc32(k.encode()) / 2 ** 32 * 2 * math.pi
        ax.plot(0.8 * math.cos(angle), 0.8 * math.sin(angle), "x", color="black")
    ax.set_aspect("equal"); ax.axis("off"); ax.set_title("3 servers × 8 virtual nodes; × = keys")


LESSON("Core", "DNS, CDNs and global traffic", """
<ul>
<li><b>DNS</b> maps names to IPs and is cached for its TTL — lower the TTL before a planned migration so the change spreads quickly.</li>
<li>A <b>CDN</b> caches static (and some dynamic) content at edge locations near users: lower latency and far less origin load. Origin load = requests × (1 − hit ratio), so going from a 90% to a 98% hit ratio cuts origin traffic five-fold.</li>
<li><b>Global load balancing</b> sends users to the nearest healthy region (geo-DNS or anycast) and fails over to the next region when one is down.</li>
</ul>
""", practice=["How Long Until DNS Changes Everywhere?", "CDN Hit Ratio and Origin Load", "Does the CDN Speed Things Up?", "Send Users to the Nearest Region", "Fail Over Between Regions"])

LESSON("Advanced", "Elasticity and safe releases", """
<ul>
<li><b>Autoscaling</b>: target tracking keeps a metric (CPU, requests per instance, queue depth) near a target by adding or removing instances; scale out fast, scale in slowly (cooldowns) to avoid oscillation.</li>
<li><b>Rolling deploys</b> replace servers in batches while keeping enough capacity serving.</li>
<li><b>Blue/green and canary</b> releases shift a small percentage of traffic to the new version first, watch error rates, and roll back instantly if they rise.</li>
</ul>
""", practice=["Autoscaling by Target Tracking", "Rolling Deploy Batches", "Shift Traffic Blue → Green"])
