from lib import *
import bisect
import hashlib
import heapq
import math
from collections import Counter, defaultdict

TOPIC(
    id="search_reliability", title="Search, Storage, Reliability & the Interview", glyph="🛡",
    blurb="The last building blocks and how to put it all together: inverted indexes, AND queries, TF-IDF, autocomplete, top-K, geohashes and nearby search, file chunking and dedupe, resumable and multipart uploads, erasure coding, SLOs, error budgets and burn rates, percentiles, retry storms, load shedding, disaster recovery, canaries — and the 45-minute interview framework.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">inverted index: term → sorted doc ids;  AND = intersect posting lists
geohash: interleave lon/lat bits → base32; same prefix ≈ nearby (check neighbours too)
error budget = (1 − SLO) × window;  burn rate = error rate / (1 − SLO)
interview: requirements → estimates → API → data model → high level → deep dives → wrap up</code></pre>
""")


Q(None, "Build an Inverted Index", "Easy", "The heart of search",
  "Lower-case each document, split on spaces, and map every term to the sorted list of document ids containing it. Return the index with terms sorted.",
  [(({1: "Cheap red shoes", 2: "red dress", 3: "running shoes for men", 4: "Red running shoes"},), {'cheap': [1], 'dress': [2], 'for': [3], 'men': [3], 'red': [1, 2, 4], 'running': [3, 4], 'shoes': [1, 3, 4]})],
  ("For each term, scan every document.", "O(t · d · L)", "O(t · d)"),
  ("One pass with <code>defaultdict(set)</code>.", "O(d · L)", "O(t · d)"),
  viz=(({1: "a b", 2: "b"},)))


@B
def inverted_index(docs):
    terms = sorted(set(w for text in docs.values() for w in text.lower().split()))
    index = {}
    for t in terms:
        index[t] = sorted(i for i, text in docs.items() if t in text.lower().split())
    return index


@O
def inverted_index(docs):
    index = defaultdict(set)
    for i, text in docs.items():
        for w in text.lower().split():
            index[w].add(i)
    return {t: sorted(ids) for t, ids in sorted(index.items())}


Q(None, "Intersect Posting Lists", "Easy", "AND queries",
  "Return the doc ids present in both sorted posting lists. Search engines walk both lists with two pointers (and skip pointers) instead of building sets.",
  [(([1, 3, 4, 7, 9, 12, 15, 20], [2, 3, 7, 8, 15, 21]), [3, 7, 15])],
  ("Check each id of one list against the other.", "O(a · b)", "O(1)"),
  ("Two pointers.", "O(a + b)", "O(1)"),
  viz=(([1, 2, 5], [2, 5, 6])))


@B
def intersect(a, b):
    return [x for x in a if x in b]


@O
def intersect(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            out.append(a[i])
            i, j = i + 1, j + 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    return out


Q(None, "Rank Results With TF-IDF", "Medium", "Rare words matter more",
  "Score each document for the query terms as Σ tf × log(N / df) (tf = count of the term in the doc, df = docs containing it). Return <code>(doc id, score rounded to 3)</code> for documents with a positive score, best first (ties by id).",
  [(({1: "red shoes red", 2: "blue shoes", 3: "red dress", 4: "running shoes"}, "red shoes"), [(1, 1.674), (3, 0.693), (2, 0.288), (4, 0.288)])],
  ("Count terms by scanning text for every query term and doc.", "O(q · d · L)", "O(d)"),
  ("Precompute term counts and document frequencies.", "O(d · L + q · d)", "O(d · L)"),
  viz=(({1: "a b", 2: "b"}, "a")))


@B
def tfidf(docs, query):
    n = len(docs)
    scores = []
    for i, text in docs.items():
        words = text.split()
        s = 0
        for t in query.split():
            tf = words.count(t)
            df = sum(1 for other in docs.values() if t in other.split())
            if tf and df:
                s += tf * math.log(n / df)
        if s > 0:
            scores.append((i, round(s, 3)))
    scores.sort(key=lambda x: (-x[1], x[0]))
    return scores


@O
def tfidf(docs, query):
    counts = {i: Counter(t.split()) for i, t in docs.items()}
    df = Counter(w for c in counts.values() for w in c)
    idf = {t: math.log(len(docs) / df[t]) for t in query.split() if df[t]}
    scores = [(i, round(sum(c[t] * w for t, w in idf.items()), 3)) for i, c in counts.items()]
    return sorted([s for s in scores if s[1] > 0], key=lambda x: (-x[1], x[0]))


Q(None, "Autocomplete", "Medium", "Top suggestions for a prefix",
  "Given past search counts, return the <code>k</code> most searched queries starting with each prefix (ties alphabetical).",
  [(({"iphone": 900, "iphone case": 400, "ipad": 700, "ice cream": 300, "iphone charger": 400, "idli": 50}, ["ip", "iphone ", "i", "x"], 3), [['iphone', 'ipad', 'iphone case'], ['iphone case', 'iphone charger'], ['iphone', 'ipad', 'iphone case'], []])],
  ("Scan all queries for each prefix, then sort.", "O(p · n log n)", "O(n)"),
  ("Sort once; <code>bisect</code> to the prefix range.", "O(n log n + p · r log r)", "O(n)"),
  viz=(({"ab": 2, "ac": 5}, ["a"], 1)))


@B
def autocomplete(counts, prefixes, k):
    out = []
    for p in prefixes:
        matches = [(-c, q) for q, c in counts.items() if q.startswith(p)]
        matches.sort()
        out.append([q for _, q in matches[:k]])
    return out


@O
def autocomplete(counts, prefixes, k):
    keys = sorted(counts)
    out = []
    for p in prefixes:
        lo, hi = bisect.bisect_left(keys, p), bisect.bisect_left(keys, p + "￿")
        out.append(heapq.nsmallest(k, keys[lo:hi], key=lambda q: (-counts[q], q)))
    return out


Q(None, "Top-K Trending Searches", "Easy", "Heavy hitters",
  "Return the <code>k</code> most frequent search terms in the stream with counts (ties alphabetical).",
  [((["ipl", "gold", "ipl", "rain", "ipl", "gold", "budget", "rain", "rain", "gold", "ipl"], 3), [('ipl', 4), ('gold', 3), ('rain', 3)])],
  ("Count and fully sort.", "O(n + u log u)", "O(u)"),
  ("Counter and <code>heapq.nsmallest</code> with k.", "O(n + u log k)", "O(u)"),
  viz=((["a", "b", "a"], 1)))


@B
def top_k_terms(stream, k):
    counts = {}
    for s in stream:
        counts[s] = counts.get(s, 0) + 1
    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:k]


@O
def top_k_terms(stream, k):
    return heapq.nsmallest(k, Counter(stream).items(), key=lambda x: (-x[1], x[0]))


BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"


Q(None, "Encode a Geohash", "Medium", "Locations as sortable strings",
  "Encode each <code>(lat, lon)</code> as a geohash of <code>precision</code> characters: alternately halve the longitude and latitude ranges (longitude first), writing 1 for the upper half, and map each 5 bits to base32. Nearby places share prefixes.",
  [(([(28.6139, 77.2090), (28.6129, 77.2295), (19.0760, 72.8777), (51.5074, -0.1278)], 6), ['ttnfuc', 'ttnfv2', 'te7ud2', 'gcpvj0'])],
  ("Build a list of bits, then convert.", "O(n · p)", "O(p)"),
  ("Accumulate 5-bit integers directly.", "O(n · p)", "O(p)"),
  viz=(([(12.97, 77.59)], 4)))


@B
def geohash(points, precision):
    out = []
    for lat, lon in points:
        lat_r, lon_r = [-90.0, 90.0], [-180.0, 180.0]
        bits = []
        even = True
        while len(bits) < precision * 5:
            rng, val = (lon_r, lon) if even else (lat_r, lat)
            mid = (rng[0] + rng[1]) / 2
            if val >= mid:
                bits.append(1)
                rng[0] = mid
            else:
                bits.append(0)
                rng[1] = mid
            even = not even
        s = ""
        for i in range(0, len(bits), 5):
            s += BASE32[int("".join(map(str, bits[i:i + 5])), 2)]
        out.append(s)
    return out


@O
def geohash(points, precision):
    def enc(lat, lon):
        rngs, vals, chars, bit, ch, even = [[-180.0, 180.0], [-90.0, 90.0]], [lon, lat], [], 0, 0, 0
        while len(chars) < precision:
            r, v = rngs[even], vals[even]
            mid = (r[0] + r[1]) / 2
            up = v >= mid
            ch = ch << 1 | up
            r[0 if up else 1] = mid
            even, bit = 1 - even, bit + 1
            if bit == 5:
                chars.append(BASE32[ch])
                bit = ch = 0
        return "".join(chars)
    return [enc(lat, lon) for lat, lon in points]


def km(a, b):
    lat1, lon1, lat2, lon2 = map(math.radians, (*a, *b))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))


Q(None, "Find Nearby Places", "Medium", "Grid cells instead of scanning everything",
  "Return <code>(name, km rounded to 2)</code> for places within <code>radius_km</code> of <code>me</code>, nearest first. The optimal version buckets places into grid cells of <code>cell</code> degrees and only checks the 9 cells around you (valid while the radius is smaller than a cell).",
  [(({"cafe": (28.6145, 77.2100), "mall": (28.6300, 77.2200), "park": (28.6000, 77.2500), "temple": (28.6129, 77.2295), "airport": (28.5562, 77.1000)}, (28.6139, 77.2090), 3.0, 0.05), [('cafe', 0.12), ('temple', 2.0), ('mall', 2.09)])],
  ("Haversine distance to every place.", "O(n)", "O(1)"),
  ("Grid buckets, then 9 cells.", "O(n) build, O(nearby) query", "O(n)"),
  viz=(({"a": (0.0, 0.0), "b": (1.0, 1.0)}, (0.0, 0.01), 5.0, 0.1)))


@B
def nearby(places, me, radius_km, cell):
    out = []
    for name, p in places.items():
        d = km(me, p)
        if d <= radius_km:
            out.append((round(d, 2), name))
    out.sort()
    return [(n, d) for d, n in out]


@O
def nearby(places, me, radius_km, cell):
    grid = defaultdict(list)
    for name, (lat, lon) in places.items():
        grid[int(lat // cell), int(lon // cell)].append(name)
    ci, cj = int(me[0] // cell), int(me[1] // cell)
    found = []
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            for name in grid.get((ci + di, cj + dj), []):
                d = km(me, places[name])
                if d <= radius_km:
                    found.append((round(d, 2), name))
    return [(n, d) for d, n in sorted(found)]


Q(None, "Chunk and Deduplicate Files", "Medium", "Upload only what changed",
  "Split each file version into chunks of <code>size</code> characters and identify chunks by SHA-256. Return <code>(chunks in v2, chunks the client must upload)</code> given the server already stores v1's chunks (Dropbox-style sync).",
  [(("the quick brown fox jumps over the lazy dog!", "the quick brown cat jumps over the lazy dog!", 8), (6, 1))],
  ("Compare chunk strings against a list.", "O(c²)", "O(c)"),
  ("A set of chunk hashes.", "O(c)", "O(c)"),
  viz=(("aaaabbbb", "aaaacccc", 4)))


@B
def chunk_dedupe(v1, v2, size):
    old = [v1[i:i + size] for i in range(0, len(v1), size)]
    new = [v2[i:i + size] for i in range(0, len(v2), size)]
    upload = []
    for c in new:
        if c not in old and c not in upload:
            upload.append(c)
    return (len(new), len(upload))


@O
def chunk_dedupe(v1, v2, size):
    def hashes(s):
        return [hashlib.sha256(s[i:i + size].encode()).hexdigest() for i in range(0, len(s), size)]
    old, new = set(hashes(v1)), hashes(v2)
    return (len(new), len(set(new) - old))


Q(None, "Resume an Interrupted Upload", "Easy", "Missing chunk ranges",
  "A file has chunks 0..n-1 and the server has received the listed ones. Return the missing chunks as inclusive <code>(start, end)</code> ranges so the client re-sends only those.",
  [((12, [0, 1, 2, 5, 6, 9]), [(3, 4), (7, 8), (10, 11)])],
  ("Walk 0..n-1 building ranges.", "O(n)", "O(n)"),
  ("Same walk over a set.", "O(n)", "O(n)"),
  viz=((5, [0, 3])))


@B
def missing_ranges(n, received):
    out, start = [], None
    for i in range(n):
        if i not in received:
            if start is None:
                start = i
        elif start is not None:
            out.append((start, i - 1))
            start = None
    if start is not None:
        out.append((start, n - 1))
    return out


@O
def missing_ranges(n, received):
    got, out, i = set(received), [], 0
    while i < n:
        if i in got:
            i += 1
            continue
        j = i
        while j + 1 < n and j + 1 not in got:
            j += 1
        out.append((i, j))
        i = j + 1
    return out


Q(None, "Pick a Multipart Part Size", "Easy", "Object storage limits",
  "Object stores allow at most 10,000 parts of at least 5 MB. For each file size (MB), use the smallest whole-MB part size ≥ 5 that keeps parts ≤ 10,000. Return <code>(part MB, parts)</code>.",
  [(([3, 100, 49_000, 200_000, 5_000_000],), [(5, 1), (5, 20), (5, 9800), (20, 10000), (500, 10000)])],
  ("Increase the part size until the count fits.", "O(n · s)", "O(1)"),
  ("Ceiling division.", "O(n)", "O(1)"),
  viz=(([60_000],)))


@B
def part_size(files_mb):
    out = []
    for size in files_mb:
        part = 5
        while math.ceil(size / part) > 10_000:
            part += 1
        out.append((part, math.ceil(size / part)))
    return out


@O
def part_size(files_mb):
    out = []
    for size in files_mb:
        part = max(5, math.ceil(size / 10_000))
        out.append((part, math.ceil(size / part)))
    return out


Q(None, "Replication vs Erasure Coding", "Easy", "Durability per byte",
  "Store <code>data_tb</code>. Return <code>(raw TB, failures tolerated)</code> for 3× replication and for each Reed-Solomon (k data, m parity) scheme in <code>schemes</code> (raw = data × (k + m) / k).",
  [((100, [(6, 3), (10, 4)]), [(300, 2), (150.0, 3), (140.0, 4)])],
  ("Loop over the schemes.", "O(s)", "O(s)"),
  ("A comprehension.", "O(s)", "O(s)"),
  viz=((10, [(4, 2)])))


@B
def erasure(data_tb, schemes):
    out = [(data_tb * 3, 2)]
    for k, m in schemes:
        out.append((round(data_tb * (k + m) / k, 1), m))
    return out


@O
def erasure(data_tb, schemes):
    return [(data_tb * 3, 2)] + [(round(data_tb * (k + m) / k, 1), m) for k, m in schemes]


Q(None, "SLOs and Error Budgets", "Easy", "How much downtime may we spend?",
  "For an availability SLO (%) over <code>days</code>, return <code>(budget minutes, minutes left after <code>used</code>, % of budget burned)</code>, rounded to 1.",
  [((99.9, 30, 20), (43.2, 23.2, 46.3)), ((99.99, 30, 5), (4.3, -0.7, 115.7))],
  ("Arithmetic step by step.", "O(1)", "O(1)"),
  ("Same, compact.", "O(1)", "O(1)"),
  viz=((99.0, 1, 10)))


@B
def error_budget(slo, days, used):
    total = days * 24 * 60
    budget = total * (100 - slo) / 100
    left = budget - used
    burned = used / budget * 100
    return (round(budget, 1), round(left, 1), round(burned, 1))


@O
def error_budget(slo, days, used):
    budget = days * 1440 * (1 - slo / 100)
    return (round(budget, 1), round(budget - used, 1), round(used / budget * 100, 1))


Q(None, "Burn-Rate Alerts", "Medium", "Page on fast budget burn",
  "Burn rate = error rate / (1 − SLO). A burn rate of 14.4 over an hour spends 2% of a 30-day budget in that hour. For hourly error rates (%), return each hour's burn rate (rounded to 1) and the hours (indexes) to page on (≥ <code>threshold</code>).",
  [(([0.05, 0.2, 1.5, 3.0, 0.1], 99.9, 14.4), ([0.5, 2.0, 15.0, 30.0, 1.0], [2, 3]))],
  ("A loop.", "O(n)", "O(n)"),
  ("Comprehensions.", "O(n)", "O(n)"),
  viz=(([0.5], 99.0, 14.4)))


@B
def burn_rate(error_pct, slo, threshold):
    rates, page = [], []
    for i, e in enumerate(error_pct):
        r = e / (100 - slo)
        rates.append(round(r, 1))
        if r >= threshold:
            page.append(i)
    return (rates, page)


@O
def burn_rate(error_pct, slo, threshold):
    raw = [e / (100 - slo) for e in error_pct]
    return ([round(r, 1) for r in raw], [i for i, r in enumerate(raw) if r >= threshold])


Q(None, "Latency Percentiles", "Easy", "Averages hide the tail",
  "Return the mean (rounded to 1) and the nearest-rank p50, p95 and p99 of the latencies (ms). One slow request barely moves the median but dominates p99.",
  [(([12, 15, 11, 13, 900, 14, 12, 16, 13, 12, 11, 14, 15, 13, 12, 18, 13, 12, 14, 450],), (79.5, 13, 450, 900))],
  ("Sort, then index.", "O(n log n)", "O(n)"),
  ("Same, via a helper.", "O(n log n)", "O(n)"),
  viz=(([1, 2, 3, 100],)))


@B
def percentiles(lat):
    s = sorted(lat)
    n = len(s)
    out = [round(sum(s) / n, 1)]
    for p in (50, 95, 99):
        rank = math.ceil(p / 100 * n)
        out.append(s[rank - 1])
    return tuple(out)


@O
def percentiles(lat):
    s = sorted(lat)
    pick = lambda p: s[math.ceil(p / 100 * len(s)) - 1]
    return (round(sum(s) / len(s), 1), pick(50), pick(95), pick(99))


Q(None, "Retry Storms", "Medium", "Retries multiply across layers",
  "A request passes through layers that each retry a failed call <code>r</code> times. If the bottom service is down, one user request causes ∏(r + 1) calls to it. Return the amplification for each stack, and for the same stack if only the top layer retries.",
  [(([[2, 2, 2], [3, 3, 3, 3], [1, 0, 0]],), [(27, 3), (256, 4), (2, 2)])],
  ("Multiply in a loop.", "O(s · l)", "O(s)"),
  ("<code>math.prod</code>.", "O(s · l)", "O(s)"),
  viz=(([[2, 2]],)))


@B
def retry_storm(stacks):
    out = []
    for layers in stacks:
        total = 1
        for r in layers:
            total *= r + 1
        out.append((total, layers[0] + 1))
    return out


@O
def retry_storm(stacks):
    return [(math.prod(r + 1 for r in layers), layers[0] + 1) for layers in stacks]


Q(None, "Shed Load by Priority", "Medium", "Degrade gracefully",
  "Under overload you can serve only <code>capacity</code> requests. Keep the highest-priority ones (priority 0 = critical, e.g. checkout; higher = less important), earliest first within a priority. Return the served ids in arrival order.",
  [(([("r1", 2), ("r2", 0), ("r3", 1), ("r4", 2), ("r5", 0), ("r6", 1), ("r7", 3)], 4), ['r2', 'r3', 'r5', 'r6'])],
  ("Sort by (priority, arrival), take the top, re-sort.", "O(n log n)", "O(n)"),
  ("<code>heapq.nsmallest</code> then sort indexes.", "O(n log c)", "O(n)"),
  viz=(([("a", 1), ("b", 0)], 1)))


@B
def shed(requests, capacity):
    indexed = [(p, i, rid) for i, (rid, p) in enumerate(requests)]
    indexed.sort()
    kept = indexed[:capacity]
    kept.sort(key=lambda x: x[1])
    return [rid for _, _, rid in kept]


@O
def shed(requests, capacity):
    keep = heapq.nsmallest(capacity, range(len(requests)), key=lambda i: (requests[i][1], i))
    return [requests[i][0] for i in sorted(keep)]


Q(None, "Which Disaster-Recovery Plan Fits?", "Easy", "RPO and RTO",
  "Each plan has <code>(name, rpo_min, rto_min, monthly_cost)</code>: RPO = data you can lose, RTO = time to recover. Return the plans meeting both targets, cheapest first.",
  [(([("backup & restore", 1440, 480, 100), ("pilot light", 15, 60, 800), ("warm standby", 1, 15, 3000), ("active-active", 0, 0, 9000)], 15, 60), ['pilot light', 'warm standby', 'active-active']), (([("backup & restore", 1440, 480, 100), ("pilot light", 15, 60, 800), ("warm standby", 1, 15, 3000), ("active-active", 0, 0, 9000)], 0, 5), ['active-active'])],
  ("Filter in a loop, then sort.", "O(p log p)", "O(p)"),
  ("A sorted comprehension.", "O(p log p)", "O(p)"),
  viz=(([("a", 10, 10, 1)], 15, 15)))


@B
def dr_plans(plans, rpo, rto):
    ok = []
    for name, p_rpo, p_rto, cost in plans:
        if p_rpo <= rpo and p_rto <= rto:
            ok.append((cost, name))
    ok.sort()
    return [name for _, name in ok]


@O
def dr_plans(plans, rpo, rto):
    return [p[0] for p in sorted((p for p in plans if p[1] <= rpo and p[2] <= rto), key=lambda p: p[3])]


Q(None, "Promote or Roll Back the Canary?", "Medium", "Automated canary analysis",
  "Compare the canary's metrics with the baseline: roll back if its error rate exceeds the baseline's by more than <code>err_margin</code> percentage points or its p99 latency is more than <code>lat_ratio</code> times the baseline's. Return the decision and the reasons.",
  [(({"err": 0.4, "p99": 180}, {"err": 0.5, "p99": 190}, 0.5, 1.2), ('promote', [])), (({"err": 0.4, "p99": 180}, {"err": 1.2, "p99": 400}, 0.5, 1.2), ('rollback', ['errors', 'latency']))],
  ("If-statements collecting reasons.", "O(1)", "O(1)"),
  ("A list of checks.", "O(1)", "O(1)"),
  viz=(({"err": 1, "p99": 100}, {"err": 3, "p99": 100}, 1, 1.5)))


@B
def canary(baseline, candidate, err_margin, lat_ratio):
    reasons = []
    if candidate["err"] - baseline["err"] > err_margin:
        reasons.append("errors")
    if candidate["p99"] > baseline["p99"] * lat_ratio:
        reasons.append("latency")
    if reasons:
        return ("rollback", reasons)
    return ("promote", reasons)


@O
def canary(baseline, candidate, err_margin, lat_ratio):
    checks = [("errors", candidate["err"] - baseline["err"] > err_margin),
              ("latency", candidate["p99"] > baseline["p99"] * lat_ratio)]
    reasons = [name for name, bad in checks if bad]
    return ("rollback" if reasons else "promote", reasons)


PHASES = [("requirements", 0.12), ("estimation", 0.08), ("api & data model", 0.12),
          ("high-level design", 0.25), ("deep dives", 0.33), ("wrap up", 0.10)]


Q(None, "Budget Your Interview Time", "Easy", "The framework, in minutes",
  "Split an interview of <code>minutes</code> across <code>PHASES</code> by weight. Return <code>(phase, minutes rounded, minute it ends at)</code>.",
  [((45,), [('requirements', 5, 5), ('estimation', 4, 9), ('api & data model', 5, 14), ('high-level design', 11, 26), ('deep dives', 15, 40), ('wrap up', 4, 45)]), ((60,), [('requirements', 7, 7), ('estimation', 5, 12), ('api & data model', 7, 19), ('high-level design', 15, 34), ('deep dives', 20, 54), ('wrap up', 6, 60)])],
  ("A loop with a running total.", "O(p)", "O(p)"),
  ("<code>itertools.accumulate</code>.", "O(p)", "O(p)"),
  viz=((30,)))


@B
def interview_plan(minutes):
    out, t = [], 0
    for name, w in PHASES:
        t += w * minutes
        out.append((name, round(w * minutes), round(t)))
    return out


@O
def interview_plan(minutes):
    from itertools import accumulate
    ends = accumulate(w * minutes for _, w in PHASES)
    return [(name, round(w * minutes), round(e)) for (name, w), e in zip(PHASES, ends)]


CHECKLIST = ["functional requirements", "non-functional requirements", "estimates", "api", "data model",
             "high-level diagram", "scaling", "bottlenecks", "failure handling", "monitoring"]


Q(None, "Self-Review a Design Answer", "Easy", "Did you cover everything?",
  "Given the topics a practice answer covered, return the <code>CHECKLIST</code> items still missing (in checklist order) and the coverage %, rounded to 1.",
  [((["api", "high-level diagram", "functional requirements", "scaling", "data model", "caching"],), (['non-functional requirements', 'estimates', 'bottlenecks', 'failure handling', 'monitoring'], 50.0))],
  ("Check each item against the list.", "O(c · a)", "O(c)"),
  ("A set of covered topics.", "O(c + a)", "O(a)"),
  viz=((["api"],)))


@B
def design_review(covered):
    missing = []
    for item in CHECKLIST:
        if item not in covered:
            missing.append(item)
    return (missing, round((len(CHECKLIST) - len(missing)) / len(CHECKLIST) * 100, 1))


@O
def design_review(covered):
    have = set(covered)
    missing = [c for c in CHECKLIST if c not in have]
    return (missing, round(100 * (1 - len(missing) / len(CHECKLIST)), 1))
