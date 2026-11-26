from lib import *
import json

LESSON("Basics", "Why MCP exists", """
<p>Every AI app wants to reach the same things: files, databases, GitHub, Slack, a company API. Before MCP, every app wrote its own connector for every system — <b>M apps × N systems</b> integrations. The <b>Model Context Protocol</b> is a shared plug: write an <b>MCP server</b> for a system once, and any <b>MCP host</b> (Claude Desktop, Claude Code, IDEs, your own agent) can use it. That's <b>M + N</b>.</p>
<table>
<tr><th>Part</th><th>Role</th><th>Example</th></tr>
<tr><td><b>Host</b></td><td>the AI application the user works in</td><td>Claude Desktop, an IDE, your agent</td></tr>
<tr><td><b>Client</b></td><td>inside the host; one connection per server</td><td>created by the host</td></tr>
<tr><td><b>Server</b></td><td>exposes tools, resources and prompts</td><td>a GitHub server, a Postgres server, your own</td></tr>
</table>
<p>A server offers three kinds of things:</p>
<ul>
<li><b>Tools</b> — actions the <i>model</i> decides to call (search issues, run a query).</li>
<li><b>Resources</b> — data the <i>application</i> reads and puts in context, addressed by URI (<code>file:///notes/todo.md</code>).</li>
<li><b>Prompts</b> — reusable templates the <i>user</i> picks (a "/summarise" command).</li>
</ul>
""", practice=["MCP Tools → Claude API Tools"])

LESSON("Basics", "The wire format: JSON-RPC 2.0", """
<p>Every MCP message is a small JSON object. There are three shapes:</p>
<pre><code class="py">{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}                         # request: expects a reply
{"jsonrpc": "2.0", "id": 1, "result": {"tools": [...]}}                     # response with the same id
{"jsonrpc": "2.0", "method": "notifications/initialized"}                   # notification: no id, no reply</code></pre>
<p>Errors use standard codes: <b>-32700</b> parse error, <b>-32600</b> invalid request, <b>-32601</b> method not found, <b>-32602</b> invalid params, <b>-32603</b> internal error.</p>
<p><b>Transports</b> carry these messages. With <b>stdio</b>, the host starts the server as a child process and they exchange one JSON message per line on stdin/stdout — simple and private, ideal for local tools. With <b>Streamable HTTP</b>, the server runs as a web service that many clients can reach, with authentication (OAuth) — used for remote servers.</p>
""", practice=["Write a JSON-RPC Request", "Read Messages from stdio", "What Kind of Message Is This?", "Answer With the Right Error", "Match Responses to Requests"])


@LD
def wire_demo():
    req = {"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {"name": "add", "arguments": {"a": 2, "b": 3}}}
    line = json.dumps(req)
    received = json.loads(line)
    reply = {"jsonrpc": "2.0", "id": received["id"],
             "result": {"content": [{"type": "text", "text": "5"}], "isError": False}}


LESSON("Core", "The lifecycle: initialize, then work", """
<ol>
<li>The client sends <code>initialize</code> with the protocol version it wants, its capabilities (e.g. <code>sampling</code>, <code>roots</code>) and its name.</li>
<li>The server replies with the version it will use and <i>its</i> capabilities (<code>tools</code>, <code>resources</code>, <code>prompts</code>, <code>logging</code>).</li>
<li>The client sends <code>notifications/initialized</code>. Now normal work starts: <code>tools/list</code>, <code>tools/call</code>, <code>resources/read</code>, <code>prompts/get</code> …</li>
</ol>
<p>Capabilities matter: a client must not call <code>prompts/list</code> on a server that didn't declare <code>prompts</code>. Long lists are <b>paginated</b> with an opaque <code>nextCursor</code>. Long tools can send <code>notifications/progress</code>, and either side can cancel a request.</p>
""", practice=["Agree on a Protocol Version", "Which Features Can Be Used?", "Paginate tools/list", "Progress Notifications", "A Whole MCP Session"])

LESSON("Core", "Tools: schemas, calls and results", """
<p>A tool is a name, a description the model reads to decide when to use it, and an <code>inputSchema</code> (JSON Schema) for its arguments:</p>
<pre><code class="py">{"name": "get_weather", "description": "Forecast for a city.",
 "inputSchema": {"type": "object", "properties": {"city": {"type": "string"}, "days": {"type": "integer"}},
                 "required": ["city"]}}</code></pre>
<p>A call returns <code>content</code> blocks (text, images, resource links) and <code>isError</code>. A tool that fails returns <code>isError: true</code> with a readable message <i>as a normal result</i>, so the model can see what went wrong and try again; protocol-level errors are for broken requests.</p>
<p><b>Writing good tools is prompt engineering</b>: clear names, a description that says when to use it, few parameters with enums where possible, and short outputs — every token a tool returns lands in the model's context.</p>
""", practice=["Validate Tool Arguments", "Describe Python Functions as Tools", "Handle tools/call", "Keep Tool Output Within Budget"])

LESSON("Core", "Build a real server in a few lines", """
<p>The official Python SDK (<code>pip install mcp</code>) turns type-hinted functions into tools, exactly like the questions here do by hand:</p>
<pre><code class="py">from mcp.server.fastmcp import FastMCP      # SDK v1; in v2 the class is MCPServer in mcp.server.mcpserver

mcp = FastMCP("weather")

@mcp.tool()
def get_weather(city: str, days: int = 1) -> str:
    \"\"\"Forecast for a city.\"\"\"
    return f"{city}: sunny for {days} day(s)"

@mcp.resource("notes://{name}")
def note(name: str) -> str:
    return open(f"notes/{name}.md").read()

if __name__ == "__main__":
    mcp.run()          # stdio transport by default</code></pre>
<p>Connect it to Claude Code with <code>claude mcp add weather -- python server.py</code>, or add it to Claude Desktop's config file. The <b>MCP Inspector</b> (<code>npx @modelcontextprotocol/inspector</code>) lets you call your tools by hand while you develop. SDK details change between versions — check the docs for the one you install.</p>
""", practice=["Read a Resource", "Route a Resource URI", "Fill a Prompt Template"])

LESSON("Advanced", "Hosts, many servers, and security", """
<p>A host usually connects to <b>several</b> servers and merges their tools into one list for the model — so it must avoid name clashes (prefix with the server name) and convert MCP tool definitions into the model API's format.</p>
<p>Security is the hard part, because tools act with the user's permissions:</p>
<ul>
<li><b>Human approval</b> for anything that writes or deletes. Tool <b>annotations</b> (<code>readOnlyHint</code>, <code>destructiveHint</code>) help a host decide, but they are hints from the server, not guarantees.</li>
<li><b>Prompt injection</b>: text returned by a tool (a web page, an email, an issue comment) can contain instructions. Treat tool output as data, never as commands.</li>
<li><b>Least privilege</b>: give each server only the tokens and folders it needs; prefer read-only by default.</li>
<li><b>Only install servers you trust</b> — a local server runs code on your machine.</li>
</ul>
""", practice=["Avoid Name Clashes Across Servers", "Decide Which Calls Need Approval"])
