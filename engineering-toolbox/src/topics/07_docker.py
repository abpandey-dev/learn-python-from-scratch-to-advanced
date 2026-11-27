from lib import *
import fnmatch
import heapq
import math
import re
from collections import defaultdict

TOPIC(
    id="docker", title="Docker & Containers", glyph="🐳",
    blurb="Containers from the inside: image references, layer caching and instruction order, multi-stage sizes, .dockerignore, Dockerfile linting, ARG and ENV, port conflicts, compose start order and variables, restart policies, health checks, CPU and memory limits, volumes, release tags, digest pinning, compose logs, base images, and Kubernetes QoS, rolling updates and probes.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">docker build -t invoice-api:1.4.2 .        # build an image from ./Dockerfile
docker run -d -p 8000:8000 --env-file .env --name api invoice-api:1.4.2
docker ps; docker logs -f api; docker exec -it api sh; docker stop api
docker compose up -d --build               # start the whole stack
docker image ls; docker system df          # what's using space</code></pre>
<p>An image is a stack of read-only layers, one per instruction; a container is a running image plus a thin writable layer that disappears when it's removed.</p>
""")


Q(None, "Read an Image Reference", "Easy", "registry/namespace/name:tag@digest",
  "Split each image reference into <code>{registry, repository, tag, digest}</code> with Docker's defaults: no registry → <code>docker.io</code>; a single-name Docker Hub image gets the <code>library/</code> namespace; no tag → <code>latest</code> (unless pinned by digest, then tag is None). A first part is a registry only if it contains a <code>.</code> or <code>:</code> or is <code>localhost</code>.",
  [((["python:3.12-slim", "nginx", "ghcr.io/acme/api:1.4.2", "localhost:5000/tools/cli", "postgres@sha256:ab12cd", "bitnami/redis:7.4"],), [{'registry': 'docker.io', 'repository': 'library/python', 'tag': '3.12-slim', 'digest': None}, {'registry': 'docker.io', 'repository': 'library/nginx', 'tag': 'latest', 'digest': None}, {'registry': 'ghcr.io', 'repository': 'acme/api', 'tag': '1.4.2', 'digest': None}, {'registry': 'localhost:5000', 'repository': 'tools/cli', 'tag': 'latest', 'digest': None}, {'registry': 'docker.io', 'repository': 'library/postgres', 'tag': None, 'digest': 'sha256:ab12cd'}, {'registry': 'docker.io', 'repository': 'bitnami/redis', 'tag': '7.4', 'digest': None}])],
  ("Partition step by step.", "O(n · L)", "O(L)"),
  ("A regular expression per reference.", "O(n · L)", "O(L)"),
  viz=((["redis:7"],)))


@B
def image_ref(refs):
    out = []
    for ref in refs:
        rest, _, digest = ref.partition("@")
        parts = rest.split("/")
        if len(parts) > 1 and ("." in parts[0] or ":" in parts[0] or parts[0] == "localhost"):
            registry, parts = parts[0], parts[1:]
        else:
            registry = "docker.io"
        path = "/".join(parts)
        tag = None
        if ":" in parts[-1]:
            path, tag = path.rsplit(":", 1)
        if registry == "docker.io" and "/" not in path:
            path = "library/" + path
        if tag is None and not digest:
            tag = "latest"
        out.append({"registry": registry, "repository": path, "tag": tag, "digest": digest or None})
    return out


@O
def image_ref(refs):
    rx = re.compile(r"^(?:(?P<reg>[^/]+[.:][^/]*|localhost)/)?(?P<repo>[^:@]+)(?::(?P<tag>[^@]+))?(?:@(?P<dig>.+))?$")
    out = []
    for ref in refs:
        m = rx.match(ref)
        reg = m["reg"] or "docker.io"
        repo = m["repo"] if reg != "docker.io" or "/" in m["repo"] else "library/" + m["repo"]
        out.append({"registry": reg, "repository": repo, "tag": m["tag"] or (None if m["dig"] else "latest"), "digest": m["dig"]})
    return out


Q(None, "Which Layers Rebuild?", "Medium", "Order your Dockerfile for the cache",
  "Each Dockerfile step is <code>(instruction, files it copies)</code>. Docker reuses cached layers until the first step whose inputs changed (a COPY of a changed file); that step and <b>every later step</b> rebuild. Return the indexes (0-based) of rebuilt steps for each set of changed files — compare copying everything early with copying the dependency list first.",
  [(([("FROM python:3.12-slim", []), ("WORKDIR /app", []), ("COPY . .", ["requirements.txt", "app/main.py", "app/db.py"]), ("RUN pip install -r requirements.txt", []), ("CMD uvicorn app.main:app", [])], [["app/main.py"], ["requirements.txt"]]), [[2, 3, 4], [2, 3, 4]]),
   (([("FROM python:3.12-slim", []), ("WORKDIR /app", []), ("COPY requirements.txt .", ["requirements.txt"]), ("RUN pip install -r requirements.txt", []), ("COPY app/ app/", ["app/main.py", "app/db.py"]), ("CMD uvicorn app.main:app", [])], [["app/main.py"], ["requirements.txt"]]), [[4, 5], [2, 3, 4, 5]])],
  ("Scan steps for each change set.", "O(c · s · f)", "O(s)"),
  ("next() for the first invalidated step, then a range.", "O(c · s · f)", "O(s)"),
  viz=(([("FROM x", []), ("COPY a .", ["a"]), ("RUN b", [])], [["a"]])))


@B
def rebuilt_steps(steps, changes):
    out = []
    for changed in changes:
        first = None
        for i, (_, files) in enumerate(steps):
            for f in files:
                if f in changed and first is None:
                    first = i
        out.append([] if first is None else list(range(first, len(steps))))
    return out


@O
def rebuilt_steps(steps, changes):
    out = []
    for changed in changes:
        first = next((i for i, (_, files) in enumerate(steps) if set(files) & set(changed)), len(steps))
        out.append(list(range(first, len(steps))))
    return out


Q(None, "Multi-Stage Builds Shrink Images", "Easy", "Ship only what runs",
  "A build has stages, each a list of <code>(layer name, size MB)</code>; the final stage also lists the files it copies <code>from</code> earlier stages (<code>(name, size)</code>). A single-stage image contains every layer of every stage; a multi-stage image contains only the final stage's layers plus the copied artefacts. Return both sizes in MB (rounded to 1).",
  [(({"builder": [("python:3.12 base", 1020.0), ("build-essential", 260.0), ("pip install wheels", 410.0), ("source", 3.2)], "final": [("python:3.12-slim base", 130.0), ("app user", 0.1)]}, [("site-packages", 180.0), ("source", 3.2)]), (1823.3, 313.3))],
  ("Add sizes with loops.", "O(l)", "O(1)"),
  ("sum() over generators.", "O(l)", "O(1)"),
  viz=(({"b": [("x", 10.0)], "final": [("y", 1.0)]}, [("z", 2.0)])))


@B
def image_sizes(stages, copied):
    single = 0.0
    for layers in stages.values():
        for _, size in layers:
            single += size
    multi = 0.0
    for _, size in stages["final"]:
        multi += size
    for _, size in copied:
        multi += size
    return (round(single, 1), round(multi, 1))


@O
def image_sizes(stages, copied):
    return (round(sum(s for layers in stages.values() for _, s in layers), 1),
            round(sum(s for _, s in stages["final"]) + sum(s for _, s in copied), 1))


Q(None, "What Goes Into the Build Context?", "Medium", ".dockerignore",
  "Docker sends the build context (the folder) to the builder, minus <code>.dockerignore</code> matches. Patterns match from the context root (<code>*</code> doesn't cross <code>/</code>, <code>**</code> matches any number of folders), a pattern also excludes everything inside a matching folder, and <code>!</code> re-includes; the last match wins. Return <code>(files sent, MB sent rounded to 1, MB saved rounded to 1)</code>.",
  [(({".git/objects/pack/p1": 380.0, ".venv/lib/torch/lib.so": 2100.0, "app/main.py": 0.02, "app/db.py": 0.01, "tests/test_api.py": 0.01, "data/train.parquet": 850.0, "data/README.md": 0.01, "requirements.txt": 0.001, "notes/todo.log": 0.3, "app/debug.log": 0.2}, [".git", ".venv", "data", "!data/README.md", "**/*.log", "tests"]), (['app/db.py', 'app/main.py', 'data/README.md', 'requirements.txt'], 0.0, 3330.5))],
  ("Match with fnmatch on every prefix of the path.", "O(f · p · d)", "O(f)"),
  ("A compiled regex per pattern.", "O(f · p)", "O(f)"),
  viz=(({"a.log": 1.0, "b.py": 1.0}, ["*.log"])))


def ignore_rx(pattern):
    r = ""
    for tok in re.split(r"(\*\*/|\*\*|\*|\?)", pattern.strip("/")):
        r += {"**/": "(?:.*/)?", "**": ".*", "*": "[^/]*", "?": "[^/]"}.get(tok, re.escape(tok))
    return re.compile(r + "(?:/.*)?$")


@B
def build_context(files, patterns):
    sent = []
    for path in sorted(files):
        excluded = False
        for p in patterns:
            neg = p.startswith("!")
            if ignore_rx(p.lstrip("!")).match(path):
                excluded = not neg
        if not excluded:
            sent.append(path)
    total = sum(files.values())
    size = sum(files[p] for p in sent)
    return (sent, round(size, 1), round(total - size, 1))


@O
def build_context(files, patterns):
    rules = [(p.startswith("!"), ignore_rx(p.lstrip("!"))) for p in reversed(patterns)]
    keep = lambda path: next((neg for neg, rx in rules if rx.match(path)), True)
    sent = sorted(p for p in files if keep(p))
    size = sum(files[p] for p in sent)
    return (sent, round(size, 1), round(sum(files.values()) - size, 1))


Q(None, "Lint a Dockerfile", "Medium", "hadolint-style rules",
  "Return sorted <code>(line, rule)</code> findings: <code>'pin base image'</code> (FROM without a tag, or with <code>:latest</code>), <code>'clean apt lists'</code> (RUN with <code>apt-get install</code> but no <code>rm -rf /var/lib/apt/lists</code>), <code>'pip no-cache'</code> (pip install without <code>--no-cache-dir</code>), <code>'use COPY'</code> (ADD of a local path, not a URL), and <code>'runs as root'</code> (no USER instruction anywhere; report line 0).",
  [((["FROM python:latest", "RUN apt-get update && apt-get install -y gcc", "ADD . /app", "RUN pip install -r /app/requirements.txt", "ADD https://example.com/model.bin /models/", "CMD [\"python\", \"/app/main.py\"]"],), [(0, 'runs as root'), (1, 'pin base image'), (2, 'clean apt lists'), (3, 'use COPY'), (4, 'pip no-cache')]),
   ((["FROM python:3.12-slim", "RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*", "COPY . /app", "RUN pip install --no-cache-dir -r /app/requirements.txt", "USER app", "CMD [\"python\", \"/app/main.py\"]"],), [])],
  ("If-statements per instruction.", "O(n)", "O(n)"),
  ("A table of (instruction, check, rule).", "O(n · r)", "O(n)"),
  viz=((["FROM ubuntu"],)))


@B
def lint_dockerfile(lines):
    out, has_user = [], False
    for i, line in enumerate(lines, 1):
        ins, _, rest = line.partition(" ")
        if ins == "FROM":
            image = rest.split()[0]
            if ":" not in image.split("/")[-1] or image.endswith(":latest"):
                out.append((i, "pin base image"))
        if ins == "RUN" and "apt-get install" in rest and "rm -rf /var/lib/apt/lists" not in rest:
            out.append((i, "clean apt lists"))
        if ins == "RUN" and "pip install" in rest and "--no-cache-dir" not in rest:
            out.append((i, "pip no-cache"))
        if ins == "ADD" and not rest.startswith(("http://", "https://")):
            out.append((i, "use COPY"))
        if ins == "USER":
            has_user = True
    if not has_user:
        out.append((0, "runs as root"))
    return sorted(out)


@O
def lint_dockerfile(lines):
    rules = [("FROM", lambda r: ":" not in r.split()[0].split("/")[-1] or r.split()[0].endswith(":latest"), "pin base image"),
             ("RUN", lambda r: "apt-get install" in r and "rm -rf /var/lib/apt/lists" not in r, "clean apt lists"),
             ("RUN", lambda r: "pip install" in r and "--no-cache-dir" not in r, "pip no-cache"),
             ("ADD", lambda r: not r.startswith(("http://", "https://")), "use COPY")]
    parsed = [l.partition(" ")[::2] for l in lines]
    out = [(i, name) for i, (ins, rest) in enumerate(parsed, 1) for kind, bad, name in rules if ins == kind and bad(rest)]
    if all(ins != "USER" for ins, _ in parsed):
        out.append((0, "runs as root"))
    return sorted(out)


Q(None, "Resolve ARG and ENV", "Medium", "Build-time vs run-time variables",
  "Process <code>ARG name=default</code> and <code>ENV name=value</code> lines in order. <code>${name}</code> in a value expands from the ENV and ARG values seen so far (ENV wins). <code>build_args</code> (from <code>--build-arg</code>) override ARG defaults. Return <code>(environment variables in the final image, sorted items)</code> — ARGs don't survive into the running container unless copied into an ENV.",
  [((["ARG PYTHON_VERSION=3.12", "ARG APP_VERSION=dev", "ENV APP_HOME=/srv/app", "ENV PATH=${APP_HOME}/bin:/usr/bin", "ENV APP_VERSION=${APP_VERSION}", "ARG SECRET_TOKEN", "ENV PYTHONUNBUFFERED=1"], {"APP_VERSION": "1.4.2", "SECRET_TOKEN": "abc"}), [('APP_HOME', '/srv/app'), ('APP_VERSION', '1.4.2'), ('PATH', '/srv/app/bin:/usr/bin'), ('PYTHONUNBUFFERED', '1')])],
  ("Two dicts and a manual ${} scanner.", "O(n · L)", "O(n)"),
  ("re.sub with a lookup function.", "O(n · L)", "O(n)"),
  viz=((["ARG A=1", "ENV B=${A}"], {})))


@B
def docker_env(lines, build_args):
    args, env = {}, {}
    for line in lines:
        ins, _, rest = line.partition(" ")
        name, _, value = rest.partition("=")
        while "${" in value:
            s = value.index("${")
            e = value.index("}", s)
            key = value[s + 2:e]
            value = value[:s] + env.get(key, args.get(key, "")) + value[e + 1:]
        if ins == "ARG":
            args[name] = build_args.get(name, value)
        else:
            env[name] = value
    return sorted(env.items())


@O
def docker_env(lines, build_args):
    args, env = {}, {}
    for line in lines:
        ins, _, rest = line.partition(" ")
        name, _, value = rest.partition("=")
        value = re.sub(r"\$\{(\w+)\}", lambda m: env.get(m[1], args.get(m[1], "")), value)
        if ins == "ARG":
            args[name] = build_args.get(name, value)
        else:
            env[name] = value
    return sorted(env.items())


Q(None, "Port Mapping Conflicts", "Easy", "-p host:container",
  "Services publish ports as <code>'host:container'</code>. Two services can't bind the same host port. Return <code>(urls as 'service -> http://localhost:HOST' in input order, conflicts as sorted (port, [services]))</code>.",
  [(({"api": ["8000:8000"], "web": ["3000:80"], "admin": ["8000:8080"], "db": ["5432:5432"], "grafana": ["3000:3000", "9090:9090"]},), (['api -> http://localhost:8000', 'web -> http://localhost:3000', 'admin -> http://localhost:8000', 'db -> http://localhost:5432', 'grafana -> http://localhost:3000', 'grafana -> http://localhost:9090'], [(3000, ['web', 'grafana']), (8000, ['api', 'admin'])]))],
  ("Group by host port with a dict of lists.", "O(p)", "O(p)"),
  ("defaultdict and comprehensions.", "O(p)", "O(p)"),
  viz=(({"a": ["80:80"], "b": ["80:81"]},)))


@B
def port_conflicts(services):
    urls, used = [], {}
    for svc, ports in services.items():
        for p in ports:
            host = p.split(":")[0]
            urls.append(f"{svc} -> http://localhost:{host}")
            used.setdefault(int(host), []).append(svc)
    conflicts = []
    for port in sorted(used):
        if len(used[port]) > 1:
            conflicts.append((port, used[port]))
    return (urls, conflicts)


@O
def port_conflicts(services):
    used = defaultdict(list)
    urls = []
    for svc, ports in services.items():
        for host in (p.split(":")[0] for p in ports):
            urls.append(f"{svc} -> http://localhost:{host}")
            used[int(host)].append(svc)
    return (urls, sorted((p, s) for p, s in used.items() if len(s) > 1))


Q(None, "Compose Start Order", "Medium", "depends_on with health checks",
  "Each service has <code>depends_on</code> (services that must be <b>healthy</b> first) and seconds it takes from start to healthy. A service starts as soon as all its dependencies are healthy. Return <code>{service: [start second, healthy second]}</code> and the time until everything is healthy.",
  [(({"db": [], "redis": [], "migrate": ["db"], "api": ["db", "redis", "migrate"], "worker": ["redis", "db"], "web": ["api"]}, {"db": 8, "redis": 2, "migrate": 5, "api": 4, "worker": 3, "web": 1}), ({'db': [0, 8], 'redis': [0, 2], 'migrate': [8, 13], 'api': [13, 17], 'worker': [8, 11], 'web': [17, 18]}, 18))],
  ("Repeatedly compute start times until nothing changes.", "O(n²)", "O(n)"),
  ("Memoised recursion: start = max of dependencies' healthy times.", "O(n + e)", "O(n)"),
  viz=(({"a": [], "b": ["a"]}, {"a": 2, "b": 1})))


@B
def compose_order(deps, ready):
    start = {s: 0 for s in deps}
    changed = True
    while changed:
        changed = False
        for s, ds in deps.items():
            t = max([start[d] + ready[d] for d in ds], default=0)
            if t != start[s]:
                start[s], changed = t, True
    out = {s: [start[s], start[s] + ready[s]] for s in deps}
    return (out, max(v[1] for v in out.values()))


@O
def compose_order(deps, ready):
    from functools import lru_cache
    @lru_cache(None)
    def healthy(s):
        return max((healthy(d) for d in deps[s]), default=0) + ready[s]
    out = {s: [healthy(s) - ready[s], healthy(s)] for s in deps}
    return (out, max(healthy(s) for s in deps))


Q(None, "Interpolate Compose Variables", "Medium", "${VAR:-default} and ${VAR:?error}",
  "Docker Compose fills <code>${VAR}</code> from the environment, <code>${VAR:-default}</code> uses the default when unset or empty, and <code>${VAR:?message}</code> stops with an error when unset or empty. Return each resolved value, or <code>'error: message'</code>.",
  [((["postgres://${DB_USER}:${DB_PASS:?set DB_PASS}@db:5432/${DB_NAME:-app}", "${API_PORT:-8000}", "${IMAGE_TAG:?IMAGE_TAG is required}", "redis://${REDIS_HOST:-redis}:6379"], {"DB_USER": "app", "DB_PASS": "s3cret", "REDIS_HOST": "", "IMAGE_TAG": ""}), ['postgres://app:s3cret@db:5432/app', '8000', 'error: IMAGE_TAG is required', 'redis://redis:6379'])],
  ("Scan for ${...} with index().", "O(n · L)", "O(L)"),
  ("re.sub with a function that may raise.", "O(n · L)", "O(L)"),
  viz=((["${A:-x}"], {})))


@B
def compose_vars(values, env):
    out = []
    for v in values:
        result, error = "", None
        i = 0
        while i < len(v):
            if v.startswith("${", i):
                j = v.index("}", i)
                inner = v[i + 2:j]
                if ":?" in inner:
                    name, msg = inner.split(":?", 1)
                    if not env.get(name):
                        error = msg
                        break
                    result += env[name]
                elif ":-" in inner:
                    name, default = inner.split(":-", 1)
                    result += env.get(name) or default
                else:
                    result += env.get(inner, "")
                i = j + 1
            else:
                result += v[i]
                i += 1
        out.append(f"error: {error}" if error else result)
    return out


@O
def compose_vars(values, env):
    def sub(m):
        name, op, arg = m.group(1), m.group(2), m.group(3)
        val = env.get(name, "")
        if op == ":?" and not val:
            raise ValueError(arg)
        return val or (arg if op == ":-" else "")
    out = []
    for v in values:
        try:
            out.append(re.sub(r"\$\{(\w+)(?:(:-|:\?)([^}]*))?\}", sub, v))
        except ValueError as e:
            out.append(f"error: {e}")
    return out


Q(None, "Restart Policies", "Medium", "no, on-failure, always",
  "A container exits with each code in <code>exits</code> in turn (it would run again if restarted). Policies: <code>'no'</code> never restarts; <code>'on-failure:N'</code> restarts after non-zero exits, at most N times; <code>'always'</code> restarts after any exit. Return <code>(restarts, final exit code)</code> for each policy. (Docker also adds growing delays between restarts.)",
  [(([1, 1, 137, 0, 2], ["no", "on-failure:2", "on-failure:5", "always"]), [(0, 1), (2, 137), (3, 0), (4, 2)])],
  ("Simulate each policy with a loop.", "O(p · e)", "O(1)"),
  ("Parse the policy into (restart test, limit) first.", "O(p · e)", "O(1)"),
  viz=(([1, 0], ["always"])))


@B
def restarts(exits, policies):
    out = []
    for pol in policies:
        n, i = 0, 0
        while True:
            code = exits[i]
            if pol == "no":
                break
            if pol == "always":
                ok = True
            else:
                ok = code != 0 and n < int(pol.split(":")[1])
            if not ok or i == len(exits) - 1:
                break
            n += 1
            i += 1
        out.append((n, exits[i]))
    return out


@O
def restarts(exits, policies):
    out = []
    for pol in policies:
        name, _, lim = pol.partition(":")
        limit = int(lim) if lim else math.inf
        n = 0
        for i, code in enumerate(exits):
            again = name == "always" or (name == "on-failure" and code != 0 and n < limit)
            if not again or i == len(exits) - 1:
                out.append((n, code))
                break
            n += 1
    return out


Q(None, "When Is a Container Unhealthy?", "Medium", "HEALTHCHECK settings",
  "A health probe runs every <code>interval</code> seconds starting at second <code>interval</code>, with results in <code>results</code>. Failures during the first <code>start_period</code> seconds don't count. The container becomes <code>unhealthy</code> after <code>retries</code> consecutive counted failures, and healthy again on the next success. Return the list of <code>(second, new status)</code> changes, starting from <code>'starting'</code> (the first success makes it <code>'healthy'</code>).",
  [(([False, False, False, True, True, False, False, False, True, False], 10, 25, 3), [(40, 'healthy'), (80, 'unhealthy'), (90, 'healthy')])],
  ("Simulate probe by probe.", "O(n)", "O(1)"),
  ("Same with a status variable and a change list.", "O(n)", "O(c)"),
  viz=(([False, True], 5, 0, 1)))


@B
def health_status(results, interval, start_period, retries):
    status, fails, changes = "starting", 0, []
    for i, ok in enumerate(results, 1):
        t = i * interval
        if ok:
            fails = 0
            if status != "healthy":
                status = "healthy"
                changes.append((t, status))
        elif t > start_period:
            fails += 1
            if fails >= retries and status != "unhealthy":
                status = "unhealthy"
                changes.append((t, status))
    return changes


@O
def health_status(results, interval, start_period, retries):
    status, fails, changes = "starting", 0, []
    for t, ok in zip(range(interval, interval * (len(results) + 1), interval), results):
        fails = 0 if ok else fails + (t > start_period)
        new = "healthy" if ok else "unhealthy" if fails >= retries else status
        if new != status:
            status = new
            changes.append((t, status))
    return changes


Q(None, "Share CPUs Fairly", "Hard", "Limits and contention",
  "Containers want <code>demand</code> CPUs but are capped at <code>limit</code>. The host has <code>cpus</code> cores. Allocate by <b>water-filling</b>: give every unsatisfied container an equal share, cap those that need less, and redistribute the leftover until all are satisfied or the CPUs are used up. Return allocations rounded to 2.",
  [(({"api": 2.0, "worker": 6.0, "cron": 0.5, "ml": 8.0}, {"api": 2.0, "worker": 4.0, "cron": 1.0, "ml": 8.0}, 8), {'api': 2.0, 'worker': 2.75, 'cron': 0.5, 'ml': 2.75}), (({"a": 1.0, "b": 1.0}, {"a": 1.0, "b": 0.5}, 4), {'a': 1.0, 'b': 0.5})],
  ("Repeated equal splits until stable.", "O(c²)", "O(c)"),
  ("Sort by need and fill from the smallest.", "O(c log c)", "O(c)"),
  viz=(({"a": 3.0, "b": 1.0}, {"a": 3.0, "b": 1.0}, 2)))


@B
def cpu_share(demand, limit, cpus):
    need = {c: min(demand[c], limit[c]) for c in demand}
    alloc = {c: 0.0 for c in demand}
    left = float(cpus)
    active = [c for c in need if need[c] > 0]
    while active and left > 1e-9:
        share = left / len(active)
        nxt = []
        for c in active:
            give = min(share, need[c] - alloc[c])
            alloc[c] += give
            left -= give
            if need[c] - alloc[c] > 1e-9:
                nxt.append(c)
        if len(nxt) == len(active):
            break
        active = nxt
    return {c: round(v, 2) for c, v in alloc.items()}


@O
def cpu_share(demand, limit, cpus):
    need = sorted((min(demand[c], limit[c]), c) for c in demand)
    alloc, left = {}, float(cpus)
    for i, (n, c) in enumerate(need):
        give = min(n, left / (len(need) - i))
        alloc[c], left = give, left - give
    return {c: round(alloc[c], 2) for c in demand}


Q(None, "Where Does the Data Go?", "Medium", "Volumes, bind mounts and the container layer",
  "Mounts map container paths to a named volume (<code>'vol:NAME'</code>) or a host folder (<code>'host:/path'</code>). A file written in the container lands in the mount with the <b>longest</b> matching path prefix, or in the container's writable layer (<code>'container layer (lost on removal)'</code>). Return where each written path ends up.",
  [(({"/var/lib/postgresql/data": "vol:pgdata", "/app": "host:/home/asha/proj", "/app/uploads": "vol:uploads"}, ["/var/lib/postgresql/data/base/1", "/app/main.py", "/app/uploads/a.png", "/tmp/cache.bin", "/application/x"]), {'/var/lib/postgresql/data/base/1': 'volume pgdata', '/app/main.py': '/home/asha/proj/main.py', '/app/uploads/a.png': 'volume uploads', '/tmp/cache.bin': 'container layer (lost on removal)', '/application/x': 'container layer (lost on removal)'})],
  ("Check every mount with startswith.", "O(f · m)", "O(1)"),
  ("Sort mounts by length once, take the first match.", "O(m log m + f · m)", "O(m)"),
  viz=(({"/data": "vol:d"}, ["/data/x", "/tmp/y"])))


@B
def data_location(mounts, writes):
    out = {}
    for f in writes:
        best = None
        for path, target in mounts.items():
            if (f == path or f.startswith(path + "/")) and (best is None or len(path) > len(best)):
                best = path
        if best is None:
            out[f] = "container layer (lost on removal)"
        else:
            kind, name = mounts[best].split(":", 1)
            out[f] = f"volume {name}" if kind == "vol" else name + f[len(best):]
    return out


@O
def data_location(mounts, writes):
    ordered = sorted(mounts, key=len, reverse=True)
    def where(f):
        p = next((p for p in ordered if f == p or f.startswith(p + "/")), None)
        if p is None:
            return "container layer (lost on removal)"
        kind, name = mounts[p].split(":", 1)
        return f"volume {name}" if kind == "vol" else name + f[len(p):]
    return {f: where(f) for f in writes}


Q(None, "Tag an Image for Release", "Easy", "Traceable tags",
  "Given the git commit sha, branch and an optional release version, return the image tags: always <code>sha-</code> + the first 7 characters; the branch with <code>/</code> turned into <code>-</code> and lower-cased; and for a version <code>X.Y.Z</code> also <code>X.Y.Z</code>, <code>X.Y</code> and <code>X</code>, plus <code>latest</code> when the branch is <code>main</code>.",
  [(("9f3a2c1d7e4b", "feature/Login-Form", None), ['sha-9f3a2c1', 'feature-login-form']), (("0b7e44aa19cc", "main", "1.4.2"), ['sha-0b7e44a', 'main', '1.4.2', '1.4', '1', 'latest'])],
  ("Append tags step by step.", "O(1)", "O(1)"),
  ("Build the version tags with a slice loop.", "O(1)", "O(1)"),
  viz=(("abcdef123", "main", None)))


@B
def release_tags(sha, branch, version):
    tags = ["sha-" + sha[:7], branch.replace("/", "-").lower()]
    if version:
        major, minor, patch = version.split(".")
        tags += [version, major + "." + minor, major]
        if branch == "main":
            tags.append("latest")
    return tags


@O
def release_tags(sha, branch, version):
    tags = [f"sha-{sha[:7]}", branch.replace("/", "-").lower()]
    if version:
        parts = version.split(".")
        tags += [".".join(parts[:i]) for i in (3, 2, 1)] + ["latest"] * (branch == "main")
    return tags


Q(None, "Pin Base Images by Digest", "Easy", "Reproducible builds",
  "Tags like <code>python:3.12-slim</code> can be moved to new images. Rewrite each <code>FROM</code> line to pin the digest from <code>digests</code> (tag → digest), keeping any <code>AS name</code>, e.g. <code>FROM python:3.12-slim@sha256:… AS build</code>. Lines with unknown images or other instructions are unchanged.",
  [((["FROM python:3.12-slim AS build", "RUN pip wheel -r requirements.txt", "FROM gcr.io/distroless/python3", "FROM python:3.12-slim", "COPY --from=build /wheels /wheels"], {"python:3.12-slim": "sha256:4c1fe2", "gcr.io/distroless/python3": "sha256:9ab077"}), ['FROM python:3.12-slim@sha256:4c1fe2 AS build', 'RUN pip wheel -r requirements.txt', 'FROM gcr.io/distroless/python3@sha256:9ab077', 'FROM python:3.12-slim@sha256:4c1fe2', 'COPY --from=build /wheels /wheels'])],
  ("Split each FROM line and rebuild it.", "O(n)", "O(n)"),
  ("One regex substitution per line.", "O(n)", "O(n)"),
  viz=((["FROM a:1"], {"a:1": "sha256:x"})))


@B
def pin_digests(lines, digests):
    out = []
    for line in lines:
        parts = line.split()
        if parts[0] == "FROM" and parts[1] in digests:
            parts[1] = parts[1] + "@" + digests[parts[1]]
            out.append(" ".join(parts))
        else:
            out.append(line)
    return out


@O
def pin_digests(lines, digests):
    return [re.sub(r"^FROM (\S+)", lambda m: f"FROM {m[1]}@{digests[m[1]]}" if m[1] in digests else m[0], l) for l in lines]


Q(None, "Read docker compose logs", "Easy", "Interleave by time",
  "Each container's log is a list of <code>(seconds, line)</code> in order. Merge them by time (ties: container name order) into lines formatted <code>'name | line'</code> with names padded to the longest name, like <code>docker compose logs</code>.",
  [(({"api-1": [(1.0, "started"), (3.5, "GET /orders 200"), (4.0, "GET /health 200")], "worker-1": [(1.2, "connected to redis"), (3.5, "job 17 done")], "db-1": [(0.4, "ready to accept connections")]},), ['db-1     | ready to accept connections', 'api-1    | started', 'worker-1 | connected to redis', 'api-1    | GET /orders 200', 'worker-1 | job 17 done', 'api-1    | GET /health 200'])],
  ("Collect everything and sort.", "O(n log n)", "O(n)"),
  ("heapq.merge of the already-sorted streams.", "O(n log c)", "O(c)"),
  viz=(({"a": [(1, "x")], "b": [(0, "y")]},)))


@B
def compose_logs(logs):
    width = max(len(n) for n in logs)
    rows = []
    for name, lines in logs.items():
        for t, line in lines:
            rows.append((t, name, line))
    rows.sort()
    return [name.ljust(width) + " | " + line for _, name, line in rows]


@O
def compose_logs(logs):
    width = max(map(len, logs))
    streams = [[(t, n, l) for t, l in lines] for n, lines in logs.items()]
    return [f"{n:<{width}} | {l}" for _, n, l in heapq.merge(*streams)]


BASES = [("scratch", 0, set()), ("distroless", 25, {"glibc"}), ("alpine", 8, {"shell", "pkg"}),
         ("debian-slim", 75, {"glibc", "shell", "pkg"}), ("ubuntu", 78, {"glibc", "shell", "pkg", "tools"})]


Q(None, "Pick a Base Image", "Easy", "Smallest that works",
  "Each base in <code>BASES</code> is <code>(name, MB, features)</code>. For each app's needed features, return the smallest base providing all of them. (Alpine uses musl instead of glibc — many Python wheels need glibc.)",
  [(([[], ["glibc"], ["shell"], ["glibc", "shell"], ["glibc", "tools"]],), ['scratch', 'distroless', 'alpine', 'debian-slim', 'ubuntu'])],
  ("Scan bases, keep the smallest match.", "O(a · b)", "O(1)"),
  ("min() with a key over matching bases.", "O(a · b)", "O(1)"),
  viz=(([["shell"]],)))


@B
def pick_base(needs):
    out = []
    for need in needs:
        best = None
        for name, size, feats in BASES:
            if set(need) <= feats and (best is None or size < best[1]):
                best = (name, size)
        out.append(best[0])
    return out


@O
def pick_base(needs):
    return [min((b for b in BASES if set(n) <= b[2]), key=lambda b: b[1])[0] for n in needs]


Q(None, "Kubernetes QoS Classes", "Easy", "Who gets evicted first?",
  "A pod's QoS class comes from its containers' CPU and memory <code>requests</code> and <code>limits</code>: <code>Guaranteed</code> if every container sets both limits and requests equal to them; <code>BestEffort</code> if no container sets any; otherwise <code>Burstable</code>. Under memory pressure BestEffort pods are evicted first.",
  [(([[{"requests": {"cpu": "500m", "memory": "512Mi"}, "limits": {"cpu": "500m", "memory": "512Mi"}}],
      [{"requests": {"cpu": "250m"}, "limits": {"memory": "1Gi"}}],
      [{"requests": {}, "limits": {}}, {"requests": {}, "limits": {}}],
      [{"requests": {"cpu": "1", "memory": "1Gi"}, "limits": {"cpu": "1", "memory": "1Gi"}}, {"requests": {}, "limits": {}}]],), ['Guaranteed', 'Burstable', 'BestEffort', 'Burstable'])],
  ("Flags per container.", "O(p · c)", "O(1)"),
  ("all()/any() over containers.", "O(p · c)", "O(1)"),
  viz=(([[{"requests": {}, "limits": {}}]],)))


@B
def qos(pods):
    out = []
    for containers in pods:
        any_set = False
        guaranteed = True
        for c in containers:
            if c["requests"] or c["limits"]:
                any_set = True
            for r in ("cpu", "memory"):
                if r not in c["limits"] or c["requests"].get(r, c["limits"][r]) != c["limits"][r]:
                    guaranteed = False
        out.append("Guaranteed" if guaranteed else "Burstable" if any_set else "BestEffort")
    return out


@O
def qos(pods):
    def guaranteed(c):
        return all(r in c["limits"] and c["requests"].get(r, c["limits"][r]) == c["limits"][r] for r in ("cpu", "memory"))
    return ["Guaranteed" if all(map(guaranteed, p)) else "Burstable" if any(c["requests"] or c["limits"] for c in p) else "BestEffort" for p in pods]


Q(None, "Plan a Rolling Update", "Medium", "maxSurge and maxUnavailable",
  "A Deployment with <code>replicas</code> pods updates in waves. Each wave may run up to <code>replicas + max_surge</code> pods and must keep at least <code>replicas − max_unavailable</code> available, so each wave replaces <code>max_surge + max_unavailable</code> pods. Return <code>(most pods at once, fewest available, waves)</code> for each setting.",
  [((10, [(1, 0), (2, 1), (0, 2), (25, 0)]), [(11, 10, 10), (12, 9, 4), (10, 8, 5), (20, 10, 1)])],
  ("Simulate the waves with a counter.", "O(r)", "O(1)"),
  ("Ceiling division.", "O(1)", "O(1)"),
  viz=((4, [(1, 1)])))


@B
def rolling_update(replicas, settings):
    out = []
    for surge, unavailable in settings:
        left, waves = replicas, 0
        while left > 0:
            left -= surge + unavailable
            waves += 1
        out.append((replicas + min(surge, replicas), replicas - unavailable, waves))
    return out


@O
def rolling_update(replicas, settings):
    return [(replicas + min(s, replicas), replicas - u, math.ceil(replicas / (s + u))) for s, u in settings]


Q(None, "Liveness vs Readiness Probes", "Medium", "Restart or stop sending traffic?",
  "Every 10 s a pod's liveness and readiness probes run. After <code>threshold</code> consecutive <b>readiness</b> failures the pod is removed from the Service (no traffic) until readiness passes again; after <code>threshold</code> consecutive <b>liveness</b> failures the container is restarted (counters reset, and it's not ready until readiness passes). Return the list of <code>(second, action)</code> events: <code>'remove from service'</code>, <code>'add to service'</code>, <code>'restart'</code>.",
  [(([(True, True), (True, False), (True, False), (True, False), (True, True), (False, False), (False, False), (False, False), (True, True)], 3), [(40, 'remove from service'), (50, 'add to service'), (80, 'restart'), (90, 'add to service')])],
  ("Counters and flags in a loop.", "O(n)", "O(1)"),
  ("Same state machine, compact.", "O(n)", "O(1)"),
  viz=(([(True, False), (True, True)], 1)))


@B
def probes(results, threshold):
    events, ready, live_fails, ready_fails = [], True, 0, 0
    for i, (live, rdy) in enumerate(results, 1):
        t = i * 10
        live_fails = 0 if live else live_fails + 1
        ready_fails = 0 if rdy else ready_fails + 1
        if live_fails >= threshold:
            events.append((t, "restart"))
            live_fails = ready_fails = 0
            if ready:
                ready = False
            continue
        if ready and ready_fails >= threshold:
            ready = False
            events.append((t, "remove from service"))
        elif not ready and rdy:
            ready = True
            events.append((t, "add to service"))
    return events


@O
def probes(results, threshold):
    ev, ready, lf, rf = [], True, 0, 0
    for t, (live, rdy) in zip(range(10, 10 * len(results) + 1, 10), results):
        lf, rf = (0 if live else lf + 1), (0 if rdy else rf + 1)
        if lf >= threshold:
            ev.append((t, "restart"))
            lf = rf = 0
            ready = False
        elif ready and rf >= threshold:
            ready = False
            ev.append((t, "remove from service"))
        elif not ready and rdy:
            ready = True
            ev.append((t, "add to service"))
    return ev
