from lib import *

THEORY("Where to cache", """
<table>
<tr><th>Layer</th><th>Example</th><th>Typical latency</th></tr>
<tr><td>Browser / app</td><td>HTTP cache, local storage</td><td>0 (no request)</td></tr>
<tr><td>CDN edge</td><td>static files, API responses</td><td>10–30 ms</td></tr>
<tr><td>In-process</td><td>a map in the service</td><td>~0.01 ms</td></tr>
<tr><td>Distributed</td><td>Redis, Memcached</td><td>~0.5 ms</td></tr>
<tr><td>Database</td><td>buffer pool, materialised views</td><td>1–10 ms</td></tr>
</table>
""")

THEORY("HTTP caching headers", """
<ul>
<li><code>Cache-Control: public, max-age=3600</code> — anyone may cache for an hour.</li>
<li><code>private</code> — only the user's browser; <code>no-store</code> — never cache.</li>
<li><code>no-cache</code> — store, but revalidate every time (with <code>ETag</code> / <code>If-None-Match</code> → 304 Not Modified).</li>
<li><code>s-maxage</code> — overrides max-age for shared caches (CDNs); <code>stale-while-revalidate</code> — serve stale while refreshing.</li>
</ul>
""")

FAQ("How do you keep a cache consistent with the database?", "<p>Update the database, then delete the cache entry (not update it — two racing updates can leave the old value). Add a TTL as a backstop. For stronger guarantees, invalidate from the database change stream (CDC) so no code path can forget.</p>")
FAQ("Redis or Memcached?", "<p>Memcached is a simple, multi-threaded key-value cache. Redis adds data structures (lists, sorted sets, streams), persistence, replication and Lua scripts — so it also serves as a rate limiter, leaderboard or queue.</p>")
FAQ("What is a cache stampede and how do you stop it?", "<p>Many requests miss the same key at once and all hit the database. Use single-flight locking, serve stale data while one request refreshes, refresh popular keys before they expire, and jitter TTLs.</p>")
FAQ("What should you not cache?", "<p>Data that must be exactly current (balances during payment), data read once, and very large values that evict many useful small ones. Cache what is read often and changes rarely.</p>")
FAQ("How do you size a cache?", "<p>Estimate the working set (hot keys × (key + value + overhead)), leave headroom (fill to ~75%), and measure the hit ratio as you grow — the curve flattens, and beyond that point more memory buys little.</p>")
FAQ("Why delete instead of update on write?", "<p>Deleting is idempotent and avoids races where an older write lands in the cache after a newer one. The next read reloads the current value.</p>")
