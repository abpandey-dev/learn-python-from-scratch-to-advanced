from lib import *
import hashlib
import io
import json
import math
import pickle
import zlib
import joblib
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


TOPIC(
    id="mlops", title="MLOps: Deploying & Monitoring Models", glyph="⟳",
    blurb="Take a model from notebook to production: experiment tracking and a model registry, data validation gates, saving and serving models, request validation, batch scoring, canary and shadow releases, latency budgets, point-in-time features, drift detection (PSI, KS), monitoring and retraining triggers.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">mlflow.log_params(p); mlflow.log_metric("auc", 0.91); mlflow.sklearn.log_model(m, "model")
joblib.dump(pipeline, "model.joblib"); m = joblib.load("model.joblib")   # ship the whole pipeline

# serve: FastAPI + pydantic
@app.post("/predict")
def predict(req: Request): return {"score": float(m.predict_proba([req.features()])[0, 1])}

pd.merge_asof(labels, features, on="ts", by="user")   # point-in-time correct features
stats.ks_2samp(train_col, live_col)                    # numeric drift
np.percentile(latencies_ms, [50, 95, 99])              # latency budget</code></pre>
<p>Docker packages code + libraries + model into one image so it runs the same everywhere; CI runs tests and builds the image; CD rolls it out (canary → full).</p>
""")

RUNS = [
    {"run": "r1", "model": "logreg", "C": 1.0, "val_auc": 0.861, "train_auc": 0.872},
    {"run": "r2", "model": "gbm", "depth": 3, "val_auc": 0.903, "train_auc": 0.931},
    {"run": "r3", "model": "gbm", "depth": 8, "val_auc": 0.897, "train_auc": 0.998},
    {"run": "r4", "model": "rf", "trees": 300, "val_auc": 0.903, "train_auc": 0.95},
]


Q(None, "Pick the Best Run", "Easy", "Experiment tracking",
  "From tracked runs, return the run id with the highest validation AUC; break ties by the smaller train−validation gap (less overfitting).",
  [((RUNS,), 'r2'), ((RUNS[:1],), 'r1')],
  ("A loop that keeps the best so far.", "O(n)", "O(1)"),
  ("A DataFrame sorted by two keys — what <code>mlflow.search_runs(order_by=...)</code> gives you.", "O(n log n)", "O(n)"),
  viz=(RUNS,))


@B
def best_run(runs):
    best = None
    for r in runs:
        gap = r["train_auc"] - r["val_auc"]
        if best is None or r["val_auc"] > best[1] or (r["val_auc"] == best[1] and gap < best[2]):
            best = (r["run"], r["val_auc"], gap)
    return best[0]


@O
def best_run(runs):
    df = pd.DataFrame(runs)
    df["gap"] = df["train_auc"] - df["val_auc"]
    return df.sort_values(["val_auc", "gap"], ascending=[False, True]).iloc[0]["run"]


Q(None, "Promote a Model Version", "Medium", "Model registry",
  "<code>versions</code> maps version → (stage, metric). Promote <code>candidate</code> to 'Production' only if its metric beats the current Production one by at least <code>margin</code>; the old one moves to 'Archived'. Return the updated stages, sorted by version.",
  [(({1: ("Archived", 0.80), 2: ("Production", 0.85), 3: ("Staging", 0.87)}, 3, 0.01), {1: 'Archived', 2: 'Archived', 3: 'Production'}),
   (({1: ("Production", 0.85), 2: ("Staging", 0.855)}, 2, 0.01), {1: 'Production', 2: 'Staging'})],
  ("Find the production version with a loop, compare, then rebuild the dict.", "O(v)", "O(v)"),
  ("A dict comprehension that rewrites stages in one pass.", "O(v)", "O(v)"),
  viz=({1: ("Archived", 0.80), 2: ("Production", 0.85), 3: ("Staging", 0.87)}, 3, 0.01))


@B
def promote(versions, candidate, margin):
    prod = None
    for v, (stage, metric) in versions.items():
        if stage == "Production":
            prod = v
    stages = {v: s for v, (s, m) in versions.items()}
    if prod is None or versions[candidate][1] >= versions[prod][1] + margin:
        if prod is not None:
            stages[prod] = "Archived"
        stages[candidate] = "Production"
    return dict(sorted(stages.items()))


@O
def promote(versions, candidate, margin):
    prod = next((v for v, (s, _) in versions.items() if s == "Production"), None)
    ok = prod is None or versions[candidate][1] >= versions[prod][1] + margin
    new = {prod: "Archived", candidate: "Production"} if ok else {}
    return {v: new.get(v, s) for v, (s, _) in sorted(versions.items())}


Q(None, "Same Data, Different Order?", "Easy", "Dataset fingerprints",
  "Return True if two datasets (lists of row tuples) contain exactly the same rows, ignoring order — so a retrain can prove it used the same data.",
  [(([(1, "a"), (2, "b"), (2, "b")], [(2, "b"), (1, "a"), (2, "b")]), True), (([(1, "a"), (2, "b")], [(1, "a"), (2, "c")]), False)],
  ("Sort both lists and compare.", "O(n log n)", "O(n)"),
  ("Hash the sorted rows with SHA-256 — a short fingerprint you can store next to the model.", "O(n log n)", "O(n)"),
  viz=([(1, "a"), (2, "b"), (2, "b")], [(2, "b"), (1, "a"), (2, "b")]))


@B
def same_data(a, b):
    return sorted(a) == sorted(b)


@O
def same_data(a, b):
    fp = lambda rows: hashlib.sha256(json.dumps(sorted(rows)).encode()).hexdigest()
    return fp(a) == fp(b)


Q(None, "Data Quality Gate", "Medium", "Validate before you train",
  "Check a batch against <code>rules</code>: required columns, max share of nulls, and min/max value per column. Return a sorted list of failure messages: <code>'missing column: c'</code>, <code>'too many nulls: c'</code>, <code>'out of range: c'</code>.",
  [(({"age": [25, None, 41, 230], "income": [5.0, 7.5, None, None]}, {"age": (0, 120, 0.3), "income": (0, 1000, 0.25), "city": (None, None, 0)}), ['missing column: city', 'out of range: age', 'too many nulls: income'])],
  ("Loop over rules and values.", "O(rows · cols)", "O(1)"),
  ("A DataFrame: <code>isna().mean()</code> and <code>between</code>.", "O(rows · cols)", "O(rows)"),
  viz=({"age": [25, None, 41, 230], "income": [5.0, 7.5, None, None]}, {"age": (0, 120, 0.3), "income": (0, 1000, 0.25), "city": (None, None, 0)}))


@B
def quality_gate(batch, rules):
    fails = []
    for col, (lo, hi, max_null) in rules.items():
        if col not in batch:
            fails.append("missing column: " + col)
            continue
        vals = batch[col]
        nulls = sum(v is None for v in vals)
        if nulls / len(vals) > max_null:
            fails.append("too many nulls: " + col)
        if any(v is not None and not (lo <= v <= hi) for v in vals):
            fails.append("out of range: " + col)
    return sorted(fails)


@O
def quality_gate(batch, rules):
    df = pd.DataFrame(batch)
    fails = [f"missing column: {c}" for c in rules if c not in df]
    for c, (lo, hi, max_null) in rules.items():
        if c in df:
            s = df[c]
            fails += [f"too many nulls: {c}"] * bool(s.isna().mean() > max_null)
            fails += [f"out of range: {c}"] * bool((~s.dropna().between(lo, hi)).any())
    return sorted(fails)


TRAIN = [21, 25, 29, 33, 35, 38, 41, 44, 47, 52, 55, 58, 61, 30, 36, 42]
LIVE = [45, 49, 52, 55, 58, 60, 62, 65, 41, 50, 57, 63, 66, 70, 39, 48]


Q(None, "Population Stability Index", "Medium", "Has the input shifted?",
  "Bin both samples using edges <code>bins</code> and return PSI = Σ (live% − train%) × ln(live% / train%), using 0.0001 in place of empty shares. Round to 4. Rule of thumb: &lt; 0.1 stable, &gt; 0.25 big shift.",
  [((TRAIN, LIVE, [0, 30, 40, 50, 60, 100]), 2.4385), ((TRAIN, TRAIN, [0, 30, 40, 50, 60, 100]), 0.0)],
  ("Count each sample into bins by hand, then sum.", "O(nb)", "O(b)"),
  ("<code>np.histogram</code> for both, then a vectorised sum.", "O(n log b)", "O(b)"),
  viz=(TRAIN, LIVE, [0, 30, 40, 50, 60, 100]))


@B
def psi(train, live, bins):
    def shares(xs):
        counts = [0] * (len(bins) - 1)
        for x in xs:
            for i in range(len(bins) - 1):
                last = i == len(bins) - 2
                if bins[i] <= x < bins[i + 1] or (last and x == bins[-1]):
                    counts[i] += 1
                    break
        return [max(c / len(xs), 0.0001) for c in counts]
    t, l = shares(train), shares(live)
    return round(sum((b - a) * math.log(b / a) for a, b in zip(t, l)), 4)


@O
def psi(train, live, bins):
    t = np.maximum(np.histogram(train, bins)[0] / len(train), 0.0001)
    l = np.maximum(np.histogram(live, bins)[0] / len(live), 0.0001)
    return round(float(((l - t) * np.log(l / t)).sum()), 4)


Q(None, "Kolmogorov–Smirnov Drift Statistic", "Medium", "Compare two distributions",
  "Return the KS statistic: the largest gap between the two samples' cumulative distribution curves, rounded to 4.",
  [((TRAIN, LIVE), 0.5625), ((TRAIN, TRAIN[::-1]), 0.0)],
  ("Evaluate both ECDFs at every observed value and take the biggest difference.", "O(n²)", "O(n)"),
  ("<code>stats.ks_2samp(a, b).statistic</code> (its p-value says whether the gap is significant).", "O(n log n)", "O(n)"),
  viz=(TRAIN, LIVE))


@B
def ks_stat(a, b):
    best = 0
    for x in sorted(set(a) | set(b)):
        fa = sum(v <= x for v in a) / len(a)
        fb = sum(v <= x for v in b) / len(b)
        best = max(best, abs(fa - fb))
    return round(best, 4)


@O
def ks_stat(a, b):
    return round(float(stats.ks_2samp(a, b).statistic), 4)


Q(None, "Training–Serving Skew", "Easy", "Same features online and offline?",
  "Compare features computed offline (training pipeline) and online (serving code) for the same request. Return the sorted names that differ by more than <code>tol</code>, or exist on one side only.",
  [(({"age": 34, "spend_7d": 120.0, "ratio": 0.51}, {"age": 34, "spend_7d": 118.0, "ratio": 0.5100001, "extra": 1}, 1e-3), ['extra', 'spend_7d'])],
  ("Loop over the union of keys.", "O(k)", "O(k)"),
  ("Align two Series and use <code>np.isclose</code>.", "O(k)", "O(k)"),
  viz=({"age": 34, "spend_7d": 120.0, "ratio": 0.51}, {"age": 34, "spend_7d": 118.0, "ratio": 0.5100001, "extra": 1}, 1e-3))


@B
def skew(offline, online, tol):
    bad = []
    for k in set(offline) | set(online):
        if k not in offline or k not in online or abs(offline[k] - online[k]) > tol:
            bad.append(k)
    return sorted(bad)


@O
def skew(offline, online, tol):
    a, b = pd.Series(offline, dtype=float).align(pd.Series(online, dtype=float))
    ok = np.isclose(a, b, rtol=0, atol=tol)
    return sorted(a.index[~ok])


XS = [[0.1, 1.0], [0.4, 0.8], [0.35, 0.2], [0.8, 0.1], [0.9, 0.7], [0.2, 0.3], [0.7, 0.9], [0.6, 0.4]]
YS = [0, 0, 0, 1, 1, 0, 1, 1]


Q(None, "Save and Reload a Model", "Easy", "Serialisation",
  "Train <code>LogisticRegression()</code>, save it to bytes and load it back. Return the reloaded model's predictions for <code>X_new</code>.",
  [((XS, YS, [[0.15, 0.5], [0.85, 0.5]]), [0, 1])],
  ("<code>pickle.dumps</code> / <code>pickle.loads</code>.", "O(model)", "O(model)"),
  ("<code>joblib.dump</code> / <code>joblib.load</code>, which handles big NumPy arrays efficiently — the usual choice for sklearn.", "O(model)", "O(model)"),
  viz=(XS, YS, [[0.15, 0.5], [0.85, 0.5]]))


@B
def reload_predict(X, y, X_new):
    model = LogisticRegression().fit(X, y)
    blob = pickle.dumps(model)
    again = pickle.loads(blob)
    return again.predict(X_new).tolist()


@O
def reload_predict(X, y, X_new):
    buf = io.BytesIO()
    joblib.dump(LogisticRegression().fit(X, y), buf)
    buf.seek(0)
    return joblib.load(buf).predict(X_new).tolist()


Q(None, "Batch Scoring in Chunks", "Easy", "Memory-safe inference",
  "Score <code>X_new</code> in chunks of <code>size</code> rows with a model trained on X, y. Return <code>(number of chunks, number predicted positive)</code>.",
  [((XS, YS, XS * 3, 5), (5, 12))],
  ("Slice with a range step and loop.", "O(n)", "O(size)"),
  ("<code>np.array_split</code> into ⌈n/size⌉ parts and a generator.", "O(n)", "O(size)"),
  viz=(XS, YS, XS * 3, 5))


@B
def chunked(X, y, X_new, size):
    model = LogisticRegression().fit(X, y)
    chunks = positives = 0
    for start in range(0, len(X_new), size):
        part = X_new[start:start + size]
        positives += int(sum(model.predict(part)))
        chunks += 1
    return (chunks, positives)


@O
def chunked(X, y, X_new, size):
    model = LogisticRegression().fit(X, y)
    parts = np.array_split(np.array(X_new), math.ceil(len(X_new) / size))
    return (len(parts), int(sum(model.predict(p).sum() for p in parts)))


SCHEMA = {"age": (int, 18, 100), "income": (float, 0.0, 1e7), "city": (str, None, None)}


Q(None, "Validate an Inference Request", "Medium", "API input checks",
  "Validate a JSON request against <code>SCHEMA</code> (type, min, max). Ints are accepted where floats are expected. Return <code>(ok, sorted errors)</code> with errors like <code>'age: missing'</code>, <code>'age: wrong type'</code>, <code>'age: out of range'</code>.",
  [(({"age": 17, "income": 50000, "city": "Pune"},), (False, ['age: out of range'])), (({"age": "34", "city": "Pune"},), (False, ['age: wrong type', 'income: missing'])), (({"age": 30, "income": 1.5, "city": "Goa"},), (True, []))],
  ("An if-chain per field.", "O(f)", "O(f)"),
  ("A table-driven loop, like what pydantic generates from a model class.", "O(f)", "O(f)"),
  viz=({"age": 17, "income": 50000, "city": "Pune"},))


@B
def validate_request(req):
    errors = []
    for field in SCHEMA:
        kind, lo, hi = SCHEMA[field]
        if field not in req:
            errors.append(field + ": missing")
            continue
        v = req[field]
        good_type = (isinstance(v, kind) or (kind is float and isinstance(v, int))) and not isinstance(v, bool)
        if not good_type:
            errors.append(field + ": wrong type")
        elif lo is not None and not (lo <= v <= hi):
            errors.append(field + ": out of range")
    return (len(errors) == 0, sorted(errors))


@O
def validate_request(req):
    def check(field, kind, lo, hi):
        if field not in req:
            return "missing"
        v = req[field]
        if not isinstance(v, (kind, int) if kind is float else kind) or isinstance(v, bool):
            return "wrong type"
        if lo is not None and not lo <= v <= hi:
            return "out of range"
    errors = sorted(f"{f}: {e}" for f, spec in SCHEMA.items() if (e := check(f, *spec)))
    return (not errors, errors)


LAT = [42, 38, 51, 47, 39, 44, 120, 41, 43, 40, 45, 300, 46, 37, 48, 50, 44, 42, 39, 41]


Q(None, "Latency Percentiles", "Easy", "p50, p95, p99",
  "Return <code>(p50, p95, p99)</code> of request latencies in ms with linear interpolation, rounded to 2. Averages hide the slow tail; percentiles don't.",
  [((LAT,), (43.5, 129.0, 265.8))],
  ("Sort and interpolate at position (n − 1) × q.", "O(n log n)", "O(n)"),
  ("<code>np.percentile(lat, [50, 95, 99])</code>.", "O(n log n)", "O(n)"),
  viz=(LAT,))


@B
def latency(lat):
    s = sorted(lat)
    def q(p):
        pos = (len(s) - 1) * p
        lo = int(pos)
        return s[lo] + (s[min(lo + 1, len(s) - 1)] - s[lo]) * (pos - lo)
    return (round(q(0.5), 2), round(q(0.95), 2), round(q(0.99), 2))


@O
def latency(lat):
    return tuple(round(float(v), 2) for v in np.percentile(lat, [50, 95, 99]))


Q(None, "Canary Routing by Hash", "Hard", "Sticky gradual rollout",
  "Send a user to the new model if CRC-32(user id) % 100 &lt; <code>pct</code>, so each user always sees the same version. Return the users routed to the canary.",
  [((["u1", "u2", "u3", "u4", "u5", "u6", "u7", "u8"], 30), ['u1', 'u3']), ((["alice", "bob"], 0), [])],
  ("Implement CRC-32 bit by bit (polynomial 0xEDB88320).", "O(chars · 8)", "O(1)"),
  ("<code>zlib.crc32</code>.", "O(chars)", "O(1)"),
  viz=(["u1", "u2", "u3", "u4"], 30))


@B
def canary(users, pct):
    def crc32(data):
        crc = 0xFFFFFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                crc = (crc >> 1) ^ 0xEDB88320 if crc & 1 else crc >> 1
        return crc ^ 0xFFFFFFFF
    return [u for u in users if crc32(u.encode()) % 100 < pct]


@O
def canary(users, pct):
    return [u for u in users if zlib.crc32(u.encode()) % 100 < pct]


Q(None, "Shadow Mode Comparison", "Easy", "Test on live traffic safely",
  "The new model runs in shadow (its answers are logged, not used). Return <code>(agreement %, indexes where they disagree)</code>, agreement rounded to 1.",
  [(([1, 0, 0, 1, 1, 0, 1, 0], [1, 0, 1, 1, 0, 0, 1, 0]), (75.0, [2, 4]))],
  ("Loop with a counter.", "O(n)", "O(n)"),
  ("Compare NumPy arrays; <code>np.flatnonzero</code> finds disagreements.", "O(n)", "O(n)"),
  viz=([1, 0, 0, 1, 1, 0, 1, 0], [1, 0, 1, 1, 0, 0, 1, 0]))


@B
def shadow(live, shadow_preds):
    diff = []
    for i, (a, b) in enumerate(zip(live, shadow_preds)):
        if a != b:
            diff.append(i)
    return (round((len(live) - len(diff)) / len(live) * 100, 1), diff)


@O
def shadow(live, shadow_preds):
    eq = np.array(live) == np.array(shadow_preds)
    return (round(float(eq.mean() * 100), 1), np.flatnonzero(~eq).tolist())


Q(None, "Should We Retrain?", "Easy", "Retraining triggers",
  "Retrain if PSI &gt; 0.2 ('drift'), live accuracy fell more than 0.05 below the accuracy at deployment ('accuracy'), or the model is older than 30 days ('age'). Return the list of reasons in that order.",
  [((0.31, 0.88, 0.91, 12), ['drift']), ((0.05, 0.80, 0.90, 45), ['accuracy', 'age']), ((0.1, 0.9, 0.91, 3), [])],
  ("Three ifs.", "O(1)", "O(1)"),
  ("A list of (reason, condition) pairs filtered by a comprehension — easy to extend.", "O(1)", "O(1)"),
  viz=(0.31, 0.88, 0.91, 12))


@B
def retrain_reasons(psi_value, live_acc, deploy_acc, age_days):
    reasons = []
    if psi_value > 0.2:
        reasons.append("drift")
    if deploy_acc - live_acc > 0.05:
        reasons.append("accuracy")
    if age_days > 30:
        reasons.append("age")
    return reasons


@O
def retrain_reasons(psi_value, live_acc, deploy_acc, age_days):
    rules = [("drift", psi_value > 0.2), ("accuracy", deploy_acc - live_acc > 0.05), ("age", age_days > 30)]
    return [name for name, hit in rules if hit]


Q(None, "Rolling Accuracy Alerts", "Medium", "Monitoring with delayed labels",
  "Labels arrive as 1 (prediction was right) or 0. Return the indexes where accuracy over the last <code>w</code> labels drops below <code>floor</code>.",
  [(([1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1], 4, 0.5), [9, 10])],
  ("Recompute each window's mean in a loop.", "O(nw)", "O(1)"),
  ("<code>rolling(w).mean()</code>.", "O(n)", "O(n)"),
  viz=([1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1], 4, 0.5))


@B
def accuracy_alerts(correct, w, floor):
    alerts = []
    for i in range(w - 1, len(correct)):
        if sum(correct[i - w + 1:i + 1]) / w < floor:
            alerts.append(i)
    return alerts


@O
def accuracy_alerts(correct, w, floor):
    r = pd.Series(correct).rolling(w).mean()
    return r.index[r < floor].tolist()


LABELS = [("u1", 5, 1), ("u1", 12, 0), ("u2", 7, 1), ("u2", 2, 0)]
FEATS = [("u1", 1, 10.0), ("u1", 6, 14.0), ("u1", 11, 20.0), ("u2", 3, 3.0), ("u2", 8, 9.0)]


Q(None, "Point-in-Time Feature Join", "Hard", "No peeking at the future",
  "For each label (user, time, y), attach the user's most recent feature value at or before that time (None if none). Return <code>(user, time, feature, y)</code> rows sorted by user then time.",
  [((LABELS, FEATS), [('u1', 5, 10.0, 1), ('u1', 12, 20.0, 0), ('u2', 2, None, 0), ('u2', 7, 3.0, 1)])],
  ("For each label, scan that user's feature rows for the latest time ≤ label time.", "O(n · m)", "O(1)"),
  ("<code>pd.merge_asof(by='user')</code> — exactly what feature stores do to build training sets.", "O((n + m) log(n + m))", "O(n + m)"),
  viz=(LABELS, FEATS))


@B
def point_in_time(labels, feats):
    out = []
    for user, t, y in sorted(labels):
        best = None
        for fu, ft, value in feats:
            if fu == user and ft <= t and (best is None or ft > best[0]):
                best = (ft, value)
        out.append((user, t, best[1] if best else None, y))
    return out


@O
def point_in_time(labels, feats):
    L = pd.DataFrame(labels, columns=["user", "t", "y"]).sort_values("t")
    F = pd.DataFrame(feats, columns=["user", "t", "feature"]).sort_values("t")
    m = pd.merge_asof(L, F, on="t", by="user").sort_values(["user", "t"])
    return [(u, t, None if pd.isna(f) else f, y) for u, t, y, f in m[["user", "t", "y", "feature"]].itertuples(index=False)]


Q(None, "Bump the Model Version", "Easy", "Semantic versioning",
  "Version 'MAJOR.MINOR.PATCH'. A new input schema bumps MAJOR, retraining on new data bumps MINOR, a bug fix bumps PATCH; lower parts reset to 0.",
  [(("2.3.7", "schema"), '3.0.0'), (("2.3.7", "retrain"), '2.4.0'), (("2.3.7", "fix"), '2.3.8')],
  ("Split, then an if-chain.", "O(1)", "O(1)"),
  ("Index of the part to bump from a dict; zero everything after it.", "O(1)", "O(1)"),
  viz=("2.3.7", "retrain"))


@B
def bump(version, change):
    major, minor, patch = (int(p) for p in version.split("."))
    if change == "schema":
        major, minor, patch = major + 1, 0, 0
    elif change == "retrain":
        minor, patch = minor + 1, 0
    else:
        patch += 1
    return f"{major}.{minor}.{patch}"


@O
def bump(version, change):
    parts = list(map(int, version.split(".")))
    i = {"schema": 0, "retrain": 1, "fix": 2}[change]
    parts = parts[:i] + [parts[i] + 1] + [0] * (2 - i)
    return ".".join(map(str, parts))


Q(None, "Pre-Deployment Checks", "Medium", "CI for models",
  "Return the names of failed checks, in order: 'auc' (AUC below <code>min_auc</code>), 'latency' (p95 above <code>max_p95</code>), 'invariance' (changing an irrelevant field such as the user's name changed any prediction).",
  [((0.86, 0.85, 80, 100, [0.2, 0.7], [0.2, 0.7]), []), ((0.82, 0.85, 140, 100, [0.2, 0.7], [0.2, 0.71]), ['auc', 'latency', 'invariance'])],
  ("Three ifs appending names.", "O(n)", "O(1)"),
  ("Checks as data, evaluated in a comprehension; <code>np.allclose</code> for invariance.", "O(n)", "O(1)"),
  viz=(0.82, 0.85, 140, 100, [0.2, 0.7], [0.2, 0.71]))


@B
def predeploy(auc, min_auc, p95, max_p95, preds, preds_renamed):
    failed = []
    if auc < min_auc:
        failed.append("auc")
    if p95 > max_p95:
        failed.append("latency")
    for a, b in zip(preds, preds_renamed):
        if abs(a - b) > 1e-9:
            failed.append("invariance")
            break
    return failed


@O
def predeploy(auc, min_auc, p95, max_p95, preds, preds_renamed):
    checks = {"auc": auc >= min_auc, "latency": p95 <= max_p95,
              "invariance": np.allclose(preds, preds_renamed, rtol=0, atol=1e-9)}
    return [name for name, ok in checks.items() if not ok]


Q(None, "How Many Replicas?", "Medium", "Capacity planning",
  "Peak traffic is <code>rps</code> requests/second, each takes <code>ms</code> milliseconds, each replica handles <code>workers</code> requests at once, and you target <code>util</code> utilisation. By Little's law, in-flight requests = rps × seconds. Return the replicas needed (round up).",
  [((400, 50, 4, 0.7), 8), ((1000, 120, 8, 0.6), 25)],
  ("Compute in-flight requests, then capacity per replica, step by step.", "O(1)", "O(1)"),
  ("One expression with <code>math.ceil</code>.", "O(1)", "O(1)"),
  viz=(400, 50, 4, 0.7))


@B
def replicas(rps, ms, workers, util):
    in_flight = rps * ms / 1000
    usable_per_replica = workers * util
    n = 0
    while n * usable_per_replica < in_flight:
        n += 1
    return n


@O
def replicas(rps, ms, workers, util):
    return math.ceil(round(rps * ms / 1000 / (workers * util), 9))


Q(None, "Scale Serving Data With Training Statistics", "Easy", "Fit once, reuse",
  "Standardise <code>serve</code> rows using the mean and (population) std learned from <code>train</code> — never statistics of the serving data. Round to 4.",
  [(([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]], [[2.0, 40.0]]), [[0.0, 2.4495]])],
  ("Compute each column's mean and std from train in loops.", "O(nd)", "O(d)"),
  ("A fitted <code>StandardScaler</code> saved inside the model pipeline.", "O(nd)", "O(d)"),
  viz=([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]], [[2.0, 40.0]]))


@B
def scale_serving(train, serve):
    d = len(train[0])
    means = [sum(r[j] for r in train) / len(train) for j in range(d)]
    stds = [math.sqrt(sum((r[j] - means[j]) ** 2 for r in train) / len(train)) for j in range(d)]
    return [[round((r[j] - means[j]) / stds[j], 4) for j in range(d)] for r in serve]


@O
def scale_serving(train, serve):
    return np.round(StandardScaler().fit(train).transform(serve), 4).tolist()
