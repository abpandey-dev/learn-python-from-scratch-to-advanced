from lib import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LESSON("Basics", "How a system design interview works", """
<p>A system design round is a 35–60 minute conversation about building a large system ("design a URL shortener", "design WhatsApp"). There's no single right answer. Interviewers judge <b>how you think</b>: do you clarify, size the problem, choose sensible components, and explain trade-offs?</p>
<p>A framework that works for every question:</p>
<ol>
<li><b>Requirements (5 min)</b>: what must it do (functional) and how well (non-functional: latency, availability, consistency, scale). Ask; don't assume.</li>
<li><b>Estimation (5 min)</b>: users, QPS and peak, storage, bandwidth. The numbers decide the design.</li>
<li><b>High-level design (10–15 min)</b>: API, data model, the main boxes and arrows.</li>
<li><b>Deep dives (15–20 min)</b>: the hard parts — scaling the hot path, failures, consistency, bottlenecks.</li>
<li><b>Wrap up</b>: trade-offs you made, what you'd monitor, what breaks first at 10× scale.</li>
</ol>
""", practice=["Functional or Non-Functional?"])

LESSON("Basics", "Estimation: the numbers to know", """
<table>
<tr><th>Fact</th><th>Value to remember</th></tr>
<tr><td>Seconds in a day</td><td>86,400 ≈ 10⁵</td></tr>
<tr><td>1 million requests a day</td><td>≈ 12 per second</td></tr>
<tr><td>Peak vs average</td><td>2–5× (measure if you can)</td></tr>
<tr><td>Memory read</td><td>~100 ns</td></tr>
<tr><td>SSD random read</td><td>~100 µs</td></tr>
<tr><td>Round trip in one data centre</td><td>~0.5 ms</td></tr>
<tr><td>Round trip across continents</td><td>~150 ms</td></tr>
<tr><td>A typical app server</td><td>a few thousand simple requests/s</td></tr>
</table>
<p>Work in powers of ten, say every assumption, and keep a running table on the whiteboard: DAU → QPS → peak → storage per day → storage over N years × replicas → bandwidth.</p>
""", practice=["Requests per Second", "How Much Storage?", "Bandwidth In and Out", "Find the Real Peak From Traffic", "Estimate a Whole System"])


@LD
def traffic_shape():
    hourly = [20, 12, 8, 6, 6, 10, 30, 60, 90, 110, 120, 125, 130, 120, 115, 110, 120, 140, 180, 220, 240, 200, 120, 60]
    avg = sum(hourly) / 24
    fig, ax = plt.subplots(figsize=(5, 2.6))
    ax.bar(range(24), hourly, color="#99c9c2")
    ax.axhline(avg, color="#b45309", label=f"average {avg:.0f}k/h")
    ax.set_xlabel("hour of day"); ax.set_ylabel("thousand requests"); ax.legend()
    ax.set_title("Design for the peak, not the average")


LESSON("Core", "From numbers to machines", """
<ul>
<li><b>Servers</b> = peak QPS ÷ (capacity per server × target utilisation), plus spares for failures and deploys.</li>
<li><b>Shards</b>: enough for both the data size <i>and</i> the throughput — whichever needs more.</li>
<li><b>Cache</b>: the 80/20 rule — about 20% of objects get 80% of reads, so cache the hot set, not everything.</li>
<li><b>Connections</b>: Little's law — concurrent = arrival rate × time each stays open. Websockets that stay open for minutes need very different servers from 50 ms HTTP requests.</li>
<li><b>Read/write ratio</b> shapes everything: read-heavy → caches and read replicas; write-heavy → partitioning, queues and log-structured storage.</li>
</ul>
""", practice=["How Many Servers?", "How Many Shards?", "How Big a Cache?", "Open Connections (Little's Law)", "Read-Heavy or Write-Heavy?", "How Big Is One Record?"])

LESSON("Core", "Latency and availability", """
<p><b>Latency adds up along a request's path</b>: count the network hops and disk reads. A cross-region call costs more than a hundred in-data-centre calls.</p>
<p><b>Availability multiplies</b>: a request that needs three services at 99.9% each is only 99.7% available. Redundancy fixes it: two independent copies at 99.5% give 99.9975%. Know your nines: 99.9% allows ~8.8 hours of downtime a year; 99.99% only ~53 minutes.</p>
<p><b>Tail latency</b>: when one request fans out to many services and waits for all, rare slow calls become common — with 100 calls, 63% of requests hit at least one p99-slow call. That's why large systems use timeouts, hedged requests and partial results.</p>
""", practice=["Add Up a Request's Latency", "What Do the Nines Mean?", "Availability in Series and in Parallel", "Fan-Out Makes the Tail Worse"])

LESSON("Advanced", "IDs, units, cost and growth", """
<ul>
<li><b>IDs</b>: n items need ⌈log₂ n⌉ bits, or ⌈log₆₂ n⌉ base-62 characters (7 characters cover 3.5 trillion).</li>
<li><b>Cost</b> is a requirement too: tiering cold data to archive storage often cuts the bill by 70–80%.</li>
<li><b>Growth</b>: estimate when each resource runs out at the current growth rate, and say what you'd change before then.</li>
</ul>
""", practice=["How Long Must an ID Be?", "What Will Storage Cost?", "When Will We Run Out?", "Human-Readable Sizes"])
