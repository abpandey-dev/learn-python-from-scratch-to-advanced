from lib import *

THEORY("ACID vs BASE", """
<table>
<tr><th>ACID (most relational)</th><th>BASE (many NoSQL)</th></tr>
<tr><td>Atomic, Consistent, Isolated, Durable</td><td>Basically Available, Soft state, Eventually consistent</td></tr>
<tr><td>correctness first</td><td>availability and scale first</td></tr>
</table>
""")

THEORY("Isolation levels", """
<table>
<tr><th>Level</th><th>Prevents</th></tr>
<tr><td>Read committed</td><td>dirty reads</td></tr>
<tr><td>Repeatable read / snapshot</td><td>non-repeatable reads</td></tr>
<tr><td>Serializable</td><td>all anomalies, incl. write skew</td></tr>
</table>
""")

FAQ("SQL or NoSQL?", "<p>Default to SQL for structured data with relationships and transactions. Choose NoSQL for a clear reason: huge write throughput, simple key access at massive scale, flexible documents, or a specialised model (graph, search, time-series).</p>")
FAQ("How do you scale a database?", "<p>In order: indexes and query fixes, caching, read replicas, vertical scaling, then partitioning or sharding — and archive old data. Sharding is last because it complicates joins, transactions and operations.</p>")
FAQ("What is replication lag and how do you handle it?", "<p>The delay before a replica applies the primary's writes. Route a user's reads to the primary right after they write, use monotonic reads (same replica), or wait for a replication position before reading.</p>")
FAQ("What makes a good shard key?", "<p>High cardinality, even distribution of data and traffic, and present in most queries. Avoid monotonically increasing keys with range sharding and low-cardinality keys like country.</p>")
FAQ("B-tree or LSM tree?", "<p>B-trees suit read-heavy workloads with in-place updates; LSM trees suit write-heavy workloads, trading some read cost and background compaction for fast sequential writes.</p>")
FAQ("How do you do a transaction across shards?", "<p>Avoid it by choosing a shard key that keeps related rows together. Otherwise use two-phase commit (blocking, slow) or a saga of local transactions with compensations (covered in the consistency topic).</p>")
