from lib import *
import heapq
import math
import zlib
from collections import Counter, defaultdict

TOPIC(
    id="queues", title="Queues & Streams", glyph="📬",
    blurb="Decoupling with messages: backlogs and consumer counts, Kafka partitions, keys and consumer groups, lag and offsets, at-least-once redelivery, retries with backoff and jitter, dead-letter queues, visibility timeouts, backpressure, the outbox pattern, reordering, windows and watermarks, log compaction, delay queues and queueing maths.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">consumers needed  = msgs/s × seconds per msg   (Kafka: ≤ one consumer per partition)
ordering          = only within a partition → key messages by entity id
delivery          = at-least-once + idempotent consumer ≈ exactly-once effect
retry delay       = min(cap, base × 2^attempt) × random()   # full jitter
utilisation ρ = λ / μ;  M/M/1 time in system = 1 / (μ − λ)  → explodes as ρ → 1</code></pre>
""")


Q(None, "Watch the Backlog Grow", "Easy", "Arrivals vs consumption",
  "Messages arrive per second as listed; consumers process at most <code>rate</code> per second. Return the backlog at the end of each second.",
  [(([80, 120, 200, 150, 60, 40, 30], 100), [0, 20, 120, 170, 130, 70, 0])],
  ("Loop with a running backlog.", "O(n)", "O(n)"),
  ("<code>itertools.accumulate</code> with a max-0 step.", "O(n)", "O(n)"),
  viz=(([120, 50], 100)))


@B
def backlog(arrivals, rate):
    out, q = [], 0
    for a in arrivals:
        q = q + a - rate
        if q < 0:
            q = 0
        out.append(q)
    return out


@O
def backlog(arrivals, rate):
    from itertools import accumulate
    return list(accumulate(arrivals, lambda q, a: max(0, q + a - rate), initial=0))[1:]


Q(None, "How Many Consumers and Partitions?", "Easy", "Throughput sizing",
  "Messages arrive at <code>msgs_per_s</code>, each takes <code>ms_each</code> to process, and you keep <code>headroom</code> spare capacity. Return <code>(consumers needed, partitions needed)</code> — in Kafka each partition is read by at most one consumer in a group, so you need at least as many partitions.",
  [((12000, 5, 0.25), (80, 80)), ((300, 200, 0.5), (120, 120))],
  ("Count up until capacity suffices.", "O(c)", "O(1)"),
  ("<code>math.ceil</code>.", "O(1)", "O(1)"),
  viz=((100, 10, 0.0)))


@B
def consumers_needed(msgs_per_s, ms_each, headroom):
    per_consumer = 1000 / ms_each
    c = 0
    while c * per_consumer * (1 - headroom) < msgs_per_s - 1e-9:
        c += 1
    return (c, c)


@O
def consumers_needed(msgs_per_s, ms_each, headroom):
    c = math.ceil(round(msgs_per_s * ms_each / 1000 / (1 - headroom), 9))
    return (c, c)


Q(None, "Partition by Key", "Easy", "Order per key",
  "Send each <code>(key, event)</code> to partition <code>crc32(key) % p</code>. Return each partition's events in order. All events for one key stay in one partition, so their order is kept.",
  [(([("order-1", "created"), ("order-2", "created"), ("order-1", "paid"), ("order-3", "created"), ("order-2", "cancelled"), ("order-1", "shipped")], 3), [['order-2:created', 'order-2:cancelled'], ['order-1:created', 'order-1:paid', 'order-1:shipped'], ['order-3:created']])],
  ("A list of lists.", "O(n)", "O(n)"),
  ("Same with a comprehension per partition.", "O(n · p)", "O(n)"),
  viz=(([("a", "x"), ("a", "y")], 2)))


@B
def partition_events(events, p):
    parts = [[] for _ in range(p)]
    for key, ev in events:
        parts[zlib.crc32(key.encode()) % p].append(key + ":" + ev)
    return parts


@O
def partition_events(events, p):
    return [[f"{k}:{e}" for k, e in events if zlib.crc32(k.encode()) % p == i] for i in range(p)]


Q(None, "Assign Partitions to a Consumer Group", "Medium", "Range assignment",
  "Split partitions 0..n-1 among the sorted consumers in contiguous ranges; the first <code>n % c</code> consumers get one extra. Return the mapping. Extra consumers beyond n get nothing — they sit idle.",
  [((7, ["c2", "c1", "c3"]), {'c1': [0, 1, 2], 'c2': [3, 4], 'c3': [5, 6]}), ((2, ["a", "b", "c"]), {'a': [0], 'b': [1], 'c': []})],
  ("Hand out partitions one consumer at a time.", "O(n + c)", "O(n)"),
  ("<code>divmod</code> for sizes, then slices.", "O(n + c)", "O(n)"),
  viz=((3, ["a", "b"])))


@B
def range_assign(n, consumers):
    consumers = sorted(consumers)
    out, nxt = {}, 0
    for i, c in enumerate(consumers):
        size = n // len(consumers)
        if i < n % len(consumers):
            size += 1
        out[c] = list(range(nxt, nxt + size))
        nxt += size
    return out


@O
def range_assign(n, consumers):
    q, r = divmod(n, len(consumers))
    out, start = {}, 0
    for i, c in enumerate(sorted(consumers)):
        end = start + q + (i < r)
        out[c], start = list(range(start, end)), end
    return out


Q(None, "Consumer Lag", "Easy", "How far behind are we?",
  "Lag is the newest offset minus the committed offset per partition. Return the lag per partition, the total, and the partitions lagging more than <code>alert</code>.",
  [(([1500, 980, 2200, 760], [1490, 400, 2200, 100], 500), ([10, 580, 0, 660], 1250, [1, 3]))],
  ("A loop with three outputs.", "O(p)", "O(p)"),
  ("<code>zip</code> and comprehensions.", "O(p)", "O(p)"),
  viz=(([10, 20], [5, 20], 3)))


@B
def consumer_lag(end_offsets, committed, alert):
    lags, hot = [], []
    for i in range(len(end_offsets)):
        lag = end_offsets[i] - committed[i]
        lags.append(lag)
        if lag > alert:
            hot.append(i)
    return (lags, sum(lags), hot)


@O
def consumer_lag(end_offsets, committed, alert):
    lags = [e - c for e, c in zip(end_offsets, committed)]
    return (lags, sum(lags), [i for i, l in enumerate(lags) if l > alert])


Q(None, "Duplicates After a Crash", "Medium", "At-least-once delivery",
  "A consumer processes messages 0..n-1 and commits its offset after every <code>commit_every</code> messages. It crashes right after processing message <code>crash_at</code>, restarts from the last commit and finishes. Return <code>(messages processed twice, total processing runs)</code>.",
  [((100, 10, 57), (8, 108)), ((100, 1, 57), (0, 100)), ((100, 50, 49), (0, 100))],
  ("Simulate processing and commits.", "O(n)", "O(1)"),
  ("Arithmetic on the last commit point.", "O(1)", "O(1)"),
  viz=((10, 5, 7)))


@B
def crash_duplicates(n, commit_every, crash_at):
    committed, processed = 0, 0
    for i in range(crash_at + 1):
        processed += 1
        if (i + 1) % commit_every == 0:
            committed = i + 1
    for i in range(committed, n):
        processed += 1
    return (processed - n, processed)


@O
def crash_duplicates(n, commit_every, crash_at):
    committed = (crash_at + 1) // commit_every * commit_every
    dup = crash_at + 1 - committed
    return (dup, n + dup)


Q(None, "Exponential Backoff", "Easy", "Don't hammer a struggling service",
  "Return the wait (ms) before each retry: <code>min(cap, base × factor^attempt)</code> for attempts 0..n-1.",
  [((100, 2, 5000, 8), [100, 200, 400, 800, 1600, 3200, 5000, 5000])],
  ("A loop multiplying the delay.", "O(n)", "O(n)"),
  ("A comprehension.", "O(n)", "O(n)"),
  viz=((100, 2, 1000, 4)))


@B
def backoff(base, factor, cap, n):
    out, d = [], base
    for _ in range(n):
        out.append(min(cap, d))
        d *= factor
    return out


@O
def backoff(base, factor, cap, n):
    return [min(cap, base * factor ** i) for i in range(n)]


Q(None, "Add Full Jitter", "Easy", "Spread the retries",
  "Without jitter, every client that failed together retries together. Full jitter waits <code>random × min(cap, base × 2^attempt)</code>. Using the given random numbers (one per client, attempt 3), return each client's wait in ms (rounded) and how many distinct wait times there are without and with jitter.",
  [((100, 5000, 3, [0.12, 0.87, 0.45, 0.99, 0.03, 0.61]), ([96, 696, 360, 792, 24, 488], 1, 6))],
  ("A loop.", "O(n)", "O(n)"),
  ("A comprehension and sets.", "O(n)", "O(n)"),
  viz=((100, 5000, 1, [0.5, 0.25])))


@B
def full_jitter(base, cap, attempt, randoms):
    ceiling = min(cap, base * 2 ** attempt)
    waits = []
    for r in randoms:
        waits.append(round(r * ceiling))
    return (waits, 1, len(set(waits)))


@O
def full_jitter(base, cap, attempt, randoms):
    ceiling = min(cap, base * 2 ** attempt)
    waits = [round(r * ceiling) for r in randoms]
    return (waits, 1, len(set(waits)))


Q(None, "Send Poison Messages to a Dead-Letter Queue", "Medium", "Don't retry forever",
  "Each message fails a given number of times before it would succeed (a large number means it never will). Try each at most <code>max_attempts</code> times. Return <code>(succeeded, dead-lettered, total attempts)</code>.",
  [(({"m1": 0, "m2": 2, "m3": 99, "m4": 1, "m5": 5}, 3), (['m1', 'm2', 'm4'], ['m3', 'm5'], 12))],
  ("Simulate attempts per message.", "O(n · a)", "O(n)"),
  ("Compare failures with max attempts directly.", "O(n)", "O(n)"),
  viz=(({"a": 0, "b": 9}, 2)))


@B
def dead_letter(failures, max_attempts):
    ok, dlq, attempts = [], [], 0
    for m, f in failures.items():
        tries = 0
        done = False
        while tries < max_attempts and not done:
            tries += 1
            if tries > f:
                done = True
        attempts += tries
        if done:
            ok.append(m)
        else:
            dlq.append(m)
    return (ok, dlq, attempts)


@O
def dead_letter(failures, max_attempts):
    ok = [m for m, f in failures.items() if f < max_attempts]
    dlq = [m for m, f in failures.items() if f >= max_attempts]
    return (ok, dlq, sum(min(f + 1, max_attempts) for f in failures.values()))


Q(None, "Visibility Timeouts", "Easy", "SQS-style redelivery",
  "A received message is hidden for <code>timeout</code> seconds; if not deleted in time it becomes visible and another consumer gets it too. For each processing time, return how many times the message gets delivered.",
  [(([5, 30, 31, 75, 120], 30), [1, 1, 2, 3, 4])],
  ("Count deliveries by stepping through time.", "O(n · d)", "O(n)"),
  ("Ceiling division.", "O(n)", "O(n)"),
  viz=(([10, 50], 30)))


@B
def deliveries(durations, timeout):
    out = []
    for d in durations:
        count, visible_again = 1, timeout
        while visible_again < d:
            count += 1
            visible_again += timeout
        out.append(count)
    return out


@O
def deliveries(durations, timeout):
    return [max(1, math.ceil(d / timeout)) for d in durations]


Q(None, "Backpressure With a Bounded Queue", "Medium", "Reject early, stay healthy",
  "Each tick, the listed number of requests arrive at a queue of <code>capacity</code> (extras are rejected with 429/503), then <code>service</code> are processed. Return <code>(rejected total, deepest queue)</code>.",
  [(([5, 12, 20, 3, 0, 15], 10, 6), (21, 10))],
  ("Loop with a counter.", "O(n)", "O(1)"),
  ("Same with <code>min</code>/<code>max</code>.", "O(n)", "O(1)"),
  viz=(([12], 10, 5)))


@B
def bounded_queue(arrivals, capacity, service):
    q, rejected, deepest = 0, 0, 0
    for a in arrivals:
        space = capacity - q
        if a > space:
            rejected += a - space
            q = capacity
        else:
            q += a
        if q > deepest:
            deepest = q
        q -= service
        if q < 0:
            q = 0
    return (rejected, deepest)


@O
def bounded_queue(arrivals, capacity, service):
    q = rejected = deepest = 0
    for a in arrivals:
        take = min(a, capacity - q)
        rejected, q = rejected + a - take, q + take
        deepest, q = max(deepest, q), max(0, q - service)
    return (rejected, deepest)


Q(None, "Dual Writes vs the Outbox", "Medium", "Never lose an event",
  "Each order is <code>(id, db_ok, publish_ok)</code>. Writing the DB then publishing loses the event when the DB write succeeds but publishing fails; publishing first creates 'phantom' events when the DB write then fails. With the outbox pattern the event is saved in the same DB transaction and a relay retries publishing, so neither happens. Return <code>(lost, phantom, outbox problems)</code>.",
  [(([("o1", True, True), ("o2", True, False), ("o3", False, True), ("o4", True, False), ("o5", False, False)],), (['o2', 'o4'], ['o3'], 0))],
  ("Loop with if-statements.", "O(n)", "O(n)"),
  ("Comprehensions.", "O(n)", "O(n)"),
  viz=(([("a", True, False)],)))


@B
def outbox(orders):
    lost, phantom = [], []
    for oid, db_ok, pub_ok in orders:
        if db_ok and not pub_ok:
            lost.append(oid)
        if pub_ok and not db_ok:
            phantom.append(oid)
    return (lost, phantom, 0)


@O
def outbox(orders):
    return ([o for o, d, p in orders if d and not p], [o for o, d, p in orders if p and not d], 0)


Q(None, "Restore Order With a Reorder Buffer", "Medium", "Release in sequence",
  "Messages with sequence numbers 1, 2, 3, ... arrive out of order. Hold them until the next expected one arrives, then release every consecutive message. Return what is released after each arrival.",
  [(([3, 1, 2, 6, 4, 5, 7],), [[], [1], [2, 3], [], [4], [5, 6], [7]])],
  ("Keep a list; scan it for the next expected number.", "O(n²)", "O(n)"),
  ("A set of held numbers and a pointer.", "O(n)", "O(n)"),
  viz=(([2, 1],)))


@B
def reorder(arrivals):
    held, nxt, out = [], 1, []
    for s in arrivals:
        held.append(s)
        released = []
        while nxt in held:
            held.remove(nxt)
            released.append(nxt)
            nxt += 1
        out.append(released)
    return out


@O
def reorder(arrivals):
    held, nxt, out = set(), 1, []
    for s in arrivals:
        held.add(s)
        start = nxt
        while nxt in held:
            held.discard(nxt)
            nxt += 1
        out.append(list(range(start, nxt)))
    return out


Q(None, "Tumbling Window Counts", "Easy", "Stream aggregation",
  "Group events <code>(timestamp_s, amount)</code> into fixed windows of <code>size</code> seconds. Return <code>(window start, total)</code> sorted by window.",
  [(([(3, 10), (61, 5), (59, 7), (125, 1), (64, 2), (0, 4)], 60), [(0, 21), (60, 7), (120, 1)])],
  ("A dict of totals.", "O(n log n)", "O(w)"),
  ("<code>defaultdict</code> and sorted items.", "O(n log n)", "O(w)"),
  viz=(([(1, 2), (70, 3)], 60)))


@B
def tumbling(events, size):
    totals = {}
    for ts, amount in events:
        start = ts - ts % size
        totals[start] = totals.get(start, 0) + amount
    return sorted(totals.items())


@O
def tumbling(events, size):
    totals = defaultdict(int)
    for ts, amount in events:
        totals[ts // size * size] += amount
    return sorted(totals.items())


Q(None, "Drop Late Events With a Watermark", "Medium", "Event time vs arrival order",
  "Events arrive in the listed order carrying their event time. The watermark is the highest event time seen so far minus <code>lateness</code>; an event older than the current watermark is too late and is dropped. Return the dropped event times.",
  [(([10, 12, 11, 20, 14, 16, 25, 21, 9], 5), [14, 9])],
  ("Track the max seen in a loop.", "O(n)", "O(n)"),
  ("Same, as a single pass.", "O(n)", "O(n)"),
  viz=(([10, 3], 5)))


@B
def late_events(times, lateness):
    highest, dropped = None, []
    for t in times:
        if highest is not None and t < highest - lateness:
            dropped.append(t)
        else:
            if highest is None or t > highest:
                highest = t
    return dropped


@O
def late_events(times, lateness):
    highest, dropped = -math.inf, []
    for t in times:
        if t < highest - lateness:
            dropped.append(t)
        else:
            highest = max(highest, t)
    return dropped


Q(None, "Pub/Sub Fan-Out", "Easy", "One message, many subscribers",
  "Subscribers listen to topics. For the published messages (topic names), return how many messages each subscriber receives and the total deliveries.",
  [(({"email": ["orders", "refunds"], "analytics": ["orders", "clicks", "refunds"], "fraud": ["orders"]}, ["orders", "clicks", "orders", "refunds", "clicks"]), ({'email': 3, 'analytics': 5, 'fraud': 2}, 10))],
  ("For each message, loop over subscribers.", "O(m · s)", "O(s)"),
  ("Count messages per topic first.", "O(m + s · t)", "O(t)"),
  viz=(({"a": ["x"]}, ["x", "y"])))


@B
def fan_out(subs, messages):
    counts = {s: 0 for s in subs}
    for m in messages:
        for s, topics in subs.items():
            if m in topics:
                counts[s] += 1
    return (counts, sum(counts.values()))


@O
def fan_out(subs, messages):
    per_topic = Counter(messages)
    counts = {s: sum(per_topic[t] for t in topics) for s, topics in subs.items()}
    return (counts, sum(counts.values()))


Q(None, "A Delay Queue", "Medium", "Run jobs at a scheduled time",
  "Jobs <code>(run_at, name)</code> are added in any order. A worker wakes at each time in <code>ticks</code> and runs every due job (earliest first, ties by name). Return <code>(tick, [jobs run])</code> for ticks that ran something.",
  [(([(30, "reminder"), (5, "retry-7"), (12, "cleanup"), (5, "retry-3"), (31, "report")], [0, 10, 20, 30, 40]), [(10, ['retry-3', 'retry-7']), (20, ['cleanup']), (30, ['reminder']), (40, ['report'])])],
  ("Sort the remaining jobs at every tick.", "O(t · n log n)", "O(n)"),
  ("A min-heap.", "O(n log n + t)", "O(n)"),
  viz=(([(2, "a"), (1, "b")], [1, 2])))


@B
def delay_queue(jobs, ticks):
    pending, out = list(jobs), []
    for t in ticks:
        pending.sort()
        due = [j for j in pending if j[0] <= t]
        pending = [j for j in pending if j[0] > t]
        if due:
            out.append((t, [name for _, name in due]))
    return out


@O
def delay_queue(jobs, ticks):
    heap, out = list(jobs), []
    heapq.heapify(heap)
    for t in ticks:
        ran = []
        while heap and heap[0][0] <= t:
            ran.append(heapq.heappop(heap)[1])
        if ran:
            out.append((t, ran))
    return out


Q(None, "Log Compaction", "Medium", "Keep the latest value per key",
  "A compacted topic keeps only the newest record per key (a None value is a delete and is removed too). Records are <code>(key, value)</code> at offsets 0, 1, 2…; return the surviving <code>(offset, key, value)</code> in offset order.",
  [(([("u1", "Pune"), ("u2", "Goa"), ("u1", "Delhi"), ("u3", "Agra"), ("u2", None), ("u1", "Mumbai")],), [(3, 'u3', 'Agra'), (5, 'u1', 'Mumbai')])],
  ("For each record, check whether a later one has the same key.", "O(n²)", "O(n)"),
  ("Remember the last offset per key in one pass.", "O(n)", "O(k)"),
  viz=(([("a", 1), ("a", 2)],)))


@B
def compact_log(records):
    out = []
    for i, (k, v) in enumerate(records):
        later = False
        for j in range(i + 1, len(records)):
            if records[j][0] == k:
                later = True
        if not later and v is not None:
            out.append((i, k, v))
    return out


@O
def compact_log(records):
    last = {k: i for i, (k, _) in enumerate(records)}
    return [(i, k, v) for k, i in sorted(last.items(), key=lambda x: x[1]) for v in [records[i][1]] if v is not None]


Q(None, "Why Queues Explode Near 100%", "Medium", "Queueing theory",
  "For a single worker serving <code>mu</code> jobs/s (M/M/1 queue), return the utilisation % and average time in system (ms, rounded to 1) for each arrival rate — or 'unstable' when arrivals ≥ service rate.",
  [((100, [50, 80, 90, 95, 99, 100, 120]), [(50.0, 20.0), (80.0, 50.0), (90.0, 100.0), (95.0, 200.0), (99.0, 1000.0), 'unstable', 'unstable'])],
  ("A loop with if/else.", "O(n)", "O(n)"),
  ("A comprehension.", "O(n)", "O(n)"),
  viz=((10, [5, 9])))


@B
def mm1(mu, lambdas):
    out = []
    for lam in lambdas:
        if lam >= mu:
            out.append("unstable")
        else:
            out.append((round(lam / mu * 100, 1), round(1000 / (mu - lam), 1)))
    return out


@O
def mm1(mu, lambdas):
    return ["unstable" if l >= mu else (round(l / mu * 100, 1), round(1000 / (mu - l), 1)) for l in lambdas]


Q(None, "Producer Batching (batch size and linger)", "Medium", "Throughput vs latency",
  "A producer sends a batch when it reaches <code>max_batch</code> messages, or <code>linger</code> ms after the batch's first message — whichever comes first. Given message arrival times (ms, sorted), return <code>(send time, batch size)</code> for each batch.",
  [(([0, 1, 2, 3, 4, 20, 22, 50, 51, 52, 53, 54, 55], 5, 10), [(4, 5), (30, 2), (54, 5), (65, 1)])],
  ("Simulate with a list for the open batch.", "O(n)", "O(b)"),
  ("Same with a start time and a counter.", "O(n)", "O(1)"),
  viz=(([0, 1, 30], 2, 10)))


@B
def batching(times, max_batch, linger):
    out, batch = [], []
    for t in times:
        if batch and t >= batch[0] + linger:
            out.append((batch[0] + linger, len(batch)))
            batch = []
        batch.append(t)
        if len(batch) == max_batch:
            out.append((t, len(batch)))
            batch = []
    if batch:
        out.append((batch[0] + linger, len(batch)))
    return out


@O
def batching(times, max_batch, linger):
    out, start, size = [], None, 0
    for t in times:
        if size and t >= start + linger:
            out.append((start + linger, size))
            size = 0
        if size == 0:
            start = t
        size += 1
        if size == max_batch:
            out.append((t, size))
            size = 0
    if size:
        out.append((start + linger, size))
    return out
