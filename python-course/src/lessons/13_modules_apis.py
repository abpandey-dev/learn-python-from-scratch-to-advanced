from lib import *
import json
from urllib.parse import urlencode, quote

LESSON("Basics", "Modules: one file, one job", """
<p>Once a program grows past a few hundred lines, you split it into <b>modules</b>. A module is just a <code>.py</code> file, and its name is the file name without <code>.py</code>. <code>import</code> runs that file once and gives you its names.</p>
<pre><code class="py"># prices.py
TAX = 0.18
def with_tax(amount):
    return round(amount * (1 + TAX), 2)

# main.py
import prices                 # use as prices.with_tax(100)
from prices import with_tax   # use as with_tax(100)
import prices as p            # short alias: p.with_tax(100)</code></pre>
<p>Every module has a <code>__name__</code>. It is <code>"__main__"</code> when you run the file directly, and the module's own name when someone imports it. That's why scripts end with:</p>
<pre><code class="py">if __name__ == "__main__":
    main()        # runs for `python prices.py`, not for `import prices`</code></pre>
<p><b>Where does Python look?</b> First the folder of the script you ran, then the standard library, then installed packages (<code>site-packages</code>). The list is in <code>sys.path</code>. Naming your own file <code>json.py</code> or <code>random.py</code> hides the real module — a classic beginner bug.</p>
""", practice=["What Does import * Bring In?"])

LESSON("Basics", "Packages and the standard library", """
<p>A <b>package</b> is a folder of modules. Dotted names follow the folders:</p>
<pre><code class="text">app/
    __init__.py        # runs when the package is imported (may be empty)
    api/
        __init__.py
        orders.py      # import app.api.orders
    utils.py           # inside app.api.orders: from ..utils import slugify</code></pre>
<p>Relative imports start with dots: one dot is "this package", two dots is "the parent". They only work inside a package, not in a script you run directly.</p>
<p>Python ships with a big <b>standard library</b>. Learn where things live before installing anything:</p>
<table>
<tr><th>Need</th><th>Module</th></tr>
<tr><td>JSON, CSV</td><td><code>json</code>, <code>csv</code></td></tr>
<tr><td>Dates and times</td><td><code>datetime</code>, <code>zoneinfo</code></td></tr>
<tr><td>Counting, queues, defaults</td><td><code>collections</code> (<code>Counter</code>, <code>deque</code>, <code>defaultdict</code>)</td></tr>
<tr><td>Files and paths</td><td><code>pathlib</code>, <code>os</code>, <code>shutil</code></td></tr>
<tr><td>URLs and HTTP</td><td><code>urllib.parse</code>, <code>urllib.request</code></td></tr>
<tr><td>Text patterns</td><td><code>re</code></td></tr>
<tr><td>Caching, partials</td><td><code>functools</code></td></tr>
<tr><td>Logs instead of prints</td><td><code>logging</code></td></tr>
<tr><td>Small databases</td><td><code>sqlite3</code></td></tr>
</table>
""", practice=["Resolve a Relative Import", "Days Between ISO Dates"])

LESSON("Core", "pip and virtual environments", """
<p>Libraries outside the standard library (pandas, requests, scikit-learn) are installed with <b>pip</b> from PyPI. If every project installs into one global Python, project A needing pandas 1.5 and project B needing pandas 2.2 will fight. A <b>virtual environment</b> gives each project its own private <code>site-packages</code>.</p>
<pre><code class="bash">python -m venv .venv              # create (once per project)
source .venv/bin/activate         # macOS / Linux   (.venv\\Scripts\\activate on Windows)
pip install pandas==2.2.3 requests
pip freeze &gt; requirements.txt     # record exact versions
pip install -r requirements.txt   # a teammate recreates the same set
deactivate</code></pre>
<p>Rules that save hours:</p>
<ul>
<li>Never commit <code>.venv</code> to git; commit <code>requirements.txt</code> (or <code>pyproject.toml</code>).</li>
<li>Pin versions for anything that runs in production, so a new release can't break you overnight.</li>
<li>Use <code>python -m pip</code> if you are unsure which Python <code>pip</code> belongs to.</li>
<li>Versions compare part by part as numbers: 1.10 is newer than 1.9.</li>
</ul>
""", practice=["Read a requirements.txt", "Compare Version Numbers"])

