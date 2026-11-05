from lib import *
import math
import numpy as np


TOPIC(
    id="ml-system-design", title="ML System Design", glyph="⇄",
    blurb="How to answer 'design a recommender, fraud or RAG system': a repeatable framework, back-of-envelope sizing, data and label problems, online vs offline metrics, serving trade-offs and monitoring.",
    theory="""
<h3>The framework, in order</h3>
<ol><li><b>Clarify:</b> users, goal, scale, latency, constraints.</li>
<li><b>Frame it:</b> business metric, ML task, labels.</li>
<li><b>Data:</b> sources, features, leakage, freshness.</li>
<li><b>Model:</b> baseline first, then complexity if earned.</li>
<li><b>Evaluate:</b> offline metrics, then an online experiment.</li>
<li><b>Serve:</b> batch or real-time, latency, cost, fallback.</li>
<li><b>Monitor:</b> drift, quality, retraining, feedback loops.</li></ol>
""")


Q(None, "Requests per Second", "Easy", "Back of the envelope",
  "From daily active users and requests per user per day, return (average QPS, peak QPS at the given peak multiple), rounded to 1 decimal.",
  [((10000000, 20, 3), (2314.8, 6944.4))],
  ("Divide by seconds in a day, step by step.", "O(1)", "O(1)"),
  ("One line.", "O(1)", "O(1)"),
  names=["dau", "per_user", "peak"])


@B
def qps(dau, per_user, peak):
    per_day = dau * per_user
    seconds = 24 * 60 * 60
    average = per_day / seconds
    return (round(average, 1), round(average * peak, 1))


@O
def qps(dau, per_user, peak):
    avg = dau * per_user / 86400
    return (round(avg, 1), round(avg * peak, 1))


Q(None, "Embedding Storage", "Easy", "Will it fit in memory?",
  "Return the GB (10⁹ bytes) needed for n vectors of dimension d, at 4 bytes each, times a replication factor.",
  [((100000000, 768, 2), 614.4), ((1000000, 384, 1), 1.54)],
  ("Multiply one step at a time.", "O(1)", "O(1)"),
  ("One line.", "O(1)", "O(1)"),
  names=["n", "d", "replicas"])


@B
def embedding_gb(n, d, replicas):
    bytes_each = d * 4
    total = n * bytes_each * replicas
    return round(total / 1e9, 2)


@O
def embedding_gb(n, d, replicas):
    return round(n * d * 4 * replicas / 1e9, 2)


Q(None, "Latency Budget", "Easy", "Where the time goes",
  "Steps run in sequence, except that fetches in one list run in parallel. Given steps as numbers or lists, return the total ms and whether it meets the budget.",
  [(([5, [10, 30, 20], 40, 5], 100), (80, True)), (([50, [60], 10], 100), (120, False))],
  ("A loop with a type check.", "O(n)", "O(1)"),
  ("A generator with <code>max</code>.", "O(n)", "O(1)"),
  names=["steps", "budget"])


@B
def latency_budget(steps, budget):
    total = 0
    for s in steps:
        if isinstance(s, list):
            total += max(s)
        else:
            total += s
    return (total, total <= budget)


@O
def latency_budget(steps, budget):
    total = sum(max(s) if isinstance(s, list) else s for s in steps)
    return (total, total <= budget)


Q(None, "How Many Servers?", "Easy", "Capacity",
  "Each server handles qps_each at target_util utilisation. Return the servers needed for the peak, rounded up, plus spare (N+spare).",
  [((3000, 100, 0.7, 2), 45)],
  ("Usable capacity, then divide.", "O(1)", "O(1)"),
  ("One line.", "O(1)", "O(1)"),
  names=["peak", "qps_each", "target_util", "spare"])


@B
def servers_needed(peak, qps_each, target_util, spare):
    usable = qps_each * target_util
    need = math.ceil(peak / usable)
    return need + spare


@O
def servers_needed(peak, qps_each, target_util, spare):
    return math.ceil(peak / (qps_each * target_util)) + spare


