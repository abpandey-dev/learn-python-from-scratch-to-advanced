from lib import *
import bisect
import heapq
import math
import zlib

TOPIC(
    id="load-balancing", title="Load Balancing, Routing & CDNs", glyph="⇉",
    blurb="Spread traffic and survive failures: round robin, weighted and least-connections balancing, sticky hashing, consistent hashing with virtual nodes, health checks, power of two choices, path routing, DNS TTLs, CDN hit ratios, geo routing, autoscaling, rolling and blue/green deploys, and regional failover.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">round robin: server = i % n            least connections: pick min(active)
hash(key) % n   → adding a server moves ~all keys
consistent hash ring: key → first server clockwise; adding one moves ~1/n keys
health check: out after k failures, back after m successes
desired = ceil(current × metric / target)       # target-tracking autoscaling
CDN: origin load = requests × (1 − hit ratio)</code></pre>
""")

H = lambda s: zlib.crc32(s.encode())


Q(None, "Round Robin", "Easy", "The simplest balancer",
  "Assign requests in order to servers in turn. Return the server for each request.",
  [((["a", "b", "c"], 7), ['a', 'b', 'c', 'a', 'b', 'c', 'a'])],
  ("A counter that wraps around.", "O(r)", "O(r)"),
  ("Index with <code>i % n</code>.", "O(r)", "O(r)"),
  viz=((["a", "b", "c"], 5)))


@B
def round_robin(servers, requests):
    out, i = [], 0
    for _ in range(requests):
        out.append(servers[i])
        i += 1
        if i == len(servers):
            i = 0
    return out


@O
def round_robin(servers, requests):
    return [servers[i % len(servers)] for i in range(requests)]


Q(None, "Weighted Round Robin", "Medium", "Bigger servers get more",
  "Smooth weighted round robin (as nginx does): each turn, add every server's weight to its current score, pick the highest (first on ties), then subtract the total weight from the winner. Return the order of picks.",
  [(({"a": 5, "b": 1, "c": 1}, 7), ['a', 'a', 'b', 'a', 'c', 'a', 'a']), (({"big": 3, "small": 1}, 8), ['big', 'big', 'small', 'big', 'big', 'big', 'small', 'big'])],
  ("Track scores in a dict.", "O(r · n)", "O(n)"),
  ("Same algorithm with <code>max</code> over the scores.", "O(r · n)", "O(n)"),
  viz=(({"a": 5, "b": 1, "c": 1}, 7)))


@B
def weighted_rr(weights, requests):
    current = {s: 0 for s in weights}
    total = sum(weights.values())
    out = []
    for _ in range(requests):
        best = None
        for s, w in weights.items():
            current[s] += w
            if best is None or current[s] > current[best]:
                best = s
        current[best] -= total
        out.append(best)
    return out


@O
def weighted_rr(weights, requests):
    current, total, out = dict.fromkeys(weights, 0), sum(weights.values()), []
    for _ in range(requests):
        for s in weights:
            current[s] += weights[s]
        best = max(weights, key=current.get)
        current[best] -= total
        out.append(best)
    return out


Q(None, "Least Connections", "Medium", "Send work to the least busy",
  "Requests arrive one per second (at t = 0, 1, 2, …) and take <code>durations[i]</code> seconds. Each goes to the server with the fewest active requests at that moment (lowest index on ties). Return the server index chosen for each request.",
  [(([10, 1, 1, 1, 1, 10, 1], 2), [0, 1, 1, 1, 1, 1, 0])],
  ("For each request, count active requests per server by scanning.", "O(r²)", "O(r)"),
  ("Keep each server's finish times in a min-heap and pop the finished ones.", "O(r log r)", "O(r)"),
  viz=([10, 1, 1, 1], 2))


@B
def least_conn(durations, n):
    busy = [[] for _ in range(n)]
    out = []
    for t, d in enumerate(durations):
        active = [sum(1 for end in busy[s] if end > t) for s in range(n)]
        s = active.index(min(active))
        busy[s].append(t + d)
        out.append(s)
    return out


@O
def least_conn(durations, n):
    ends = [[] for _ in range(n)]
    out = []
    for t, d in enumerate(durations):
        for h in ends:
            while h and h[0] <= t:
                heapq.heappop(h)
        s = min(range(n), key=lambda i: len(ends[i]))
        heapq.heappush(ends[s], t + d)
        out.append(s)
    return out


Q(None, "Sticky Routing by Client IP", "Easy", "Same client, same server",
  "Route each client IP to <code>servers[crc32(ip) % n]</code>. Return the mapping, and how many of the clients move if one server is added at the end.",
  [((["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4", "10.0.0.5", "10.0.0.6"], ["s1", "s2", "s3"]), ({'10.0.0.1': 's3', '10.0.0.2': 's3', '10.0.0.3': 's3', '10.0.0.4': 's1', '10.0.0.5': 's3', '10.0.0.6': 's3'}, 4))],
  ("Loop twice: before and after.", "O(c)", "O(c)"),
  ("Comprehensions with the hash helper <code>H</code>.", "O(c)", "O(c)"),
  viz=((["10.0.0.1", "10.0.0.2"], ["s1", "s2", "s3"])))


@B
def ip_hash(ips, servers):
    before, moved = {}, 0
    bigger = servers + ["s_new"]
    for ip in ips:
        before[ip] = servers[zlib.crc32(ip.encode()) % len(servers)]
        if bigger[zlib.crc32(ip.encode()) % len(bigger)] != before[ip]:
            moved += 1
    return (before, moved)


@O
def ip_hash(ips, servers):
    bigger = servers + ["s_new"]
    before = {ip: servers[H(ip) % len(servers)] for ip in ips}
    return (before, sum(bigger[H(ip) % len(bigger)] != before[ip] for ip in ips))


Q(None, "Consistent Hashing Lookup", "Medium", "The hash ring",
  "Place each server on a ring at position crc32(name). A key goes to the first server at or after crc32(key) going clockwise (wrapping around). Return the server for each key.",
  [((["cache-a", "cache-b", "cache-c"], ["user:1", "user:2", "user:3", "photo:9", "cart:7"]), {'user:1': 'cache-c', 'user:2': 'cache-b', 'user:3': 'cache-b', 'photo:9': 'cache-c', 'cart:7': 'cache-b'})],
  ("For each key scan all servers for the smallest position ≥ the key's (else the smallest overall).", "O(k · n)", "O(n)"),
  ("Sort positions once and use <code>bisect</code>.", "O((n + k) log n)", "O(n)"),
  viz=((["cache-a", "cache-b", "cache-c"], ["user:1", "photo:9"])))


@B
def ring_lookup(servers, keys):
    out = {}
    for k in keys:
        hk = zlib.crc32(k.encode())
        best = None
        for s in servers:
            hs = zlib.crc32(s.encode())
            if hs >= hk and (best is None or hs < zlib.crc32(best.encode())):
                best = s
        if best is None:
            best = min(servers, key=lambda s: zlib.crc32(s.encode()))
        out[k] = best
    return out


@O
def ring_lookup(servers, keys):
    ring = sorted((H(s), s) for s in servers)
    pos = [p for p, _ in ring]
    return {k: ring[bisect.bisect_left(pos, H(k)) % len(ring)][1] for k in keys}


Q(None, "Why Consistent Hashing Moves Fewer Keys", "Hard", "Virtual nodes",
  "With 4 servers and <code>vnodes</code> virtual nodes each (positions crc32(f'{server}#{i}')), add a fifth server. Compare with mod-N hashing (crc32(key) % servers). Return <code>(% keys moved with mod-N, % moved with the ring)</code> for keys 'key0' … 'key{n−1}', rounded to 1.",
  [((2000, 50), (79.5, 19.9))],
  ("Build both mappings in loops and count differences.", "O(k · v)", "O(v)"),
  ("A sorted ring with <code>bisect</code>.", "O(k log v)", "O(v)"),
  viz=(200, 10))


@B
def keys_moved(n, vnodes):
    def ring(servers):
        pts = []
        for s in servers:
            for i in range(vnodes):
                pts.append((zlib.crc32(f"{s}#{i}".encode()), s))
        return sorted(pts)

    def owner(pts, k):
        hk = zlib.crc32(k.encode())
        for p, s in pts:
            if p >= hk:
                return s
        return pts[0][1]
    old, new = ["s0", "s1", "s2", "s3"], ["s0", "s1", "s2", "s3", "s4"]
    r_old, r_new = ring(old), ring(new)
    mod_moved = ring_moved = 0
    for i in range(n):
        k = f"key{i}"
        h = zlib.crc32(k.encode())
        mod_moved += old[h % 4] != new[h % 5]
        ring_moved += owner(r_old, k) != owner(r_new, k)
    return (round(mod_moved / n * 100, 1), round(ring_moved / n * 100, 1))


@O
def keys_moved(n, vnodes):
    def make(servers):
        pts = sorted((H(f"{s}#{i}"), s) for s in servers for i in range(vnodes))
        return [p for p, _ in pts], [s for _, s in pts]

    def owner(ring, k):
        pos, names = ring
        return names[bisect.bisect_left(pos, H(k)) % len(pos)]
    old, new = [f"s{i}" for i in range(4)], [f"s{i}" for i in range(5)]
    ro, rn = make(old), make(new)
    keys = [f"key{i}" for i in range(n)]
    mod = sum(old[H(k) % 4] != new[H(k) % 5] for k in keys)
    rng = sum(owner(ro, k) != owner(rn, k) for k in keys)
    return (round(mod / n * 100, 1), round(rng / n * 100, 1))


Q(None, "Health Checks With Hysteresis", "Medium", "Don't flap",
  "A balancer marks a server down after <code>fail_n</code> consecutive failed checks and back up after <code>ok_n</code> consecutive passes. It starts up. Given check results (True = pass), return the status after each check ('up' / 'down').",
  [(([True, False, False, True, False, False, False, True, True, False, True, True, True], 3, 2), ['up', 'up', 'up', 'up', 'up', 'up', 'down', 'down', 'up', 'up', 'up', 'up', 'up'])],
  ("Two counters and an if-chain.", "O(c)", "O(c)"),
  ("Same state machine, written compactly.", "O(c)", "O(c)"),
  viz=([True, False, False, False, True, True], 3, 2))


@B
def health(checks, fail_n, ok_n):
    status, fails, oks, out = "up", 0, 0, []
    for ok in checks:
        if ok:
            oks += 1
            fails = 0
        else:
            fails += 1
            oks = 0
        if status == "up" and fails >= fail_n:
            status = "down"
        elif status == "down" and oks >= ok_n:
            status = "up"
        out.append(status)
    return out


@O
def health(checks, fail_n, ok_n):
    status, run, out = "up", 0, []
    for i, ok in enumerate(checks):
        run = run + 1 if i and checks[i - 1] == ok else 1
        if status == "up" and not ok and run >= fail_n:
            status = "down"
        elif status == "down" and ok and run >= ok_n:
            status = "up"
        out.append(status)
    return out


Q(None, "Fail Over to a Healthy Server", "Easy", "Skip the dead ones",
  "Route each request round-robin, but skip servers marked down (try the next one). Return the server per request, or None if all are down.",
  [((["a", "b", "c", "d"], {"b", "d"}, 5), ['a', 'c', 'a', 'c', 'a']), ((["a", "b"], {"a", "b"}, 2), [None, None])],
  ("Advance the pointer until an up server is found.", "O(r · n)", "O(r)"),
  ("Filter healthy servers once, then index.", "O(r + n)", "O(n)"),
  viz=((["a", "b", "c", "d"], {"b", "d"}, 5)))


@B
def failover(servers, down, requests):
    out, i = [], 0
    for _ in range(requests):
        chosen = None
        for _ in range(len(servers)):
            s = servers[i % len(servers)]
            i += 1
            if s not in down:
                chosen = s
                break
        out.append(chosen)
    return out


@O
def failover(servers, down, requests):
    healthy = [s for s in servers if s not in down]
    return [healthy[i % len(healthy)] if healthy else None for i in range(requests)]


Q(None, "Power of Two Choices", "Medium", "Nearly optimal, almost free",
  "For each request you sample two servers (given as <code>pairs</code>) and send it to the one with fewer requests so far (the first on ties). Compare with sending to only the first sample. Return <code>(max load with one choice, max load with two choices)</code>.",
  [(([(0, 1), (0, 2), (0, 3), (1, 0), (0, 2), (0, 1), (3, 0), (0, 2), (1, 3), (0, 2), (2, 1), (0, 3)], 4), (8, 3))],
  ("Two simulations with load lists.", "O(r)", "O(n)"),
  ("Same, with <code>min</code> over the pair.", "O(r)", "O(n)"),
  viz=([(0, 1), (0, 2), (0, 3), (1, 0)], 4))


@B
def two_choices(pairs, n):
    one, two = [0] * n, [0] * n
    for a, b in pairs:
        one[a] += 1
        if two[b] < two[a]:
            two[b] += 1
        else:
            two[a] += 1
    return (max(one), max(two))


@O
def two_choices(pairs, n):
    one, two = [0] * n, [0] * n
    for a, b in pairs:
        one[a] += 1
        two[min((a, b), key=lambda s: two[s])] += 1
    return (max(one), max(two))


ROUTES = {"/api/": "api-pool", "/api/v2/": "api-v2-pool", "/static/": "cdn-origin", "/": "web-pool"}


Q(None, "Route by Path (Layer 7)", "Easy", "Longest prefix wins",
  "An L7 load balancer routes by URL path: pick the backend whose prefix in <code>ROUTES</code> is the longest one the path starts with.",
  [((["/api/users/7", "/api/v2/orders", "/static/logo.png", "/about"],), ['api-pool', 'api-v2-pool', 'cdn-origin', 'web-pool'])],
  ("Check every prefix and keep the longest match.", "O(p · r)", "O(1)"),
  ("<code>max</code> over the matching prefixes by length.", "O(p · r)", "O(1)"),
  viz=((["/api/v2/orders", "/about"],)))


@B
def route_path(paths):
    out = []
    for p in paths:
        best = ""
        for prefix in ROUTES:
            if p.startswith(prefix) and len(prefix) > len(best):
                best = prefix
        out.append(ROUTES[best])
    return out


@O
def route_path(paths):
    return [ROUTES[max((r for r in ROUTES if p.startswith(r)), key=len)] for p in paths]


Q(None, "How Long Until DNS Changes Everywhere?", "Easy", "TTLs",
  "You change a DNS record at time 0. Resolvers cached it at the given times (seconds before the change) with TTL <code>ttl</code>. Return the time (seconds after the change) when the last resolver's cache expires. Lower TTLs before planned migrations.",
  [(([5, 120, 299, 30], 300), 295), (([5, 20], 60), 55)],
  ("For each, remaining = ttl − age; take the max.", "O(n)", "O(1)"),
  ("<code>max</code> over a generator.", "O(n)", "O(1)"),
  viz=([5, 120, 299], 300))


@B
def dns_settle(ages, ttl):
    worst = 0
    for a in ages:
        remaining = ttl - a
        if remaining > worst:
            worst = remaining
    return worst


@O
def dns_settle(ages, ttl):
    return max(0, max(ttl - a for a in ages))


Q(None, "CDN Hit Ratio and Origin Load", "Medium", "Edge caching",
  "Requests for objects arrive as <code>(time_s, object)</code>. The CDN edge keeps each object for <code>ttl</code> seconds after fetching it from the origin. Return <code>(origin fetches, hit ratio %)</code> rounded to 1.",
  [(([(0, "a"), (1, "a"), (2, "b"), (30, "a"), (61, "a"), (62, "b"), (70, "b")], 60), (4, 42.9))],
  ("Track each object's fetch time in a dict.", "O(r)", "O(o)"),
  ("Same, with <code>dict.get</code> and a default of −∞.", "O(r)", "O(o)"),
  viz=([(0, "a"), (1, "a"), (61, "a")], 60))


@B
def cdn(requests, ttl):
    fetched, misses = {}, 0
    for t, obj in requests:
        if obj not in fetched or t - fetched[obj] >= ttl:
            misses += 1
            fetched[obj] = t
    return (misses, round((1 - misses / len(requests)) * 100, 1))


@O
def cdn(requests, ttl):
    fetched, misses = {}, 0
    for t, obj in requests:
        if t - fetched.get(obj, -math.inf) >= ttl:
            misses, fetched[obj] = misses + 1, t
    return (misses, round((1 - misses / len(requests)) * 100, 1))


Q(None, "Does the CDN Speed Things Up?", "Easy", "Weighted latency",
  "A hit at the edge takes <code>edge_ms</code>; a miss goes to the origin and takes <code>origin_ms</code>. Return the average latency (ms, rounded to 1) for each hit ratio in <code>ratios</code>.",
  [((20, 180, [0.0, 0.5, 0.9, 0.98]), [180.0, 100.0, 36.0, 23.2])],
  ("A weighted average in a loop.", "O(n)", "O(n)"),
  ("A comprehension.", "O(n)", "O(n)"),
  viz=(20, 180, [0.5, 0.9]))


@B
def cdn_latency(edge, origin, ratios):
    out = []
    for h in ratios:
        out.append(round(h * edge + (1 - h) * origin, 1))
    return out


@O
def cdn_latency(edge, origin, ratios):
    return [round(origin - h * (origin - edge), 1) for h in ratios]


REGIONS = {"mumbai": (19.08, 72.88), "singapore": (1.35, 103.82), "frankfurt": (50.11, 8.68), "virginia": (38.95, -77.45)}


Q(None, "Send Users to the Nearest Region", "Medium", "Geo routing",
  "Route each user (lat, lon) to the closest region in <code>REGIONS</code> by great-circle (haversine) distance. Return the region per user.",
  [(([(28.6, 77.2), (51.5, -0.13), (40.7, -74.0), (-33.9, 151.2)],), ['mumbai', 'frankfurt', 'virginia', 'singapore'])],
  ("Haversine by hand for every region.", "O(u · r)", "O(1)"),
  ("A haversine helper and <code>min</code>.", "O(u · r)", "O(1)"),
  viz=(([(28.6, 77.2), (51.5, -0.13)],)))


@B
def nearest_region(users):
    out = []
    for lat, lon in users:
        best, best_d = None, None
        for name, (rlat, rlon) in REGIONS.items():
            p1, p2 = math.radians(lat), math.radians(rlat)
            dp, dl = p2 - p1, math.radians(rlon - lon)
            a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
            d = 2 * 6371 * math.asin(math.sqrt(a))
            if best_d is None or d < best_d:
                best, best_d = name, d
        out.append(best)
    return out


@O
def nearest_region(users):
    def km(a, b):
        p1, p2 = map(math.radians, (a[0], b[0]))
        h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(b[1] - a[1]) / 2) ** 2
        return 2 * 6371 * math.asin(math.sqrt(h))
    return [min(REGIONS, key=lambda r: km(u, REGIONS[r])) for u in users]


Q(None, "Autoscaling by Target Tracking", "Medium", "Scale on a metric",
  "Every minute, desired = ⌈current × cpu / target⌉, clamped to [<code>lo</code>, <code>hi</code>]. Scale-in (shrinking) only happens if at least <code>cooldown</code> minutes passed since the last change; scale-out is immediate. Return the instance count after each minute.",
  [(([40, 85, 90, 70, 30, 25, 20, 20], 4, 60, 2, 20, 2), [3, 5, 8, 10, 10, 5, 5, 2])],
  ("Simulate minute by minute.", "O(m)", "O(m)"),
  ("Same simulation, compact.", "O(m)", "O(m)"),
  viz=([40, 85, 30, 20], 4, 60, 2, 20, 2))


@B
def autoscale(cpu, start, target, lo, hi, cooldown):
    n, last_change, out = start, -10 ** 9, []
    for minute, c in enumerate(cpu):
        desired = math.ceil(n * c / target)
        if desired < lo:
            desired = lo
        if desired > hi:
            desired = hi
        if desired > n or (desired < n and minute - last_change >= cooldown):
            if desired != n:
                last_change = minute
            n = desired
        out.append(n)
    return out


@O
def autoscale(cpu, n, target, lo, hi, cooldown):
    last, out = -10 ** 9, []
    for m, c in enumerate(cpu):
        d = min(hi, max(lo, math.ceil(n * c / target)))
        if d > n or (d < n and m - last >= cooldown):
            n, last = d, m
        out.append(n)
    return out


Q(None, "Rolling Deploy Batches", "Easy", "Keep capacity during a release",
  "Update servers in batches so that at least <code>min_pct</code>% stay serving. Return <code>(largest batch size, number of batches)</code> for <code>n</code> servers.",
  [((20, 75), (5, 4)), ((7, 90), (1, 7))],
  ("Grow the batch while capacity stays above the floor.", "O(n)", "O(1)"),
  ("Floor arithmetic, at least 1 per batch.", "O(1)", "O(1)"),
  viz=(20, 75))


@B
def rolling(n, min_pct):
    batch = 1
    while (n - (batch + 1)) / n * 100 >= min_pct:
        batch += 1
    batches = n // batch + (1 if n % batch else 0)
    return (batch, batches)


@O
def rolling(n, min_pct):
    batch = max(1, math.floor(round(n * (100 - min_pct) / 100, 9)))
    return (batch, math.ceil(n / batch))


Q(None, "Shift Traffic Blue → Green", "Easy", "Progressive rollout",
  "Move traffic to the new (green) version in steps of <code>pcts</code>%. At each step, if the green error rate exceeds <code>max_err</code>, roll back to 0% and stop. Return the green % after each step that ran.",
  [(([1, 5, 25, 50, 100], [0.1, 0.2, 0.3, 0.2, 0.1], 1.0), [1, 5, 25, 50, 100]), (([1, 5, 25, 50, 100], [0.1, 0.2, 2.5, 0.2, 0.1], 1.0), [1, 5, 0])],
  ("A loop with an early stop.", "O(s)", "O(s)"),
  ("<code>zip</code> and a for-else.", "O(s)", "O(s)"),
  viz=([1, 5, 25], [0.1, 2.5, 0.1], 1.0))


@B
def blue_green(pcts, errs, max_err):
    out = []
    for i in range(len(pcts)):
        if errs[i] > max_err:
            out.append(0)
            break
        out.append(pcts[i])
    return out


@O
def blue_green(pcts, errs, max_err):
    out = []
    for p, e in zip(pcts, errs):
        out.append(0 if e > max_err else p)
        if e > max_err:
            break
    return out


Q(None, "Fail Over Between Regions", "Medium", "Global traffic management",
  "Each user has a region preference list (nearest first). Send them to the first healthy region. Return <code>{user: region or 'unavailable'}</code> and the count per region.",
  [(({"u1": ["mumbai", "singapore"], "u2": ["frankfurt", "virginia"], "u3": ["mumbai", "frankfurt", "virginia"], "u4": ["singapore"]}, {"mumbai"}), ({'u1': 'singapore', 'u2': 'frankfurt', 'u3': 'frankfurt', 'u4': 'singapore'}, {'frankfurt': 2, 'singapore': 2}))],
  ("Loops with a found flag.", "O(u · r)", "O(u)"),
  ("<code>next</code> with a default, then a Counter.", "O(u · r)", "O(u)"),
  viz=({"u1": ["mumbai", "singapore"], "u4": ["singapore"]}, {"mumbai"}))


@B
def region_failover(prefs, down):
    route, counts = {}, {}
    for u, regions in prefs.items():
        chosen = "unavailable"
        for r in regions:
            if r not in down:
                chosen = r
                break
        route[u] = chosen
        counts[chosen] = counts.get(chosen, 0) + 1
    return (route, dict(sorted(counts.items())))


@O
def region_failover(prefs, down):
    from collections import Counter
    route = {u: next((r for r in rs if r not in down), "unavailable") for u, rs in prefs.items()}
    return (route, dict(sorted(Counter(route.values()).items())))


Q(None, "Drain Connections Before Removing a Server", "Easy", "Graceful shutdown",
  "Before removing a server, the balancer stops sending it new requests and waits up to <code>timeout</code> seconds for in-flight ones (given as seconds remaining). Return <code>(requests finished cleanly, requests cut off, seconds the drain took)</code>.",
  [(([0.2, 3.5, 12.0, 0.8, 45.0], 30), (4, 1, 30)), (([1.0, 2.0], 30), (2, 0, 2.0))],
  ("Count with a loop and track the longest finished request.", "O(n)", "O(1)"),
  ("Comprehensions and <code>min</code>.", "O(n)", "O(n)"),
  viz=([0.2, 3.5, 45.0], 30))


@B
def drain(remaining, timeout):
    done = cut = 0
    longest = 0
    for r in remaining:
        if r <= timeout:
            done += 1
            longest = max(longest, r)
        else:
            cut += 1
    took = timeout if cut else longest
    return (done, cut, took)


@O
def drain(remaining, timeout):
    done = [r for r in remaining if r <= timeout]
    cut = len(remaining) - len(done)
    return (len(done), cut, timeout if cut else max(done, default=0))


Q(None, "What Sticky Sessions Cost You", "Medium", "Stateless servers",
  "Users are pinned to servers, and each server keeps its users' sessions in memory. When server <code>dead</code> crashes, its users are logged out. Return <code>(users logged out, % of all users)</code> — then compare with storing sessions in a shared store such as Redis, where nobody is logged out.",
  [(({"u1": "s1", "u2": "s2", "u3": "s1", "u4": "s3", "u5": "s1", "u6": "s2"}, "s1"), (3, 50.0))],
  ("Count in a loop.", "O(u)", "O(1)"),
  ("<code>sum</code> over a generator.", "O(u)", "O(1)"),
  viz=({"u1": "s1", "u2": "s2", "u3": "s1"}, "s1"))


@B
def sticky_loss(assignment, dead):
    lost = 0
    for user, server in assignment.items():
        if server == dead:
            lost += 1
    return (lost, round(lost / len(assignment) * 100, 1))


@O
def sticky_loss(assignment, dead):
    lost = sum(s == dead for s in assignment.values())
    return (lost, round(lost / len(assignment) * 100, 1))
