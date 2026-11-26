from lib import *
import hashlib
import zlib
from collections import defaultdict

TOPIC(
    id="consistency", title="Consistency & Distributed Systems", glyph="🧭",
    blurb="What happens when machines disagree: CAP and PACELC, Lamport and vector clocks, clock skew, last-writer-wins, CRDTs, idempotency, two-phase commit vs sagas, majorities and split brain, Raft voting, leases and fencing tokens, heartbeats, gossip and Merkle-tree anti-entropy.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">CAP: during a network Partition choose Consistency or Availability
PACELC: else (normal operation) choose Latency or Consistency
majority quorum: n // 2 + 1 nodes; tolerates (n - 1) // 2 failures → use odd cluster sizes
Lamport: on send/local c += 1; on receive c = max(c, msg) + 1
idempotent: doing it twice has the same effect as once (dedupe by request id)</code></pre>
""")


Q(None, "CP or AP?", "Easy", "What to give up during a partition",
  "For each system, return 'CP' (refuse requests rather than return wrong data) if a stale or conflicting answer is harmful, else 'AP' (stay available, reconcile later). Each item is <code>(name, stale_is_harmful)</code>.",
  [(([("bank balance", True), ("social likes", False), ("seat booking", True), ("shopping cart", False), ("DNS", False), ("distributed lock", True)],), [('bank balance', 'CP'), ('social likes', 'AP'), ('seat booking', 'CP'), ('shopping cart', 'AP'), ('DNS', 'AP'), ('distributed lock', 'CP')])],
  ("If/else per system.", "O(n)", "O(n)"),
  ("A comprehension.", "O(n)", "O(n)"),
  viz=(([("bank balance", True), ("likes", False)],)))


@B
def cap_choice(systems):
    out = []
    for name, harmful in systems:
        if harmful:
            out.append((name, "CP"))
        else:
            out.append((name, "AP"))
    return out


@O
def cap_choice(systems):
    return [(name, "CP" if harmful else "AP") for name, harmful in systems]


Q(None, "Lamport Clocks", "Medium", "Logical time",
  "Events run in this global order: <code>(process, 'local'|'send'|'recv', message)</code>. Apply Lamport's rules and return each event's timestamp.",
  [(([("A", "local", None), ("A", "send", "m1"), ("B", "local", None), ("B", "recv", "m1"), ("B", "send", "m2"), ("A", "local", None), ("C", "recv", "m2"), ("A", "recv", "m2")],), [1, 2, 1, 3, 4, 3, 5, 5])],
  ("Clock dict per process and if/elif.", "O(e)", "O(p + m)"),
  ("Same, compacted with <code>max</code>.", "O(e)", "O(p + m)"),
  viz=(([("A", "send", "m"), ("B", "recv", "m")],)))


@B
def lamport(events):
    clock, sent, out = {}, {}, []
    for p, kind, msg in events:
        c = clock.get(p, 0)
        if kind == "recv":
            c = max(c, sent[msg]) + 1
        else:
            c = c + 1
        if kind == "send":
            sent[msg] = c
        clock[p] = c
        out.append(c)
    return out


@O
def lamport(events):
    clock, sent, out = defaultdict(int), {}, []
    for p, kind, msg in events:
        clock[p] = max(clock[p], sent[msg] if kind == "recv" else 0) + 1
        if kind == "send":
            sent[msg] = clock[p]
        out.append(clock[p])
    return out


Q(None, "Compare Vector Clocks", "Medium", "Happened-before or concurrent?",
  "For each pair of vector clocks (dicts node → counter, missing = 0) return 'before', 'after', 'equal' or 'concurrent'. Concurrent versions are real conflicts the application must merge.",
  [(([({"A": 1, "B": 2}, {"A": 2, "B": 2}), ({"A": 3}, {"A": 2, "B": 1}), ({"A": 1, "B": 1}, {"A": 1, "B": 1}), ({"A": 2, "B": 0}, {"A": 1})],), ['before', 'concurrent', 'equal', 'after'])],
  ("Track 'some less' and 'some greater' flags.", "O(p · k)", "O(k)"),
  ("<code>all</code> over the union of keys.", "O(p · k)", "O(k)"),
  viz=(([({"A": 1}, {"A": 2})],)))


@B
def compare_vc(pairs):
    out = []
    for a, b in pairs:
        less = greater = False
        for k in set(a) | set(b):
            x, y = a.get(k, 0), b.get(k, 0)
            if x < y:
                less = True
            if x > y:
                greater = True
        if less and greater:
            out.append("concurrent")
        elif less:
            out.append("before")
        elif greater:
            out.append("after")
        else:
            out.append("equal")
    return out


@O
def compare_vc(pairs):
    def cmp(a, b):
        keys = a.keys() | b.keys()
        le = all(a.get(k, 0) <= b.get(k, 0) for k in keys)
        ge = all(a.get(k, 0) >= b.get(k, 0) for k in keys)
        return "equal" if le and ge else "before" if le else "after" if ge else "concurrent"
    return [cmp(a, b) for a, b in pairs]


Q(None, "Run Vector Clocks", "Medium", "One counter per process",
  "Using the same event format as the Lamport question, keep a vector clock per process (on receive, take the element-wise max, then increment your own entry). Return each process's final clock as a sorted list of <code>(node, counter)</code> pairs.",
  [(([("A", "local", None), ("A", "send", "m1"), ("B", "recv", "m1"), ("B", "send", "m2"), ("C", "local", None), ("C", "recv", "m2")],), {'A': [('A', 2)], 'B': [('A', 2), ('B', 2)], 'C': [('A', 2), ('B', 2), ('C', 2)]})],
  ("Dicts of dicts with explicit loops.", "O(e · p)", "O(p²)"),
  ("<code>defaultdict(Counter)</code> and dict merges.", "O(e · p)", "O(p²)"),
  viz=(([("A", "send", "m"), ("B", "recv", "m")],)))


@B
def vector_clocks(events):
    clocks, sent = {}, {}
    for p, kind, msg in events:
        if p not in clocks:
            clocks[p] = {}
        if kind == "recv":
            for k, v in sent[msg].items():
                if v > clocks[p].get(k, 0):
                    clocks[p][k] = v
        clocks[p][p] = clocks[p].get(p, 0) + 1
        if kind == "send":
            sent[msg] = dict(clocks[p])
    result = {}
    for p in clocks:
        result[p] = sorted(clocks[p].items())
    return result


@O
def vector_clocks(events):
    clocks, sent = defaultdict(dict), {}
    for p, kind, msg in events:
        c = clocks[p]
        if kind == "recv":
            c.update({k: max(v, c.get(k, 0)) for k, v in sent[msg].items()})
        c[p] = c.get(p, 0) + 1
        if kind == "send":
            sent[msg] = dict(c)
    return {p: sorted(c.items()) for p, c in clocks.items()}


Q(None, "Clock Skew Reorders Events", "Medium", "Why wall clocks lie",
  "Events <code>(node, true_ms, name)</code> are stamped with the node's wall clock = true time + <code>skew[node]</code>. Return the order a system sorting by wall clock would see, and how many pairs of events end up in the wrong order.",
  [(([("n1", 100, "create"), ("n2", 105, "update"), ("n1", 110, "delete"), ("n3", 120, "restore")], {"n1": 0, "n2": -20, "n3": -15}), (['update', 'create', 'restore', 'delete'], 2))],
  ("Sort, then compare every pair.", "O(n²)", "O(n)"),
  ("Same pair count with a comprehension.", "O(n²)", "O(n)"),
  viz=(([("a", 1, "x"), ("b", 2, "y")], {"a": 0, "b": -5})))


@B
def skew_order(events, skew):
    stamped = sorted(events, key=lambda e: e[1] + skew[e[0]])
    order = [e[2] for e in stamped]
    wrong = 0
    for i in range(len(stamped)):
        for j in range(i + 1, len(stamped)):
            if stamped[i][1] > stamped[j][1]:
                wrong += 1
    return (order, wrong)


@O
def skew_order(events, skew):
    s = sorted(events, key=lambda e: e[1] + skew[e[0]])
    return ([e[2] for e in s], sum(s[i][1] > s[j][1] for i in range(len(s)) for j in range(i + 1, len(s))))


Q(None, "Last Writer Wins", "Easy", "Simple conflict resolution",
  "Concurrent writes <code>(value, timestamp, node)</code> to the same key are resolved by the highest timestamp, ties broken by node id. Return the surviving value and the values silently lost.",
  [(([("blue", 1005, "n2"), ("green", 1005, "n3"), ("red", 1001, "n1")],), ('green', ['blue', 'red']))],
  ("Find the max with a loop.", "O(n)", "O(n)"),
  ("<code>max</code> on (timestamp, node).", "O(n)", "O(n)"),
  viz=(([("a", 1, "n1"), ("b", 2, "n2")],)))


@B
def lww(writes):
    best = writes[0]
    for w in writes[1:]:
        if (w[1], w[2]) > (best[1], best[2]):
            best = w
    lost = []
    for w in writes:
        if w is not best:
            lost.append(w[0])
    return (best[0], sorted(lost))


@O
def lww(writes):
    win = max(writes, key=lambda w: (w[1], w[2]))
    return (win[0], sorted(w[0] for w in writes if w is not win))


Q(None, "Merge a Grow-Only Counter (CRDT)", "Easy", "Conflict-free by design",
  "Each replica keeps a count per node. Merging takes the max per node; the counter's value is the sum. Return the merged state (sorted pairs) and the value. Merging in any order gives the same result.",
  [(([{"a": 5, "b": 2}, {"a": 3, "b": 4, "c": 1}, {"c": 2}],), ([('a', 5), ('b', 4), ('c', 2)], 11))],
  ("Loop over replicas and nodes.", "O(r · n)", "O(n)"),
  ("Dict comprehension over the union of nodes.", "O(r · n)", "O(n)"),
  viz=(([{"a": 1}, {"a": 2, "b": 1}],)))


@B
def gcounter(replicas):
    merged = {}
    for r in replicas:
        for node, c in r.items():
            if c > merged.get(node, 0):
                merged[node] = c
    return (sorted(merged.items()), sum(merged.values()))


@O
def gcounter(replicas):
    nodes = set().union(*replicas)
    merged = {n: max(r.get(n, 0) for r in replicas) for n in nodes}
    return (sorted(merged.items()), sum(merged.values()))


Q(None, "Make the Payment Idempotent", "Medium", "Retries without double charges",
  "Clients retry on timeouts, so the same request can arrive twice. Apply each <code>(request_id, amount)</code> debit once; repeats return the stored result. Return <code>(final balance, duplicates ignored)</code>; compare with applying everything.",
  [((1000, [("r1", 200), ("r2", 50), ("r1", 200), ("r3", 300), ("r2", 50), ("r1", 200)]), (450, 3))],
  ("A list of seen ids.", "O(n²)", "O(n)"),
  ("A set of seen ids.", "O(n)", "O(n)"),
  viz=((100, [("a", 10), ("a", 10)])))


@B
def idempotent(balance, requests):
    seen, dupes = [], 0
    for rid, amount in requests:
        if rid in seen:
            dupes += 1
        else:
            seen.append(rid)
            balance -= amount
    return (balance, dupes)


@O
def idempotent(balance, requests):
    done = {}
    for rid, amount in requests:
        done.setdefault(rid, amount)
    return (balance - sum(done.values()), len(requests) - len(done))


Q(None, "Two-Phase Commit", "Medium", "All or nothing across services",
  "For each scenario <code>(votes, coordinator_alive_after_prepare)</code>: if any participant votes 'no', 'abort'; if all vote 'yes' but the coordinator crashes before sending the decision, participants are stuck 'blocked' holding locks; otherwise 'commit'.",
  [(([(["yes", "yes", "yes"], True), (["yes", "no", "yes"], True), (["yes", "yes"], False), (["no", "yes"], False)],), ['commit', 'abort', 'blocked', 'abort'])],
  ("If/elif per scenario.", "O(s · p)", "O(s)"),
  ("A conditional expression.", "O(s · p)", "O(s)"),
  viz=(([(["yes", "yes"], True)],)))


@B
def two_pc(scenarios):
    out = []
    for votes, alive in scenarios:
        if "no" in votes:
            out.append("abort")
        elif not alive:
            out.append("blocked")
        else:
            out.append("commit")
    return out


@O
def two_pc(scenarios):
    return ["abort" if "no" in v else "commit" if alive else "blocked" for v, alive in scenarios]


Q(None, "Run a Saga", "Medium", "Compensate instead of rolling back",
  "A saga runs local steps in order. If a step fails, run the compensations of the completed steps in reverse. Steps are <code>(name, succeeds)</code>; return the actions executed (compensation of X is 'undo X').",
  [(([("reserve stock", True), ("charge card", True), ("book courier", False), ("send email", True)],), ['reserve stock', 'charge card', 'book courier', 'undo charge card', 'undo reserve stock']),
   (([("reserve stock", True), ("charge card", True)],), ['reserve stock', 'charge card'])],
  ("Loop, and on failure loop back over done steps.", "O(n)", "O(n)"),
  ("Same with <code>reversed</code>.", "O(n)", "O(n)"),
  viz=(([("a", True), ("b", False)],)))


@B
def saga(steps):
    actions, done = [], []
    for name, ok in steps:
        actions.append(name)
        if not ok:
            i = len(done) - 1
            while i >= 0:
                actions.append("undo " + done[i])
                i -= 1
            return actions
        done.append(name)
    return actions


@O
def saga(steps):
    actions = []
    for i, (name, ok) in enumerate(steps):
        actions.append(name)
        if not ok:
            return actions + [f"undo {n}" for n, _ in reversed(steps[:i])]
    return actions


Q(None, "Which Side Keeps Working After a Split?", "Easy", "Majority quorums",
  "A cluster of <code>n</code> nodes splits into groups of the given sizes. Only a group with a strict majority may elect a leader and accept writes (this prevents split brain). Return a bool per group and the failures an n-node cluster tolerates.",
  [((5, [3, 2]), ([True, False], 2)), ((4, [2, 2]), ([False, False], 1)), ((7, [3, 2, 2]), ([False, False, False], 3))],
  ("Compare each size with n/2.", "O(g)", "O(g)"),
  ("Comprehension with <code>n // 2 + 1</code>.", "O(g)", "O(g)"),
  viz=((3, [2, 1])))


@B
def majority(n, groups):
    out = []
    for g in groups:
        out.append(g > n / 2)
    return (out, (n - 1) // 2)


@O
def majority(n, groups):
    return ([g >= n // 2 + 1 for g in groups], (n - 1) // 2)


Q(None, "Who Wins the Raft Vote?", "Medium", "Up-to-date logs only",
  "A candidate with log end <code>(last_term, last_index)</code> asks the other nodes for votes. A node votes yes only if the candidate's log is at least as up-to-date as its own (compare term, then index). The candidate votes for itself. Return <code>(votes, wins a majority?)</code> for each candidate.",
  [(([(5, 10), (5, 8), (4, 20)], [(5, 9), (5, 10), (4, 30), (3, 2)]), [(5, True), (3, True), (2, False)])],
  ("Count with explicit comparisons.", "O(c · n)", "O(1)"),
  ("Tuple comparison inside <code>sum</code>.", "O(c · n)", "O(1)"),
  viz=(([(2, 3)], [(2, 2), (1, 9)])))


@B
def raft_vote(candidates, voters):
    n = len(voters) + 1
    out = []
    for ct, ci in candidates:
        votes = 1
        for vt, vi in voters:
            if ct > vt or (ct == vt and ci >= vi):
                votes += 1
        out.append((votes, votes > n // 2))
    return out


@O
def raft_vote(candidates, voters):
    need = (len(voters) + 1) // 2 + 1
    out = []
    for cand in candidates:
        votes = 1 + sum(cand >= v for v in voters)
        out.append((votes, votes >= need))
    return out


Q(None, "Fencing Tokens", "Medium", "Stop the zombie lock holder",
  "A lock service hands out increasing tokens. The storage remembers the highest token seen and rejects writes with a lower one — so a client that paused (GC, network) after its lock expired can't corrupt data. Writes are <code>(client, token)</code>; return the accepted clients in order.",
  [(([("A", 33), ("B", 34), ("A", 33), ("B", 34), ("C", 35), ("B", 34)],), ['A', 'B', 'B', 'C'])],
  ("Track the max token in a loop.", "O(n)", "O(1)"),
  ("Same, one condition.", "O(n)", "O(1)"),
  viz=(([("A", 1), ("B", 2), ("A", 1)],)))


@B
def fencing(writes):
    highest, accepted = -1, []
    for client, token in writes:
        if token >= highest:
            highest = token
            accepted.append(client)
    return accepted


@O
def fencing(writes):
    highest, accepted = -1, []
    for client, token in writes:
        if token >= highest:
            highest, accepted = token, accepted + [client]
    return accepted


Q(None, "When Did the Leader Lease Lapse?", "Easy", "Leases",
  "A leader renews a lease of <code>lease</code> seconds at each heartbeat time. Return the <code>(start, end)</code> gaps where the lease had expired before the next renewal (no one may act as leader then).",
  [(([0, 4, 8, 20, 23, 35], 5), [(13, 20), (28, 35)])],
  ("Compare consecutive heartbeats.", "O(n)", "O(n)"),
  ("<code>zip</code> over neighbours.", "O(n)", "O(n)"),
  viz=(([0, 10], 5)))


@B
def lease_gaps(beats, lease):
    gaps = []
    for i in range(1, len(beats)):
        if beats[i] - beats[i - 1] > lease:
            gaps.append((beats[i - 1] + lease, beats[i]))
    return gaps


@O
def lease_gaps(beats, lease):
    return [(a + lease, b) for a, b in zip(beats, beats[1:]) if b - a > lease]


Q(None, "A Heartbeat Failure Detector", "Easy", "Suspect silent nodes",
  "Given each node's last heartbeat time, the current time and a timeout, return the nodes to suspect (sorted). Note a slow node and a dead node look the same.",
  [(({"n1": 98, "n2": 91, "n3": 100, "n4": 70}, 100, 5), ['n2', 'n4'])],
  ("Loop and compare.", "O(n log n)", "O(n)"),
  ("Sorted comprehension.", "O(n log n)", "O(n)"),
  viz=(({"a": 1, "b": 9}, 10, 5)))


@B
def suspects(last_beat, now, timeout):
    out = []
    for node, t in last_beat.items():
        if now - t > timeout:
            out.append(node)
    out.sort()
    return out


@O
def suspects(last_beat, now, timeout):
    return sorted(n for n, t in last_beat.items() if now - t > timeout)


Q(None, "How Fast Does Gossip Spread?", "Easy", "Epidemic protocols",
  "One node knows an update. Each round every informed node tells <code>fanout</code> new nodes. Return the rounds needed to reach all <code>n</code> nodes for each n — it grows like log n.",
  [(([10, 100, 1000, 1_000_000], 2), [3, 5, 7, 13])],
  ("Simulate round by round.", "O(log n)", "O(1)"),
  ("Multiply by (1 + fanout) each round.", "O(log n)", "O(1)"),
  viz=(([10], 2)))


@B
def gossip_rounds(ns, fanout):
    out = []
    for n in ns:
        informed, rounds = 1, 0
        while informed < n:
            informed = informed + informed * fanout
            rounds += 1
        out.append(rounds)
    return out


@O
def gossip_rounds(ns, fanout):
    def rounds(n):
        r, reach = 0, 1
        while reach < n:
            r, reach = r + 1, reach * (1 + fanout)
        return r
    return [rounds(n) for n in ns]


Q(None, "Find Divergent Buckets (Merkle Anti-Entropy)", "Medium", "Compare hashes, not data",
  "Two replicas split keys into <code>b</code> buckets by <code>crc32(key) % b</code>. Instead of sending all data, they compare one hash per bucket and only sync buckets whose hashes differ. Return the differing buckets.",
  [(({"k1": 1, "k2": 2, "k3": 3, "k4": 4, "k5": 5}, {"k1": 1, "k2": 20, "k3": 3, "k4": 4, "k6": 6}, 4), [0, 2, 3])],
  ("Compare the sorted items of each bucket directly.", "O(n)", "O(n)"),
  ("Hash each bucket with SHA-256 and compare digests.", "O(n)", "O(b)"),
  viz=(({"a": 1}, {"a": 2}, 2)))


@B
def merkle_diff(a, b, buckets):
    def items(d, i):
        return sorted((k, v) for k, v in d.items() if zlib.crc32(k.encode()) % buckets == i)
    return [i for i in range(buckets) if items(a, i) != items(b, i)]


@O
def merkle_diff(a, b, buckets):
    def digests(d):
        groups = defaultdict(list)
        for k, v in sorted(d.items()):
            groups[zlib.crc32(k.encode()) % buckets].append(f"{k}={v}")
        return [hashlib.sha256("|".join(groups[i]).encode()).hexdigest() for i in range(buckets)]
    da, db = digests(a), digests(b)
    return [i for i in range(buckets) if da[i] != db[i]]


Q(None, "Deduplicate by Sequence Number", "Easy", "Effectively-once delivery",
  "Producers number their messages. The consumer remembers the highest sequence per producer and drops anything not higher (a retry or replay). Return <code>(accepted count, dropped messages)</code>.",
  [(([("p1", 1), ("p1", 2), ("p2", 1), ("p1", 2), ("p1", 3), ("p2", 1), ("p2", 2), ("p1", 1)],), (5, [('p1', 2), ('p2', 1), ('p1', 1)]))],
  ("Dict of last sequence numbers.", "O(n)", "O(p)"),
  ("Same, using <code>dict.get</code>.", "O(n)", "O(p)"),
  viz=(([("p", 1), ("p", 1)],)))


@B
def seq_dedupe(messages):
    last, accepted, dropped = {}, 0, []
    for p, s in messages:
        if p in last and s <= last[p]:
            dropped.append((p, s))
        else:
            last[p] = s
            accepted += 1
    return (accepted, dropped)


@O
def seq_dedupe(messages):
    last, dropped = {}, []
    for p, s in messages:
        if s > last.get(p, 0):
            last[p] = s
        else:
            dropped.append((p, s))
    return (len(messages) - len(dropped), dropped)


Q(None, "Monotonic Reads", "Medium", "Never go back in time",
  "A client reads from the replicas listed in <code>reads</code>; replicas hold different versions. To avoid seeing older data after newer, if a replica is behind the highest version the client has seen, it reads from the primary instead. Return <code>(server used, version seen)</code> for each read.",
  [(({"r1": 7, "r2": 5, "r3": 8}, 9, ["r2", "r1", "r2", "r3", "r1"]), [('r2', 5), ('r1', 7), ('primary', 9), ('primary', 9), ('primary', 9)])],
  ("Track the max version seen in a loop.", "O(n)", "O(1)"),
  ("Same with a conditional expression.", "O(n)", "O(1)"),
  viz=(({"a": 2, "b": 1}, 3, ["a", "b"])))


@B
def monotonic_reads(replicas, primary_version, reads):
    seen, out = 0, []
    for r in reads:
        if replicas[r] >= seen:
            out.append((r, replicas[r]))
            seen = replicas[r]
        else:
            out.append(("primary", primary_version))
            seen = primary_version
    return out


@O
def monotonic_reads(replicas, primary_version, reads):
    seen, out = 0, []
    for r in reads:
        server, v = (r, replicas[r]) if replicas[r] >= seen else ("primary", primary_version)
        out.append((server, v))
        seen = v
    return out


Q(None, "How Many Nodes for Consensus?", "Easy", "Crash vs Byzantine faults",
  "To survive f crashed nodes, Raft/Paxos needs 2f + 1 nodes (majority f + 1). To survive f nodes that lie (Byzantine), BFT protocols need 3f + 1. Return <code>(raft nodes, raft majority, BFT nodes)</code> for each f.",
  [(([1, 2, 3],), [(3, 2, 4), (5, 3, 7), (7, 4, 10)])],
  ("A loop.", "O(n)", "O(n)"),
  ("A comprehension.", "O(n)", "O(n)"),
  viz=(([1],)))


@B
def consensus_size(fs):
    out = []
    for f in fs:
        out.append((2 * f + 1, f + 1, 3 * f + 1))
    return out


@O
def consensus_size(fs):
    return [(2 * f + 1, (2 * f + 1) // 2 + 1, 3 * f + 1) for f in fs]