Q(None, "Cache Effect on Traffic", "Easy", "Reducing load",
  "Return the QPS reaching the model after a cache with the given hit rate, and the model's cost per day at cost_per_1k calls (a made-up rate), rounded to 2 decimals.",
  [((1000, 0.8, 0.5), (200.0, 8640.0))],
  ("Misses, then calls per day, then cost.", "O(1)", "O(1)"),
  ("One line each.", "O(1)", "O(1)"),
  names=["qps", "hit_rate", "cost_per_1k"])


@B
def after_cache(qps, hit_rate, cost_per_1k):
    misses = qps * (1 - hit_rate)
    calls = misses * 86400
    return (round(misses, 2), round(calls / 1000 * cost_per_1k, 2))


@O
def after_cache(qps, hit_rate, cost_per_1k):
    m = qps * (1 - hit_rate)
    return (round(m, 2), round(m * 86.4 * cost_per_1k, 2))


Q(None, "Split by Time", "Easy", "Prevent leakage",
  "Rows are (timestamp, label). Train on everything before the cut time, test on the rest. Return (train labels, test labels), keeping time order.",
  [(([(3, "c"), (1, "a"), (4, "d"), (2, "b")], 3),  (['a', 'b'], ['c', 'd']))],
  ("Sort, then two loops.", "O(n log n)", "O(n)"),
  ("Sort, then binary search for the cut.", "O(n log n)", "O(n)"),
  names=["rows", "cut"])


@B
def time_split(rows, cut):
    ordered = sorted(rows)
    train, test = [], []
    for t, y in ordered:
        if t < cut:
            train.append(y)
        else:
            test.append(y)
    return (train, test)


@O
def time_split(rows, cut):
    import bisect
    ordered = sorted(rows)
    i = bisect.bisect_left([t for t, _ in ordered], cut)
    return ([y for _, y in ordered[:i]], [y for _, y in ordered[i:]])


Q(None, "Spot Feature Leakage", "Medium", "Too good to be true",
  "A feature is suspect if |correlation with the label| exceeds the limit, or it's only known after the event. Given features {name: (values, available_before)}, return suspects, sorted.",
  [(({"age": ([20, 30, 40, 50], True), "refund_issued": ([0, 0, 1, 1], True), "chargeback_date": ([0, 1, 1, 0], False)}, [0, 0, 1, 1], 0.95), ['chargeback_date', 'refund_issued'])],
  ("Correlation by hand, in a loop.", "O(f·n)", "O(f)"),
  ("<code>np.corrcoef</code> in a comprehension.", "O(f·n)", "O(f)"),
  names=["features", "label", "limit"])


@B
def leak_suspects(features, label, limit):
    def corr(x, y):
        mx, my = sum(x) / len(x), sum(y) / len(y)
        c = sum((a - mx) * (b - my) for a, b in zip(x, y))
        return c / math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))
    out = []
    for name, (values, before) in features.items():
        if not before or abs(corr(values, label)) > limit:
            out.append(name)
    return sorted(out)


@O
def leak_suspects(features, label, limit):
    return sorted(n for n, (v, before) in features.items()
                  if not before or abs(np.corrcoef(v, label)[0, 1]) > limit)


Q(None, "Target Encoding Without Leakage", "Hard", "Only use the past",
  "Replace each category with the running mean of earlier labels in that category (the global prior if there are none). Return values rounded to 4 decimals.",
  [((["a", "a", "b", "a"], [1, 0, 1, 1], 0.5), [0.5, 1.0, 0.5, 0.5])],
  ("For each row, scan all earlier rows.", "O(n²)", "O(n)"),
  ("Keep a running sum and count per category.", "O(n)", "O(c)"),
  names=["cats", "labels", "prior"])


@B
def target_encode(cats, labels, prior):
    out = []
    for i, c in enumerate(cats):
        past = [labels[j] for j in range(i) if cats[j] == c]
        out.append(round(sum(past) / len(past), 4) if past else prior)
    return out


@O
def target_encode(cats, labels, prior):
    totals, counts, out = {}, {}, []
    for c, y in zip(cats, labels):
        out.append(round(totals[c] / counts[c], 4) if c in counts else prior)
        totals[c] = totals.get(c, 0) + y
        counts[c] = counts.get(c, 0) + 1
    return out


