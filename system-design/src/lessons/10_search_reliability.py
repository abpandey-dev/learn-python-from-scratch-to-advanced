from lib import *
from collections import defaultdict

LESSON("Basics", "Search and autocomplete", """
<p>Databases can't do fast full-text search with <code>LIKE '%shoe%'</code>. A search engine (Elasticsearch, OpenSearch, Solr) builds an <b>inverted index</b>: each term → the sorted list of documents containing it. A query intersects posting lists, then ranks matches (TF-IDF, BM25, plus signals like popularity, or a learned model). Index updates flow from the database through a queue or CDC, so search is eventually consistent.</p>
<p><b>Autocomplete</b> precomputes top suggestions per prefix (a trie or sorted list with cached results), updated from search logs in batches; <b>trending</b> uses top-K counting over a sliding window.</p>
""", practice=["Build an Inverted Index", "Intersect Posting Lists", "Rank Results With TF-IDF", "Autocomplete", "Top-K Trending Searches"])


@LD
def index_demo():
    docs = {1: "red shoes", 2: "red dress", 3: "running shoes"}
    index = defaultdict(list)
    for i, text in docs.items():
        for w in text.split():
            index[w].append(i)
    print(dict(index))
    print("red AND shoes →", sorted(set(index["red"]) & set(index["shoes"])))


LESSON("Core", "Location and file storage", """
<p><b>Nearby search</b> (ride hailing, food delivery, maps): bucket locations by <b>geohash</b> or a grid/quadtree/S2 cell, look up your cell and its neighbours, then compute exact distances. Moving drivers update their cell in an in-memory store every few seconds.</p>
<p><b>File storage</b> (Dropbox, Google Drive, S3): metadata in a database, bytes in object storage. Split files into chunks identified by hash — upload only changed chunks, deduplicate identical ones, and resume interrupted uploads. Object stores keep data durable with replication or cheaper <b>erasure coding</b>.</p>
""", practice=["Encode a Geohash", "Find Nearby Places", "Chunk and Deduplicate Files", "Resume an Interrupted Upload", "Pick a Multipart Part Size", "Replication vs Erasure Coding"])

LESSON("Core", "Reliability and operations", """
<ul>
<li><b>SLI</b> (what you measure: success rate, p99 latency) → <b>SLO</b> (target: 99.9%) → <b>error budget</b> (0.1% = 43 minutes a month). Spend the budget on releases; when it's gone, freeze risky changes.</li>
<li>Alert on <b>burn rate</b>, not on every error; watch the four golden signals: latency, traffic, errors, saturation.</li>
<li>Percentiles, not averages: p99 is what your heaviest users feel.</li>
<li>Prevent cascades: timeouts, retries only at one layer with backoff, circuit breakers, bulkheads, <b>load shedding</b> by priority.</li>
<li>Plan disasters with <b>RPO</b> (data loss allowed) and <b>RTO</b> (time to recover); release with canaries and automatic rollback.</li>
</ul>
""", practice=["SLOs and Error Budgets", "Burn-Rate Alerts", "Latency Percentiles", "Retry Storms", "Shed Load by Priority", "Which Disaster-Recovery Plan Fits?", "Promote or Roll Back the Canary?"])

LESSON("Advanced", "The 45-minute system design interview", """
<ol>
<li><b>Requirements (5 min)</b>: functional features, non-functional (scale, latency, availability, consistency), what's out of scope.</li>
<li><b>Estimates (3–4 min)</b>: QPS, peak, storage, bandwidth — only what changes the design.</li>
<li><b>API and data model (5 min)</b>: endpoints, main tables or keys, the access patterns.</li>
<li><b>High-level design (10 min)</b>: clients → load balancer → services → cache → databases, queues, storage. Walk one request end to end.</li>
<li><b>Deep dives (15 min)</b>: the hardest parts — scaling the hot path, sharding, consistency, failure handling. Offer trade-offs, then choose.</li>
<li><b>Wrap up (4–5 min)</b>: bottlenecks, monitoring, what you'd do with more time.</li>
</ol>
<p>Practise the classics with this course's building blocks: URL shortener, rate limiter, news feed, chat, notification service, search autocomplete, web crawler, ride hailing, file storage, video streaming, payment system, distributed cache.</p>
""", practice=["Budget Your Interview Time", "Self-Review a Design Answer"])
