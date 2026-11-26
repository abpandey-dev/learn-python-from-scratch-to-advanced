from lib import *
import heapq
import math
import zlib
from collections import Counter, defaultdict
from itertools import islice

TOPIC(
    id="feeds_chat", title="News Feed, Chat & Notifications", glyph="💬",
    blurb="Real-time social systems: fan-out on write vs read, the celebrity problem, merging and ranking timelines, author diversity, chat sequence numbers, unread counts, receipts, presence, routing to connection servers, group fan-out, reconnect sync, typing throttles, notification digests, quiet hours, channels, device tokens and sharded counters.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">fan-out on write (push): post → insert into every follower's feed; fast reads, slow for celebrities
fan-out on read (pull):  read → merge posts of everyone you follow; cheap writes, slow reads
hybrid: push for normal users, pull for accounts with millions of followers
chat ordering: server assigns a per-conversation sequence number; clients sync from their last seq</code></pre>
""")


Q(None, "Push or Pull: Count the Work", "Easy", "Fan-out on write vs read",
  "Each user posts <code>posts[u]</code> times a day and has <code>followers[u]</code> followers. Fan-out on write inserts every post into every follower's feed. Fan-out on read makes each feed read query every followed account. Return <code>(write-time inserts per day, read-time queries per day)</code> given <code>reads</code> feed reads per day and <code>follows</code> accounts followed per reader.",
  [(({"asha": 120, "ravi": 300, "star": 5_000_000}, {"asha": 3, "ravi": 1, "star": 2}, 2_000_000, 150), (10000660, 300000000))],
  ("Loop and add.", "O(u)", "O(1)"),
  ("<code>sum</code> of products.", "O(u)", "O(1)"),
  viz=(({"a": 10}, {"a": 2}, 100, 5)))


@B
def push_vs_pull(followers, posts, reads, follows):
    writes = 0
    for u in followers:
        writes += followers[u] * posts[u]
    return (writes, reads * follows)


@O
def push_vs_pull(followers, posts, reads, follows):
    return (sum(followers[u] * posts[u] for u in followers), reads * follows)


Q(None, "Hybrid Fan-Out for Celebrities", "Medium", "Push most, pull the famous",
  "Accounts with more than <code>limit</code> followers are 'pull' (their posts are merged at read time); the rest are 'push'. Return the sorted pull accounts and the number of feed inserts per day for the push accounts.",
  [(({"asha": 120, "ravi": 300, "star": 5_000_000, "brand": 900_000}, {"asha": 3, "ravi": 1, "star": 2, "brand": 10}, 100_000), (['brand', 'star'], 660))],
  ("Loop with if/else.", "O(u log u)", "O(u)"),
  ("Comprehensions.", "O(u log u)", "O(u)"),
  viz=(({"a": 10, "b": 1000}, {"a": 1, "b": 1}, 100)))


@B
def hybrid_fanout(followers, posts, limit):
    pull, inserts = [], 0
    for u, f in followers.items():
        if f > limit:
            pull.append(u)
        else:
            inserts += f * posts[u]
    return (sorted(pull), inserts)


@O
def hybrid_fanout(followers, posts, limit):
    return (sorted(u for u, f in followers.items() if f > limit),
            sum(f * posts[u] for u, f in followers.items() if f <= limit))


Q(None, "Merge a Pull Timeline", "Medium", "k-way merge",
  "Each followed account's posts are <code>(timestamp, id)</code>, newest first. Return the <code>k</code> newest post ids across the accounts the reader follows.",
  [(({"a": [(50, "a3"), (20, "a2"), (5, "a1")], "b": [(45, "b2"), (44, "b1")], "c": [(60, "c9"), (10, "c1")], "d": [(99, "d1")]}, ["a", "b", "c"], 4), ['c9', 'a3', 'b2', 'b1'])],
  ("Gather all posts and sort.", "O(n log n)", "O(n)"),
  ("<code>heapq.merge(..., reverse=True)</code>, take k.", "O(k log f)", "O(f)"),
  viz=(({"a": [(2, "a2")], "b": [(3, "b1")]}, ["a", "b"], 2)))


@B
def pull_timeline(posts, following, k):
    allp = []
    for u in following:
        allp += posts[u]
    allp.sort(reverse=True)
    return [pid for _, pid in allp[:k]]


@O
def pull_timeline(posts, following, k):
    return [pid for _, pid in islice(heapq.merge(*(posts[u] for u in following), reverse=True), k)]


Q(None, "Rank the Feed", "Easy", "Engagement with time decay",
  "Score each post <code>(id, likes, comments, age_hours)</code> as (likes + 2 × comments) / (age + 2)^1.5 and return ids from highest score.",
  [(([("p1", 100, 10, 1), ("p2", 900, 50, 20), ("p3", 30, 30, 0), ("p4", 5000, 100, 72)],), ['p3', 'p1', 'p2', 'p4'])],
  ("Compute scores into a list, sort it.", "O(n log n)", "O(n)"),
  ("<code>sorted</code> with a key function.", "O(n log n)", "O(n)"),
  viz=(([("a", 10, 1, 1), ("b", 100, 0, 30)],)))


@B
def rank_feed(posts):
    scored = []
    for pid, likes, comments, age in posts:
        scored.append(((likes + 2 * comments) / (age + 2) ** 1.5, pid))
    scored.sort(reverse=True)
    return [pid for _, pid in scored]


@O
def rank_feed(posts):
    return [p[0] for p in sorted(posts, key=lambda p: (p[1] + 2 * p[2]) / (p[3] + 2) ** 1.5, reverse=True)]


Q(None, "Keep the Feed Diverse", "Easy", "Cap posts per author",
  "From a ranked list of <code>(post, author)</code>, keep at most <code>cap</code> posts per author (in ranked order) and return the first <code>n</code> post ids.",
  [(([("p1", "news"), ("p2", "news"), ("p3", "asha"), ("p4", "news"), ("p5", "news"), ("p6", "ravi"), ("p7", "asha")], 2, 5), ['p1', 'p2', 'p3', 'p6', 'p7'])],
  ("Count with a dict in a loop.", "O(p)", "O(a)"),
  ("Counter and early stop.", "O(p)", "O(a)"),
  viz=(([("a", "x"), ("b", "x"), ("c", "x")], 1, 2)))


@B
def diverse(ranked, cap, n):
    counts, out = {}, []
    for pid, author in ranked:
        if counts.get(author, 0) < cap:
            out.append(pid)
            counts[author] = counts.get(author, 0) + 1
    return out[:n]


@O
def diverse(ranked, cap, n):
    counts, out = Counter(), []
    for pid, author in ranked:
        if counts[author] < cap:
            counts[author] += 1
            out.append(pid)
            if len(out) == n:
                break
    return out


Q(None, "Order Chat Messages", "Easy", "Server-assigned sequence numbers",
  "Client clocks can't be trusted, so the chat server gives each conversation its own increasing sequence number as messages arrive. Messages are <code>(conversation, text)</code> in arrival order; return <code>(conversation, seq, text)</code>.",
  [(([("c1", "hi"), ("c2", "yo"), ("c1", "how are you?"), ("c1", "👋"), ("c2", "lunch?")],), [('c1', 1, 'hi'), ('c2', 1, 'yo'), ('c1', 2, 'how are you?'), ('c1', 3, '👋'), ('c2', 2, 'lunch?')])],
  ("Count earlier messages per conversation.", "O(n²)", "O(n)"),
  ("A counter per conversation.", "O(n)", "O(c)"),
  viz=(([("a", "x"), ("a", "y")],)))


@B
def chat_seq(messages):
    out = []
    for i, (c, text) in enumerate(messages):
        seq = 1 + sum(1 for j in range(i) if messages[j][0] == c)
        out.append((c, seq, text))
    return out


@O
def chat_seq(messages):
    nxt, out = Counter(), []
    for c, text in messages:
        nxt[c] += 1
        out.append((c, nxt[c], text))
    return out


Q(None, "Unread Counts", "Easy", "Latest seq minus last read",
  "For each conversation, the latest sequence number is <code>latest[c]</code> and the user's read pointer is <code>read[c]</code> (missing = 0). Return unread per conversation (only non-zero) and the badge total.",
  [(({"c1": 40, "c2": 12, "c3": 7, "c4": 3}, {"c1": 40, "c2": 5, "c4": 1}), ({'c2': 7, 'c3': 7, 'c4': 2}, 16))],
  ("A loop.", "O(c)", "O(c)"),
  ("A dict comprehension.", "O(c)", "O(c)"),
  viz=(({"a": 5}, {"a": 2})))


@B
def unread(latest, read):
    out = {}
    for c, s in latest.items():
        n = s - read.get(c, 0)
        if n > 0:
            out[c] = n
    total = 0
    for n in out.values():
        total += n
    return (out, total)


@O
def unread(latest, read):
    out = {c: s - read.get(c, 0) for c, s in latest.items() if s > read.get(c, 0)}
    return (out, sum(out.values()))


Q(None, "Delivery Receipts", "Easy", "Sent → delivered → read",
  "Receipt events <code>(message, state)</code> may arrive out of order. A message's state only moves forward (sent < delivered < read). Return each message's final state, sorted by message.",
  [(([("m1", "sent"), ("m2", "sent"), ("m1", "read"), ("m1", "delivered"), ("m2", "delivered"), ("m3", "sent"), ("m2", "sent")],), [('m1', 'read'), ('m2', 'delivered'), ('m3', 'sent')])],
  ("Compare ranks with if-statements.", "O(e)", "O(m)"),
  ("<code>max</code> by rank.", "O(e)", "O(m)"),
  viz=(([("a", "read"), ("a", "sent")],)))


@B
def receipts(events):
    rank = {"sent": 0, "delivered": 1, "read": 2}
    state = {}
    for m, s in events:
        if m not in state or rank[s] > rank[state[m]]:
            state[m] = s
    return sorted(state.items())


@O
def receipts(events):
    order = ["sent", "delivered", "read"]
    state = {}
    for m, s in events:
        state[m] = max(state.get(m, "sent"), s, key=order.index)
    return sorted(state.items())


Q(None, "Who Is Online?", "Easy", "Presence from heartbeats",
  "Clients send heartbeats. A user is 'online' if their last heartbeat was within 30 s of <code>now</code>, 'away' within 300 s, else 'offline' (never seen = offline). Return the status of each user in <code>users</code>.",
  [(([("asha", 100), ("ravi", 50), ("asha", 990), ("meera", 800), ("ravi", 700)], 1000, ["asha", "ravi", "meera", "dev"]), ['online', 'away', 'away', 'offline'])],
  ("Find each user's last heartbeat by scanning.", "O(u · h)", "O(1)"),
  ("A dict of last heartbeats.", "O(h + u)", "O(u)"),
  viz=(([("a", 95)], 100, ["a", "b"])))


@B
def presence(beats, now, users):
    out = []
    for u in users:
        last = None
        for name, t in beats:
            if name == u and (last is None or t > last):
                last = t
        if last is not None and now - last <= 30:
            out.append("online")
        elif last is not None and now - last <= 300:
            out.append("away")
        else:
            out.append("offline")
    return out


@O
def presence(beats, now, users):
    last = {}
    for u, t in beats:
        last[u] = max(t, last.get(u, t))
    def status(u):
        gap = now - last.get(u, -math.inf)
        return "online" if gap <= 30 else "away" if gap <= 300 else "offline"
    return [status(u) for u in users]


Q(None, "Route Messages to Connection Servers", "Medium", "Session registry",
  "Online users hold a WebSocket to one chat server (<code>sessions</code>: user → server). For each message <code>(sender, recipient)</code>, deliver it via the recipient's server, or queue a push notification if they're offline. Return <code>(deliveries per server, offline recipients notified, in order)</code>.",
  [(({"asha": "ws-1", "ravi": "ws-2", "meera": "ws-1"}, [("asha", "ravi"), ("ravi", "meera"), ("asha", "dev"), ("meera", "asha"), ("ravi", "dev")]), ({'ws-1': 2, 'ws-2': 1}, ['dev', 'dev']))],
  ("A loop with dict counting.", "O(m)", "O(s)"),
  ("A Counter and a comprehension.", "O(m)", "O(s)"),
  viz=(({"a": "s1"}, [("b", "a"), ("a", "b")])))


@B
def route_messages(sessions, messages):
    per_server, offline = {}, []
    for _, to in messages:
        if to in sessions:
            per_server[sessions[to]] = per_server.get(sessions[to], 0) + 1
        else:
            offline.append(to)
    return (dict(sorted(per_server.items())), offline)


@O
def route_messages(sessions, messages):
    c = Counter(sessions[to] for _, to in messages if to in sessions)
    return (dict(sorted(c.items())), [to for _, to in messages if to not in sessions])


Q(None, "Group Chat Fan-Out", "Easy", "Every member gets a copy",
  "Groups map to member lists. Each message <code>(group, sender)</code> is delivered to every member except the sender. Return the total deliveries and each user's inbox count (sorted).",
  [(({"family": ["asha", "ravi", "meera"], "team": ["asha", "dev", "kim", "lee"]}, [("family", "asha"), ("team", "dev"), ("team", "asha"), ("family", "meera")]), (10, [('asha', 2), ('dev', 1), ('kim', 2), ('lee', 2), ('meera', 1), ('ravi', 2)]))],
  ("Nested loops.", "O(m · g)", "O(u)"),
  ("Counter update per message.", "O(m · g)", "O(u)"),
  viz=(({"g": ["a", "b"]}, [("g", "a")])))


@B
def group_fanout(groups, messages):
    inbox = {}
    for g, sender in messages:
        for m in groups[g]:
            if m != sender:
                inbox[m] = inbox.get(m, 0) + 1
    return (sum(inbox.values()), sorted(inbox.items()))


@O
def group_fanout(groups, messages):
    inbox = Counter(m for g, s in messages for m in groups[g] if m != s)
    return (sum(inbox.values()), sorted(inbox.items()))


Q(None, "How Many WebSocket Servers?", "Easy", "Long-lived connections",
  "Return <code>(servers needed, total memory in GB rounded to 1)</code> for <code>online</code> concurrent users, at most <code>per_server</code> connections per server and <code>kb_each</code> KB of memory per connection.",
  [((10_000_000, 50_000, 64), (200, 610.4)), ((250_000, 100_000, 20), (3, 4.8))],
  ("Count servers in a loop.", "O(s)", "O(1)"),
  ("<code>math.ceil</code>.", "O(1)", "O(1)"),
  viz=((1000, 300, 10)))


@B
def ws_servers(online, per_server, kb_each):
    servers = 0
    while servers * per_server < online:
        servers += 1
    return (servers, round(online * kb_each / 1024 / 1024, 1))


@O
def ws_servers(online, per_server, kb_each):
    return (math.ceil(online / per_server), round(online * kb_each / 2 ** 20, 1))


Q(None, "Sync After Reconnecting", "Medium", "Catch up from the last seq",
  "After reconnecting, a client sends its last seen seq per conversation; the server returns missed messages in pages of <code>page</code> per request. Return <code>(missed per conversation, requests needed)</code> (conversations with nothing missed need no request).",
  [(({"c1": 120, "c2": 45, "c3": 9}, {"c1": 20, "c2": 45, "c3": 0}, 50), ({'c1': 100, 'c2': 0, 'c3': 9}, 3))],
  ("Loop with page counting.", "O(c · p)", "O(c)"),
  ("Ceiling division.", "O(c)", "O(c)"),
  viz=(({"a": 10}, {"a": 3}, 5)))


@B
def reconnect_sync(latest, seen, page):
    missed, requests = {}, 0
    for c in latest:
        m = latest[c] - seen.get(c, 0)
        missed[c] = m
        while m > 0:
            requests += 1
            m -= page
    return (missed, requests)


@O
def reconnect_sync(latest, seen, page):
    missed = {c: s - seen.get(c, 0) for c, s in latest.items()}
    return (missed, sum(math.ceil(m / page) for m in missed.values()))


Q(None, "Throttle the Typing Indicator", "Easy", "At most one event per interval",
  "Keystroke times (ms) would each send a 'typing…' event. Send one only if at least <code>interval</code> ms passed since the last one sent. Return the send times.",
  [(([0, 100, 250, 900, 1000, 1500, 3200, 3300], 1000), [0, 1000, 3200])],
  ("Track the last sent time.", "O(n)", "O(n)"),
  ("Same, one condition.", "O(n)", "O(n)"),
  viz=(([0, 10, 2000], 1000)))


@B
def throttle(times, interval):
    sent = []
    for t in times:
        if not sent or t - sent[-1] >= interval:
            sent.append(t)
    return sent


@O
def throttle(times, interval):
    sent, last = [], -math.inf
    for t in times:
        if t - last >= interval:
            sent.append(t)
            last = t
    return sent


Q(None, "Notification Digests", "Medium", "Don't buzz the phone 30 times",
  "Per user, the first notification sends immediately and opens a window of <code>window</code> s; further notifications inside the window are collapsed into one digest sent when the window ends. Return <code>(user, send_time, count)</code> sorted by user and time.",
  [(([("asha", 0), ("asha", 10), ("asha", 50), ("ravi", 5), ("asha", 70), ("asha", 200), ("ravi", 300)], 60),  [('asha', 0, 1), ('asha', 60, 2), ('asha', 70, 1), ('asha', 200, 1), ('ravi', 5, 1), ('ravi', 300, 1)])],
  ("Group per user, then walk their times.", "O(n log n)", "O(n)"),
  ("Same with <code>defaultdict(list)</code>.", "O(n log n)", "O(n)"),
  viz=(([("a", 0), ("a", 5)], 60)))


@B
def digests(notes, window):
    users = sorted(set(u for u, _ in notes))
    out = []
    for u in users:
        times = sorted(t for x, t in notes if x == u)
        i = 0
        while i < len(times):
            start = times[i]
            out.append((u, start, 1))
            j = i + 1
            while j < len(times) and times[j] < start + window:
                j += 1
            if j - i - 1 > 0:
                out.append((u, start + window, j - i - 1))
            i = j
    return out


@O
def digests(notes, window):
    per = defaultdict(list)
    for u, t in notes:
        per[u].append(t)
    out = []
    for u in sorted(per):
        times, i = sorted(per[u]), 0
        while i < len(times):
            start, j = times[i], i + 1
            while j < len(times) and times[j] < start + window:
                j += 1
            out.append((u, start, 1))
            if j > i + 1:
                out.append((u, start + window, j - i - 1))
            i = j
    return out


Q(None, "Respect Quiet Hours", "Medium", "Time zones matter",
  "Notifications are <code>(user, utc_hour)</code>; <code>tz</code> gives each user's UTC offset in whole hours. Quiet hours are 22:00–07:00 local. Return the UTC hour each notification is delivered (now, or 07:00 local the same/next morning), modulo 24.",
  [(([("asha", 18), ("ravi", 3), ("meera", 12), ("asha", 1)], {"asha": 5, "ravi": -5, "meera": 9}), [2, 12, 12, 2])],
  ("Step forward hour by hour until not quiet.", "O(n · 24)", "O(n)"),
  ("Compute local hour and shift directly.", "O(n)", "O(n)"),
  viz=(([("a", 23)], {"a": 0})))


@B
def quiet_hours(notes, tz):
    out = []
    for u, h in notes:
        local = (h + tz[u]) % 24
        while local >= 22 or local < 7:
            local = (local + 1) % 24
        out.append((local - tz[u]) % 24)
    return out


@O
def quiet_hours(notes, tz):
    def deliver(u, h):
        local = (h + tz[u]) % 24
        return h if 7 <= local < 22 else (7 - tz[u]) % 24
    return [deliver(u, h) for u, h in notes]


Q(None, "Choose Notification Channels", "Easy", "User preferences",
  "Events are <code>(user, type)</code>. Use the user's preference for that type if set, else <code>defaults[type]</code>. Return the channels per event and the total sends per channel (sorted).",
  [(([("asha", "otp"), ("asha", "promo"), ("ravi", "order"), ("ravi", "promo"), ("meera", "otp")], {"asha": {"promo": []}, "ravi": {"order": ["email"]}}, {"otp": ["sms"], "order": ["push", "email"], "promo": ["push"]}), ([['sms'], [], ['email'], ['push'], ['sms']], [('email', 1), ('push', 1), ('sms', 2)]))],
  ("Nested ifs and a counting dict.", "O(e · c)", "O(c)"),
  ("<code>dict.get</code> chains and Counter.", "O(e · c)", "O(c)"),
  viz=(([("a", "otp")], {}, {"otp": ["sms"]})))


@B
def channels(events, prefs, defaults):
    out, totals = [], {}
    for u, t in events:
        if u in prefs and t in prefs[u]:
            ch = prefs[u][t]
        else:
            ch = defaults[t]
        out.append(ch)
        for c in ch:
            totals[c] = totals.get(c, 0) + 1
    return (out, sorted(totals.items()))


@O
def channels(events, prefs, defaults):
    out = [prefs.get(u, {}).get(t, defaults[t]) for u, t in events]
    return (out, sorted(Counter(c for ch in out for c in ch).items()))


Q(None, "Handle Push-Token Responses", "Medium", "Clean up dead devices",
  "Each device token gets responses for successive attempts: 'ok' (delivered), 'invalid' (uninstalled — delete the token) or 'unavailable' (retry). Try at most <code>max_attempts</code>. Return sorted lists <code>(delivered, removed, gave up)</code>.",
  [(({"t1": ["ok"], "t2": ["unavailable", "ok"], "t3": ["invalid"], "t4": ["unavailable", "unavailable", "unavailable", "ok"], "t5": ["unavailable", "invalid"]}, 3), (['t1', 't2'], ['t3', 't5'], ['t4']))],
  ("Loop over attempts per token.", "O(t · a)", "O(t)"),
  ("Find the first final response in the allowed attempts.", "O(t · a)", "O(t)"),
  viz=(({"a": ["ok"], "b": ["invalid"]}, 2)))


@B
def push_tokens(responses, max_attempts):
    delivered, removed, gave_up = [], [], []
    for tok, rs in responses.items():
        result = None
        for i in range(min(max_attempts, len(rs))):
            if rs[i] == "ok":
                result = "ok"
                break
            if rs[i] == "invalid":
                result = "invalid"
                break
        if result == "ok":
            delivered.append(tok)
        elif result == "invalid":
            removed.append(tok)
        else:
            gave_up.append(tok)
    return (sorted(delivered), sorted(removed), sorted(gave_up))


@O
def push_tokens(responses, max_attempts):
    final = {t: next((r for r in rs[:max_attempts] if r != "unavailable"), "gave up") for t, rs in responses.items()}
    return tuple(sorted(t for t, f in final.items() if f == k) for k in ("ok", "invalid", "gave up"))


Q(None, "Sharded Like Counters", "Medium", "Spread a hot counter",
  "One row receiving thousands of likes per second becomes a lock hotspot. Spread increments over <code>n</code> sub-counters by <code>crc32(event_id) % n</code>; a read sums them. Return the sub-counter values and the total.",
  [(([f"like-{i}" for i in range(500)], 3), ([184, 162, 154], 500))],
  ("A list of counters.", "O(e)", "O(n)"),
  ("Counter.", "O(e)", "O(n)"),
  viz=(([f"l{i}" for i in range(6)], 2)))


@B
def sharded_counter(events, n):
    shards = [0] * n
    for e in events:
        shards[zlib.crc32(e.encode()) % n] += 1
    return (shards, sum(shards))


@O
def sharded_counter(events, n):
    c = Counter(zlib.crc32(e.encode()) % n for e in events)
    shards = [c[i] for i in range(n)]
    return (shards, sum(shards))


Q(None, "How Much Chat Storage?", "Easy", "Size the message store",
  "Return <code>(messages per day, write QPS, TB per year)</code> for <code>dau</code> users sending <code>per_user</code> messages a day of <code>bytes_each</code> bytes, stored <code>copies</code> times. Round QPS and TB to 1.",
  [((500_000_000, 40, 200, 3), (20000000000, 231481.5, 4380.0))],
  ("Step-by-step arithmetic.", "O(1)", "O(1)"),
  ("Same, compact.", "O(1)", "O(1)"),
  viz=((1000, 10, 100, 3)))


@B
def chat_storage(dau, per_user, bytes_each, copies):
    per_day = dau * per_user
    qps_ = per_day / (24 * 3600)
    tb = per_day * 365 * bytes_each * copies / 1_000_000_000_000
    return (per_day, round(qps_, 1), round(tb, 1))


@O
def chat_storage(dau, per_user, bytes_each, copies):
    n = dau * per_user
    return (n, round(n / 86400, 1), round(n * 365 * bytes_each * copies / 1e12, 1))
