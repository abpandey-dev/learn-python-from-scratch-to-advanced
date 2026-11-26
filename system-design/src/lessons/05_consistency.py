from lib import *

LESSON("Basics", "CAP, PACELC and consistency models", """
<p>Networks fail. When a <b>partition</b> splits your nodes, each side must either refuse requests (stay <b>consistent</b>, CP) or keep answering with possibly stale data (stay <b>available</b>, AP). <b>PACELC</b> adds: even without partitions you trade <b>latency</b> against consistency, because waiting for replicas takes time.</p>
<table>
<tr><th>Model</th><th>Promise</th></tr>
<tr><td>Linearizable (strong)</td><td>behaves like one copy; every read sees the latest write</td></tr>
<tr><td>Read-your-writes</td><td>you always see your own updates</td></tr>
<tr><td>Monotonic reads</td><td>you never see time go backwards</td></tr>
<tr><td>Eventual</td><td>replicas converge if writes stop</td></tr>
</table>
""", practice=["CP or AP?", "Monotonic Reads"])

LESSON("Core", "Time and ordering", """
<p>Machine clocks drift and jump (NTP corrections), so wall-clock timestamps can order events wrongly. <b>Lamport clocks</b> give an order consistent with cause and effect; <b>vector clocks</b> also detect when two updates were <b>concurrent</b> (a true conflict). Conflicts are resolved by last-writer-wins (simple, loses data), by the application (merge carts), or with <b>CRDTs</b> — data types whose merges always converge.</p>
""", practice=["Lamport Clocks", "Run Vector Clocks", "Compare Vector Clocks", "Clock Skew Reorders Events", "Last Writer Wins", "Merge a Grow-Only Counter (CRDT)"])

LESSON("Core", "Idempotency and distributed transactions", """
<p>Over a network you can't tell "request lost" from "response lost", so clients retry — and every handler that changes state must be <b>idempotent</b>: store a request id and return the saved result on repeats. True exactly-once delivery doesn't exist; at-least-once delivery plus idempotent processing gives <b>effectively once</b>.</p>
<p>For a change spanning services: <b>two-phase commit</b> (prepare, then commit) is atomic but blocks if the coordinator dies. A <b>saga</b> runs local transactions and on failure runs compensating actions (refund, release stock) — the usual choice for microservices.</p>
""", practice=["Make the Payment Idempotent", "Deduplicate by Sequence Number", "Two-Phase Commit", "Run a Saga"])

LESSON("Advanced", "Consensus, leaders and failure detection", """
<p>Many systems need one leader (one writer, one scheduler). <b>Raft</b> and Paxos elect it with a <b>majority</b> vote: a 5-node cluster survives 2 failures, and a minority side of a partition can't elect a second leader — no split brain. Raft voters only accept candidates whose log is at least as complete as theirs.</p>
<ul>
<li><b>Heartbeats</b> detect failure, but slow and dead look the same — so timeouts are a trade-off.</li>
<li>A <b>lease</b> lets a leader act for a fixed time; <b>fencing tokens</b> stop an old leader that wakes up late.</li>
<li><b>Gossip</b> spreads membership and state in O(log n) rounds; <b>Merkle trees</b> find which data differs between replicas cheaply.</li>
</ul>
<p>In practice use etcd, ZooKeeper or Consul rather than writing consensus yourself.</p>
""", practice=["Which Side Keeps Working After a Split?", "Who Wins the Raft Vote?", "How Many Nodes for Consensus?", "When Did the Leader Lease Lapse?", "Fencing Tokens", "A Heartbeat Failure Detector", "How Fast Does Gossip Spread?", "Find Divergent Buckets (Merkle Anti-Entropy)"])


@LD
def lamport_demo():
    clock = {"A": 0, "B": 0}
    clock["A"] += 1; sent = clock["A"]; print("A sends at", sent)
    clock["B"] += 1; print("B local event at", clock["B"])
    clock["B"] = max(clock["B"], sent) + 1; print("B receives at", clock["B"], "— always after the send")