Q(None, "Feature Hashing", "Easy", "Huge vocabularies in fixed space",
  "Map each string to a bucket with (sum of character codes) mod m (a stand-in for a real hash). Return bucket counts.",
  [((["ab", "ba", "c"], 4), [0, 0, 0, 3])],
  ("Loop and add.", "O(total)", "O(m)"),
  ("<code>np.bincount</code>.", "O(total)", "O(m)"),
  names=["items", "m"])


@B
def hash_features(items, m):
    out = [0] * m
    for s in items:
        total = 0
        for ch in s:
            total += ord(ch)
        out[total % m] += 1
    return out


@O
def hash_features(items, m):
    return np.bincount([sum(map(ord, s)) % m for s in items], minlength=m)


Q(None, "Correct for Negative Downsampling", "Medium", "Calibrated probabilities",
  "You trained keeping a fraction w of negatives. Correct a predicted probability p with p / (p + (1 − p)/w). Round to 4 decimals.",
  [((0.5, 0.1), 0.0909), ((0.1, 0.01), 0.0011), ((0.5, 1.0), 0.5)],
  ("Convert to odds, scale, and convert back.", "O(1)", "O(1)"),
  ("The closed formula.", "O(1)", "O(1)"),
  names=["p", "w"])


@B
def recalibrate(p, w):
    odds = p / (1 - p)
    corrected = odds * w
    return round(corrected / (1 + corrected), 4)


@O
def recalibrate(p, w):
    return round(p / (p + (1 - p) / w), 4)


Q(None, "Expected Calibration Error", "Medium", "Do probabilities mean what they say?",
  "Split [0, 1] into b equal bins. ECE = Σ (bin share)·|mean prediction − mean label|. Round to 4 decimals.",
  [(([0.1, 0.2, 0.8, 0.9], [0, 0, 1, 1], 2), 0.15), (([0.9, 0.9, 0.9, 0.9], [1, 0, 0, 0], 2), 0.65)],
  ("Lists per bin.", "O(n + b)", "O(n)"),
  ("Bin ids with array masks.", "O(n·b)", "O(n)"),
  names=["p", "y", "b"])


@B
def ece(p, y, b):
    bins = [[] for _ in range(b)]
    for a, t in zip(p, y):
        bins[min(int(a * b), b - 1)].append((a, t))
    total = 0.0
    for rows in bins:
        if rows:
            gap = abs(sum(r[0] for r in rows) / len(rows) - sum(r[1] for r in rows) / len(rows))
            total += len(rows) / len(p) * gap
    return round(total, 4)


@O
def ece(p, y, b):
    p, y = np.array(p), np.array(y)
    ids = np.minimum((p * b).astype(int), b - 1)
    return round(float(sum((ids == k).mean() * abs(p[ids == k].mean() - y[ids == k].mean()) for k in np.unique(ids))), 4)


Q(None, "Pick a Threshold by Cost", "Medium", "Connect ML to money",
  "Each false positive costs fp and each false negative costs fn. Try each threshold and return the cheapest (first on a tie) and its total cost.",
  [(([0.9, 0.7, 0.4, 0.2], [1, 0, 1, 0], [0.3, 0.5, 0.8], 1, 10), (0.3, 1))],
  ("Loops over thresholds and rows.", "O(t·n)", "O(1)"),
  ("Boolean arrays.", "O(t·n)", "O(n)"),
  names=["p", "y", "thresholds", "fp", "fn"])


@B
def best_threshold(p, y, thresholds, fp, fn):
    best, best_cost = None, float("inf")
    for t in thresholds:
        cost = 0
        for a, label in zip(p, y):
            if a >= t and label == 0:
                cost += fp
            elif a < t and label == 1:
                cost += fn
        if cost < best_cost:
            best, best_cost = t, cost
    return (best, best_cost)


@O
def best_threshold(p, y, thresholds, fp, fn):
    p, y = np.array(p), np.array(y)
    costs = [int(fp * ((p >= t) & (y == 0)).sum() + fn * ((p < t) & (y == 1)).sum()) for t in thresholds]
    i = int(np.argmin(costs))
    return (thresholds[i], costs[i])


