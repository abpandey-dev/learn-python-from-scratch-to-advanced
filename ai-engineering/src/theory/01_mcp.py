from lib import *

THEORY("MCP in one table", """
<table>
<tr><th>Primitive</th><th>Controlled by</th><th>Methods</th></tr>
<tr><td>Tools</td><td>the model</td><td><code>tools/list</code>, <code>tools/call</code></td></tr>
<tr><td>Resources</td><td>the application</td><td><code>resources/list</code>, <code>resources/templates/list</code>, <code>resources/read</code>, <code>resources/subscribe</code></td></tr>
<tr><td>Prompts</td><td>the user</td><td><code>prompts/list</code>, <code>prompts/get</code></td></tr>
<tr><td>Sampling (client feature)</td><td>server asks the host's model</td><td><code>sampling/createMessage</code></td></tr>
<tr><td>Roots (client feature)</td><td>which folders a server may use</td><td><code>roots/list</code></td></tr>
<tr><td>Elicitation (client feature)</td><td>server asks the user a question</td><td><code>elicitation/create</code></td></tr>
</table>
""")

THEORY("Transports", """
<ul>
<li><b>stdio</b>: the host launches the server process; newline-delimited JSON on stdin/stdout; logs go to stderr. Local, simple, no network.</li>
<li><b>Streamable HTTP</b>: one HTTP endpoint; requests by POST, responses as JSON or a server-sent-event stream; sessions via a header; authorisation with OAuth 2.1. For remote, multi-user servers.</li>
</ul>
""")

THEORY("MCP vs function calling", """
<p><b>Function calling</b> is how a model API lets the model request a tool (Claude's <code>tools</code> parameter and <code>tool_use</code> blocks). <b>MCP</b> is how an application <i>discovers and runs</i> tools that live in separate servers. A host lists MCP tools, passes them to the model as function definitions, and when the model asks for one, forwards the call to the right server with <code>tools/call</code>. They're complementary layers.</p>
""")

FAQ("What problem does MCP solve?", "<p>It standardises how AI applications connect to tools and data, so a connector written once as an MCP server works with every MCP host — M + N integrations instead of M × N.</p>")
FAQ("Tools vs resources vs prompts?", "<p>Tools are actions the model chooses to call; resources are data the application reads into context by URI; prompts are templates the user selects. They differ in who is in control.</p>")
FAQ("When would you use stdio vs HTTP transport?", "<p>stdio for local servers the host launches itself (files, local databases, developer tools); Streamable HTTP for remote servers shared by many users, with OAuth authorisation.</p>")
FAQ("How should a tool report a failure?", "<p>Return a normal result with isError true and a helpful message, so the model can read it and recover. Use JSON-RPC errors only for malformed requests or unknown methods.</p>")
FAQ("What are the main security risks of MCP?", "<p>Tools act with the user's permissions, tool output can carry prompt injections, and local servers run code on the machine. Mitigate with approval for side effects, least-privilege credentials, trusted servers only and treating tool output as untrusted data.</p>")
FAQ("How do you design a good tool?", "<p>A clear name and description that says when to use it, a small typed input schema with enums, idempotent behaviour where possible, and short, structured output that fits the model's context.</p>")
