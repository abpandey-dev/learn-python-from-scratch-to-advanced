from lib import *
import math

TOPIC(
    id="estimation", title="Requirements & Back-of-the-Envelope Estimation", glyph="≈",
    blurb="Every design starts with numbers: requests per second and peaks, storage with replication, bandwidth, read/write ratios, latency numbers, availability nines, servers, shards and cache size, Little's law, tail latency under fan-out, IDs and cost.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">avg QPS  = daily requests / 86,400          (≈ 10⁵ seconds in a day)
peak QPS = avg × 2–5
storage  = items/day × bytes × days × replicas
servers  = ⌈peak QPS / (QPS per server × target utilisation)⌉
in flight = arrival rate × latency          (Little's law)
availability in series = a₁ × a₂ × …;  redundant copies = 1 − (1 − a)ⁿ
99.9% ≈ 8.8 h down / year · 99.99% ≈ 53 min · 99.999% ≈ 5 min</code></pre>
<p>Round aggressively and say your assumptions out loud — interviewers grade the reasoning, not the third digit.</p>
""")


Q(None, "Requests per Second", "Easy", "Average and peak",
  "<code>dau</code> users each make <code>per_user</code> requests a day. Return <code>(average QPS, peak QPS)</code> with peak = average × <code>peak_factor</code>, both rounded to whole numbers.",
  [((10_000_000, 20, 3), (2315, 6944)), ((500_000, 4, 5), (23, 116))],
  ("Multiply, then divide by the seconds in a day.", "O(1)", "O(1)"),
  ("Same, as one expression with 86,400 written once.", "O(1)", "O(1)"),
  viz=((10_000_000, 20, 3)))


@B
def qps(dau, per_user, peak_factor):
    per_day = dau * per_user
    avg = per_day / (24 * 60 * 60)
    return (round(avg), round(avg * peak_factor))


@O
def qps(dau, per_user, peak_factor):
    avg = dau * per_user / 86_400
    return (round(avg), round(avg * peak_factor))


Q(None, "How Much Storage?", "Easy", "Items × size × time × replicas",
  "Each day <code>items</code> new records of <code>bytes_each</code> bytes are stored, kept for <code>years</code> years with <code>replicas</code> copies. Return terabytes (10¹² bytes), rounded to 1.",
  [((100_000_000, 500, 5, 3), 273.8), ((2_000_000, 2_000_000, 1, 3), 4380.0)],
  ("Step by step: per day, per year, total, replicas.", "O(1)", "O(1)"),
  ("One product.", "O(1)", "O(1)"),
  viz=((100_000_000, 500, 5, 3)))


@B
def storage_tb(items, bytes_each, years, replicas):
    per_day = items * bytes_each
    per_year = per_day * 365
    total = per_year * years * replicas
    return round(total / 1e12, 1)


@O
def storage_tb(items, bytes_each, years, replicas):
    return round(items * bytes_each * 365 * years * replicas / 1e12, 1)


Q(None, "Bandwidth In and Out", "Easy", "MB per second",
  "Writes arrive at <code>write_qps</code> of <code>write_kb</code> KB each; reads at <code>read_qps</code> of <code>read_kb</code> KB each. Return <code>(ingress MB/s, egress MB/s)</code> rounded to 1 (1 MB = 1000 KB).",
  [((2000, 1, 40000, 50), (2.0, 2000.0))],
  ("Two products and divisions.", "O(1)", "O(1)"),
  ("One tuple expression.", "O(1)", "O(1)"),
  viz=((2000, 1, 40000, 50)))


@B
def bandwidth(write_qps, write_kb, read_qps, read_kb):
    ingress = write_qps * write_kb / 1000
    egress = read_qps * read_kb / 1000
    return (round(ingress, 1), round(egress, 1))


@O
def bandwidth(write_qps, write_kb, read_qps, read_kb):
    return tuple(round(q * kb / 1000, 1) for q, kb in ((write_qps, write_kb), (read_qps, read_kb)))


Q(None, "Read-Heavy or Write-Heavy?", "Easy", "Shape the design",
  "Given reads and writes per second, return <code>(ratio reads:writes rounded to 1, label)</code>: 'read-heavy' if the ratio ≥ 10, 'write-heavy' if ≤ 0.5, else 'balanced'. Read-heavy systems lean on caches and replicas; write-heavy ones on partitioning and log-structured storage.",
  [((50000, 500), (100.0, 'read-heavy')), ((2000, 8000), (0.2, 'write-heavy')), ((3000, 1500), (2.0, 'balanced'))],
  ("An if-chain.", "O(1)", "O(1)"),
  ("A conditional expression.", "O(1)", "O(1)"),
  viz=((50000, 500)))


@B
def workload(reads, writes):
    ratio = reads / writes
    if ratio >= 10:
        label = "read-heavy"
    elif ratio <= 0.5:
        label = "write-heavy"
    else:
        label = "balanced"
    return (round(ratio, 1), label)


@O
def workload(reads, writes):
    r = reads / writes
    return (round(r, 1), "read-heavy" if r >= 10 else "write-heavy" if r <= 0.5 else "balanced")


LATENCY_US = {"memory": 0.1, "ssd_read": 100, "disk_seek": 10_000, "same_dc": 500, "cross_region": 150_000, "cache_hit": 1_000}


Q(None, "Add Up a Request's Latency", "Easy", "Latency numbers",
  "Using typical latencies in microseconds (<code>LATENCY_US</code>), return the total in milliseconds (rounded to 2) for a request path given as a list of steps.",
  [((["same_dc", "cache_hit", "same_dc", "ssd_read"],), 2.1), ((["cross_region", "disk_seek", "cross_region"],), 310.0)],
  ("Loop and add.", "O(n)", "O(1)"),
  ("<code>sum</code> with a lookup.", "O(n)", "O(1)"),
  viz=((["same_dc", "cache_hit", "ssd_read"],)))


@B
def path_ms(steps):
    total = 0
    for s in steps:
        total += LATENCY_US[s]
    return round(total / 1000, 2)


@O
def path_ms(steps):
    return round(sum(map(LATENCY_US.get, steps)) / 1000, 2)


Q(None, "What Do the Nines Mean?", "Easy", "Availability → downtime",
  "For each availability percentage, return the allowed downtime per year in minutes and per 30-day month in minutes, both rounded to 1.",
  [(([99.0, 99.9, 99.99, 99.999],), [(5256.0, 432.0), (525.6, 43.2), (52.6, 4.3), (5.3, 0.4)])],
  ("Minutes per year × (1 − a).", "O(n)", "O(n)"),
  ("A comprehension.", "O(n)", "O(n)"),
  viz=(([99.9, 99.99],)))


@B
def downtime(levels):
    out = []
    for a in levels:
        down = 1 - a / 100
        out.append((round(365 * 24 * 60 * down, 1), round(30 * 24 * 60 * down, 1)))
    return out


@O
def downtime(levels):
    return [(round(525_600 * (1 - a / 100), 1), round(43_200 * (1 - a / 100), 1)) for a in levels]


Q(None, "Availability in Series and in Parallel", "Medium", "Dependencies vs redundancy",
  "A request needs every component in <code>chain</code> (availability fractions). One of them, at index <code>k</code>, can be made redundant with <code>copies</code> independent copies. Return <code>(availability before, after)</code> as percentages rounded to 3.",
  [(([0.999, 0.995, 0.9999], 1, 2), (99.391, 99.888)), (([0.99, 0.99, 0.99], 0, 3), (97.03, 98.01))],
  ("Multiply in a loop; the redundant part is 1 − (1 − a)ⁿ.", "O(n)", "O(n)"),
  ("<code>math.prod</code>.", "O(n)", "O(n)"),
  viz=(([0.999, 0.995, 0.9999], 1, 2)))


@B
def availability(chain, k, copies):
    before = 1.0
    for a in chain:
        before *= a
    after = 1.0
    for i, a in enumerate(chain):
        after *= (1 - (1 - a) ** copies) if i == k else a
    return (round(before * 100, 3), round(after * 100, 3))


@O
def availability(chain, k, copies):
    improved = [1 - (1 - a) ** copies if i == k else a for i, a in enumerate(chain)]
    return (round(math.prod(chain) * 100, 3), round(math.prod(improved) * 100, 3))


Q(None, "How Many Servers?", "Easy", "Capacity with headroom",
  "Each server handles <code>per_server</code> requests per second; run them at most at <code>util</code> utilisation, and add <code>spare</code> extra servers so one failure (or a deploy) doesn't overload the rest. Return the server count for <code>peak</code> QPS.",
  [((120_000, 2_000, 0.7, 1), 87), ((500, 2_000, 0.7, 1), 2)],
  ("Increase n until n × capacity ≥ peak.", "O(n)", "O(1)"),
  ("Ceiling division.", "O(1)", "O(1)"),
  viz=((120_000, 2_000, 0.7, 1)))


@B
def servers(peak, per_server, util, spare):
    n = 0
    while n * per_server * util < peak:
        n += 1
    return n + spare


@O
def servers(peak, per_server, util, spare):
    return math.ceil(round(peak / (per_server * util), 9)) + spare


Q(None, "How Big a Cache?", "Easy", "The 80/20 rule",
  "Cache the hottest <code>hot_share</code> of the objects read each day: <code>daily_reads</code> reads of <code>kb</code> KB, where each distinct object is read <code>reads_per_object</code> times a day on average. Return GB needed (1 GB = 10⁶ KB), rounded to 1.",
  [((1_000_000_000, 10, 20, 0.2), 100.0)],
  ("Distinct objects, then the hot share, then size.", "O(1)", "O(1)"),
  ("One expression.", "O(1)", "O(1)"),
  viz=((1_000_000_000, 10, 20, 0.2)))


@B
def cache_gb(daily_reads, kb, reads_per_object, hot_share):
    distinct = daily_reads / reads_per_object
    hot = distinct * hot_share
    return round(hot * kb / 1e6, 1)


@O
def cache_gb(daily_reads, kb, reads_per_object, hot_share):
    return round(daily_reads / reads_per_object * hot_share * kb / 1e6, 1)


Q(None, "How Many Shards?", "Medium", "Size and throughput both count",
  "Each shard holds at most <code>shard_tb</code> TB and serves <code>shard_qps</code> QPS. Return <code>(shards for data, shards for traffic, shards needed)</code> for <code>data_tb</code> TB at <code>qps</code>.",
  [((120, 2, 300_000, 25_000), (60, 12, 60)), ((10, 2, 300_000, 25_000), (5, 12, 12))],
  ("Two ceiling divisions and a max.", "O(1)", "O(1)"),
  ("Same with <code>math.ceil</code>.", "O(1)", "O(1)"),
  viz=((120, 2, 300_000, 25_000)))


@B
def shards(data_tb, shard_tb, qps_, shard_qps):
    by_data = data_tb // shard_tb + (1 if data_tb % shard_tb else 0)
    by_qps = qps_ // shard_qps + (1 if qps_ % shard_qps else 0)
    return (by_data, by_qps, max(by_data, by_qps))


@O
def shards(data_tb, shard_tb, qps_, shard_qps):
    d, q = math.ceil(data_tb / shard_tb), math.ceil(qps_ / shard_qps)
    return (d, q, max(d, q))


Q(None, "Open Connections (Little's Law)", "Easy", "Concurrency",
  "Requests arrive at <code>rps</code> per second and stay open for <code>secs</code> seconds on average (long-polling and websockets stay open much longer). Return the number of concurrent connections.",
  [((50_000, 0.2), 10000), ((2_000, 300), 600000)],
  ("Multiply.", "O(1)", "O(1)"),
  ("Multiply and round.", "O(1)", "O(1)"),
  viz=((50_000, 0.2)))


@B
def concurrent(rps, secs):
    return round(rps * secs)


@O
def concurrent(rps, secs):
    return round(rps * secs)


Q(None, "Fan-Out Makes the Tail Worse", "Medium", "Tail latency",
  "A request calls <code>n</code> back-end services in parallel and waits for all. If each is fast 99% of the time (p99), what % of requests hit at least one slow call? Return values for each n, rounded to 1.",
  [(([1, 10, 50, 100],), [1.0, 9.6, 39.5, 63.4])],
  ("1 − 0.99ⁿ in a loop.", "O(n)", "O(n)"),
  ("A comprehension.", "O(n)", "O(n)"),
  viz=(([1, 10, 100],)))


@B
def slow_share(ns):
    out = []
    for n in ns:
        out.append(round((1 - 0.99 ** n) * 100, 1))
    return out


@O
def slow_share(ns):
    return [round((1 - 0.99 ** n) * 100, 1) for n in ns]


Q(None, "Human-Readable Sizes", "Easy", "Units",
  "Format a number of bytes as the largest unit (B, KB, MB, GB, TB, PB, base 1000) that keeps the value ≥ 1, with one decimal place, e.g. '1.5 GB'.",
  [((999,), '999.0 B'), ((1_500_000_000,), '1.5 GB'), ((2.3e15,), '2.3 PB')],
  ("Divide by 1000 in a loop.", "O(1)", "O(1)"),
  ("<code>log10</code> picks the unit directly.", "O(1)", "O(1)"),
  viz=((1_500_000_000,)))


@B
def human(nbytes):
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    value = nbytes
    while value >= 1000 and i < len(units) - 1:
        value /= 1000
        i += 1
    return f"{value:.1f} {units[i]}"


@O
def human(nbytes):
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = min(len(units) - 1, int(math.log10(nbytes) // 3)) if nbytes >= 1 else 0
    return f"{nbytes / 1000 ** i:.1f} {units[i]}"


Q(None, "How Long Must an ID Be?", "Easy", "Bits and characters",
  "To give <code>n</code> things unique IDs, return <code>(bits needed, base-62 characters needed)</code>.",
  [((1_000_000,), (20, 4)), ((3_500_000_000_000,), (42, 7))],
  ("Double / multiply until the capacity reaches n.", "O(log n)", "O(1)"),
  ("Logarithms with a ceiling.", "O(1)", "O(1)"),
  viz=((1_000_000,)))


@B
def id_length(n):
    bits, cap = 0, 1
    while cap < n:
        cap *= 2
        bits += 1
    chars, cap = 0, 1
    while cap < n:
        cap *= 62
        chars += 1
    return (bits, chars)


@O
def id_length(n):
    return (math.ceil(math.log2(n)), math.ceil(round(math.log(n, 62), 12)))


Q(None, "What Will Storage Cost?", "Easy", "Money matters in design",
  "Store <code>tb</code> TB on standard storage at <code>std</code> $/GB-month, or keep the newest <code>hot_share</code> on standard and move the rest to archive storage at <code>archive</code> $/GB-month. Return <code>(monthly $ all-standard, monthly $ tiered)</code> rounded to 0.",
  [((500, 0.023, 0.004, 0.1), (11500, 2950))],
  ("Two products.", "O(1)", "O(1)"),
  ("Same, with GB computed once.", "O(1)", "O(1)"),
  viz=(500, 0.023, 0.004, 0.1))


@B
def storage_cost(tb, std, archive, hot_share):
    gb = tb * 1000
    all_std = gb * std
    tiered = gb * hot_share * std + gb * (1 - hot_share) * archive
    return (round(all_std), round(tiered))


@O
def storage_cost(tb, std, archive, hot):
    gb = tb * 1000
    return (round(gb * std), round(gb * (hot * std + (1 - hot) * archive)))


Q(None, "When Will We Run Out?", "Medium", "Growth planning",
  "Storage is <code>used</code> TB of <code>capacity</code> TB and grows <code>pct</code>% a month (compounding). Return the number of whole months until it's full (the first month the usage exceeds capacity).",
  [((40, 100, 8), 12), ((90, 100, 1), 11)],
  ("Multiply month by month.", "O(months)", "O(1)"),
  ("Solve with logarithms, then ceiling.", "O(1)", "O(1)"),
  viz=((40, 100, 8)))


@B
def months_left(used, capacity, pct):
    months = 0
    while used <= capacity:
        used *= 1 + pct / 100
        months += 1
    return months


@O
def months_left(used, capacity, pct):
    m = math.log(capacity / used) / math.log(1 + pct / 100)
    return math.floor(m) + 1


SCHEMA = {"user_id": "bigint", "created_at": "timestamp", "text": ("varchar", 140), "lat": "double", "lon": "double",
          "flags": "int", "media_url": ("varchar", 200)}
SIZES = {"bigint": 8, "int": 4, "double": 8, "timestamp": 8, "bool": 1}


Q(None, "How Big Is One Record?", "Easy", "Size from the schema",
  "Add up a record's size: fixed types from <code>SIZES</code>, and <code>(varchar, n)</code> fields at n bytes (worst case). Return bytes, and the size of a million records in MB (rounded to 1).",
  [((SCHEMA,), (376, 376))],
  ("A loop with an isinstance check.", "O(f)", "O(1)"),
  ("<code>sum</code> over a conditional expression.", "O(f)", "O(1)"),
  viz=((SCHEMA,)))


@B
def record_size(schema):
    total = 0
    for t in schema.values():
        if isinstance(t, tuple):
            total += t[1]
        else:
            total += SIZES[t]
    return (total, round(total * 1_000_000 / 1e6, 1))


@O
def record_size(schema):
    total = sum(t[1] if isinstance(t, tuple) else SIZES[t] for t in schema.values())
    return (total, round(total, 1))


NFR = ["latency", "available", "availability", "scale", "durable", "consistent", "secure", "throughput", "cost", "within", "ms", "99."]


Q(None, "Functional or Non-Functional?", "Easy", "Requirements first",
  "Sort requirement statements: non-functional if they mention any keyword in <code>NFR</code> (case-insensitive), otherwise functional. Return <code>(functional, non_functional)</code> lists in order. Clarifying both kinds is the first five minutes of every design interview.",
  [((["Users can shorten a long URL", "Redirects complete within 100 ms", "Links never expire unless deleted", "The service is available 99.99% of the time", "Users can see click counts"],), (['Users can shorten a long URL', 'Links never expire unless deleted', 'Users can see click counts'], ['Redirects complete within 100 ms', 'The service is available 99.99% of the time']))],
  ("A loop over statements and keywords.", "O(s · k)", "O(s)"),
  ("<code>any</code> inside two comprehensions.", "O(s · k)", "O(s)"),
  viz=((["Users can shorten a long URL", "Redirects complete within 100 ms"],)))


@B
def split_requirements(statements):
    func, nonfunc = [], []
    for s in statements:
        found = False
        for k in NFR:
            if k in s.lower():
                found = True
                break
        (nonfunc if found else func).append(s)
    return (func, nonfunc)


@O
def split_requirements(statements):
    nf = lambda s: any(k in s.lower() for k in NFR)
    return ([s for s in statements if not nf(s)], [s for s in statements if nf(s)])


Q(None, "Estimate a Whole System", "Medium", "Putting it together",
  "For a photo app: <code>dau</code> users, each uploads <code>uploads</code> photos a day of <code>mb</code> MB and views <code>views</code> photos a day. Return a dict: upload QPS (avg, rounded), view QPS (avg, rounded), new storage per day in TB (rounded to 1), and egress in GB/s at average load (rounded to 1).",
  [((50_000_000, 0.2, 2, 60), {'upload_qps': 116, 'view_qps': 34722, 'storage_tb_per_day': 20.0, 'egress_gb_s': 69.4})],
  ("Compute each figure step by step.", "O(1)", "O(1)"),
  ("A dict built from shared intermediate values.", "O(1)", "O(1)"),
  viz=(50_000_000, 0.2, 2, 60))


@B
def photo_app(dau, uploads, mb, views):
    upload_qps = dau * uploads / 86400
    view_qps = dau * views / 86400
    storage_tb = dau * uploads * mb / 1e6
    egress = view_qps * mb / 1000
    return {"upload_qps": round(upload_qps), "view_qps": round(view_qps),
            "storage_tb_per_day": round(storage_tb, 1), "egress_gb_s": round(egress, 1)}


@O
def photo_app(dau, up, mb, views):
    vq = dau * views / 86_400
    return {"upload_qps": round(dau * up / 86_400), "view_qps": round(vq),
            "storage_tb_per_day": round(dau * up * mb / 1e6, 1), "egress_gb_s": round(vq * mb / 1000, 1)}


HOURLY = [20, 12, 8, 6, 6, 10, 30, 60, 90, 110, 120, 125, 130, 120, 115, 110, 120, 140, 180, 220, 240, 200, 120, 60]


Q(None, "Find the Real Peak From Traffic", "Medium", "Use data, not guesses",
  "<code>hourly</code> holds thousands of requests in each hour of a day. Return <code>(average QPS, peak-hour QPS, peak ÷ average rounded to 2)</code>, QPS rounded to whole numbers. Design for the peak (and the busiest minute inside it is higher still).",
  [((HOURLY,), (27, 67, 2.45))],
  ("Sum and max in a loop.", "O(24)", "O(1)"),
  ("<code>sum</code> and <code>max</code>.", "O(24)", "O(1)"),
  viz=((HOURLY,)))


@B
def real_peak(hourly):
    total, peak = 0, 0
    for h in hourly:
        total += h
        if h > peak:
            peak = h
    avg_qps = total * 1000 / 86400
    peak_qps = peak * 1000 / 3600
    return (round(avg_qps), round(peak_qps), round(peak_qps / avg_qps, 2))


@O
def real_peak(hourly):
    avg, peak = sum(hourly) * 1000 / 86_400, max(hourly) * 1000 / 3600
    return (round(avg), round(peak), round(peak / avg, 2))
