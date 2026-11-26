from lib import *
import bisect
import hashlib
import hmac
import math
from collections import Counter, defaultdict, deque

TOPIC(
    id="apis", title="APIs & Rate Limiting", glyph="🚦",
    blurb="Designing and protecting APIs: fixed-window, sliding-window, token-bucket and leaky-bucket limiters, per-user quotas, offset vs cursor pagination, idempotency keys, status codes, safe and idempotent methods, versioning, ETags, batching, deadlines, circuit breakers, gateways, webhook signatures and push vs poll.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">token bucket: tokens = min(cap, tokens + rate × Δt); allow if tokens ≥ 1  (allows bursts)
sliding window counter ≈ prev × (1 − elapsed/window) + current
pagination: cursor (WHERE id > last ORDER BY id LIMIT n) beats OFFSET at scale
POST + Idempotency-Key header → safe retries
429 Too Many Requests + Retry-After</code></pre>
""")


Q(None, "Fixed-Window Rate Limiter", "Easy", "Count per window",
  "Allow at most <code>limit</code> requests per window of <code>window</code> seconds (windows start at multiples of window). Return whether each request time is allowed.",
  [(([0, 1, 2, 3, 9.9, 10, 10.5, 11, 12, 25], 3, 10), [True, True, True, False, False, True, True, True, False, True])],
  ("Count earlier allowed requests in the same window.", "O(n²)", "O(n)"),
  ("A counter keyed by window number.", "O(n)", "O(w)"),
  viz=(([0, 1, 2], 2, 10)))


@B
def fixed_window(times, limit, window):
    allowed = []
    for i, t in enumerate(times):
        w = int(t // window)
        used = sum(1 for j in range(i) if allowed[j] and int(times[j] // window) == w)
        allowed.append(used < limit)
    return allowed


@O
def fixed_window(times, limit, window):
    counts, out = Counter(), []
    for t in times:
        w = int(t // window)
        out.append(counts[w] < limit)
        counts[w] += out[-1]
    return out


Q(None, "The Window-Boundary Burst", "Medium", "Fixed windows leak",
  "With a fixed-window limiter, requests at the end of one window and the start of the next all pass. Return the largest number of allowed requests inside any span of <code>window</code> seconds (span [t, t + window)).",
  [(([5, 9, 9.5, 9.8, 10, 10.1, 10.2, 14, 25], 3, 10), 6)],
  ("Apply the limiter, then check every start point.", "O(n²)", "O(n)"),
  ("Apply the limiter, then a two-pointer sweep.", "O(n)", "O(n)"),
  viz=(([9, 9.5, 10, 10.5], 2, 10)))


@B
def boundary_burst(times, limit, window):
    allowed, counts = [], {}
    for t in times:
        w = int(t // window)
        if counts.get(w, 0) < limit:
            counts[w] = counts.get(w, 0) + 1
            allowed.append(t)
    best = 0
    for start in allowed:
        best = max(best, sum(1 for t in allowed if start <= t < start + window))
    return best


@O
def boundary_burst(times, limit, window):
    counts, allowed = Counter(), []
    for t in times:
        w = int(t // window)
        if counts[w] < limit:
            counts[w] += 1
            allowed.append(t)
    best, lo = 0, 0
    for hi, t in enumerate(allowed):
        while allowed[lo] <= t - window:
            lo += 1
        best = max(best, hi - lo + 1)
    return best


Q(None, "Sliding-Window Log", "Medium", "Exact, but stores every timestamp",
  "Allow a request if fewer than <code>limit</code> allowed requests happened in the last <code>window</code> seconds (t − window, t]. Return the decisions.",
  [(([0, 1, 2, 3, 9.9, 10, 10.5, 11, 12, 25], 3, 10), [True, True, True, False, False, True, False, True, True, True])],
  ("Scan all previous allowed times.", "O(n²)", "O(n)"),
  ("A deque, popping expired timestamps.", "O(n)", "O(limit)"),
  viz=(([0, 1, 2], 2, 10)))


@B
def sliding_log(times, limit, window):
    log, out = [], []
    for t in times:
        recent = [x for x in log if x > t - window]
        ok = len(recent) < limit
        if ok:
            log.append(t)
        out.append(ok)
    return out


@O
def sliding_log(times, limit, window):
    log, out = deque(), []
    for t in times:
        while log and log[0] <= t - window:
            log.popleft()
        out.append(len(log) < limit)
        if out[-1]:
            log.append(t)
    return out


Q(None, "Sliding-Window Counter", "Medium", "Approximate and cheap",
  "Keep only two counters: the previous and current fixed window. Estimate = previous × (1 − elapsed fraction of the current window) + current. Allow if the estimate < <code>limit</code>. Return the decisions.",
  [(([1, 2, 3, 4, 5, 11, 12, 13, 15, 18, 19], 4, 10), [True, True, True, True, False, True, False, True, False, True, True])],
  ("Recount the previous window each time.", "O(n²)", "O(n)"),
  ("Roll two counters forward.", "O(n)", "O(1)"),
  viz=(([1, 2, 11], 2, 10)))


@B
def sliding_counter(times, limit, window):
    allowed_times, out = [], []
    for t in times:
        w = int(t // window)
        prev = sum(1 for x in allowed_times if int(x // window) == w - 1)
        cur = sum(1 for x in allowed_times if int(x // window) == w)
        est = prev * (1 - (t - w * window) / window) + cur
        ok = est < limit
        if ok:
            allowed_times.append(t)
        out.append(ok)
    return out


@O
def sliding_counter(times, limit, window):
    cur_w, prev, cur, out = None, 0, 0, []
    for t in times:
        w = int(t // window)
        if w != cur_w:
            prev = cur if cur_w == w - 1 else 0
            cur_w, cur = w, 0
        ok = prev * (1 - (t - w * window) / window) + cur < limit
        cur += ok
        out.append(ok)
    return out


Q(None, "Token Bucket", "Medium", "Bursts up to a cap",
  "A bucket holds up to <code>capacity</code> tokens (starting full) and refills at <code>rate</code> tokens/s. Each request spends one token or is rejected. Return the decisions.",
  [(([0, 0, 0, 0, 0, 0.5, 1, 1.2, 3, 3, 3, 3], 4, 1), [True, True, True, True, False, False, True, False, True, True, False, False])],
  ("Refill tick by tick in 0.1 s steps.", "O(T)", "O(1)"),
  ("Refill lazily by elapsed time.", "O(n)", "O(1)"),
  viz=(([0, 0, 0], 2, 1)))


@B
def token_bucket(times, capacity, rate):
    tokens, clock, out = capacity, 0, []
    for t in times:
        steps = round((t - clock) * 10)
        for _ in range(steps):
            tokens = min(capacity, tokens + rate / 10)
        clock = t
        if tokens >= 1 - 1e-9:
            tokens -= 1
            out.append(True)
        else:
            out.append(False)
    return out


@O
def token_bucket(times, capacity, rate):
    tokens, last, out = capacity, 0, []
    for t in times:
        tokens = min(capacity, tokens + (t - last) * rate)
        last = t
        ok = tokens >= 1 - 1e-9
        tokens -= ok
        out.append(ok)
    return out


Q(None, "Leaky Bucket", "Medium", "A smooth output rate",
  "Requests pour into a bucket of <code>capacity</code> that leaks at <code>rate</code> per second; a request that would overflow is dropped. Return the decisions — output is smoothed to the leak rate.",
  [(([0, 0, 0, 0, 0, 1, 1, 1, 4, 4], 3, 1), [True, True, True, False, False, True, False, False, True, True])],
  ("Leak in 0.1 s steps.", "O(T)", "O(1)"),
  ("Leak lazily by elapsed time.", "O(n)", "O(1)"),
  viz=(([0, 0, 0], 2, 1)))


@B
def leaky_bucket(times, capacity, rate):
    level, clock, out = 0.0, 0, []
    for t in times:
        for _ in range(round((t - clock) * 10)):
            level = max(0.0, level - rate / 10)
        clock = t
        if level + 1 <= capacity + 1e-9:
            level += 1
            out.append(True)
        else:
            out.append(False)
    return out


@O
def leaky_bucket(times, capacity, rate):
    level, last, out = 0.0, 0, []
    for t in times:
        level, last = max(0.0, level - (t - last) * rate), t
        ok = level + 1 <= capacity + 1e-9
        level += ok
        out.append(ok)
    return out


Q(None, "Per-User Quotas", "Easy", "One noisy client shouldn't hurt others",
  "Requests are <code>(user, second)</code>. Each user may make <code>limit</code> requests per fixed minute (60 s). Return the rejected count per user (only users with rejections, sorted).",
  [(([("u1", 1), ("u1", 2), ("u2", 3), ("u1", 4), ("u1", 30), ("u2", 59), ("u1", 61), ("u1", 62), ("u1", 63), ("u1", 64)], 3), [('u1', 2)])],
  ("Count prior requests per user per minute.", "O(n²)", "O(n)"),
  ("A counter keyed by (user, minute).", "O(n)", "O(n)"),
  viz=(([("a", 1), ("a", 2)], 1)))


@B
def user_quota(requests, limit):
    seen, rejected = [], {}
    for u, t in requests:
        used = sum(1 for su, st in seen if su == u and st // 60 == t // 60)
        if used < limit:
            seen.append((u, t))
        else:
            rejected[u] = rejected.get(u, 0) + 1
    return sorted(rejected.items())


@O
def user_quota(requests, limit):
    used, rejected = Counter(), Counter()
    for u, t in requests:
        if used[u, t // 60] < limit:
            used[u, t // 60] += 1
        else:
            rejected[u] += 1
    return sorted(rejected.items())


Q(None, "Offset vs Cursor Pagination", "Medium", "Pages that don't skip rows",
  "Paging through sorted ids with page size <code>size</code>; after page 1 is read, the ids in <code>deleted</code> are removed. Return the ids seen on the first <code>pages</code> pages with OFFSET paging and with cursor paging (id > last seen). Offset paging skips rows when earlier rows disappear.",
  [((list(range(1, 13)), 4, [2, 3], 3), ([1, 2, 3, 4, 7, 8, 9, 10, 11, 12], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]))],
  ("Slice lists for both methods.", "O(p · n)", "O(n)"),
  ("Slicing for offset, <code>bisect</code> for the cursor.", "O(p · log n)", "O(n)"),
  viz=((list(range(1, 7)), 2, [1], 2)))


@B
def pagination(ids, size, deleted, pages):
    offset_seen, cursor_seen = [], []
    data = list(ids)
    for p in range(pages):
        if p == 1:
            data = [i for i in data if i not in deleted]
        offset_seen += data[p * size:(p + 1) * size]
    data, last = list(ids), 0
    for p in range(pages):
        if p == 1:
            data = [i for i in data if i not in deleted]
        page = [i for i in data if i > last][:size]
        cursor_seen += page
        if page:
            last = page[-1]
    return (offset_seen, cursor_seen)


@O
def pagination(ids, size, deleted, pages):
    after = [i for i in ids if i not in set(deleted)]
    views = [ids] + [after] * (pages - 1)
    offset = [x for p, d in enumerate(views) for x in d[p * size:(p + 1) * size]]
    cursor, last = [], 0
    for d in views:
        k = bisect.bisect_right(d, last)
        page = d[k:k + size]
        cursor += page
        last = page[-1] if page else last
    return (offset, cursor)


Q(None, "Keyset Pagination With Ties", "Medium", "Sort by (created_at, id)",
  "Feeds sort by time, but many items share a timestamp. Use the cursor <code>(created_at, id)</code> of the last item and fetch items strictly after it. Items are <code>(created_at, id)</code>; return all pages of size <code>size</code>.",
  [(([(100, 7), (101, 2), (100, 3), (102, 9), (101, 1), (100, 5), (103, 4)], 3), [[(100, 3), (100, 5), (100, 7)], [(101, 1), (101, 2), (102, 9)], [(103, 4)]])],
  ("Sort, then filter by tuple comparison for each page.", "O(p · n)", "O(n)"),
  ("Sort once and bisect on the cursor tuple.", "O(n log n)", "O(n)"),
  viz=(([(1, 2), (1, 1), (2, 3)], 2)))


@B
def keyset(items, size):
    items = sorted(items)
    pages, cursor = [], None
    while True:
        page = [x for x in items if cursor is None or x > cursor][:size]
        if not page:
            return pages
        pages.append(page)
        cursor = page[-1]


@O
def keyset(items, size):
    items = sorted(items)
    pages, i = [], 0
    while i < len(items):
        pages.append(items[i:i + size])
        i = bisect.bisect_right(items, pages[-1][-1])
    return pages


Q(None, "Idempotency Keys", "Medium", "Safe POST retries",
  "Requests are <code>(idempotency_key, body)</code>. The first use creates order #1, #2, …; a repeat with the same body returns the saved response; a repeat with a different body returns '422 key reused'. Return each response.",
  [(([("k1", "2 shoes"), ("k2", "1 bag"), ("k1", "2 shoes"), ("k1", "3 shoes"), ("k3", "1 hat"), ("k2", "1 bag")],), ['201 order #1', '201 order #2', '201 order #1', '422 key reused', '201 order #3', '201 order #2'])],
  ("Search a list of saved (key, body, response).", "O(n²)", "O(n)"),
  ("A dict key → (body, response).", "O(n)", "O(n)"),
  viz=(([("a", "x"), ("a", "x")],)))


@B
def idempotency_keys(requests):
    saved, out, n = [], [], 0
    for key, body in requests:
        found = None
        for k, b, r in saved:
            if k == key:
                found = (b, r)
        if found is None:
            n += 1
            resp = f"201 order #{n}"
            saved.append((key, body, resp))
            out.append(resp)
        elif found[0] == body:
            out.append(found[1])
        else:
            out.append("422 key reused")
    return out


@O
def idempotency_keys(requests):
    saved, out = {}, []
    for key, body in requests:
        if key not in saved:
            saved[key] = (body, f"201 order #{len(saved) + 1}")
        b, resp = saved[key]
        out.append(resp if b == body else "422 key reused")
    return out


CODES = {"created": 201, "accepted for later": 202, "deleted": 204, "bad input": 400, "not logged in": 401,
         "not allowed": 403, "not found": 404, "version conflict": 409, "too many requests": 429,
         "server bug": 500, "dependency down": 503}


Q(None, "Pick the Status Code", "Easy", "Speak HTTP",
  "Return the HTTP status code for each situation using <code>CODES</code>; anything unknown is 500.",
  [((["created", "not logged in", "not allowed", "too many requests", "version conflict", "accepted for later", "dependency down", "who knows"],), [201, 401, 403, 429, 409, 202, 503, 500])],
  ("An if/elif chain.", "O(n)", "O(n)"),
  ("<code>dict.get</code> with a default.", "O(n)", "O(n)"),
  viz=((["created"],)))


@B
def status_codes(situations):
    out = []
    for s in situations:
        code = 500
        for k, v in CODES.items():
            if k == s:
                code = v
        out.append(code)
    return out


@O
def status_codes(situations):
    return [CODES.get(s, 500) for s in situations]


Q(None, "Safe and Idempotent Methods", "Easy", "Which calls can be retried blindly?",
  "Return <code>(method, safe, idempotent)</code>: GET, HEAD and OPTIONS are safe (no changes) and idempotent; PUT and DELETE are idempotent but not safe; POST and PATCH are neither.",
  [((["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD"],), [('GET', True, True), ('POST', False, False), ('PUT', False, True), ('PATCH', False, False), ('DELETE', False, True), ('HEAD', True, True)])],
  ("If/elif per method.", "O(n)", "O(n)"),
  ("Set membership.", "O(n)", "O(n)"),
  viz=((["GET", "POST"],)))


@B
def method_props(methods):
    out = []
    for m in methods:
        if m in ("GET", "HEAD", "OPTIONS"):
            out.append((m, True, True))
        elif m in ("PUT", "DELETE"):
            out.append((m, False, True))
        else:
            out.append((m, False, False))
    return out


@O
def method_props(methods):
    safe = {"GET", "HEAD", "OPTIONS"}
    return [(m, m in safe, m in safe | {"PUT", "DELETE"}) for m in methods]


Q(None, "Route by API Version", "Easy", "Serve the newest compatible version",
  "The server implements the sorted <code>versions</code>. A client asking for version v gets the highest implemented version ≤ v; below the oldest supported version it gets '410 Gone'.",
  [(([2, 3, 5, 8], [1, 2, 4, 5, 7, 9]), ['410 Gone', 2, 3, 5, 5, 8])],
  ("Scan the versions.", "O(r · v)", "O(1)"),
  ("<code>bisect_right</code>.", "O(r log v)", "O(1)"),
  viz=(([1, 3], [2])))


@B
def api_version(versions, requested):
    out = []
    for r in requested:
        best = None
        for v in versions:
            if v <= r:
                best = v
        out.append(best if best is not None else "410 Gone")
    return out


@O
def api_version(versions, requested):
    def pick(r):
        i = bisect.bisect_right(versions, r)
        return versions[i - 1] if i else "410 Gone"
    return [pick(r) for r in requested]


Q(None, "Conditional GET With ETags", "Medium", "304 Not Modified",
  "The ETag of a resource is the first 8 hex characters of the MD5 of its content. For each request <code>(path, If-None-Match etag or None)</code>, return 304 if the tag matches, else <code>(200, etag)</code>.",
  [(({"/a": "hello", "/b": "world"}, [("/a", None), ("/a", "5d41402a"), ("/b", "5d41402a"), ("/b", "7d793037")]), [(200, '5d41402a'), 304, (200, '7d793037'), 304])],
  ("Hash the content on every request.", "O(r · L)", "O(1)"),
  ("Compute each ETag once.", "O(n · L + r)", "O(n)"),
  viz=(({"/x": "hi"}, [("/x", None)])))


@B
def etags(resources, requests):
    out = []
    for path, tag in requests:
        etag = hashlib.md5(resources[path].encode()).hexdigest()[:8]
        if tag == etag:
            out.append(304)
        else:
            out.append((200, etag))
    return out


@O
def etags(resources, requests):
    tags = {p: hashlib.md5(c.encode()).hexdigest()[:8] for p, c in resources.items()}
    return [304 if tag == tags[p] else (200, tags[p]) for p, tag in requests]


Q(None, "Chatty vs Batched vs Parallel Calls", "Easy", "Round trips add up",
  "Fetching <code>n</code> items costs one round trip of <code>rtt</code> ms per call plus <code>item_ms</code> per item served. Return the total ms for one call per item in sequence, batches of <code>batch</code> in sequence, and one call per item with <code>concurrency</code> in flight.",
  [((100, 40, 1, 25, 10), (4100, 260, 410))],
  ("Loops adding up time.", "O(n)", "O(1)"),
  ("Closed-form with <code>math.ceil</code>.", "O(1)", "O(1)"),
  viz=((10, 40, 1, 5, 5)))


@B
def call_patterns(n, rtt, item_ms, batch, concurrency):
    seq = 0
    for _ in range(n):
        seq += rtt + item_ms
    batched, left = 0, n
    while left > 0:
        k = min(batch, left)
        batched += rtt + k * item_ms
        left -= k
    waves = 0
    left = n
    while left > 0:
        waves += 1
        left -= concurrency
    return (seq, batched, waves * (rtt + item_ms))


@O
def call_patterns(n, rtt, item_ms, batch, concurrency):
    return (n * (rtt + item_ms), math.ceil(n / batch) * rtt + n * item_ms, math.ceil(n / concurrency) * (rtt + item_ms))


Q(None, "Retries Within a Deadline", "Medium", "Timeouts must add up",
  "A request has an overall <code>deadline</code> (ms). Each try may take up to <code>try_timeout</code>; between tries the client waits the listed backoffs. Return how many tries can start and still finish before the deadline in the worst case.",
  [((1000, 300, [50, 100, 200, 400]), 2), ((500, 600, [10]), 0)],
  ("Add time until the deadline is passed.", "O(b)", "O(1)"),
  ("Same, with <code>itertools.accumulate</code>.", "O(b)", "O(b)"),
  viz=((700, 200, [100, 100])))


@B
def tries_in_deadline(deadline, try_timeout, backoffs):
    used, tries = 0, 0
    waits = [0] + list(backoffs)
    for w in waits:
        if used + w + try_timeout <= deadline:
            used += w + try_timeout
            tries += 1
        else:
            break
    return tries


@O
def tries_in_deadline(deadline, try_timeout, backoffs):
    from itertools import accumulate, takewhile
    ends = accumulate(w + try_timeout for w in [0, *backoffs])
    return sum(1 for _ in takewhile(lambda e: e <= deadline, ends))


Q(None, "A Circuit Breaker", "Hard", "Fail fast when a dependency is down",
  "Calls <code>(time, would_succeed)</code> go through a breaker. Closed: after <code>threshold</code> consecutive failures it opens. Open: calls are 'rejected' until <code>cooldown</code> seconds have passed since opening; then it is half-open and lets one call try: success closes it, failure reopens it. Return 'ok', 'fail' or 'rejected' per call.",
  [(([(0, True), (1, False), (2, False), (3, False), (4, True), (5, True), (9, False), (10, True), (15, True), (16, True)], 3, 5), ['ok', 'fail', 'fail', 'fail', 'rejected', 'rejected', 'fail', 'rejected', 'ok', 'ok'])],
  ("A state variable and if/elif branches.", "O(n)", "O(1)"),
  ("Same state machine, fewer branches.", "O(n)", "O(1)"),
  viz=(([(0, False), (1, False), (2, True)], 2, 5)))


@B
def circuit_breaker(calls, threshold, cooldown):
    state, fails, opened, out = "closed", 0, None, []
    for t, ok in calls:
        if state == "open":
            if t - opened >= cooldown:
                state = "half"
            else:
                out.append("rejected")
                continue
        if ok:
            out.append("ok")
            fails = 0
            state = "closed"
        else:
            out.append("fail")
            fails += 1
            if state == "half" or fails >= threshold:
                state = "open"
                opened = t
    return out


@O
def circuit_breaker(calls, threshold, cooldown):
    fails, opened, out = 0, None, []
    for t, ok in calls:
        if opened is not None and t - opened < cooldown:
            out.append("rejected")
            continue
        half = opened is not None
        out.append("ok" if ok else "fail")
        fails = 0 if ok else fails + 1
        opened = None if ok else (t if half or fails >= threshold else None)
    return out


Q(None, "An API Gateway", "Medium", "Auth, then route",
  "For each request <code>(path, token)</code>: return 401 if the token is not in <code>valid</code>, else the service of the longest matching route prefix, else 404.",
  [(({"/api/users": "user-svc", "/api/users/admin": "admin-svc", "/api/orders": "order-svc"}, {"t1", "t2"}, [("/api/users/42", "t1"), ("/api/users/admin/x", "t2"), ("/api/orders", "bad"), ("/api/payments", "t1")]), ['user-svc', 'admin-svc', 401, 404])],
  ("Check every route for every request.", "O(r · k)", "O(1)"),
  ("Try prefixes from longest to shortest.", "O(r · k)", "O(k)"),
  viz=(({"/a": "A"}, {"t"}, [("/a/1", "t")])))


@B
def gateway(routes, valid, requests):
    out = []
    for path, token in requests:
        if token not in valid:
            out.append(401)
            continue
        best = None
        for prefix, svc in routes.items():
            if path.startswith(prefix) and (best is None or len(prefix) > len(best[0])):
                best = (prefix, svc)
        out.append(best[1] if best else 404)
    return out


@O
def gateway(routes, valid, requests):
    ordered = sorted(routes, key=len, reverse=True)
    def route(path):
        return next((routes[p] for p in ordered if path.startswith(p)), 404)
    return [401 if token not in valid else route(path) for path, token in requests]


Q(None, "Sign Webhook Payloads (HMAC)", "Medium", "Prove the sender",
  "Webhook receivers verify an HMAC-SHA256 signature of the body with a shared secret. Return the first 16 hex characters of the signature for each payload. The brute force builds HMAC by hand (inner and outer padded hashes); the optimal uses the <code>hmac</code> module.",
  [(("s3cret", ['{"order":1,"status":"paid"}', '{"order":1,"status":"refunded"}']), ['efb845265d0aec52', 'f86dbec2aaa2f23e'])],
  ("HMAC by hand: H((K ⊕ opad) ‖ H((K ⊕ ipad) ‖ m)).", "O(L)", "O(L)"),
  ("<code>hmac.new(key, msg, hashlib.sha256)</code>.", "O(L)", "O(L)"),
  viz=(("k", ["hi"])))


@B
def sign_payloads(secret, payloads):
    key = secret.encode().ljust(64, b"\0")
    ipad = bytes(b ^ 0x36 for b in key)
    opad = bytes(b ^ 0x5C for b in key)
    out = []
    for p in payloads:
        inner = hashlib.sha256(ipad + p.encode()).digest()
        out.append(hashlib.sha256(opad + inner).hexdigest()[:16])
    return out


@O
def sign_payloads(secret, payloads):
    return [hmac.new(secret.encode(), p.encode(), hashlib.sha256).hexdigest()[:16] for p in payloads]


Q(None, "Polling vs Push", "Easy", "Wasted requests",
  "<code>clients</code> each poll every <code>poll_s</code> seconds, but each client only gets <code>updates_per_min</code> real updates per minute. Return <code>(poll requests/s, pushed messages/s over WebSockets/SSE, % of polls that find nothing)</code>, rounded to 1.",
  [((100000, 5, 1), (20000.0, 1666.7, 91.7)), ((2000, 30, 4), (66.7, 133.3, 0.0))],
  ("Step by step arithmetic.", "O(1)", "O(1)"),
  ("Same, compact.", "O(1)", "O(1)"),
  viz=((100, 10, 1)))


@B
def poll_vs_push(clients, poll_s, updates_per_min):
    polls = clients / poll_s
    pushes = clients * updates_per_min / 60
    useful = pushes
    if useful > polls:
        useful = polls
    wasted = (polls - useful) / polls * 100
    return (round(polls, 1), round(pushes, 1), round(wasted, 1))


@O
def poll_vs_push(clients, poll_s, updates_per_min):
    polls, pushes = clients / poll_s, clients * updates_per_min / 60
    return (round(polls, 1), round(pushes, 1), round((1 - min(pushes, polls) / polls) * 100, 1))
