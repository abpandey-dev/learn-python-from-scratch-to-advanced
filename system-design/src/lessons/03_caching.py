from lib import *
from collections import OrderedDict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LESSON("Basics", "Why caches work", """
<p>Most traffic is <b>skewed</b>: a small set of keys (the home page, popular products, a celebrity's profile) gets most requests. Keeping those in memory — microseconds away instead of milliseconds — cuts latency and protects the database. Two numbers decide everything:</p>
<pre><code class="py">average latency = cache_ms + (1 − hit_ratio) × db_ms
DB load         = requests × (1 − hit_ratio)        # 99% hits → 1/100 of the traffic</code></pre>
<p>Caches live at every layer: the browser, the CDN, an in-process map, a shared Redis/Memcached cluster, the database's own buffer pool.</p>
""", practice=["What a Hit Ratio Buys You", "A Two-Level Cache", "How Much Memory Will Redis Need?", "Warm the Cache Before Launch"])


@LD
def hit_ratio_curve():
    ratios = [i / 100 for i in range(50, 100)]
    fig, ax = plt.subplots(figsize=(5, 2.6))
    ax.plot([r * 100 for r in ratios], [100_000 * (1 - r) for r in ratios], color="#0f766e")
    ax.set_xlabel("hit ratio %"); ax.set_ylabel("DB QPS"); ax.set_title("100k QPS: the last few % matter most")


LESSON("Core", "Eviction policies", """
<p>Memory is limited, so something must go when the cache is full:</p>
<table>
<tr><th>Policy</th><th>Evicts</th><th>Note</th></tr>
<tr><td>LRU</td><td>least recently used</td><td>the default; hash map + linked list → O(1)</td></tr>
<tr><td>LFU</td><td>least frequently used</td><td>keeps long-term favourites; needs ageing</td></tr>
<tr><td>FIFO</td><td>oldest inserted</td><td>simple, ignores reuse</td></tr>
<tr><td>Size-aware</td><td>by bytes, not count</td><td>what real caches do</td></tr>
<tr><td>Belady (optimal)</td><td>next used farthest in the future</td><td>needs the future — a benchmark only</td></tr>
</table>
<p>"Design an LRU cache" is one of the most common interview coding questions: <code>OrderedDict</code> in Python, or a dict pointing into a doubly linked list.</p>
""", practice=["An LRU Cache", "An LFU Cache", "FIFO vs LRU", "Evict by Size, Not Count", "The Best Possible Eviction (Belady)"])


@LD
def lru_demo():
    cache = OrderedDict()
    for k in ["a", "b", "c", "a", "d"]:
        if k in cache:
            cache.move_to_end(k)
        else:
            if len(cache) == 3:
                print("evict", cache.popitem(last=False)[0])
            cache[k] = 1
        print(k, "->", list(cache))


LESSON("Core", "Reading and writing through a cache", """
<ul>
<li><b>Cache-aside</b> (lazy loading): the app reads the cache, on a miss reads the DB and fills the cache. On a write, update the DB and <b>delete</b> the cache entry. Most common.</li>
<li><b>Read-through</b>: the cache itself loads from the DB on a miss.</li>
<li><b>Write-through</b>: every write goes to cache and DB together — always fresh, slower writes.</li>
<li><b>Write-back</b> (write-behind): write to the cache, flush to the DB later in batches — fast, but data is lost if the cache dies before flushing.</li>
</ul>
<p>Every cached value has a <b>TTL</b> as a safety net: even if an invalidation is missed, staleness is bounded.</p>
""", practice=["A Cache With Expiry", "Cache-Aside and the Stale Read", "Write-Through or Write-Back?", "What to Invalidate After a Write"])

LESSON("Advanced", "When caches fail you", """
<ul>
<li><b>Stampede</b> (thundering herd): a hot key expires and thousands of requests hit the DB at once. Fix: single-flight (one loader per key), serve stale while one request refreshes, refresh ahead of expiry.</li>
<li><b>Synchronised expiry</b>: keys loaded together expire together. Fix: add random jitter to TTLs.</li>
<li><b>Penetration</b>: requests for ids that don't exist always miss. Fix: cache "not found" briefly, or a Bloom filter.</li>
<li><b>Hot keys</b>: one key overloads one cache node. Fix: replicate it, or add a small local cache.</li>
<li><b>Low hit ratio from bad keys</b>: the same content under many URLs. Fix: normalise the cache key.</li>
</ul>
""", practice=["Cache Stampede", "Add Jitter to Expiry Times", "Serve Stale While Revalidating", "Cache the Misses Too", "Find the Hot Keys", "Normalise the Cache Key", "Read the Cache-Control Header"])
