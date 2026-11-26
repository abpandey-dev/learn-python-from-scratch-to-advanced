from lib import *
import bisect
import zlib
from collections import Counter

LESSON("Basics", "Choosing a database", """
<table>
<tr><th>Type</th><th>Examples</th><th>Pick it for</th></tr>
<tr><td>Relational</td><td>PostgreSQL, MySQL</td><td>transactions, joins, constraints — the default</td></tr>
<tr><td>Key-value</td><td>Redis, DynamoDB</td><td>fast lookups by key, sessions, carts</td></tr>
<tr><td>Document</td><td>MongoDB</td><td>flexible, nested records</td></tr>
<tr><td>Wide-column</td><td>Cassandra, Bigtable</td><td>huge write volumes, time-ordered data</td></tr>
<tr><td>Graph</td><td>Neo4j</td><td>many-hop relationships</td></tr>
<tr><td>Search</td><td>Elasticsearch, OpenSearch</td><td>full-text and faceted search</td></tr>
<tr><td>Time-series</td><td>TimescaleDB, Prometheus</td><td>metrics over time</td></tr>
</table>
<p>In an interview, start relational unless a requirement pushes you elsewhere — and say which requirement.</p>
""", practice=["Pick a Database", "Join in the Application", "The N+1 Query Problem"])

LESSON("Core", "Indexes and storage engines", """
<p>An <b>index</b> is a sorted structure (usually a B-tree) that finds rows in O(log n) instead of scanning the table. A composite index on <code>(country, city, age)</code> helps queries that filter from the left: <code>country</code>, or <code>country + city</code> — not <code>city</code> alone.</p>
<p><b>B-trees</b> update pages in place: great reads, steady writes (PostgreSQL, MySQL). <b>LSM trees</b> append writes to an in-memory table, flush sorted files (SSTables) and merge them in the background (compaction): very fast writes, reads may check several files — Bloom filters help skip them (Cassandra, RocksDB).</p>
""", practice=["What an Index Saves", "The Leftmost-Prefix Rule", "Read From an LSM Tree", "Compact the SSTables"])

LESSON("Core", "Replication", """
<p>Copies of the data give read scale and survive failures.</p>
<ul>
<li><b>Leader-follower</b>: one primary takes writes, replicas serve reads. Asynchronous replication means replicas lag — a user may not see their own update. Fixes: read your own writes from the primary, or wait until the replica has caught up.</li>
<li><b>Multi-leader</b>: writes in several regions, conflicts must be resolved.</li>
<li><b>Leaderless</b> (Dynamo style): write to W of N replicas, read from R. If <code>R + W &gt; N</code> the read and write sets overlap, so a read sees the latest write; stale replicas are fixed by read repair.</li>
</ul>
""", practice=["Reading From a Lagging Replica", "Quorums: R + W > N", "Read Repair", "How Many Read Replicas?"])

LESSON("Core", "Sharding (partitioning)", """
<p>When one machine can't hold the data or the writes, split rows across shards by a <b>shard key</b>.</p>
<ul>
<li><b>Hash sharding</b> spreads keys evenly but range queries hit every shard.</li>
<li><b>Range sharding</b> keeps neighbours together (good for scans) but sequential keys like timestamps all land on the newest shard.</li>
<li>A good shard key has many distinct values, even traffic, and appears in most queries — otherwise queries must <b>scatter-gather</b> across all shards.</li>
<li>Resharding: split big shards, use consistent hashing or many small virtual shards so data moves in small pieces.</li>
</ul>
""", practice=["Hash Sharding", "Range Sharding and the Hot Shard", "Choose a Shard Key", "Split Oversized Shards", "Scatter-Gather Queries", "Global Top-K Across Shards"])


@LD
def shard_demo():
    keys = [f"order:{i}" for i in range(12)]
    print("hash :", Counter(zlib.crc32(k.encode()) % 3 for k in keys))
    times = list(range(1000, 1012))
    print("range:", Counter(bisect.bisect_right([500, 900], t) for t in times), "← all new writes on the last shard")


LESSON("Advanced", "Transactions and concurrency", """
<p>Two requests doing read → modify → write on the same row can overwrite each other (the <b>lost update</b>). Fixes:</p>
<ul>
<li>Atomic updates: <code>UPDATE account SET bal = bal - 30 WHERE id = 7</code>.</li>
<li>Pessimistic locks: <code>SELECT ... FOR UPDATE</code>.</li>
<li>Optimistic locking: keep a version column, <code>UPDATE ... WHERE version = 4</code>, retry if 0 rows changed.</li>
</ul>
<p>Size connection pools with Little's law (QPS × query time) and remember the database's own connection limit — a pooler such as PgBouncer sits in between at scale.</p>
""", practice=["The Lost Update", "Optimistic Locking", "How Many Database Connections?"])
