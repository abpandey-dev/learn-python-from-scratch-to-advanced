from lib import *
import json
import importlib.util
import re
from collections import Counter, deque
from datetime import date
from functools import lru_cache
from urllib.parse import urlencode, quote, urlparse, parse_qs


TOPIC(
    id="modules-apis", title="Modules, Packages, APIs & JSON", glyph="{ }",
    blurb="Split code into modules and packages, install libraries in a virtual environment, read and write JSON, and call web APIs the safe way: status codes, pagination, retries, rate limits and caching.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">import math                     # whole module: math.sqrt(9)
from math import sqrt, pi       # just some names
import numpy as np              # a short alias
if __name__ == "__main__":      # runs only when the file is run directly
    main()

python -m venv .venv && source .venv/bin/activate   # a private set of libraries
pip install requests==2.32.3 && pip freeze > requirements.txt

text = json.dumps(data, indent=2)      # Python -> JSON text
data = json.loads(text)                # JSON text -> Python
with open("d.json") as f: data = json.load(f)

r = requests.get(url, params={"page": 2}, headers={"Authorization": f"Bearer {token}"}, timeout=10)
r.raise_for_status(); payload = r.json()</code></pre>
""")


Q(None, "Read a Nested JSON Field", "Easy", "Nested dicts and lists",
  "Follow <code>path</code> (a list of keys and list indexes) into parsed JSON. Return <code>default</code> if any step is missing.",
  [(({"user": {"tags": ["a", "b"]}}, ["user", "tags", 1], None), 'b'),
   (({"user": {"tags": []}}, ["user", "tags", 0], "none"), 'none'),
   (({"user": None}, ["user", "name"], "?"), '?')],
  ("Check the type and the key or index at every step before stepping in.", "O(depth)", "O(1)"),
  ("Just try every step and catch the three errors a missing step can raise.", "O(depth)", "O(1)"),
  viz=({"user": {"tags": ["a", "b"]}}, ["user", "tags", 1], None))


@B
def dig(data, path, default):
    cur = data
    for step in path:
        if isinstance(cur, dict) and step in cur:
            cur = cur[step]
        elif isinstance(cur, list) and isinstance(step, int) and -len(cur) <= step < len(cur):
            cur = cur[step]
        else:
            return default
    return cur


@O
def dig(data, path, default):
    cur = data
    try:
        for step in path:
            cur = cur[step]
    except (KeyError, IndexError, TypeError):
        return default
    return cur


Q(None, "JSON Text for a Flat Record", "Easy", "json.dumps",
  "Turn a flat dict of strings, ints and booleans into compact JSON text with keys sorted, like <code>{\"a\": 1, \"b\": true}</code>.",
  [(({"name": "Asha", "age": 31, "admin": False},), '{"admin": false, "age": 31, "name": "Asha"}'), (({},), '{}')],
  ("Build the text yourself: quote strings, lower-case booleans, join with commas.", "O(n log n)", "O(n)"),
  ("<code>json.dumps(record, sort_keys=True)</code> already knows every rule, including escaping.", "O(n log n)", "O(n)"),
  viz=({"name": "Asha", "age": 31, "admin": False},))


@B
def to_json(record):
    parts = []
    for key in sorted(record):
        value = record[key]
        if isinstance(value, bool):
            text = "true" if value else "false"
        elif isinstance(value, str):
            text = '"' + value + '"'
        else:
            text = str(value)
        parts.append('"' + key + '": ' + text)
    return "{" + ", ".join(parts) + "}"


@O
def to_json(record):
    return json.dumps(record, sort_keys=True)


Q(None, "What Survives a JSON Round Trip?", "Medium", "Type mapping",
  "Return what you get back after <code>json.loads(json.dumps(x))</code>: tuples become lists and dict keys become strings.",
  [(({1: (2, 3), "x": [True, None]},), {'1': [2, 3], 'x': [True, None]}), (((1, ("a", 2.5)),), [1, ['a', 2.5]])],
  ("Walk the value recursively: tuples to lists, every key to <code>str</code> (with True → 'true').", "O(n)", "O(n)"),
  ("Do the round trip itself.", "O(n)", "O(n)"),
  viz=({1: (2, 3), "x": [True, None]},))


@B
def round_trip(x):
    if isinstance(x, dict):
        out = {}
        for k, v in x.items():
            if isinstance(k, bool):
                key = "true" if k else "false"
            elif k is None:
                key = "null"
            else:
                key = str(k)
            out[key] = round_trip(v)
        return out
    if isinstance(x, (list, tuple)):
        return [round_trip(v) for v in x]
    return x


@O
def round_trip(x):
    return json.loads(json.dumps(x))


Q(None, "Count Records by Status", "Easy", "json.loads + counting",
  "<code>text</code> is a JSON array of objects that each have a <code>status</code>. Return a dict of status → count, sorted by status.",
  [(('[{"id":1,"status":"paid"},{"id":2,"status":"failed"},{"id":3,"status":"paid"}]',), {'failed': 1, 'paid': 2}), (("[]",), {})],
  ("Parse, then count in a dictionary with <code>get</code>.", "O(n log n)", "O(n)"),
  ("Parse, then <code>Counter</code>.", "O(n log n)", "O(n)"),
  viz=('[{"id":1,"status":"paid"},{"id":2,"status":"failed"},{"id":3,"status":"paid"}]',))


@B
def status_counts(text):
    records = json.loads(text)
    counts = {}
    for r in records:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    return {k: counts[k] for k in sorted(counts)}


@O
def status_counts(text):
    counts = Counter(r["status"] for r in json.loads(text))
    return dict(sorted(counts.items()))


Q(None, "Flatten Nested JSON", "Medium", "Recursion · dotted keys",
  "Flatten nested dicts into one level with dotted keys: <code>{\"a\": {\"b\": 1}}</code> → <code>{\"a.b\": 1}</code>. Lists stay as values.",
  [(({"id": 7, "user": {"name": "Ravi", "address": {"city": "Pune"}}, "tags": ["x"]},), {'id': 7, 'tags': ['x'], 'user.address.city': 'Pune', 'user.name': 'Ravi'}), (({"a": {}},), {})],
  ("An explicit stack of (prefix, dict) pairs.", "O(n)", "O(n)"),
  ("A short recursive function that passes the prefix down.", "O(n)", "O(depth)"),
  viz=({"id": 7, "user": {"name": "Ravi", "address": {"city": "Pune"}}},))


@B
def flatten(obj):
    out = {}
    stack = [("", obj)]
    while stack:
        prefix, d = stack.pop()
        for k, v in d.items():
            key = prefix + "." + k if prefix else k
            if isinstance(v, dict):
                stack.append((key, v))
            else:
                out[key] = v
    return dict(sorted(out.items()))


@O
def flatten(obj, prefix=""):
    out = {}
    for k, v in obj.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            out.update(flatten(v, key))
        else:
            out[key] = v
    return dict(sorted(out.items()))


Q(None, "Build a Query String", "Easy", "URL encoding",
  "Turn a dict of parameters into a query string. Spaces become <code>%20</code> and characters outside letters, digits and <code>-_.~</code> are percent-encoded.",
  [(({"q": "data science", "page": 2},), 'q=data%20science&page=2'), (({"city": "São Paulo", "sort": "-date"},), 'city=S%C3%A3o%20Paulo&sort=-date')],
  ("Encode each character yourself: UTF-8 bytes, then <code>%XX</code> for anything unsafe.", "O(n)", "O(n)"),
  ("<code>urlencode(params, quote_via=quote)</code>.", "O(n)", "O(n)"),
  viz=({"q": "data science", "page": 2},))


@B
def query_string(params):
    safe = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.~"

    def enc(text):
        out = ""
        for byte in str(text).encode("utf-8"):
            ch = chr(byte)
            out += ch if ch in safe else "%" + format(byte, "02X")
        return out

    return "&".join(enc(k) + "=" + enc(v) for k, v in params.items())


@O
def query_string(params):
    return urlencode(params, quote_via=quote)


Q(None, "Pull Apart a URL", "Medium", "urllib.parse",
  "Return <code>(scheme, host, path, params)</code> where params maps each query key to its first value.",
  [(("https://api.shop.in/v2/orders?status=paid&limit=50",), ('https', 'api.shop.in', '/v2/orders', {'status': 'paid', 'limit': '50'})), (("http://localhost:8000/health",), ('http', 'localhost:8000', '/health', {}))],
  ("Split on <code>://</code>, then the first <code>/</code>, then <code>?</code>, <code>&amp;</code> and <code>=</code>.", "O(n)", "O(n)"),
  ("<code>urlparse</code> and <code>parse_qs</code>, which also handle ports, fragments and encoding.", "O(n)", "O(n)"),
  viz=("https://api.shop.in/v2/orders?status=paid&limit=50",))


@B
def parse_url(url):
    scheme, rest = url.split("://", 1)
    rest, _, query = rest.partition("?")
    host, slash, path = rest.partition("/")
    params = {}
    if query:
        for pair in query.split("&"):
            k, _, v = pair.partition("=")
            params.setdefault(k, v)
    return (scheme, host, slash + path, params)


@O
def parse_url(url):
    p = urlparse(url)
    params = {k: v[0] for k, v in parse_qs(p.query).items()}
    return (p.scheme, p.netloc, p.path, params)


Q(None, "Join API Paths Without Double Slashes", "Easy", "Building endpoints",
  "Join a base URL and path parts with exactly one <code>/</code> between them.",
  [(("https://api.x.com/v1/", ["/users/", "42"]), 'https://api.x.com/v1/users/42'), (("https://api.x.com", ["orders"]), 'https://api.x.com/orders')],
  ("Trim slashes at the joins one part at a time.", "O(n)", "O(n)"),
  ("Strip every part and <code>'/'.join</code> once.", "O(n)", "O(n)"),
  viz=("https://api.x.com/v1/", ["/users/", "42"]))


@B
def join_url(base, parts):
    url = base
    for part in parts:
        while url.endswith("/"):
            url = url[:-1]
        while part.startswith("/"):
            part = part[1:]
        while part.endswith("/"):
            part = part[:-1]
        url = url + "/" + part
    return url


@O
def join_url(base, parts):
    return "/".join([base.rstrip("/")] + [p.strip("/") for p in parts])


Q(None, "Classify an HTTP Status Code", "Easy", "Status families",
  "Return 'ok' for 2xx, 'redirect' for 3xx, 'retry' for 429 or any 5xx, 'client error' for other 4xx, else 'unknown'.",
  [((200,), 'ok'), ((201,), 'ok'), ((304,), 'redirect'), ((404,), 'client error'), ((429,), 'retry'), ((503,), 'retry'), ((99,), 'unknown')],
  ("An if-chain over ranges.", "O(1)", "O(1)"),
  ("Special-case 429, then look up the family <code>code // 100</code> in a dict.", "O(1)", "O(1)"),
  viz=(429,))


@B
def status_kind(code):
    if 200 <= code <= 299:
        return "ok"
    if 300 <= code <= 399:
        return "redirect"
    if code == 429:
        return "retry"
    if 400 <= code <= 499:
        return "client error"
    if 500 <= code <= 599:
        return "retry"
    return "unknown"


@O
def status_kind(code):
    if code == 429:
        return "retry"
    families = {2: "ok", 3: "redirect", 4: "client error", 5: "retry"}
    return families.get(code // 100, "unknown")


Q(None, "Exponential Backoff Delays", "Easy", "Retry timing",
  "Return the wait (seconds) before each of <code>tries</code> retries: <code>base × 2^i</code>, never more than <code>cap</code>.",
  [((1, 5, 10), [1, 2, 4, 8, 10]), ((0.5, 4, 100), [0.5, 1.0, 2.0, 4.0]), ((2, 0, 10), [])],
  ("A loop that doubles a running delay and clips it.", "O(n)", "O(n)"),
  ("One comprehension with <code>min</code>.", "O(n)", "O(n)"),
  viz=(1, 5, 10))


@B
def backoff(base, tries, cap):
    delays = []
    d = base
    for _ in range(tries):
        delays.append(d if d < cap else cap)
        d = d * 2
    return delays


@O
def backoff(base, tries, cap):
    return [min(cap, base * 2 ** i) for i in range(tries)]


Q(None, "Call With Retries", "Medium", "Retry loop",
  "<code>responses</code> is the list of status codes the server will send, in order. Keep calling while the answer is retryable (429 or 5xx) and you have attempts left. Return <code>(final status, attempts used)</code>.",
  [(([503, 503, 200], 5), (200, 3)), (([500, 500, 500, 500], 3), (500, 3)), (([404, 200], 3), (404, 1))],
  ("A while loop with a counter and a flag.", "O(n)", "O(1)"),
  ("A for loop over attempts that returns as soon as the answer is final.", "O(n)", "O(1)"),
  viz=([503, 503, 200], 5))


@B
def call_with_retries(responses, max_attempts):
    attempts = 0
    status = None
    done = False
    while not done:
        status = responses[attempts]
        attempts += 1
        retryable = status == 429 or 500 <= status <= 599
        if not retryable or attempts == max_attempts:
            done = True
    return (status, attempts)


@O
def call_with_retries(responses, max_attempts):
    for attempt in range(1, max_attempts + 1):
        status = responses[attempt - 1]
        if not (status == 429 or status >= 500):
            break
    return (status, attempt)


PAGES = {None: {"items": [1, 2, 3], "next": "c2"}, "c2": {"items": [4, 5], "next": "c3"}, "c3": {"items": [6], "next": None}}


Q(None, "Collect Every Page", "Medium", "Cursor pagination",
  "<code>pages</code> fakes an API: <code>pages[cursor]</code> returns <code>{\"items\": [...], \"next\": cursor or None}</code>. Start from cursor None and return all items in order.",
  [((PAGES,), [1, 2, 3, 4, 5, 6]), (({None: {"items": [], "next": None}},), [])],
  ("A while-True loop that breaks when there is no next cursor.", "O(n)", "O(n)"),
  ("A generator that yields items page by page, so a caller could stop early.", "O(n)", "O(1) per page"),
  viz=(PAGES,))


@B
def all_items(pages):
    items = []
    cursor = None
    while True:
        page = pages[cursor]
        for item in page["items"]:
            items.append(item)
        if page["next"] is None:
            break
        cursor = page["next"]
    return items


@O
def all_items(pages):
    def walk():
        cursor = None
        while True:
            page = pages[cursor]
            yield from page["items"]
            cursor = page["next"]
            if cursor is None:
                return
    return list(walk())


Q(None, "Days Between ISO Dates", "Easy", "datetime from JSON",
  "APIs send dates as ISO text like <code>\"2026-03-01\"</code>. Return the number of days from <code>start</code> to <code>end</code>.",
  [(("2026-02-27", "2026-03-01"), 2), (("2024-02-28", "2024-03-01"), 2), (("2026-01-10", "2026-01-10"), 0)],
  ("Count days by hand: days in each month, with the leap-year rule.", "O(years)", "O(1)"),
  ("<code>date.fromisoformat</code>, then subtract: a <code>timedelta</code> knows its <code>.days</code>.", "O(1)", "O(1)"),
  viz=("2024-02-28", "2024-03-01"))


@B
def days_between(start, end):
    def day_number(text):
        y, m, d = (int(p) for p in text.split("-"))
        months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        total = 0
        for year in range(1, y):
            leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
            total += 366 if leap else 365
        leap = y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)
        for month in range(1, m):
            total += 29 if month == 2 and leap else months[month - 1]
        return total + d
    return day_number(end) - day_number(start)


@O
def days_between(start, end):
    return (date.fromisoformat(end) - date.fromisoformat(start)).days


Q(None, "Validate an API Response", "Medium", "Schema checks",
  "<code>schema</code> maps each required field to a type name ('str', 'int', 'list'). Return a sorted list of problems: <code>'missing: f'</code> or <code>'wrong type: f'</code>.",
  [(({"id": 5, "name": "Mina", "tags": "x"}, {"id": "int", "name": "str", "tags": "list", "email": "str"}), ['missing: email', 'wrong type: tags']),
   (({"id": 1}, {"id": "int"}), [])],
  ("Loop over the schema and append messages.", "O(k log k)", "O(k)"),
  ("Map type names to classes and build both lists with comprehensions.", "O(k log k)", "O(k)"),
  viz=({"id": 5, "name": "Mina", "tags": "x"}, {"id": "int", "name": "str", "tags": "list", "email": "str"}))


@B
def validate(payload, schema):
    problems = []
    for field in schema:
        if field not in payload:
            problems.append("missing: " + field)
        else:
            value = payload[field]
            kind = schema[field]
            ok = (kind == "str" and isinstance(value, str)) or (kind == "int" and isinstance(value, int)) \
                or (kind == "list" and isinstance(value, list))
            if not ok:
                problems.append("wrong type: " + field)
    return sorted(problems)


@O
def validate(payload, schema):
    types = {"str": str, "int": int, "list": list}
    missing = [f"missing: {f}" for f in schema if f not in payload]
    wrong = [f"wrong type: {f}" for f, t in schema.items() if f in payload and not isinstance(payload[f], types[t])]
    return sorted(missing + wrong)


Q(None, "Sliding-Window Rate Limiter", "Medium", "Rate limits · deque",
  "Allow at most <code>limit</code> requests in any <code>window</code> seconds. Given request times (sorted), return True/False for each: was it allowed? Rejected requests don't count.",
  [(([0, 1, 2, 3, 10, 11], 3, 10), [True, True, True, False, True, True]), (([0, 0, 0], 2, 1), [True, True, False])],
  ("For each request, count earlier allowed requests still inside the window.", "O(n²)", "O(n)"),
  ("Keep allowed times in a deque and drop old ones from the left.", "O(n)", "O(limit)"),
  viz=([0, 1, 2, 3, 10, 11], 3, 10))


@B
def allowed(times, limit, window):
    accepted = []
    result = []
    for t in times:
        recent = 0
        for a in accepted:
            if t - a < window:
                recent += 1
        if recent < limit:
            accepted.append(t)
            result.append(True)
        else:
            result.append(False)
    return result


@O
def allowed(times, limit, window):
    recent = deque()
    result = []
    for t in times:
        while recent and t - recent[0] >= window:
            recent.popleft()
        ok = len(recent) < limit
        if ok:
            recent.append(t)
        result.append(ok)
    return result


Q(None, "Cache Repeated API Calls", "Medium", "Memoisation · lru_cache",
  "A slow <code>fetch(user_id)</code> is called for each id in <code>ids</code>. With a cache, how many real calls happen? Return <code>(real calls, results)</code> where each result is <code>'user-&lt;id&gt;'</code>.",
  [(([3, 1, 3, 3, 2, 1],), (3, ['user-3', 'user-1', 'user-3', 'user-3', 'user-2', 'user-1'])), (([],), (0, []))],
  ("A dict cache checked before each call.", "O(n)", "O(unique)"),
  ("Wrap the function with <code>functools.lru_cache</code> and read its hit/miss info.", "O(n)", "O(unique)"),
  viz=([3, 1, 3, 3, 2, 1],))


@B
def cached_calls(ids):
    real = 0
    cache = {}
    results = []
    for i in ids:
        if i not in cache:
            real += 1
            cache[i] = "user-" + str(i)
        results.append(cache[i])
    return (real, results)


@O
def cached_calls(ids):
    @lru_cache(maxsize=None)
    def fetch(user_id):
        return f"user-{user_id}"
    results = [fetch(i) for i in ids]
    return (fetch.cache_info().misses, results)


Q(None, "What Does import * Bring In?", "Easy", "__all__ and private names",
  "Given a module's top-level names and its <code>__all__</code> (or None), return the names <code>from module import *</code> would import, sorted. Without <code>__all__</code>, names starting with <code>_</code> are skipped.",
  [((["load", "save", "_cache", "VERSION"], None), ['VERSION', 'load', 'save']), ((["load", "save", "_cache"], ["load"]), ['load'])],
  ("Two branches with a loop each.", "O(n log n)", "O(n)"),
  ("One expression: <code>__all__</code> if given, else a filtered comprehension.", "O(n log n)", "O(n)"),
  viz=(["load", "save", "_cache", "VERSION"], None))


@B
def star_names(names, all_list):
    out = []
    if all_list is not None:
        for n in all_list:
            out.append(n)
    else:
        for n in names:
            if not n.startswith("_"):
                out.append(n)
    return sorted(out)


@O
def star_names(names, all_list):
    return sorted(all_list if all_list is not None else [n for n in names if not n.startswith("_")])


Q(None, "Resolve a Relative Import", "Medium", "Packages",
  "Inside package <code>package</code>, resolve a relative import like <code>'..utils'</code> to its absolute name. One dot is the current package; each extra dot goes up a level.",
  [(("..utils", "app.api.v1"), 'app.api.utils'), ((".models", "app.api"), 'app.api.models'), (("...core.db", "app.api.v1"), 'app.core.db')],
  ("Count leading dots, drop that many − 1 parts from the package, then add the rest.", "O(n)", "O(n)"),
  ("<code>importlib.util.resolve_name</code> does exactly what <code>import</code> does.", "O(n)", "O(n)"),
  viz=("..utils", "app.api.v1"))


@B
def resolve(name, package):
    dots = len(name) - len(name.lstrip("."))
    rest = name[dots:]
    parts = package.split(".")
    base = parts[:len(parts) - (dots - 1)]
    return ".".join(base + ([rest] if rest else []))


@O
def resolve(name, package):
    return importlib.util.resolve_name(name, package)


Q(None, "Read a requirements.txt", "Easy", "Pinned dependencies",
  "Return a dict of package → version spec (like <code>'==2.2.0'</code>, or <code>''</code> if unpinned). Skip blank lines and comments; package names are lower-cased.",
  [(("# web\nrequests==2.32.3\n\nPandas>=2.2\nnumpy  # latest\n",), {'requests': '==2.32.3', 'pandas': '>=2.2', 'numpy': ''})],
  ("Strip comments, then scan each line for the first of <code>= &lt; &gt; ! ~</code>.", "O(n)", "O(n)"),
  ("One regular expression: a name, then an optional operator and version.", "O(n)", "O(n)"),
  viz=("# web\nrequests==2.32.3\n\nPandas>=2.2\nnumpy  # latest\n",))


@B
def requirements(text):
    out = {}
    for line in text.split("\n"):
        line = line.split("#")[0].strip()
        if not line:
            continue
        cut = len(line)
        for i, ch in enumerate(line):
            if ch in "=<>!~":
                cut = i
                break
        out[line[:cut].strip().lower()] = line[cut:].replace(" ", "")
    return out


@O
def requirements(text):
    out = {}
    for line in text.splitlines():
        m = re.match(r"\s*([A-Za-z0-9_.\-]+)\s*([=<>!~].*)?$", line.split("#")[0])
        if m:
            out[m.group(1).lower()] = (m.group(2) or "").replace(" ", "")
    return out


Q(None, "Compare Version Numbers", "Easy", "Versions are not strings",
  "Return −1, 0 or 1 comparing versions like <code>'1.10.0'</code> and <code>'1.9'</code> part by part (missing parts count as 0).",
  [(("1.10.0", "1.9"), 1), (("2.0", "2.0.0"), 0), (("0.9.9", "1.0"), -1)],
  ("Walk both lists of parts, padding the shorter with zeros.", "O(n)", "O(n)"),
  ("Pad to equal length and compare tuples of ints; <code>(a &gt; b) - (a &lt; b)</code> gives the sign.", "O(n)", "O(n)"),
  viz=("1.10.0", "1.9"))


@B
def compare_versions(a, b):
    pa = a.split(".")
    pb = b.split(".")
    for i in range(max(len(pa), len(pb))):
        x = int(pa[i]) if i < len(pa) else 0
        y = int(pb[i]) if i < len(pb) else 0
        if x > y:
            return 1
        if x < y:
            return -1
    return 0


@O
def compare_versions(a, b):
    pa, pb = [list(map(int, v.split("."))) for v in (a, b)]
    n = max(len(pa), len(pb))
    ta, tb = tuple(pa + [0] * (n - len(pa))), tuple(pb + [0] * (n - len(pb)))
    return (ta > tb) - (ta < tb)