Q(None, "Lift at the Top", "Easy", "When you can only review some",
  "Return precision in the top k by score, and lift (that ÷ overall positive rate), rounded to 4 decimals.",
  [(([0.9, 0.8, 0.3, 0.2, 0.1], [1, 1, 0, 0, 0], 2), (1.0, 2.5))],
  ("Sort pairs.", "O(n log n)", "O(n)"),
  ("<code>argsort</code>.", "O(n log n)", "O(n)"),
  names=["scores", "y", "k"])


@B
def lift_at_k(scores, y, k):
    pairs = sorted(zip(scores, y), reverse=True)
    hits = sum(t for _, t in pairs[:k])
    precision = hits / k
    return (round(precision, 4), round(precision / (sum(y) / len(y)), 4))


@O
def lift_at_k(scores, y, k):
    s, y = np.array(scores), np.array(y)
    precision = y[np.argsort(-s)[:k]].mean()
    return (round(float(precision), 4), round(float(precision / y.mean()), 4))


Q(None, "Training vs Serving Skew", "Medium", "The silent bug",
  "Given the same feature computed offline and online for the same rows, return the share that differ by more than tol, rounded to 4 decimals, and whether it's above 1%.",
  [(([1.0, 2.0, 3.0, 4.0], [1.0, 2.5, 3.0, 4.001], 0.01), (0.25, True))],
  ("Count in a loop.", "O(n)", "O(1)"),
  ("<code>np.abs(a − b) &gt; tol</code>.", "O(n)", "O(n)"),
  names=["offline", "online", "tol"])


@B
def skew(offline, online, tol):
    bad = 0
    for a, b in zip(offline, online):
        if abs(a - b) > tol:
            bad += 1
    share = bad / len(offline)
    return (round(share, 4), share > 0.01)


@O
def skew(offline, online, tol):
    share = (np.abs(np.array(offline) - np.array(online)) > tol).mean()
    return (round(float(share), 4), bool(share > 0.01))


Q(None, "Canary Decision", "Medium", "Roll out safely",
  "Metrics are {name: (baseline, canary, higher_is_better, max relative worsening)}. Return ('promote' or 'rollback', metrics that failed, sorted).",
  [(({"ctr": (0.1, 0.104, True, 0.02), "p95_ms": (100, 130, False, 0.1)},), ('rollback', ['p95_ms'])), (({"ctr": (0.1, 0.099, True, 0.02)},), ('promote', []))],
  ("Handle both directions with an if.", "O(k)", "O(k)"),
  ("A sign factor handles both in one formula.", "O(k log k)", "O(k)"))


@B
def canary(metrics):
    failed = []
    for name, (base, new, higher, limit) in metrics.items():
        if higher:
            worse = (base - new) / base
        else:
            worse = (new - base) / base
        if worse > limit:
            failed.append(name)
    failed.sort()
    return ("rollback" if failed else "promote", failed)


@O
def canary(metrics):
    failed = sorted(n for n, (b, c, h, lim) in metrics.items() if (1 if h else -1) * (b - c) / b > lim)
    return ("rollback" if failed else "promote", failed)


Q(None, "When to Retrain", "Easy", "Triggers, not a habit",
  "Retrain if drift (PSI) exceeds 0.25, the live metric fell more than 5% below baseline, or the model is older than max_age days. Return the reasons, in that order.",
  [((0.3, 0.8, 0.9, 10, 30), ['drift', 'quality']), ((0.05, 0.89, 0.9, 40, 30), ['age']), ((0.05, 0.89, 0.9, 10, 30), [])],
  ("Three ifs.", "O(1)", "O(1)"),
  ("A filtered list of pairs.", "O(1)", "O(1)"),
  names=["psi", "metric", "baseline", "age", "max_age"])


@B
def retrain_reasons(psi, metric, baseline, age, max_age):
    out = []
    if psi > 0.25:
        out.append("drift")
    if metric < baseline * 0.95:
        out.append("quality")
    if age > max_age:
        out.append("age")
    return out


@O
def retrain_reasons(psi, metric, baseline, age, max_age):
    checks = [("drift", psi > 0.25), ("quality", metric < baseline * 0.95), ("age", age > max_age)]
    return [name for name, hit in checks if hit]


