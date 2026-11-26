import numpy as np
import pandas as pd

ISSUES = {
    "bug": ["app crashes when opening the cart", "checkout button does nothing", "images fail to load on the product page",
            "search shows no results for valid items"],
    "billing": ["charged twice for one order", "refund not received after return", "coupon discount not applied",
                "invoice shows the wrong GST amount"],
    "delivery": ["order delayed by more than a week", "parcel marked delivered but not received",
                 "courier did not come for the pickup", "wrong item delivered"],
    "login": ["OTP not received on mobile", "cannot reset the password", "account locked after failed attempts"],
}


def make_data(rng):
    rows = []
    products = ["App", "Web", "Payments", "Delivery"]
    for i in range(1, 241):
        cat = rng.choice(list(ISSUES), p=[0.32, 0.26, 0.28, 0.14])
        product = {"bug": rng.choice(["App", "Web"], p=[0.7, 0.3]), "billing": "Payments",
                   "delivery": "Delivery", "login": rng.choice(["App", "Web"])}[cat]
        text = rng.choice(ISSUES[cat])
        priority = rng.choice(["low", "medium", "high"], p=[0.3, 0.45, 0.25] if cat != "billing" else [0.15, 0.4, 0.45])
        status = rng.choice(["open", "closed"], p=[0.45, 0.55])
        rows.append((f"T{i:03d}", product, cat, priority, status, int(rng.integers(1, 61)), text))
    return {"support_tickets.csv": pd.DataFrame(rows, columns=["ticket_id", "product", "category", "priority", "status", "day", "text"])}


