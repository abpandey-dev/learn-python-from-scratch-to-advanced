from lib import *

LESSON("Basics", "Environments and dependencies", """
<p>Every project gets its own <b>virtual environment</b> — a folder with its own Python and packages — so projects can't break each other. Dependencies are declared in <code>pyproject.toml</code>; a <b>lockfile</b> records the exact versions of everything installed, so every machine and every CI run gets the same set.</p>
<pre><code class="py">uv init invoice-bot &amp;&amp; cd invoice-bot   # pyproject.toml + .venv
uv add fastapi "pydantic>=2,<3"         # updates pyproject.toml and uv.lock
uv add --dev pytest ruff mypy
uv run pytest                           # run inside the environment
uv sync --frozen                        # CI: install exactly the lockfile

# the classic way
python -m venv .venv &amp;&amp; source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt</code></pre>
<p>Activating an environment just puts its <code>bin</code> folder first on <code>PATH</code> — that's why <code>python</code> suddenly means a different program.</p>
""", practice=["Read pyproject.toml", "Which python Runs?", "How Big Is the Environment?"])

LESSON("Core", "Versions and specifiers", """
<p>Versions compare number by number (<code>1.10 &gt; 1.9</code>), and pre-releases (<code>2.0.0rc1</code>) come before the final release and aren't installed unless you ask. Specifiers say which versions you accept:</p>
<table>
<tr><th>Specifier</th><th>Means</th><th>Use for</th></tr>
<tr><td><code>==1.4.2</code></td><td>exactly that</td><td>lockfiles, reproducible apps</td></tr>
<tr><td><code>&gt;=2,&lt;3</code></td><td>any 2.x</td><td>libraries: allow fixes, block breaking changes</td></tr>
<tr><td><code>~=1.4.2</code></td><td>≥1.4.2 and 1.4.*</td><td>patch updates only</td></tr>
<tr><td><code>!=1.5.0</code></td><td>skip a broken release</td><td>known bugs</td></tr>
</table>
<p>Rule of thumb: <b>applications pin</b> (via a lockfile), <b>libraries use ranges</b> so they don't fight with other libraries.</p>
""", practice=["Sort Versions Correctly", "Does the Version Match?", "Pick the Newest Allowed Version", "Parse a Requirement Line", "Evaluate Environment Markers", "Pin, Range or Unbounded?"])

LESSON("Core", "How installers resolve and install", """
<p>The <b>resolver</b> picks one version of every package so that all constraints hold at once — a search that backtracks when a choice leads to a conflict. If no combination works, you get a resolution error naming the packages that disagree. Installers then download <b>wheels</b> — pre-built archives whose filename tags say which Python, ABI and platform they work on — and fall back to building from source if none match.</p>
<pre><code class="py">uv tree                      # what depends on what
uv tree --invert --package idna   # who pulls in idna
pip install "pydantic<2" "langchain>=0.3"   # → ResolutionImpossible: shows the conflict</code></pre>
""", practice=["Resolve Dependencies", "Spot Version Conflicts", "Read a Wheel Filename", "Measure the Dependency Tree", "Why Is This Package Installed?"])

LESSON("Advanced", "Keeping dependencies healthy and config clean", """
<ul>
<li>Review <b>lockfile diffs</b> in PRs; let <b>Dependabot</b> or <b>Renovate</b> open small upgrade PRs (patches automatically, majors reviewed).</li>
<li>Run <b>pip-audit</b> or <b>osv-scanner</b> in CI to catch packages with known vulnerabilities.</li>
<li>Publishing a library? Follow <b>semantic versioning</b>: any breaking API change is a major bump.</li>
<li><b>Configuration</b> belongs outside the code (twelve-factor): defaults in code, overridden by a file, environment variables, then command-line flags. Secrets live in environment variables or a secret manager — never in Git (add <code>.env</code> to <code>.gitignore</code>).</li>
</ul>
<pre><code class="py">from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    db_url: str = "sqlite:///dev.db"
    workers: int = 1
    model_config = {"env_prefix": "APP_", "env_file": ".env"}
settings = Settings()        # reads APP_DB_URL, APP_WORKERS from env or .env</code></pre>
""", practice=["What Changed in the Lockfile?", "Find Vulnerable Packages", "Safe Automatic Upgrades", "Is This Release Breaking?", "Configuration Precedence", "Parse a .env File"])
