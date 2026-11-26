from lib import *

THEORY("Classic questions → building blocks", """
<table>
<tr><th>Question</th><th>Key ideas</th></tr>
<tr><td>URL shortener</td><td>base62, ID generation, cache, 302 redirects</td></tr>
<tr><td>Rate limiter</td><td>token bucket / sliding window in Redis, gateway</td></tr>
<tr><td>News feed</td><td>hybrid fan-out, ranking, feed cache</td></tr>
<tr><td>Chat</td><td>WebSockets, session registry, per-conversation seq</td></tr>
<tr><td>Notifications</td><td>queues, preferences, retries, digests</td></tr>
<tr><td>Autocomplete</td><td>trie / prefix index, top-K, batch updates</td></tr>
<tr><td>Web crawler</td><td>URL frontier queue, politeness, dedupe with Bloom filters</td></tr>
<tr><td>Ride hailing / nearby</td><td>geohash or quadtree, in-memory location updates</td></tr>
<tr><td>File storage</td><td>chunking, dedupe, metadata DB + object storage</td></tr>
<tr><td>Video streaming</td><td>transcoding pipeline, CDN, adaptive bitrate</td></tr>
<tr><td>Payments</td><td>idempotency, ledger, sagas, reconciliation</td></tr>
<tr><td>Distributed cache / KV store</td><td>consistent hashing, replication, quorums</td></tr>
</table>
""")

THEORY("How many nines?", """
<table>
<tr><th>Availability</th><th>Downtime / month</th></tr>
<tr><td>99%</td><td>7.3 hours</td></tr>
<tr><td>99.9%</td><td>43.8 minutes</td></tr>
<tr><td>99.99%</td><td>4.4 minutes</td></tr>
<tr><td>99.999%</td><td>26 seconds</td></tr>
</table>
""")

FAQ("What do interviewers look for?", "<p>Clarifying the problem, numbers that drive decisions, a clear working design, depth on the hard parts, explicit trade-offs, and handling of failures — communicated as a conversation, not a monologue.</p>")
FAQ("How do you design search for an e-commerce site?", "<p>Stream product changes into a search engine's inverted index; rank by text relevance plus business signals; add filters (facets), autocomplete from query logs, and cache popular queries.</p>")
FAQ("What is an error budget used for?", "<p>It turns reliability into a shared number: while budget remains, teams ship; when it's spent, they prioritise reliability work. It stops both over- and under-investing in reliability.</p>")
FAQ("How do you find nearby drivers quickly?", "<p>Index driver locations by geohash or grid cell in memory, query your cell plus neighbours, compute exact distances for the few candidates, and refresh locations every few seconds.</p>")
FAQ("How do you prevent a retry storm?", "<p>Retry at one layer only, with capped exponential backoff and jitter, retry budgets, and circuit breakers; return errors quickly when overloaded instead of queueing forever.</p>")
FAQ("What should you do if you don't know something in the interview?", "<p>Say so, reason from first principles, state an assumption, and keep going. Interviewers value structured thinking over memorised answers.</p>")
