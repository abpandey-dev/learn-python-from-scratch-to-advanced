from lib import *
import ast
import builtins
import re
from collections import Counter, defaultdict

TOPIC(
    id="code-quality", title="Code Quality, Linting & Type Hints", glyph="✎",
    blurb="Build the checks that linters and type checkers run, with Python's ast module: unused imports, complexity, long lines, naming, mutable defaults, swallowed errors, docstring and type-hint coverage, runtime type checks, import sorting, duplicates, dead code, magic numbers, long functions, whitespace, shadowed builtins, old-style formatting, line counts, layer rules and rule selection.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">pip install ruff mypy
ruff check .            # lint (pyflakes, pycodestyle, isort, bugbear rules and more)
ruff check --fix .      # auto-fix what's safe
ruff format .           # format like Black
mypy app/               # static type checking

def total(prices: list[float], discount: float = 0.0) -> float: ...</code></pre>
<p>Linters read your code as a syntax tree (<code>ast.parse</code>) without running it — the questions here do the same.</p>
""")


def names_used(tree):
    used = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Name):
            used.add(n.id)
        elif isinstance(n, ast.Attribute):
            base = n
            while isinstance(base, ast.Attribute):
                base = base.value
            if isinstance(base, ast.Name):
                used.add(base.id)
    return used


Q(None, "Find Unused Imports", "Medium", "Ruff F401",
  "Parse the source and return the imported names (the name bound in the module, e.g. <code>np</code> for <code>import numpy as np</code>, <code>os</code> for <code>import os.path</code>) that are never used, sorted.",
  [(("import os\nimport sys\nimport numpy as np\nfrom pathlib import Path, PurePath\nfrom typing import List\nimport os.path\n\ndef main(args: List[str]) -> None:\n    p = Path(args[0])\n    print(os.getcwd(), p)\n",), ['PurePath', 'np', 'sys'])],
  ("Collect imports, then scan every node for each name.", "O(i · n)", "O(i)"),
  ("Collect used names once with the helper.", "O(n)", "O(n)"),
  viz=(("import os\nimport re\nprint(os.sep)\n",)))


@B
def unused_imports(src):
    tree = ast.parse(src)
    imported = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                imported.append(a.asname or a.name.split(".")[0])
        elif isinstance(n, ast.ImportFrom):
            for a in n.names:
                imported.append(a.asname or a.name)
    unused = []
    for name in imported:
        found = False
        for n in ast.walk(tree):
            if isinstance(n, ast.Name) and n.id == name:
                found = True
        if not found and name not in unused:
            unused.append(name)
    return sorted(unused)


@O
def unused_imports(src):
    tree = ast.parse(src)
    bound = {a.asname or (a.name.split(".")[0] if isinstance(n, ast.Import) else a.name)
             for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom)) for a in n.names}
    return sorted(bound - names_used(tree))


Q(None, "Cyclomatic Complexity", "Medium", "How many paths through a function?",
  "Complexity = 1 + the number of decision points: each <code>if</code>/<code>elif</code>, <code>for</code>, <code>while</code>, <code>except</code> handler, conditional expression, comprehension <code>if</code>, and each extra operand of <code>and</code>/<code>or</code>. Return <code>{function name: complexity}</code>. Above ~10, a function is hard to test.",
  [(("def ship(order):\n    if not order.items:\n        return None\n    for item in order.items:\n        if item.weight > 30 and not item.freight_ok:\n            raise ValueError('too heavy')\n    try:\n        rate = lookup(order.zone)\n    except KeyError:\n        rate = 0\n    return rate if rate else default_rate()\n\ndef tiny(x):\n    return [y for y in x if y > 0]\n",), {'ship': 7, 'tiny': 2})],
  ("Walk the function and count each node type with if-statements.", "O(n)", "O(1)"),
  ("A tuple of decision node types and a sum.", "O(n)", "O(1)"),
  viz=(("def f(x):\n    if x:\n        return 1\n    return 0\n",)))


@B
def complexity(src):
    out = {}
    for fn in ast.parse(src).body:
        if not isinstance(fn, ast.FunctionDef):
            continue
        c = 1
        for n in ast.walk(fn):
            if isinstance(n, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.IfExp)):
                c += 1
            elif isinstance(n, ast.BoolOp):
                c += len(n.values) - 1
            elif isinstance(n, ast.comprehension):
                c += len(n.ifs)
        out[fn.name] = c
    return out


@O
def complexity(src):
    DECISIONS = (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.IfExp)
    def score(n):
        if isinstance(n, DECISIONS):
            return 1
        if isinstance(n, ast.BoolOp):
            return len(n.values) - 1
        return len(n.ifs) if isinstance(n, ast.comprehension) else 0
    return {f.name: 1 + sum(map(score, ast.walk(f))) for f in ast.parse(src).body if isinstance(f, ast.FunctionDef)}


Q(None, "Lines Too Long", "Easy", "E501",
  "Return <code>(line number, length)</code> for every line longer than <code>limit</code> characters (Black's default is 88).",
  [(("def f():\n    return 1\n" + "x = '" + "a" * 90 + "'\n" + "# " + "b" * 86 + "\n" + "y = 2\n", 88), [(3, 96)])],
  ("A loop with enumerate.", "O(n)", "O(n)"),
  ("A comprehension.", "O(n)", "O(n)"),
  viz=(("ab\nabcdef\n", 4)))


@B
def long_lines(src, limit):
    out = []
    n = 0
    for line in src.split("\n"):
        n += 1
        if len(line) > limit:
            out.append((n, len(line)))
    return out


@O
def long_lines(src, limit):
    return [(i, len(l)) for i, l in enumerate(src.splitlines(), 1) if len(l) > limit]


SNAKE = re.compile(r"^_{0,2}[a-z][a-z0-9_]*$")
CAPWORDS = re.compile(r"^_?[A-Z][a-zA-Z0-9]*$")
UPPER = re.compile(r"^_?[A-Z][A-Z0-9_]*$")


Q(None, "Check Naming Conventions", "Easy", "PEP 8 names",
  "Report <code>(line, name, rule)</code> for: functions not in <code>snake_case</code> (rule <code>'function'</code>), classes not in <code>CapWords</code> (<code>'class'</code>), and module-level assignments to names that are neither UPPER_CASE constants nor snake_case (<code>'variable'</code>). Use the regexes <code>SNAKE</code>, <code>CAPWORDS</code>, <code>UPPER</code>.",
  [(("MAX_RETRIES = 3\nmaxSize = 10\n\nclass user_account:\n    pass\n\nclass HttpClient:\n    def SendRequest(self):\n        pass\n\ndef parse_config():\n    pass\n\ndef LoadData():\n    pass\n",), [(2, 'maxSize', 'variable'), (4, 'user_account', 'class'), (8, 'SendRequest', 'function'), (14, 'LoadData', 'function')])],
  ("Walk the tree; check each kind with if/elif.", "O(n)", "O(v)"),
  ("A rule table of (node type, regex, rule).", "O(n)", "O(v)"),
  viz=(("def BadName():\n    pass\n",)))


@B
def naming(src):
    tree = ast.parse(src)
    out = []
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef) and not SNAKE.match(n.name):
            out.append((n.lineno, n.name, "function"))
        elif isinstance(n, ast.ClassDef) and not CAPWORDS.match(n.name):
            out.append((n.lineno, n.name, "class"))
    for n in tree.body:
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name) and not (UPPER.match(t.id) or SNAKE.match(t.id)):
                    out.append((n.lineno, t.id, "variable"))
    return sorted(out)


@O
def naming(src):
    tree = ast.parse(src)
    out = [(n.lineno, n.name, "function") for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and not SNAKE.match(n.name)]
    out += [(n.lineno, n.name, "class") for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and not CAPWORDS.match(n.name)]
    out += [(n.lineno, t.id, "variable") for n in tree.body if isinstance(n, ast.Assign) for t in n.targets
            if isinstance(t, ast.Name) and not (UPPER.match(t.id) or SNAKE.match(t.id))]
    return sorted(out)


Q(None, "Mutable Default Arguments", "Easy", "Bugbear B006",
  "A default like <code>items=[]</code> is created <b>once</b> and shared between calls — a classic bug. Return the names of functions with a default that is a list, dict or set literal, or a call to <code>list()</code>, <code>dict()</code> or <code>set()</code>.",
  [(("def add(item, items=[]):\n    items.append(item)\n    return items\n\ndef ok(item, items=None):\n    items = items or []\n\ndef cfg(options={}, *, tags=set()):\n    pass\n\ndef counter(start=0, seen=dict()):\n    pass\n",), ['add', 'cfg', 'counter'])],
  ("Check each default with if-statements.", "O(n)", "O(f)"),
  ("A helper predicate and any().", "O(n)", "O(f)"),
  viz=(("def f(x=[]):\n    pass\n",)))


@B
def mutable_defaults(src):
    out = []
    for fn in ast.walk(ast.parse(src)):
        if not isinstance(fn, ast.FunctionDef):
            continue
        defaults = fn.args.defaults + [d for d in fn.args.kw_defaults if d is not None]
        bad = False
        for d in defaults:
            if isinstance(d, (ast.List, ast.Dict, ast.Set)):
                bad = True
            if isinstance(d, ast.Call) and isinstance(d.func, ast.Name) and d.func.id in ("list", "dict", "set"):
                bad = True
        if bad:
            out.append(fn.name)
    return out


@O
def mutable_defaults(src):
    def mutable(d):
        return isinstance(d, (ast.List, ast.Dict, ast.Set)) or (
            isinstance(d, ast.Call) and getattr(d.func, "id", "") in {"list", "dict", "set"})
    return [f.name for f in ast.walk(ast.parse(src)) if isinstance(f, ast.FunctionDef)
            and any(mutable(d) for d in f.args.defaults + f.args.kw_defaults if d is not None)]


Q(None, "Swallowed Exceptions", "Medium", "Errors that vanish",
  "Return <code>(line, issue)</code> for each <code>except</code> handler: <code>'bare except'</code> if it has no exception type, <code>'swallowed'</code> if its body is only <code>pass</code> (or <code>...</code>), or both (sorted) as separate entries. Silent failures are the hardest bugs to find in production.",
  [(("try:\n    load()\nexcept:\n    pass\n\ntry:\n    parse()\nexcept ValueError:\n    log.warning('bad input')\n\ntry:\n    send()\nexcept Exception:\n    pass\n\ntry:\n    go()\nexcept:\n    retry()\n",), [(3, 'bare except'), (3, 'swallowed'), (13, 'swallowed'), (18, 'bare except')])],
  ("Walk handlers with if-statements.", "O(n)", "O(h)"),
  ("A comprehension over handlers and checks.", "O(n)", "O(h)"),
  viz=(("try:\n    x()\nexcept:\n    pass\n",)))


@B
def swallowed(src):
    out = []
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.ExceptHandler):
            if n.type is None:
                out.append((n.lineno, "bare except"))
            only_pass = True
            for s in n.body:
                if not (isinstance(s, ast.Pass) or (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and s.value.value is Ellipsis)):
                    only_pass = False
            if only_pass:
                out.append((n.lineno, "swallowed"))
    return sorted(out)


@O
def swallowed(src):
    def empty(s):
        return isinstance(s, ast.Pass) or (isinstance(s, ast.Expr) and getattr(s.value, "value", None) is Ellipsis)
    hs = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.ExceptHandler)]
    return sorted([(h.lineno, "bare except") for h in hs if h.type is None] + [(h.lineno, "swallowed") for h in hs if all(map(empty, h.body))])


Q(None, "Docstring Coverage", "Easy", "interrogate",
  "Count public functions, methods and classes (names not starting with <code>_</code>) and return <code>(coverage % rounded to 1, names missing a docstring in source order)</code>.",
  [(('class Cart:\n    """A shopping cart."""\n\n    def add(self, item):\n        """Add an item."""\n\n    def total(self):\n        return 0\n\n    def _recalc(self):\n        pass\n\ndef checkout(cart):\n    pass\n\ndef refund(order):\n    """Refund an order."""\n',), (60.0, ['total', 'checkout']))],
  ("Walk and check with if-statements.", "O(n)", "O(d)"),
  ("Filter public definitions, then use ast.get_docstring.", "O(n)", "O(d)"),
  viz=(('def f():\n    """Doc."""\n',)))


@B
def docstring_coverage(src):
    total, missing = 0, []
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and not n.name.startswith("_"):
            total += 1
            first = n.body[0]
            has = isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str)
            if not has:
                missing.append((n.lineno, n.name))
    missing.sort()
    return (round((total - len(missing)) / total * 100, 1), [m for _, m in missing])


@O
def docstring_coverage(src):
    defs = sorted((n.lineno, n.name, ast.get_docstring(n)) for n in ast.walk(ast.parse(src))
                  if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and not n.name.startswith("_"))
    missing = [name for _, name, doc in defs if doc is None]
    return (round(100 * (1 - len(missing) / len(defs)), 1), missing)


Q(None, "Type Hint Coverage", "Easy", "How much of the code is typed?",
  "For every function, count its parameters (excluding <code>self</code> and <code>cls</code>) plus its return value as slots; a slot is covered if it has an annotation. Return <code>(coverage % rounded to 1, {function: covered/total as 'c/t'})</code>.",
  [(("def total(prices: list[float], discount: float = 0.0) -> float:\n    pass\n\ndef parse(text, strict=False):\n    pass\n\nclass Repo:\n    def get(self, id: int):\n        pass\n\n    @classmethod\n    def build(cls, url: str) -> 'Repo':\n        pass\n",), (60.0, {'total': '3/3', 'parse': '0/3', 'get': '1/2', 'build': '2/2'}))],
  ("Count with loops.", "O(n)", "O(f)"),
  ("Comprehensions over all argument kinds.", "O(n)", "O(f)"),
  viz=(("def f(x: int):\n    pass\n",)))


@B
def hint_coverage(src):
    per, cov, tot = {}, 0, 0
    for fn in ast.walk(ast.parse(src)):
        if not isinstance(fn, ast.FunctionDef):
            continue
        args = fn.args.posonlyargs + fn.args.args + fn.args.kwonlyargs
        c = t = 0
        for a in args:
            if a.arg in ("self", "cls"):
                continue
            t += 1
            if a.annotation is not None:
                c += 1
        t += 1
        if fn.returns is not None:
            c += 1
        per[fn.name] = f"{c}/{t}"
        cov += c
        tot += t
    return (round(cov / tot * 100, 1), per)


@O
def hint_coverage(src):
    per, cov, tot = {}, 0, 0
    for fn in (n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef)):
        slots = [a.annotation for a in fn.args.posonlyargs + fn.args.args + fn.args.kwonlyargs if a.arg not in ("self", "cls")] + [fn.returns]
        c = sum(s is not None for s in slots)
        per[fn.name], cov, tot = f"{c}/{len(slots)}", cov + c, tot + len(slots)
    return (round(100 * cov / tot, 1), per)


def type_ok(value, hint):
    if hint.endswith(" | None"):
        return value is None or type_ok(value, hint[:-7])
    if hint.startswith("list[") and hint.endswith("]"):
        return isinstance(value, list) and all(type_ok(v, hint[5:-1]) for v in value)
    if hint == "float":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if hint == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    return type(value).__name__ == hint


Q(None, "Check Call Arguments Against Hints", "Medium", "What mypy and pydantic catch",
  "Given parameter hints (strings like <code>'int'</code>, <code>'float'</code>, <code>'str'</code>, <code>'bool'</code>, <code>'list[int]'</code>, <code>'str | None'</code>) and a list of calls (dicts of argument values), return for each call the sorted parameter names whose value doesn't match. An int is acceptable for float; a bool is not an int. Use <code>type_ok</code>.",
  [(({"user_id": "int", "amount": "float", "note": "str | None", "tags": "list[str]", "urgent": "bool"},
     [{"user_id": 7, "amount": 10, "note": None, "tags": ["a"], "urgent": False},
      {"user_id": "7", "amount": 9.5, "note": "hi", "tags": [], "urgent": 1},
      {"user_id": True, "amount": "3", "note": 5, "tags": ["a", 2], "urgent": True}]), [[], ['urgent', 'user_id'], ['amount', 'note', 'tags', 'user_id']])],
  ("Loop over calls and parameters.", "O(c · p)", "O(p)"),
  ("A comprehension per call.", "O(c · p)", "O(p)"),
  viz=(({"x": "int"}, [{"x": "1"}])))


@B
def bad_args(hints, calls):
    out = []
    for call in calls:
        wrong = []
        for name, hint in hints.items():
            if not type_ok(call[name], hint):
                wrong.append(name)
        out.append(sorted(wrong))
    return out


@O
def bad_args(hints, calls):
    return [sorted(n for n, h in hints.items() if not type_ok(c[n], h)) for c in calls]


STDLIB = {"os", "sys", "json", "re", "math", "pathlib", "typing", "datetime", "collections", "logging", "itertools", "functools"}


Q(None, "Sort Imports Like isort", "Medium", "Three groups, alphabetical",
  "Order import lines into three groups — standard library (top module in <code>STDLIB</code>), third-party, then local (top module equals <code>local</code>) — separated by one blank line (<code>''</code>). Within a group, plain <code>import x</code> lines come before <code>from x import y</code>, each sorted case-insensitively by module.",
  [((["from app.models import User", "import requests", "import os", "from pathlib import Path", "import numpy as np", "from typing import Any", "import app.config", "import json", "from fastapi import FastAPI"], "app"), ['import json', 'import os', 'from pathlib import Path', 'from typing import Any', '', 'import numpy as np', 'import requests', 'from fastapi import FastAPI', '', 'import app.config', 'from app.models import User'])],
  ("Bucket lines with loops, then sort each bucket.", "O(n log n)", "O(n)"),
  ("A sort key of (group, style, module).", "O(n log n)", "O(n)"),
  viz=((["import sys", "import requests"], "app")))


@B
def sort_imports(lines, local):
    groups = [[], [], []]
    for line in lines:
        module = line.split()[1]
        top = module.split(".")[0]
        g = 0 if top in STDLIB else 2 if top == local else 1
        groups[g].append(line)
    out = []
    for g in groups:
        if not g:
            continue
        plain = sorted([l for l in g if l.startswith("import ")], key=lambda l: l.split()[1].lower())
        froms = sorted([l for l in g if l.startswith("from ")], key=lambda l: l.split()[1].lower())
        if out:
            out.append("")
        out += plain + froms
    return out


@O
def sort_imports(lines, local):
    def key(line):
        mod = line.split()[1]
        top = mod.split(".")[0]
        return (0 if top in STDLIB else 2 if top == local else 1, line.startswith("from"), mod.lower())
    out, prev = [], None
    for line in sorted(lines, key=key):
        if prev is not None and key(line)[0] != prev:
            out.append("")
        out.append(line)
        prev = key(line)[0]
    return out


Q(None, "Find Duplicated Code", "Medium", "Copy-paste detection",
  "Normalise each line (strip spaces; skip blank lines) and find every block of <code>k</code> consecutive normalised lines that appears in more than one place. Return sorted <code>(file, start line)</code> pairs of the duplicated blocks' locations (line numbers are the original 1-based numbers).",
  [(({"a.py": "def f(x):\n    y = x * 2\n    z = y + 1\n    return z\n", "b.py": "def g(x):\n\n    y = x * 2\n    z = y + 1\n    return z\n"}, 3), [('a.py', 2), ('b.py', 3)])],
  ("Compare every block with every other block.", "O(b²)", "O(b)"),
  ("Index blocks in a dict keyed by their text.", "O(b)", "O(b)"),
  viz=(({"a": "x\ny\n", "b": "x\ny\n"}, 2)))


def blocks(files, k):
    out = []
    for name, src in files.items():
        lines = [(i, l.strip()) for i, l in enumerate(src.splitlines(), 1) if l.strip()]
        for j in range(len(lines) - k + 1):
            out.append((name, lines[j][0], tuple(t for _, t in lines[j:j + k])))
    return out


@B
def duplicates(files, k):
    bl = blocks(files, k)
    found = set()
    for i in range(len(bl)):
        for j in range(len(bl)):
            if i != j and bl[i][2] == bl[j][2]:
                found.add((bl[i][0], bl[i][1]))
    return sorted(found)


@O
def duplicates(files, k):
    where = defaultdict(list)
    for name, line, text in blocks(files, k):
        where[text].append((name, line))
    return sorted(loc for locs in where.values() if len(locs) > 1 for loc in locs)


Q(None, "Unreachable Code", "Easy", "Statements after return",
  "Return the line numbers of statements that come after a <code>return</code>, <code>raise</code>, <code>break</code> or <code>continue</code> in the same block (only the first unreachable statement of each block).",
  [(("def f(x):\n    if x < 0:\n        raise ValueError('neg')\n        print('never')\n    for i in range(x):\n        if i == 3:\n            break\n            i += 1\n    return x\n    x = 0\n",), [4, 8, 10])],
  ("Walk every node with a body and scan it.", "O(n)", "O(1)"),
  ("Same, also covering else blocks via a field list.", "O(n)", "O(1)"),
  viz=(("def f():\n    return 1\n    x = 2\n",)))


@B
def unreachable(src):
    out = []
    for n in ast.walk(ast.parse(src)):
        for field in ("body", "orelse", "finalbody"):
            block = getattr(n, field, None)
            if not isinstance(block, list):
                continue
            for i, s in enumerate(block[:-1]):
                if isinstance(s, (ast.Return, ast.Raise, ast.Break, ast.Continue)):
                    out.append(block[i + 1].lineno)
                    break
    return sorted(out)


@O
def unreachable(src):
    STOP = (ast.Return, ast.Raise, ast.Break, ast.Continue)
    out = []
    for n in ast.walk(ast.parse(src)):
        for block in (getattr(n, f, None) for f in ("body", "orelse", "finalbody")):
            if isinstance(block, list):
                i = next((i for i, s in enumerate(block[:-1]) if isinstance(s, STOP)), None)
                if i is not None:
                    out.append(block[i + 1].lineno)
    return sorted(out)


Q(None, "Magic Numbers", "Easy", "Name your constants",
  "Inside function bodies, report <code>(line, value)</code> for numeric literals other than 0, 1, -1 and 2 — they should be named constants. (Negative numbers appear as a minus applied to a positive literal; report the positive literal.)",
  [(("TAX = 0.18\n\ndef price(base, qty):\n    if qty > 100:\n        base *= 0.85\n    total = base * qty * (1 + TAX)\n    return round(total, 2)\n\ndef retry():\n    for attempt in range(5):\n        sleep(2 ** attempt * 0.25)\n",), [(4, 100), (5, 0.85), (10, 5), (11, 0.25)])],
  ("Walk functions and test each constant.", "O(n)", "O(m)"),
  ("A comprehension over function bodies.", "O(n)", "O(m)"),
  viz=(("def f():\n    return 42\n",)))


@B
def magic_numbers(src):
    out = []
    for fn in ast.walk(ast.parse(src)):
        if isinstance(fn, ast.FunctionDef):
            for n in ast.walk(fn):
                if isinstance(n, ast.Constant) and type(n.value) in (int, float) and n.value not in (0, 1, -1, 2):
                    out.append((n.lineno, n.value))
    return sorted(out)


@O
def magic_numbers(src):
    funcs = [f for f in ast.walk(ast.parse(src)) if isinstance(f, ast.FunctionDef)]
    return sorted((n.lineno, n.value) for f in funcs for n in ast.walk(f)
                  if isinstance(n, ast.Constant) and type(n.value) in (int, float) and n.value not in (0, 1, -1, 2))


Q(None, "Functions That Do Too Much", "Easy", "Size limits",
  "Return <code>(function, reasons)</code> for functions with more than <code>max_lines</code> lines (from the <code>def</code> line to its last line) or more than <code>max_args</code> parameters (all kinds, excluding <code>self</code>). Reasons are <code>'too long'</code> and/or <code>'too many args'</code>.",
  [(("def a(x, y):\n    return x + y\n\ndef build(name, size, color, owner, tags, notes):\n    pass\n\ndef big(x):\n" + "    x += 1\n" * 30 + "    return x\n", 25, 5), [('build', ['too many args']), ('big', ['too long'])])],
  ("Compute both measures with loops.", "O(n)", "O(f)"),
  ("Use end_lineno and list lengths.", "O(n)", "O(f)"),
  viz=(("def f(a, b, c):\n    pass\n", 10, 2)))


@B
def too_big(src, max_lines, max_args):
    out = []
    for fn in ast.walk(ast.parse(src)):
        if not isinstance(fn, ast.FunctionDef):
            continue
        reasons = []
        if fn.end_lineno - fn.lineno + 1 > max_lines:
            reasons.append("too long")
        n = 0
        for a in fn.args.posonlyargs + fn.args.args + fn.args.kwonlyargs:
            if a.arg != "self":
                n += 1
        if fn.args.vararg:
            n += 1
        if fn.args.kwarg:
            n += 1
        if n > max_args:
            reasons.append("too many args")
        if reasons:
            out.append((fn.name, reasons))
    return out


@O
def too_big(src, max_lines, max_args):
    out = []
    for fn in (f for f in ast.walk(ast.parse(src)) if isinstance(f, ast.FunctionDef)):
        a = fn.args
        n = sum(x.arg != "self" for x in a.posonlyargs + a.args + a.kwonlyargs) + bool(a.vararg) + bool(a.kwarg)
        r = ["too long"] * (fn.end_lineno - fn.lineno + 1 > max_lines) + ["too many args"] * (n > max_args)
        if r:
            out.append((fn.name, r))
    return out


Q(None, "Whitespace Problems", "Easy", "W291, W292, W391",
  "Report <code>(line, code)</code>: <code>'W291'</code> trailing whitespace on a line, <code>'W391'</code> blank line(s) at the end of the file (report the first trailing blank line), <code>'W292'</code> no newline at the end of the file (report the last line).",
  [(("x = 1  \ny = 2\n\n\n",), [(1, 'W291'), (3, 'W391')]), (("def f():\n\treturn 1 ",), [(2, 'W291'), (2, 'W292')])],
  ("Walk lines with flags.", "O(n)", "O(n)"),
  ("Comprehension plus two end-of-file checks.", "O(n)", "O(n)"),
  viz=(("a \n",)))


@B
def whitespace(src):
    lines = src.split("\n")
    has_final_newline = src.endswith("\n")
    if has_final_newline:
        lines = lines[:-1]
    out = []
    for i, l in enumerate(lines, 1):
        if l != l.rstrip():
            out.append((i, "W291"))
    if not has_final_newline:
        out.append((len(lines), "W292"))
    j = len(lines)
    while j > 0 and lines[j - 1].strip() == "":
        j -= 1
    if j < len(lines):
        out.append((j + 1, "W391"))
    return sorted(out)


@O
def whitespace(src):
    lines = src.splitlines()
    out = [(i, "W291") for i, l in enumerate(lines, 1) if l and l != l.rstrip()]
    if not src.endswith("\n"):
        out.append((len(lines), "W292"))
    tail = len(lines) - len(src.rstrip().splitlines()) if src.strip() else 0
    if tail:
        out.append((len(lines) - tail + 1, "W391"))
    return sorted(out)


Q(None, "Shadowed Builtins", "Easy", "Don't name a variable list",
  "Return sorted <code>(line, name)</code> for assignments, function parameters and function names that reuse a Python builtin name (<code>list</code>, <code>id</code>, <code>type</code>, <code>sum</code>, …). Shadowing breaks the builtin for the rest of the scope.",
  [(("def max(values):\n    return sorted(values)[-1]\n\ndef load(id, type='json'):\n    list = []\n    sum = 0\n    total = 0\n    return list\n",), [(1, 'max'), (4, 'id'), (4, 'type'), (5, 'list'), (6, 'sum')])],
  ("Check each node kind against the builtins with if-statements.", "O(n)", "O(v)"),
  ("One generator of (line, name) for all binding nodes.", "O(n)", "O(v)"),
  viz=(("dict = {}\n",)))


@B
def shadowed(src):
    names = set(dir(builtins))
    out = []
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.FunctionDef) and n.name in names:
            out.append((n.lineno, n.name))
        if isinstance(n, ast.arg) and n.arg in names:
            out.append((n.lineno, n.arg))
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store) and n.id in names:
            out.append((n.lineno, n.id))
    return sorted(out)


@O
def shadowed(src):
    def bound(n):
        if isinstance(n, ast.FunctionDef):
            yield n.lineno, n.name
        elif isinstance(n, ast.arg):
            yield n.lineno, n.arg
        elif isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
            yield n.lineno, n.id
    b = set(dir(builtins))
    return sorted(x for n in ast.walk(ast.parse(src)) for x in bound(n) if x[1] in b)


Q(None, "Old-Style String Formatting", "Easy", "Use f-strings",
  "Report <code>(line, style)</code> for <code>'%'</code> formatting (a string literal on the left of <code>%</code>) and <code>'format'</code> (calling <code>.format</code> on a string literal). Tools like ruff and pyupgrade rewrite these as f-strings.",
  [(("name = 'Asha'\nmsg = 'Hello %s, you have %d items' % (name, 3)\nline = '{} -> {}'.format(a, b)\nok = f'{name} logged in'\nn = 10 % 3\n",), [(2, '%'), (3, 'format')])],
  ("Walk the tree and check node shapes.", "O(n)", "O(m)"),
  ("Two comprehensions.", "O(n)", "O(m)"),
  viz=(("x = '%s' % y\n",)))


@B
def old_format(src):
    out = []
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Mod) and isinstance(n.left, ast.Constant) and isinstance(n.left.value, str):
            out.append((n.lineno, "%"))
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "format" \
                and isinstance(n.func.value, ast.Constant) and isinstance(n.func.value.value, str):
            out.append((n.lineno, "format"))
    return sorted(out)


@O
def old_format(src):
    nodes = list(ast.walk(ast.parse(src)))
    is_str = lambda x: isinstance(x, ast.Constant) and isinstance(x.value, str)
    return sorted([(n.lineno, "%") for n in nodes if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Mod) and is_str(n.left)]
                  + [(n.lineno, "format") for n in nodes if isinstance(n, ast.Call) and getattr(n.func, "attr", "") == "format" and is_str(getattr(n.func, "value", None))])


Q(None, "Count Lines of Code", "Easy", "cloc",
  "Return <code>{'code': …, 'comment': …, 'blank': …}</code>: blank lines are empty after stripping; comment lines start with <code>#</code> after stripping; everything else is code.",
  [(("# app entry point\nimport os\n\ndef main():\n    # read config\n    path = os.getenv('CFG')  # inline comments count as code\n\n    return path\n",), {'code': 4, 'comment': 2, 'blank': 2})],
  ("Counters in a loop.", "O(n)", "O(1)"),
  ("<code>Counter</code> over a classifier.", "O(n)", "O(1)"),
  viz=(("x = 1\n\n# c\n",)))


@B
def cloc(src):
    code = comment = blank = 0
    for line in src.splitlines():
        s = line.strip()
        if not s:
            blank += 1
        elif s.startswith("#"):
            comment += 1
        else:
            code += 1
    return {"code": code, "comment": comment, "blank": blank}


@O
def cloc(src):
    c = Counter("blank" if not l.strip() else "comment" if l.strip()[0] == "#" else "code" for l in src.splitlines())
    return {k: c[k] for k in ("code", "comment", "blank")}


Q(None, "Enforce Architecture Layers", "Medium", "import-linter",
  "Layers are listed from top to bottom (e.g. <code>api → services → repositories → models</code>). A module may import from lower layers but never from a higher one. <code>imports</code> maps modules (named <code>layer.something</code>) to the modules they import. Return sorted violations <code>(importer, imported)</code>.",
  [((["api", "services", "repositories", "models"], {"api.orders": ["services.orders", "models.order"], "services.orders": ["repositories.orders", "api.schemas"], "repositories.orders": ["models.order", "services.pricing"], "models.order": [], "services.pricing": ["models.order"]}), [('repositories.orders', 'services.pricing'), ('services.orders', 'api.schemas')])],
  ("Look up both layers' positions with list.index each time.", "O(e · l)", "O(1)"),
  ("A dict from layer to rank.", "O(e)", "O(l)"),
  viz=((["a", "b"], {"b.x": ["a.y"]})))


@B
def layer_violations(layers, imports):
    out = []
    for mod, deps in imports.items():
        for d in deps:
            if layers.index(d.split(".")[0]) < layers.index(mod.split(".")[0]):
                out.append((mod, d))
    return sorted(out)


@O
def layer_violations(layers, imports):
    rank = {l: i for i, l in enumerate(layers)}
    top = lambda m: rank[m.split(".")[0]]
    return sorted((m, d) for m, deps in imports.items() for d in deps if top(d) < top(m))


Q(None, "Which Lint Rules Are On?", "Medium", "select and ignore",
  "Ruff enables rules by code prefix: <code>select</code> turns prefixes on, <code>ignore</code> turns them off, and the <b>longest</b> matching prefix decides (if a select and an ignore prefix are equally long, ignore wins). Return the enabled rule codes from <code>rules</code>, in order.",
  [((["E", "F", "I", "B006", "UP"], ["E501", "F4", "UP0"], ["E501", "E711", "F401", "F841", "I001", "B006", "B008", "UP006", "UP101", "W291"]), ['E711', 'F841', 'I001', 'B006', 'UP101'])],
  ("Find the longest matching prefix in each list by looping.", "O(r · p)", "O(1)"),
  ("max() over the matching prefixes with a key.", "O(r · p)", "O(1)"),
  viz=((["E"], ["E5"], ["E501", "E711"])))


@B
def enabled_rules(select, ignore, rules):
    out = []
    for r in rules:
        best_sel = 0
        for p in select:
            if r.startswith(p) and len(p) > best_sel:
                best_sel = len(p)
        best_ign = 0
        for p in ignore:
            if r.startswith(p) and len(p) > best_ign:
                best_ign = len(p)
        if best_sel > best_ign:
            out.append(r)
    return out


@O
def enabled_rules(select, ignore, rules):
    longest = lambda prefixes, r: max((len(p) for p in prefixes if r.startswith(p)), default=0)
    return [r for r in rules if longest(select, r) > longest(ignore, r)]
