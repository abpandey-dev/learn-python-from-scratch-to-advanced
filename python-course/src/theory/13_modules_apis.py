from lib import *

THEORY("Module, package, library", """
<ul>
<li><b>Module</b>: one <code>.py</code> file. Imported once per program; later imports reuse the cached copy in <code>sys.modules</code>.</li>
<li><b>Package</b>: a folder of modules, usually with <code>__init__.py</code>. Dotted names follow folders.</li>
<li><b>Library / distribution</b>: what you install with pip (one distribution can contain several packages; its pip name can differ from its import name, e.g. <code>pip install scikit-learn</code> → <code>import sklearn</code>).</li>
<li><b>Standard library</b>: modules that ship with Python.</li>
</ul>
""")

THEORY("How import finds a module", """
<ol>
<li>Already in <code>sys.modules</code>? Reuse it (that's why module-level code runs only once).</li>
<li>Otherwise search <code>sys.path</code> in order: the script's folder, <code>PYTHONPATH</code>, the standard library, <code>site-packages</code>.</li>
<li>Run the file top to bottom, and bind the name in the importing module.</li>
</ol>
<p><code>from m import *</code> imports the names in <code>m.__all__</code> if it exists, otherwise every name that doesn't start with <code>_</code>. Avoid it outside quick experiments: it hides where names come from.</p>
""")

THEORY("HTTP status codes worth knowing", """
<table>
<tr><th>Code</th><th>Meaning</th><th>What to do</th></tr>
<tr><td>200 / 201 / 204</td><td>OK / created / no content</td><td>use the body</td></tr>
<tr><td>301 / 302 / 304</td><td>moved / found elsewhere / not modified</td><td>follow, or use your cached copy</td></tr>
<tr><td>400</td><td>bad request</td><td>fix your parameters</td></tr>
<tr><td>401 / 403</td><td>not logged in / not allowed</td><td>check the token and permissions</td></tr>
<tr><td>404</td><td>not found</td><td>don't retry</td></tr>
<tr><td>429</td><td>too many requests</td><td>slow down, honour <code>Retry-After</code></td></tr>
<tr><td>500 / 502 / 503 / 504</td><td>server-side failure</td><td>retry with backoff</td></tr>
</table>
""")

THEORY("Idempotency", """
<p>A request is <b>idempotent</b> if sending it twice has the same effect as once. GET, PUT and DELETE should be; POST usually isn't (two POSTs create two orders). Retrying is only safe for idempotent requests — many payment APIs accept an <i>idempotency key</i> so a retried POST isn't applied twice.</p>
""")

FAQ("What does if __name__ == \"__main__\" do?", "<p>It runs the block only when the file is executed directly, not when it is imported. That lets one file be both a reusable module and a script.</p>")
FAQ("Why use a virtual environment?", "<p>Each project gets its own installed packages and versions, so projects can't break each other, and <code>requirements.txt</code> can recreate the exact set on another machine or server.</p>")
FAQ("json.load vs json.loads?", "<p><code>loads</code> parses a string; <code>load</code> reads from a file object. Likewise <code>dumps</code> returns a string and <code>dump</code> writes to a file.</p>")
FAQ("Which errors should a client retry?", "<p>Timeouts, connection errors, 429 and 5xx — with exponential backoff, jitter and a maximum number of attempts. Not other 4xx errors, which mean the request itself is wrong.</p>")
FAQ("What is pagination and why do APIs use it?", "<p>Returning results a page at a time keeps responses small and fast. Offset pagination (page=3) is simple but can skip or repeat rows when data changes; cursor pagination (next=abc) is stable.</p>")
FAQ("Where should API keys live?", "<p>In environment variables or a secrets manager, read with <code>os.environ</code>. Never in code, notebooks or git history.</p>")
