from lib import *
import itertools
import json
import logging
import re
import zlib
from collections import Counter, defaultdict

TOPIC(
    id="logging", title="Logging, Metrics & Errors in Production", glyph="📈",
    blurb="Make code you can run and debug in production: log levels, formats and JSON logs, logger hierarchies, rotation, error rates, request tracing, redaction, retries, exception chaining, Prometheus counters and histograms, quantiles and rates, health checks, feature flags, log sampling, alert cooldowns, error grouping, config validation and uptime.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">import logging
log = logging.getLogger(__name__)            # one logger per module
logging.basicConfig(level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s")

log.info("order placed", extra={"order_id": 42})
try:
    charge(card)
except PaymentError:
    log.exception("charge failed")           # logs the traceback too
    raise</code></pre>
<p>Levels: DEBUG &lt; INFO &lt; WARNING &lt; ERROR &lt; CRITICAL. Production usually logs INFO and above.</p>
""")

LEVELS = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "CRITICAL": 50}


class ListHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.lines = []

    def emit(self, record):
        self.lines.append(self.format(record))


_counter = itertools.count()


def fresh_logger(name, level):
    log = logging.getLogger(f"q{next(_counter)}.{name}")
    log.handlers, log.propagate = [], False
    log.setLevel(level)
    return log


Q(None, "Which Messages Get Logged?", "Easy", "Log levels",
  "A logger set to <code>level</code> emits records at that level or above. Return the emitted messages as <code>'LEVEL message'</code>. The brute force compares numbers by hand; the optimal sends the records through a real <code>logging</code> logger with a handler that collects lines.",
  [(("WARNING", [("DEBUG", "cache miss key=user:7"), ("INFO", "order 42 placed"), ("WARNING", "retrying payment"), ("ERROR", "payment failed"), ("CRITICAL", "db down")]), ['WARNING retrying payment', 'ERROR payment failed', 'CRITICAL db down']),
   (("DEBUG", [("DEBUG", "x"), ("INFO", "y")]), ['DEBUG x', 'INFO y'])],
  ("Compare level numbers in a loop.", "O(n)", "O(n)"),
  ("A real logger and handler.", "O(n)", "O(n)"),
  viz=(("INFO", [("DEBUG", "a"), ("INFO", "b")])))


@B
def emitted(level, records):
    out = []
    for lvl, msg in records:
        if LEVELS[lvl] >= LEVELS[level]:
            out.append(lvl + " " + msg)
    return out


@O
def emitted(level, records):
    log, h = fresh_logger("app", level), ListHandler()
    h.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    log.addHandler(h)
    for lvl, msg in records:
        log.log(LEVELS[lvl], msg)
    return h.lines


Q(None, "Format Log Lines", "Easy", "%(levelname)-8s and friends",
  "Format each record <code>(level, logger name, line number, message)</code> with the pattern <code>'%(levelname)-8s %(name)s:%(lineno)d %(message)s'</code> (level left-aligned and padded to 8 characters).",
  [(([("INFO", "app.api", 41, "GET /orders 200 12ms"), ("ERROR", "app.db", 108, "connection refused"), ("WARNING", "app", 7, "config file missing, using defaults")],), ['INFO     app.api:41 GET /orders 200 12ms', 'ERROR    app.db:108 connection refused', 'WARNING  app:7 config file missing, using defaults'])],
  ("An f-string with ljust.", "O(n)", "O(n)"),
  ("<code>logging.Formatter</code> on real LogRecords.", "O(n)", "O(n)"),
  viz=(([("INFO", "a", 1, "hi")],)))


@B
def format_logs(records):
    out = []
    for lvl, name, line, msg in records:
        out.append(lvl.ljust(8) + " " + name + ":" + str(line) + " " + msg)
    return out


@O
def format_logs(records):
    f = logging.Formatter("%(levelname)-8s %(name)s:%(lineno)d %(message)s")
    return [f.format(logging.LogRecord(name, LEVELS[lvl], "app.py", line, msg, None, None)) for lvl, name, line, msg in records]


SECRET_KEYS = ("password", "token", "secret", "authorization")


Q(None, "Structured JSON Logs", "Medium", "Logs machines can query",
  "Turn each record (a dict with <code>level</code>, <code>msg</code> and any extra fields) into one JSON line with keys sorted, replacing the value of any key whose name contains a word from <code>SECRET_KEYS</code> (case-insensitive) with <code>'[REDACTED]'</code>. JSON logs let tools like Datadog, Loki or CloudWatch filter by field.",
  [(([{"level": "INFO", "msg": "login ok", "user_id": 7, "ip": "10.0.0.5"}, {"level": "ERROR", "msg": "auth failed", "user": "asha", "Password": "hunter2"}, {"level": "INFO", "msg": "call api", "api_token": "sk-123", "latency_ms": 84}],), ['{"ip": "10.0.0.5", "level": "INFO", "msg": "login ok", "user_id": 7}', '{"Password": "[REDACTED]", "level": "ERROR", "msg": "auth failed", "user": "asha"}', '{"api_token": "[REDACTED]", "latency_ms": 84, "level": "INFO", "msg": "call api"}'])],
  ("Build a cleaned dict with a loop, then json.dumps.", "O(n · k)", "O(k)"),
  ("A dict comprehension inside json.dumps.", "O(n · k)", "O(k)"),
  viz=(([{"level": "INFO", "msg": "x", "token": "t"}],)))


@B
def json_logs(records):
    out = []
    for r in records:
        clean = {}
        for k, v in r.items():
            hidden = False
            for word in SECRET_KEYS:
                if word in k.lower():
                    hidden = True
            clean[k] = "[REDACTED]" if hidden else v
        out.append(json.dumps(clean, sort_keys=True))
    return out


@O
def json_logs(records):
    secret = lambda k: any(w in k.lower() for w in SECRET_KEYS)
    return [json.dumps({k: "[REDACTED]" if secret(k) else v for k, v in r.items()}, sort_keys=True) for r in records]


Q(None, "The Logger Hierarchy", "Medium", "Effective levels",
  "Loggers form a tree by dotted name (<code>app.db</code> is a child of <code>app</code>). A logger without its own level uses the nearest ancestor's, and the root logger defaults to <code>WARNING</code>. Given the levels set explicitly, return the effective level of each logger asked about.",
  [(({"app": "INFO", "app.db": "DEBUG", "app.api.auth": "ERROR"}, ["app", "app.db.pool", "app.api", "app.api.auth.jwt", "urllib3.connectionpool", "app.db"]), {'app': 'INFO', 'app.db.pool': 'DEBUG', 'app.api': 'INFO', 'app.api.auth.jwt': 'ERROR', 'urllib3.connectionpool': 'WARNING', 'app.db': 'DEBUG'})],
  ("Strip name parts until one is configured.", "O(q · d)", "O(1)"),
  ("Generate every prefix and take the longest configured one.", "O(q · d)", "O(d)"),
  viz=(({"a": "INFO"}, ["a.b", "c"])))


@B
def effective_levels(configured, names):
    out = {}
    for name in names:
        n = name
        while n and n not in configured:
            n = n.rpartition(".")[0]
        out[name] = configured.get(n, "WARNING") if n else "WARNING"
    return out


@O
def effective_levels(configured, names):
    def level(name):
        parts = name.split(".")
        prefixes = [".".join(parts[:i]) for i in range(len(parts), 0, -1)]
        return next((configured[p] for p in prefixes if p in configured), "WARNING")
    return {n: level(n) for n in names}


Q(None, "Rotate Log Files by Size", "Medium", "RotatingFileHandler",
  "Lines of the given byte sizes are written to <code>app.log</code>. If writing a line would push the file past <code>max_bytes</code> (and the file isn't empty), the files rotate first: <code>app.log.N-1 → app.log.N</code> … <code>app.log → app.log.1</code>, keeping at most <code>backups</code> old files (the oldest is deleted). Return the final size of each file, newest first.",
  [(([300, 400, 350, 500, 200, 600, 100, 450], 1000, 2), {'app.log': 450, 'app.log.1': 900, 'app.log.2': 850})],
  ("Keep a list of file sizes and shift it.", "O(n · b)", "O(b)"),
  ("A deque with a max length.", "O(n)", "O(b)"),
  viz=(([6, 6, 6], 10, 1)))


@B
def rotate(lines, max_bytes, backups):
    files = [0]
    for size in lines:
        if files[0] > 0 and files[0] + size > max_bytes:
            files = [0] + files
            if len(files) > backups + 1:
                files = files[:backups + 1]
        files[0] += size
    names = ["app.log"] + [f"app.log.{i}" for i in range(1, len(files))]
    return dict(zip(names, files))


@O
def rotate(lines, max_bytes, backups):
    from collections import deque
    files = deque([0], maxlen=backups + 1)
    for size in lines:
        if files[0] and files[0] + size > max_bytes:
            files.appendleft(0)
        files[0] += size
    return {("app.log" if i == 0 else f"app.log.{i}"): s for i, s in enumerate(files)}


Q(None, "Error Rate per Minute", "Easy", "From logs to a metric",
  "Records are JSON strings with <code>ts</code> (seconds) and <code>level</code>. Return <code>{minute: error %}</code> (ERROR and CRITICAL count as errors), rounded to 1, for each minute (<code>ts // 60</code>) that has records.",
  [((['{"ts": 5, "level": "INFO"}', '{"ts": 30, "level": "ERROR"}', '{"ts": 59, "level": "INFO"}', '{"ts": 61, "level": "INFO"}', '{"ts": 75, "level": "INFO"}', '{"ts": 130, "level": "CRITICAL"}', '{"ts": 140, "level": "ERROR"}', '{"ts": 150, "level": "WARNING"}'],), {0: 33.3, 1: 0.0, 2: 66.7})],
  ("Two dicts of counts.", "O(n)", "O(m)"),
  ("A dict of [errors, total] pairs.", "O(n)", "O(m)"),
  viz=((['{"ts": 1, "level": "ERROR"}'],)))


@B
def error_rate(lines):
    total, errors = {}, {}
    for line in lines:
        r = json.loads(line)
        m = r["ts"] // 60
        total[m] = total.get(m, 0) + 1
        if r["level"] in ("ERROR", "CRITICAL"):
            errors[m] = errors.get(m, 0) + 1
    return {m: round(errors.get(m, 0) / total[m] * 100, 1) for m in sorted(total)}


@O
def error_rate(lines):
    c = defaultdict(lambda: [0, 0])
    for r in map(json.loads, lines):
        c[r["ts"] // 60][0] += r["level"] in ("ERROR", "CRITICAL")
        c[r["ts"] // 60][1] += 1
    return {m: round(100 * e / t, 1) for m, (e, t) in sorted(c.items())}


Q(None, "Follow a Request Across Services", "Medium", "Correlation ids",
  "Each service logs <code>(ms, request_id, service, message)</code>. Return, per request id (sorted), the services in time order (consecutive duplicates collapsed) and the total duration in ms (last minus first timestamp). Passing one id through every hop is what makes this possible.",
  [(([(100, "r-7", "gateway", "GET /checkout"), (103, "r-9", "gateway", "GET /health"), (105, "r-7", "orders", "load cart"), (104, "r-9", "gateway", "200"), (140, "r-7", "payments", "charge 499"), (190, "r-7", "orders", "order created"), (196, "r-7", "gateway", "201")],), {'r-7': (['gateway', 'orders', 'payments', 'orders', 'gateway'], 96), 'r-9': (['gateway'], 1)})],
  ("Group with a dict of lists, sort each.", "O(n log n)", "O(n)"),
  ("groupby on records sorted by (id, time).", "O(n log n)", "O(n)"),
  viz=(([(1, "a", "x", "m"), (5, "a", "y", "m")],)))


@B
def trace_requests(records):
    by_id = {}
    for ms, rid, svc, _ in records:
        by_id.setdefault(rid, []).append((ms, svc))
    out = {}
    for rid in sorted(by_id):
        events = sorted(by_id[rid])
        path = []
        for _, svc in events:
            if not path or path[-1] != svc:
                path.append(svc)
        out[rid] = (path, events[-1][0] - events[0][0])
    return out


@O
def trace_requests(records):
    out = {}
    for rid, grp in itertools.groupby(sorted(records, key=lambda r: (r[1], r[0])), key=lambda r: r[1]):
        g = list(grp)
        out[rid] = ([s for s, _ in itertools.groupby(r[2] for r in g)], g[-1][0] - g[0][0])
    return out


REDACT = [(re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[EMAIL]"),
          (re.compile(r"\b(?:\d[ -]?){12}(\d{4})\b"), r"****\1"),
          (re.compile(r"(?i)bearer\s+[\w.-]+"), "Bearer [TOKEN]")]


Q(None, "Redact Personal Data From Logs", "Medium", "Privacy by default",
  "Apply the substitutions in <code>REDACT</code> in order to each message: emails → <code>[EMAIL]</code>, 16-digit card numbers (spaces or dashes allowed) → <code>****</code> plus the last 4 digits, bearer tokens → <code>Bearer [TOKEN]</code>. Return the messages and the number of messages changed.",
  [((["payment ok for asha.k@example.com card 4111 1111 1111 1234", "Authorization: Bearer eyJhbGciOi.payload.sig", "order 42 shipped", "refund to 5500-0000-0000-0004 requested by ravi@shop.in"],), (['payment ok for [EMAIL] card ****1234', 'Authorization: Bearer [TOKEN]', 'order 42 shipped', 'refund to ****0004 requested by [EMAIL]'], 3))],
  ("Loop over messages and patterns.", "O(n · p · L)", "O(L)"),
  ("functools.reduce over the patterns.", "O(n · p · L)", "O(L)"),
  viz=((["mail a@b.co"],)))


@B
def redact(messages):
    out, changed = [], 0
    for m in messages:
        new = m
        for rx, repl in REDACT:
            new = rx.sub(repl, new)
        out.append(new)
        if new != m:
            changed += 1
    return (out, changed)


@O
def redact(messages):
    from functools import reduce
    out = [reduce(lambda s, p: p[0].sub(p[1], s), REDACT, m) for m in messages]
    return (out, sum(a != b for a, b in zip(out, messages)))


Q(None, "Retry With Backoff", "Medium", "Transient failures",
  "A call fails for its first <code>failures</code> attempts, then succeeds. Retry up to <code>max_attempts</code> attempts in total, sleeping <code>base × 2^(attempt−1)</code> seconds after each failed attempt (no sleep after the last). Only exceptions in <code>retry_on</code> are retried; <code>error</code> is the exception the call raises. Return <code>(outcome, attempts, seconds slept)</code> — outcome is <code>'ok'</code> or the error name.",
  [((2, "TimeoutError", ["TimeoutError", "ConnectionError"], 5, 0.5), ('ok', 3, 1.5)), ((9, "TimeoutError", ["TimeoutError"], 4, 1.0), ('TimeoutError', 4, 7.0)), ((1, "ValueError", ["TimeoutError"], 4, 1.0), ('ValueError', 1, 0.0))],
  ("Simulate attempt by attempt.", "O(a)", "O(1)"),
  ("A decorator-style wrapper around a fake call.", "O(a)", "O(1)"),
  viz=((1, "TimeoutError", ["TimeoutError"], 3, 1.0)))


@B
def retry_sim(failures, error, retry_on, max_attempts, base):
    attempts, slept = 0, 0.0
    while True:
        attempts += 1
        if attempts > failures:
            return ("ok", attempts, slept)
        if error not in retry_on or attempts == max_attempts:
            return (error, attempts, slept)
        slept += base * 2 ** (attempts - 1)


@O
def retry_sim(failures, error, retry_on, max_attempts, base):
    calls, slept = [0], [0.0]
    exc = {"TimeoutError": TimeoutError, "ConnectionError": ConnectionError, "ValueError": ValueError}
    def flaky():
        calls[0] += 1
        if calls[0] <= failures:
            raise exc[error]()
        return "ok"
    def retrying(fn):
        for attempt in range(1, max_attempts + 1):
            try:
                return fn()
            except Exception as e:
                if type(e).__name__ not in retry_on or attempt == max_attempts:
                    return type(e).__name__
                slept[0] += base * 2 ** (attempt - 1)
    return (retrying(flaky), calls[0], slept[0])


class ConfigError(Exception):
    pass


def get_setting(config, key):
    try:
        return int(config[key])
    except KeyError as e:
        raise ConfigError(f"missing setting {key}") from e
    except ValueError as e:
        raise ConfigError(f"setting {key} must be an integer") from e


Q(None, "Wrap Errors With Context", "Medium", "raise … from …",
  "<code>get_setting</code> turns low-level errors into a <code>ConfigError</code> with a helpful message, keeping the original as <code>__cause__</code>. For each key, return the value, or <code>[message, [exception names from outer to inner cause]]</code>.",
  [(({"PORT": "8080", "WORKERS": "four", "TIMEOUT": "30"}, ["PORT", "WORKERS", "DB_URL", "TIMEOUT"]), [8080, ['setting WORKERS must be an integer', ['ConfigError', 'ValueError']], ['missing setting DB_URL', ['ConfigError', 'KeyError']], 30])],
  ("try/except and walk the cause chain with a while loop.", "O(k · d)", "O(d)"),
  ("Same, with a generator over the chain.", "O(k · d)", "O(d)"),
  viz=(({"A": "1"}, ["A", "B"])))


@B
def settings(config, keys):
    out = []
    for k in keys:
        try:
            out.append(get_setting(config, k))
        except ConfigError as e:
            chain, cur = [], e
            while cur is not None:
                chain.append(type(cur).__name__)
                cur = cur.__cause__
            out.append([str(e), chain])
    return out


@O
def settings(config, keys):
    def chain(e):
        while e:
            yield type(e).__name__
            e = e.__cause__
    out = []
    for k in keys:
        try:
            out.append(get_setting(config, k))
        except ConfigError as e:
            out.append([str(e), list(chain(e))])
    return out


Q(None, "A Prometheus Histogram", "Medium", "Buckets, sum and count",
  "Prometheus histograms count observations into <b>cumulative</b> buckets (<code>le</code> = less than or equal) plus <code>+Inf</code>, and keep a sum and count. Return <code>({bucket label: count}, sum rounded to 3, count)</code> for the latencies (seconds).",
  [(([0.012, 0.045, 0.08, 0.2, 0.21, 0.35, 0.9, 1.7, 0.05, 0.03], [0.025, 0.05, 0.1, 0.25, 0.5, 1.0]), ({'0.025': 1, '0.05': 4, '0.1': 5, '0.25': 7, '0.5': 8, '1.0': 9, '+Inf': 10}, 3.577, 10))],
  ("For each bucket, count observations ≤ it.", "O(b · n)", "O(b)"),
  ("Sort once and bisect for each bucket.", "O(n log n + b log n)", "O(n)"),
  viz=(([0.1, 0.3], [0.2])))


@B
def histogram(obs, buckets):
    counts = {}
    for b in buckets:
        c = 0
        for o in obs:
            if o <= b:
                c += 1
        counts[str(b)] = c
    counts["+Inf"] = len(obs)
    return (counts, round(sum(obs), 3), len(obs))


@O
def histogram(obs, buckets):
    import bisect
    s = sorted(obs)
    counts = {str(b): bisect.bisect_right(s, b) for b in buckets}
    counts["+Inf"] = len(s)
    return (counts, round(sum(s), 3), len(s))


Q(None, "Estimate a Percentile From Buckets", "Medium", "histogram_quantile",
  "Given cumulative bucket counts (<code>[(upper bound, count)]</code> ascending, the last bound may be <code>'+Inf'</code>), estimate quantile q like PromQL's <code>histogram_quantile</code>: find the first bucket whose count ≥ q × total, then interpolate linearly inside it (from the previous bound, or 0). If it lands in +Inf, return the last finite bound. Round to 4.",
  [(([(0.05, 40), (0.1, 70), (0.25, 90), (0.5, 97), (1.0, 100), ("+Inf", 100)], [0.5, 0.9, 0.95, 0.99]), [0.0667, 0.25, 0.4286, 0.8333]), (([(0.1, 5), ("+Inf", 10)], [0.9]), [0.1])],
  ("Scan the buckets for each quantile.", "O(q · b)", "O(1)"),
  ("Bisect on the counts.", "O(q log b)", "O(b)"),
  viz=(([(1.0, 10), ("+Inf", 10)], [0.5])))


@B
def bucket_quantile(buckets, qs):
    total = buckets[-1][1]
    out = []
    for q in qs:
        rank = q * total
        prev_b, prev_c = 0.0, 0
        for b, c in buckets:
            if c >= rank:
                if b == "+Inf":
                    out.append(prev_b)
                else:
                    out.append(round(prev_b + (b - prev_b) * (rank - prev_c) / (c - prev_c), 4))
                break
            prev_b, prev_c = b, c
    return out


@O
def bucket_quantile(buckets, qs):
    import bisect
    counts = [c for _, c in buckets]
    def est(q):
        rank = q * counts[-1]
        i = bisect.bisect_left(counts, rank)
        lo_b, lo_c = (buckets[i - 1] if i else (0.0, 0))
        hi_b, hi_c = buckets[i]
        return lo_b if hi_b == "+Inf" else round(lo_b + (hi_b - lo_b) * (rank - lo_c) / (hi_c - lo_c), 4)
    return [est(q) for q in qs]


Q(None, "Rate From a Counter With Resets", "Medium", "Why rate() handles restarts",
  "A counter only goes up, but resets to 0 when the process restarts. Given samples <code>(seconds, value)</code>, compute the total increase (when a value drops, treat the new value as the increase since the reset) and the per-second rate over the whole window, rounded to 3.",
  [(([(0, 1200), (15, 1290), (30, 1400), (45, 30), (60, 140), (75, 260)],), (460, 6.133))],
  ("Walk neighbouring samples with an index.", "O(n)", "O(1)"),
  ("<code>zip</code> over pairs.", "O(n)", "O(1)"),
  viz=(([(0, 5), (10, 2)],)))


@B
def counter_rate(samples):
    inc = 0
    for i in range(1, len(samples)):
        prev, cur = samples[i - 1][1], samples[i][1]
        if cur >= prev:
            inc += cur - prev
        else:
            inc += cur
    secs = samples[-1][0] - samples[0][0]
    return (inc, round(inc / secs, 3))


@O
def counter_rate(samples):
    inc = sum(b - a if b >= a else b for (_, a), (_, b) in zip(samples, samples[1:]))
    return (inc, round(inc / (samples[-1][0] - samples[0][0]), 3))


Q(None, "Aggregate Health Checks", "Easy", "/health for a load balancer",
  "Dependencies are <code>(name, ok, critical)</code>. Overall status is <code>'unhealthy'</code> (HTTP 503) if any critical dependency is down, <code>'degraded'</code> (HTTP 200 — still serve traffic) if only non-critical ones are down, else <code>'healthy'</code> (200). Return <code>(status, http code, failing names sorted)</code>.",
  [(([("postgres", True, True), ("redis", False, False), ("email", True, False)],), ('degraded', 200, ['redis'])), (([("postgres", False, True), ("redis", False, False)],), ('unhealthy', 503, ['postgres', 'redis'])), (([("postgres", True, True)],), ('healthy', 200, []))],
  ("Flags in a loop.", "O(d)", "O(d)"),
  ("any() over the failures.", "O(d)", "O(d)"),
  viz=(([("db", False, True)],)))


@B
def health(deps):
    failing, critical_down = [], False
    for name, ok, critical in deps:
        if not ok:
            failing.append(name)
            if critical:
                critical_down = True
    if critical_down:
        return ("unhealthy", 503, sorted(failing))
    if failing:
        return ("degraded", 200, sorted(failing))
    return ("healthy", 200, [])


@O
def health(deps):
    down = [(n, c) for n, ok, c in deps if not ok]
    status = "unhealthy" if any(c for _, c in down) else "degraded" if down else "healthy"
    return (status, 503 if status == "unhealthy" else 200, sorted(n for n, _ in down))


Q(None, "Roll Out a Feature Flag", "Medium", "Percentage rollouts",
  "A flag is on for users in <code>allow</code>, off for users in <code>deny</code>, and otherwise on when <code>crc32(flag + ':' + user) % 100 < percent</code> — the same user always gets the same answer, and raising the percentage only adds users. Return the users with the flag on (in input order) for each percentage.",
  [(("new_checkout", [f"u{i}" for i in range(1, 21)], ["u7"], ["u3"], [10, 50]), {10: ['u7', 'u10', 'u14', 'u15'], 50: ['u6', 'u7', 'u10', 'u13', 'u14', 'u15', 'u16', 'u17', 'u18', 'u19']})],
  ("Compute each user's bucket with a loop per percentage.", "O(p · u)", "O(u)"),
  ("Compute buckets once and filter per percentage.", "O(u + p · u)", "O(u)"),
  viz=(("f", ["a", "b"], [], [], [50])))


@B
def rollout(flag, users, allow, deny, percents):
    out = {}
    for pct in percents:
        on = []
        for u in users:
            if u in deny:
                continue
            if u in allow or zlib.crc32(f"{flag}:{u}".encode()) % 100 < pct:
                on.append(u)
        out[pct] = on
    return out


@O
def rollout(flag, users, allow, deny, percents):
    bucket = {u: zlib.crc32(f"{flag}:{u}".encode()) % 100 for u in users}
    return {p: [u for u in users if u not in deny and (u in allow or bucket[u] < p)] for p in percents}


Q(None, "Sample Logs, Keep Every Error", "Easy", "Cut log costs safely",
  "Keep every WARNING and above; keep INFO and DEBUG only for requests where <code>crc32(request_id) % n == 0</code>, so a sampled request keeps all its lines. Return <code>(kept count, kept by level)</code>.",
  [(([("INFO", f"r{i // 3}") for i in range(60)] + [("ERROR", "r5"), ("WARNING", "r11"), ("ERROR", "r2")], 4), (18, {'ERROR': 2, 'INFO': 15, 'WARNING': 1}))],
  ("A loop with a level check and a hash check.", "O(n)", "O(1)"),
  ("A comprehension and Counter.", "O(n)", "O(1)"),
  viz=(([("INFO", "a"), ("ERROR", "b")], 2)))


@B
def sample_logs(records, n):
    kept = {}
    for lvl, rid in records:
        if LEVELS[lvl] >= 30 or zlib.crc32(rid.encode()) % n == 0:
            kept[lvl] = kept.get(lvl, 0) + 1
    return (sum(kept.values()), dict(sorted(kept.items())))


@O
def sample_logs(records, n):
    kept = Counter(l for l, r in records if LEVELS[l] >= 30 or zlib.crc32(r.encode()) % n == 0)
    return (sum(kept.values()), dict(sorted(kept.items())))


Q(None, "Alert Without Spamming", "Easy", "Cooldowns",
  "Alerts fire as <code>(second, key)</code>. Notify for a key only if it hasn't been notified within the last <code>cooldown</code> seconds; otherwise count it as suppressed. Return <code>(notifications as (second, key), suppressed per key)</code>.",
  [(([(0, "db-down"), (20, "db-down"), (40, "disk-90"), (290, "db-down"), (310, "db-down"), (650, "disk-90")], 300), ([(0, 'db-down'), (40, 'disk-90'), (310, 'db-down'), (650, 'disk-90')], {'db-down': 2}))],
  ("Track the last notification per key.", "O(n)", "O(k)"),
  ("Same with dict.get and a Counter.", "O(n)", "O(k)"),
  viz=(([(0, "a"), (1, "a")], 10)))


@B
def cooldown_alerts(alerts, cooldown):
    last, sent, suppressed = {}, [], {}
    for t, key in alerts:
        if key in last and t - last[key] < cooldown:
            suppressed[key] = suppressed.get(key, 0) + 1
        else:
            last[key] = t
            sent.append((t, key))
    return (sent, dict(sorted(suppressed.items())))


@O
def cooldown_alerts(alerts, cooldown):
    last, sent, sup = {}, [], Counter()
    for t, k in alerts:
        if t - last.get(k, -cooldown) < cooldown:
            sup[k] += 1
        else:
            last[k] = t
            sent.append((t, k))
    return (sent, dict(sorted(sup.items())))


Q(None, "Group Errors Like Sentry", "Medium", "Fingerprints",
  "Thousands of errors are often the same bug with different ids. Normalise each message — quoted strings → <code>'?'</code>, hex ids of 8+ characters → <code>X</code>, numbers → <code>N</code> — and return <code>(fingerprint, count)</code>, most common first (ties alphabetical).",
  [((["Order 4211 not found", "Order 977 not found", "User 'asha' has no cart", "User 'ravi' has no cart", "Timeout after 30s calling payments", "Order 12 not found", "Job 9f3a2c1d7e failed", "Job 0b7e44aa19 failed", "Timeout after 31s calling payments"],), [('Order N not found', 3), ('Job X failed', 2), ('Timeout after Ns calling payments', 2), ("User '?' has no cart", 2)])],
  ("Normalise with chained re.sub, count in a dict.", "O(n · L)", "O(g)"),
  ("A pattern list and Counter.most_common.", "O(n · L)", "O(g)"),
  viz=((["id 1", "id 2"],)))


@B
def group_errors(messages):
    counts = {}
    for m in messages:
        f = re.sub(r"'[^']*'", "'?'", m)
        f = re.sub(r"\b[0-9a-f]{8,}\b", "X", f)
        f = re.sub(r"\d+", "N", f)
        counts[f] = counts.get(f, 0) + 1
    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))


@O
def group_errors(messages):
    rules = [(r"'[^']*'", "'?'"), (r"\b[0-9a-f]{8,}\b", "X"), (r"\d+", "N")]
    def fp(m):
        for rx, rep in rules:
            m = re.sub(rx, rep, m)
        return m
    return sorted(Counter(map(fp, messages)).items(), key=lambda x: (-x[1], x[0]))


SCHEMA = {"port": ("int", True, None, None), "log_level": ("str", False, "INFO", ["DEBUG", "INFO", "WARNING", "ERROR"]),
          "workers": ("int", False, 2, None), "db_url": ("str", True, None, None), "debug": ("bool", False, False, None)}


Q(None, "Validate Configuration at Startup", "Medium", "Fail fast",
  "Check a config dict against <code>SCHEMA</code> (key → (type, required, default, allowed values)): missing required keys, wrong types (<code>'int'</code>, <code>'str'</code>, <code>'bool'</code>; a bool is not an int), values not allowed, and unknown keys are errors. Return <code>(final config with defaults filled, sorted errors)</code> — crash at startup rather than at 3 a.m.",
  [(({"port": 8080, "log_level": "VERBOSE", "workers": True, "colour": "blue"},), ({'port': 8080, 'debug': False}, ['colour: unknown setting', 'db_url: missing', "log_level: must be one of ['DEBUG', 'INFO', 'WARNING', 'ERROR']", 'workers: expected int'])), (({"port": 8000, "db_url": "postgres://db/app"},), ({'port': 8000, 'log_level': 'INFO', 'workers': 2, 'db_url': 'postgres://db/app', 'debug': False}, []))],
  ("If-statements per key.", "O(k)", "O(k)"),
  ("A type map and comprehensions.", "O(k)", "O(k)"),
  viz=(({"port": "x"},)))


@B
def validate_config(cfg):
    final, errors = {}, []
    for key, (typ, required, default, allowed) in SCHEMA.items():
        if key not in cfg:
            if required:
                errors.append(f"{key}: missing")
            else:
                final[key] = default
            continue
        v = cfg[key]
        ok = (typ == "int" and isinstance(v, int) and not isinstance(v, bool)) or (typ == "str" and isinstance(v, str)) or (typ == "bool" and isinstance(v, bool))
        if not ok:
            errors.append(f"{key}: expected {typ}")
        elif allowed and v not in allowed:
            errors.append(f"{key}: must be one of {allowed}")
        else:
            final[key] = v
    for key in cfg:
        if key not in SCHEMA:
            errors.append(f"{key}: unknown setting")
    return (final, sorted(errors))


@O
def validate_config(cfg):
    check = {"int": lambda v: type(v) is int, "str": lambda v: isinstance(v, str), "bool": lambda v: isinstance(v, bool)}
    final, errors = {}, [f"{k}: unknown setting" for k in cfg.keys() - SCHEMA.keys()]
    for k, (typ, req, default, allowed) in SCHEMA.items():
        if k not in cfg:
            if req:
                errors.append(f"{k}: missing")
            else:
                final[k] = default
        elif not check[typ](cfg[k]):
            errors.append(f"{k}: expected {typ}")
        elif allowed and cfg[k] not in allowed:
            errors.append(f"{k}: must be one of {allowed}")
        else:
            final[k] = cfg[k]
    return (final, sorted(errors))


Q(None, "Uptime From Health Checks", "Easy", "Availability and outages",
  "A check runs every minute (<code>True</code> = up). Return <code>(availability % rounded to 3, number of outages, longest outage in minutes)</code>.",
  [(([True] * 50 + [False] * 3 + [True] * 400 + [False] * 12 + [True] * 975,), (98.958, 2, 12))],
  ("Walk the list tracking the current outage.", "O(n)", "O(1)"),
  ("itertools.groupby runs.", "O(n)", "O(r)"),
  viz=(([True, False, True],)))


@B
def uptime(checks):
    up, outages, longest, run = 0, 0, 0, 0
    for c in checks:
        if c:
            up += 1
            run = 0
        else:
            if run == 0:
                outages += 1
            run += 1
            longest = max(longest, run)
    return (round(up / len(checks) * 100, 3), outages, longest)


@O
def uptime(checks):
    downs = [len(list(g)) for ok, g in itertools.groupby(checks) if not ok]
    return (round(100 * sum(checks) / len(checks), 3), len(downs), max(downs, default=0))
