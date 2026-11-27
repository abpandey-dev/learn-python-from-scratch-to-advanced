from lib import *

LESSON("Basics", "Your first CI workflow", """
<p><b>Continuous integration</b> runs your checks on every push and pull request, so a broken change is caught in minutes, not in production. In GitHub Actions a <b>workflow</b> (a YAML file in <code>.github/workflows/</code>) is triggered by <b>events</b> and contains <b>jobs</b>; each job runs <b>steps</b> on a fresh runner machine.</p>
<pre><code class="py">name: ci
on:
  pull_request:
  push: {branches: [main]}
concurrency: {group: "ci-${{ github.ref }}", cancel-in-progress: true}
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix: {python: ["3.11", "3.12"]}
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
        with: {python-version: "${{ matrix.python }}", enable-cache: true}
      - run: uv sync --frozen
      - run: uv run ruff check . &amp;&amp; uv run ruff format --check .
      - run: uv run mypy app
      - run: uv run pytest -q --cov=app
      - if: failure()
        run: echo "tests failed on ${{ matrix.python }}"</code></pre>
""", practice=["Expand a Build Matrix", "Which Steps Run?", "Can the Pull Request Merge Yet?", "Validate a Workflow", "Scheduled Workflows Run in UTC"])

LESSON("Core", "Fast pipelines", """
<ul>
<li>Run independent jobs in <b>parallel</b>; only chain with <code>needs:</code> when one really depends on another. The <b>critical path</b> sets the minimum time.</li>
<li><b>Cache</b> dependencies keyed on the lockfile hash, with a restore-key fallback.</li>
<li>Use <b>path filters</b> so docs changes don't run the whole test suite.</li>
<li><b>Shard</b> long test suites across parallel jobs; <b>cancel</b> superseded runs; re-run only failed jobs.</li>
<li>Watch cost: macOS and Windows minutes are multiplied.</li>
</ul>
<pre><code class="py">jobs:
  test:
    strategy: {matrix: {shard: [1, 2, 3]}}
    steps:
      - run: uv run pytest --splits 3 --group ${{ matrix.shard }}   # pytest-split
  build:
    needs: [test]
    ...
      - uses: actions/upload-artifact@v4
        with: {name: wheel, path: dist/}</code></pre>
""", practice=["Job Waves and the Critical Path", "Which Workflows Run for This Change?", "Cache Hits, Partial Hits and Misses", "Cancel Superseded Runs", "Split Tests Across Shards", "Re-run Only Failed Jobs", "What Does CI Cost?", "Pass Files Between Jobs"])

LESSON("Core", "Continuous delivery", """
<p>Once checks pass, the pipeline builds an image, tags it, pushes it to a registry and deploys it — first to <b>dev</b>, then <b>staging</b>, then <b>production</b> after tests and, often, a manual approval (GitHub <b>environments</b> support required reviewers). Releases get version tags and a changelog generated from commit messages.</p>
<pre><code class="py">  release:
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    environment: production          # waits for approval
    permissions: {contents: write, packages: write}
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with: {registry: ghcr.io, username: "${{ github.actor }}", password: "${{ secrets.GITHUB_TOKEN }}"}
      - uses: docker/build-push-action@v6
        with: {push: true, tags: "ghcr.io/acme/api:${{ github.ref_name }}"}</code></pre>
""", practice=["Should This Run Push an Image?", "Promote Through Environments", "Generate a Changelog", "Measure Delivery: DORA Metrics"])

LESSON("Advanced", "Securing the pipeline", """
<ul>
<li>Store credentials in <b>secrets</b> (masked in logs) — never in the YAML. Prefer short-lived <b>OIDC</b> credentials for cloud deploys over long-lived keys.</li>
<li>Give the <code>GITHUB_TOKEN</code> <b>least-privilege</b> <code>permissions:</code> per job.</li>
<li><b>Pin</b> third-party actions to commit SHAs, and let Dependabot update them.</li>
<li>Don't run untrusted pull-request code with access to secrets (<code>pull_request_target</code> is dangerous).</li>
</ul>
""", practice=["Mask Secrets in Logs", "Pin Third-Party Actions", "Least-Privilege Token Permissions"])