Q(None, "Recommendation: Two-Stage Funnel", "Medium", "Retrieve, then rank",
  "Candidate scores are cheap; ranking scores are costly. Take the top r by cheap score, re-rank those with rank_scores, and return the top k ids, plus how many costly calls were made.",
  [((["a", "b", "c", "d"], [0.9, 0.8, 0.1, 0.7], {"a": 0.2, "b": 0.9, "d": 0.5}, 3, 2), (['b', 'd'], 3))],
  ("Sort everything by the cheap score, then sort a slice.", "O(n log n)", "O(n)"),
  ("<code>heapq.nlargest</code> for each stage.", "O(n log r)", "O(r)"),
  names=["ids", "cheap", "rank_scores", "r", "k"])


@B
def two_stage(ids, cheap, rank_scores, r, k):
    by_cheap = sorted(zip(cheap, ids), reverse=True)[:r]
    shortlisted = [i for _, i in by_cheap]
    ranked = sorted(shortlisted, key=lambda i: -rank_scores[i])
    return (ranked[:k], len(shortlisted))


@O
def two_stage(ids, cheap, rank_scores, r, k):
    import heapq
    short = [i for _, i in heapq.nlargest(r, zip(cheap, ids))]
    return (heapq.nlargest(k, short, key=rank_scores.get), len(short))


Q(None, "Batch or Real Time?", "Medium", "A cost and freshness call",
  "Return the cheaper option's name and daily cost. Batch costs batch_runs × run_cost. Real-time costs calls × cost_per_call. If freshness is required ('needs_fresh'), it must be real time.",
  [((4, 50, 1000000, 0.001, False), ('batch', 200)), ((4, 50, 100000, 0.001, False), ('real_time', 100.0)), ((4, 50, 1000000, 0.001, True), ('real_time', 1000.0))],
  ("Ifs in order.", "O(1)", "O(1)"),
  ("<code>min</code> over a tuple of options.", "O(1)", "O(1)"),
  names=["batch_runs", "run_cost", "calls", "cost_per_call", "needs_fresh"])


@B
def serving_choice(batch_runs, run_cost, calls, cost_per_call, needs_fresh):
    batch = batch_runs * run_cost
    online = calls * cost_per_call
    if needs_fresh:
        return ("real_time", round(online, 2))
    if batch < online:
        return ("batch", round(batch, 2))
    return ("real_time", round(online, 2))


@O
def serving_choice(batch_runs, run_cost, calls, cost_per_call, needs_fresh):
    online = ("real_time", round(calls * cost_per_call, 2))
    return online if needs_fresh else min(("batch", round(batch_runs * run_cost, 2)), online, key=lambda o: o[1])


Q(None, "RAG Assistant Budget", "Easy", "An LLM system design staple",
  "Given a context window, system prompt tokens, question tokens, reserved answer tokens and chunk size, return how many chunks fit.",
  [((8000, 500, 100, 1000, 400), 16), ((1000, 500, 100, 500, 400), 0)],
  ("Subtract one at a time, then divide.", "O(1)", "O(1)"),
  ("One line, floored at 0.", "O(1)", "O(1)"),
  names=["window", "system", "question", "answer", "chunk"])


@B
def chunks_that_fit(window, system, question, answer, chunk):
    room = window - system
    room = room - question
    room = room - answer
    if room < 0:
        return 0
    return room // chunk


@O
def chunks_that_fit(window, system, question, answer, chunk):
    return max(0, window - system - question - answer) // chunk


Q(None, "Position Bias Correction", "Medium", "Clicks depend on where it was shown",
  "Items at lower positions are seen less. Given (clicks, impressions, chance the position is seen) per item, return corrected click rates: clicks ÷ (impressions × seen), rounded to 4 decimals.",
  [(([(50, 1000, 1.0), (20, 1000, 0.25)],), [0.05, 0.08])],
  ("A loop.", "O(n)", "O(n)"),
  ("Array columns.", "O(n)", "O(n)"))


@B
def debiased_ctr(rows):
    return [round(c / (n * seen), 4) for c, n, seen in rows]


@O
def debiased_ctr(rows):
    r = np.array(rows, float)
    return (r[:, 0] / (r[:, 1] * r[:, 2])).round(4)
