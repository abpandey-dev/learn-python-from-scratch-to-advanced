from lib import *
import bisect
import heapq
import math
import zlib
from collections import ChainMap, Counter, defaultdict
from itertools import islice

TOPIC(
    id="databases", title="Databases, Replication & Sharding", glyph="🗄",
    blurb="Choosing a database, indexes and the leftmost-prefix rule, LSM trees and compaction, replication lag, quorums (R + W > N) and read repair, hash vs range sharding, shard keys, hot shards, scatter-gather, joins, N+1 queries, lost updates and optimistic locking, connection pools and read replicas.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">index      → O(log n) lookups instead of scanning every row; slows writes a little
replication → copies for reads and failover; async = fast but replicas lag
quorum     → N copies, write to W, read from R; R + W > N means reads see the latest write
sharding   → split data by a shard key; hash = even spread, range = efficient range scans
little's law: connections needed = QPS × query time (s)</code></pre>
""")


RULES = [("relationships", "graph"), ("full-text", "search engine"), ("metrics", "time-series"),
         ("transactions", "relational"), ("flexible schema", "document"),
         ("massive writes", "wide-column"), ("key lookups", "key-value")]


Q(None, "Pick a Database", "Easy", "Match needs to a data model",
  "For each workload (a list of needs), return the first matching database type using the priority order in <code>RULES</code>, or 'relational' when nothing matches — a relational database is the safe default.",
  [(([["transactions", "reports"], ["key lookups", "sessions"], ["relationships", "recommendations"], ["massive writes", "key lookups"], ["full-text", "flexible schema"], ["reports"]],), ['relational', 'key-value', 'graph', 'wide-column', 'search engine', 'relational'])],
  ("An if/elif chain per workload.", "O(w · r)", "O(1)"),
  ("<code>next(...)</code> over the rule table.", "O(w · r)", "O(1)"),
  viz=(([["transactions"], ["key lookups"]],)))


@B
def pick_db(workloads):
    out = []
    for needs in workloads:
        if "relationships" in needs:
            out.append("graph")
        elif "full-text" in needs:
            out.append("search engine")
        elif "metrics" in needs:
            out.append("time-series")
        elif "transactions" in needs:
            out.append("relational")
        elif "flexible schema" in needs:
            out.append("document")
        elif "massive writes" in needs:
            out.append("wide-column")
        elif "key lookups" in needs:
            out.append("key-value")
        else:
            out.append("relational")
    return out


@O
def pick_db(workloads):
    return [next((db for need, db in RULES if need in needs), "relational") for needs in workloads]


Q(None, "What an Index Saves", "Easy", "Rows examined",
  "Count rows examined to find all rows where <code>field == value</code>: a full scan reads every row; an index (sorted keys) costs about ⌈log₂ n⌉ steps plus one per match. Return <code>(scan, indexed)</code> for each query.",
  [(([{"id": i, "city": ["Pune", "Delhi", "Goa", "Pune"][i % 4]} for i in range(1000)], [("city", "Goa"), ("id", 7)]), [(1000, 260), (1000, 11)])],
  ("Scan and count matches per query.", "O(q · n)", "O(1)"),
  ("Build a dict index per field once.", "O(n + q)", "O(n)"),
  viz=(([{"id": 1, "city": "Pune"}, {"id": 2, "city": "Goa"}], [("city", "Goa")])))


@B
def index_savings(rows, queries):
    out = []
    for field, value in queries:
        matches = sum(1 for r in rows if r[field] == value)
        out.append((len(rows), math.ceil(math.log2(len(rows))) + matches))
    return out


@O
def index_savings(rows, queries):
    index = defaultdict(Counter)
    for r in rows:
        for f, v in r.items():
            index[f][v] += 1
    steps = math.ceil(math.log2(len(rows)))
    return [(len(rows), steps + index[f][v]) for f, v in queries]


Q(None, "The Leftmost-Prefix Rule", "Medium", "Composite indexes",
  "An index on columns <code>cols</code> (in order) can be used for a query only from the left: stop at the first column the query doesn't filter on, and after the first column filtered by a range. Each query maps columns to 'eq' or 'range'. Return how many index columns each query can use.",
  [((["country", "city", "age"], [{"country": "eq", "city": "eq"}, {"city": "eq"}, {"country": "eq", "age": "range"}, {"country": "range", "city": "eq"}, {"country": "eq", "city": "eq", "age": "range"}]), [2, 0, 1, 1, 3])],
  ("Walk the index columns with a counter.", "O(q · c)", "O(1)"),
  ("Same walk with an early break.", "O(q · c)", "O(1)"),
  viz=((["a", "b"], [{"a": "eq", "b": "eq"}, {"b": "eq"}])))


@B
def usable_columns(cols, queries):
    out = []
    for q in queries:
        used = 0
        for c in cols:
            if c not in q:
                break
            used += 1
            if q[c] == "range":
                break
        out.append(used)
    return out


@O
def usable_columns(cols, queries):
    def use(q):
        n = 0
        for c in cols:
            if c not in q:
                return n
            n += 1
            if q[c] == "range":
                return n
        return n
    return [use(q) for q in queries]


Q(None, "Read From an LSM Tree", "Medium", "Memtable, then SSTables",
  "An LSM store checks the in-memory <code>memtable</code>, then the on-disk <code>sstables</code> from newest to oldest; the first hit wins and a value of None is a tombstone (deleted). Return the value for each key (None if deleted or absent) and how many tables were checked in total.",
  [(({"k3": 30}, [{"k1": 11, "k2": None}, {"k1": 10, "k2": 20, "k4": 40}], ["k1", "k2", "k3", "k4", "k5"]), ([11, None, 30, 40, None], 11))],
  ("Loop through the tables for each key, counting.", "O(k · t)", "O(1)"),
  ("Same, with a generator over the table list.", "O(k · t)", "O(1)"),
  viz=(({"a": 1}, [{"b": 2}], ["a", "b"])))


@B
def lsm_get(memtable, sstables, keys):
    values, checked = [], 0
    for k in keys:
        found = None
        for table in [memtable] + sstables:
            checked += 1
            if k in table:
                found = table[k]
                break
        values.append(found)
    return (values, checked)


@O
def lsm_get(memtable, sstables, keys):
    tables, values, checked = [memtable, *sstables], [], 0
    for k in keys:
        i = next((i for i, t in enumerate(tables) if k in t), None)
        checked += len(tables) if i is None else i + 1
        values.append(None if i is None else tables[i][k])
    return (values, checked)


Q(None, "Compact the SSTables", "Medium", "Merge and drop tombstones",
  "Compaction merges SSTables (given oldest first) into one: the newest value of each key wins, and tombstones (None) are dropped. Return the sorted <code>(key, value)</code> pairs.",
  [(([{"a": 1, "b": 2, "c": 3}, {"b": 20, "d": 4}, {"a": None, "e": 5}],), [('b', 20), ('c', 3), ('d', 4), ('e', 5)])],
  ("Update a dict table by table.", "O(total)", "O(keys)"),
  ("<code>ChainMap</code> over the tables newest first.", "O(total)", "O(keys)"),
  viz=(([{"a": 1}, {"a": None, "b": 2}],)))


@B
def compact(sstables):
    merged = {}
    for t in sstables:
        for k, v in t.items():
            merged[k] = v
    return sorted((k, v) for k, v in merged.items() if v is not None)


@O
def compact(sstables):
    view = ChainMap(*reversed(sstables))
    return sorted((k, view[k]) for k in view if view[k] is not None)


Q(None, "Reading From a Lagging Replica", "Medium", "Async replication",
  "Writes <code>(time, key, value)</code> reach the replica <code>lag</code> seconds later. For each read <code>(time, key)</code> served by the replica, return the value it sees (starting from <code>initial</code>) and how many reads were stale compared with the primary.",
  [(({"bal": 100}, [(1, "bal", 80), (5, "bal", 50)], 3, [(2, "bal"), (4, "bal"), (6, "bal"), (9, "bal")]), ([100, 80, 80, 50], 2))],
  ("Replay applicable writes for each read.", "O(r · w)", "O(k)"),
  ("Same, as the last visible write per key.", "O(r · w)", "O(k)"),
  viz=(({"x": 0}, [(1, "x", 1)], 2, [(2, "x"), (3, "x")])))


@B
def replica_reads(initial, writes, lag, reads):
    seen, stale = [], 0
    for t, k in reads:
        replica, primary = dict(initial), dict(initial)
        for wt, wk, wv in writes:
            if wt <= t:
                primary[wk] = wv
            if wt + lag <= t:
                replica[wk] = wv
        seen.append(replica[k])
        if replica[k] != primary[k]:
            stale += 1
    return (seen, stale)


@O
def replica_reads(initial, writes, lag, reads):
    def value(k, t):
        return next((v for wt, wk, v in reversed(writes) if wk == k and wt <= t), initial[k])
    seen = [value(k, t - lag) for t, k in reads]
    return (seen, sum(s != value(k, t) for s, (t, k) in zip(seen, reads)))


Q(None, "Quorums: R + W > N", "Easy", "Tunable consistency",
  "For each <code>(N, W, R)</code>, return <code>(reads always see the latest write?, replica failures a write tolerates, failures a read tolerates)</code>.",
  [(([(3, 2, 2), (3, 1, 1), (3, 3, 1), (5, 3, 3), (5, 1, 5)],), [(True, 1, 1), (False, 2, 2), (True, 0, 2), (True, 2, 2), (True, 4, 0)])],
  ("Compute each term with if-statements.", "O(c)", "O(c)"),
  ("A comprehension.", "O(c)", "O(c)"),
  viz=(([(3, 2, 2)],)))


@B
def quorum(configs):
    out = []
    for n, w, r in configs:
        strong = False
        if r + w > n:
            strong = True
        out.append((strong, n - w, n - r))
    return out


@O
def quorum(configs):
    return [(r + w > n, n - w, n - r) for n, w, r in configs]


Q(None, "Read Repair", "Easy", "Pick the newest, fix the rest",
  "A quorum read got <code>(replica, version, value)</code> replies. Return the value with the highest version and the replicas (sorted) that hold an older version and need repair.",
  [(([("r1", 7, "blue"), ("r2", 9, "green"), ("r3", 7, "blue")],), ('green', ['r1', 'r3']))],
  ("Find the max version with a loop, then collect the others.", "O(n)", "O(n)"),
  ("<code>max</code> with a key.", "O(n)", "O(n)"),
  viz=(([("r1", 1, "a"), ("r2", 2, "b")],)))


@B
def read_repair(replies):
    best = replies[0]
    for rep in replies:
        if rep[1] > best[1]:
            best = rep
    stale = []
    for rep in replies:
        if rep[1] < best[1]:
            stale.append(rep[0])
    return (best[2], sorted(stale))


@O
def read_repair(replies):
    _, v, value = max(replies, key=lambda r: r[1])
    return (value, sorted(r for r, ver, _ in replies if ver < v))


Q(None, "Hash Sharding", "Easy", "Even spread",
  "Assign each key to shard <code>crc32(key) % n</code>. Return how many keys land on each shard.",
  [(([f"user:{i}" for i in range(1000)], 3), [330, 326, 344])],
  ("Count with a list.", "O(k)", "O(n)"),
  ("<code>Counter</code>.", "O(k)", "O(n)"),
  viz=(([f"user:{i}" for i in range(8)], 2)))


@B
def hash_shards(keys, n):
    counts = [0] * n
    for k in keys:
        counts[zlib.crc32(k.encode()) % n] += 1
    return counts


@O
def hash_shards(keys, n):
    c = Counter(zlib.crc32(k.encode()) % n for k in keys)
    return [c[i] for i in range(n)]


Q(None, "Range Sharding and the Hot Shard", "Medium", "Sequential keys pile up",
  "Shards own key ranges split at <code>bounds</code> (shard i holds keys below bounds[i]; the last shard holds the rest). Return keys per shard. Try it with timestamps: every new write lands on the last shard.",
  [(([100, 200, 300], [5, 150, 210, 250, 299, 320, 330, 340, 350, 360]), [1, 1, 3, 5])],
  ("Compare each key with the bounds in order.", "O(k · b)", "O(b)"),
  ("<code>bisect_right</code>.", "O(k log b)", "O(b)"),
  viz=(([100], [5, 150])))


@B
def range_shards(bounds, keys):
    counts = [0] * (len(bounds) + 1)
    for k in keys:
        i = 0
        while i < len(bounds) and k >= bounds[i]:
            i += 1
        counts[i] += 1
    return counts


@O
def range_shards(bounds, keys):
    c = Counter(bisect.bisect_right(bounds, k) for k in keys)
    return [c[i] for i in range(len(bounds) + 1)]


Q(None, "Choose a Shard Key", "Medium", "Avoid skew",
  "Hash-shard <code>records</code> on each candidate field into <code>n</code> shards. Return the largest shard's share (%, rounded to 1) for each candidate, and the candidate with the smallest maximum.",
  [(([{"user": f"u{i}", "country": "IN" if i % 10 < 8 else "US", "day": f"d{i % 3}"} for i in range(200)], ["user", "country", "day"], 4), ({'user': 25.0, 'country': 100.0, 'day': 66.5}, 'user'))],
  ("Count shard sizes per candidate.", "O(c · r)", "O(n)"),
  ("<code>Counter</code> per candidate and <code>min</code>.", "O(c · r)", "O(n)"),
  viz=(([{"user": "u1", "country": "IN"}, {"user": "u2", "country": "IN"}], ["user", "country"], 2)))


@B
def shard_key(records, candidates, n):
    shares = {}
    for c in candidates:
        counts = [0] * n
        for r in records:
            counts[zlib.crc32(str(r[c]).encode()) % n] += 1
        shares[c] = round(max(counts) / len(records) * 100, 1)
    best = candidates[0]
    for c in candidates:
        if shares[c] < shares[best]:
            best = c
    return (shares, best)


@O
def shard_key(records, candidates, n):
    shares = {c: round(max(Counter(zlib.crc32(str(r[c]).encode()) % n for r in records).values()) / len(records) * 100, 1)
              for c in candidates}
    return (shares, min(candidates, key=shares.get))


Q(None, "Split Oversized Shards", "Medium", "Resharding by halves",
  "Shards are sorted key lists. Split any shard larger than <code>max_size</code> in half (left gets the smaller half), repeating until all fit. Return the new shard sizes in key order.",
  [(([list(range(10)), list(range(10, 13)), list(range(13, 30))], 4), [2, 3, 2, 3, 3, 4, 4, 4, 2, 3])],
  ("Loop until no shard is too big.", "O(n · s)", "O(n)"),
  ("Recursive split per shard.", "O(n)", "O(n)"),
  viz=(([list(range(6))], 2)))


@B
def split_shards(shards, max_size):
    shards = [list(s) for s in shards]
    changed = True
    while changed:
        changed = False
        out = []
        for s in shards:
            if len(s) > max_size:
                out += [s[:len(s) // 2], s[len(s) // 2:]]
                changed = True
            else:
                out.append(s)
        shards = out
    return [len(s) for s in shards]


@O
def split_shards(shards, max_size):
    def sizes(n):
        return [n] if n <= max_size else sizes(n // 2) + sizes(n - n // 2)
    return [x for s in shards for x in sizes(len(s))]


Q(None, "Scatter-Gather Queries", "Easy", "Queries without the shard key",
  "A query with a shard key goes to one shard; a query without (None) goes to every shard, waits for the slowest, then merges (<code>merge_ms</code>). Return each query's latency.",
  [(([12, 9, 30, 11], 4, [0, None, 2, None, 3]), [12, 34, 30, 34, 11])],
  ("If/else per query.", "O(q · s)", "O(1)"),
  ("Precompute the scatter latency once.", "O(q + s)", "O(1)"),
  viz=(([10, 20], 2, [0, None])))


@B
def scatter(shard_ms, merge_ms, queries):
    out = []
    for q in queries:
        if q is None:
            out.append(max(shard_ms) + merge_ms)
        else:
            out.append(shard_ms[q])
    return out


@O
def scatter(shard_ms, merge_ms, queries):
    everywhere = max(shard_ms) + merge_ms
    return [everywhere if q is None else shard_ms[q] for q in queries]


Q(None, "Global Top-K Across Shards", "Medium", "Merge sorted results",
  "Each shard returns its scores sorted from high to low. Return the global top <code>k</code>.",
  [(([[98, 90, 75, 60], [99, 70, 65], [95, 94, 93, 10]], 5), [99, 98, 95, 94, 93])],
  ("Concatenate and sort.", "O(n log n)", "O(n)"),
  ("<code>heapq.merge(..., reverse=True)</code> and stop after k.", "O(k log s)", "O(s)"),
  viz=(([[9, 5], [8, 7]], 3)))


@B
def top_k(shards, k):
    return sorted([x for s in shards for x in s], reverse=True)[:k]


@O
def top_k(shards, k):
    return list(islice(heapq.merge(*shards, reverse=True), k))


Q(None, "Join in the Application", "Easy", "Hash join",
  "After sharding, a join may happen in your code. Return <code>(name, total order amount)</code> for every user (0 when no orders), sorted by name.",
  [(([(1, "Asha"), (2, "Ravi"), (3, "Meera")], [(1, 250), (3, 99), (1, 50), (4, 10)]), [('Asha', 300), ('Meera', 99), ('Ravi', 0)])],
  ("Nested loops: for each user scan all orders.", "O(u · o)", "O(u)"),
  ("Sum orders into a dict, then look up each user.", "O(u + o)", "O(u)"),
  viz=(([(1, "A")], [(1, 5)])))


@B
def app_join(users, orders):
    out = []
    for uid, name in users:
        total = 0
        for ouid, amount in orders:
            if ouid == uid:
                total += amount
        out.append((name, total))
    return sorted(out)


@O
def app_join(users, orders):
    totals = defaultdict(int)
    for uid, amount in orders:
        totals[uid] += amount
    return sorted((name, totals[uid]) for uid, name in users)


Q(None, "The N+1 Query Problem", "Easy", "Batch your lookups",
  "Loading posts and then each post's author one by one costs 1 + n queries. Batching unique author ids in groups of <code>batch</code> costs 1 + ⌈unique / batch⌉. Return both counts.",
  [(([7, 3, 7, 9, 3, 1, 7, 2, 9, 4], 3), (11, 3))],
  ("Count with a loop and a set.", "O(n)", "O(n)"),
  ("Arithmetic on <code>len(set(...))</code>.", "O(n)", "O(n)"),
  viz=(([1, 1, 2], 2)))


@B
def n_plus_one(author_ids, batch):
    naive = 1
    for _ in author_ids:
        naive += 1
    unique = []
    for a in author_ids:
        if a not in unique:
            unique.append(a)
    batched = 1
    remaining = len(unique)
    while remaining > 0:
        batched += 1
        remaining -= batch
    return (naive, batched)


@O
def n_plus_one(author_ids, batch):
    return (1 + len(author_ids), 1 + math.ceil(len(set(author_ids)) / batch))


Q(None, "The Lost Update", "Medium", "Read-modify-write races",
  "Two transactions each read a counter into a local copy, then write back copy + delta. Run the interleaved <code>schedule</code> of <code>(tx, 'read')</code> and <code>(tx, 'write', delta)</code>. Return <code>(final value with read-modify-write, final value with atomic increments)</code>.",
  [((100, [("T1", "read"), ("T2", "read"), ("T1", "write", 10), ("T2", "write", -30)]), (70, 80)),
   ((100, [("T1", "read"), ("T1", "write", 10), ("T2", "read"), ("T2", "write", -30)]), (80, 80))],
  ("Simulate with a dict of local copies.", "O(s)", "O(t)"),
  ("Same; atomic = start + sum of deltas.", "O(s)", "O(t)"),
  viz=((0, [("A", "read"), ("B", "read"), ("A", "write", 1), ("B", "write", 1)])))


@B
def lost_update(start, schedule):
    value, local = start, {}
    for step in schedule:
        if step[1] == "read":
            local[step[0]] = value
        else:
            value = local[step[0]] + step[2]
    atomic = start
    for step in schedule:
        if step[1] == "write":
            atomic += step[2]
    return (value, atomic)


@O
def lost_update(start, schedule):
    value, local = start, {}
    for tx, op, *delta in schedule:
        if op == "read":
            local[tx] = value
        else:
            value = local[tx] + delta[0]
    return (value, start + sum(s[2] for s in schedule if s[1] == "write"))


Q(None, "Optimistic Locking", "Easy", "Compare the version, then write",
  "A row has <code>value</code> and <code>version</code>. Each update <code>(client, expected_version, new_value)</code> succeeds only if the version still matches, then bumps it. Return <code>(final value, final version, rejected clients)</code>.",
  [(("draft", 1, [("alice", 1, "v-alice"), ("bob", 1, "v-bob"), ("bob", 2, "v-bob2"), ("carol", 2, "v-carol")]), ('v-bob2', 3, ['bob', 'carol']))],
  ("Loop with if-statements.", "O(u)", "O(u)"),
  ("Same loop with tuple updates.", "O(u)", "O(u)"),
  viz=(("x", 1, [("a", 1, "y"), ("b", 1, "z")])))


@B
def optimistic(value, version, updates):
    rejected = []
    for client, expected, new in updates:
        if expected == version:
            value = new
            version = version + 1
        else:
            rejected.append(client)
    return (value, version, rejected)


@O
def optimistic(value, version, updates):
    rejected = []
    for client, expected, new in updates:
        if expected != version:
            rejected.append(client)
            continue
        value, version = new, version + 1
    return (value, version, rejected)


Q(None, "How Many Database Connections?", "Easy", "Little's law",
  "Connections in use = QPS × query time. Return <code>(connections needed, pool size per app instance, fits under the database's max connections?)</code>.",
  [((4000, 15, 12, 100), (60, 5, True)), ((20000, 25, 40, 300), (500, 13, False))],
  ("Multiply and ceiling-divide with loops.", "O(1)", "O(1)"),
  ("<code>math.ceil</code>.", "O(1)", "O(1)"),
  viz=((1000, 10, 2, 50)))


@B
def pool_size(qps_, query_ms, instances, db_max):
    needed = qps_ * query_ms / 1000
    if needed != int(needed):
        needed = int(needed) + 1
    needed = int(needed)
    per = needed // instances
    if per * instances < needed:
        per += 1
    return (needed, per, needed <= db_max)


@O
def pool_size(qps_, query_ms, instances, db_max):
    needed = math.ceil(qps_ * query_ms / 1000)
    return (needed, math.ceil(needed / instances), needed <= db_max)


Q(None, "How Many Read Replicas?", "Easy", "Replicas also apply every write",
  "Every node can serve <code>node_qps</code>; each replica spends <code>write_qps</code> of that applying replicated writes. Reads go to replicas only. Return <code>(replicas needed, primary utilisation %)</code>, rounded to 1.",
  [((50000, 2000, 10000), (7, 20.0)), ((9000, 6000, 8000), (5, 75.0))],
  ("Add replicas until capacity covers the reads.", "O(r)", "O(1)"),
  ("Ceiling division.", "O(1)", "O(1)"),
  viz=((1000, 100, 500)))


@B
def read_replicas(read_qps, write_qps, node_qps):
    replicas = 0
    while replicas * (node_qps - write_qps) < read_qps:
        replicas += 1
    return (replicas, round(write_qps / node_qps * 100, 1))


@O
def read_replicas(read_qps, write_qps, node_qps):
    return (math.ceil(read_qps / (node_qps - write_qps)), round(write_qps / node_qps * 100, 1))
