from lib import *
import json
import re
import zlib


TOPIC(
    id="shipping", title="Shipping AI Products: Streaming, Coding Agents & Guardrails", glyph="🚀",
    blurb="Turn a prototype into a product: streaming responses and tool input, structured output and repair, retries and fallbacks, coding-agent tools (edits, diffs, the test-fix loop), sandboxing and computer use, semantic caching, budgets, guardrails, prompt versioning and cost planning.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">with client.messages.stream(model="claude-opus-5-5", max_tokens=1024, messages=msgs) as stream:
    for text in stream.text_stream:
        send_to_browser(text)                      # server-sent events to the UI
# retry 429 / 500 / 529 with backoff (honour retry-after); don't retry 400s
# edits: replace a UNIQUE old string; run tests after every change; stop after N failed attempts
# guardrails: validate input → call model → validate output → log</code></pre>
""")

SSE = ('event: message_start\ndata: {"type": "message_start"}\n\n'
       'event: content_block_delta\ndata: {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "Hel"}}\n\n'
       'event: content_block_delta\ndata: {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "lo!"}}\n\n'
       'event: message_stop\ndata: {"type": "message_stop"}\n\n')


Q(None, "Parse a Server-Sent Event Stream", "Medium", "SSE",
  "Streaming APIs send events as blocks separated by a blank line, each with <code>event:</code> and <code>data:</code> lines. Return <code>[(event name, parsed data)]</code>.",
  [((SSE,), [('message_start', {'type': 'message_start'}), ('content_block_delta', {'type': 'content_block_delta', 'index': 0, 'delta': {'type': 'text_delta', 'text': 'Hel'}}), ('content_block_delta', {'type': 'content_block_delta', 'index': 0, 'delta': {'type': 'text_delta', 'text': 'lo!'}}), ('message_stop', {'type': 'message_stop'})])],
  ("Split into blocks, then lines, by hand.", "O(n)", "O(n)"),
  ("A regex over each block.", "O(n)", "O(n)"),
  viz=((SSE,)))


@B
def parse_sse(stream):
    out = []
    for block in stream.split("\n\n"):
        if not block.strip():
            continue
        event, data = None, None
        for line in block.split("\n"):
            if line.startswith("event: "):
                event = line[len("event: "):]
            elif line.startswith("data: "):
                data = json.loads(line[len("data: "):])
        out.append((event, data))
    return out


@O
def parse_sse(stream):
    return [(m[1], json.loads(m[2])) for m in re.finditer(r"event: (.+)\ndata: (.+)", stream)]


Q(None, "Assemble Streamed Text", "Easy", "Text deltas",
  "From parsed stream events, join the <code>text_delta</code> pieces in order, stopping at <code>message_stop</code>. This is what the UI shows as it arrives.",
  [(([("content_block_delta", {"delta": {"type": "text_delta", "text": "Hel"}}), ("ping", {}),
      ("content_block_delta", {"delta": {"type": "text_delta", "text": "lo!"}}), ("message_stop", {}),
      ("content_block_delta", {"delta": {"type": "text_delta", "text": " ignored"}})],), 'Hello!')],
  ("A loop with a break.", "O(n)", "O(n)"),
  ("<code>itertools.takewhile</code> then a join.", "O(n)", "O(n)"),
  viz=([("content_block_delta", {"delta": {"type": "text_delta", "text": "Hel"}}), ("message_stop", {})],))


@B
def assemble_text(events):
    text = ""
    for name, data in events:
        if name == "message_stop":
            break
        if name == "content_block_delta" and data["delta"]["type"] == "text_delta":
            text += data["delta"]["text"]
    return text


@O
def assemble_text(events):
    from itertools import takewhile
    live = takewhile(lambda e: e[0] != "message_stop", events)
    return "".join(d["delta"]["text"] for n, d in live if n == "content_block_delta" and d["delta"]["type"] == "text_delta")


Q(None, "Stream a Tool Call's Arguments", "Medium", "Partial JSON",
  "When a model streams a tool call, the arguments arrive as <code>input_json_delta</code> fragments of a JSON string. Concatenate the fragments per content-block index and parse each once its block stops. Return <code>{index: parsed input}</code>.",
  [(([("delta", 1, '{"city": "Pu'), ("delta", 1, 'ne", "da'), ("delta", 2, '{"q": "mcp"}'), ("delta", 1, 'ys": 3}'), ("stop", 2, None), ("stop", 1, None)],), {1: {'city': 'Pune', 'days': 3}, 2: {'q': 'mcp'}})],
  ("A dict of strings appended in a loop.", "O(n)", "O(n)"),
  ("<code>defaultdict(list)</code> and one join per block.", "O(n)", "O(n)"),
  viz=([("delta", 1, '{"city": "Pu'), ("delta", 1, 'ne"}'), ("stop", 1, None)],))


@B
def stream_tool_input(events):
    buf, done = {}, {}
    for kind, idx, frag in events:
        if kind == "delta":
            buf[idx] = buf.get(idx, "") + frag
        else:
            done[idx] = json.loads(buf[idx])
    return dict(sorted(done.items()))


@O
def stream_tool_input(events):
    from collections import defaultdict
    parts = defaultdict(list)
    done = {}
    for kind, idx, frag in events:
        if kind == "delta":
            parts[idx].append(frag)
        else:
            done[idx] = json.loads("".join(parts[idx]))
    return dict(sorted(done.items()))


Q(None, "Measure Streaming Speed", "Easy", "TTFT and tokens/s",
  "Given the request time and the arrival time of each streamed token (seconds), return <code>(time to first token, tokens per second after the first, total time)</code> rounded to 2.",
  [((10.0, [10.8, 10.85, 10.9, 10.95, 11.0, 11.05, 11.1]), (0.8, 20.0, 1.1))],
  ("Differences by hand.", "O(1)", "O(1)"),
  ("The same with indexing.", "O(1)", "O(1)"),
  viz=(10.0, [10.8, 10.85, 10.9, 10.95]))


@B
def stream_speed(start, times):
    ttft = times[0] - start
    rate = (len(times) - 1) / (times[-1] - times[0])
    return (round(ttft, 2), round(rate, 2), round(times[-1] - start, 2))


@O
def stream_speed(start, t):
    return (round(t[0] - start, 2), round((len(t) - 1) / (t[-1] - t[0]), 2), round(t[-1] - start, 2))


Q(None, "Rescue JSON From a Reply", "Medium", "Structured output",
  "Models sometimes wrap JSON in prose or ```json fences. Return the parsed object, or <code>{'error': 'no valid JSON'}</code>. (Prefer the API's structured-output or tool-use features; keep a parser like this as a safety net.)",
  [(('Here you go:\n```json\n{"name": "Asha", "plan": "pro"}\n```',), {'name': 'Asha', 'plan': 'pro'}), (('{"ok": true}',), {'ok': True}), (("Sorry, I can't.",), {'error': 'no valid JSON'})],
  ("Strip fences by hand, then look for braces.", "O(n)", "O(n)"),
  ("Try a fenced block first, then the outermost braces.", "O(n)", "O(n)"),
  viz=(('```json\n{"name": "Asha"}\n```',)))


@B
def rescue_json(text):
    t = text
    if "```" in t:
        start = t.find("```")
        end = t.find("```", start + 3)
        t = t[start + 3:end]
        if t.startswith("json"):
            t = t[4:]
    a, b = t.find("{"), t.rfind("}")
    if a == -1 or b < a:
        return {"error": "no valid JSON"}
    try:
        return json.loads(t[a:b + 1])
    except ValueError:
        return {"error": "no valid JSON"}


@O
def rescue_json(text):
    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    body = fenced.group(1) if fenced else text
    m = re.search(r"\{.*\}", body, re.S)
    try:
        return json.loads(m.group()) if m else {"error": "no valid JSON"}
    except json.JSONDecodeError:
        return {"error": "no valid JSON"}


Q(None, "What to Do About an API Error", "Easy", "Retry policy",
  "Return the action for each HTTP status: 'retry' for 429, 500, 502, 503, 504 and 529 (overloaded); 'fix request' for other 4xx; 'ok' for 2xx. Then the wait before attempt n (from 0) is the <code>retry-after</code> header if given, else min(30, 2ⁿ). Return <code>(actions, waits for the retried ones in order)</code>.",
  [(([(200, None), (429, 12), (529, None), (400, None), (503, None)],), (['ok', 'retry', 'retry', 'fix request', 'retry'], [12, 2, 4]))],
  ("If-chains and a retry counter.", "O(n)", "O(n)"),
  ("A set of retryable codes and a counter.", "O(n)", "O(n)"),
  viz=([(429, 12), (529, None), (400, None)],))


@B
def error_policy(responses):
    actions, waits, n = [], [], 0
    for code, retry_after in responses:
        if code in (429, 500, 502, 503, 504, 529):
            actions.append("retry")
            waits.append(retry_after if retry_after is not None else min(30, 2 ** n))
            n += 1
        elif 400 <= code < 500:
            actions.append("fix request")
        else:
            actions.append("ok")
    return (actions, waits)


@O
def error_policy(responses):
    retryable = {429, 500, 502, 503, 504, 529}
    actions, waits = [], []
    for code, after in responses:
        action = "retry" if code in retryable else "fix request" if 400 <= code < 500 else "ok"
        if action == "retry":
            waits.append(after if after is not None else min(30, 2 ** len(waits)))
        actions.append(action)
    return (actions, waits)


Q(None, "A Safe Edit Tool", "Medium", "Unique string replacement",
  "Coding agents edit files by replacing an exact <code>old</code> string with <code>new</code>. Refuse if <code>old</code> appears 0 times ('not found') or more than once ('not unique: N matches') — ambiguous edits corrupt code. Return the new text or the error.",
  [(("def add(a, b):\n    return a - b\n", "return a - b", "return a + b"), 'def add(a, b):\n    return a + b\n'), (("x = 1\nx = 1\n", "x = 1", "x = 2"), 'not unique: 2 matches'), (("pass\n", "return", "x"), 'not found')],
  ("Count occurrences with a sliding loop.", "O(n·m)", "O(n)"),
  ("<code>str.count</code> and <code>str.replace(old, new, 1)</code>.", "O(n)", "O(n)"),
  viz=(("def add(a, b):\n    return a - b\n", "return a - b", "return a + b")))


@B
def safe_edit(text, old, new):
    count, i = 0, 0
    while True:
        j = text.find(old, i)
        if j == -1:
            break
        count += 1
        i = j + 1
    if count == 0:
        return "not found"
    if count > 1:
        return "not unique: " + str(count) + " matches"
    k = text.find(old)
    return text[:k] + new + text[k + len(old):]


@O
def safe_edit(text, old, new):
    n = text.count(old)
    return text.replace(old, new, 1) if n == 1 else "not found" if n == 0 else f"not unique: {n} matches"


Q(None, "Apply a Diff Hunk", "Medium", "Patches",
  "Apply a simple diff to a file's lines: hunk lines starting with ' ' must match the file (context), '-' lines are removed (and must match), '+' lines are added. The hunk starts at line <code>start</code> (1-based). Return the new lines, or 'conflict' if anything doesn't match.",
  [((["a", "b", "c", "d"], 2, [" b", "-c", "+C", "+c2", " d"]), ['a', 'b', 'C', 'c2', 'd']), ((["a", "b", "x", "d"], 2, [" b", "-c", "+C"]), 'conflict')],
  ("Walk the hunk with a file pointer.", "O(n)", "O(n)"),
  ("Same walk, splitting each hunk line into its marker and text.", "O(n)", "O(n)"),
  viz=((["a", "b", "c", "d"], 2, [" b", "-c", "+C", " d"])))


@B
def apply_hunk(lines, start, hunk):
    out = lines[:start - 1]
    i = start - 1
    for h in hunk:
        tag, text = h[0], h[1:]
        if tag == "+":
            out.append(text)
        else:
            if i >= len(lines) or lines[i] != text:
                return "conflict"
            if tag == " ":
                out.append(text)
            i += 1
    return out + lines[i:]


@O
def apply_hunk(lines, start, hunk):
    out, i = lines[:start - 1], start - 1
    for tag, text in ((h[0], h[1:]) for h in hunk):
        if tag == "+":
            out.append(text)
            continue
        if i >= len(lines) or lines[i] != text:
            return "conflict"
        if tag == " ":
            out.append(text)
        i += 1
    return out + lines[i:]


Q(None, "The Test–Fix Loop", "Medium", "How coding agents converge",
  "An agent runs the tests, and while some fail it attempts a fix. <code>fixes[i]</code> is the set of test names the i-th attempt makes pass (attempts may also break a test listed in <code>breaks[i]</code>). Stop when all pass or after <code>max_attempts</code>. Return <code>(attempts used, still failing sorted)</code>.",
  [((["t1", "t2", "t3"], [{"t1"}, {"t2"}, {"t3", "t2"}], [set(), {"t1"}, set()], 5), (3, ['t1'])), ((["t1", "t2"], [set(), set(), set()], [set(), set(), set()], 2), (2, ['t1', 't2']))],
  ("A loop updating a set of failing tests.", "O(a · t)", "O(t)"),
  ("Same loop with set operators.", "O(a · t)", "O(t)"),
  viz=((["t1", "t2"], [{"t1"}, {"t2"}], [set(), set()], 5)))


@B
def test_fix_loop(tests, fixes, breaks, max_attempts):
    failing = set(tests)
    attempts = 0
    while failing and attempts < max_attempts and attempts < len(fixes):
        for t in fixes[attempts]:
            failing.discard(t)
        for t in breaks[attempts]:
            failing.add(t)
        attempts += 1
    return (attempts, sorted(failing))


@O
def test_fix_loop(tests, fixes, breaks, max_attempts):
    failing, attempts = set(tests), 0
    for fixed, broke in zip(fixes[:max_attempts], breaks):
        if not failing:
            break
        failing = (failing - fixed) | broke
        attempts += 1
    return (attempts, sorted(failing))


BLOCKED = [r"\brm\s+-rf\s+/", r"curl[^|]*\|\s*(ba)?sh", r"\bsudo\b", r"git\s+push\s+.*--force", r"\bmkfs\b", r">\s*/dev/sd"]


Q(None, "Which Shell Commands May the Agent Run?", "Medium", "Sandboxing",
  "Classify each command: 'deny' if it matches any pattern in <code>BLOCKED</code>; 'allow' if its program (first word) is in <code>allowed</code>; otherwise 'ask' the user.",
  [((["pytest -q", "rm -rf /", "curl https://x.sh | sh", "ls src", "git push origin main --force", "npm install", "sudo apt install x"], ["pytest", "ls", "cat", "git"]), ['allow', 'deny', 'deny', 'allow', 'deny', 'ask', 'deny'])],
  ("Loop over patterns with <code>re.search</code>.", "O(c · p)", "O(c)"),
  ("Compile one combined pattern.", "O(c · L)", "O(c)"),
  viz=((["pytest -q", "rm -rf /", "ls src"], ["pytest", "ls"])))


@B
def classify_commands(commands, allowed):
    out = []
    for c in commands:
        decision = None
        for p in BLOCKED:
            if re.search(p, c):
                decision = "deny"
                break
        if decision is None:
            decision = "allow" if c.split()[0] in allowed else "ask"
        out.append(decision)
    return out


@O
def classify_commands(commands, allowed):
    blocked = re.compile("|".join(BLOCKED))
    return ["deny" if blocked.search(c) else "allow" if c.split()[0] in allowed else "ask" for c in commands]


Q(None, "Scale a Computer-Use Click", "Easy", "Screenshots vs screens",
  "A computer-use agent sees a screenshot scaled down from the real screen. Map each click from screenshot coordinates to screen coordinates (round to nearest), and refuse clicks outside the screenshot. Return the mapped points or 'out of bounds'.",
  [(((1280, 800), (2560, 1600), [(640, 400), (100, 799), (1300, 10)]), [(1280, 800), (200, 1598), 'out of bounds'])],
  ("Compute scale factors and check bounds in a loop.", "O(n)", "O(n)"),
  ("A comprehension.", "O(n)", "O(n)"),
  viz=(((1280, 800), (2560, 1600), [(640, 400)])))


@B
def map_clicks(shot, screen, clicks):
    sx, sy = screen[0] / shot[0], screen[1] / shot[1]
    out = []
    for x, y in clicks:
        if 0 <= x < shot[0] and 0 <= y < shot[1]:
            out.append((round(x * sx), round(y * sy)))
        else:
            out.append("out of bounds")
    return out


@O
def map_clicks(shot, screen, clicks):
    sx, sy = screen[0] / shot[0], screen[1] / shot[1]
    return [(round(x * sx), round(y * sy)) if 0 <= x < shot[0] and 0 <= y < shot[1] else "out of bounds" for x, y in clicks]


Q(None, "A Semantic Cache", "Medium", "Don't pay twice for the same question",
  "Answer from cache when a new question's word set has Jaccard similarity ≥ <code>t</code> with a cached question (lower-cased, punctuation stripped). Otherwise call the model and cache it. Return <code>(hits, calls)</code> for the stream of questions. (Production caches use embeddings and expire entries.)",
  [((["What is your refund policy?", "what's the refund policy", "Refund policy?", "How do I reset my password?", "What is your refund policy"], 0.5), (2, 3))],
  ("Loop over the cache for each question.", "O(n²)", "O(n)"),
  ("A helper for word sets; <code>any</code> for the lookup.", "O(n²)", "O(n)"),
  viz=(["What is your refund policy?", "Refund policy?"], 0.5))


@B
def semantic_cache(questions, t):
    cache, hits, calls = [], 0, 0
    for q in questions:
        words = set(re.sub(r"[^\w\s]", "", q.lower()).split())
        hit = False
        for c in cache:
            if len(words & c) / len(words | c) >= t:
                hit = True
                break
        if hit:
            hits += 1
        else:
            calls += 1
            cache.append(words)
    return (hits, calls)


@O
def semantic_cache(questions, t):
    words = lambda q: set(re.sub(r"[^\w\s]", "", q.lower()).split())
    cache, hits = [], 0
    for q in map(words, questions):
        if any(len(q & c) / len(q | c) >= t for c in cache):
            hits += 1
        else:
            cache.append(q)
    return (hits, len(cache))


Q(None, "A Daily Budget per User", "Easy", "Cost guards",
  "Each user may use <code>limit</code> tokens per day. Requests are <code>(user, day, tokens)</code>; accept if it fits in that user's remaining budget for that day. Return 'ok' / 'over budget' per request.",
  [(([("u1", 1, 3000), ("u1", 1, 4000), ("u2", 1, 9000), ("u1", 1, 2500), ("u1", 2, 9000), ("u2", 1, 1500)], 8000), ['ok', 'ok', 'over budget', 'over budget', 'over budget', 'ok'])],
  ("A dict keyed by (user, day).", "O(n)", "O(u·d)"),
  ("Same with <code>defaultdict(int)</code>.", "O(n)", "O(u·d)"),
  viz=([("u1", 1, 3000), ("u1", 1, 6000)], 8000))


@B
def budget_guard(requests, limit):
    used, out = {}, []
    for user, day, tokens in requests:
        key = (user, day)
        if used.get(key, 0) + tokens <= limit:
            used[key] = used.get(key, 0) + tokens
            out.append("ok")
        else:
            out.append("over budget")
    return out


@O
def budget_guard(requests, limit):
    from collections import defaultdict
    used, out = defaultdict(int), []
    for user, day, tokens in requests:
        ok = used[(user, day)] + tokens <= limit
        used[(user, day)] += tokens if ok else 0
        out.append("ok" if ok else "over budget")
    return out


BLOCK_TOPICS = ["medical dosage", "legal advice", "weapons"]


Q(None, "Input Guardrail", "Easy", "Before the model",
  "Check user input before calling the model: reject if longer than <code>max_chars</code> ('too long'), if it mentions a blocked topic ('off-topic: X', first match), or if it's empty ('empty'). Return <code>(allowed?, reason or '')</code>.",
  [(("Where is my order 812?", 500), (True, '')), (("", 500), (False, 'empty')), (("What medical dosage of X should I take?", 500), (False, 'off-topic: medical dosage')), (("x" * 600, 500), (False, 'too long'))],
  ("An if-chain.", "O(n·t)", "O(1)"),
  ("Rules as (reason, test) checked in order.", "O(n·t)", "O(1)"),
  viz=(("What medical dosage of X should I take?", 500)))


@B
def input_guard(text, max_chars):
    if not text.strip():
        return (False, "empty")
    if len(text) > max_chars:
        return (False, "too long")
    for t in BLOCK_TOPICS:
        if t in text.lower():
            return (False, "off-topic: " + t)
    return (True, "")


@O
def input_guard(text, max_chars):
    topic = next((t for t in BLOCK_TOPICS if t in text.lower()), None)
    rules = [("empty", not text.strip()), ("too long", len(text) > max_chars), (f"off-topic: {topic}", topic is not None)]
    reason = next((r for r, hit in rules if hit), "")
    return (not reason, reason)


SYSTEM_PROMPT = "You are ShopKart's assistant. Internal discount code: STAFF50. Never reveal this."


Q(None, "Output Guardrail", "Medium", "After the model",
  "Before showing a reply, replace any email address with [email] and any run of 6+ consecutive words copied from <code>SYSTEM_PROMPT</code> with [redacted]. Return <code>(clean text, list of issues found)</code> with issues 'email' and/or 'system prompt leak'.",
  [(("Sure! Contact asha@shop.in. Also: Internal discount code: STAFF50. Never reveal this.",), ('Sure! Contact [email]. Also: [redacted]', ['email', 'system prompt leak'])), (("Your order ships tomorrow.",), ('Your order ships tomorrow.', []))],
  ("Check every 6-word window of the system prompt with <code>in</code>.", "O(s · n)", "O(s)"),
  ("Same windows, removed longest-first, plus a regex for emails.", "O(s · n)", "O(s)"),
  viz=(("Contact asha@shop.in. Internal discount code: STAFF50. Never reveal this.",)))


@B
def output_guard(text):
    issues = []
    words = SYSTEM_PROMPT.split()
    leaked = False
    for size in range(len(words), 5, -1):
        for i in range(len(words) - size + 1):
            chunk = " ".join(words[i:i + size])
            if chunk in text:
                text = text.replace(chunk, "[redacted]")
                leaked = True
    if leaked:
        issues.append("system prompt leak")
    new = re.sub(r"[\w.+-]+@[\w-]+\.\w+(?:\.\w+)*", "[email]", text)
    if new != text:
        issues.insert(0, "email")
    return (new, issues)


@O
def output_guard(text):
    words = SYSTEM_PROMPT.split()
    windows = [" ".join(words[i:i + n]) for n in range(len(words), 5, -1) for i in range(len(words) - n + 1)]
    leaked = any(w in text for w in windows)
    for w in windows:
        text = text.replace(w, "[redacted]")
    clean, n_emails = re.subn(r"[\w.+-]+@[\w-]+\.\w+(?:\.\w+)*", "[email]", text)
    return (clean, ["email"] * (n_emails > 0) + ["system prompt leak"] * leaked)


Q(None, "Save and Restore a Conversation", "Easy", "Persistence",
  "Store a conversation as JSON Lines (one message per line) and load it back. Return <code>(the text, whether the loaded messages equal the originals)</code>.",
  [(([{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello! ✓"}],), ('{"role": "user", "content": "Hi"}\n{"role": "assistant", "content": "Hello! ✓"}\n', True))],
  ("Build lines with <code>json.dumps</code> in a loop.", "O(n)", "O(n)"),
  ("Join and split with comprehensions; <code>ensure_ascii=False</code> keeps text readable.", "O(n)", "O(n)"),
  viz=([{"role": "user", "content": "Hi"}],))


@B
def jsonl_roundtrip(messages):
    text = ""
    for m in messages:
        text += json.dumps(m, ensure_ascii=False) + "\n"
    loaded = []
    for line in text.split("\n"):
        if line:
            loaded.append(json.loads(line))
    return (text, loaded == messages)


@O
def jsonl_roundtrip(messages):
    text = "".join(json.dumps(m, ensure_ascii=False) + "\n" for m in messages)
    return (text, [json.loads(l) for l in text.splitlines()] == messages)


Q(None, "Roll Out a New Prompt Version", "Medium", "Prompt versioning",
  "Prompts are versioned like code. In 'dev', everyone gets the newest version; in 'prod', a user gets the new version if <code>zlib.crc32(user) % 100 &lt; pct</code>, else the stable one. Return each user's version.",
  [((["u1", "u2", "u3", "u4", "u5", "u6"], "prod", "v7", "v6", 50), ['v7', 'v6', 'v7', 'v6', 'v7', 'v7']), ((["u1", "u2"], "dev", "v7", "v6", 0), ['v7', 'v7'])],
  ("A loop with an if.", "O(n)", "O(n)"),
  ("A comprehension.", "O(n)", "O(n)"),
  viz=((["u1", "u2", "u3"], "prod", "v7", "v6", 50)))


@B
def prompt_version(users, env, new, stable, pct):
    out = []
    for u in users:
        if env == "dev":
            out.append(new)
        elif zlib.crc32(u.encode()) % 100 < pct:
            out.append(new)
        else:
            out.append(stable)
    return out


@O
def prompt_version(users, env, new, stable, pct):
    return [new if env == "dev" or zlib.crc32(u.encode()) % 100 < pct else stable for u in users]


Q(None, "What Will This Feature Cost per Month?", "Easy", "Planning",
  "Monthly cost = users × requests per user per day × 30 × (input tokens × in price + output tokens × out price) / 10⁶. With prompt caching, <code>cached_share</code> of input tokens are billed at 10%. Return <code>(monthly $, with caching $, $ per user with caching)</code> rounded to 2.",
  [((5000, 6, 3000, 400, 3.0, 15.0, 0.7), (13500.0, 8397.0, 1.68))],
  ("Step by step.", "O(1)", "O(1)"),
  ("Factor out the per-request cost.", "O(1)", "O(1)"),
  viz=((5000, 6, 3000, 400, 3.0, 15.0, 0.7)))


@B
def monthly_cost(users, per_day, inp, out, pin, pout, cached_share):
    requests = users * per_day * 30
    plain = requests * (inp * pin + out * pout) / 1e6
    cached_input = inp * cached_share * pin * 0.1 + inp * (1 - cached_share) * pin
    cached = requests * (cached_input + out * pout) / 1e6
    return (round(plain, 2), round(cached, 2), round(cached / users, 2))


@O
def monthly_cost(users, per_day, inp, out, pin, pout, cached_share):
    n = users * per_day * 30
    plain = n * (inp * pin + out * pout) / 1e6
    cached = n * (inp * pin * (1 - 0.9 * cached_share) + out * pout) / 1e6
    return (round(plain, 2), round(cached, 2), round(cached / users, 2))


CHECKS = ["evals pass", "guardrails on", "rate limits set", "costs alerted", "traces on", "fallback model", "privacy review"]


Q(None, "Ready to Launch?", "Easy", "Release checklist",
  "Given the checks done, return <code>(ready?, missing checks in CHECKS order)</code>.",
  [((["evals pass", "traces on", "guardrails on", "rate limits set", "costs alerted", "fallback model", "privacy review"],), (True, [])),
   ((["evals pass", "traces on"],), (False, ['guardrails on', 'rate limits set', 'costs alerted', 'fallback model', 'privacy review']))],
  ("A loop over CHECKS.", "O(c)", "O(c)"),
  ("A set for O(1) lookups and a comprehension.", "O(c)", "O(c)"),
  viz=((["evals pass", "traces on"],)))


@B
def launch_ready(done):
    missing = []
    for c in CHECKS:
        if c not in done:
            missing.append(c)
    return (len(missing) == 0, missing)


@O
def launch_ready(done):
    have = set(done)
    missing = [c for c in CHECKS if c not in have]
    return (not missing, missing)


Q(None, "Send Chunks to the Browser", "Easy", "Server-side streaming",
  "Your backend relays model text to the browser as server-sent events: one <code>data: {\"text\": chunk}</code> line plus a blank line per chunk, then <code>data: [DONE]</code>. Skip empty chunks. Return the response body. (In FastAPI, return a <code>StreamingResponse</code> of these strings with media type <code>text/event-stream</code>.)",
  [((["Hel", "", "lo", " ✓"],), 'data: {"text": "Hel"}\n\ndata: {"text": "lo"}\n\ndata: {"text": " ✓"}\n\ndata: [DONE]\n\n')],
  ("String concatenation in a loop.", "O(n)", "O(n)"),
  ("A generator joined once — the same generator can feed a StreamingResponse.", "O(n)", "O(n)"),
  viz=((["Hel", "lo"],)))


@B
def to_sse(chunks):
    body = ""
    for c in chunks:
        if c:
            body += "data: " + json.dumps({"text": c}, ensure_ascii=False) + "\n\n"
    return body + "data: [DONE]\n\n"


@O
def to_sse(chunks):
    def events():
        for c in filter(None, chunks):
            yield f"data: {json.dumps({'text': c}, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"
    return "".join(events())
