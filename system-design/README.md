# System Design

10 topics · theory with 60 theory questions · 41 lessons from basics to advanced · 200 practice questions with answers · Estimation, load balancing, caching, databases and sharding, consistency, queues, APIs and rate limiting, then full designs: URL shortener, chat, news feed, notifications, search, storage and reliability · every building block is simulated in plain Python so you can see how it behaves, then written the efficient way, both shown running step by step.

**Live site:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/

Every solution is run against its test cases by `build.py` before the site is generated, and each animation is recorded from a real run of the code you see.

## Topics

- [Requirements & Back-of-the-Envelope Estimation](#requirements-back-of-the-envelope-estimation) — Every design starts with numbers: requests per second and peaks, storage with replication, bandwidth, read/write ratios, latency numbers, availability nines, servers, shards and cache size, Little's law, tail latency under fan-out, IDs and cost.
- [Load Balancing, Routing & CDNs](#load-balancing-routing-cdns) — Spread traffic and survive failures: round robin, weighted and least-connections balancing, sticky hashing, consistent hashing with virtual nodes, health checks, power of two choices, path routing, DNS TTLs, CDN hit ratios, geo routing, autoscaling, rolling and blue/green deploys, and regional failover.
- [Caching](#caching) — The fastest request is the one you don't make: eviction policies (LRU, LFU, FIFO, optimal), TTLs, cache-aside, write-through and write-back, stampedes and single-flight, jittered expiry, cache keys, invalidation, negative caching, two-level caches, hot keys, sizing and HTTP cache headers.
- [Databases, Replication & Sharding](#databases-replication-sharding) — Choosing a database, indexes and the leftmost-prefix rule, LSM trees and compaction, replication lag, quorums (R + W > N) and read repair, hash vs range sharding, shard keys, hot shards, scatter-gather, joins, N+1 queries, lost updates and optimistic locking, connection pools and read replicas.
- [Consistency & Distributed Systems](#consistency-distributed-systems) — What happens when machines disagree: CAP and PACELC, Lamport and vector clocks, clock skew, last-writer-wins, CRDTs, idempotency, two-phase commit vs sagas, majorities and split brain, Raft voting, leases and fencing tokens, heartbeats, gossip and Merkle-tree anti-entropy.
- [Queues & Streams](#queues-streams) — Decoupling with messages: backlogs and consumer counts, Kafka partitions, keys and consumer groups, lag and offsets, at-least-once redelivery, retries with backoff and jitter, dead-letter queues, visibility timeouts, backpressure, the outbox pattern, reordering, windows and watermarks, log compaction, delay queues and queueing maths.
- [APIs & Rate Limiting](#apis-rate-limiting) — Designing and protecting APIs: fixed-window, sliding-window, token-bucket and leaky-bucket limiters, per-user quotas, offset vs cursor pagination, idempotency keys, status codes, safe and idempotent methods, versioning, ETags, batching, deadlines, circuit breakers, gateways, webhook signatures and push vs poll.
- [URL Shortener & ID Generation](#url-shortener-id-generation) — The classic first design question: base62 codes, code length and capacity, hashing with collision handling, ticket ranges and key-generation services, Snowflake IDs (compose, decode, sequence limits, clock rollback), time-sortable IDs, birthday-paradox collisions, Bloom filters, aliases, expiry, analytics and URL canonicalisation.
- [News Feed, Chat & Notifications](#news-feed-chat-notifications) — Real-time social systems: fan-out on write vs read, the celebrity problem, merging and ranking timelines, author diversity, chat sequence numbers, unread counts, receipts, presence, routing to connection servers, group fan-out, reconnect sync, typing throttles, notification digests, quiet hours, channels, device tokens and sharded counters.
- [Search, Storage, Reliability & the Interview](#search-storage-reliability-the-interview) — The last building blocks and how to put it all together: inverted indexes, AND queries, TF-IDF, autocomplete, top-K, geohashes and nearby search, file chunking and dedupe, resumable and multipart uploads, erasure coding, SLOs, error budgets and burn rates, percentiles, retry storms, load shedding, disaster recovery, canaries — and the 45-minute interview framework.

## Requirements & Back-of-the-Envelope Estimation

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Requests per Second](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/estimation/requests-per-second) | Easy | Average and peak |
| 2 | [How Much Storage?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/estimation/how-much-storage) | Easy | Items × size × time × replicas |
| 3 | [Bandwidth In and Out](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/estimation/bandwidth-in-and-out) | Easy | MB per second |
| 4 | [Read-Heavy or Write-Heavy?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/estimation/read-heavy-or-write-heavy) | Easy | Shape the design |
| 5 | [Add Up a Request's Latency](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/estimation/add-up-a-requests-latency) | Easy | Latency numbers |
| 6 | [What Do the Nines Mean?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/estimation/what-do-the-nines-mean) | Easy | Availability → downtime |
| 7 | [Availability in Series and in Parallel](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/estimation/availability-in-series-and-in-parallel) | Medium | Dependencies vs redundancy |
| 8 | [How Many Servers?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/estimation/how-many-servers) | Easy | Capacity with headroom |
| 9 | [How Big a Cache?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/estimation/how-big-a-cache) | Easy | The 80/20 rule |
| 10 | [How Many Shards?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/estimation/how-many-shards) | Medium | Size and throughput both count |
| 11 | [Open Connections (Little's Law)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/estimation/open-connections-littles-law) | Easy | Concurrency |
| 12 | [Fan-Out Makes the Tail Worse](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/estimation/fan-out-makes-the-tail-worse) | Medium | Tail latency |
| 13 | [Human-Readable Sizes](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/estimation/human-readable-sizes) | Easy | Units |
| 14 | [How Long Must an ID Be?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/estimation/how-long-must-an-id-be) | Easy | Bits and characters |
| 15 | [What Will Storage Cost?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/estimation/what-will-storage-cost) | Easy | Money matters in design |
| 16 | [When Will We Run Out?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/estimation/when-will-we-run-out) | Medium | Growth planning |
| 17 | [How Big Is One Record?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/estimation/how-big-is-one-record) | Easy | Size from the schema |
| 18 | [Functional or Non-Functional?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/estimation/functional-or-non-functional) | Easy | Requirements first |
| 19 | [Estimate a Whole System](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/estimation/estimate-a-whole-system) | Medium | Putting it together |
| 20 | [Find the Real Peak From Traffic](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/estimation/find-the-real-peak-from-traffic) | Medium | Use data, not guesses |

## Load Balancing, Routing & CDNs

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Round Robin](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/load-balancing/round-robin) | Easy | The simplest balancer |
| 2 | [Weighted Round Robin](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/load-balancing/weighted-round-robin) | Medium | Bigger servers get more |
| 3 | [Least Connections](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/load-balancing/least-connections) | Medium | Send work to the least busy |
| 4 | [Sticky Routing by Client IP](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/load-balancing/sticky-routing-by-client-ip) | Easy | Same client, same server |
| 5 | [Consistent Hashing Lookup](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/load-balancing/consistent-hashing-lookup) | Medium | The hash ring |
| 6 | [Why Consistent Hashing Moves Fewer Keys](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/load-balancing/why-consistent-hashing-moves-fewer-keys) | Hard | Virtual nodes |
| 7 | [Health Checks With Hysteresis](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/load-balancing/health-checks-with-hysteresis) | Medium | Don't flap |
| 8 | [Fail Over to a Healthy Server](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/load-balancing/fail-over-to-a-healthy-server) | Easy | Skip the dead ones |
| 9 | [Power of Two Choices](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/load-balancing/power-of-two-choices) | Medium | Nearly optimal, almost free |
| 10 | [Route by Path (Layer 7)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/load-balancing/route-by-path-layer-7) | Easy | Longest prefix wins |
| 11 | [How Long Until DNS Changes Everywhere?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/load-balancing/how-long-until-dns-changes-everywhere) | Easy | TTLs |
| 12 | [CDN Hit Ratio and Origin Load](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/load-balancing/cdn-hit-ratio-and-origin-load) | Medium | Edge caching |
| 13 | [Does the CDN Speed Things Up?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/load-balancing/does-the-cdn-speed-things-up) | Easy | Weighted latency |
| 14 | [Send Users to the Nearest Region](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/load-balancing/send-users-to-the-nearest-region) | Medium | Geo routing |
| 15 | [Autoscaling by Target Tracking](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/load-balancing/autoscaling-by-target-tracking) | Medium | Scale on a metric |
| 16 | [Rolling Deploy Batches](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/load-balancing/rolling-deploy-batches) | Easy | Keep capacity during a release |
| 17 | [Shift Traffic Blue → Green](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/load-balancing/shift-traffic-blue-green) | Easy | Progressive rollout |
| 18 | [Fail Over Between Regions](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/load-balancing/fail-over-between-regions) | Medium | Global traffic management |
| 19 | [Drain Connections Before Removing a Server](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/load-balancing/drain-connections-before-removing-a-server) | Easy | Graceful shutdown |
| 20 | [What Sticky Sessions Cost You](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/load-balancing/what-sticky-sessions-cost-you) | Medium | Stateless servers |

## Caching

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [An LRU Cache](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/caching/an-lru-cache) | Medium | Evict the least recently used |
| 2 | [An LFU Cache](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/caching/an-lfu-cache) | Medium | Evict the least frequently used |
| 3 | [FIFO vs LRU](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/caching/fifo-vs-lru) | Medium | Policy matters |
| 4 | [A Cache With Expiry](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/caching/a-cache-with-expiry) | Easy | TTL |
| 5 | [Cache-Aside and the Stale Read](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/caching/cache-aside-and-the-stale-read) | Medium | Forgetting to invalidate |
| 6 | [Write-Through or Write-Back?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/caching/write-through-or-write-back) | Medium | Counting database writes |
| 7 | [What a Hit Ratio Buys You](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/caching/what-a-hit-ratio-buys-you) | Easy | Latency and DB load |
| 8 | [Cache Stampede](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/caching/cache-stampede) | Medium | Single-flight |
| 9 | [Add Jitter to Expiry Times](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/caching/add-jitter-to-expiry-times) | Easy | Avoid synchronized expiry |
| 10 | [Normalise the Cache Key](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/caching/normalise-the-cache-key) | Medium | More hits from the same data |
| 11 | [What to Invalidate After a Write](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/caching/what-to-invalidate-after-a-write) | Medium | Tagged invalidation |
| 12 | [Cache the Misses Too](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/caching/cache-the-misses-too) | Easy | Negative caching |
| 13 | [A Two-Level Cache](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/caching/a-two-level-cache) | Easy | Local memory + Redis |
| 14 | [Find the Hot Keys](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/caching/find-the-hot-keys) | Easy | Skewed traffic |
| 15 | [Evict by Size, Not Count](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/caching/evict-by-size-not-count) | Medium | Byte-budgeted LRU |
| 16 | [How Much Memory Will Redis Need?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/caching/how-much-memory-will-redis-need) | Easy | Sizing a cache cluster |
| 17 | [The Best Possible Eviction (Belady)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/caching/the-best-possible-eviction-belady) | Hard | An upper bound for any policy |
| 18 | [Read the Cache-Control Header](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/caching/read-the-cache-control-header) | Medium | HTTP caching |
| 19 | [Warm the Cache Before Launch](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/caching/warm-the-cache-before-launch) | Easy | Pre-loading |
| 20 | [Serve Stale While Revalidating](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/caching/serve-stale-while-revalidating) | Medium | stale-while-revalidate |

## Databases, Replication & Sharding

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Pick a Database](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/databases/pick-a-database) | Easy | Match needs to a data model |
| 2 | [What an Index Saves](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/databases/what-an-index-saves) | Easy | Rows examined |
| 3 | [The Leftmost-Prefix Rule](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/databases/the-leftmost-prefix-rule) | Medium | Composite indexes |
| 4 | [Read From an LSM Tree](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/databases/read-from-an-lsm-tree) | Medium | Memtable, then SSTables |
| 5 | [Compact the SSTables](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/databases/compact-the-sstables) | Medium | Merge and drop tombstones |
| 6 | [Reading From a Lagging Replica](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/databases/reading-from-a-lagging-replica) | Medium | Async replication |
| 7 | [Quorums: R + W > N](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/databases/quorums-r-w-n) | Easy | Tunable consistency |
| 8 | [Read Repair](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/databases/read-repair) | Easy | Pick the newest, fix the rest |
| 9 | [Hash Sharding](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/databases/hash-sharding) | Easy | Even spread |
| 10 | [Range Sharding and the Hot Shard](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/databases/range-sharding-and-the-hot-shard) | Medium | Sequential keys pile up |
| 11 | [Choose a Shard Key](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/databases/choose-a-shard-key) | Medium | Avoid skew |
| 12 | [Split Oversized Shards](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/databases/split-oversized-shards) | Medium | Resharding by halves |
| 13 | [Scatter-Gather Queries](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/databases/scatter-gather-queries) | Easy | Queries without the shard key |
| 14 | [Global Top-K Across Shards](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/databases/global-top-k-across-shards) | Medium | Merge sorted results |
| 15 | [Join in the Application](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/databases/join-in-the-application) | Easy | Hash join |
| 16 | [The N+1 Query Problem](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/databases/the-n-1-query-problem) | Easy | Batch your lookups |
| 17 | [The Lost Update](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/databases/the-lost-update) | Medium | Read-modify-write races |
| 18 | [Optimistic Locking](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/databases/optimistic-locking) | Easy | Compare the version, then write |
| 19 | [How Many Database Connections?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/databases/how-many-database-connections) | Easy | Little's law |
| 20 | [How Many Read Replicas?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/databases/how-many-read-replicas) | Easy | Replicas also apply every write |

## Consistency & Distributed Systems

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [CP or AP?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/consistency/cp-or-ap) | Easy | What to give up during a partition |
| 2 | [Lamport Clocks](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/consistency/lamport-clocks) | Medium | Logical time |
| 3 | [Compare Vector Clocks](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/consistency/compare-vector-clocks) | Medium | Happened-before or concurrent? |
| 4 | [Run Vector Clocks](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/consistency/run-vector-clocks) | Medium | One counter per process |
| 5 | [Clock Skew Reorders Events](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/consistency/clock-skew-reorders-events) | Medium | Why wall clocks lie |
| 6 | [Last Writer Wins](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/consistency/last-writer-wins) | Easy | Simple conflict resolution |
| 7 | [Merge a Grow-Only Counter (CRDT)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/consistency/merge-a-grow-only-counter-crdt) | Easy | Conflict-free by design |
| 8 | [Make the Payment Idempotent](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/consistency/make-the-payment-idempotent) | Medium | Retries without double charges |
| 9 | [Two-Phase Commit](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/consistency/two-phase-commit) | Medium | All or nothing across services |
| 10 | [Run a Saga](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/consistency/run-a-saga) | Medium | Compensate instead of rolling back |
| 11 | [Which Side Keeps Working After a Split?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/consistency/which-side-keeps-working-after-a-split) | Easy | Majority quorums |
| 12 | [Who Wins the Raft Vote?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/consistency/who-wins-the-raft-vote) | Medium | Up-to-date logs only |
| 13 | [Fencing Tokens](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/consistency/fencing-tokens) | Medium | Stop the zombie lock holder |
| 14 | [When Did the Leader Lease Lapse?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/consistency/when-did-the-leader-lease-lapse) | Easy | Leases |
| 15 | [A Heartbeat Failure Detector](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/consistency/a-heartbeat-failure-detector) | Easy | Suspect silent nodes |
| 16 | [How Fast Does Gossip Spread?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/consistency/how-fast-does-gossip-spread) | Easy | Epidemic protocols |
| 17 | [Find Divergent Buckets (Merkle Anti-Entropy)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/consistency/find-divergent-buckets-merkle-anti-entropy) | Medium | Compare hashes, not data |
| 18 | [Deduplicate by Sequence Number](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/consistency/deduplicate-by-sequence-number) | Easy | Effectively-once delivery |
| 19 | [Monotonic Reads](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/consistency/monotonic-reads) | Medium | Never go back in time |
| 20 | [How Many Nodes for Consensus?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/consistency/how-many-nodes-for-consensus) | Easy | Crash vs Byzantine faults |

## Queues & Streams

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Watch the Backlog Grow](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/queues/watch-the-backlog-grow) | Easy | Arrivals vs consumption |
| 2 | [How Many Consumers and Partitions?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/queues/how-many-consumers-and-partitions) | Easy | Throughput sizing |
| 3 | [Partition by Key](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/queues/partition-by-key) | Easy | Order per key |
| 4 | [Assign Partitions to a Consumer Group](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/queues/assign-partitions-to-a-consumer-group) | Medium | Range assignment |
| 5 | [Consumer Lag](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/queues/consumer-lag) | Easy | How far behind are we? |
| 6 | [Duplicates After a Crash](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/queues/duplicates-after-a-crash) | Medium | At-least-once delivery |
| 7 | [Exponential Backoff](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/queues/exponential-backoff) | Easy | Don't hammer a struggling service |
| 8 | [Add Full Jitter](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/queues/add-full-jitter) | Easy | Spread the retries |
| 9 | [Send Poison Messages to a Dead-Letter Queue](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/queues/send-poison-messages-to-a-dead-letter-queue) | Medium | Don't retry forever |
| 10 | [Visibility Timeouts](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/queues/visibility-timeouts) | Easy | SQS-style redelivery |
| 11 | [Backpressure With a Bounded Queue](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/queues/backpressure-with-a-bounded-queue) | Medium | Reject early, stay healthy |
| 12 | [Dual Writes vs the Outbox](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/queues/dual-writes-vs-the-outbox) | Medium | Never lose an event |
| 13 | [Restore Order With a Reorder Buffer](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/queues/restore-order-with-a-reorder-buffer) | Medium | Release in sequence |
| 14 | [Tumbling Window Counts](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/queues/tumbling-window-counts) | Easy | Stream aggregation |
| 15 | [Drop Late Events With a Watermark](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/queues/drop-late-events-with-a-watermark) | Medium | Event time vs arrival order |
| 16 | [Pub/Sub Fan-Out](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/queues/pub-sub-fan-out) | Easy | One message, many subscribers |
| 17 | [A Delay Queue](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/queues/a-delay-queue) | Medium | Run jobs at a scheduled time |
| 18 | [Log Compaction](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/queues/log-compaction) | Medium | Keep the latest value per key |
| 19 | [Why Queues Explode Near 100%](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/queues/why-queues-explode-near-100) | Medium | Queueing theory |
| 20 | [Producer Batching (batch size and linger)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/queues/producer-batching-batch-size-and-linger) | Medium | Throughput vs latency |

## APIs & Rate Limiting

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Fixed-Window Rate Limiter](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/apis/fixed-window-rate-limiter) | Easy | Count per window |
| 2 | [The Window-Boundary Burst](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/apis/the-window-boundary-burst) | Medium | Fixed windows leak |
| 3 | [Sliding-Window Log](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/apis/sliding-window-log) | Medium | Exact, but stores every timestamp |
| 4 | [Sliding-Window Counter](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/apis/sliding-window-counter) | Medium | Approximate and cheap |
| 5 | [Token Bucket](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/apis/token-bucket) | Medium | Bursts up to a cap |
| 6 | [Leaky Bucket](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/apis/leaky-bucket) | Medium | A smooth output rate |
| 7 | [Per-User Quotas](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/apis/per-user-quotas) | Easy | One noisy client shouldn't hurt others |
| 8 | [Offset vs Cursor Pagination](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/apis/offset-vs-cursor-pagination) | Medium | Pages that don't skip rows |
| 9 | [Keyset Pagination With Ties](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/apis/keyset-pagination-with-ties) | Medium | Sort by (created_at, id) |
| 10 | [Idempotency Keys](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/apis/idempotency-keys) | Medium | Safe POST retries |
| 11 | [Pick the Status Code](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/apis/pick-the-status-code) | Easy | Speak HTTP |
| 12 | [Safe and Idempotent Methods](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/apis/safe-and-idempotent-methods) | Easy | Which calls can be retried blindly? |
| 13 | [Route by API Version](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/apis/route-by-api-version) | Easy | Serve the newest compatible version |
| 14 | [Conditional GET With ETags](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/apis/conditional-get-with-etags) | Medium | 304 Not Modified |
| 15 | [Chatty vs Batched vs Parallel Calls](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/apis/chatty-vs-batched-vs-parallel-calls) | Easy | Round trips add up |
| 16 | [Retries Within a Deadline](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/apis/retries-within-a-deadline) | Medium | Timeouts must add up |
| 17 | [A Circuit Breaker](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/apis/a-circuit-breaker) | Hard | Fail fast when a dependency is down |
| 18 | [An API Gateway](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/apis/an-api-gateway) | Medium | Auth, then route |
| 19 | [Sign Webhook Payloads (HMAC)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/apis/sign-webhook-payloads-hmac) | Medium | Prove the sender |
| 20 | [Polling vs Push](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/apis/polling-vs-push) | Easy | Wasted requests |

## URL Shortener & ID Generation

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Base62 Encode](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/ids/base62-encode) | Easy | Numbers to short codes |
| 2 | [Base62 Decode](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/ids/base62-decode) | Easy | Short codes back to numbers |
| 3 | [How Long Will the Codes Last?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/ids/how-long-will-the-codes-last) | Easy | Capacity planning |
| 4 | [Hash, Then Handle Collisions](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/ids/hash-then-handle-collisions) | Medium | Content-derived codes |
| 5 | [Hand Out ID Ranges](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/ids/hand-out-id-ranges) | Medium | Ticket server / range allocation |
| 6 | [A Key-Generation Service](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/ids/a-key-generation-service) | Medium | Pre-made keys and what a crash wastes |
| 7 | [Build a Snowflake ID](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/ids/build-a-snowflake-id) | Medium | Time + machine + sequence |
| 8 | [Decode a Snowflake ID](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/ids/decode-a-snowflake-id) | Easy | Read the timestamp back |
| 9 | [When the Sequence Runs Out](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/ids/when-the-sequence-runs-out) | Easy | IDs per millisecond |
| 10 | [The Clock Went Backwards](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/ids/the-clock-went-backwards) | Medium | Never issue a duplicate |
| 11 | [Time-Sortable String IDs](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/ids/time-sortable-string-ids) | Medium | ULID-style timestamps |
| 12 | [When Do Random IDs Collide?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/ids/when-do-random-ids-collide) | Medium | The birthday paradox |
| 13 | [A Bloom Filter for Taken Codes](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/ids/a-bloom-filter-for-taken-codes) | Medium | Maybe yes, definitely no |
| 14 | [Validate Custom Aliases](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/ids/validate-custom-aliases) | Easy | User-chosen short links |
| 15 | [Expire Old Links](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/ids/expire-old-links) | Easy | TTL cleanup |
| 16 | [Click Analytics](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/ids/click-analytics) | Easy | Aggregate redirect events |
| 17 | [Canonicalise URLs Before Shortening](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/ids/canonicalise-urls-before-shortening) | Medium | One long URL, one code |
| 18 | [Napkin Maths for a Shortener](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/ids/napkin-maths-for-a-shortener) | Easy | Size the system |
| 19 | [Machine IDs Across Data Centres](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/ids/machine-ids-across-data-centres) | Easy | Pack and check the worker bits |
| 20 | [Sequential IDs Leak Your Numbers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/ids/sequential-ids-leak-your-numbers) | Easy | Why public IDs should be random |

## News Feed, Chat & Notifications

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Push or Pull: Count the Work](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/feeds_chat/push-or-pull-count-the-work) | Easy | Fan-out on write vs read |
| 2 | [Hybrid Fan-Out for Celebrities](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/feeds_chat/hybrid-fan-out-for-celebrities) | Medium | Push most, pull the famous |
| 3 | [Merge a Pull Timeline](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/feeds_chat/merge-a-pull-timeline) | Medium | k-way merge |
| 4 | [Rank the Feed](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/feeds_chat/rank-the-feed) | Easy | Engagement with time decay |
| 5 | [Keep the Feed Diverse](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/feeds_chat/keep-the-feed-diverse) | Easy | Cap posts per author |
| 6 | [Order Chat Messages](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/feeds_chat/order-chat-messages) | Easy | Server-assigned sequence numbers |
| 7 | [Unread Counts](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/feeds_chat/unread-counts) | Easy | Latest seq minus last read |
| 8 | [Delivery Receipts](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/feeds_chat/delivery-receipts) | Easy | Sent → delivered → read |
| 9 | [Who Is Online?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/feeds_chat/who-is-online) | Easy | Presence from heartbeats |
| 10 | [Route Messages to Connection Servers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/feeds_chat/route-messages-to-connection-servers) | Medium | Session registry |
| 11 | [Group Chat Fan-Out](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/feeds_chat/group-chat-fan-out) | Easy | Every member gets a copy |
| 12 | [How Many WebSocket Servers?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/feeds_chat/how-many-websocket-servers) | Easy | Long-lived connections |
| 13 | [Sync After Reconnecting](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/feeds_chat/sync-after-reconnecting) | Medium | Catch up from the last seq |
| 14 | [Throttle the Typing Indicator](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/feeds_chat/throttle-the-typing-indicator) | Easy | At most one event per interval |
| 15 | [Notification Digests](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/feeds_chat/notification-digests) | Medium | Don't buzz the phone 30 times |
| 16 | [Respect Quiet Hours](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/feeds_chat/respect-quiet-hours) | Medium | Time zones matter |
| 17 | [Choose Notification Channels](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/feeds_chat/choose-notification-channels) | Easy | User preferences |
| 18 | [Handle Push-Token Responses](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/feeds_chat/handle-push-token-responses) | Medium | Clean up dead devices |
| 19 | [Sharded Like Counters](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/feeds_chat/sharded-like-counters) | Medium | Spread a hot counter |
| 20 | [How Much Chat Storage?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/feeds_chat/how-much-chat-storage) | Easy | Size the message store |

## Search, Storage, Reliability & the Interview

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Build an Inverted Index](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/search_reliability/build-an-inverted-index) | Easy | The heart of search |
| 2 | [Intersect Posting Lists](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/search_reliability/intersect-posting-lists) | Easy | AND queries |
| 3 | [Rank Results With TF-IDF](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/search_reliability/rank-results-with-tf-idf) | Medium | Rare words matter more |
| 4 | [Autocomplete](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/search_reliability/autocomplete) | Medium | Top suggestions for a prefix |
| 5 | [Top-K Trending Searches](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/search_reliability/top-k-trending-searches) | Easy | Heavy hitters |
| 6 | [Encode a Geohash](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/search_reliability/encode-a-geohash) | Medium | Locations as sortable strings |
| 7 | [Find Nearby Places](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/search_reliability/find-nearby-places) | Medium | Grid cells instead of scanning everything |
| 8 | [Chunk and Deduplicate Files](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/search_reliability/chunk-and-deduplicate-files) | Medium | Upload only what changed |
| 9 | [Resume an Interrupted Upload](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/search_reliability/resume-an-interrupted-upload) | Easy | Missing chunk ranges |
| 10 | [Pick a Multipart Part Size](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/search_reliability/pick-a-multipart-part-size) | Easy | Object storage limits |
| 11 | [Replication vs Erasure Coding](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/search_reliability/replication-vs-erasure-coding) | Easy | Durability per byte |
| 12 | [SLOs and Error Budgets](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/search_reliability/slos-and-error-budgets) | Easy | How much downtime may we spend? |
| 13 | [Burn-Rate Alerts](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/search_reliability/burn-rate-alerts) | Medium | Page on fast budget burn |
| 14 | [Latency Percentiles](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/search_reliability/latency-percentiles) | Easy | Averages hide the tail |
| 15 | [Retry Storms](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/search_reliability/retry-storms) | Medium | Retries multiply across layers |
| 16 | [Shed Load by Priority](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/search_reliability/shed-load-by-priority) | Medium | Degrade gracefully |
| 17 | [Which Disaster-Recovery Plan Fits?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/search_reliability/which-disaster-recovery-plan-fits) | Easy | RPO and RTO |
| 18 | [Promote or Roll Back the Canary?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/search_reliability/promote-or-roll-back-the-canary) | Medium | Automated canary analysis |
| 19 | [Budget Your Interview Time](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/search_reliability/budget-your-interview-time) | Easy | The framework, in minutes |
| 20 | [Self-Review a Design Answer](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/#/q/search_reliability/self-review-a-design-answer) | Easy | Did you cover everything? |

## Build

```bash
python3 handbook/build.py --book system-design
```

Sources live in `system-design/src/`: `topics/` (questions and solutions), `lessons/` and `theory/`.
