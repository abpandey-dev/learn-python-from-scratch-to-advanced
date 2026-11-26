from lib import *

THEORY("Queue vs log", """
<table>
<tr><th></th><th>Queue (SQS, RabbitMQ)</th><th>Log (Kafka)</th></tr>
<tr><td>After consuming</td><td>message deleted</td><td>kept for retention period</td></tr>
<tr><td>Replay</td><td>no</td><td>yes, reset the offset</td></tr>
<tr><td>Ordering</td><td>best effort (FIFO queues exist)</td><td>per partition</td></tr>
<tr><td>Many readers</td><td>competing consumers</td><td>independent consumer groups</td></tr>
</table>
""")

FAQ("How do you guarantee ordering?", "<p>Only within a partition: key messages by the entity whose order matters (order id, user id). Global ordering needs a single partition, which limits throughput.</p>")
FAQ("What happens if a consumer is too slow?", "<p>Lag grows. Add consumers (up to the partition count), add partitions, batch work, or make processing faster; alert on lag.</p>")
FAQ("How do you handle a message that always fails?", "<p>Retry a limited number of times with backoff, then move it to a dead-letter queue, alert, and fix or replay it later — so it doesn't block the rest.</p>")
FAQ("Why use the outbox pattern?", "<p>To change the database and publish an event atomically without distributed transactions: both go into one local transaction, and a relay publishes reliably afterwards.</p>")
FAQ("Queue or direct API call?", "<p>Call directly when the caller needs the answer now. Use a queue when work can happen later, needs retries, or must absorb spikes.</p>")
FAQ("Why does latency explode as utilisation approaches 100%?", "<p>Random arrivals cluster; with no spare capacity the queue can't catch up, so waits grow like 1 / (1 − utilisation). Keep busy resources well below 100%.</p>")
