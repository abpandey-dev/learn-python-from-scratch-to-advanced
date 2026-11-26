from lib import *

LESSON("Basics", "Why put a queue in the middle?", """
<p>A queue <b>decouples</b> producers from consumers: the checkout service drops an "order placed" message and returns; email, inventory and analytics consume it at their own pace. Queues absorb spikes (the backlog grows, then drains), let you retry failed work, and let you scale consumers separately.</p>
<table>
<tr><th>Style</th><th>Examples</th><th>Model</th></tr>
<tr><td>Message queue</td><td>SQS, RabbitMQ</td><td>each message to one consumer, deleted after ack</td></tr>
<tr><td>Log / stream</td><td>Kafka, Kinesis, Pub/Sub</td><td>append-only, partitioned, replayable; many consumer groups</td></tr>
<tr><td>Pub/sub</td><td>SNS, Redis pub/sub</td><td>each message to every subscriber</td></tr>
</table>
""", practice=["Watch the Backlog Grow", "How Many Consumers and Partitions?", "Pub/Sub Fan-Out", "Why Queues Explode Near 100%"])

LESSON("Core", "Kafka in one lesson", """
<p>A topic is split into <b>partitions</b>, each an ordered log. Producers pick a partition by key, so all events for <code>order-42</code> stay in order. Consumers in a <b>group</b> share partitions (one consumer per partition), and each records an <b>offset</b> — how far it has read. Lag = newest offset − committed offset is the key health metric. Producers <b>batch</b> messages for throughput (batch size + linger time). Compacted topics keep the latest value per key, acting like a table.</p>
""", practice=["Partition by Key", "Assign Partitions to a Consumer Group", "Consumer Lag", "Producer Batching (batch size and linger)", "Log Compaction"])

LESSON("Core", "Delivery guarantees and failure handling", """
<ul>
<li><b>At-most-once</b>: commit before processing — may lose messages.</li>
<li><b>At-least-once</b>: process, then commit — may process twice after a crash. The usual choice, with idempotent consumers.</li>
<li><b>Retries</b> use exponential backoff with jitter; after N failures move the message to a <b>dead-letter queue</b> for inspection.</li>
<li>SQS hides a received message for a <b>visibility timeout</b>; if processing takes longer, it's delivered again.</li>
<li><b>Backpressure</b>: bound your queues and reject or slow producers rather than running out of memory.</li>
</ul>
""", practice=["Duplicates After a Crash", "Exponential Backoff", "Add Full Jitter", "Send Poison Messages to a Dead-Letter Queue", "Visibility Timeouts", "Backpressure With a Bounded Queue", "A Delay Queue"])

LESSON("Advanced", "The outbox pattern and stream processing", """
<p>Writing to the database and publishing an event are two systems — one can succeed while the other fails. The <b>transactional outbox</b> writes the event to an outbox table in the same transaction as the change; a relay (or CDC such as Debezium) publishes it, retrying until it succeeds.</p>
<p>Stream processors (Flink, Kafka Streams, Spark) aggregate over <b>windows</b> by event time. Events arrive late and out of order, so a <b>watermark</b> says "we've probably seen everything up to time T"; later events are dropped or sent to a side output.</p>
""", practice=["Dual Writes vs the Outbox", "Restore Order With a Reorder Buffer", "Tumbling Window Counts", "Drop Late Events With a Watermark"])


@LD
def backlog_demo():
    q = 0
    for second, arrivals in enumerate([80, 150, 220, 90, 40]):
        q = max(0, q + arrivals - 100)
        print(f"t={second}s arrivals={arrivals:3}  backlog={q}")
