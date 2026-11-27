from lib import *
import fnmatch
import heapq
import itertools
import math
import re
import statistics
from collections import defaultdict

TOPIC(
    id="cicd", title="CI/CD With GitHub Actions", glyph="⚙",
    blurb="Automate everything after git push: matrix builds, job graphs and critical paths, path and branch filters, cache keys, concurrency, secret masking, step conditions, check status, artifacts, workflow validation, schedules in UTC, CI minutes, test sharding, reruns, changelogs, image pushing rules, environment promotion and DORA metrics.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py"># .github/workflows/ci.yml
name: ci
on:
  push: {branches: [main]}
  pull_request:
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix: {python: ["3.11", "3.12"]}
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv sync --frozen
      - run: uv run ruff check . &amp;&amp; uv run mypy app
      - run: uv run pytest -q --cov=app</code></pre>
<p>CI = every change is built and tested automatically. CD = every change that passes can be released automatically.</p>
""")


Q(None, "Expand a Build Matrix", "Medium", "strategy.matrix",
  "Expand the matrix axes (in key order, first key varying slowest) into jobs, remove combinations matching every key of any <code>exclude</code> entry, then apply <code>include</code> entries: if an include's matrix keys match existing jobs, add its extra keys to those jobs; otherwise append it as a new job. Return the job dicts.",
  [(({"os": ["ubuntu", "windows"], "python": ["3.11", "3.12"]}, [{"os": "windows", "python": "3.11"}], [{"os": "ubuntu", "python": "3.12", "coverage": True}, {"os": "macos", "python": "3.12"}]), [{'os': 'ubuntu', 'python': '3.11'}, {'os': 'ubuntu', 'python': '3.12', 'coverage': True}, {'os': 'windows', 'python': '3.12'}, {'os': 'macos', 'python': '3.12'}])],
  ("Nested loops building dicts.", "O(product · (e + i))", "O(product)"),
  ("<code>itertools.product</code> and comprehensions.", "O(product · (e + i))", "O(product)"),
  viz=(({"py": ["3.11", "3.12"]}, [], [])))


@B
def expand_matrix(axes, exclude, include):
    jobs = [{}]
    for key, values in axes.items():
        new = []
        for j in jobs:
            for v in values:
                d = dict(j)
                d[key] = v
                new.append(d)
        jobs = new
    kept = []
    for j in jobs:
        drop = False
        for e in exclude:
            if all(j.get(k) == v for k, v in e.items()):
                drop = True
        if not drop:
            kept.append(j)
    for inc in include:
        core = {k: v for k, v in inc.items() if k in axes}
        matched = False
        for j in kept:
            if all(j[k] == v for k, v in core.items()):
                j.update(inc)
                matched = True
        if not matched:
            kept.append(dict(inc))
    return kept


@O
def expand_matrix(axes, exclude, include):
    jobs = [dict(zip(axes, c)) for c in itertools.product(*axes.values())]
    jobs = [j for j in jobs if not any(all(j.get(k) == v for k, v in e.items()) for e in exclude)]
    for inc in include:
        hits = [j for j in jobs if all(j[k] == v for k, v in inc.items() if k in axes)]
        for j in hits:
            j.update(inc)
        if not hits:
            jobs.append(dict(inc))
    return jobs


Q(None, "Job Waves and the Critical Path", "Medium", "needs:",
  "Jobs run in parallel unless they <code>need</code> other jobs. Return <code>(waves of jobs that can run together, each sorted, minimum pipeline minutes with unlimited runners)</code>. A job starts when all its needs have finished.",
  [(({"lint": [], "unit": [], "build": ["lint"], "integration": ["build", "unit"], "e2e": ["build"], "deploy": ["integration", "e2e"]}, {"lint": 1, "unit": 4, "build": 6, "integration": 8, "e2e": 12, "deploy": 3}), ([['lint', 'unit'], ['build'], ['e2e', 'integration'], ['deploy']], 22))],
  ("Repeatedly collect jobs whose needs are done.", "O(j²)", "O(j)"),
  ("Memoised finish times; waves by longest chain of needs.", "O(j + e)", "O(j)"),
  viz=(({"a": [], "b": ["a"]}, {"a": 1, "b": 2})))


@B
def job_waves(needs, minutes):
    done, waves = set(), []
    while len(done) < len(needs):
        wave = sorted(j for j in needs if j not in done and all(n in done for n in needs[j]))
        waves.append(wave)
        done |= set(wave)
    finish = {}
    for wave in waves:
        for j in wave:
            finish[j] = max([finish[n] for n in needs[j]], default=0) + minutes[j]
    return (waves, max(finish.values()))


@O
def job_waves(needs, minutes):
    from functools import lru_cache
    @lru_cache(None)
    def level(j):
        return 1 + max(map(level, needs[j]), default=-1)
    @lru_cache(None)
    def finish(j):
        return minutes[j] + max(map(finish, needs[j]), default=0)
    waves = defaultdict(list)
    for j in needs:
        waves[level(j)].append(j)
    return ([sorted(waves[i]) for i in sorted(waves)], max(map(finish, needs)))


def path_match(pattern, path):
    rx = "".join({"**/": "(?:.*/)?", "**": ".*", "*": "[^/]*"}.get(t, re.escape(t)) for t in re.split(r"(\*\*/|\*\*|\*)", pattern))
    return re.fullmatch(rx, path) is not None


Q(None, "Which Workflows Run for This Change?", "Medium", "on.push.paths",
  "Each workflow has <code>paths</code> (run only if some changed file matches; empty means any) and <code>paths_ignore</code> (don't run if every changed file matches). <code>**</code> matches across folders (<code>**/</code> also matches no folder at all), <code>*</code> within one (use <code>path_match</code>). For each change set, return the workflows that run, sorted.",
  [(({"backend": {"paths": ["app/**", "pyproject.toml"], "paths_ignore": []}, "frontend": {"paths": ["web/**"], "paths_ignore": []}, "docs": {"paths": ["docs/**", "*.md"], "paths_ignore": []}, "ci": {"paths": [], "paths_ignore": ["**/*.md", "docs/**"]}},
     [["app/api/orders.py"], ["README.md"], ["web/src/App.tsx", "docs/guide.md"], ["pyproject.toml", "uv.lock"]]), [['backend', 'ci'], ['docs'], ['ci', 'docs', 'frontend'], ['backend', 'ci']])],
  ("Nested loops over workflows, files and patterns.", "O(c · w · f · p)", "O(w)"),
  ("any()/all() comprehensions.", "O(c · w · f · p)", "O(w)"),
  viz=(({"x": {"paths": ["a/**"], "paths_ignore": []}}, [["a/b.py"]])))


@B
def triggered(workflows, changes):
    out = []
    for files in changes:
        run = []
        for name, wf in workflows.items():
            ok = True
            if wf["paths"]:
                ok = False
                for f in files:
                    for p in wf["paths"]:
                        if path_match(p, f):
                            ok = True
            if ok and wf["paths_ignore"]:
                every = True
                for f in files:
                    if not any(path_match(p, f) for p in wf["paths_ignore"]):
                        every = False
                if every:
                    ok = False
            if ok:
                run.append(name)
        out.append(sorted(run))
    return out


@O
def triggered(workflows, changes):
    hit = lambda pats, f: any(path_match(p, f) for p in pats)
    def runs(wf, files):
        wanted = not wf["paths"] or any(hit(wf["paths"], f) for f in files)
        ignored = bool(wf["paths_ignore"]) and all(hit(wf["paths_ignore"], f) for f in files)
        return wanted and not ignored
    return [sorted(n for n, wf in workflows.items() if runs(wf, files)) for files in changes]


Q(None, "Cache Hits, Partial Hits and Misses", "Medium", "actions/cache keys",
  "The cache key is <code>'{os}-py{python}-{lock hash}'</code> and the restore key is the prefix <code>'{os}-py{python}-'</code>. For each run, return <code>'hit'</code> if an exact key is cached, <code>'partial'</code> if some cached key starts with the restore prefix (an older cache is restored, then updated), else <code>'miss'</code>. After a run that wasn't a hit, its exact key is saved.",
  [(([("ubuntu", "3.12", "a1"), ("ubuntu", "3.12", "a1"), ("ubuntu", "3.12", "b7"), ("ubuntu", "3.11", "b7"), ("macos", "3.12", "b7"), ("ubuntu", "3.12", "a1")],), ['miss', 'hit', 'partial', 'miss', 'miss', 'hit'])],
  ("A list of saved keys, scanned each time.", "O(r²)", "O(r)"),
  ("A set of keys and a set of prefixes.", "O(r)", "O(r)"),
  viz=(([("u", "3", "x"), ("u", "3", "y")],)))


@B
def cache_results(runs):
    saved, out = [], []
    for os_, py, h in runs:
        key, prefix = f"{os_}-py{py}-{h}", f"{os_}-py{py}-"
        if key in saved:
            out.append("hit")
            continue
        out.append("partial" if any(k.startswith(prefix) for k in saved) else "miss")
        saved.append(key)
    return out


@O
def cache_results(runs):
    keys, prefixes, out = set(), set(), []
    for os_, py, h in runs:
        key, prefix = f"{os_}-py{py}-{h}", f"{os_}-py{py}-"
        out.append("hit" if key in keys else "partial" if prefix in prefixes else "miss")
        keys.add(key)
        prefixes.add(prefix)
    return out


Q(None, "Cancel Superseded Runs", "Medium", "concurrency: cancel-in-progress",
  "Runs are <code>(id, start minute, end minute, group)</code> sorted by start. With <code>cancel-in-progress</code>, a new run in a group cancels a still-running earlier run of the same group (one that hasn't ended before the new run starts). Return <code>(cancelled ids, runner-minutes saved)</code> — e.g. pushing three commits quickly to one PR builds only the last.",
  [(([("r1", 0, 12, "pr-7"), ("r2", 3, 15, "pr-7"), ("r3", 4, 14, "main"), ("r4", 5, 17, "pr-7"), ("r5", 20, 30, "pr-7"), ("r6", 21, 28, "main")],), (['r1', 'r2'], 19))],
  ("Track the running run per group.", "O(n)", "O(g)"),
  ("Same with dict.get and a walrus.", "O(n)", "O(g)"),
  viz=(([("a", 0, 10, "g"), ("b", 2, 9, "g")],)))


@B
def cancelled_runs(runs):
    current, cancelled, saved = {}, [], 0
    for rid, start, end, group in runs:
        if group in current:
            pid, pend = current[group]
            if pend > start:
                cancelled.append(pid)
                saved += pend - start
        current[group] = (rid, end)
    return (cancelled, saved)


@O
def cancelled_runs(runs):
    current, cancelled, saved = {}, [], 0
    for rid, start, end, group in runs:
        if (prev := current.get(group)) and prev[1] > start:
            cancelled.append(prev[0])
            saved += prev[1] - start
        current[group] = (rid, end)
    return (cancelled, saved)


Q(None, "Mask Secrets in Logs", "Easy", "*** in the job output",
  "GitHub replaces every registered secret value in log output with <code>***</code>. Mask all occurrences of each secret (longest secrets first, so a secret containing another is fully hidden). Return the masked lines and how many replacements were made.",
  [((["Logging in to registry with token ghp_ABC123xyz", "export DB_URL=postgres://app:Pa55word@db/prod", "password is Pa55word, again Pa55word", "all clean here"], ["ghp_ABC123xyz", "Pa55word", "postgres://app:Pa55word@db/prod"]), (['Logging in to registry with token ***', 'export DB_URL=***', 'password is ***, again ***', 'all clean here'], 4))],
  ("Loop with str.count and replace.", "O(n · s · L)", "O(L)"),
  ("One alternation regex with subn.", "O(n · L)", "O(s)"),
  viz=((["key=s3"], ["s3"])))


@B
def mask_secrets(lines, secrets):
    order = sorted(secrets, key=len, reverse=True)
    out, n = [], 0
    for line in lines:
        for s in order:
            n += line.count(s)
            line = line.replace(s, "***")
        out.append(line)
    return (out, n)


@O
def mask_secrets(lines, secrets):
    rx = re.compile("|".join(re.escape(s) for s in sorted(secrets, key=len, reverse=True)))
    out, n = [], 0
    for line in lines:
        line, k = rx.subn("***", line)
        out.append(line)
        n += k
    return (out, n)


Q(None, "Which Steps Run?", "Medium", "if: success(), failure(), always()",
  "Steps run in order with a condition: <code>'success'</code> (default: run only if nothing before failed), <code>'failure'</code> (run only if something before failed), <code>'always'</code>. <code>outcome</code> says whether a step would pass when run. Return <code>(steps that ran, job result)</code> — the job fails if any step that ran failed.",
  [(([("checkout", "success", True), ("install", "success", True), ("test", "success", False), ("coverage report", "success", True), ("upload test results", "always", True), ("notify on failure", "failure", True)],), (['checkout', 'install', 'test', 'upload test results', 'notify on failure'], 'failure')),
   (([("checkout", "success", True), ("test", "success", True), ("notify on failure", "failure", True), ("cleanup", "always", True)],), (['checkout', 'test', 'cleanup'], 'success'))],
  ("A failed flag and if/elif.", "O(n)", "O(n)"),
  ("A condition table keyed by name.", "O(n)", "O(n)"),
  viz=(([("a", "success", False), ("b", "always", True)],)))


@B
def steps_run(steps):
    failed, ran = False, []
    for name, cond, ok in steps:
        if cond == "always" or (cond == "success" and not failed) or (cond == "failure" and failed):
            ran.append(name)
            if not ok:
                failed = True
    return (ran, "failure" if failed else "success")


@O
def steps_run(steps):
    failed, ran = False, []
    for name, cond, ok in steps:
        if {"always": True, "success": not failed, "failure": failed}[cond]:
            ran.append(name)
            failed |= not ok
    return (ran, "failure" if failed else "success")


Q(None, "Can the Pull Request Merge Yet?", "Easy", "Combined check status",
  "Given check runs <code>(name, status)</code> where status is <code>queued</code>, <code>in_progress</code>, <code>success</code>, <code>failure</code>, <code>skipped</code> or <code>cancelled</code>, and the <code>required</code> checks: return <code>'failure'</code> if any required check failed or was cancelled, <code>'pending'</code> if any required check is missing or not finished, else <code>'success'</code> (skipped counts as passing).",
  [(([("lint", "success"), ("tests (3.12)", "in_progress"), ("tests (3.11)", "success"), ("docs", "failure")], ["lint", "tests (3.12)", "tests (3.11)"]), 'pending'),
   (([("lint", "success"), ("tests", "cancelled")], ["lint", "tests"]), 'failure'),
   (([("lint", "success"), ("deploy-preview", "skipped")], ["lint", "deploy-preview", "security"]), 'pending'),
   (([("lint", "success"), ("tests", "skipped")], ["lint", "tests"]), 'success')],
  ("Loop over required checks with flags.", "O(r + c)", "O(c)"),
  ("A status dict and any().", "O(r + c)", "O(c)"),
  viz=(([("a", "success")], ["a"])))


@B
def combined_status(checks, required):
    status = {}
    for n, s in checks:
        status[n] = s
    pending = False
    for r in required:
        s = status.get(r)
        if s in ("failure", "cancelled"):
            return "failure"
        if s not in ("success", "skipped"):
            pending = True
    return "pending" if pending else "success"


@O
def combined_status(checks, required):
    st = dict(checks)
    got = [st.get(r) for r in required]
    if any(s in ("failure", "cancelled") for s in got):
        return "failure"
    return "success" if all(s in ("success", "skipped") for s in got) else "pending"


Q(None, "Validate a Workflow", "Medium", "Catch mistakes before pushing",
  "Each job has <code>runs_on</code>, <code>needs</code> and <code>steps</code>. Return sorted errors: <code>'JOB: missing runs-on'</code>, <code>'JOB: no steps'</code>, <code>'JOB: needs unknown job X'</code>, and <code>'cycle: A, B, …'</code> (the jobs in any dependency cycle, sorted) if the needs graph has a cycle.",
  [(({"lint": {"runs_on": "ubuntu-latest", "needs": [], "steps": ["ruff"]}, "test": {"runs_on": "ubuntu-latest", "needs": ["lint", "deploy"], "steps": ["pytest"]}, "build": {"runs_on": "", "needs": ["lint", "package"], "steps": []}, "deploy": {"runs_on": "ubuntu-latest", "needs": ["test"], "steps": ["kubectl"]}},), ['build: missing runs-on', 'build: needs unknown job package', 'build: no steps', 'cycle: deploy, test'])],
  ("Checks in a loop; peel off jobs with no remaining needs to find a cycle.", "O(j²)", "O(j)"),
  ("Kahn's algorithm over known needs.", "O(j + e)", "O(j)"),
  viz=(({"a": {"runs_on": "x", "needs": ["a"], "steps": ["s"]}},)))


@B
def validate_workflow(jobs):
    errors = []
    for name, j in jobs.items():
        if not j["runs_on"]:
            errors.append(f"{name}: missing runs-on")
        if not j["steps"]:
            errors.append(f"{name}: no steps")
        for n in j["needs"]:
            if n not in jobs:
                errors.append(f"{name}: needs unknown job {n}")
    left = {n: [d for d in j["needs"] if d in jobs] for n, j in jobs.items()}
    changed = True
    while changed:
        changed = False
        for n in list(left):
            if all(d not in left for d in left[n]):
                del left[n]
                changed = True
    if left:
        errors.append("cycle: " + ", ".join(sorted(left)))
    return sorted(errors)


@O
def validate_workflow(jobs):
    errors = [f"{n}: missing runs-on" for n, j in jobs.items() if not j["runs_on"]]
    errors += [f"{n}: no steps" for n, j in jobs.items() if not j["steps"]]
    errors += [f"{n}: needs unknown job {d}" for n, j in jobs.items() for d in j["needs"] if d not in jobs]
    indeg = {n: sum(d in jobs for d in j["needs"]) for n, j in jobs.items()}
    users = defaultdict(list)
    for n, j in jobs.items():
        for d in j["needs"]:
            if d in jobs:
                users[d].append(n)
    queue = [n for n, k in indeg.items() if k == 0]
    while queue:
        for u in users[queue.pop()]:
            indeg[u] -= 1
            if indeg[u] == 0:
                queue.append(u)
    stuck = sorted(n for n, k in indeg.items() if k > 0)
    return sorted(errors + ([f"cycle: {', '.join(stuck)}"] if stuck else []))


Q(None, "Scheduled Workflows Run in UTC", "Easy", "Convert cron times",
  "GitHub Actions cron schedules are in UTC. For each <code>'minute hour'</code> pair, return the local time <code>'HH:MM'</code> for a UTC offset in minutes (e.g. +330 for IST), plus whether it lands on the previous, same or next day (<code>-1</code>, <code>0</code>, <code>+1</code>).",
  [((["30 3", "0 0", "45 20", "15 23"], 330), [('09:00', 0), ('05:30', 0), ('02:15', 1), ('04:45', 1)]), ((["0 2", "30 23"], -300), [('21:00', -1), ('18:30', 0)])],
  ("Add minutes and fix overflow with if-statements.", "O(n)", "O(n)"),
  ("divmod on total minutes.", "O(n)", "O(n)"),
  viz=((["0 0"], 60)))


@B
def utc_to_local(schedules, offset):
    out = []
    for s in schedules:
        m, h = map(int, s.split())
        total = h * 60 + m + offset
        day = 0
        if total < 0:
            total += 1440
            day = -1
        elif total >= 1440:
            total -= 1440
            day = 1
        out.append((f"{total // 60:02d}:{total % 60:02d}", day))
    return out


@O
def utc_to_local(schedules, offset):
    out = []
    for s in schedules:
        m, h = map(int, s.split())
        day, mins = divmod(h * 60 + m + offset, 1440)
        out.append((f"{mins // 60:02d}:{mins % 60:02d}", day))
    return out


MULTIPLIER = {"linux": 1, "windows": 2, "macos": 10}


Q(None, "What Does CI Cost?", "Easy", "Runner minutes",
  "Jobs are <code>(runner, minutes)</code> per run. Each job's minutes round <b>up</b> to whole minutes, then multiply by the runner's multiplier (Linux 1, Windows 2, macOS 10). Given runs per month and free minutes, return <code>(billable minutes per month, cost at price per minute rounded to 2)</code>.",
  [(([("linux", 3.2), ("linux", 7.9), ("windows", 6.1), ("macos", 11.5)], 400, 3000, 0.008), (55400, 443.2))],
  ("A loop with math.ceil.", "O(j)", "O(1)"),
  ("sum() over a generator.", "O(j)", "O(1)"),
  viz=(([("linux", 1.5)], 10, 0, 0.01)))


@B
def ci_cost(jobs, runs, free, price):
    per_run = 0
    for runner, mins in jobs:
        per_run += math.ceil(mins) * MULTIPLIER[runner]
    billable = per_run * runs - free
    if billable < 0:
        billable = 0
    return (billable, round(billable * price, 2))


@O
def ci_cost(jobs, runs, free, price):
    billable = max(0, runs * sum(math.ceil(m) * MULTIPLIER[r] for r, m in jobs) - free)
    return (billable, round(billable * price, 2))


Q(None, "Split Tests Across Shards", "Medium", "Parallel test jobs",
  "Split test files (with their durations in seconds) across <code>n</code> parallel jobs to minimise the slowest job: sort longest first and give each file to the currently least-loaded shard (ties: lowest shard number). Return <code>(shard totals, slowest shard seconds)</code>.",
  [(({"test_api.py": 210, "test_db.py": 340, "test_cli.py": 30, "test_models.py": 95, "test_auth.py": 160, "test_reports.py": 280, "test_utils.py": 15, "test_e2e.py": 410}, 3), ([505, 515, 520], 520))],
  ("Scan all shards for the minimum each time.", "O(f · n)", "O(n)"),
  ("A min-heap of (load, shard).", "O(f log n)", "O(n)"),
  viz=(({"a": 3, "b": 2, "c": 2}, 2)))


@B
def shard_tests(durations, n):
    loads = [0] * n
    for _, d in sorted(durations.items(), key=lambda x: (-x[1], x[0])):
        i = loads.index(min(loads))
        loads[i] += d
    return (loads, max(loads))


@O
def shard_tests(durations, n):
    heap, loads = [(0, i) for i in range(n)], [0] * n
    for _, d in sorted(durations.items(), key=lambda x: (-x[1], x[0])):
        load, i = heapq.heappop(heap)
        loads[i] = load + d
        heapq.heappush(heap, (loads[i], i))
    return (loads, max(loads))


Q(None, "Re-run Only Failed Jobs", "Easy", "Save time on flaky failures",
  "A pipeline ran jobs <code>(name, minutes, passed)</code>. Re-running the whole workflow costs every job again; re-running failed jobs costs only those. Return <code>(minutes for a full re-run, minutes for failed-only, minutes saved)</code>.",
  [(([("lint", 1, True), ("unit", 6, True), ("integration", 14, False), ("e2e", 22, True), ("build", 9, False)],), (52, 23, 29))],
  ("Two running totals.", "O(j)", "O(1)"),
  ("Two sum() calls.", "O(j)", "O(1)"),
  viz=(([("a", 2, False), ("b", 3, True)],)))


@B
def rerun_cost(jobs):
    full = failed = 0
    for _, m, ok in jobs:
        full += m
        if not ok:
            failed += m
    return (full, failed, full - failed)


@O
def rerun_cost(jobs):
    full, failed = sum(m for _, m, _ in jobs), sum(m for _, m, ok in jobs if not ok)
    return (full, failed, full - failed)


Q(None, "Generate a Changelog", "Medium", "From conventional commits",
  "Group commit subjects into changelog sections in this order: <code>Breaking changes</code> (any <code>!</code> before the colon), <code>Features</code> (feat), <code>Fixes</code> (fix, perf); other types are left out. Return markdown lines: <code>'### Section'</code> followed by <code>'- description (scope)'</code> items (scope only if present), sections without items omitted.",
  [((["feat(api): add bulk export", "fix: handle empty cart", "chore: bump deps", "feat!: drop Python 3.10", "perf(db): batch inserts", "docs: fix typo", "fix(auth): refresh token race"],), ['### Breaking changes', '- drop Python 3.10', '### Features', '- add bulk export (api)', '### Fixes', '- handle empty cart', '- batch inserts (db)', '- refresh token race (auth)'])],
  ("Parse each subject and append to section lists.", "O(c)", "O(c)"),
  ("A regex and a section lookup.", "O(c)", "O(c)"),
  viz=((["feat: x"],)))


@B
def changelog(commits):
    sections = {"Breaking changes": [], "Features": [], "Fixes": []}
    for c in commits:
        head, _, desc = c.partition(": ")
        breaking = head.endswith("!")
        head = head.rstrip("!")
        typ, _, scope = head.partition("(")
        scope = scope.rstrip(")")
        item = "- " + desc + (f" ({scope})" if scope else "")
        if breaking:
            sections["Breaking changes"].append(item)
        elif typ == "feat":
            sections["Features"].append(item)
        elif typ in ("fix", "perf"):
            sections["Fixes"].append(item)
    out = []
    for title, items in sections.items():
        if items:
            out.append("### " + title)
            out += items
    return out


@O
def changelog(commits):
    rx = re.compile(r"^(\w+)(?:\(([^)]*)\))?(!)?: (.*)$")
    sections = {"Breaking changes": [], "Features": [], "Fixes": []}
    for c in commits:
        typ, scope, bang, desc = rx.match(c).groups()
        title = "Breaking changes" if bang else {"feat": "Features", "fix": "Fixes", "perf": "Fixes"}.get(typ)
        if title:
            sections[title].append(f"- {desc}" + (f" ({scope})" if scope else ""))
    return [line for t, items in sections.items() if items for line in [f"### {t}", *items]]


Q(None, "Should This Run Push an Image?", "Easy", "Build everywhere, publish carefully",
  "For each event <code>(event, ref)</code>: pull requests build but never push; a push to <code>refs/heads/main</code> pushes tags <code>main</code> and <code>latest</code>; a tag push <code>refs/tags/vX.Y.Z</code> pushes <code>X.Y.Z</code>; other branches push nothing. Return the list of tags pushed for each event.",
  [(([("pull_request", "refs/pull/42/merge"), ("push", "refs/heads/main"), ("push", "refs/tags/v1.4.2"), ("push", "refs/heads/feature/x"), ("push", "refs/tags/nightly")],), [[], ['main', 'latest'], ['1.4.2'], [], []])],
  ("If/elif per event.", "O(e)", "O(e)"),
  ("A regex for version tags.", "O(e)", "O(e)"),
  viz=(([("push", "refs/heads/main")],)))


@B
def push_tags(events):
    out = []
    for event, ref in events:
        if event == "pull_request":
            out.append([])
        elif ref == "refs/heads/main":
            out.append(["main", "latest"])
        elif ref.startswith("refs/tags/v") and all(p.isdigit() for p in ref[len("refs/tags/v"):].split(".")) and ref.count(".") == 2:
            out.append([ref[len("refs/tags/v"):]])
        else:
            out.append([])
    return out


@O
def push_tags(events):
    def tags(event, ref):
        if event != "push":
            return []
        if ref == "refs/heads/main":
            return ["main", "latest"]
        m = re.fullmatch(r"refs/tags/v(\d+\.\d+\.\d+)", ref)
        return [m[1]] if m else []
    return [tags(e, r) for e, r in events]


Q(None, "Promote Through Environments", "Medium", "dev → staging → prod",
  "A build is deployed to <code>dev</code> if CI passed, promoted to <code>staging</code> if dev's smoke tests passed, and to <code>prod</code> only if staging tests passed <b>and</b> it was approved. Each build is a dict of booleans <code>ci</code>, <code>dev_smoke</code>, <code>staging_tests</code>, <code>approved</code>. Return the furthest environment each build reaches (or <code>'none'</code>).",
  [(([{"ci": True, "dev_smoke": True, "staging_tests": True, "approved": True}, {"ci": True, "dev_smoke": True, "staging_tests": True, "approved": False}, {"ci": True, "dev_smoke": False, "staging_tests": True, "approved": True}, {"ci": False, "dev_smoke": True, "staging_tests": True, "approved": True}],), ['prod', 'staging', 'dev', 'none'])],
  ("Nested if-statements.", "O(b)", "O(b)"),
  ("Walk a list of (environment, gate) pairs.", "O(b)", "O(b)"),
  viz=(([{"ci": True, "dev_smoke": False, "staging_tests": False, "approved": False}],)))


@B
def promotion(builds):
    out = []
    for b in builds:
        env = "none"
        if b["ci"]:
            env = "dev"
            if b["dev_smoke"]:
                env = "staging"
                if b["staging_tests"] and b["approved"]:
                    env = "prod"
        out.append(env)
    return out


@O
def promotion(builds):
    gates = [("dev", lambda b: b["ci"]), ("staging", lambda b: b["dev_smoke"]), ("prod", lambda b: b["staging_tests"] and b["approved"])]
    out = []
    for b in builds:
        env = "none"
        for name, ok in gates:
            if not ok(b):
                break
            env = name
        out.append(env)
    return out


Q(None, "Measure Delivery: DORA Metrics", "Medium", "How good is your delivery pipeline?",
  "Deployments are <code>(deploy hour, commit hour, failed, restored hour or None)</code> over <code>days</code> days. Return <code>{deploys_per_day (rounded to 2), lead_time_hours (median of deploy − commit, rounded to 1), change_failure_pct (rounded to 1), mttr_hours (mean of restored − deploy for failures, rounded to 1)}</code> — the four DORA metrics.",
  [(([(10, 2, False, None), (34, 30, True, 36.5), (58, 41, False, None), (80, 79, False, None), (105, 96, True, 109.0), (130, 120, False, None), (150, 149, False, None)], 7), {'deploys_per_day': 1.0, 'lead_time_hours': 8, 'change_failure_pct': 28.6, 'mttr_hours': 3.2})],
  ("Accumulate in a loop.", "O(n log n)", "O(n)"),
  ("statistics.median and comprehensions.", "O(n log n)", "O(n)"),
  viz=(([(5, 1, False, None)], 1)))


@B
def dora(deploys, days):
    leads = sorted(d - c for d, c, _, _ in deploys)
    n = len(leads)
    median = leads[n // 2] if n % 2 else (leads[n // 2 - 1] + leads[n // 2]) / 2
    fails = [(d, r) for d, _, f, r in deploys if f]
    mttr = 0
    for d, r in fails:
        mttr += r - d
    return {"deploys_per_day": round(len(deploys) / days, 2), "lead_time_hours": round(median, 1),
            "change_failure_pct": round(len(fails) / len(deploys) * 100, 1), "mttr_hours": round(mttr / len(fails), 1) if fails else 0}


@O
def dora(deploys, days):
    fails = [r - d for d, _, f, r in deploys if f]
    return {"deploys_per_day": round(len(deploys) / days, 2), "lead_time_hours": round(statistics.median(d - c for d, c, _, _ in deploys), 1),
            "change_failure_pct": round(100 * len(fails) / len(deploys), 1), "mttr_hours": round(statistics.mean(fails), 1) if fails else 0}


Q(None, "Pass Files Between Jobs", "Easy", "upload-artifact / download-artifact",
  "Jobs run in the listed order; each uploads some artifacts and downloads others. A download fails if no <b>earlier</b> job uploaded that artifact. Return sorted <code>(job, missing artifact)</code> errors and the artifacts uploaded but never downloaded.",
  [(([("build", ["wheel", "sbom"], []), ("test", ["coverage"], ["wheel"]), ("docker", ["image-digest"], ["wheel", "frontend-dist"]), ("deploy", [], ["image-digest", "coverage-badge"])],), ([('deploy', 'coverage-badge'), ('docker', 'frontend-dist')], ['coverage', 'sbom']))],
  ("Lists searched in a loop.", "O(j · a²)", "O(a)"),
  ("Sets of uploaded and downloaded names.", "O(j · a)", "O(a)"),
  viz=(([("a", ["x"], []), ("b", [], ["y"])],)))


@B
def artifacts(jobs):
    uploaded, downloaded, errors = [], [], []
    for name, ups, downs in jobs:
        for d in downs:
            if d not in uploaded:
                errors.append((name, d))
            downloaded.append(d)
        uploaded += ups
    unused = sorted(u for u in uploaded if u not in downloaded)
    return (sorted(errors), unused)


@O
def artifacts(jobs):
    up, down, errors = set(), set(), []
    for name, ups, downs in jobs:
        errors += [(name, d) for d in downs if d not in up]
        down |= set(downs)
        up |= set(ups)
    return (sorted(errors), sorted(up - down))


Q(None, "Pin Third-Party Actions", "Easy", "Supply-chain safety",
  "A tag like <code>@v4</code> can be moved by whoever controls the action, so security-conscious teams pin third-party actions to a full 40-character commit SHA. Return the <code>uses:</code> values that aren't pinned, ignoring local actions (starting with <code>./</code>) and Docker images (starting with <code>docker://</code>).",
  [((["actions/checkout@v4", "astral-sh/setup-uv@b5f58b2abc5763ade55e4e9d0fe52cd1ff7979ca", "./.github/actions/notify", "docker://alpine:3.20", "softprops/action-gh-release@master", "aws-actions/configure-aws-credentials@v4.0.2"],), ['actions/checkout@v4', 'softprops/action-gh-release@master', 'aws-actions/configure-aws-credentials@v4.0.2'])],
  ("Check each part with string methods.", "O(n)", "O(n)"),
  ("A regex for a 40-hex SHA.", "O(n)", "O(n)"),
  viz=((["a/b@v1"],)))


@B
def unpinned_actions(uses):
    out = []
    for u in uses:
        if u.startswith("./") or u.startswith("docker://"):
            continue
        ref = u.split("@")[-1]
        if not (len(ref) == 40 and all(c in "0123456789abcdef" for c in ref)):
            out.append(u)
    return out


@O
def unpinned_actions(uses):
    return [u for u in uses if not u.startswith(("./", "docker://")) and not re.search(r"@[0-9a-f]{40}$", u)]


NEEDS = {"checkout": {"contents": "read"}, "create release": {"contents": "write"}, "push image": {"packages": "write"},
         "comment on PR": {"pull-requests": "write"}, "read PR": {"pull-requests": "read"}, "deploy to AWS": {"id-token": "write"},
         "upload SARIF": {"security-events": "write"}}


Q(None, "Least-Privilege Token Permissions", "Medium", "permissions:",
  "Each step needs certain <code>GITHUB_TOKEN</code> scopes (<code>NEEDS</code>). Return the smallest <code>permissions:</code> block for each job: for each scope, <code>'write'</code> if any step needs write, else <code>'read'</code>; sorted by scope. Granting only what's needed limits damage if a step is compromised.",
  [(({"test": ["checkout"], "release": ["checkout", "create release", "push image"], "review": ["read PR", "checkout", "comment on PR"], "deploy": ["checkout", "deploy to AWS", "upload SARIF"]},), {'test': {'contents': 'read'}, 'release': {'contents': 'write', 'packages': 'write'}, 'review': {'contents': 'read', 'pull-requests': 'write'}, 'deploy': {'contents': 'read', 'id-token': 'write', 'security-events': 'write'}})],
  ("Merge scope dicts with if-statements.", "O(j · s)", "O(p)"),
  ("max() with write ranked above read.", "O(j · s)", "O(p)"),
  viz=(({"a": ["checkout", "create release"]},)))


@B
def permissions(jobs):
    out = {}
    for job, steps in jobs.items():
        perms = {}
        for st in steps:
            for scope, level in NEEDS[st].items():
                if perms.get(scope) != "write":
                    perms[scope] = level
        out[job] = dict(sorted(perms.items()))
    return out


@O
def permissions(jobs):
    rank = {"read": 0, "write": 1}
    def merge(steps):
        p = defaultdict(lambda: "read")
        for st in steps:
            for scope, lvl in NEEDS[st].items():
                p[scope] = max(p[scope], lvl, key=rank.get)
        return dict(sorted(p.items()))
    return {j: merge(s) for j, s in jobs.items()}
