from lib import *

THEORY("Non-functional requirements to ask about", """
<table>
<tr><th>Property</th><th>Question to ask</th></tr>
<tr><td>Scale</td><td>How many users, requests per second, items stored?</td></tr>
<tr><td>Latency</td><td>How fast must reads and writes be (p50, p99)?</td></tr>
<tr><td>Availability</td><td>How many nines? What happens during an outage?</td></tr>
<tr><td>Consistency</td><td>Must every reader see the latest write immediately?</td></tr>
<tr><td>Durability</td><td>Can we ever lose data?</td></tr>
<tr><td>Cost, security, compliance</td><td>Budgets, data residency, privacy rules</td></tr>
</table>
""")

THEORY("Powers of ten", """
<table>
<tr><th>Power</th><th>Name</th><th>Bytes</th></tr>
<tr><td>10³</td><td>thousand</td><td>KB</td></tr>
<tr><td>10⁶</td><td>million</td><td>MB</td></tr>
<tr><td>10⁹</td><td>billion</td><td>GB</td></tr>
<tr><td>10¹²</td><td>trillion</td><td>TB</td></tr>
<tr><td>10¹⁵</td><td>quadrillion</td><td>PB</td></tr>
</table>
""")

FAQ("Why estimate at all?", "<p>The numbers decide the design: 100 QPS fits on one server with one database; 1 million QPS needs caching, sharding and many replicas. Estimating shows the interviewer you design for the real scale.</p>")
FAQ("How do you handle a peak you can't predict?", "<p>Design for the expected peak with headroom, autoscale stateless tiers, queue or shed load gracefully, and rate-limit per client so one burst can't take everything down.</p>")
FAQ("Why does availability drop as you add dependencies?", "<p>A request succeeds only if every service it needs succeeds, so availabilities multiply. Redundancy, timeouts, fallbacks and removing hard dependencies push it back up.</p>")
FAQ("What is tail latency and why does it matter?", "<p>The slowest requests (p99, p999). With fan-out to many services, a rare slow call becomes likely for each user request, so the tail of each service sets the typical latency of the whole system.</p>")
FAQ("How precise should estimates be?", "<p>Within an order of magnitude. Round to easy numbers, state assumptions, and focus on what the numbers imply for the design.</p>")
FAQ("What's the first thing you do in a design interview?", "<p>Clarify requirements — functional and non-functional — and agree the scope with the interviewer before drawing anything.</p>")
