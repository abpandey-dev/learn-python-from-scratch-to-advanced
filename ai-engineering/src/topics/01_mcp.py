from lib import *
import inspect
import json
import re


TOPIC(
    id="mcp", title="MCP: Connecting AI to Tools and Data", glyph="⇄",
    blurb="The Model Context Protocol from the wire up: JSON-RPC messages, the stdio transport, the initialize handshake, tools, resources and prompts, input-schema validation, errors, pagination, permissions, and turning MCP tools into LLM tool definitions.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py"># Every MCP message is JSON-RPC 2.0
{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_weather", "arguments": {"city": "Pune"}}}
{"jsonrpc": "2.0", "id": 1, "result": {"content": [{"type": "text", "text": "31°C"}], "isError": false}}
{"jsonrpc": "2.0", "method": "notifications/initialized"}            # no id = notification
{"jsonrpc": "2.0", "id": 7, "error": {"code": -32601, "message": "Method not found"}}

# Lifecycle: initialize → notifications/initialized → tools/list, tools/call, resources/read, prompts/get …
# stdio transport: one JSON message per line on stdin / stdout</code></pre>
<p>Servers expose three things: <b>tools</b> (the model calls them), <b>resources</b> (data the app reads, addressed by URI) and <b>prompts</b> (reusable templates the user picks).</p>
""")


Q(None, "Write a JSON-RPC Request", "Easy", "Message shape",
  "Return the JSON text of a JSON-RPC 2.0 request with keys in this order: <code>jsonrpc</code>, <code>id</code>, <code>method</code>, <code>params</code> (omit <code>params</code> if it is None).",
  [((1, "tools/list", None), '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}'), ((2, "tools/call", {"name": "add", "arguments": {"a": 2, "b": 3}}), '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "add", "arguments": {"a": 2, "b": 3}}}')],
  ("Build the text by hand with string pieces.", "O(n)", "O(n)"),
  ("Build a dict and <code>json.dumps</code> it — insertion order is kept.", "O(n)", "O(n)"),
  viz=(2, "tools/call", {"name": "add", "arguments": {"a": 2, "b": 3}}))


@B
def request(msg_id, method, params):
    text = '{"jsonrpc": "2.0", "id": ' + str(msg_id) + ', "method": "' + method + '"'
    if params is not None:
        text += ', "params": ' + json.dumps(params)
    return text + "}"


@O
def request(msg_id, method, params):
    msg = {"jsonrpc": "2.0", "id": msg_id, "method": method}
    if params is not None:
        msg["params"] = params
    return json.dumps(msg)


Q(None, "Read Messages from stdio", "Easy", "Newline-delimited JSON",
  "The stdio transport sends one JSON message per line. Given the raw text read from stdout, return the <code>method</code> of each message that has one (skip blank lines and responses).",
  [(('{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}\n\n{"jsonrpc":"2.0","method":"notifications/initialized"}\n{"jsonrpc":"2.0","id":1,"result":{}}\n',), ['initialize', 'notifications/initialized'])],
  ("Split on newlines, skip empties, parse each and collect methods.", "O(n)", "O(n)"),
  ("A comprehension over <code>splitlines()</code>.", "O(n)", "O(n)"),
  viz=('{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}\n{"jsonrpc":"2.0","method":"notifications/initialized"}\n',))


@B
def methods(stream):
    out = []
    for line in stream.split("\n"):
        line = line.strip()
        if line == "":
            continue
        msg = json.loads(line)
        if "method" in msg:
            out.append(msg["method"])
    return out


@O
def methods(stream):
    msgs = [json.loads(l) for l in stream.splitlines() if l.strip()]
    return [m["method"] for m in msgs if "method" in m]


Q(None, "What Kind of Message Is This?", "Easy", "Requests, notifications, responses",
  "Return 'request' (method and id), 'notification' (method, no id), 'result' (id and result), 'error' (id and error) or 'invalid'.",
  [(({"jsonrpc": "2.0", "id": 3, "method": "tools/list"},), 'request'), (({"jsonrpc": "2.0", "method": "notifications/progress"},), 'notification'),
   (({"jsonrpc": "2.0", "id": 3, "result": {}},), 'result'), (({"jsonrpc": "2.0", "id": 3, "error": {"code": -32601}},), 'error'), (({"id": 1},), 'invalid')],
  ("An if-chain on which keys exist.", "O(1)", "O(1)"),
  ("Map the set of present keys to a kind with a small lookup table.", "O(1)", "O(1)"),
  viz=({"jsonrpc": "2.0", "method": "notifications/progress"},))


@B
def kind(msg):
    if "method" in msg and "id" in msg:
        return "request"
    if "method" in msg:
        return "notification"
    if "id" in msg and "result" in msg:
        return "result"
    if "id" in msg and "error" in msg:
        return "error"
    return "invalid"


@O
def kind(msg):
    shape = frozenset(k for k in ("id", "method", "result", "error") if k in msg)
    table = {frozenset({"id", "method"}): "request", frozenset({"method"}): "notification",
             frozenset({"id", "result"}): "result", frozenset({"id", "error"}): "error"}
    return table.get(shape, "invalid")


ERRORS = {"parse": (-32700, "Parse error"), "invalid": (-32600, "Invalid Request"),
          "method": (-32601, "Method not found"), "params": (-32602, "Invalid params"), "internal": (-32603, "Internal error")}


Q(None, "Answer With the Right Error", "Easy", "JSON-RPC error codes",
  "A server receives <code>raw</code> text and knows <code>methods</code>. Return the error code to send back, or 0 if the request is fine: -32700 if it isn't JSON, -32600 if it has no <code>method</code> string, -32601 if the method is unknown.",
  [(('{"jsonrpc":"2.0","id":1,"method":"tools/list"}', ["tools/list", "tools/call"]), 0), (("{oops", ["tools/list"]), -32700),
   (('{"jsonrpc":"2.0","id":1}', ["tools/list"]), -32600), (('{"jsonrpc":"2.0","id":1,"method":"tools/delete"}', ["tools/list"]), -32601)],
  ("Nested try / if.", "O(n)", "O(n)"),
  ("Same checks, using the named <code>ERRORS</code> table so codes aren't magic numbers.", "O(n)", "O(n)"),
  viz=('{"jsonrpc":"2.0","id":1,"method":"tools/delete"}', ["tools/list"]))


@B
def error_code(raw, methods):
    try:
        msg = json.loads(raw)
    except ValueError:
        return -32700
    if not isinstance(msg, dict) or not isinstance(msg.get("method"), str):
        return -32600
    if msg["method"] not in methods:
        return -32601
    return 0


@O
def error_code(raw, methods):
    try:
        msg = json.loads(raw)
    except json.JSONDecodeError:
        return ERRORS["parse"][0]
    if not isinstance(msg, dict) or not isinstance(msg.get("method"), str):
        return ERRORS["invalid"][0]
    return 0 if msg["method"] in methods else ERRORS["method"][0]


SCHEMA = {"type": "object", "properties": {"city": {"type": "string"}, "days": {"type": "integer"},
                                            "units": {"type": "string", "enum": ["metric", "imperial"]}},
          "required": ["city"]}


Q(None, "Validate Tool Arguments", "Medium", "inputSchema",
  "Check <code>args</code> against a tool's JSON-Schema <code>inputSchema</code> (types string / integer / number / boolean, <code>enum</code>, <code>required</code>, no unknown keys). Return a sorted list of problems like <code>'missing: city'</code>, <code>'type: days'</code>, <code>'enum: units'</code>, <code>'unknown: x'</code>.",
  [((SCHEMA, {"city": "Pune", "days": 3}), []), ((SCHEMA, {"days": "3", "units": "kelvin", "x": 1}), ['enum: units', 'missing: city', 'type: days', 'unknown: x']), ((SCHEMA, {"city": "Goa", "days": True}), ['type: days'])],
  ("Loop over the schema and the arguments with if-statements.", "O(k)", "O(k)"),
  ("A type table <code>{'string': str, …}</code>; remember <code>bool</code> is a subclass of <code>int</code> in Python.", "O(k)", "O(k)"),
  viz=(SCHEMA, {"days": "3", "units": "kelvin", "x": 1}))


@B
def validate_args(schema, args):
    problems = []
    props = schema["properties"]
    for name in schema.get("required", []):
        if name not in args:
            problems.append("missing: " + name)
    for name, value in args.items():
        if name not in props:
            problems.append("unknown: " + name)
            continue
        t = props[name]["type"]
        ok = False
        if t == "string":
            ok = isinstance(value, str)
        elif t == "integer":
            ok = isinstance(value, int) and not isinstance(value, bool)
        elif t == "number":
            ok = isinstance(value, (int, float)) and not isinstance(value, bool)
        elif t == "boolean":
            ok = isinstance(value, bool)
        if not ok:
            problems.append("type: " + name)
        elif "enum" in props[name] and value not in props[name]["enum"]:
            problems.append("enum: " + name)
    return sorted(problems)


@O
def validate_args(schema, args):
    types = {"string": (str,), "integer": (int,), "number": (int, float), "boolean": (bool,)}
    props = schema["properties"]
    problems = [f"missing: {n}" for n in schema.get("required", []) if n not in args]
    for name, value in args.items():
        spec = props.get(name)
        if spec is None:
            problems.append(f"unknown: {name}")
        elif not isinstance(value, types[spec["type"]]) or (isinstance(value, bool) and spec["type"] != "boolean"):
            problems.append(f"type: {name}")
        elif value not in spec.get("enum", [value]):
            problems.append(f"enum: {name}")
    return sorted(problems)


def get_weather(city: str, days: int = 1) -> str:
    """Forecast for a city.

    Longer notes the model doesn't need."""
    return f"{city}: sunny for {days} day(s)"


def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


FUNCS = {"get_weather": get_weather, "add": add}


Q(None, "Describe Python Functions as Tools", "Medium", "tools/list from code",
  "Build the <code>tools/list</code> entries for the Python functions named in <code>fn_names</code> (look them up in <code>FUNCS</code>), like an MCP SDK's <code>@tool</code> decorator does: name, the docstring's first line as description, and an <code>inputSchema</code> from the type hints (str → string, int → integer, float → number, bool → boolean). Parameters without defaults are required.",
  [((["get_weather", "add"],), [{'name': 'get_weather', 'description': 'Forecast for a city.', 'inputSchema': {'type': 'object', 'properties': {'city': {'type': 'string'}, 'days': {'type': 'integer'}}, 'required': ['city']}}, {'name': 'add', 'description': 'Add two numbers.', 'inputSchema': {'type': 'object', 'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}}, 'required': ['a', 'b']}}])],
  ("Read <code>__annotations__</code>, <code>__defaults__</code> and the code object's argument names by hand.", "O(params)", "O(params)"),
  ("<code>inspect.signature</code> gives every parameter with its annotation and default.", "O(params)", "O(params)"),
  viz=(["get_weather"],))


@B
def describe_tools(fn_names):
    names = {str: "string", int: "integer", float: "number", bool: "boolean"}
    tools = []
    for f in [FUNCS[n] for n in fn_names]:
        argnames = f.__code__.co_varnames[:f.__code__.co_argcount]
        n_defaults = len(f.__defaults__ or ())
        props, required = {}, []
        for i, arg in enumerate(argnames):
            props[arg] = {"type": names[f.__annotations__[arg]]}
            if i < len(argnames) - n_defaults:
                required.append(arg)
        tools.append({"name": f.__name__, "description": f.__doc__.strip().split("\n")[0],
                      "inputSchema": {"type": "object", "properties": props, "required": required}})
    return tools


@O
def describe_tools(fn_names):
    names = {str: "string", int: "integer", float: "number", bool: "boolean"}
    tools = []
    for f in map(FUNCS.get, fn_names):
        params = inspect.signature(f).parameters.values()
        tools.append({
            "name": f.__name__,
            "description": inspect.getdoc(f).splitlines()[0],
            "inputSchema": {"type": "object",
                            "properties": {p.name: {"type": names[p.annotation]} for p in params},
                            "required": [p.name for p in params if p.default is inspect.Parameter.empty]},
        })
    return tools


Q(None, "Handle tools/call", "Medium", "Results and isError",
  "Run the named tool from <code>registry</code> with the arguments and return an MCP result: <code>{'content': [{'type': 'text', 'text': str(value)}], 'isError': False}</code>. Unknown tools or exceptions return the error text with <code>isError: True</code> — tool failures are results the model can read, not protocol errors.",
  [(({"name": "add", "arguments": {"a": 2, "b": 3.5}},), {'content': [{'type': 'text', 'text': '5.5'}], 'isError': False}), (({"name": "add", "arguments": {"a": 1}},), {'content': [{'type': 'text', 'text': "TypeError: add() missing 1 required positional argument: 'b'"}], 'isError': True}), (({"name": "rm", "arguments": {}},), {'content': [{'type': 'text', 'text': 'Unknown tool: rm'}], 'isError': True})],
  ("Look up, call, catch, and build the dict in two branches.", "O(1)", "O(1)"),
  ("A small helper that formats both outcomes the same way.", "O(1)", "O(1)"),
  viz=({"name": "add", "arguments": {"a": 2, "b": 3.5}},))


REGISTRY = {"add": add, "get_weather": get_weather}


@B
def call_tool(params):
    name = params["name"]
    if name not in REGISTRY:
        return {"content": [{"type": "text", "text": "Unknown tool: " + name}], "isError": True}
    try:
        value = REGISTRY[name](**params.get("arguments", {}))
    except Exception as e:
        return {"content": [{"type": "text", "text": type(e).__name__ + ": " + str(e)}], "isError": True}
    return {"content": [{"type": "text", "text": str(value)}], "isError": False}


@O
def call_tool(params):
    def result(text, is_error):
        return {"content": [{"type": "text", "text": text}], "isError": is_error}
    fn = REGISTRY.get(params["name"])
    if fn is None:
        return result(f"Unknown tool: {params['name']}", True)
    try:
        return result(str(fn(**params.get("arguments", {}))), False)
    except Exception as e:
        return result(f"{type(e).__name__}: {e}", True)


Q(None, "Agree on a Protocol Version", "Easy", "initialize",
  "In <code>initialize</code> the client proposes a protocol version. The server answers with the same version if it supports it, otherwise with its newest supported version. Versions are dates like '2025-06-18'.",
  [(("2025-06-18", ["2024-11-05", "2025-03-26", "2025-06-18"]), '2025-06-18'), (("2026-01-01", ["2024-11-05", "2025-06-18"]), '2025-06-18')],
  ("Loop to check membership and find the max.", "O(v)", "O(1)"),
  ("Dates in ISO form sort as text, so <code>max</code> works directly.", "O(v)", "O(1)"),
  viz=("2026-01-01", ["2024-11-05", "2025-06-18"]))


@B
def negotiate(requested, supported):
    newest = supported[0]
    for v in supported:
        if v == requested:
            return v
        if v > newest:
            newest = v
    return newest


@O
def negotiate(requested, supported):
    return requested if requested in supported else max(supported)


Q(None, "Which Features Can Be Used?", "Easy", "Capability negotiation",
  "Client and server each list capabilities. A feature is usable if the side that must provide it declares it: tools, resources, prompts and logging come from the <b>server</b>; sampling, roots and elicitation from the <b>client</b>. Return the usable features, sorted.",
  [((["sampling", "roots"], ["tools", "resources", "logging"]), ['logging', 'resources', 'roots', 'sampling', 'tools']), (([], ["tools"]), ['tools'])],
  ("Check each known feature against the right side in an if-chain.", "O(f)", "O(f)"),
  ("Two sets and an intersection each.", "O(f)", "O(f)"),
  viz=(["sampling", "roots"], ["tools", "resources", "logging"]))


@B
def usable(client_caps, server_caps):
    out = []
    for f in ["tools", "resources", "prompts", "logging"]:
        if f in server_caps:
            out.append(f)
    for f in ["sampling", "roots", "elicitation"]:
        if f in client_caps:
            out.append(f)
    return sorted(out)


@O
def usable(client_caps, server_caps):
    server_side, client_side = {"tools", "resources", "prompts", "logging"}, {"sampling", "roots", "elicitation"}
    return sorted((server_side & set(server_caps)) | (client_side & set(client_caps)))


Q(None, "Route a Resource URI", "Medium", "Resource templates",
  "Resources are addressed by URI. Given templates like <code>'notes://{folder}/{name}'</code>, return <code>(template, parameters)</code> for the first template that matches <code>uri</code>, or None. Parameters match one path segment (no '/').",
  [((["notes://{folder}/{name}", "db://customers/{id}"], "db://customers/C042"), ('db://customers/{id}', {'id': 'C042'})), ((["notes://{folder}/{name}"], "notes://work/todo.md"), ('notes://{folder}/{name}', {'folder': 'work', 'name': 'todo.md'})),
   ((["notes://{folder}/{name}"], "notes://a/b/c"), None)],
  ("Split both on '/' and compare segment by segment.", "O(t · s)", "O(s)"),
  ("Turn each template into a regex with named groups.", "O(t · s)", "O(s)"),
  viz=(["notes://{folder}/{name}", "db://customers/{id}"], "db://customers/C042"))


@B
def route(templates, uri):
    for t in templates:
        a, b = t.split("/"), uri.split("/")
        if len(a) != len(b):
            continue
        params, ok = {}, True
        for x, y in zip(a, b):
            if x.startswith("{") and x.endswith("}"):
                params[x[1:-1]] = y
            elif x != y:
                ok = False
                break
        if ok:
            return (t, params)
    return None


@O
def route(templates, uri):
    for t in templates:
        pattern = re.sub(r"\\\{(\w+)\\\}", r"(?P<\1>[^/]+)", re.escape(t))
        m = re.fullmatch(pattern, uri)
        if m:
            return (t, m.groupdict())
    return None


Q(None, "Read a Resource", "Easy", "resources/read",
  "Return the <code>resources/read</code> result for a text file: <code>{'contents': [{'uri': uri, 'mimeType': …, 'text': text}]}</code> with the MIME type from the extension (.md → text/markdown, .json → application/json, .csv → text/csv, otherwise text/plain).",
  [(("file:///docs/guide.md", "# Hi"), {'contents': [{'uri': 'file:///docs/guide.md', 'mimeType': 'text/markdown', 'text': '# Hi'}]}), (("file:///data/x.parquet", "..."), {'contents': [{'uri': 'file:///data/x.parquet', 'mimeType': 'text/plain', 'text': '...'}]})],
  ("An if-chain on the extension.", "O(1)", "O(1)"),
  ("A dict lookup on the suffix.", "O(1)", "O(1)"),
  viz=("file:///docs/guide.md", "# Hi"))


@B
def read_resource(uri, text):
    if uri.endswith(".md"):
        mime = "text/markdown"
    elif uri.endswith(".json"):
        mime = "application/json"
    elif uri.endswith(".csv"):
        mime = "text/csv"
    else:
        mime = "text/plain"
    return {"contents": [{"uri": uri, "mimeType": mime, "text": text}]}


@O
def read_resource(uri, text):
    mime = {"md": "text/markdown", "json": "application/json", "csv": "text/csv"}.get(uri.rsplit(".", 1)[-1], "text/plain")
    return {"contents": [{"uri": uri, "mimeType": mime, "text": text}]}


Q(None, "Paginate tools/list", "Medium", "Cursors",
  "A server with many tools returns them in pages of <code>size</code>. The cursor is the index (as text) of the next tool. Return the page for <code>cursor</code> (None = start) as <code>{'tools': [...names], 'nextCursor': … or None}</code>.",
  [((["a", "b", "c", "d", "e"], 2, None), {'tools': ['a', 'b'], 'nextCursor': '2'}), ((["a", "b", "c", "d", "e"], 2, "4"), {'tools': ['e'], 'nextCursor': None})],
  ("Convert the cursor, loop to collect a page.", "O(size)", "O(size)"),
  ("Slicing.", "O(size)", "O(size)"),
  viz=(["a", "b", "c", "d", "e"], 2, None))


@B
def page(tools, size, cursor):
    start = 0 if cursor is None else int(cursor)
    out = []
    i = start
    while i < len(tools) and len(out) < size:
        out.append(tools[i])
        i += 1
    return {"tools": out, "nextCursor": str(i) if i < len(tools) else None}


@O
def page(tools, size, cursor):
    start = int(cursor or 0)
    end = start + size
    return {"tools": tools[start:end], "nextCursor": str(end) if end < len(tools) else None}


Q(None, "MCP Tools → Claude API Tools", "Easy", "Bridging protocols",
  "An MCP client hands tools to the model. Convert MCP tool definitions to Claude API tool definitions: same <code>name</code> and <code>description</code>, and <code>inputSchema</code> becomes <code>input_schema</code>.",
  [(([{"name": "add", "description": "Add two numbers.", "inputSchema": {"type": "object", "properties": {}}}],), [{'name': 'add', 'description': 'Add two numbers.', 'input_schema': {'type': 'object', 'properties': {}}}])],
  ("Build each new dict field by field.", "O(t)", "O(t)"),
  ("A comprehension.", "O(t)", "O(t)"),
  viz=([{"name": "add", "description": "Add two numbers.", "inputSchema": {"type": "object", "properties": {}}}],))


@B
def to_claude_tools(mcp_tools):
    out = []
    for t in mcp_tools:
        out.append({"name": t["name"], "description": t["description"], "input_schema": t["inputSchema"]})
    return out


@O
def to_claude_tools(mcp_tools):
    return [{"name": t["name"], "description": t["description"], "input_schema": t["inputSchema"]} for t in mcp_tools]


Q(None, "Avoid Name Clashes Across Servers", "Medium", "Namespacing",
  "A host connects to several MCP servers. Prefix every tool with its server (<code>server__tool</code>), and return <code>(sorted names, lookup)</code> where lookup maps each prefixed name back to <code>(server, tool)</code>.",
  [(({"github": ["search", "create_issue"], "files": ["search", "read"]},), (['files__read', 'files__search', 'github__create_issue', 'github__search'], {'github__search': ('github', 'search'), 'github__create_issue': ('github', 'create_issue'), 'files__search': ('files', 'search'), 'files__read': ('files', 'read')}))],
  ("Nested loops filling a list and a dict.", "O(t)", "O(t)"),
  ("One dict comprehension; the sorted keys are the names.", "O(t log t)", "O(t)"),
  viz=({"github": ["search", "create_issue"], "files": ["search", "read"]},))


@B
def namespace(servers):
    lookup = {}
    for server, tools in servers.items():
        for tool in tools:
            lookup[server + "__" + tool] = (server, tool)
    return (sorted(lookup), lookup)


@O
def namespace(servers):
    lookup = {f"{s}__{t}": (s, t) for s, tools in servers.items() for t in tools}
    return (sorted(lookup), lookup)


Q(None, "Match Responses to Requests", "Medium", "Out-of-order replies",
  "A client sent requests (id → method) and receives responses in any order, some of them errors. Return <code>{method: 'ok' or error message}</code> plus a list of ids still waiting, as <code>(results, pending)</code>.",
  [(({1: "tools/list", 2: "tools/call", 3: "resources/read"}, [{"id": 2, "result": {}}, {"id": 1, "error": {"code": -32603, "message": "boom"}}]), ({'tools/call': 'ok', 'tools/list': 'boom'}, [3]))],
  ("Loop over responses, look each id up, then find ids never answered.", "O(n)", "O(n)"),
  ("A dict comprehension for results and set difference for pending.", "O(n)", "O(n)"),
  viz=({1: "tools/list", 2: "tools/call", 3: "resources/read"}, [{"id": 2, "result": {}}, {"id": 1, "error": {"code": -32603, "message": "boom"}}]))


@B
def match(sent, responses):
    results = {}
    answered = []
    for r in responses:
        method = sent[r["id"]]
        answered.append(r["id"])
        if "error" in r:
            results[method] = r["error"]["message"]
        else:
            results[method] = "ok"
    pending = []
    for i in sent:
        if i not in answered:
            pending.append(i)
    return (results, sorted(pending))


@O
def match(sent, responses):
    results = {sent[r["id"]]: r["error"]["message"] if "error" in r else "ok" for r in responses}
    return (results, sorted(set(sent) - {r["id"] for r in responses}))


PROMPTS = {"summarise": {"arguments": ["topic", "length"], "template": "Summarise {topic} in {length} bullet points."}}


Q(None, "Fill a Prompt Template", "Easy", "prompts/get",
  "Return the <code>prompts/get</code> result: <code>{'messages': [{'role': 'user', 'content': {'type': 'text', 'text': filled}}]}</code>. If an argument is missing, return <code>{'error': 'missing: name'}</code> for the first missing one.",
  [(("summarise", {"topic": "MCP", "length": "3"}), {'messages': [{'role': 'user', 'content': {'type': 'text', 'text': 'Summarise MCP in 3 bullet points.'}}]}), (("summarise", {"topic": "MCP"}), {'error': 'missing: length'})],
  ("Replace each {name} by hand after checking arguments.", "O(n)", "O(n)"),
  ("<code>str.format(**arguments)</code>.", "O(n)", "O(n)"),
  viz=("summarise", {"topic": "MCP", "length": "3"}))


@B
def get_prompt(name, arguments):
    spec = PROMPTS[name]
    for a in spec["arguments"]:
        if a not in arguments:
            return {"error": "missing: " + a}
    text = spec["template"]
    for k, v in arguments.items():
        text = text.replace("{" + k + "}", v)
    return {"messages": [{"role": "user", "content": {"type": "text", "text": text}}]}


@O
def get_prompt(name, arguments):
    spec = PROMPTS[name]
    missing = [a for a in spec["arguments"] if a not in arguments]
    if missing:
        return {"error": f"missing: {missing[0]}"}
    return {"messages": [{"role": "user", "content": {"type": "text", "text": spec["template"].format(**arguments)}}]}


TOOLS_META = [{"name": "read_file", "annotations": {"readOnlyHint": True}},
              {"name": "write_file", "annotations": {"readOnlyHint": False, "destructiveHint": False}},
              {"name": "delete_repo", "annotations": {"destructiveHint": True}},
              {"name": "mystery", "annotations": {}}]


Q(None, "Decide Which Calls Need Approval", "Medium", "Tool annotations · permissions",
  "Using MCP tool annotations, return <code>{tool: 'allow' | 'ask' | 'deny'}</code>: deny anything on the user's <code>blocked</code> list; allow read-only tools (<code>readOnlyHint</code> true); ask for everything else. Annotations are hints from the server, so a missing hint means 'ask'.",
  [((TOOLS_META, ["delete_repo"]), {'read_file': 'allow', 'write_file': 'ask', 'delete_repo': 'deny', 'mystery': 'ask'}), ((TOOLS_META, []), {'read_file': 'allow', 'write_file': 'ask', 'delete_repo': 'ask', 'mystery': 'ask'})],
  ("An if-chain per tool.", "O(t)", "O(t)"),
  ("A dict comprehension with a conditional expression.", "O(t)", "O(t)"),
  viz=(TOOLS_META, ["delete_repo"]))


@B
def policy(tools, blocked):
    out = {}
    for t in tools:
        if t["name"] in blocked:
            out[t["name"]] = "deny"
        elif t["annotations"].get("readOnlyHint") is True:
            out[t["name"]] = "allow"
        else:
            out[t["name"]] = "ask"
    return out


@O
def policy(tools, blocked):
    return {t["name"]: "deny" if t["name"] in blocked else "allow" if t["annotations"].get("readOnlyHint") is True else "ask"
            for t in tools}


Q(None, "Keep Tool Output Within Budget", "Easy", "Context hygiene",
  "Tool results go into the model's context. If <code>text</code> is longer than <code>max_tokens</code> (estimate 4 characters per token), keep the first part and append <code>'\\n…[truncated N chars]'</code> where N is the number of characters removed.",
  [(("x" * 50, 10), 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n…[truncated 10 chars]'), (("short", 10), 'short')],
  ("Compute the limit and build the string step by step.", "O(n)", "O(n)"),
  ("A conditional expression with slicing.", "O(n)", "O(n)"),
  viz=("x" * 50, 10))


@B
def truncate(text, max_tokens):
    limit = max_tokens * 4
    if len(text) <= limit:
        return text
    removed = len(text) - limit
    return text[:limit] + "\n…[truncated " + str(removed) + " chars]"


@O
def truncate(text, max_tokens):
    limit = max_tokens * 4
    return text if len(text) <= limit else f"{text[:limit]}\n…[truncated {len(text) - limit} chars]"


Q(None, "Progress Notifications", "Easy", "Long-running tools",
  "A long tool sends <code>notifications/progress</code> with <code>progress</code> and <code>total</code>. Return the percentage (rounded down) after each notification, ignoring any that go backwards.",
  [(([(10, 200), (50, 200), (40, 200), (200, 200)],), [5, 25, 100])],
  ("Track the best progress so far in a loop.", "O(n)", "O(n)"),
  ("Same loop with integer division; keep the last accepted value.", "O(n)", "O(n)"),
  viz=([(10, 200), (50, 200), (40, 200), (200, 200)],))


@B
def percents(notes):
    out, best = [], -1
    for progress, total in notes:
        if progress < best:
            continue
        best = progress
        out.append(int(progress / total * 100))
    return out


@O
def percents(notes):
    out, best = [], -1
    for progress, total in notes:
        if progress >= best:
            best = progress
            out.append(progress * 100 // total)
    return out


def tool_result(params):
    # the tools/call handler from earlier, as a plain helper the session can use
    try:
        value = REGISTRY[params["name"]](**params.get("arguments", {}))
        return {"content": [{"type": "text", "text": str(value)}], "isError": False}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"{type(e).__name__}: {e}"}], "isError": True}


Q(None, "A Whole MCP Session", "Hard", "Putting it together",
  "Write a tiny server: <code>handle(msg)</code> answers <code>initialize</code> (with <code>protocolVersion</code> '2025-06-18' and <code>capabilities</code> {'tools': {}}), <code>tools/list</code> (names of REGISTRY tools, sorted) and <code>tools/call</code> (using the <code>tool_result</code> helper); notifications get no reply; anything else gets error -32601. Run the client <code>script</code> and return the list of replies' <code>result</code> or <code>error.code</code>.",
  [(([{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}},
      {"jsonrpc": "2.0", "method": "notifications/initialized"},
      {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
      {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "add", "arguments": {"a": 1, "b": 2}}},
      {"jsonrpc": "2.0", "id": 4, "method": "ping/pong"}],), [{'protocolVersion': '2025-06-18', 'capabilities': {'tools': {}}}, {'tools': ['add', 'get_weather']}, {'content': [{'type': 'text', 'text': '3'}], 'isError': False}, -32601])],
  ("An if-chain inside a loop.", "O(n)", "O(n)"),
  ("A dispatch table from method name to handler function.", "O(n)", "O(n)"),
  viz=([{"jsonrpc": "2.0", "id": 2, "method": "tools/list"}],))


@B
def session(script):
    out = []
    for msg in script:
        if "id" not in msg:
            continue
        m = msg["method"]
        if m == "initialize":
            out.append({"protocolVersion": "2025-06-18", "capabilities": {"tools": {}}})
        elif m == "tools/list":
            out.append({"tools": sorted(REGISTRY)})
        elif m == "tools/call":
            out.append(tool_result(msg["params"]))
        else:
            out.append(-32601)
    return out


@O
def session(script):
    handlers = {"initialize": lambda p: {"protocolVersion": "2025-06-18", "capabilities": {"tools": {}}},
                "tools/list": lambda p: {"tools": sorted(REGISTRY)},
                "tools/call": tool_result}
    replies = []
    for msg in (m for m in script if "id" in m):
        h = handlers.get(msg["method"])
        replies.append(h(msg.get("params", {})) if h else -32601)
    return replies
