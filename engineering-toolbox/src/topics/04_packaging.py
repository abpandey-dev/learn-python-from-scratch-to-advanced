from lib import *
import itertools
import re
import tomllib
from collections import defaultdict, deque

TOPIC(
    id="packaging", title="Packages, Versions & Environments", glyph="📦",
    blurb="What pip, uv and poetry do for you: comparing versions, matching specifiers, picking and resolving versions, reading pyproject.toml, parsing requirements and markers, wheel tags, lockfile diffs, vulnerability checks, dependency trees, conflicts, configuration precedence, .env files, PATH lookup, pinning policy, safe upgrades, install size and semantic-version API checks.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">uv venv &amp;&amp; source .venv/bin/activate     # isolated environment per project
uv add fastapi "pydantic>=2,<3"           # add deps to pyproject.toml and the lockfile
uv lock --upgrade-package requests        # upgrade one package in the lockfile
uv sync                                   # install exactly what the lockfile says
uv tree                                   # see the dependency tree
pip install -r requirements.txt           # the classic way
pip-audit                                 # check for known vulnerabilities</code></pre>
<p>Specifiers: <code>==1.4.2</code> exact · <code>&gt;=1.4,&lt;2</code> range · <code>~=1.4.2</code> means ≥1.4.2 and ==1.4.* · <code>!=1.5.0</code> exclude.</p>
""")

PRE = {"a": 0, "b": 1, "rc": 2}


def vkey(v):
    m = re.fullmatch(r"(\d+(?:\.\d+)*)(?:(a|b|rc)(\d+))?", v)
    release = [int(x) for x in m.group(1).split(".")]
    release += [0] * (4 - len(release))
    pre = (PRE[m.group(2)], int(m.group(3))) if m.group(2) else (3, 0)
    return (tuple(release), pre)


def is_pre(v):
    return vkey(v)[1][0] < 3


def satisfies(v, spec):
    for part in [p.strip() for p in spec.split(",") if p.strip()]:
        op, target = re.fullmatch(r"(~=|==|!=|>=|<=|>|<)\s*(\S+)", part).groups()
        if target.endswith(".*"):
            prefix = target[:-2].split(".")
            same = [str(x) for x in vkey(v)[0][:len(prefix)]] == prefix
            if (op == "==") != same:
                return False
            continue
        a, b = vkey(v), vkey(target)
        if op == "~=":
            head = target.split(".")[:-1]
            if not (a >= b and [str(x) for x in a[0][:len(head)]] == head):
                return False
        elif not {"==": a == b, "!=": a != b, ">=": a >= b, "<=": a <= b, ">": a > b, "<": a < b}[op]:
            return False
    return True


Q(None, "Sort Versions Correctly", "Easy", "1.10 comes after 1.9",
  "Sort version strings from oldest to newest. Compare release numbers as integers (missing parts count as 0), and a pre-release (<code>a</code> alpha < <code>b</code> beta < <code>rc</code>) comes before the final release. String sorting gets this wrong.",
  [((["1.10.0", "1.9.3", "2.0.0", "2.0.0rc1", "1.9", "2.0.0a2", "2.0.0b1", "1.9.10", "0.12"],), ['0.12', '1.9', '1.9.3', '1.9.10', '1.10.0', '2.0.0a2', '2.0.0b1', '2.0.0rc1', '2.0.0'])],
  ("Insertion sort with a hand-written compare.", "O(n²)", "O(n)"),
  ("<code>sorted</code> with the <code>vkey</code> tuple.", "O(n log n)", "O(n)"),
  viz=((["1.10", "1.9"],)))


@B
def sort_versions(versions):
    out = []
    for v in versions:
        i = 0
        while i < len(out) and vkey(out[i]) <= vkey(v):
            i += 1
        out.insert(i, v)
    return out


@O
def sort_versions(versions):
    return sorted(versions, key=vkey)


Q(None, "Does the Version Match?", "Medium", "Version specifiers",
  "For each specifier (comma means AND), return which of the versions satisfy it, using <code>satisfies</code>-style rules: <code>==1.4.*</code> matches any 1.4 release; <code>~=1.4.2</code> means ≥1.4.2 and 1.4.*; <code>~=1.4</code> means ≥1.4 and 1.*.",
  [((["1.3.9", "1.4.0", "1.4.2", "1.4.7", "1.5.0", "2.0.0"], [">=1.4,<2", "~=1.4.2", "~=1.4", "==1.4.*", "!=1.5.0,>1.4.0"]), {'>=1.4,<2': ['1.4.0', '1.4.2', '1.4.7', '1.5.0'], '~=1.4.2': ['1.4.2', '1.4.7'], '~=1.4': ['1.4.0', '1.4.2', '1.4.7', '1.5.0'], '==1.4.*': ['1.4.0', '1.4.2', '1.4.7'], '!=1.5.0,>1.4.0': ['1.4.2', '1.4.7', '2.0.0']})],
  ("Loop specs and versions calling the helper.", "O(s · v)", "O(v)"),
  ("A comprehension.", "O(s · v)", "O(v)"),
  viz=((["1.0", "2.0"], [">=1.5"])))


@B
def matching(versions, specs):
    out = {}
    for s in specs:
        ok = []
        for v in versions:
            if satisfies(v, s):
                ok.append(v)
        out[s] = ok
    return out


@O
def matching(versions, specs):
    return {s: [v for v in versions if satisfies(v, s)] for s in specs}


Q(None, "Pick the Newest Allowed Version", "Easy", "What pip install chooses",
  "Return the newest version that satisfies the specifier for each <code>(package, spec)</code>, skipping pre-releases unless <code>allow_pre</code> is True. Return None if nothing matches.",
  [(({"requests": ["2.30.0", "2.31.0", "2.32.3", "3.0.0b1"], "numpy": ["1.26.4", "2.0.0", "2.1.3", "2.2.0rc1"], "django": ["4.2.16", "5.0.9", "5.1.3"]}, [("requests", ">=2.31,<4"), ("numpy", "<2"), ("django", ">=6")], False), {'requests': '2.32.3', 'numpy': '1.26.4', 'django': None}),
   (({"requests": ["2.30.0", "2.31.0", "2.32.3", "3.0.0b1"], "numpy": ["1.26.4", "2.0.0", "2.1.3", "2.2.0rc1"], "django": ["4.2.16", "5.0.9", "5.1.3"]}, [("requests", ">=2.31,<4"), ("numpy", ">=2")], True), {'requests': '3.0.0b1', 'numpy': '2.2.0rc1'})],
  ("Filter, then find the max by comparing keys in a loop.", "O(r · v)", "O(v)"),
  ("<code>max</code> with a key and a default.", "O(r · v)", "O(1)"),
  viz=(({"x": ["1.0", "2.0"]}, [("x", "<2")], False)))


@B
def newest_allowed(available, wanted, allow_pre):
    out = {}
    for pkg, spec in wanted:
        best = None
        for v in available[pkg]:
            if is_pre(v) and not allow_pre:
                continue
            if satisfies(v, spec) and (best is None or vkey(v) > vkey(best)):
                best = v
        out[pkg] = best
    return out


@O
def newest_allowed(available, wanted, allow_pre):
    return {p: max((v for v in available[p] if satisfies(v, s) and (allow_pre or not is_pre(v))), key=vkey, default=None)
            for p, s in wanted}


def consistent(choice, index, root):
    for p, spec in root.items():
        if p in choice and not satisfies(choice[p], spec):
            return False
    for p, v in choice.items():
        for dep, spec in index[p][v].items():
            if dep in choice and not satisfies(choice[dep], spec):
                return False
    return True


Q(None, "Resolve Dependencies", "Hard", "Backtracking like pip and uv",
  "<code>index[pkg][version]</code> lists that version's requirements <code>{dep: spec}</code>; every package in the index is part of the install. Choose one version per package so that the root requirements and all requirements between chosen versions hold, preferring newer versions for packages earlier in alphabetical order. Return the choice (sorted dict) or <code>'conflict'</code>.",
  [(({"app-lib": {"2.0.0": {"httpx": ">=0.27", "pydantic": ">=2"}, "1.5.0": {"httpx": ">=0.24", "pydantic": ">=1.10,<2"}},
      "httpx": {"0.28.0": {"anyio": ">=4"}, "0.27.0": {"anyio": ">=3"}, "0.24.0": {"anyio": ">=3,<4"}},
      "anyio": {"4.4.0": {}, "3.7.1": {}},
      "pydantic": {"2.9.0": {}, "1.10.18": {}}}, {"pydantic": "<2"}), {'anyio': '4.4.0', 'app-lib': '1.5.0', 'httpx': '0.28.0', 'pydantic': '1.10.18'}),
   (({"a": {"2.0": {"b": ">=2"}}, "b": {"1.0": {}}}, {}), 'conflict')],
  ("Try every combination, newest first, and keep the first that works.", "O(product of versions)", "O(p)"),
  ("Backtracking: choose package by package, undo when a constraint breaks.", "O(product) worst case, far less in practice", "O(p)"),
  viz=(({"a": {"2.0": {"b": "<2"}, "1.0": {}}, "b": {"2.0": {}, "1.0": {}}}, {})))


@B
def resolve(index, root):
    pkgs = sorted(index)
    options = [sorted(index[p], key=vkey, reverse=True) for p in pkgs]
    for combo in itertools.product(*options):
        choice = dict(zip(pkgs, combo))
        if consistent(choice, index, root):
            return choice
    return "conflict"


@O
def resolve(index, root):
    pkgs = sorted(index)
    def go(i, choice):
        if i == len(pkgs):
            return dict(choice)
        for v in sorted(index[pkgs[i]], key=vkey, reverse=True):
            choice[pkgs[i]] = v
            if consistent(choice, index, root):
                found = go(i + 1, choice)
                if found:
                    return found
            del choice[pkgs[i]]
        return None
    return go(0, {}) or "conflict"


Q(None, "Read pyproject.toml", "Easy", "The modern project file",
  "Parse the TOML text with <code>tomllib</code> and return <code>{'name', 'version', 'requires_python', 'dependencies' (count), 'dev' (count of the 'dev' optional group, 0 if absent), 'scripts' (sorted names)}</code>.",
  [(('[project]\nname = "invoice-bot"\nversion = "0.3.1"\nrequires-python = ">=3.11"\ndependencies = [\n  "fastapi>=0.115",\n  "pydantic>=2,<3",\n  "httpx",\n]\n\n[project.optional-dependencies]\ndev = ["pytest", "ruff", "mypy"]\n\n[project.scripts]\ninvoice-bot = "invoice_bot.cli:main"\ninvoice-admin = "invoice_bot.admin:main"\n',), {'name': 'invoice-bot', 'version': '0.3.1', 'requires_python': '>=3.11', 'dependencies': 3, 'dev': 3, 'scripts': ['invoice-admin', 'invoice-bot']})],
  ("Parse, then read keys step by step.", "O(n)", "O(n)"),
  ("Parse, then <code>dict.get</code> chains.", "O(n)", "O(n)"),
  viz=(('[project]\nname = "x"\nversion = "1"\n',)))


@B
def read_pyproject(text):
    data = tomllib.loads(text)
    p = data["project"]
    dev = 0
    if "optional-dependencies" in p and "dev" in p["optional-dependencies"]:
        dev = len(p["optional-dependencies"]["dev"])
    scripts = []
    if "scripts" in p:
        scripts = sorted(p["scripts"])
    return {"name": p["name"], "version": p["version"], "requires_python": p.get("requires-python"),
            "dependencies": len(p.get("dependencies", [])), "dev": dev, "scripts": scripts}


@O
def read_pyproject(text):
    p = tomllib.loads(text)["project"]
    return {"name": p["name"], "version": p["version"], "requires_python": p.get("requires-python"),
            "dependencies": len(p.get("dependencies", [])), "dev": len(p.get("optional-dependencies", {}).get("dev", [])),
            "scripts": sorted(p.get("scripts", {}))}


REQ = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)\s*(?:\[([^\]]*)\])?\s*([^;]*?)\s*(?:;\s*(.*))?$")


Q(None, "Parse a Requirement Line", "Medium", "name[extras] spec ; marker",
  "Split each requirement into <code>{'name' (lower-case, with _ and . turned into -), 'extras' (sorted list), 'spec' (spaces removed), 'marker' (or None)}</code>, e.g. <code>Requests[socks] >= 2.31, <3 ; python_version >= '3.9'</code>.",
  [((["Requests[socks] >= 2.31, <3 ; python_version >= '3.9'", "numpy", "Pydantic_Settings>=2.4", "uvicorn[standard,watch]==0.30.6", "typing.extensions; python_version < '3.11'"],), [{'name': 'requests', 'extras': ['socks'], 'spec': '>=2.31,<3', 'marker': "python_version >= '3.9'"}, {'name': 'numpy', 'extras': [], 'spec': '', 'marker': None}, {'name': 'pydantic-settings', 'extras': [], 'spec': '>=2.4', 'marker': None}, {'name': 'uvicorn', 'extras': ['standard', 'watch'], 'spec': '==0.30.6', 'marker': None}, {'name': 'typing-extensions', 'extras': [], 'spec': '', 'marker': "python_version < '3.11'"}])],
  ("Partition the string by hand.", "O(n · L)", "O(L)"),
  ("One regular expression (<code>REQ</code>).", "O(n · L)", "O(L)"),
  viz=((["httpx>=0.27"],)))


@B
def parse_requirements(lines):
    out = []
    for line in lines:
        body, _, marker = line.partition(";")
        body = body.strip()
        extras = []
        if "[" in body:
            name, rest = body.split("[", 1)
            ex, spec = rest.split("]", 1)
            extras = sorted(e.strip() for e in ex.split(",") if e.strip())
        else:
            i = 0
            while i < len(body) and (body[i].isalnum() or body[i] in "._-"):
                i += 1
            name, spec = body[:i], body[i:]
        name = name.strip().lower().replace("_", "-").replace(".", "-")
        out.append({"name": name, "extras": extras, "spec": spec.replace(" ", ""), "marker": marker.strip() or None})
    return out


@O
def parse_requirements(lines):
    out = []
    for line in lines:
        name, extras, spec, marker = REQ.match(line).groups()
        out.append({"name": re.sub(r"[_.]", "-", name.lower()), "extras": sorted(e.strip() for e in (extras or "").split(",") if e.strip()),
                    "spec": spec.replace(" ", ""), "marker": marker.strip() if marker else None})
    return out


def marker_true(marker, env):
    def atom(text):
        m = re.fullmatch(r"\s*(\w+)\s*(==|!=|>=|<=|>|<)\s*'([^']*)'\s*", text)
        var, op, val = m.groups()
        left = env[var]
        if var.endswith("version"):
            a, b = vkey(left), vkey(val)
        else:
            a, b = left, val
        return {"==": a == b, "!=": a != b, ">=": a >= b, "<=": a <= b, ">": a > b, "<": a < b}[op]
    return any(all(atom(t) for t in part.split(" and ")) for part in marker.split(" or "))


Q(None, "Evaluate Environment Markers", "Medium", "Install this only on Linux, Python < 3.11",
  "Markers decide whether a requirement applies here. Support comparisons of a variable with a quoted value, joined by <code>and</code>/<code>or</code> (and binds tighter). Version variables (names ending in <code>version</code>) compare as versions. Return a bool per marker for the environment <code>env</code>.",
  [((["python_version >= '3.10'", "python_version < '3.11' and sys_platform == 'linux'", "sys_platform == 'win32' or platform_machine == 'arm64'", "python_version >= '3.9' and python_version < '3.10' or sys_platform == 'darwin'"], {"python_version": "3.12", "sys_platform": "darwin", "platform_machine": "arm64"}), [True, False, True, True])],
  ("Split on or/and and evaluate each comparison by hand.", "O(m · t)", "O(t)"),
  ("The same with the <code>marker_true</code> helper.", "O(m · t)", "O(t)"),
  viz=((["python_version >= '3.10'"], {"python_version": "3.12"})))


@B
def markers(marker_list, env):
    out = []
    for m in marker_list:
        result = False
        for part in m.split(" or "):
            ok = True
            for t in part.split(" and "):
                if not marker_true(t, env):
                    ok = False
            if ok:
                result = True
        out.append(result)
    return out


@O
def markers(marker_list, env):
    return [marker_true(m, env) for m in marker_list]


Q(None, "Read a Wheel Filename", "Medium", "Will this wheel install here?",
  "Wheel names are <code>name-version(-build)?-python-abi-platform.whl</code>, and each tag part may hold several tags joined by <code>.</code>. For each file, return <code>(name, version, compatible)</code> where compatible means some combination of its python, abi and platform tags is in <code>supported</code> (a list of <code>'py-abi-platform'</code> strings).",
  [((["numpy-2.1.3-cp312-cp312-macosx_14_0_arm64.whl", "requests-2.32.3-py3-none-any.whl", "pydantic_core-2.23.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", "six-1.16.0-py2.py3-none-any.whl"], ["cp312-cp312-macosx_14_0_arm64", "cp312-none-any", "py3-none-any"]), [('numpy', '2.1.3', True), ('requests', '2.32.3', True), ('pydantic_core', '2.23.4', False), ('six', '1.16.0', True)])],
  ("Split and check every tag combination with nested loops.", "O(f · t³)", "O(1)"),
  ("<code>itertools.product</code> of the tag sets.", "O(f · t³)", "O(s)"),
  viz=((["x-1.0-py3-none-any.whl"], ["py3-none-any"])))


@B
def wheel_info(files, supported):
    out = []
    for f in files:
        parts = f[:-4].split("-")
        name, version = parts[0], parts[1]
        py, abi, plat = parts[-3], parts[-2], parts[-1]
        ok = False
        for a in py.split("."):
            for b in abi.split("."):
                for c in plat.split("."):
                    if f"{a}-{b}-{c}" in supported:
                        ok = True
        out.append((name, version, ok))
    return out


@O
def wheel_info(files, supported):
    sup = set(supported)
    out = []
    for f in files:
        p = f.removesuffix(".whl").split("-")
        tags = itertools.product(*(x.split(".") for x in p[-3:]))
        out.append((p[0], p[1], any("-".join(t) in sup for t in tags)))
    return out


Q(None, "What Changed in the Lockfile?", "Easy", "Review dependency updates",
  "Compare two lockfiles (package → version) and return <code>{'added', 'removed', 'upgraded', 'downgraded'}</code>, each a sorted list (changes written as <code>'pkg old -> new'</code>).",
  [(({"fastapi": "0.110.0", "starlette": "0.36.3", "pydantic": "2.6.4", "anyio": "4.3.0", "sniffio": "1.3.1"}, {"fastapi": "0.115.4", "starlette": "0.41.2", "pydantic": "2.6.4", "anyio": "4.2.0", "typing-extensions": "4.12.2"}), {'added': ['typing-extensions'], 'removed': ['sniffio'], 'upgraded': ['fastapi 0.110.0 -> 0.115.4', 'starlette 0.36.3 -> 0.41.2'], 'downgraded': ['anyio 4.3.0 -> 4.2.0']})],
  ("Loop over the union of names.", "O(n)", "O(n)"),
  ("Set operations and comprehensions.", "O(n)", "O(n)"),
  viz=(({"a": "1.0"}, {"a": "2.0"})))


@B
def lock_diff(old, new):
    out = {"added": [], "removed": [], "upgraded": [], "downgraded": []}
    for p in sorted(set(old) | set(new)):
        if p not in old:
            out["added"].append(p)
        elif p not in new:
            out["removed"].append(p)
        elif vkey(new[p]) > vkey(old[p]):
            out["upgraded"].append(f"{p} {old[p]} -> {new[p]}")
        elif vkey(new[p]) < vkey(old[p]):
            out["downgraded"].append(f"{p} {old[p]} -> {new[p]}")
    return out


@O
def lock_diff(old, new):
    both = sorted(old.keys() & new.keys())
    fmt = lambda p: f"{p} {old[p]} -> {new[p]}"
    return {"added": sorted(new.keys() - old.keys()), "removed": sorted(old.keys() - new.keys()),
            "upgraded": [fmt(p) for p in both if vkey(new[p]) > vkey(old[p])],
            "downgraded": [fmt(p) for p in both if vkey(new[p]) < vkey(old[p])]}


Q(None, "Find Vulnerable Packages", "Medium", "pip-audit",
  "Advisories are <code>(id, package, affected spec, fixed version)</code>. Return <code>(package, installed version, advisory id, fixed version)</code> for every installed package matching an advisory, sorted.",
  [(({"jinja2": "3.1.3", "requests": "2.32.3", "urllib3": "1.26.18", "cryptography": "41.0.7", "django": "5.1.3"},
     [("GHSA-h75v", "jinja2", "<3.1.4", "3.1.4"), ("GHSA-9wx4", "requests", "<2.32.0", "2.32.0"), ("GHSA-34jh", "urllib3", ">=1.26.0,<1.26.19", "1.26.19"),
      ("GHSA-3ww4", "cryptography", ">=37.0.0,<42.0.4", "42.0.4"), ("GHSA-x2fm", "django", ">=5.0,<5.0.8", "5.0.8")]), [('cryptography', '41.0.7', 'GHSA-3ww4', '42.0.4'), ('jinja2', '3.1.3', 'GHSA-h75v', '3.1.4'), ('urllib3', '1.26.18', 'GHSA-34jh', '1.26.19')])],
  ("Loop advisories and check installed versions.", "O(a)", "O(a)"),
  ("A sorted comprehension.", "O(a log a)", "O(a)"),
  viz=(({"x": "1.0"}, [("A1", "x", "<2", "2.0")])))


@B
def vulnerable(installed, advisories):
    out = []
    for aid, pkg, spec, fixed in advisories:
        if pkg in installed:
            if satisfies(installed[pkg], spec):
                out.append((pkg, installed[pkg], aid, fixed))
    out.sort()
    return out


@O
def vulnerable(installed, advisories):
    return sorted((p, installed[p], a, f) for a, p, s, f in advisories if p in installed and satisfies(installed[p], s))


Q(None, "Measure the Dependency Tree", "Medium", "uv tree",
  "<code>deps</code> maps each package to its direct dependencies. For each top-level package, return <code>(number of distinct transitive dependencies, depth of the deepest chain)</code> (a package with no deps has depth 0).",
  [(({"fastapi": ["starlette", "pydantic"], "starlette": ["anyio"], "anyio": ["idna", "sniffio"], "pydantic": ["pydantic-core", "annotated-types", "typing-extensions"], "pydantic-core": ["typing-extensions"], "annotated-types": [], "typing-extensions": [], "idna": [], "sniffio": [], "requests": ["urllib3", "idna", "certifi", "charset-normalizer"], "urllib3": [], "certifi": [], "charset-normalizer": []}, ["fastapi", "requests"]), {'fastapi': (8, 3), 'requests': (4, 1)})],
  ("Recursive DFS for each question separately.", "O(t · (n + e))", "O(n)"),
  ("Memoised depth and descendant sets.", "O(n + e)", "O(n²)"),
  viz=(({"a": ["b"], "b": []}, ["a"])))


@B
def tree_stats(deps, top):
    out = {}
    for t in top:
        seen, stack = set(), list(deps[t])
        while stack:
            d = stack.pop()
            if d not in seen:
                seen.add(d)
                stack += deps[d]
        def depth(p):
            return 0 if not deps[p] else 1 + max(depth(c) for c in deps[p])
        out[t] = (len(seen), depth(t))
    return out


@O
def tree_stats(deps, top):
    from functools import lru_cache
    @lru_cache(None)
    def below(p):
        s = set(deps[p])
        for c in deps[p]:
            s |= below(c)
        return frozenset(s)
    @lru_cache(None)
    def depth(p):
        return 1 + max(map(depth, deps[p])) if deps[p] else 0
    return {t: (len(below(t)), depth(t)) for t in top}


Q(None, "Why Is This Package Installed?", "Medium", "Reverse dependencies",
  "Return, for each target, the top-level packages that pull it in (directly or indirectly), sorted. Use the same graph shape as the previous question; <code>top</code> are the packages you asked for.",
  [(({"fastapi": ["starlette", "pydantic"], "starlette": ["anyio"], "anyio": ["idna", "sniffio"], "pydantic": ["typing-extensions"], "typing-extensions": [], "idna": [], "sniffio": [], "requests": ["urllib3", "idna", "certifi"], "urllib3": [], "certifi": [], "httpx": ["anyio", "certifi", "idna"]}, ["fastapi", "requests", "httpx"], ["idna", "certifi", "typing-extensions"]), {'idna': ['fastapi', 'httpx', 'requests'], 'certifi': ['httpx', 'requests'], 'typing-extensions': ['fastapi']})],
  ("DFS from each top-level package.", "O(t · (n + e))", "O(n)"),
  ("Reverse the graph and walk up from each target.", "O(q · (n + e))", "O(n + e)"),
  viz=(({"a": ["b"], "b": []}, ["a"], ["b"])))


@B
def why_installed(deps, top, targets):
    reach = {}
    for t in top:
        seen, stack = set(), [t]
        while stack:
            d = stack.pop()
            if d not in seen:
                seen.add(d)
                stack += deps[d]
        reach[t] = seen
    return {x: sorted(t for t in top if x in reach[t] and x != t) for x in targets}


@O
def why_installed(deps, top, targets):
    up = defaultdict(list)
    for p, ds in deps.items():
        for d in ds:
            up[d].append(p)
    out = {}
    for x in targets:
        seen, q = set(), deque([x])
        while q:
            for parent in up[q.popleft()]:
                if parent not in seen:
                    seen.add(parent)
                    q.append(parent)
        out[x] = sorted(seen & set(top))
    return out


Q(None, "Spot Version Conflicts", "Medium", "Two packages want different things",
  "Several packages constrain the same dependency. For each dependency in <code>constraints</code> (dep → list of <code>(who, spec)</code>), return the versions from <code>available[dep]</code> that satisfy <b>all</b> constraints, or the string <code>'conflict: '</code> followed by the requesters sorted and comma-separated if none do.",
  [(({"pydantic": [("fastapi", ">=1.7.4,!=2.0.0"), ("langchain", ">=2,<3"), ("old-sdk", "<2")], "httpx": [("openai", ">=0.23,<1"), ("anthropic", ">=0.25,<1")]}, {"pydantic": ["1.10.18", "2.0.0", "2.9.2"], "httpx": ["0.24.1", "0.27.2", "0.28.0"]}), {'pydantic': 'conflict: fastapi, langchain, old-sdk', 'httpx': ['0.27.2', '0.28.0']})],
  ("Check every version against every constraint.", "O(d · v · c)", "O(v)"),
  ("Combine constraints into one spec and filter.", "O(d · v · c)", "O(v)"),
  viz=(({"x": [("a", "<2"), ("b", ">=2")]}, {"x": ["1.0", "2.0"]})))


@B
def conflicts(constraints, available):
    out = {}
    for dep, reqs in constraints.items():
        ok = []
        for v in available[dep]:
            good = True
            for _, spec in reqs:
                if not satisfies(v, spec):
                    good = False
            if good:
                ok.append(v)
        out[dep] = ok if ok else "conflict: " + ", ".join(sorted(w for w, _ in reqs))
    return out


@O
def conflicts(constraints, available):
    out = {}
    for dep, reqs in constraints.items():
        combined = ",".join(s for _, s in reqs)
        ok = [v for v in available[dep] if satisfies(v, combined)]
        out[dep] = ok or "conflict: " + ", ".join(sorted(w for w, _ in reqs))
    return out


Q(None, "Configuration Precedence", "Medium", "Defaults < file < env < flags",
  "Settings come from four layers, later ones winning: <code>defaults</code>, the config <code>file</code>, environment variables (<code>APP_</code> prefix, lower-cased key: <code>APP_DB_URL</code> → <code>db_url</code>; other variables ignored) and command-line <code>flags</code>. Return <code>{key: [value, source]}</code> sorted by key.",
  [(({"db_url": "sqlite:///dev.db", "log_level": "INFO", "workers": "1", "debug": "false"}, {"log_level": "WARNING", "workers": "4"}, {"APP_DB_URL": "postgres://prod/db", "APP_WORKERS": "8", "HOME": "/home/asha"}, {"debug": "true"}), {'db_url': ['postgres://prod/db', 'env'], 'debug': ['true', 'flag'], 'log_level': ['WARNING', 'file'], 'workers': ['8', 'env']})],
  ("Apply each layer in a loop, remembering the source.", "O(k)", "O(k)"),
  ("Merge (value, source) dicts in order with dict unions.", "O(k)", "O(k)"),
  viz=(({"a": "1"}, {}, {"APP_A": "2"}, {})))


@B
def resolve_config(defaults, file, environ, flags):
    out = {}
    for k, v in defaults.items():
        out[k] = [v, "default"]
    for k, v in file.items():
        out[k] = [v, "file"]
    for k, v in environ.items():
        if k.startswith("APP_"):
            out[k[4:].lower()] = [v, "env"]
    for k, v in flags.items():
        out[k] = [v, "flag"]
    return dict(sorted(out.items()))


@O
def resolve_config(defaults, file, environ, flags):
    env = {k[4:].lower(): v for k, v in environ.items() if k.startswith("APP_")}
    layers = [(defaults, "default"), (file, "file"), (env, "env"), (flags, "flag")]
    merged = {}
    for layer, src in layers:
        merged |= {k: [v, src] for k, v in layer.items()}
    return dict(sorted(merged.items()))


Q(None, "Parse a .env File", "Medium", "Twelve-factor config",
  "Parse <code>.env</code> text into a dict: skip blank lines and <code>#</code> comments; allow an optional <code>export </code> prefix; strip matching single or double quotes from values; drop an unquoted value's trailing <code> # comment</code>; and expand <code>${NAME}</code> using variables defined earlier in the file (unknown → empty).",
  [(("# database\nexport DB_HOST=localhost\nDB_PORT=5432\nDB_USER='app'\nDB_URL=\"postgres://${DB_USER}@${DB_HOST}:${DB_PORT}/shop\"\nDEBUG=true # local only\n\nGREETING=\"hello # not a comment\"\nMISSING=${NOPE}x\n",), {'DB_HOST': 'localhost', 'DB_PORT': '5432', 'DB_USER': 'app', 'DB_URL': 'postgres://app@localhost:5432/shop', 'DEBUG': 'true', 'GREETING': 'hello # not a comment', 'MISSING': 'x'})],
  ("Line by line with string methods.", "O(n · L)", "O(k)"),
  ("A regex per line and re.sub for expansion.", "O(n · L)", "O(k)"),
  viz=(("A=1\nB=${A}2\n",)))


@B
def parse_env(text):
    env = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:]
        key, _, value = line.partition("=")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        elif " #" in value:
            value = value.split(" #")[0].strip()
        while "${" in value:
            start = value.index("${")
            end = value.index("}", start)
            value = value[:start] + env.get(value[start + 2:end], "") + value[end + 1:]
        env[key.strip()] = value
    return env


@O
def parse_env(text):
    env = {}
    for line in text.splitlines():
        m = re.match(r"^\s*(?:export\s+)?([A-Za-z_]\w*)\s*=\s*(.*?)\s*$", line)
        if not m or line.strip().startswith("#"):
            continue
        key, v = m.groups()
        q = re.fullmatch(r"(['\"])(.*)\1", v)
        v = q.group(2) if q else re.sub(r"\s+#.*$", "", v)
        env[key] = re.sub(r"\$\{(\w+)\}", lambda g: env.get(g.group(1), ""), v)
    return env


Q(None, "Which python Runs?", "Easy", "PATH and virtual environments",
  "A shell runs the first matching executable along <code>PATH</code> (directories in order). Activating a virtual environment just puts its <code>bin</code> folder first. For each command, return <code>(path that runs, other matches that are shadowed)</code>, or <code>(None, [])</code> if not found.",
  [((["/home/asha/proj/.venv/bin", "/usr/local/bin", "/usr/bin"], {"/home/asha/proj/.venv/bin": ["python", "pip", "pytest"], "/usr/local/bin": ["python", "uv"], "/usr/bin": ["python", "git", "pip"]}, ["python", "git", "pytest", "pip", "docker"]), {'python': ('/home/asha/proj/.venv/bin/python', ['/usr/local/bin/python', '/usr/bin/python']), 'git': ('/usr/bin/git', []), 'pytest': ('/home/asha/proj/.venv/bin/pytest', []), 'pip': ('/home/asha/proj/.venv/bin/pip', ['/usr/bin/pip']), 'docker': (None, [])})],
  ("Scan directories for each command.", "O(c · d)", "O(d)"),
  ("A comprehension of matching paths.", "O(c · d)", "O(d)"),
  viz=((["/a", "/b"], {"/a": ["x"], "/b": ["x"]}, ["x"])))


@B
def which(path_dirs, contents, commands):
    out = {}
    for c in commands:
        hits = []
        for d in path_dirs:
            if c in contents.get(d, []):
                hits.append(d + "/" + c)
        out[c] = (hits[0], hits[1:]) if hits else (None, [])
    return out


@O
def which(path_dirs, contents, commands):
    out = {}
    for c in commands:
        hits = [f"{d}/{c}" for d in path_dirs if c in contents.get(d, ())]
        out[c] = (hits[0], hits[1:]) if hits else (None, [])
    return out


Q(None, "Pin, Range or Unbounded?", "Easy", "Apps pin, libraries range",
  "Classify each requirement spec: <code>'pinned'</code> (a single <code>==</code> without <code>*</code>), <code>'compatible'</code> (has an upper bound: <code>&lt;</code>, <code>&lt;=</code>, <code>~=</code> or <code>==X.*</code>), <code>'lower bound only'</code> (only <code>&gt;=</code>/<code>&gt;</code>/<code>!=</code>), or <code>'unbounded'</code> (empty). Return a dict.",
  [(({"django": "==5.1.3", "requests": ">=2.31", "pydantic": ">=2,<3", "numpy": "", "httpx": "~=0.27.0", "boto3": "==1.35.*"},), {'django': 'pinned', 'requests': 'lower bound only', 'pydantic': 'compatible', 'numpy': 'unbounded', 'httpx': 'compatible', 'boto3': 'compatible'})],
  ("If/elif on the operators present.", "O(n)", "O(n)"),
  ("A regex for the operators and a lookup.", "O(n)", "O(n)"),
  viz=(({"a": "==1.0"},)))


@B
def pin_kind(specs):
    out = {}
    for name, s in specs.items():
        parts = [p for p in s.split(",") if p]
        if not parts:
            out[name] = "unbounded"
        elif len(parts) == 1 and parts[0].startswith("==") and "*" not in parts[0]:
            out[name] = "pinned"
        elif any(p.startswith(("<", "~=")) or (p.startswith("==") and "*" in p) for p in parts):
            out[name] = "compatible"
        else:
            out[name] = "lower bound only"
    return out


@O
def pin_kind(specs):
    def kind(s):
        if not s:
            return "unbounded"
        if re.fullmatch(r"==[^,*]+", s):
            return "pinned"
        return "compatible" if re.search(r"(^|,)(<|~=|==[^,]*\*)", s) else "lower bound only"
    return {n: kind(s) for n, s in specs.items()}


Q(None, "Safe Automatic Upgrades", "Medium", "Dependabot and Renovate policies",
  "For each installed package, pick the newest available non-pre-release upgrade allowed by the policy: <code>'patch'</code> (same major and minor), <code>'minor'</code> (same major) or <code>'major'</code> (anything newer). Return <code>{package: new version or None}</code>.",
  [(({"django": "5.0.4", "requests": "2.31.0", "numpy": "1.26.2"}, {"django": ["5.0.4", "5.0.9", "5.1.3", "6.0a1"], "requests": ["2.31.0", "2.32.3"], "numpy": ["1.26.2", "1.26.4", "2.1.3"]}, "patch"), {'django': '5.0.9', 'requests': None, 'numpy': '1.26.4'}),
   (({"django": "5.0.4", "requests": "2.31.0", "numpy": "1.26.2"}, {"django": ["5.0.4", "5.0.9", "5.1.3", "6.0a1"], "requests": ["2.31.0", "2.32.3"], "numpy": ["1.26.2", "1.26.4", "2.1.3"]}, "minor"), {'django': '5.1.3', 'requests': '2.32.3', 'numpy': '1.26.4'})],
  ("Check each candidate with if-statements.", "O(p · v)", "O(1)"),
  ("Compare release prefixes and take the max.", "O(p · v)", "O(1)"),
  viz=(({"a": "1.0.0"}, {"a": ["1.0.1", "1.1.0"]}, "patch")))


@B
def safe_upgrade(installed, available, policy):
    out = {}
    for p, cur in installed.items():
        c = vkey(cur)[0]
        best = None
        for v in available[p]:
            if is_pre(v) or vkey(v) <= vkey(cur):
                continue
            n = vkey(v)[0]
            if policy == "patch" and n[:2] != c[:2]:
                continue
            if policy == "minor" and n[0] != c[0]:
                continue
            if best is None or vkey(v) > vkey(best):
                best = v
        out[p] = best
    return out


@O
def safe_upgrade(installed, available, policy):
    keep = {"patch": 2, "minor": 1, "major": 0}[policy]
    def allowed(cur, v):
        return not is_pre(v) and vkey(v) > vkey(cur) and vkey(v)[0][:keep] == vkey(cur)[0][:keep]
    return {p: max((v for v in available[p] if allowed(cur, v)), key=vkey, default=None) for p, cur in installed.items()}


Q(None, "How Big Is the Environment?", "Easy", "Shared dependencies count once",
  "Given installed sizes in MB and the dependency graph, return the total size of installing <code>top</code> (each package counted once), rounded to 1, and the size each top-level package would add on its own (itself plus its transitive deps).",
  [(({"torch": 780.0, "numpy": 38.5, "pandas": 70.2, "scipy": 110.4, "sympy": 72.0, "mpmath": 5.5, "pytz": 2.4, "networkx": 9.6}, {"torch": ["numpy", "sympy", "networkx"], "sympy": ["mpmath"], "pandas": ["numpy", "pytz"], "scipy": ["numpy"], "numpy": [], "mpmath": [], "pytz": [], "networkx": []}, ["torch", "pandas", "scipy"]), (1088.6, {'torch': 905.6, 'pandas': 111.1, 'scipy': 148.9}))],
  ("Walk the graph per package with a stack.", "O(t · (n + e))", "O(n)"),
  ("A reusable closure helper and set unions.", "O(t · (n + e))", "O(n)"),
  viz=(({"a": 1.0, "b": 2.0}, {"a": ["b"], "b": []}, ["a"])))


@B
def env_size(sizes, deps, top):
    alone = {}
    everything = set()
    for t in top:
        seen, stack = set(), [t]
        while stack:
            p = stack.pop()
            if p not in seen:
                seen.add(p)
                stack += deps[p]
        alone[t] = round(sum(sizes[p] for p in seen), 1)
        everything |= seen
    return (round(sum(sizes[p] for p in everything), 1), alone)


@O
def env_size(sizes, deps, top):
    def closure(p, seen):
        if p not in seen:
            seen.add(p)
            for d in deps[p]:
                closure(d, seen)
        return seen
    parts = {t: closure(t, set()) for t in top}
    return (round(sum(sizes[p] for p in set().union(*parts.values())), 1), {t: round(sum(sizes[p] for p in s), 1) for t, s in parts.items()})


Q(None, "Is This Release Breaking?", "Medium", "Semantic versioning for libraries",
  "Compare a library's public API before and after (function → list of parameters; a parameter ending in <code>=</code> is optional). Return the required bump: <code>'major'</code> if a function or required-or-optional parameter was removed, or a new <b>required</b> parameter was added; <code>'minor'</code> if a function or optional parameter was added; otherwise <code>'patch'</code>.",
  [(({"connect": ["url", "timeout="], "fetch": ["key"]}, {"connect": ["url", "timeout=", "retries="], "fetch": ["key"], "close": []}), 'minor'),
   (({"connect": ["url", "timeout="], "fetch": ["key"]}, {"connect": ["url", "timeout="], "fetch": ["key", "region"]}), 'major'),
   (({"connect": ["url", "timeout="], "fetch": ["key"]}, {"connect": ["url"]}), 'major'),
   (({"connect": ["url"]}, {"connect": ["url"]}), 'patch')],
  ("Flags set while looping over functions and parameters.", "O(f · p)", "O(1)"),
  ("Set differences.", "O(f · p)", "O(p)"),
  viz=(({"f": ["a"]}, {"f": ["a", "b="]})))


@B
def required_bump(old, new):
    major = minor = False
    for fn, params in old.items():
        if fn not in new:
            major = True
            continue
        for p in params:
            if p not in new[fn]:
                major = True
        for p in new[fn]:
            if p not in params:
                if p.endswith("="):
                    minor = True
                else:
                    major = True
    for fn in new:
        if fn not in old:
            minor = True
    return "major" if major else "minor" if minor else "patch"


@O
def required_bump(old, new):
    removed = set(old) - set(new) or any(set(old[f]) - set(new[f]) for f in old if f in new)
    added = {p for f in old if f in new for p in set(new[f]) - set(old[f])}
    if removed or any(not p.endswith("=") for p in added):
        return "major"
    return "minor" if added or set(new) - set(old) else "patch"