PROJECT = dict(
    slug="mcp-multi-agent-assistant",
    title="Multi-Agent Support Analyst over an MCP Server",
    role="AI Engineer",
    level="Advanced",
    hours="8–10",
    summary="Expose a ticket database through your own MCP server, then build an orchestrator with research and writer agents that call it, a reviewer that rejects uncited claims, and tracing of every tool call — with an optional real Claude agent loop.",
    skills=["MCP", "JSON-RPC", "tool schemas", "multi-agent orchestration", "citations", "reviewer agents", "tracing", "Claude API tool use"],
    brief="""
**The situation.** *ShopKart*'s head of customer support asks every Monday: *"What are customers complaining about, which issues are most urgent, and where should engineering look first?"* Today an analyst spends half a day reading tickets.

You'll build an AI system that answers it, the way modern AI products are built:

1. An **MCP server** that exposes the ticket database as tools any AI host can use (Claude Desktop, Claude Code, your own agent).
2. An **MCP client** that talks to it over JSON-RPC.
3. A **multi-agent** pipeline: an orchestrator fans out to research agents, a writer drafts the report with citations, and a reviewer rejects any claim without a source.
4. **Tracing** of every tool call, so you can see what the agents did.

Everything runs offline with deterministic stand-ins for the model; the last section swaps in a real Claude agent loop if you have an API key.
""",
    deliverable="an MCP server (tools/list and tools/call over JSON-RPC), a client, an orchestrator with research, writer and reviewer agents, a cited Monday report, and a trace summary — plus the same server packaged as a real MCP server file.",
    data_notes="""
**support_tickets.csv** — 240 tickets from the last 60 days:

| Column | Meaning |
|---|---|
| ticket_id | T001 … T240 |
| product | App, Web, Payments, Delivery |
| category | bug, billing, delivery, login |
| priority | low, medium, high |
| status | open, closed |
| day | 1 … 60 |
| text | the customer's issue, in short |

The tools below are given — your job is the protocol, the agents and the checks around them.
""",
    setup="""
import inspect, json, re, time
from collections import Counter
tickets = load("support_tickets.csv")


def search_tickets(query: str, limit: int = 5) -> str:
    \"\"\"Search open tickets by keywords; most matching words first.\"\"\"
    words = set(re.findall(r"[a-z]+", query.lower()))
    scored = []
    for row in tickets[tickets.status == "open"].itertuples():
        hits = len(words & set(re.findall(r"[a-z]+", row.text.lower() + " " + row.category + " " + row.product.lower())))
        if hits:
            scored.append((-hits, row.ticket_id, row))
    scored.sort()
    return json.dumps([{"id": r.ticket_id, "product": r.product, "priority": r.priority, "text": r.text} for _, _, r in scored[:limit]])


def ticket_counts(field: str) -> str:
    \"\"\"Count open tickets by a field: product, category or priority.\"\"\"
    if field not in ("product", "category", "priority"):
        raise ValueError(f"unknown field: {field}")
    return json.dumps(tickets[tickets.status == "open"][field].value_counts().sort_index().to_dict())


def get_ticket(ticket_id: str) -> str:
    \"\"\"Full details of one ticket.\"\"\"
    row = tickets[tickets.ticket_id == ticket_id]
    if row.empty:
        raise KeyError(f"no ticket {ticket_id}")
    return row.iloc[0].to_json()


TOOLS = {"search_tickets": search_tickets, "ticket_counts": ticket_counts, "get_ticket": get_ticket}


# Used by the last check: one full run of your pipeline.
def run_pipeline():
    TRACE.clear()
    findings, sources = orchestrate(["charged twice refund", "parcel not delivered", "app crashes cart"])
    counts = call("ticket_counts", {"field": "category"})
    report = write_report(findings, counts)
    review(report, sources)
    call("ticket_counts", {"field": "category"})   # the orchestrator asks twice: a wasted repeat
    return trace_summary(TRACE)
""",
    milestones=[
        dict(title="Describe the tools (tools/list)",
             task="""
An MCP server tells clients what tools it has. Write `list_tools()` returning one entry per function in `TOOLS` (in that order):
`{"name": …, "description": first line of the docstring, "inputSchema": {"type": "object", "properties": {param: {"type": …}}, "required": [params without defaults]}}` — with Python types mapped str → "string", int → "integer".
""",
             hint="`inspect.signature(fn).parameters.values()` gives each parameter's `.annotation` and `.default` (which is `inspect.Parameter.empty` when there is none). `inspect.getdoc(fn)` gives the docstring.",
             starter="""
def list_tools():
    raise NotImplementedError
""",
             solution="""
def list_tools():
    types = {str: "string", int: "integer", float: "number", bool: "boolean"}
    out = []
    for name, fn in TOOLS.items():
        params = list(inspect.signature(fn).parameters.values())
        out.append({"name": name, "description": inspect.getdoc(fn).splitlines()[0],
                    "inputSchema": {"type": "object",
                                    "properties": {p.name: {"type": types[p.annotation]} for p in params},
                                    "required": [p.name for p in params if p.default is inspect.Parameter.empty]}})
    return out
""",
             call="list_tools()", tol=1e-9),
        dict(title="The server: handle JSON-RPC messages",
             task="""
Write `handle(raw)` — the heart of an MCP server. It receives one JSON-RPC message as text and returns the reply as text, or `None` for notifications (no `id`):
- invalid JSON → error `-32700`; `initialize` → result `{"protocolVersion": "2025-06-18", "capabilities": {"tools": {}}, "serverInfo": {"name": "tickets", "version": "1.0"}}`
- `tools/list` → `{"tools": list_tools()}`
- `tools/call` → `{"content": [{"type": "text", "text": <tool output>}], "isError": False}`; if the tool raises, the same shape with the error message and `"isError": True`
- anything else → error `-32601` with message `"Method not found"`.

Replies look like `{"jsonrpc": "2.0", "id": …, "result": …}` or `{"jsonrpc": "2.0", "id": …, "error": {"code": …, "message": …}}` (use id `None` when the JSON couldn't be parsed).
""",
             starter="""
def handle(raw):
    raise NotImplementedError
""",
             solution="""
def handle(raw):
    try:
        msg = json.loads(raw)
    except json.JSONDecodeError:
        return json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}})
    if "id" not in msg:
        return None
    method, params = msg.get("method"), msg.get("params", {})
    if method == "initialize":
        result = {"protocolVersion": "2025-06-18", "capabilities": {"tools": {}}, "serverInfo": {"name": "tickets", "version": "1.0"}}
    elif method == "tools/list":
        result = {"tools": list_tools()}
    elif method == "tools/call":
        try:
            text, is_error = TOOLS[params["name"]](**params.get("arguments", {})), False
        except Exception as e:
            text, is_error = f"{type(e).__name__}: {e}", True
        result = {"content": [{"type": "text", "text": text}], "isError": is_error}
    else:
        return json.dumps({"jsonrpc": "2.0", "id": msg["id"], "error": {"code": -32601, "message": "Method not found"}})
    return json.dumps({"jsonrpc": "2.0", "id": msg["id"], "result": result})
""",
             call="""[json.loads(handle('{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}'))["result"]["protocolVersion"],
 handle('{"jsonrpc":"2.0","method":"notifications/initialized"}'),
 len(json.loads(handle('{"jsonrpc":"2.0","id":2,"method":"tools/list"}'))["result"]["tools"]),
 json.loads(handle(json.dumps({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "ticket_counts", "arguments": {"field": "priority"}}})))["result"],
 json.loads(handle(json.dumps({"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "ticket_counts", "arguments": {"field": "colour"}}})))["result"]["isError"],
 json.loads(handle('{"jsonrpc":"2.0","id":5,"method":"tools/delete"}'))["error"]["code"],
 json.loads(handle("{oops"))["error"]["code"]]""".replace("\n", ""), tol=1e-9),
        dict(title="The client: call tools over the protocol",
             task="""
Agents never touch `TOOLS` directly; they go through the protocol, exactly as they would with a remote server. Write `call(name, arguments)`:
1. build a `tools/call` request with a new id each time (use the global counter `NEXT_ID`, starting at 100),
2. send its JSON text to `handle`, parse the reply,
3. return the parsed JSON of the tool's text output — or raise `RuntimeError(text)` if `isError` is true.

Also record every call in the list `TRACE` as `(name, arguments)`; you'll use it later.
""",
             starter="""
NEXT_ID = 100
TRACE = []


def call(name, arguments):
    raise NotImplementedError
""",
             solution="""
NEXT_ID = 100
TRACE = []


def call(name, arguments):
    global NEXT_ID
    NEXT_ID += 1
    request = {"jsonrpc": "2.0", "id": NEXT_ID, "method": "tools/call", "params": {"name": name, "arguments": arguments}}
    TRACE.append((name, arguments))
    reply = json.loads(handle(json.dumps(request)))
    block = reply["result"]
    text = block["content"][0]["text"]
    if block["isError"]:
        raise RuntimeError(text)
    return json.loads(text)
""",
             call="[call('ticket_counts', {'field': 'category'}), [t['id'] for t in call('search_tickets', {'query': 'refund not received', 'limit': 3})]]", tol=1e-9),
        dict(title="Research agents, fanned out",
             task="""
The orchestrator gives each research agent one topic. A research agent searches tickets for its topic (limit 5) and returns `{"topic": …, "count": number found, "high": ids of high-priority matches, "sources": all ids found}`.

Write `research(topic)` and `orchestrate(topics)`, which runs `research` for every topic and returns `(list of findings, all sources de-duplicated in first-seen order)`.
""",
             hint="`dict.fromkeys(...)` de-duplicates while keeping order.",
             starter="""
def research(topic):
    raise NotImplementedError


def orchestrate(topics):
    raise NotImplementedError
""",
             solution="""
def research(topic):
    found = call("search_tickets", {"query": topic, "limit": 5})
    return {"topic": topic, "count": len(found), "high": [t["id"] for t in found if t["priority"] == "high"],
            "sources": [t["id"] for t in found]}


def orchestrate(topics):
    findings = [research(t) for t in topics]
    sources = list(dict.fromkeys(s for f in findings for s in f["sources"]))
    return findings, sources
""",
             call="orchestrate(['charged twice refund', 'parcel not delivered', 'app crashes cart'])", tol=1e-9,
             after="Here the agents run one after another. Because they're independent, a real orchestrator runs them in parallel (`asyncio.gather` or a thread pool), so total time is the slowest agent, not the sum."),
        dict(title="A writer agent with citations",
             task="""
Write `write_report(findings, counts)` that returns the Monday report as text:
- first line: `"Open tickets by category: "` followed by `category n` pairs from `counts`, joined with `", "`,
- then one line per finding: `"- <topic>: <count> open tickets, <k> high priority [T001, T002]"`, citing that finding's high-priority ids (or all its sources if there are none).

Every claim must carry its sources — that's what lets a reviewer (and the support head) check it.
""",
             starter="""
def write_report(findings, counts):
    raise NotImplementedError
""",
             solution="""
def write_report(findings, counts):
    lines = ["Open tickets by category: " + ", ".join(f"{k} {v}" for k, v in counts.items())]
    for f in findings:
        cite = f["high"] or f["sources"]
        lines.append(f"- {f['topic']}: {f['count']} open tickets, {len(f['high'])} high priority [{', '.join(cite)}]")
    return "\\n".join(lines)
""",
             call="write_report(*[orchestrate(['charged twice refund', 'parcel not delivered'])[0]], call('ticket_counts', {'field': 'category'})).splitlines()", tol=1e-9),
        dict(title="A reviewer agent that rejects unsupported claims",
             task="""
Write `review(report, allowed_ids)` returning a sorted list of problems:
- `"uncited: <line>"` for every line starting with `"- "` that has no `[T…]` citation,
- `"unknown source: T…"` for every cited id not in `allowed_ids` (a hallucinated source).

An empty list means the report can be published. The check reviews your real report and a doctored one.
""",
             hint="`re.findall(r'T\\d{3}', line)` finds ids.",
             starter="""
def review(report, allowed_ids):
    raise NotImplementedError
""",
             solution="""
def review(report, allowed_ids):
    problems = set()
    allowed = set(allowed_ids)
    for line in report.splitlines():
        ids = re.findall(r"T\\d{3}", line)
        if line.startswith("- ") and not ids:
            problems.add(f"uncited: {line}")
        problems.update(f"unknown source: {i}" for i in ids if i not in allowed)
    return sorted(problems)
""",
             call="""(lambda f, s: [review(write_report(f, call('ticket_counts', {'field': 'category'})), s), review("Top issue\\n- refunds are slow\\n- login fails [T999]", s)])(*orchestrate(['charged twice refund', 'parcel not delivered']))""", tol=1e-9),
        dict(title="What did the agents do? A trace summary",
             task="""
Write `trace_summary(trace)` returning `{"calls": total tool calls, "by_tool": {tool: count} sorted by tool name, "repeated": number of calls that exactly repeat an earlier (tool, arguments)}`. Repeats are wasted work — a sign an agent should cache or remember results.

The check resets `TRACE`, runs one full pipeline, and summarises it.
""",
             hint="Turn arguments into a hashable key with `json.dumps(args, sort_keys=True)`.",
             starter="""
def trace_summary(trace):
    raise NotImplementedError
""",
             solution="""
def trace_summary(trace):
    keys = [(name, json.dumps(args, sort_keys=True)) for name, args in trace]
    return {"calls": len(trace), "by_tool": dict(sorted(Counter(n for n, _ in trace).items())),
            "repeated": len(keys) - len(set(keys))}

""",
             call="run_pipeline()", tol=1e-9),
    ],
    extra=[
        ("## Run it as a real MCP server\n\nThe official Python SDK does the protocol work you just wrote by hand. Save this as `tickets_server.py` next to the CSV, install with `pip install mcp pandas`, and connect it to Claude Code with `claude mcp add tickets -- python tickets_server.py` (or add it to Claude Desktop's config). SDK import paths differ between versions — check the docs for the one you install.\n\n```python\nimport json, pandas as pd\nfrom mcp.server.fastmcp import FastMCP     # SDK v1; v2 renames it to MCPServer (mcp.server.mcpserver)\n\nmcp = FastMCP(\"tickets\")\ntickets = pd.read_csv(\"support_tickets.csv\")\n\n@mcp.tool()\ndef ticket_counts(field: str) -> str:\n    \"\"\"Count open tickets by a field: product, category or priority.\"\"\"\n    return json.dumps(tickets[tickets.status == \"open\"][field].value_counts().to_dict())\n\nif __name__ == \"__main__\":\n    mcp.run()\n```", None),
        ("## Optional: let Claude drive the tools\n\nReplace the scripted agents with a real model: give Claude the tools (converted from your `list_tools()`) and run the agent loop, sending every tool call through your MCP client. Needs an Anthropic API key and costs a few cents.", '''
import os, importlib.util
if os.environ.get("ANTHROPIC_API_KEY") and importlib.util.find_spec("anthropic"):
    import anthropic
    client = anthropic.Anthropic()
    claude_tools = [{"name": t["name"], "description": t["description"], "input_schema": t["inputSchema"]} for t in list_tools()]
    messages = [{"role": "user", "content": "Which issues should engineering look at first this week? Cite ticket ids."}]
    for _ in range(8):
        reply = client.messages.create(model="claude-opus-5-5", max_tokens=1500, tools=claude_tools, messages=messages)
        messages.append({"role": "assistant", "content": reply.content})
        if reply.stop_reason != "tool_use":
            break
        results = []
        for block in reply.content:
            if block.type == "tool_use":
                try:
                    out = json.dumps(call(block.name, block.input))
                except RuntimeError as e:
                    out = str(e)
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": out})
        messages.append({"role": "user", "content": results})
    print("".join(b.text for b in reply.content if b.type == "text"))
else:
    print("No API key or anthropic package — the scripted agents above already show the full pipeline.")
''')],
    present="""
Write a short design document (your README):

1. **Architecture diagram**: MCP server ↔ client ↔ orchestrator → research agents → writer → reviewer, with tracing.
2. **The tools**: names, schemas and why each exists.
3. **The Monday report** your pipeline produced, and the reviewer's verdict.
4. **Trace**: how many tool calls, and the wasted repeat — how you'd remove it (caching, shared memory).
5. **Security**: read-only tools, no destructive operations, tool output treated as data (prompt injection).
6. **Next steps**: real Claude agents, parallel research, an evaluation set of weekly questions.
""",
    resume=[
        "Built an MCP server exposing a support-ticket database as typed tools over JSON-RPC, usable from Claude Desktop and Claude Code",
        "Designed a multi-agent pipeline (orchestrator, research, writer and reviewer agents) producing cited weekly reports, with a reviewer that rejects uncited or hallucinated sources",
        "Added tracing of every tool call, finding **X%** redundant calls, and an optional Claude agent loop driving the same MCP tools",
    ],
    interview=[
        "Why put the tools behind MCP instead of calling Python functions directly?",
        "Walk me through what happens on the wire when an agent calls a tool.",
        "How does your reviewer stop hallucinated citations? What can it still miss?",
        "When is multi-agent worth it here, and when would one agent be better?",
        "How would you secure this server before exposing it to other teams?",
        "How would you evaluate the weekly report's quality over time?",
    ],
    extensions=[
        "Run the research agents in parallel with asyncio and measure the speed-up.",
        "Add a `resources` endpoint that serves the weekly report itself by URI.",
        "Cache tool results in the client to remove repeated calls.",
        "Build an eval set of 20 weekly questions with expected ticket ids and score the pipeline.",
    ],
)
