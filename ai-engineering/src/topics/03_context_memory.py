from lib import *
import re
from collections import deque


TOPIC(
    id="context-memory", title="Context Engineering & Agent Memory", glyph="▤",
    blurb="Decide what the model sees: token budgets, trimming and compaction, ordering for prompt caching, 'lost in the middle', clearing old tool results, just-in-time retrieval, and long-term memory — extracting facts, add/update/skip decisions, recall with recency, and resolving conflicts.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">tokens ≈ len(text) / 4                       # rough English estimate; use the API's token counter for real numbers
order = [system, tools, documents, history, latest question]   # stable first → cacheable prefix
if used &gt; 0.8 * window: compact(history)      # summarise the oldest turns
memory ops: ADD new fact · UPDATE changed fact (keep history) · SKIP duplicate
recall score = relevance × 0.5 ** (age / half_life)</code></pre>
<p>Context engineering = giving the model <b>the smallest set of high-signal tokens</b> that lets it do the task.</p>
""")


def toks(text):
    return (len(text) + 3) // 4


Q(None, "Estimate Tokens", "Easy", "Budgets start with counting",
  "Estimate tokens as ⌈characters ÷ 4⌉ per message. Return <code>(tokens per message, total)</code>.",
  [((["You are a helpful assistant.", "Summarise MCP in one line.", ""],), ([7, 7, 0], 14))],
  ("Loop with ceiling division.", "O(n)", "O(n)"),
  ("A comprehension with the <code>toks</code> helper, then <code>sum</code>.", "O(n)", "O(n)"),
  viz=(["You are a helpful assistant.", "Summarise MCP in one line."],))


@B
def count_tokens(messages):
    per = []
    for m in messages:
        n = len(m) // 4
        if len(m) % 4:
            n += 1
        per.append(n)
    return (per, sum(per))


@O
def count_tokens(messages):
    per = [toks(m) for m in messages]
    return (per, sum(per))


Q(None, "Fit the History Into the Window", "Medium", "Trimming",
  "Always keep message 0 (the system prompt) and the newest message. Then add older messages from newest to oldest while the total stays ≤ <code>window</code>. Return the kept indexes in order.",
  [(([300, 900, 400, 700, 200, 100], 1300), [0, 3, 4, 5]), (([300, 900, 400, 700, 200, 100], 400), [0, 5])],
  ("Walk backwards with a running total.", "O(n)", "O(n)"),
  ("Same walk, collecting into a set and sorting at the end.", "O(n log n)", "O(n)"),
  viz=([300, 900, 400, 700, 200, 100], 1300))


@B
def fit_window(sizes, window):
    kept = [0, len(sizes) - 1]
    used = sizes[0] + sizes[-1]
    i = len(sizes) - 2
    while i > 0:
        if used + sizes[i] > window:
            break
        kept.append(i)
        used += sizes[i]
        i -= 1
    return sorted(kept)


@O
def fit_window(sizes, window):
    kept, used = {0, len(sizes) - 1}, sizes[0] + sizes[-1]
    for i in range(len(sizes) - 2, 0, -1):
        if used + sizes[i] > window:
            break
        kept.add(i)
        used += sizes[i]
    return sorted(kept)


Q(None, "Compact the Conversation", "Medium", "Summarise the oldest turns",
  "When the history (after the system prompt) exceeds <code>trigger</code> tokens, replace the oldest messages with one summary of <code>summary</code> tokens, keeping the newest <code>keep</code> messages. Return <code>(tokens before, tokens after, messages after including the system prompt)</code>.",
  [(([500, 1200, 3000, 2500, 1800, 900, 400], 6000, 3, 600), (10300, 4200, 5)), (([500, 100, 200], 6000, 3, 600), (800, 800, 3))],
  ("Sum, check, then rebuild the list.", "O(n)", "O(n)"),
  ("Slicing: system + [summary] + last keep.", "O(n)", "O(n)"),
  viz=([500, 1200, 3000, 2500, 1800, 900, 400], 6000, 3, 600))


@B
def compact(sizes, trigger, keep, summary):
    before = 0
    for s in sizes:
        before += s
    history = sizes[1:]
    if before - sizes[0] <= trigger:
        return (before, before, len(sizes))
    new = [sizes[0], summary]
    for s in history[len(history) - keep:]:
        new.append(s)
    return (before, sum(new), len(new))


@O
def compact(sizes, trigger, keep, summary):
    before = sum(sizes)
    if before - sizes[0] <= trigger:
        return (before, before, len(sizes))
    new = [sizes[0], summary, *sizes[-keep:]]
    return (before, sum(new), len(new))


Q(None, "Avoid 'Lost in the Middle'", "Medium", "Ordering documents",
  "Models attend best to the start and end of a long context. Given document ids ranked by relevance (best first), place them so the best is first, the second-best is last, the third is second, the fourth second-to-last, and so on.",
  [((["d1", "d2", "d3", "d4", "d5"],), ['d1', 'd3', 'd5', 'd4', 'd2']), ((["a", "b"],), ['a', 'b'])],
  ("Fill a result list from both ends alternately.", "O(n)", "O(n)"),
  ("Even ranks go to the front in order, odd ranks to the back reversed.", "O(n)", "O(n)"),
  viz=(["d1", "d2", "d3", "d4", "d5"],))


@B
def edges_first(ranked):
    out = [None] * len(ranked)
    left, right = 0, len(ranked) - 1
    for i, d in enumerate(ranked):
        if i % 2 == 0:
            out[left] = d
            left += 1
        else:
            out[right] = d
            right -= 1
    return out


@O
def edges_first(ranked):
    return ranked[0::2] + ranked[1::2][::-1]


Q(None, "Put Stable Content First", "Easy", "Cache-friendly order",
  "Prompt caches reuse an identical <b>prefix</b>. Order blocks so everything that never changes comes first (keeping their original order), then things that change per user, then per-request content. Each block is <code>(name, 'static' | 'per_user' | 'per_request')</code>; return the names in the new order.",
  [(([("question", "per_request"), ("system", "static"), ("user_profile", "per_user"), ("tools", "static"), ("retrieved_docs", "per_request")],), ['system', 'tools', 'user_profile', 'question', 'retrieved_docs'])],
  ("Three passes, one per kind.", "O(n)", "O(n)"),
  ("A stable <code>sorted</code> with a rank key.", "O(n log n)", "O(n)"),
  viz=([("question", "per_request"), ("system", "static"), ("user_profile", "per_user"), ("tools", "static")],))


@B
def cache_order(blocks):
    out = []
    for kind in ["static", "per_user", "per_request"]:
        for name, k in blocks:
            if k == kind:
                out.append(name)
    return out


@O
def cache_order(blocks):
    rank = {"static": 0, "per_user": 1, "per_request": 2}
    return [name for name, k in sorted(blocks, key=lambda b: rank[b[1]])]


Q(None, "What Does Caching Save?", "Medium", "Prompt-cache pricing",
  "A request has <code>prefix</code> cacheable tokens and <code>rest</code> other input tokens, sent <code>n</code> times. Input costs <code>price</code> per million tokens; writing the cache costs 1.25× and reading it 0.1×. The first request writes the cache; later ones read it. Return <code>(cost without caching, cost with caching, % saved)</code>, money rounded to 4 and % to 1.",
  [((50000, 2000, 20, 3.0), (3.12, 0.5925, 81.0)), ((1000, 2000, 2, 3.0), (0.018, 0.0161, 10.8))],
  ("Add request by request.", "O(n)", "O(1)"),
  ("A closed-form formula.", "O(1)", "O(1)"),
  viz=((50000, 2000, 20, 3.0)))


@B
def cache_savings(prefix, rest, n, price):
    per_token = price / 1_000_000
    plain = 0
    cached = 0
    for i in range(n):
        plain += (prefix + rest) * per_token
        if i == 0:
            cached += (prefix * 1.25 + rest) * per_token
        else:
            cached += (prefix * 0.1 + rest) * per_token
    return (round(plain, 4), round(cached, 4), round((plain - cached) / plain * 100, 1))


@O
def cache_savings(prefix, rest, n, price):
    p = price / 1e6
    plain = n * (prefix + rest) * p
    cached = (prefix * 1.25 + (n - 1) * prefix * 0.1 + n * rest) * p
    return (round(plain, 4), round(cached, 4), round((plain - cached) / plain * 100, 1))


Q(None, "Clear Old Tool Results", "Easy", "Context editing",
  "Agents pile up tool outputs the model no longer needs. Replace every tool result except the newest <code>keep</code> with a 10-token placeholder. Messages are <code>(kind, tokens)</code>. Return <code>(tokens before, tokens after)</code>.",
  [(([("user", 50), ("tool", 4000), ("assistant", 200), ("tool", 6000), ("tool", 3000), ("assistant", 150)], 1), (13400, 3420))],
  ("Find tool positions, then rebuild sizes in a loop.", "O(n)", "O(n)"),
  ("Indexes of tool messages; a comprehension decides each size.", "O(n)", "O(n)"),
  viz=([("user", 50), ("tool", 4000), ("assistant", 200), ("tool", 6000), ("tool", 3000)], 1))


@B
def clear_tools(messages, keep):
    tool_idx = []
    for i, (kind, _) in enumerate(messages):
        if kind == "tool":
            tool_idx.append(i)
    old = tool_idx[:len(tool_idx) - keep] if keep else tool_idx
    after = 0
    for i, (kind, n) in enumerate(messages):
        after += 10 if i in old else n
    return (sum(n for _, n in messages), after)


@O
def clear_tools(messages, keep):
    tools = [i for i, (k, _) in enumerate(messages) if k == "tool"]
    old = set(tools[:-keep] if keep else tools)
    return (sum(n for _, n in messages), sum(10 if i in old else n for i, (_, n) in enumerate(messages)))


Q(None, "Share the Budget Between Sections", "Medium", "Allocation",
  "Split <code>budget</code> tokens between sections. Each gets its <code>minimum</code> first; the remainder is shared in proportion to <code>weight</code> (rounded down). No section gets more than it <code>wants</code>. Return <code>{section: tokens}</code>.",
  [(({"system": (500, 0, 500), "memory": (200, 1, 3000), "docs": (1000, 3, 20000), "history": (500, 2, 6000)}, 8000), {'system': 500, 'memory': 1166, 'docs': 3900, 'history': 2433})],
  ("Give minimums, then loop over sections computing shares.", "O(s)", "O(s)"),
  ("Same steps with comprehensions.", "O(s)", "O(s)"),
  viz=({"system": (500, 0, 500), "memory": (200, 1, 3000), "docs": (1000, 3, 20000)}, 8000))


@B
def allocate(sections, budget):
    out = {}
    left = budget
    for name, (minimum, weight, wants) in sections.items():
        out[name] = minimum
        left -= minimum
    total_w = 0
    for name, (minimum, weight, wants) in sections.items():
        total_w += weight
    for name, (minimum, weight, wants) in sections.items():
        extra = left * weight // total_w if total_w else 0
        out[name] = min(wants, minimum + extra)
    return out


@O
def allocate(sections, budget):
    left = budget - sum(m for m, _, _ in sections.values())
    total_w = sum(w for _, w, _ in sections.values()) or 1
    return {name: min(wants, m + left * w // total_w) for name, (m, w, wants) in sections.items()}


Q(None, "Choose Few-Shot Examples", "Medium", "Dynamic examples",
  "Pick the <code>k</code> examples whose words overlap most with the query (Jaccard similarity of lower-cased word sets); ties keep the original order.",
  [(("refund my late order", ["where is my order", "refund for a damaged item", "change my password", "late delivery refund please"], 2), ['where is my order', 'late delivery refund please'])],
  ("Score each example with set operations, then sort.", "O(e · w)", "O(e)"),
  ("<code>sorted</code> with a key, which is stable for ties.", "O(e · w)", "O(e)"),
  viz=("refund my late order", ["where is my order", "refund for a damaged item", "late delivery refund please"], 2))


@B
def pick_examples(query, examples, k):
    q = set(query.lower().split())
    scored = []
    for i, ex in enumerate(examples):
        e = set(ex.lower().split())
        scored.append((len(q & e) / len(q | e), i, ex))
    scored.sort(key=lambda t: (-t[0], t[1]))
    return [ex for _, _, ex in scored[:k]]


@O
def pick_examples(query, examples, k):
    q = set(query.lower().split())
    jac = lambda ex: len(q & set(ex.lower().split())) / len(q | set(ex.lower().split()))
    return sorted(examples, key=jac, reverse=True)[:k]


Q(None, "Load Files Just in Time", "Easy", "Preload vs on-demand",
  "An agent can preload every file into context, or list file names (5 tokens each) and read only what it needs. Return <code>(preload tokens, just-in-time tokens)</code> for the files it actually <code>used</code>.",
  [(({"README.md": 1200, "api.py": 5400, "models.py": 8000, "tests.py": 6600, "CHANGELOG.md": 9000}, ["README.md", "api.py"]), (30200, 6625))],
  ("Two running totals in a loop.", "O(f)", "O(1)"),
  ("Two <code>sum</code> expressions.", "O(f)", "O(1)"),
  viz=({"README.md": 1200, "api.py": 5400, "models.py": 8000}, ["README.md"]))


@B
def jit_tokens(files, used):
    preload, jit = 0, 0
    for name, size in files.items():
        preload += size
        jit += 5
        if name in used:
            jit += size
    return (preload, jit)


@O
def jit_tokens(files, used):
    return (sum(files.values()), 5 * len(files) + sum(files[u] for u in used))


Q(None, "The Hidden Cost of Long Chats", "Medium", "History is re-sent every turn",
  "Every turn re-sends the whole history. Each turn adds <code>per_turn</code> tokens. Return the total input tokens over <code>turns</code> turns <b>(a)</b> without compaction and <b>(b)</b> when history is compacted to <code>summary</code> tokens whenever it would exceed <code>trigger</code>.",
  [((40, 2000, 30000, 3000), (1640000, 653000))],
  ("Simulate turn by turn for both strategies.", "O(t)", "O(1)"),
  ("Closed form for (a): per_turn × t(t+1)/2; simulate (b).", "O(t)", "O(1)"),
  viz=((10, 2000, 8000, 1000)))


@B
def chat_cost(turns, per_turn, trigger, summary):
    plain = 0
    hist = 0
    for _ in range(turns):
        hist += per_turn
        plain += hist
    compacted = 0
    hist = 0
    for _ in range(turns):
        hist += per_turn
        if hist > trigger:
            hist = summary + per_turn
        compacted += hist
    return (plain, compacted)


@O
def chat_cost(turns, per_turn, trigger, summary):
    plain = per_turn * turns * (turns + 1) // 2
    hist = compacted = 0
    for _ in range(turns):
        hist = hist + per_turn if hist + per_turn <= trigger else summary + per_turn
        compacted += hist
    return (plain, compacted)


PATTERNS = [(r"my name is (\w+)", "name"), (r"i live in (\w+)", "city"), (r"i prefer (\w+)", "preference"),
            (r"i work (?:at|for) (\w+)", "employer")]


Q(None, "Extract Facts to Remember", "Medium", "Memory extraction",
  "Pull simple facts from a user's messages with <code>PATTERNS</code> (case-insensitive). Later messages override earlier ones. Return <code>{key: value}</code>. (Real systems ask an LLM to extract facts; the pipeline around it is the same.)",
  [((["Hi, my name is Asha", "I live in Pune and I prefer email", "Actually I live in Mumbai now"],), {'name': 'Asha', 'city': 'Mumbai', 'preference': 'email'})],
  ("Loop over messages and patterns with <code>re.search</code>.", "O(m · p)", "O(k)"),
  ("A dict comprehension over every match, in order — later keys overwrite earlier ones.", "O(m · p)", "O(k)"),
  viz=(["Hi, my name is Asha", "I live in Pune and I prefer email"],))


@B
def extract_facts(messages):
    facts = {}
    for m in messages:
        for pattern, key in PATTERNS:
            found = re.search(pattern, m, re.I)
            if found:
                facts[key] = found.group(1)
    return facts


@O
def extract_facts(messages):
    return {key: m.group(1) for msg in messages for pattern, key in PATTERNS if (m := re.search(pattern, msg, re.I))}


Q(None, "Add, Update or Skip?", "Medium", "Memory consolidation",
  "For each new fact <code>(key, value)</code> decide against the store: 'ADD' if the key is new, 'SKIP' if the value is the same (ignoring case), 'UPDATE' otherwise. Apply them in order, keeping replaced values in a history list. Return <code>(decisions, final store, history)</code>.",
  [(({"city": "Pune", "name": "Asha"}, [("city", "pune"), ("city", "Mumbai"), ("diet", "vegetarian"), ("name", "Asha")]), (['SKIP', 'UPDATE', 'ADD', 'SKIP'], {'city': 'Mumbai', 'name': 'Asha', 'diet': 'vegetarian'}, [('city', 'Pune')]))],
  ("An if-chain that also updates the store.", "O(n)", "O(n)"),
  ("Same logic with a helper returning the decision.", "O(n)", "O(n)"),
  viz=({"city": "Pune"}, [("city", "pune"), ("city", "Mumbai")]))


@B
def consolidate(store, facts):
    store = dict(store)
    decisions, history = [], []
    for key, value in facts:
        if key not in store:
            decisions.append("ADD")
            store[key] = value
        elif store[key].lower() == value.lower():
            decisions.append("SKIP")
        else:
            decisions.append("UPDATE")
            history.append((key, store[key]))
            store[key] = value
    return (decisions, store, history)


@O
def consolidate(store, facts):
    store, decisions, history = dict(store), [], []
    for key, value in facts:
        old = store.get(key)
        op = "ADD" if old is None else "SKIP" if old.lower() == value.lower() else "UPDATE"
        decisions.append(op)
        if op == "UPDATE":
            history.append((key, old))
        if op != "SKIP":
            store[key] = value
    return (decisions, store, history)


MEMORIES = [("prefers email over phone", 30), ("lives in Mumbai", 2), ("allergic to peanuts", 200),
            ("asked about refund for order 812", 1), ("prefers window seats on flights", 90)]


Q(None, "Recall the Right Memories", "Medium", "Relevance × recency",
  "Score each memory <code>(text, age_days)</code> as (number of query words it contains) × 0.5^(age / half_life). Return the top <code>k</code> texts with a score above 0 (ties: newer first).",
  [(("how should I contact you about my refund", 30, 2), ['asked about refund for order 812']), (("is the user allergic to anything", 30, 3), ['allergic to peanuts'])],
  ("Score in a loop and sort.", "O(m · w)", "O(m)"),
  ("A key function with <code>sorted</code>.", "O(m · w)", "O(m)"),
  viz=(("how should I contact you about my refund", 30, 2)))


@B
def recall(query, half_life, k):
    q = set(query.lower().split())
    scored = []
    for text, age in MEMORIES:
        overlap = 0
        for w in text.lower().split():
            if w in q:
                overlap += 1
        score = overlap * 0.5 ** (age / half_life)
        if score > 0:
            scored.append((score, -age, text))
    scored.sort(reverse=True)
    return [t for _, _, t in scored[:k]]


@O
def recall(query, half_life, k):
    q = set(query.lower().split())
    score = lambda m: sum(w in q for w in m[0].lower().split()) * 0.5 ** (m[1] / half_life)
    ranked = sorted((m for m in MEMORIES if score(m) > 0), key=lambda m: (score(m), -m[1]), reverse=True)
    return [t for t, _ in ranked[:k]]


Q(None, "Short-Term Buffer, Long-Term Store", "Easy", "Memory tiers",
  "Keep the last <code>n</code> messages in a short-term buffer. When a new message pushes one out, the oldest moves to long-term memory. Return <code>(short-term, long-term)</code> after all messages.",
  [((["m1", "m2", "m3", "m4", "m5"], 3), (['m3', 'm4', 'm5'], ['m1', 'm2']))],
  ("A list with pop(0).", "O(n · b)", "O(n)"),
  ("A <code>deque(maxlen=n)</code>: check whether it's full before appending.", "O(n)", "O(n)"),
  viz=(["m1", "m2", "m3", "m4", "m5"], 3))


@B
def tiers(messages, n):
    short, long_term = [], []
    for m in messages:
        short.append(m)
        if len(short) > n:
            long_term.append(short.pop(0))
    return (short, long_term)


@O
def tiers(messages, n):
    short, long_term = deque(maxlen=n), []
    for m in messages:
        if len(short) == n:
            long_term.append(short[0])
        short.append(m)
    return (list(short), long_term)


Q(None, "A Notes File the Agent Keeps", "Easy", "Structured note-taking",
  "Long tasks outlive the context window, so agents keep a to-do file. Apply commands <code>('add', item)</code>, <code>('done', item)</code>, <code>('drop', item)</code> and return <code>(open items, done items)</code> in the order they were added. Adding an existing item does nothing.",
  [(([("add", "read spec"), ("add", "write tests"), ("add", "read spec"), ("done", "read spec"), ("add", "fix bug"), ("drop", "write tests")],), (['fix bug'], ['read spec']))],
  ("Two lists and if-statements.", "O(n²)", "O(n)"),
  ("One ordered dict of item → status.", "O(n)", "O(n)"),
  viz=([("add", "read spec"), ("add", "write tests"), ("done", "read spec")],))


@B
def notes(commands):
    open_items, done = [], []
    for cmd, item in commands:
        if cmd == "add" and item not in open_items and item not in done:
            open_items.append(item)
        elif cmd == "done" and item in open_items:
            open_items.remove(item)
            done.append(item)
        elif cmd == "drop" and item in open_items:
            open_items.remove(item)
    return (open_items, done)


@O
def notes(commands):
    status = {}
    for cmd, item in commands:
        if cmd == "add":
            status.setdefault(item, "open")
        elif status.get(item) == "open":
            status[item] = "done" if cmd == "done" else "dropped"
    order = list(status)
    return ([i for i in order if status[i] == "open"], [i for i in order if status[i] == "done"])


Q(None, "Newest Fact Wins", "Easy", "Conflicting memories",
  "Memories arrive as <code>(key, value, timestamp)</code> in any order. Keep the value with the latest timestamp for each key. Return <code>{key: value}</code> sorted by key.",
  [(([("city", "Pune", 5), ("city", "Mumbai", 9), ("diet", "veg", 3), ("city", "Delhi", 7)],), {'city': 'Mumbai', 'diet': 'veg'})],
  ("A dict holding (timestamp, value) and comparisons.", "O(n)", "O(k)"),
  ("Sort by timestamp, then a dict comprehension lets later ones overwrite.", "O(n log n)", "O(k)"),
  viz=([("city", "Pune", 5), ("city", "Mumbai", 9), ("city", "Delhi", 7)],))


@B
def newest(memories):
    best = {}
    for key, value, ts in memories:
        if key not in best or ts > best[key][0]:
            best[key] = (ts, value)
    return {k: best[k][1] for k in sorted(best)}


@O
def newest(memories):
    latest = {k: v for k, v, _ in sorted(memories, key=lambda m: m[2])}
    return dict(sorted(latest.items()))


Q(None, "Assemble the Final Prompt", "Medium", "Putting it together",
  "Build the context: system prompt, then recalled memories as a bullet list under 'Known about the user:', then documents in 'lost in the middle' order, then the question. Skip any section that is empty. Sections are separated by a blank line. Return the text.",
  [(("You are ShopKart's assistant.", ["lives in Mumbai"], ["d1", "d2", "d3"], "Where is my order?"), "You are ShopKart's assistant.\n\nKnown about the user:\n- lives in Mumbai\n\nd1\nd3\nd2\n\nWhere is my order?"),
   (("Be brief.", [], [], "Hi"), 'Be brief.\n\nHi')],
  ("Append sections to a list with if-statements.", "O(n)", "O(n)"),
  ("A list of optional sections filtered for empties, joined once.", "O(n)", "O(n)"),
  viz=("You are ShopKart's assistant.", ["lives in Mumbai"], ["d1", "d2", "d3"], "Where is my order?"))


@B
def assemble(system, memories, docs, question):
    parts = [system]
    if memories:
        text = "Known about the user:"
        for m in memories:
            text += "\n- " + m
        parts.append(text)
    if docs:
        ordered = [None] * len(docs)
        left, right = 0, len(docs) - 1
        for i, d in enumerate(docs):
            if i % 2 == 0:
                ordered[left] = d
                left += 1
            else:
                ordered[right] = d
                right -= 1
        parts.append("\n".join(ordered))
    parts.append(question)
    return "\n\n".join(parts)


@O
def assemble(system, memories, docs, question):
    sections = [system,
                "Known about the user:\n" + "\n".join(f"- {m}" for m in memories) if memories else "",
                "\n".join(docs[0::2] + docs[1::2][::-1]),
                question]
    return "\n\n".join(s for s in sections if s)


Q(None, "Is the Prefix Cached?", "Medium", "Cache hits",
  "A cache hit needs the new request to start with exactly the same blocks as an earlier one. Count the tokens of the leading blocks that match (blocks are <code>(text, tokens)</code>). It only counts as a hit if those tokens reach <code>minimum</code>. Return <code>(matching prefix tokens, hit?)</code>.",
  [(([("SYS", 900), ("TOOLS", 1500), ("DOCS", 4000), ("Q1", 50)], [("SYS", 900), ("TOOLS", 1500), ("DOCS", 4000), ("Q2", 60)], 1024), (6400, True)),
   (([("SYS", 900), ("TOOLS", 1500)], [("SYS v2", 905), ("TOOLS", 1500)], 1024), (0, False)),
   (([("SYS", 500), ("Q1", 20)], [("SYS", 500), ("Q2", 20)], 1024), (500, False))],
  ("Walk both lists until the first difference.", "O(b)", "O(1)"),
  ("<code>itertools.takewhile</code> over the zipped blocks.", "O(b)", "O(1)"),
  viz=([("SYS", 900), ("TOOLS", 1500), ("Q1", 50)], [("SYS", 900), ("TOOLS", 1500), ("Q2", 60)], 1024))


@B
def prefix_hit(old, new, minimum):
    total = 0
    for a, b in zip(old, new):
        if a != b:
            break
        total += a[1]
    return (total, total >= minimum)


@O
def prefix_hit(old, new, minimum):
    from itertools import takewhile
    total = sum(a[1] for a, b in takewhile(lambda p: p[0] == p[1], zip(old, new)))
    return (total, total >= minimum)


Q(None, "What's Eating the Window?", "Easy", "Context audits",
  "Given token counts per section, return <code>(sections sorted by share, largest first, as (name, % rounded to 1)), names taking over 40%)</code>. Auditing the context is the first step of any context-engineering fix.",
  [(({"system": 1200, "tools": 9000, "history": 14000, "docs": 6000, "question": 80},), ([('history', 46.2), ('tools', 29.7), ('docs', 19.8), ('system', 4.0), ('question', 0.3)], ['history']))],
  ("Compute shares in a loop, then sort.", "O(s log s)", "O(s)"),
  ("A sorted comprehension.", "O(s log s)", "O(s)"),
  viz=({"system": 1200, "tools": 9000, "history": 14000, "docs": 6000, "question": 80},))


@B
def window_audit(sections):
    total = 0
    for n in sections.values():
        total += n
    shares = []
    for name, n in sections.items():
        shares.append((name, round(n / total * 100, 1)))
    shares.sort(key=lambda x: -x[1])
    big = [name for name, pct in shares if pct > 40]
    return (shares, big)


@O
def window_audit(sections):
    total = sum(sections.values())
    shares = sorted(((k, round(v / total * 100, 1)) for k, v in sections.items()), key=lambda x: -x[1])
    return (shares, [k for k, pct in shares if pct > 40])
