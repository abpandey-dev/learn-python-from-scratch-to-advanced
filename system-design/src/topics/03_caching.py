from lib import *
import math
from collections import Counter, OrderedDict, defaultdict
from urllib.parse import parse_qsl, urlencode, urlparse

TOPIC(
    id="caching", title="Caching", glyph="⚡",
    blurb="The fastest request is the one you don't make: eviction policies (LRU, LFU, FIFO, optimal), TTLs, cache-aside, write-through and write-back, stampedes and single-flight, jittered expiry, cache keys, invalidation, negative caching, two-level caches, hot keys, sizing and HTTP cache headers.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">cache-aside:   v = cache.get(k) or db.get(k); cache.set(k, v, ttl)     # app manages the cache
write-through: write db and cache together;  write-back: write cache, flush to db later
effective latency = hit × cache_ms + (1 − hit) × db_ms
DB load = requests × (1 − hit ratio)
stampede fix: single-flight lock per key, TTL jitter, serve stale while refreshing</code></pre>
<p>"There are only two hard things in computer science: cache invalidation and naming things."</p>
""")


Q(None, "An LRU Cache", "Medium", "Evict the least recently used",
  "Simulate an LRU cache of <code>capacity</code> keys over the <code>accesses</code>. Return <code>(hits, misses, keys left from least to most recent)</code>.",
  [((3, ["a", "b", "c", "a", "d", "b", "e", "a", "c"]), (1, 8, ['e', 'a', 'c'])), ((2, ["x", "x", "y", "x", "z", "y"]), (2, 4, ['z', 'y']))],
  ("A list ordered by recency: remove and re-append on each access (O(n) per access).", "O(a · c)", "O(c)"),
  ("<code>OrderedDict.move_to_end</code> and <code>popitem(last=False)</code> make every step O(1).", "O(a)", "O(c)"),
  viz=((3, ["a", "b", "c", "a", "d"])))


@B
def lru(capacity, accesses):
    order, hits, misses = [], 0, 0
    for k in accesses:
        if k in order:
            hits += 1
            order.remove(k)
        else:
            misses += 1
            if len(order) == capacity:
                order.pop(0)
        order.append(k)
    return (hits, misses, order)


@O
def lru(capacity, accesses):
    cache, hits = OrderedDict(), 0
    for k in accesses:
        if k in cache:
            hits += 1
            cache.move_to_end(k)
        else:
            if len(cache) == capacity:
                cache.popitem(last=False)
            cache[k] = True
    return (hits, len(accesses) - hits, list(cache))


Q(None, "An LFU Cache", "Medium", "Evict the least frequently used",
  "Simulate an LFU cache: on a miss with a full cache, evict the key used the fewest times (ties: the one used least recently). Return the evicted keys in order.",
  [((2, ["a", "a", "b", "c", "b", "b", "d", "c"]), ['b', 'c', 'a', 'd'])],
  ("Track counts and last-use times; scan for the victim.", "O(a · c)", "O(c)"),
  ("<code>min</code> with a (count, last_used) key.", "O(a · c)", "O(c)"),
  viz=((2, ["a", "a", "b", "c", "b"])))


@B
def lfu_evictions(capacity, accesses):
    count, last, evicted = {}, {}, []
    for t, k in enumerate(accesses):
        if k not in count and len(count) == capacity:
            victim = None
            for key in count:
                if victim is None or count[key] < count[victim] or (count[key] == count[victim] and last[key] < last[victim]):
                    victim = key
            del count[victim]
            del last[victim]
            evicted.append(victim)
        count[k] = count.get(k, 0) + 1
        last[k] = t
    return evicted


@O
def lfu_evictions(capacity, accesses):
    count, last, evicted = {}, {}, []
    for t, k in enumerate(accesses):
        if k not in count and len(count) == capacity:
            victim = min(count, key=lambda x: (count[x], last[x]))
            del count[victim], last[victim]
            evicted.append(victim)
        count[k], last[k] = count.get(k, 0) + 1, t
    return evicted


Q(None, "FIFO vs LRU", "Medium", "Policy matters",
  "Compare hit ratios (%) of FIFO (evict the oldest inserted) and LRU on the same access pattern and capacity. Round to 1.",
  [((3, ["home", "a", "home", "b", "home", "c", "home", "d", "home", "a"]), (30.0, 40.0))],
  ("Two list-based simulations.", "O(a · c)", "O(c)"),
  ("A deque for FIFO and an OrderedDict for LRU.", "O(a)", "O(c)"),
  viz=((3, ["home", "a", "home", "b", "home", "c"])))


@B
def fifo_vs_lru(capacity, accesses):
    fifo, f_hits = [], 0
    for k in accesses:
        if k in fifo:
            f_hits += 1
        else:
            if len(fifo) == capacity:
                fifo.pop(0)
            fifo.append(k)
    lru_list, l_hits = [], 0
    for k in accesses:
        if k in lru_list:
            l_hits += 1
            lru_list.remove(k)
        elif len(lru_list) == capacity:
            lru_list.pop(0)
        lru_list.append(k)
    n = len(accesses)
    return (round(f_hits / n * 100, 1), round(l_hits / n * 100, 1))


@O
def fifo_vs_lru(capacity, accesses):
    from collections import deque
    fifo, f_hits = deque(), 0
    for k in accesses:
        if k in fifo:
            f_hits += 1
        else:
            if len(fifo) == capacity:
                fifo.popleft()
            fifo.append(k)
    cache, l_hits = OrderedDict(), 0
    for k in accesses:
        if k in cache:
            l_hits += 1
            cache.move_to_end(k)
        else:
            if len(cache) == capacity:
                cache.popitem(last=False)
            cache[k] = 1
    n = len(accesses)
    return (round(f_hits / n * 100, 1), round(l_hits / n * 100, 1))


Q(None, "A Cache With Expiry", "Easy", "TTL",
  "Process operations <code>('set', t, key, value, ttl)</code> and <code>('get', t, key)</code>. A value expires once t ≥ set time + ttl. Return the results of the gets (None when missing or expired).",
  [(([("set", 0, "price", 100, 10), ("get", 5, "price"), ("get", 10, "price"), ("set", 12, "price", 120, 10), ("get", 15, "price"), ("get", 15, "stock")],), [100, None, 120, None])],
  ("A dict of (value, expires_at) with if-checks.", "O(n)", "O(k)"),
  ("Same, with a conditional expression on the lookup.", "O(n)", "O(k)"),
  viz=(([("set", 0, "price", 100, 10), ("get", 5, "price"), ("get", 10, "price")],)))


@B
def ttl_cache(ops):
    store, out = {}, []
    for op in ops:
        if op[0] == "set":
            _, t, k, v, ttl = op
            store[k] = (v, t + ttl)
        else:
            _, t, k = op
            if k in store and t < store[k][1]:
                out.append(store[k][0])
            else:
                out.append(None)
    return out


@O
def ttl_cache(ops):
    store, out = {}, []
    for op in ops:
        if op[0] == "set":
            store[op[2]] = (op[3], op[1] + op[4])
        else:
            v, exp = store.get(op[2], (None, -math.inf))
            out.append(v if op[1] < exp else None)
    return out


Q(None, "Cache-Aside and the Stale Read", "Medium", "Forgetting to invalidate",
  "Reads use cache-aside (check cache, else read DB and fill the cache). Writes update the DB, and also delete the cache entry only if <code>invalidate</code> is True. Return <code>(DB reads, reads that returned a stale value)</code>.",
  [(([("r", "x"), ("r", "x"), ("w", "x", 2), ("r", "x"), ("r", "y"), ("w", "y", 5), ("r", "y")], {"x": 1, "y": 9}, False), (2, 2)),
   (([("r", "x"), ("r", "x"), ("w", "x", 2), ("r", "x"), ("r", "y"), ("w", "y", 5), ("r", "y")], {"x": 1, "y": 9}, True), (4, 0))],
  ("Two dicts and if-statements.", "O(n)", "O(k)"),
  ("Same with <code>dict.pop</code> for the delete.", "O(n)", "O(k)"),
  viz=(([("r", "x"), ("w", "x", 2), ("r", "x")], {"x": 1}, False)))


@B
def cache_aside(ops, db, invalidate):
    db, cache = dict(db), {}
    db_reads = stale = 0
    for op in ops:
        if op[0] == "r":
            k = op[1]
            if k in cache:
                value = cache[k]
            else:
                db_reads += 1
                value = db[k]
                cache[k] = value
            if value != db[k]:
                stale += 1
        else:
            db[op[1]] = op[2]
            if invalidate and op[1] in cache:
                del cache[op[1]]
    return (db_reads, stale)


@O
def cache_aside(ops, db, invalidate):
    db, cache, db_reads, stale = dict(db), {}, 0, 0
    for op in ops:
        if op[0] == "w":
            db[op[1]] = op[2]
            if invalidate:
                cache.pop(op[1], None)
            continue
        if op[1] not in cache:
            db_reads += 1
            cache[op[1]] = db[op[1]]
        stale += cache[op[1]] != db[op[1]]
    return (db_reads, stale)


Q(None, "Write-Through or Write-Back?", "Medium", "Counting database writes",
  "A cache of unlimited size receives writes <code>(key, value)</code>. Write-through writes every update to the DB immediately. Write-back only marks the key dirty and writes the latest value when <code>flush</code> happens at the given write indexes (after that write) and at the end. Return <code>(DB writes write-through, DB writes write-back)</code>.",
  [(([("a", 1), ("a", 2), ("b", 1), ("a", 3), ("b", 2), ("a", 4)], [2]), (6, 4))],
  ("Count each write; track a dirty set and flush it.", "O(n)", "O(k)"),
  ("Same, with set operations.", "O(n)", "O(k)"),
  viz=(([("a", 1), ("a", 2), ("b", 1)], [1])))


@B
def write_policies(writes, flush_at):
    through = len(writes)
    dirty, back = set(), 0
    for i, (k, v) in enumerate(writes):
        dirty.add(k)
        if i in flush_at:
            back += len(dirty)
            dirty = set()
    back += len(dirty)
    return (through, back)


@O
def write_policies(writes, flush_at):
    dirty, back = set(), 0
    for i, (k, _) in enumerate(writes):
        dirty.add(k)
        if i in flush_at:
            back, dirty = back + len(dirty), set()
    return (len(writes), back + len(dirty))


Q(None, "What a Hit Ratio Buys You", "Easy", "Latency and DB load",
  "For each hit ratio, return <code>(average latency ms rounded to 2, DB QPS rounded)</code> given <code>qps</code>, cache latency <code>cache_ms</code> and DB latency <code>db_ms</code> (a miss pays both).",
  [((50000, 0.5, 8, [0.0, 0.8, 0.95, 0.99]), [(8.5, 50000), (2.1, 10000), (0.9, 2500), (0.58, 500)])],
  ("A loop.", "O(n)", "O(n)"),
  ("A comprehension.", "O(n)", "O(n)"),
  viz=((50000, 0.5, 8, [0.8, 0.99])))


@B
def hit_ratio_effect(qps_, cache_ms, db_ms, ratios):
    out = []
    for h in ratios:
        latency = h * cache_ms + (1 - h) * (cache_ms + db_ms)
        out.append((round(latency, 2), round(qps_ * (1 - h))))
    return out


@O
def hit_ratio_effect(qps_, cache_ms, db_ms, ratios):
    return [(round(cache_ms + (1 - h) * db_ms, 2), round(qps_ * (1 - h))) for h in ratios]


Q(None, "Cache Stampede", "Medium", "Single-flight",
  "A popular key expires; requests for it arrive at the given times (ms) and a DB load takes <code>load_ms</code>. Without protection, every request that arrives before the cache is refilled goes to the DB. With single-flight, only the first one does and the others wait for it. Return <code>(DB loads without, with single-flight)</code>.",
  [(([0, 2, 3, 5, 8, 40, 41, 120], 30), (5, 1))],
  ("Simulate: track when the cache becomes full again.", "O(r)", "O(1)"),
  ("Same logic: a request misses if it arrives before the refill.", "O(r)", "O(1)"),
  viz=(([0, 2, 3, 40], 30)))


@B
def stampede(arrivals, load_ms):
    without = 0
    filled_at = None
    for t in arrivals:
        if filled_at is None or t < filled_at:
            without += 1
            if filled_at is None:
                filled_at = t + load_ms
    with_sf = 1
    return (without, with_sf)


@O
def stampede(arrivals, load_ms):
    ready = arrivals[0] + load_ms
    return (sum(t < ready for t in arrivals), 1)


Q(None, "Add Jitter to Expiry Times", "Easy", "Avoid synchronized expiry",
  "Keys were all cached at time 0 with TTL <code>ttl</code>; with jitter, key i's TTL becomes ttl + <code>jitter[i]</code>. Return <code>(most keys expiring in the same second without jitter, with jitter)</code>.",
  [((300, [0, 12, 45, 3, 30, 59, 12, 27, 50, 8]), (10, 2))],
  ("Count expiry seconds in a dict.", "O(n)", "O(n)"),
  ("<code>Counter(...).most_common(1)</code>.", "O(n)", "O(n)"),
  viz=((300, [0, 12, 45, 3])))


@B
def jitter_effect(ttl, jitter):
    without = len(jitter)
    counts = {}
    for j in jitter:
        counts[ttl + j] = counts.get(ttl + j, 0) + 1
    return (without, max(counts.values()))


@O
def jitter_effect(ttl, jitter):
    return (len(jitter), Counter(ttl + j for j in jitter).most_common(1)[0][1])


TRACKING = {"utm_source", "utm_medium", "utm_campaign", "fbclid", "gclid"}


Q(None, "Normalise the Cache Key", "Medium", "More hits from the same data",
  "Build a cache key from a URL: lower-case the host and path, drop tracking parameters in <code>TRACKING</code>, sort the remaining parameters. Return the key for each URL and how many distinct keys there are.",
  [((["https://Shop.in/Search?q=shoes&page=2&utm_source=mail", "https://shop.in/search?page=2&q=shoes", "https://shop.in/search?q=shoes&page=2&gclid=x1", "https://shop.in/search?q=bags"],), (['shop.in/search?page=2&q=shoes', 'shop.in/search?page=2&q=shoes', 'shop.in/search?page=2&q=shoes', 'shop.in/search?q=bags'], 2))],
  ("Split by hand on '?', '&' and '='.", "O(n · L)", "O(n)"),
  ("<code>urlparse</code>, <code>parse_qsl</code> and <code>urlencode</code>.", "O(n · L)", "O(n)"),
  viz=((["https://Shop.in/Search?q=shoes&utm_source=mail"],)))


@B
def cache_keys(urls):
    keys = []
    for u in urls:
        base, _, query = u.partition("?")
        scheme, _, rest = base.partition("://")
        params = []
        for pair in query.split("&") if query else []:
            k, _, v = pair.partition("=")
            if k not in TRACKING:
                params.append((k, v))
        params.sort()
        key = rest.lower()
        if params:
            key += "?" + "&".join(k + "=" + v for k, v in params)
        keys.append(key)
    return (keys, len(set(keys)))


@O
def cache_keys(urls):
    def key(u):
        p = urlparse(u)
        q = sorted((k, v) for k, v in parse_qsl(p.query) if k not in TRACKING)
        return (p.netloc + p.path).lower() + (f"?{urlencode(q)}" if q else "")
    keys = [key(u) for u in urls]
    return (keys, len(set(keys)))


Q(None, "What to Invalidate After a Write", "Medium", "Tagged invalidation",
  "Cached pages are tagged with the records they show. When records change, delete every cached key that has any of their tags. Return the keys to delete, sorted.",
  [(({"page:home": {"product:1", "product:2", "banner"}, "page:p1": {"product:1"}, "page:p3": {"product:3"}, "api:cart:7": {"product:2", "user:7"}}, ["product:2", "user:9"]), ['api:cart:7', 'page:home'])],
  ("Check each key's tags against each changed record.", "O(k · t)", "O(k)"),
  ("Build a reverse index tag → keys, then union.", "O(k · t)", "O(k · t)"),
  viz=(({"page:home": {"product:1", "banner"}, "page:p1": {"product:1"}}, ["product:1"])))


@B
def to_invalidate(tags, changed):
    out = []
    for key, ts in tags.items():
        for c in changed:
            if c in ts:
                out.append(key)
                break
    return sorted(out)


@O
def to_invalidate(tags, changed):
    reverse = defaultdict(set)
    for key, ts in tags.items():
        for t in ts:
            reverse[t].add(key)
    return sorted(set().union(*(reverse[c] for c in changed)))


Q(None, "Cache the Misses Too", "Easy", "Negative caching",
  "Requests ask for ids; some don't exist (not in <code>db</code>). Without negative caching every lookup of a missing id hits the DB; with it, the first 'not found' is cached too. Count DB hits both ways (found values are always cached).",
  [((["7", "x9", "7", "x9", "x9", "8", "x9", "8"], {"7", "8"}), (6, 3))],
  ("Two simulations with sets.", "O(n)", "O(n)"),
  ("Count distinct ids vs repeated misses.", "O(n)", "O(n)"),
  viz=((["7", "x9", "x9"], {"7"})))


@B
def negative_cache(requests, db):
    cached, without = set(), 0
    for r in requests:
        if r in cached:
            continue
        without += 1
        if r in db:
            cached.add(r)
    with_neg = len(set(requests))
    return (without, with_neg)


@O
def negative_cache(requests, db):
    found = {r for r in requests if r in db}
    missing_hits = sum(r not in db for r in requests)
    return (len(found) + missing_hits, len(set(requests)))


Q(None, "A Two-Level Cache", "Easy", "Local memory + Redis",
  "Requests first check an in-process cache (hit ratio <code>h1</code>, <code>l1_ms</code>), then Redis (hit ratio <code>h2</code> of what's left, <code>l2_ms</code>), then the DB (<code>db_ms</code>). Return the average latency in ms (rounded to 3) and the % of requests reaching the DB (rounded to 2).",
  [((0.6, 0.9, 0.01, 0.5, 6.0), (0.45, 4.0))],
  ("Add the paths step by step.", "O(1)", "O(1)"),
  ("One expression per figure.", "O(1)", "O(1)"),
  viz=((0.6, 0.9, 0.01, 0.5, 6.0)))


@B
def two_level(h1, h2, l1_ms, l2_ms, db_ms):
    p_l1 = h1
    p_l2 = (1 - h1) * h2
    p_db = (1 - h1) * (1 - h2)
    latency = p_l1 * l1_ms + p_l2 * (l1_ms + l2_ms) + p_db * (l1_ms + l2_ms + db_ms)
    return (round(latency, 3), round(p_db * 100, 2))


@O
def two_level(h1, h2, l1_ms, l2_ms, db_ms):
    miss1, miss2 = 1 - h1, (1 - h1) * (1 - h2)
    return (round(l1_ms + miss1 * l2_ms + miss2 * db_ms, 3), round(miss2 * 100, 2))


Q(None, "Find the Hot Keys", "Easy", "Skewed traffic",
  "Return the keys that receive more than <code>share</code> of all requests (e.g. a celebrity's profile), most requested first. Hot keys overload one cache node; fix with replicas or a local cache.",
  [((["u1"] * 50 + ["u2"] * 5 + ["u3"] * 30 + ["u4"] * 15, 0.2), ['u1', 'u3'])],
  ("Count in a dict, then filter and sort.", "O(n + k log k)", "O(k)"),
  ("<code>Counter.most_common</code>.", "O(n + k log k)", "O(k)"),
  viz=((["u1"] * 5 + ["u2"] + ["u3"] * 3, 0.2)))


@B
def hot_keys(requests, share):
    counts = {}
    for r in requests:
        counts[r] = counts.get(r, 0) + 1
    hot = [(c, k) for k, c in counts.items() if c / len(requests) > share]
    hot.sort(reverse=True)
    return [k for _, k in hot]


@O
def hot_keys(requests, share):
    return [k for k, c in Counter(requests).most_common() if c / len(requests) > share]


Q(None, "Evict by Size, Not Count", "Medium", "Byte-budgeted LRU",
  "A cache holds at most <code>max_bytes</code>. Items <code>(key, size)</code> are accessed in order; on a miss, evict least-recently-used items until the new one fits (skip items bigger than the whole cache). Return the evicted keys in order.",
  [((100, [("a", 40), ("b", 30), ("a", 40), ("c", 50), ("d", 20), ("b", 30), ("huge", 500)]), ['b', 'a'])],
  ("A recency list and a running total.", "O(n · c)", "O(c)"),
  ("An OrderedDict of sizes.", "O(n)", "O(c)"),
  viz=((100, [("a", 40), ("b", 30), ("c", 50)])))


@B
def size_lru(max_bytes, items):
    order, sizes, used, evicted = [], {}, 0, []
    for k, size in items:
        if k in sizes:
            order.remove(k)
            order.append(k)
            continue
        if size > max_bytes:
            continue
        while used + size > max_bytes:
            victim = order.pop(0)
            used -= sizes.pop(victim)
            evicted.append(victim)
        order.append(k)
        sizes[k] = size
        used += size
    return evicted


@O
def size_lru(max_bytes, items):
    cache, used, evicted = OrderedDict(), 0, []
    for k, size in items:
        if k in cache:
            cache.move_to_end(k)
        elif size <= max_bytes:
            while used + size > max_bytes:
                victim, vs = cache.popitem(last=False)
                used -= vs
                evicted.append(victim)
            cache[k], used = size, used + size
    return evicted


Q(None, "How Much Memory Will Redis Need?", "Easy", "Sizing a cache cluster",
  "Store <code>n</code> keys of <code>key_bytes</code> with values of <code>value_bytes</code>, plus <code>overhead</code> bytes per entry for the store's own structures. Keep memory under <code>fill</code> of each node's <code>node_gb</code> GB. Return <code>(total GB rounded to 1, nodes needed)</code>.",
  [((200_000_000, 30, 500, 90, 64, 0.75), (124.0, 3))],
  ("Multiply, then ceiling divide.", "O(1)", "O(1)"),
  ("Same with <code>math.ceil</code>.", "O(1)", "O(1)"),
  viz=((200_000_000, 30, 500, 90, 64, 0.75)))


@B
def redis_size(n, key_bytes, value_bytes, overhead, node_gb, fill):
    total = n * (key_bytes + value_bytes + overhead) / 1e9
    usable = node_gb * fill
    nodes = 0
    while nodes * usable < total:
        nodes += 1
    return (round(total, 1), nodes)


@O
def redis_size(n, key_bytes, value_bytes, overhead, node_gb, fill):
    total = n * (key_bytes + value_bytes + overhead) / 1e9
    return (round(total, 1), math.ceil(total / (node_gb * fill)))


Q(None, "The Best Possible Eviction (Belady)", "Hard", "An upper bound for any policy",
  "The optimal offline policy evicts the key whose next use is farthest in the future (or never). Return <code>(optimal hits, LRU hits)</code> for the same capacity — real policies can only approach the optimum because they can't see the future.",
  [((3, ["a", "b", "c", "d", "a", "b", "e", "a", "b", "c", "d", "e"]), (5, 2))],
  ("For each eviction, scan ahead to find every key's next use.", "O(a² )", "O(c)"),
  ("Precompute next-use positions with one backward pass.", "O(a · c)", "O(a)"),
  viz=((2, ["a", "b", "c", "a", "b"])))


@B
def belady(capacity, accesses):
    cache, hits = set(), 0
    for i, k in enumerate(accesses):
        if k in cache:
            hits += 1
            continue
        if len(cache) == capacity:
            def next_use(x):
                for j in range(i + 1, len(accesses)):
                    if accesses[j] == x:
                        return j
                return math.inf
            cache.remove(max(sorted(cache), key=next_use))
        cache.add(k)
    order, lru_hits = [], 0
    for k in accesses:
        if k in order:
            lru_hits += 1
            order.remove(k)
        elif len(order) == capacity:
            order.pop(0)
        order.append(k)
    return (hits, lru_hits)


@O
def belady(capacity, accesses):
    nxt, seen = [math.inf] * len(accesses), {}
    for i in range(len(accesses) - 1, -1, -1):
        nxt[i] = seen.get(accesses[i], math.inf)
        seen[accesses[i]] = i
    cache, hits = {}, 0
    for i, k in enumerate(accesses):
        if k in cache:
            hits += 1
        elif len(cache) == capacity:
            del cache[max(sorted(cache), key=cache.get)]
        cache[k] = nxt[i]
    od, lru_hits = OrderedDict(), 0
    for k in accesses:
        if k in od:
            lru_hits += 1
            od.move_to_end(k)
        else:
            if len(od) == capacity:
                od.popitem(last=False)
            od[k] = 1
    return (hits, lru_hits)


Q(None, "Read the Cache-Control Header", "Medium", "HTTP caching",
  "For each response header, decide <code>(can a shared cache such as a CDN store it?, seconds it stays fresh)</code>: not storable if it has <code>no-store</code> or <code>private</code>; freshness is <code>s-maxage</code> if present, else <code>max-age</code>, else 0. <code>no-cache</code> means storable but 0 seconds fresh (always revalidate).",
  [((["public, max-age=3600", "private, max-age=600", "no-store", "max-age=60, s-maxage=300", "no-cache"],), [(True, 3600), (False, 0), (False, 0), (True, 300), (True, 0)])],
  ("Split on commas and check each directive.", "O(n · d)", "O(d)"),
  ("Parse each header into a dict of directives once.", "O(n · d)", "O(d)"),
  viz=((["public, max-age=3600", "no-store"],)))


@B
def cache_control(headers):
    out = []
    for h in headers:
        parts = [p.strip() for p in h.split(",")]
        storable = "no-store" not in parts and "private" not in parts
        fresh = 0
        s_max = None
        for p in parts:
            if p.startswith("max-age="):
                fresh = int(p.split("=")[1])
            if p.startswith("s-maxage="):
                s_max = int(p.split("=")[1])
        if s_max is not None:
            fresh = s_max
        if "no-cache" in parts:
            fresh = 0
        out.append((storable, fresh if storable else 0))
    return out


@O
def cache_control(headers):
    out = []
    for h in headers:
        d = dict((p.strip().split("=") + [None])[:2] for p in h.split(","))
        storable = not ({"no-store", "private"} & d.keys())
        fresh = 0 if "no-cache" in d else int(d.get("s-maxage") or d.get("max-age") or 0)
        out.append((storable, fresh if storable else 0))
    return out


Q(None, "Warm the Cache Before Launch", "Easy", "Pre-loading",
  "Before a big sale, preload the <code>k</code> most requested keys from yesterday's log. Return the hit ratio (%) on today's requests that this warm cache would give on its own (before any other fills), rounded to 1.",
  [((["p1", "p2", "p1", "p3", "p1", "p2", "p4"], ["p1", "p2", "p5", "p1", "p3", "p1", "p2", "p6"], 2), 62.5)],
  ("Count yesterday, pick the top k, count today's hits.", "O(n log n)", "O(n)"),
  ("<code>Counter.most_common(k)</code>.", "O(n log n)", "O(n)"),
  viz=((["p1", "p2", "p1"], ["p1", "p3"], 1)))


@B
def warm_cache(yesterday, today, k):
    counts = {}
    for r in yesterday:
        counts[r] = counts.get(r, 0) + 1
    top = sorted(counts, key=lambda x: (-counts[x], yesterday.index(x)))[:k]
    hits = 0
    for r in today:
        if r in top:
            hits += 1
    return round(hits / len(today) * 100, 1)


@O
def warm_cache(yesterday, today, k):
    warm = {key for key, _ in Counter(yesterday).most_common(k)}
    return round(sum(r in warm for r in today) / len(today) * 100, 1)


Q(None, "Serve Stale While Revalidating", "Medium", "stale-while-revalidate",
  "A value was fetched at time 0. It is fresh for <code>ttl</code> seconds and may be served stale for <code>swr</code> more seconds while one background refresh (taking <code>load</code> seconds) runs. For each request time, return 'fresh', 'stale' (served old value; starts a refresh if none is running) or 'miss' (too old: the user waits for a fetch). A finished fetch resets the value's age to the time it completed.",
  [(([5, 12, 13, 14, 16, 40, 41, 44], 10, 20, 3), ['fresh', 'stale', 'stale', 'stale', 'fresh', 'stale', 'stale', 'fresh'])],
  ("Track fetched_at and a pending refresh time; update before each request.", "O(n)", "O(1)"),
  ("Same state machine with fewer branches.", "O(n)", "O(1)"),
  viz=(([5, 12, 16], 10, 20, 3)))


@B
def swr(times, ttl, swr_window, load):
    fetched, pending, out = 0, None, []
    for t in times:
        if pending is not None and pending <= t:
            fetched, pending = pending, None
        age = t - fetched
        if age < ttl:
            out.append("fresh")
        elif age < ttl + swr_window:
            out.append("stale")
            if pending is None:
                pending = t + load
        else:
            out.append("miss")
            fetched, pending = t + load, None
    return out


@O
def swr(times, ttl, swr_window, load):
    fetched, pending, out = 0, None, []
    for t in times:
        if pending is not None and pending <= t:
            fetched, pending = pending, None
        age = t - fetched
        state = "fresh" if age < ttl else "stale" if age < ttl + swr_window else "miss"
        out.append(state)
        if state == "stale" and pending is None:
            pending = t + load
        elif state == "miss":
            fetched, pending = t + load, None
    return out
