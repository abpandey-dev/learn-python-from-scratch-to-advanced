from lib import *
import hashlib
import math
import re
import zlib
from collections import Counter, defaultdict
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

TOPIC(
    id="ids", title="URL Shortener & ID Generation", glyph="🔗",
    blurb="The classic first design question: base62 codes, code length and capacity, hashing with collision handling, ticket ranges and key-generation services, Snowflake IDs (compose, decode, sequence limits, clock rollback), time-sortable IDs, birthday-paradox collisions, Bloom filters, aliases, expiry, analytics and URL canonicalisation.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">base62 alphabet: 0-9 a-z A-Z;  62^7 ≈ 3.5 trillion codes
snowflake (64 bits): 1 sign | 41 ms timestamp | 10 machine | 12 sequence  → 4096 ids/ms/machine
random ids collide after about sqrt(2^bits) draws (birthday paradox)
redirect: 301 (cached by browsers, fewer hits) vs 302 (every click reaches you → analytics)</code></pre>
""")

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


Q(None, "Base62 Encode", "Easy", "Numbers to short codes",
  "Encode each non-negative integer in base 62 using <code>ALPHABET</code> (0 → '0').",
  [(([0, 61, 62, 125, 3843, 1_000_000, 56_800_235_583],), ['0', 'Z', '10', '21', 'ZZ', '4c92', 'ZZZZZZ'])],
  ("Repeated division, building a list.", "O(n · log v)", "O(log v)"),
  ("<code>divmod</code> in a helper.", "O(n · log v)", "O(log v)"),
  viz=(([125],)))


@B
def b62_encode(nums):
    out = []
    for n in nums:
        if n == 0:
            out.append("0")
            continue
        s = ""
        while n > 0:
            s = ALPHABET[n % 62] + s
            n = n // 62
        out.append(s)
    return out


@O
def b62_encode(nums):
    def enc(n):
        s = []
        while True:
            n, r = divmod(n, 62)
            s.append(ALPHABET[r])
            if n == 0:
                return "".join(reversed(s))
    return [enc(n) for n in nums]


Q(None, "Base62 Decode", "Easy", "Short codes back to numbers",
  "Decode each base62 code back to its integer.",
  [((["0", "Z", "10", "21", "ZZ", "4c92", "ZZZZZZ"],), [0, 61, 62, 125, 3843, 1000000, 56800235583])],
  ("Search the alphabet for each character.", "O(n · L · 62)", "O(1)"),
  ("A char → value dict and Horner's rule.", "O(n · L)", "O(62)"),
  viz=((["21"],)))


@B
def b62_decode(codes):
    out = []
    for c in codes:
        n = 0
        for ch in c:
            n = n * 62 + ALPHABET.index(ch)
        out.append(n)
    return out


@O
def b62_decode(codes):
    value = {ch: i for i, ch in enumerate(ALPHABET)}
    out = []
    for c in codes:
        n = 0
        for ch in c:
            n = n * 62 + value[ch]
        out.append(n)
    return out


Q(None, "How Long Will the Codes Last?", "Easy", "Capacity planning",
  "For each code length, return <code>(number of codes, years until exhausted)</code> at <code>per_day</code> new links (years rounded to 1).",
  [(([5, 6, 7, 8], 100_000_000), [(916132832, 0.0), (56800235584, 1.6), (3521614606208, 96.5), (218340105584896, 5981.9)])],
  ("Multiply 62 in a loop.", "O(L)", "O(1)"),
  ("<code>62 ** L</code>.", "O(1)", "O(1)"),
  viz=(([6], 1_000_000)))


@B
def code_capacity(lengths, per_day):
    out = []
    for L in lengths:
        n = 1
        for _ in range(L):
            n *= 62
        out.append((n, round(n / per_day / 365, 1)))
    return out


@O
def code_capacity(lengths, per_day):
    return [(62 ** L, round(62 ** L / per_day / 365, 1)) for L in lengths]


Q(None, "Hash, Then Handle Collisions", "Medium", "Content-derived codes",
  "Take the first <code>k</code> hex characters of MD5(url). If that code is taken by a different URL, append '#1', '#2', … to the URL and rehash until free. The same URL always gets its existing code. Return the codes.",
  [((["a.com/1", "a.com/2", "a.com/3", "a.com/1", "b.com/9", "b.com/8", "c.com/x"], 1), ['f', '8', '6', 'f', 'e', '7', '5'])],
  ("Search a list of (code, url) pairs.", "O(n² · r)", "O(n)"),
  ("Dicts in both directions.", "O(n · r)", "O(n)"),
  viz=((["x", "y"], 1)))


@B
def hash_codes(urls, k):
    taken, out = [], []
    for u in urls:
        existing = [c for c, url in taken if url == u]
        if existing:
            out.append(existing[0])
            continue
        attempt, salt = u, 0
        while True:
            code = hashlib.md5(attempt.encode()).hexdigest()[:k]
            if code not in [c for c, _ in taken]:
                break
            salt += 1
            attempt = f"{u}#{salt}"
        taken.append((code, u))
        out.append(code)
    return out


@O
def hash_codes(urls, k):
    by_code, by_url, out = {}, {}, []
    for u in urls:
        if u not in by_url:
            salt, code = 0, hashlib.md5(u.encode()).hexdigest()[:k]
            while code in by_code:
                salt += 1
                code = hashlib.md5(f"{u}#{salt}".encode()).hexdigest()[:k]
            by_code[code], by_url[u] = u, code
        out.append(by_url[u])
    return out


Q(None, "Hand Out ID Ranges", "Medium", "Ticket server / range allocation",
  "A central counter hands each app server a block of <code>block</code> ids at a time; servers use their block locally without coordination. For a sequence of servers asking for one id each, return the ids issued.",
  [((["s1", "s1", "s2", "s1", "s2", "s3", "s1", "s1"], 3), [1, 2, 4, 3, 5, 7, 10, 11])],
  ("Lists of remaining ids per server.", "O(n · b)", "O(s · b)"),
  ("Keep (next, end) per server.", "O(n)", "O(s)"),
  viz=((["a", "b", "a"], 2)))


@B
def id_ranges(requests, block):
    counter, pools, out = 1, {}, []
    for s in requests:
        if not pools.get(s):
            pools[s] = list(range(counter, counter + block))
            counter += block
        out.append(pools[s].pop(0))
    return out


@O
def id_ranges(requests, block):
    counter, state, out = 1, {}, []
    for s in requests:
        nxt, end = state.get(s, (0, 0))
        if nxt == end:
            nxt, end, counter = counter, counter + block, counter + block
        out.append(nxt)
        state[s] = (nxt + 1, end)
    return out


Q(None, "A Key-Generation Service", "Medium", "Pre-made keys and what a crash wastes",
  "A KGS holds <code>pool</code> unused keys and gives servers batches of <code>batch</code>. Events are <code>('use', server)</code> (take one key; fetch a batch if the server has none) and <code>('crash', server)</code> (its unused keys are lost). Return <code>(keys used, keys wasted, keys left in the pool)</code>.",
  [((1000, 10, [("use", "a"), ("use", "a"), ("use", "b"), ("crash", "a"), ("use", "a"), ("use", "b"), ("crash", "b")]), (5, 16, 970))],
  ("Lists of keys per server.", "O(e · b)", "O(s · b)"),
  ("Counters per server.", "O(e)", "O(s)"),
  viz=((100, 5, [("use", "a"), ("crash", "a")])))


@B
def kgs(pool, batch, events):
    held, used, wasted = {}, 0, 0
    for kind, s in events:
        if kind == "use":
            if not held.get(s):
                held[s] = list(range(batch))
                pool -= batch
            held[s].pop()
            used += 1
        else:
            wasted += len(held.get(s, []))
            held[s] = []
    return (used, wasted, pool)


@O
def kgs(pool, batch, events):
    held, used, wasted = defaultdict(int), 0, 0
    for kind, s in events:
        if kind == "crash":
            wasted, held[s] = wasted + held[s], 0
            continue
        if held[s] == 0:
            held[s], pool = batch, pool - batch
        held[s], used = held[s] - 1, used + 1
    return (used, wasted, pool)


EPOCH = 1_700_000_000_000


Q(None, "Build a Snowflake ID", "Medium", "Time + machine + sequence",
  "Compose 64-bit ids: <code>(ms − EPOCH) &lt;&lt; 22 | machine &lt;&lt; 12 | sequence</code> for each <code>(unix_ms, machine, sequence)</code>. IDs sort by time and need no coordination.",
  [(([(1_700_000_000_000, 1, 0), (1_700_000_000_001, 1, 0), (1_700_000_000_001, 1, 1), (1_700_000_000_001, 2, 0), (1_767_225_600_000, 1023, 4095)],), [4096, 4198400, 4198401, 4202496, 281964602986594303])],
  ("Multiply by powers of two.", "O(n)", "O(n)"),
  ("Shifts and ORs.", "O(n)", "O(n)"),
  viz=(([(1_700_000_000_005, 3, 2)],)))


@B
def snowflake(parts):
    out = []
    for ms, machine, seq in parts:
        out.append((ms - EPOCH) * 2 ** 22 + machine * 2 ** 12 + seq)
    return out


@O
def snowflake(parts):
    return [(ms - EPOCH) << 22 | m << 12 | s for ms, m, s in parts]


Q(None, "Decode a Snowflake ID", "Easy", "Read the timestamp back",
  "Return <code>(unix_ms, machine, sequence)</code> for each id.",
  [(([0, 4198401, 4202497, 281964602986594303],), [(1700000000000, 0, 0), (1700000000001, 1, 1), (1700000000001, 2, 1), (1767225600000, 1023, 4095)])],
  ("Integer division and modulo.", "O(n)", "O(n)"),
  ("Shifts and masks.", "O(n)", "O(n)"),
  viz=(([4198401],)))


@B
def unsnowflake(ids):
    out = []
    for i in ids:
        out.append((i // 2 ** 22 + EPOCH, i // 2 ** 12 % 1024, i % 4096))
    return out


@O
def unsnowflake(ids):
    return [((i >> 22) + EPOCH, (i >> 12) & 0x3FF, i & 0xFFF) for i in ids]


Q(None, "When the Sequence Runs Out", "Easy", "IDs per millisecond",
  "With <code>seq_bits</code> sequence bits, one machine makes 2^seq_bits ids per ms; extra requests wait for the next ms. For each burst size (requests arriving in the same ms), return how many milliseconds it takes to issue them.",
  [(([1, 4096, 4097, 10000, 50000], 12), [1, 1, 2, 3, 13])],
  ("Subtract per-ms capacity in a loop.", "O(n · b)", "O(1)"),
  ("Ceiling division.", "O(n)", "O(n)"),
  viz=(([5000], 12)))


@B
def seq_overflow(bursts, seq_bits):
    out = []
    for b in bursts:
        ms = 0
        while b > 0:
            b -= 2 ** seq_bits
            ms += 1
        out.append(ms)
    return out


@O
def seq_overflow(bursts, seq_bits):
    return [math.ceil(b / (1 << seq_bits)) for b in bursts]


Q(None, "The Clock Went Backwards", "Medium", "Never issue a duplicate",
  "An ID generator reads the clock for each request. If the clock is behind the last timestamp used (NTP adjusted it), keep using the last timestamp and continue its sequence instead of going back. Return <code>(timestamp, sequence)</code> per request.",
  [(([100, 100, 101, 99, 99, 101, 102],), [(100, 0), (100, 1), (101, 0), (101, 1), (101, 2), (101, 3), (102, 0)])],
  ("Track last timestamp and sequence with if/elif.", "O(n)", "O(1)"),
  ("<code>max</code> of clock and last.", "O(n)", "O(1)"),
  viz=(([5, 4],)))


@B
def clock_back(readings):
    last, seq, out = -1, 0, []
    for t in readings:
        if t > last:
            last, seq = t, 0
        else:
            seq += 1
        out.append((last, seq))
    return out


@O
def clock_back(readings):
    last, seq, out = -1, 0, []
    for t in readings:
        ts = max(t, last)
        seq = seq + 1 if ts == last else 0
        last = ts
        out.append((ts, seq))
    return out


CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


Q(None, "Time-Sortable String IDs", "Medium", "ULID-style timestamps",
  "Encode each millisecond timestamp as 10 characters of Crockford base32 (as ULIDs do). Return the codes and whether sorting the strings gives the same order as sorting the numbers — the reason ULIDs and UUIDv7 make good database keys.",
  [(([1_700_000_000_000, 1_700_000_000_001, 1_600_000_000_000, 1_800_000_000_000],), (['01HF7YAT00', '01HF7YAT01', '01EJ3PX000', '01MCC5RM00'], True))],
  ("Divide by 32 ten times.", "O(n)", "O(n)"),
  ("Shift by 5 bits ten times.", "O(n)", "O(n)"),
  viz=(([1_700_000_000_000],)))


@B
def ulid_time(times):
    codes = []
    for t in times:
        s = ""
        for _ in range(10):
            s = CROCKFORD[t % 32] + s
            t //= 32
        codes.append(s)
    same = [c for _, c in sorted(zip(times, codes))] == sorted(codes)
    return (codes, same)


@O
def ulid_time(times):
    codes = ["".join(CROCKFORD[(t >> (5 * i)) & 31] for i in range(9, -1, -1)) for t in times]
    return (codes, sorted(codes) == [c for _, c in sorted(zip(times, codes))])


Q(None, "When Do Random IDs Collide?", "Medium", "The birthday paradox",
  "With ids of <code>bits</code> random bits, the chance of any collision among n ids ≈ 1 − e^(−n² / 2^(bits+1)). Return it (rounded to 4) for each n.",
  [(([1000, 100_000, 1_000_000, 100_000_000], 40), [0.0, 0.0045, 0.3654, 1.0]), (([1_000_000_000], 122), [0.0])],
  ("A loop.", "O(n)", "O(n)"),
  ("<code>math.expm1</code> for accuracy with tiny values.", "O(n)", "O(n)"),
  viz=(([1000], 32)))


@B
def birthday(ns, bits):
    out = []
    for n in ns:
        out.append(round(1 - math.exp(-n * n / 2 ** (bits + 1)), 4))
    return out


@O
def birthday(ns, bits):
    return [round(-math.expm1(-n * n / 2 ** (bits + 1)), 4) for n in ns]


Q(None, "A Bloom Filter for Taken Codes", "Medium", "Maybe yes, definitely no",
  "Insert <code>taken</code> codes into a Bloom filter of <code>m</code> bits using k hash functions <code>crc32(f'{i}:{code}') % m</code>. For each query return True ('maybe taken') or False ('definitely free'). False positives are possible; false negatives aren't.",
  [((["abc", "xyz", "q1w2", "zz9"], 32, 3, ["abc", "zz9", "new1", "hello", "q1w2", "free7"]), [True, True, False, False, True, False])],
  ("A list of booleans.", "O((t + q) · k)", "O(m)"),
  ("An integer used as a bit set.", "O((t + q) · k)", "O(m)"),
  viz=((["a"], 16, 2, ["a", "b"])))


@B
def bloom(taken, m, k, queries):
    bits = [False] * m
    for c in taken:
        for i in range(k):
            bits[zlib.crc32(f"{i}:{c}".encode()) % m] = True
    out = []
    for q in queries:
        maybe = True
        for i in range(k):
            if not bits[zlib.crc32(f"{i}:{q}".encode()) % m]:
                maybe = False
        out.append(maybe)
    return out


@O
def bloom(taken, m, k, queries):
    def positions(s):
        return [zlib.crc32(f"{i}:{s}".encode()) % m for i in range(k)]
    mask = 0
    for c in taken:
        for p in positions(c):
            mask |= 1 << p
    return [all(mask >> p & 1 for p in positions(q)) for q in queries]


RESERVED = {"api", "admin", "login", "help"}


Q(None, "Validate Custom Aliases", "Easy", "User-chosen short links",
  "An alias must be 4–20 characters of letters, digits or '-', not in <code>RESERVED</code> (case-insensitive) and not already in <code>taken</code>. Return 'ok', 'invalid', 'reserved' or 'taken' for each.",
  [((["my-shop", "ab", "Admin", "sale_2025", "promo", "summer-sale"], {"promo"}), ['ok', 'invalid', 'reserved', 'invalid', 'taken', 'ok'])],
  ("Check characters one by one.", "O(n · L)", "O(1)"),
  ("A regular expression.", "O(n · L)", "O(1)"),
  viz=((["ab", "good1"], set())))


@B
def aliases(requests, taken):
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
    out = []
    for a in requests:
        if not (4 <= len(a) <= 20) or any(ch not in allowed for ch in a):
            out.append("invalid")
        elif a.lower() in RESERVED:
            out.append("reserved")
        elif a in taken:
            out.append("taken")
        else:
            out.append("ok")
    return out


@O
def aliases(requests, taken):
    pattern = re.compile(r"[A-Za-z0-9-]{4,20}")
    return ["invalid" if not pattern.fullmatch(a) else "reserved" if a.lower() in RESERVED
            else "taken" if a in taken else "ok" for a in requests]


Q(None, "Expire Old Links", "Easy", "TTL cleanup",
  "Links are <code>(code, created_day, ttl_days or None)</code>. On day <code>today</code>, return the expired codes (a link with ttl t expires on day created + t).",
  [(([("a1", 0, 30), ("b2", 10, 7), ("c3", 5, None), ("d4", 20, 30), ("e5", 1, 49)], 50), ['a1', 'b2', 'd4', 'e5'])],
  ("A loop.", "O(n)", "O(n)"),
  ("A comprehension.", "O(n)", "O(n)"),
  viz=(([("a", 0, 1)], 2)))


@B
def expired(links, today):
    out = []
    for code, created, ttl in links:
        if ttl is not None and created + ttl <= today:
            out.append(code)
    return out


@O
def expired(links, today):
    return [c for c, d, ttl in links if ttl is not None and d + ttl <= today]


Q(None, "Click Analytics", "Easy", "Aggregate redirect events",
  "Clicks are <code>(code, country)</code>. Return, per code (sorted), the total clicks and the top country (ties: alphabetical).",
  [(([("x1", "IN"), ("x1", "US"), ("x2", "DE"), ("x1", "IN"), ("x2", "DE"), ("x2", "FR"), ("x1", "US"), ("x3", "IN")],), [('x1', 4, 'IN'), ('x2', 3, 'DE'), ('x3', 1, 'IN')])],
  ("Nested dicts of counts.", "O(n + c log c)", "O(n)"),
  ("<code>defaultdict(Counter)</code>.", "O(n + c log c)", "O(n)"),
  viz=(([("a", "IN")],)))


@B
def click_stats(clicks):
    per = {}
    for code, country in clicks:
        per.setdefault(code, {})
        per[code][country] = per[code].get(country, 0) + 1
    out = []
    for code in sorted(per):
        counts = per[code]
        top = sorted(counts, key=lambda c: (-counts[c], c))[0]
        out.append((code, sum(counts.values()), top))
    return out


@O
def click_stats(clicks):
    per = defaultdict(Counter)
    for code, country in clicks:
        per[code][country] += 1
    return [(code, sum(c.values()), min(c, key=lambda k: (-c[k], k))) for code, c in sorted(per.items())]


Q(None, "Canonicalise URLs Before Shortening", "Medium", "One long URL, one code",
  "Lower-case the scheme and host, drop default ports (:80 for http, :443 for https), drop the #fragment, use '/' for an empty path, and sort query parameters. Return the canonical URLs and how many distinct ones there are.",
  [((["HTTPS://Example.com:443/a?b=2&a=1#top", "https://example.com/a?a=1&b=2", "http://example.com:80", "http://EXAMPLE.com/", "https://example.com:8443/a"],), (['https://example.com/a?a=1&b=2', 'https://example.com/a?a=1&b=2', 'http://example.com/', 'http://example.com/', 'https://example.com:8443/a'], 3))],
  ("String splitting by hand.", "O(n · L)", "O(n)"),
  ("<code>urlsplit</code> / <code>urlunsplit</code>.", "O(n · L)", "O(n)"),
  viz=((["HTTP://A.com:80/x#f"],)))


@B
def canonical(urls):
    out = []
    for u in urls:
        u = u.split("#")[0]
        scheme, rest = u.split("://", 1)
        scheme = scheme.lower()
        if "?" in rest:
            rest, query = rest.split("?", 1)
        else:
            query = ""
        if "/" in rest:
            host, path = rest.split("/", 1)
            path = "/" + path
        else:
            host, path = rest, "/"
        host = host.lower()
        if (scheme == "http" and host.endswith(":80")) or (scheme == "https" and host.endswith(":443")):
            host = host.rsplit(":", 1)[0]
        params = sorted(query.split("&")) if query else []
        out.append(f"{scheme}://{host}{path}" + ("?" + "&".join(params) if params else ""))
    return (out, len(set(out)))


@O
def canonical(urls):
    def canon(u):
        p = urlsplit(u)
        scheme, host = p.scheme.lower(), p.hostname
        port = f":{p.port}" if p.port and p.port != {"http": 80, "https": 443}[scheme] else ""
        query = urlencode(sorted(parse_qsl(p.query)))
        return urlunsplit((scheme, host + port, p.path or "/", query, ""))
    out = [canon(u) for u in urls]
    return (out, len(set(out)))


Q(None, "Napkin Maths for a Shortener", "Easy", "Size the system",
  "Given new links per day, the read:write ratio, years kept and bytes per record, return <code>(write QPS, read QPS, storage in TB)</code>, rounded to 1.",
  [((100_000_000, 100, 5, 500), (1157.4, 115740.7, 91.2))],
  ("Step-by-step arithmetic.", "O(1)", "O(1)"),
  ("Same, compact.", "O(1)", "O(1)"),
  viz=((1_000_000, 10, 1, 500)))


@B
def shortener_math(per_day, ratio, years, record_bytes):
    seconds = 24 * 60 * 60
    writes = per_day / seconds
    reads = writes * ratio
    records = per_day * 365 * years
    tb = records * record_bytes / 10 ** 12
    return (round(writes, 1), round(reads, 1), round(tb, 1))


@O
def shortener_math(per_day, ratio, years, record_bytes):
    w = per_day / 86400
    return (round(w, 1), round(w * ratio, 1), round(per_day * 365 * years * record_bytes / 1e12, 1))


Q(None, "Machine IDs Across Data Centres", "Easy", "Pack and check the worker bits",
  "Snowflake's 10 machine bits are often 5 bits of data centre + 5 bits of worker. Return the machine id <code>dc &lt;&lt; 5 | worker</code> for each <code>(dc, worker)</code> (or 'out of range' if either is ≥ 32), and the machine ids that appear more than once.",
  [(([(0, 1), (1, 1), (3, 31), (1, 1), (32, 0), (2, 40)],), ([1, 33, 127, 33, 'out of range', 'out of range'], [33]))],
  ("Compute, then count duplicates with a list.", "O(n²)", "O(n)"),
  ("A comprehension and a Counter.", "O(n)", "O(n)"),
  viz=(([(1, 2)],)))


@B
def machine_ids(pairs):
    ids = []
    for dc, w in pairs:
        if dc >= 32 or w >= 32:
            ids.append("out of range")
        else:
            ids.append(dc * 32 + w)
    dupes = []
    for i in ids:
        if i != "out of range" and ids.count(i) > 1 and i not in dupes:
            dupes.append(i)
    return (ids, sorted(dupes))


@O
def machine_ids(pairs):
    ids = ["out of range" if dc >= 32 or w >= 32 else dc << 5 | w for dc, w in pairs]
    c = Counter(i for i in ids if i != "out of range")
    return (ids, sorted(i for i, n in c.items() if n > 1))


Q(None, "Sequential IDs Leak Your Numbers", "Easy", "Why public IDs should be random",
  "A competitor creates an order on several days and notes its id. With sequential ids, the difference between consecutive observations reveals orders per day. Observations are <code>(day, id)</code>; return the average orders per day between each pair (rounded to 1).",
  [(([(1, 10_500), (8, 24_500), (15, 45_500), (16, 49_000)],), [2000.0, 3000.0, 3500.0])],
  ("Loop over neighbours.", "O(n)", "O(n)"),
  ("<code>zip</code> over neighbours.", "O(n)", "O(n)"),
  viz=(([(1, 10), (2, 30)],)))


@B
def id_leak(observations):
    out = []
    for i in range(1, len(observations)):
        d0, id0 = observations[i - 1]
        d1, id1 = observations[i]
        out.append(round((id1 - id0) / (d1 - d0), 1))
    return out


@O
def id_leak(observations):
    return [round((b - a) / (e - d), 1) for (d, a), (e, b) in zip(observations, observations[1:])]
