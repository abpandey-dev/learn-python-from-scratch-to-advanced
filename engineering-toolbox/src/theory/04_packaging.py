from lib import *

THEORY("Tools at a glance", """
<table>
<tr><th>Tool</th><th>Does</th></tr>
<tr><td>pip + venv</td><td>install packages into an environment (built in)</td></tr>
<tr><td>uv</td><td>very fast all-in-one: environments, resolving, lockfiles, Python versions</td></tr>
<tr><td>poetry / pdm</td><td>project management with lockfiles</td></tr>
<tr><td>conda / mamba</td><td>also manages non-Python libraries (CUDA, GDAL)</td></tr>
<tr><td>pip-audit / osv-scanner</td><td>known-vulnerability checks</td></tr>
</table>
""")

FAQ("Why use a virtual environment?", "<p>So each project has its own package versions and can't break another project or the system Python, and so the environment can be rebuilt from its lockfile.</p>")
FAQ("requirements.txt vs pyproject.toml vs lockfile?", "<p>pyproject.toml declares what your project needs (ranges); a lockfile pins every package, including transitive ones, to exact versions; requirements.txt is the older format used for either.</p>")
FAQ("What does ~=1.4.2 mean?", "<p>Compatible release: at least 1.4.2 but still 1.4.* — patch updates only. <code>~=1.4</code> allows any 1.x from 1.4 upwards.</p>")
FAQ("How do you handle a dependency conflict?", "<p>Read which packages constrain the shared dependency, upgrade or downgrade one of them so their ranges overlap, or isolate them in separate services or environments.</p>")
FAQ("Where should secrets go?", "<p>Environment variables injected at runtime or a secret manager (AWS Secrets Manager, Vault). Never in code or Git; keep a .env.example with dummy values.</p>")
FAQ("Should libraries pin exact versions?", "<p>No — pinning in a library causes conflicts for everyone using it. Libraries declare compatible ranges; applications pin via lockfiles.</p>")
