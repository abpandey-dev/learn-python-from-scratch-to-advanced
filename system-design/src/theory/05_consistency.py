from lib import *

THEORY("Fallacies of distributed computing", """
<ul>
<li>The network is reliable — it isn't; retry with idempotency.</li>
<li>Latency is zero — every hop costs; batch and cache.</li>
<li>Bandwidth is infinite; the network is secure; topology doesn't change.</li>
<li>There is one administrator; transport cost is zero; the network is homogeneous.</li>
</ul>
""")

THEORY("2PC vs saga", """
<table>
<tr><th></th><th>Two-phase commit</th><th>Saga</th></tr>
<tr><td>Atomicity</td><td>true atomic commit</td><td>eventual, via compensations</td></tr>
<tr><td>Locks</td><td>held across services</td><td>local only</td></tr>
<tr><td>Failure</td><td>blocks if coordinator dies</td><td>keeps going, must design undo steps</td></tr>
<tr><td>Use</td><td>within one database cluster</td><td>across microservices</td></tr>
</table>
""")

FAQ("Explain CAP in one minute.", "<p>When a network partition happens, a distributed system must choose between answering every request (availability) and never returning stale data (consistency). Without partitions you can have both, but you still trade latency for consistency (PACELC).</p>")
FAQ("Why are clusters usually 3 or 5 nodes?", "<p>Consensus needs a majority. 3 nodes tolerate 1 failure, 5 tolerate 2; an even count adds a node without adding tolerance (4 still tolerates only 1).</p>")
FAQ("How do you make an API idempotent?", "<p>Have clients send an idempotency key; store the key with the result in the same transaction as the change; on a repeat, return the stored result instead of doing the work again.</p>")
FAQ("What is split brain?", "<p>Two nodes both believing they are leader after a partition, both accepting writes. Prevent it with majority quorums and fencing tokens.</p>")
FAQ("Is exactly-once delivery possible?", "<p>Not over an unreliable network. Systems achieve exactly-once <i>effects</i> with at-least-once delivery plus deduplication or idempotent writes (and transactions, as in Kafka).</p>")
FAQ("When would you use a CRDT?", "<p>For data edited concurrently in many places without coordination — counters, sets, collaborative text, offline-first apps — where every replica must converge automatically.</p>")