LESSON("Core", "JSON: the language APIs speak", """
<p><b>JSON</b> is text that looks like Python dicts and lists. Almost every web API sends and receives it.</p>
<table>
<tr><th>JSON</th><th>Python</th></tr>
<tr><td>object <code>{}</code></td><td>dict (keys are always strings)</td></tr>
<tr><td>array <code>[]</code></td><td>list (tuples are written as arrays)</td></tr>
<tr><td>string, number</td><td>str, int / float</td></tr>
<tr><td><code>true</code> / <code>false</code> / <code>null</code></td><td><code>True</code> / <code>False</code> / <code>None</code></td></tr>
</table>
<pre><code class="py">text = json.dumps({"id": 1, "ok": True}, indent=2)   # dump to a string
data = json.loads(text)                               # load from a string
with open("orders.json") as f:
    orders = json.load(f)                             # load / dump (no s) work with files</code></pre>
<p>Dates have no JSON type, so APIs send ISO text like <code>"2026-03-01"</code>; turn it back with <code>date.fromisoformat</code>. Real API data is nested and has gaps, so read deep fields defensively.</p>
""", practice=["JSON Text for a Flat Record", "What Survives a JSON Round Trip?", "Count Records by Status", "Read a Nested JSON Field", "Flatten Nested JSON"])


@LD
def json_demo():
    order = {"id": 17, "items": ("pen", "book"), "paid": True, "coupon": None}
    text = json.dumps(order)
    back = json.loads(text)
    same = back == order
    items_type = type(back["items"]).__name__


LESSON("Core", "Calling a web API", """
<p>An <b>API</b> is a URL that returns data instead of a web page. You send an HTTP <b>request</b> and get a <b>response</b> with a status code, headers and a body (usually JSON).</p>
<pre><code class="py">import os, requests

r = requests.get(
    "https://api.example.com/v1/orders",
    params={"status": "paid", "limit": 50},                     # becomes ?status=paid&amp;limit=50
    headers={"Authorization": f"Bearer {os.environ['API_TOKEN']}"},
    timeout=10,                                                 # never wait forever
)
r.raise_for_status()      # turns 4xx / 5xx into an exception
orders = r.json()</code></pre>
<table>
<tr><th>Method</th><th>Meaning</th></tr>
<tr><td>GET</td><td>read</td></tr>
<tr><td>POST</td><td>create (send JSON with <code>json=...</code>)</td></tr>
<tr><td>PUT / PATCH</td><td>replace / update part</td></tr>
<tr><td>DELETE</td><td>remove</td></tr>
</table>
<p>Keep secrets such as tokens in environment variables, never in code or notebooks you share. The browser IDE can't make real network calls, so the practice questions fake the server with plain data — the logic is identical.</p>
""", practice=["Build a Query String", "Pull Apart a URL", "Join API Paths Without Double Slashes", "Classify an HTTP Status Code", "Validate an API Response"])


@LD
def query_demo():
    params = {"q": "data science", "page": 2}
    query = urlencode(params, quote_via=quote)
    url = "https://api.example.com/search?" + query


LESSON("Advanced", "Robust API clients: pages, retries, limits, caching", """
<p>Real APIs fail and limit you. A production client handles four things:</p>
<ol>
<li><b>Pagination.</b> Big results come in pages. Follow the <code>next</code> cursor (or page number) until there isn't one.</li>
<li><b>Retries with backoff.</b> 429 (too many requests) and 5xx (server trouble) are often temporary: wait 1 s, 2 s, 4 s… with a cap, plus a little random jitter so many clients don't retry together. 4xx errors like 404 won't fix themselves, so don't retry them.</li>
<li><b>Rate limits.</b> Respect "N requests per window" yourself instead of waiting for 429s. A sliding window keeps the timestamps of recent calls.</li>
<li><b>Caching.</b> Don't fetch the same thing twice: <code>functools.lru_cache</code> for one run, a file or database cache across runs.</li>
</ol>
<pre><code class="py">for attempt in range(5):
    r = requests.get(url, timeout=10)
    if r.status_code != 429 and r.status_code &lt; 500:
        break
    time.sleep(min(30, 2 ** attempt) + random.random())</code></pre>
""", practice=["Collect Every Page", "Exponential Backoff Delays", "Call With Retries", "Sliding-Window Rate Limiter", "Cache Repeated API Calls"])
