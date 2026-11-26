from lib import *
import heapq
from collections import Counter, deque
from graphlib import TopologicalSorter


TOPIC(
    id="multi-agent", title="Agents & Multi-Agent Orchestration", glyph="⚙⚙",
    blurb="How agent systems really work: the tool loop, routing, planning with dependencies, parallel fan-out, orchestrator–workers, handoffs, shared state, evaluator–optimizer loops, budgets, loop detection, worker pools and graph workflows like LangGraph.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">while steps &lt; max_steps:                     # the agent loop
    reply = model(messages, tools)
    if reply.stop_reason != "tool_use": break
    messages += [reply, run_tools(reply)]

# patterns, simplest first
prompt chain → router → parallel fan-out → orchestrator–workers → evaluator–optimizer → autonomous agent
TopologicalSorter(deps).static_order()        # plan order
asyncio.gather(*[worker(t) for t in tasks])    # fan-out</code></pre>
<p>Start with the simplest pattern that works. Every extra agent multiplies cost, latency and ways to fail.</p>
""")


Q(None, "Run the Agent Loop", "Easy", "Tool use until done",
  "A scripted model returns, at each step, either <code>('tool', name, arg)</code> or <code>('final', text)</code>. Run the loop: call tools from <code>TOOLS</code>, stop on 'final' or after <code>max_steps</code> model calls. Return <code>(final text or 'stopped: max steps', tool results in order)</code>.",
  [(([("tool", "search", "mcp"), ("tool", "calc", "2*21"), ("final", "done")], 5), ('done', ['3 results for mcp', '42'])), (([("tool", "search", "x")] * 4, 3), ('stopped: max steps', ['3 results for x', '3 results for x', '3 results for x']))],
  ("A while loop with a step counter.", "O(steps)", "O(steps)"),
  ("A for loop over <code>range(max_steps)</code> with an early return.", "O(steps)", "O(steps)"),
  viz=([("tool", "search", "mcp"), ("tool", "calc", "2*21"), ("final", "done")], 5))


TOOLS = {"search": lambda q: f"3 results for {q}", "calc": lambda e: str(eval(e, {"__builtins__": {}}))}


@B
def agent_loop(script, max_steps):
    results = []
    step = 0
    while step < max_steps:
        action = script[step]
        step += 1
        if action[0] == "final":
            return (action[1], results)
        results.append(TOOLS[action[1]](action[2]))
    return ("stopped: max steps", results)


@O
def agent_loop(script, max_steps):
    results = []
    for action in script[:max_steps]:
        if action[0] == "final":
            return (action[1], results)
        results.append(TOOLS[action[1]](action[2]))
    return ("stopped: max steps", results)


ROUTES = {"billing": ["refund", "invoice", "charge", "payment"], "tech": ["error", "crash", "login", "bug"],
          "sales": ["price", "plan", "upgrade", "discount"]}


Q(None, "Route to a Specialist", "Easy", "Router pattern",
  "Send a request to the specialist whose keywords appear most often in it (words are lower-cased, punctuation stripped). Ties go to the earlier route in <code>ROUTES</code>; no match goes to 'general'.",
  [(("I was charged twice, please refund the payment",), 'billing'), (("App crash after login",), 'tech'), (("Hello there",), 'general')],
  ("Count matches per route with nested loops.", "O(w · k)", "O(r)"),
  ("A Counter of words, then sum per route and <code>max</code>.", "O(w + k)", "O(w)"),
  viz=("I was charged twice, please refund the payment",))


@B
def route(text):
    words = [w.strip(".,!?").lower() for w in text.split()]
    best, best_n = "general", 0
    for name, keys in ROUTES.items():
        n = 0
        for w in words:
            if w in keys:
                n += 1
        if n > best_n:
            best, best_n = name, n
    return best


@O
def route(text):
    counts = Counter(w.strip(".,!?").lower() for w in text.split())
    scores = {name: sum(counts[k] for k in keys) for name, keys in ROUTES.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "general"


PLAN = {"write_report": ["analyse", "fetch_news"], "analyse": ["fetch_sales", "fetch_news"], "fetch_sales": [], "fetch_news": []}


Q(None, "Order a Plan", "Medium", "Dependencies · topological sort",
  "A planner produced tasks with dependencies (task → tasks it needs first). Return an order that respects them; among tasks that are ready at the same time, take them alphabetically.",
  [((PLAN,), ['fetch_news', 'fetch_sales', 'analyse', 'write_report']), (({"c": ["a"], "b": ["a"], "a": []},), ['a', 'b', 'c'])],
  ("Kahn's algorithm: repeatedly take the alphabetically-first task whose needs are done.", "O(n² )", "O(n)"),
  ("<code>graphlib.TopologicalSorter</code> plus a min-heap, so the alphabetically-first ready task always goes next.", "O(n log n + e)", "O(n + e)"),
  viz=(PLAN,))


@B
def plan_order(deps):
    done, order = set(), []
    while len(order) < len(deps):
        ready = sorted(t for t in deps if t not in done and all(d in done for d in deps[t]))
        order.append(ready[0])
        done.add(ready[0])
    return order


@O
def plan_order(deps):
    ts = TopologicalSorter(deps)
    ts.prepare()
    ready, order = [], []
    while ts.is_active():
        for t in ts.get_ready():      # each task is offered once, so keep it in a heap
            heapq.heappush(ready, t)
        t = heapq.heappop(ready)
        order.append(t)
        ts.done(t)
    return order


Q(None, "How Long With Parallel Workers?", "Medium", "Fan-out · critical path",
  "Each task takes <code>secs[task]</code> and can start as soon as its dependencies finish (unlimited workers). Return <code>(total time if run one by one, total time in parallel)</code>.",
  [((PLAN, {"fetch_sales": 4, "fetch_news": 6, "analyse": 3, "write_report": 2}), (15, 11))],
  ("Recursively compute each task's finish time = its time + the latest dependency's finish.", "O(n + e)", "O(n)"),
  ("Same recurrence with <code>functools.cache</code>, written as one expression.", "O(n + e)", "O(n)"),
  viz=(PLAN, {"fetch_sales": 4, "fetch_news": 6, "analyse": 3, "write_report": 2}))


@B
def wall_time(deps, secs):
    finish = {}

    def end(t):
        if t not in finish:
            latest = 0
            for d in deps[t]:
                latest = max(latest, end(d))
            finish[t] = latest + secs[t]
        return finish[t]
    return (sum(secs.values()), max(end(t) for t in deps))


@O
def wall_time(deps, secs):
    from functools import cache

    @cache
    def end(t):
        return secs[t] + max((end(d) for d in deps[t]), default=0)
    return (sum(secs.values()), max(map(end, deps)))


Q(None, "Combine Worker Answers by Vote", "Easy", "Orchestrator–workers",
  "Several workers answered the same question. Return <code>(winning answer, share of votes rounded to 2)</code>; ties go to the answer seen first. Answers are compared after stripping and lower-casing.",
  [((["Paris", "paris ", "Lyon", "Paris"],), ('paris', 0.75)), ((["A", "B"],), ('a', 0.5))],
  ("Count in a dict and track the first-seen order.", "O(n)", "O(n)"),
  ("<code>Counter.most_common</code> keeps first-seen order for ties.", "O(n)", "O(n)"),
  viz=(["Paris", "paris ", "Lyon", "Paris"],))


@B
def vote(answers):
    counts, order = {}, []
    for a in answers:
        a = a.strip().lower()
        if a not in counts:
            counts[a] = 0
            order.append(a)
        counts[a] += 1
    best = order[0]
    for a in order:
        if counts[a] > counts[best]:
            best = a
    return (best, round(counts[best] / len(answers), 2))


@O
def vote(answers):
    best, n = Counter(a.strip().lower() for a in answers).most_common(1)[0]
    return (best, round(n / len(answers), 2))


Q(None, "Follow the Handoffs", "Medium", "Handoff pattern",
  "Agents hand the conversation to each other. <code>handoffs[agent]</code> is the agent it passes to, or None if it answers itself. Start at <code>start</code>; return the path of agents, or the path ending in 'LOOP' if an agent repeats, or 'TOO DEEP' after <code>max_hops</code> handoffs.",
  [(({"triage": "billing", "billing": "refunds", "refunds": None}, "triage", 5), ['triage', 'billing', 'refunds']),
   (({"a": "b", "b": "a"}, "a", 5), ['a', 'b', 'LOOP']), (({"a": "b", "b": "c", "c": "d", "d": None}, "a", 2), ['a', 'b', 'c', 'TOO DEEP'])],
  ("A loop with a visited list.", "O(h)", "O(h)"),
  ("Same loop with a set for O(1) repeat checks.", "O(h)", "O(h)"),
  viz=({"triage": "billing", "billing": "refunds", "refunds": None}, "triage", 5))


@B
def follow(handoffs, start, max_hops):
    path = [start]
    hops = 0
    while handoffs[path[-1]] is not None:
        nxt = handoffs[path[-1]]
        if nxt in path:
            return path + ["LOOP"]
        hops += 1
        if hops > max_hops:
            return path + ["TOO DEEP"]
        path.append(nxt)
    return path


@O
def follow(handoffs, start, max_hops):
    path, seen = [start], {start}
    while (nxt := handoffs[path[-1]]) is not None:
        if nxt in seen:
            return path + ["LOOP"]
        if len(path) > max_hops:
            return path + ["TOO DEEP"]
        path.append(nxt)
        seen.add(nxt)
    return path


Q(None, "Shared State Without Lost Updates", "Medium", "Blackboard · optimistic locking",
  "Agents write to a shared state. Each update is <code>(agent, key, value, version_seen)</code>; it applies only if <code>version_seen</code> equals the key's current version (starting at 0), and then the version goes up by 1. Return <code>(final state, rejected agents in order)</code>.",
  [(([("planner", "plan", "v1", 0), ("coder", "plan", "v2", 0), ("coder", "code", "x=1", 0), ("reviewer", "plan", "v3", 1)],), ({'plan': 'v3', 'code': 'x=1'}, ['coder']))],
  ("Two dicts updated in a loop.", "O(u)", "O(k)"),
  ("Same, with <code>dict.get(key, 0)</code> for the version.", "O(u)", "O(k)"),
  viz=([("planner", "plan", "v1", 0), ("coder", "plan", "v2", 0), ("reviewer", "plan", "v3", 1)],))


@B
def apply_updates(updates):
    state, version, rejected = {}, {}, []
    for agent, key, value, seen in updates:
        current = version[key] if key in version else 0
        if seen == current:
            state[key] = value
            version[key] = current + 1
        else:
            rejected.append(agent)
    return (state, rejected)


@O
def apply_updates(updates):
    state, version, rejected = {}, {}, []
    for agent, key, value, seen in updates:
        if seen == version.get(key, 0):
            state[key], version[key] = value, seen + 1
        else:
            rejected.append(agent)
    return (state, rejected)


Q(None, "Deliver Messages Between Agents", "Medium", "Inboxes · queues",
  "Agents talk through inboxes. When an agent reads a message, <code>rules[agent]</code> lists who it forwards to. Starting with one message to <code>first</code>, process messages first-in-first-out and return the order in which agents read messages (stop after <code>limit</code> reads).",
  [(({"user": ["planner"], "planner": ["coder", "tester"], "coder": ["reviewer"], "tester": [], "reviewer": []}, "user", 10), ['user', 'planner', 'coder', 'tester', 'reviewer']),
   (({"a": ["b"], "b": ["a"]}, "a", 5), ['a', 'b', 'a', 'b', 'a'])],
  ("A list used as a queue (pop(0)).", "O(n²)", "O(n)"),
  ("<code>collections.deque</code> for O(1) pops from the front.", "O(n)", "O(n)"),
  viz=({"user": ["planner"], "planner": ["coder", "tester"], "coder": ["reviewer"], "tester": [], "reviewer": []}, "user", 10))


@B
def deliver(rules, first, limit):
    queue, reads = [first], []
    while queue and len(reads) < limit:
        agent = queue.pop(0)
        reads.append(agent)
        for nxt in rules[agent]:
            queue.append(nxt)
    return reads


@O
def deliver(rules, first, limit):
    queue, reads = deque([first]), []
    while queue and len(reads) < limit:
        agent = queue.popleft()
        reads.append(agent)
        queue.extend(rules[agent])
    return reads


Q(None, "Evaluator–Optimizer Loop", "Easy", "Generate, critique, retry",
  "A generator produces drafts; an evaluator scores each (here <code>scores[i]</code> for draft i). Stop at the first draft scoring ≥ <code>target</code>, or after <code>max_rounds</code> drafts and return the best one seen. Return <code>(draft index, score, rounds used)</code>.",
  [(([0.4, 0.7, 0.9, 0.95], 0.85, 5), (2, 0.9, 3)), (([0.4, 0.7, 0.6], 0.85, 3), (1, 0.7, 3))],
  ("A loop tracking the best so far.", "O(r)", "O(1)"),
  ("Find the first passing index with <code>next</code>; otherwise <code>max</code> over the tried drafts.", "O(r)", "O(1)"),
  viz=([0.4, 0.7, 0.9, 0.95], 0.85, 5))


@B
def refine(scores, target, max_rounds):
    best = 0
    for i in range(min(max_rounds, len(scores))):
        if scores[i] > scores[best]:
            best = i
        if scores[i] >= target:
            return (i, scores[i], i + 1)
    return (best, scores[best], min(max_rounds, len(scores)))


@O
def refine(scores, target, max_rounds):
    tried = scores[:max_rounds]
    hit = next((i for i, s in enumerate(tried) if s >= target), None)
    if hit is not None:
        return (hit, tried[hit], hit + 1)
    best = max(range(len(tried)), key=tried.__getitem__)
    return (best, tried[best], len(tried))


Q(None, "Stay Within the Token Budget", "Easy", "Cost control",
  "Run tasks in order; each costs <code>tokens[task]</code>. Skip a task that would push the total past <code>budget</code>, but keep trying smaller later tasks. Return <code>(done tasks, tokens used)</code>.",
  [(({"plan": 2000, "research": 9000, "draft": 4000, "polish": 1500}, 8000), (['plan', 'draft', 'polish'], 7500))],
  ("A running total in a loop.", "O(n)", "O(n)"),
  ("Same loop; a list comprehension can't carry the running total cleanly, so a loop is the right tool.", "O(n)", "O(n)"),
  viz=({"plan": 2000, "research": 9000, "draft": 4000, "polish": 1500}, 8000))


@B
def within_budget(tokens, budget):
    done, used = [], 0
    for task, cost in tokens.items():
        if used + cost <= budget:
            done.append(task)
            used += cost
    return (done, used)


@O
def within_budget(tokens, budget):
    done, used = [], 0
    for task, cost in tokens.items():
        if used + cost > budget:
            continue
        done.append(task)
        used += cost
    return (done, used)


Q(None, "What Do Extra Agents Cost?", "Medium", "Token multiplication",
  "One agent solving a task reads <code>context</code> tokens once and writes <code>output</code>. An orchestrator with <code>n</code> workers: the orchestrator reads the context and writes a plan of <code>plan</code> tokens; each worker reads the context plus the plan and writes <code>output</code>; the orchestrator then reads all worker outputs and writes <code>output</code>. Return <code>(single total, multi total, ratio rounded to 1)</code>.",
  [((20000, 1000, 500, 4), (21000, 111500, 5.3)), ((2000, 800, 300, 3), (2800, 14800, 5.3))],
  ("Add up each agent's reads and writes step by step.", "O(n)", "O(1)"),
  ("A closed-form expression.", "O(1)", "O(1)"),
  viz=((20000, 1000, 500, 4)))


@B
def multi_cost(context, output, plan, n):
    single = context + output
    total = context + plan
    for _ in range(n):
        total += context + plan + output
    total += n * output + output
    return (single, total, round(total / single, 1))


@O
def multi_cost(context, output, plan, n):
    single = context + output
    multi = (context + plan) + n * (context + plan + output) + (n * output + output)
    return (single, multi, round(multi / single, 1))


Q(None, "Catch an Agent Going in Circles", "Easy", "Loop detection",
  "Return the index of the first step whose <code>(tool, argument)</code> already happened earlier — a sign the agent is stuck — or -1.",
  [(([("search", "mcp"), ("read", "a.md"), ("search", "mcp spec"), ("read", "a.md")],), 3), (([("a", 1), ("b", 2)],), -1)],
  ("Compare with every earlier step.", "O(n²)", "O(1)"),
  ("A set of seen steps.", "O(n)", "O(n)"),
  viz=([("search", "mcp"), ("read", "a.md"), ("search", "mcp spec"), ("read", "a.md")],))


@B
def first_repeat(steps):
    for i in range(len(steps)):
        for j in range(i):
            if steps[j] == steps[i]:
                return i
    return -1


@O
def first_repeat(steps):
    seen = set()
    for i, s in enumerate(steps):
        if s in seen:
            return i
        seen.add(s)
    return -1


Q(None, "Each Agent Only Gets Its Own Tools", "Easy", "Least privilege",
  "<code>allowed[agent]</code> lists the tools an agent may use. Return the calls <code>(agent, tool)</code> that must be refused, in order.",
  [(({"researcher": ["search", "read"], "writer": ["write_file"]}, [("researcher", "search"), ("writer", "search"), ("researcher", "write_file"), ("writer", "write_file")]), [('writer', 'search'), ('researcher', 'write_file')])],
  ("A loop with an if.", "O(c)", "O(c)"),
  ("Convert to sets once; a comprehension filters.", "O(c)", "O(a + c)"),
  viz=({"researcher": ["search", "read"], "writer": ["write_file"]}, [("researcher", "search"), ("writer", "search")]))


@B
def refused(allowed, calls):
    out = []
    for agent, tool in calls:
        if tool not in allowed.get(agent, []):
            out.append((agent, tool))
    return out


@O
def refused(allowed, calls):
    sets = {a: set(t) for a, t in allowed.items()}
    return [(a, t) for a, t in calls if t not in sets.get(a, set())]


Q(None, "Workers That Time Out", "Easy", "Partial results",
  "Fan out to workers that take <code>secs</code> seconds each; wait at most <code>timeout</code>. Return <code>(finished workers, timed-out workers)</code>, each list sorted. A good orchestrator answers with partial results instead of waiting forever.",
  [(({"news": 2.5, "sales": 7.0, "weather": 1.2, "stocks": 5.0}, 5.0), (['news', 'stocks', 'weather'], ['sales']))],
  ("Two lists filled in a loop.", "O(n log n)", "O(n)"),
  ("Two sorted comprehensions.", "O(n log n)", "O(n)"),
  viz=({"news": 2.5, "sales": 7.0, "weather": 1.2, "stocks": 5.0}, 5.0))


@B
def with_timeout(secs, timeout):
    done, late = [], []
    for w, s in secs.items():
        if s <= timeout:
            done.append(w)
        else:
            late.append(w)
    return (sorted(done), sorted(late))


@O
def with_timeout(secs, timeout):
    return (sorted(w for w, s in secs.items() if s <= timeout), sorted(w for w, s in secs.items() if s > timeout))


Q(None, "Map–Reduce Over a Long Document", "Medium", "How many model calls?",
  "Summarise <code>n_chunks</code> chunks: one call per chunk (map), then combine summaries <code>fan_in</code> at a time, level after level, until one remains (reduce). Return <code>(map calls, reduce calls, reduce levels)</code>.",
  [((40, 5), (40, 11, 3)), ((1, 5), (1, 0, 0)), ((26, 5), (26, 9, 3))],
  ("Simulate each level: ⌈k / fan_in⌉ calls until k = 1.", "O(log n)", "O(1)"),
  ("Same loop with <code>-(-k // fan_in)</code> for ceiling division.", "O(log n)", "O(1)"),
  viz=((26, 5)))


@B
def map_reduce(n_chunks, fan_in):
    k, calls, levels = n_chunks, 0, 0
    while k > 1:
        groups = k // fan_in
        if k % fan_in:
            groups += 1
        calls += groups
        levels += 1
        k = groups
    return (n_chunks, calls, levels)


@O
def map_reduce(n_chunks, fan_in):
    k, calls, levels = n_chunks, 0, 0
    while k > 1:
        k = -(-k // fan_in)
        calls, levels = calls + k, levels + 1
    return (n_chunks, calls, levels)


Q(None, "Hand Off Only What's Needed", "Easy", "Context on handoff",
  "When agent A hands off to agent B, send a summary (<code>summary_tokens</code>) plus only the last <code>k</code> messages, instead of the whole history. Return <code>(tokens if sending everything, tokens sent, % saved rounded to 1)</code>.",
  [(([1200, 800, 3000, 450, 600, 900], 2, 300), (6950, 1800, 74.1))],
  ("Add up in loops.", "O(n)", "O(1)"),
  ("<code>sum</code> with slicing.", "O(n)", "O(1)"),
  viz=([1200, 800, 3000, 450, 600, 900], 2, 300))


@B
def handoff_tokens(messages, k, summary_tokens):
    full = 0
    for m in messages:
        full += m
    sent = summary_tokens
    for m in messages[len(messages) - k:]:
        sent += m
    return (full, sent, round((full - sent) / full * 100, 1))


@O
def handoff_tokens(messages, k, summary_tokens):
    full, sent = sum(messages), summary_tokens + sum(messages[-k:])
    return (full, sent, round((full - sent) / full * 100, 1))


Q(None, "A Pool of Workers", "Hard", "Concurrency limits",
  "<code>n</code> workers take tasks in the given order; each task starts on whichever worker frees up first. Return the time all tasks finish (rate limits often cap concurrency like this).",
  [(([5, 3, 8, 2, 4, 6], 2), 17), (([5, 3, 8, 2, 4, 6], 3), 11), (([4, 4], 5), 4)],
  ("Track each worker's free time in a list and pick the minimum each time.", "O(t · n)", "O(n)"),
  ("A min-heap of free times.", "O(t log n)", "O(n)"),
  viz=([5, 3, 8, 2, 4, 6], 2))


@B
def pool_finish(durations, n):
    free = [0] * n
    for d in durations:
        i = free.index(min(free))
        free[i] += d
    return max(free)


@O
def pool_finish(durations, n):
    heap = [0] * n
    for d in durations:
        heapq.heappush(heap, heapq.heappop(heap) + d)
    return max(heap)


GRAPH = {"start": lambda s: "draft",
         "draft": lambda s: "review",
         "review": lambda s: "publish" if s["score"] >= 8 else ("draft" if s["rounds"] < 3 else "escalate"),
         "publish": lambda s: None, "escalate": lambda s: None}


Q(None, "Run a Graph Workflow", "Hard", "State machines (LangGraph style)",
  "Run the workflow <code>GRAPH</code>: each node is a function of the state returning the next node or None. Visiting 'draft' adds 1 to <code>rounds</code> and sets <code>score</code> to the next value from <code>scores</code>. Return the list of nodes visited.",
  [(([5, 9],), ['start', 'draft', 'review', 'draft', 'review', 'publish']), (([4, 5, 6, 7],), ['start', 'draft', 'review', 'draft', 'review', 'draft', 'review', 'escalate'])],
  ("A while loop with if-statements for the node's side effects.", "O(steps)", "O(steps)"),
  ("A table of node actions plus the same loop — how graph frameworks separate state updates from routing.", "O(steps)", "O(steps)"),
  viz=(([5, 9],)))


@B
def run_graph(scores):
    state = {"rounds": 0, "score": 0}
    it = iter(scores)
    node, path = "start", []
    while node is not None:
        path.append(node)
        if node == "draft":
            state["rounds"] += 1
            state["score"] = next(it)
        node = GRAPH[node](state)
    return path


@O
def run_graph(scores):
    it = iter(scores)
    actions = {"draft": lambda s: s.update(rounds=s["rounds"] + 1, score=next(it))}
    state, node, path = {"rounds": 0, "score": 0}, "start", []
    while node:
        path.append(node)
        actions.get(node, lambda s: None)(state)
        node = GRAPH[node](state)
    return path


Q(None, "Merge Sources From Workers", "Easy", "Citations",
  "Each worker returns the sources it used. Return one de-duplicated list in order of first appearance.",
  [(([["kb/1", "kb/4"], ["kb/4", "web/2"], [], ["kb/1", "kb/9"]],), ['kb/1', 'kb/4', 'web/2', 'kb/9'])],
  ("A list plus a membership check.", "O(n²)", "O(n)"),
  ("<code>dict.fromkeys</code> keeps first-seen order and removes duplicates.", "O(n)", "O(n)"),
  viz=([["kb/1", "kb/4"], ["kb/4", "web/2"], [], ["kb/1", "kb/9"]],))


@B
def merge_sources(lists):
    out = []
    for lst in lists:
        for s in lst:
            if s not in out:
                out.append(s)
    return out


@O
def merge_sources(lists):
    return list(dict.fromkeys(s for lst in lists for s in lst))


Q(None, "Pick the Simplest Pattern That Works", "Easy", "Design judgement",
  "Choose a pattern from a task's traits, checking in this order: if <code>steps_known</code> and not <code>needs_tools</code> → 'single call'; if <code>steps_known</code> → 'prompt chain'; if <code>categories</code> → 'router'; if <code>independent_parts</code> → 'parallel fan-out'; if <code>needs_quality_loop</code> → 'evaluator-optimizer'; otherwise 'autonomous agent'.",
  [(({"steps_known": True, "needs_tools": False},), 'single call'), (({"categories": True},), 'router'),
   (({"independent_parts": True, "needs_quality_loop": True},), 'parallel fan-out'), (({},), 'autonomous agent')],
  ("An if-chain with <code>.get(key, False)</code>.", "O(1)", "O(1)"),
  ("An ordered list of (condition, pattern) rules and <code>next</code>.", "O(r)", "O(r)"),
  viz=({"categories": True},))


@B
def choose_pattern(traits):
    if traits.get("steps_known", False) and not traits.get("needs_tools", False):
        return "single call"
    if traits.get("steps_known", False):
        return "prompt chain"
    if traits.get("categories", False):
        return "router"
    if traits.get("independent_parts", False):
        return "parallel fan-out"
    if traits.get("needs_quality_loop", False):
        return "evaluator-optimizer"
    return "autonomous agent"


@O
def choose_pattern(traits):
    t = lambda k: traits.get(k, False)
    rules = [(t("steps_known") and not t("needs_tools"), "single call"), (t("steps_known"), "prompt chain"),
             (t("categories"), "router"), (t("independent_parts"), "parallel fan-out"),
             (t("needs_quality_loop"), "evaluator-optimizer")]
    return next((name for ok, name in rules if ok), "autonomous agent")
