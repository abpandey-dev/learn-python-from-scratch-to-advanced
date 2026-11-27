from lib import *
import ast
import itertools
import math
from collections import Counter, defaultdict
from unittest.mock import Mock

TOPIC(
    id="testing", title="Testing With pytest", glyph="✓",
    blurb="How testing really works and how to do it well: approximate equality, parametrize ids, fixture order and scopes, mocks, injected clocks, line and branch coverage, mutation testing, flaky tests, property-based shrinking, boundary values and partitions, test selection, the pyramid, snapshots, test smells, summaries and durations.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">def test_total_with_discount():                 # tests are plain functions named test_*
    cart = Cart([Item("pen", 10.0, qty=3)])     # arrange
    total = cart.total(discount=0.1)            # act
    assert total == pytest.approx(27.0)         # assert

@pytest.mark.parametrize("age, ok", [(17, False), (18, True)])
def test_is_adult(age, ok): assert is_adult(age) is ok

pytest -q                      # run quietly
pytest -k cart -x              # only tests matching "cart", stop at first failure
pytest --cov=app --cov-report=term-missing</code></pre>
""")


Q(None, "Compare Floats Like pytest.approx", "Easy", "Never use == on floats",
  "<code>pytest.approx</code> treats two numbers as equal if they differ by at most <code>max(rel × |expected|, abs)</code> with rel = 1e-6 and abs = 1e-12. Return a bool for each <code>(got, expected)</code> pair.",
  [(([(0.1 + 0.2, 0.3), (1e-13, 0.0), (100.00005, 100.0), (100.001, 100.0), (1000000.5, 1000000.0), (2.5, 2.6)],), [True, True, True, False, True, False])],
  ("Compute the tolerance by hand.", "O(n)", "O(n)"),
  ("One comprehension. (Note <code>math.isclose</code> is slightly different: its relative tolerance uses the larger of the two numbers, while <code>approx</code> uses the expected value.)", "O(n)", "O(n)"),
  viz=(([(0.1 + 0.2, 0.3)],)))


@B
def approx_equal(pairs):
    out = []
    for got, want in pairs:
        tol = max(1e-6 * abs(want), 1e-12)
        out.append(abs(got - want) <= tol)
    return out


@O
def approx_equal(pairs):
    return [abs(g - w) <= max(1e-6 * abs(w), 1e-12) for g, w in pairs]


Q(None, "Parametrize: Generate Test Ids", "Easy", "One test, many cases",
  "<code>@pytest.mark.parametrize</code> stacked on several arguments runs the cartesian product. Given the test name and an ordered list of <code>(argument, values)</code>, return the test ids pytest shows, e.g. <code>test_price[card-1]</code> (values joined by <code>-</code>, first argument varying slowest).",
  [(("test_price", [("method", ["card", "upi"]), ("qty", [1, 10]), ("member", [True, False])]), ['test_price[card-1-True]', 'test_price[card-1-False]', 'test_price[card-10-True]', 'test_price[card-10-False]', 'test_price[upi-1-True]', 'test_price[upi-1-False]', 'test_price[upi-10-True]', 'test_price[upi-10-False]'])],
  ("Recursive nested loops.", "O(product)", "O(product)"),
  ("<code>itertools.product</code>.", "O(product)", "O(product)"),
  viz=(("t", [("a", [1, 2])])))


@B
def param_ids(name, params):
    combos = [[]]
    for _, values in params:
        new = []
        for c in combos:
            for v in values:
                new.append(c + [str(v)])
        combos = new
    return [f"{name}[{'-'.join(c)}]" for c in combos]


@O
def param_ids(name, params):
    return [f"{name}[{'-'.join(map(str, c))}]" for c in itertools.product(*(v for _, v in params))]


Q(None, "Fixture Setup and Teardown Order", "Medium", "Dependencies first, cleanup in reverse",
  "Fixtures can request other fixtures (<code>deps</code>). For a test requesting <code>wanted</code> fixtures in order, pytest sets each up after its own dependencies (depth-first, in request order, each only once) and tears them down in exact reverse order. Return <code>(setup order, teardown order)</code>.",
  [(({"db": ["config"], "client": ["app", "db"], "app": ["config"], "config": [], "tmp_dir": []}, ["client", "tmp_dir", "db"]), (['config', 'app', 'db', 'client', 'tmp_dir'], ['tmp_dir', 'client', 'db', 'app', 'config']))],
  ("Recursive depth-first setup with a visited list.", "O(f + d)", "O(f)"),
  ("Same, with a set for visited.", "O(f + d)", "O(f)"),
  viz=(({"a": ["b"], "b": []}, ["a"])))


@B
def fixture_order(deps, wanted):
    order = []
    def setup(f):
        if f in order:
            return
        for d in deps[f]:
            setup(d)
        order.append(f)
    for f in wanted:
        setup(f)
    return (order, list(reversed(order)))


@O
def fixture_order(deps, wanted):
    order, seen = [], set()
    def setup(f):
        if f not in seen:
            seen.add(f)
            for d in deps[f]:
                setup(d)
            order.append(f)
    for f in wanted:
        setup(f)
    return (order, order[::-1])


Q(None, "How Often Does Each Fixture Run?", "Medium", "Fixture scopes",
  "Tests are <code>(module, [fixtures used])</code>. A <code>function</code>-scoped fixture is set up for every test that uses it, a <code>module</code>-scoped one once per module that uses it, a <code>session</code>-scoped one once in total. Return set-up counts per fixture, sorted by name. Expensive fixtures (a database) should have wide scopes.",
  [(([("test_api.py", ["client", "db"]), ("test_api.py", ["client"]), ("test_api.py", ["db", "tmp_path"]), ("test_models.py", ["db"]), ("test_models.py", ["tmp_path"])], {"client": "function", "db": "module", "tmp_path": "function", "settings": "session"}), [('client', 2), ('db', 2), ('tmp_path', 2)])],
  ("Track what's alive per scope while looping.", "O(t · f)", "O(f)"),
  ("Count distinct scope keys with sets.", "O(t · f)", "O(t · f)"),
  viz=(([("m", ["a"]), ("m", ["a"])], {"a": "module"})))


@B
def fixture_setups(tests, scopes):
    counts, seen = {}, set()
    for i, (module, fixtures) in enumerate(tests):
        for f in fixtures:
            key = {"function": (f, i), "module": (f, module), "session": (f,)}[scopes[f]]
            if key not in seen:
                seen.add(key)
                counts[f] = counts.get(f, 0) + 1
    return sorted(counts.items())


@O
def fixture_setups(tests, scopes):
    keys = defaultdict(set)
    for i, (module, fixtures) in enumerate(tests):
        for f in fixtures:
            keys[f].add({"function": i, "module": module, "session": 0}[scopes[f]])
    return sorted((f, len(k)) for f, k in keys.items())


def remind_overdue(invoices, today, send_email):
    for inv in invoices:
        if not inv["paid"] and inv["due"] < today:
            send_email(inv["email"], f"Invoice {inv['id']} is overdue")


Q(None, "Mock a Dependency and Check the Calls", "Medium", "Test behaviour without sending real email",
  "<code>remind_overdue(invoices, today, send_email)</code> emails customers with unpaid invoices past due. Call it with a test double for <code>send_email</code> and return <code>(number of calls, list of (to, subject))</code>. The brute force records calls in a hand-written fake; the optimal uses <code>unittest.mock.Mock</code>.",
  [(([{"id": 1, "email": "a@x.com", "due": 10, "paid": False}, {"id": 2, "email": "b@x.com", "due": 30, "paid": False}, {"id": 3, "email": "c@x.com", "due": 5, "paid": True}, {"id": 4, "email": "d@x.com", "due": 19, "paid": False}], 20), (2, [('a@x.com', 'Invoice 1 is overdue'), ('d@x.com', 'Invoice 4 is overdue')]))],
  ("A list-appending fake function.", "O(n)", "O(n)"),
  ("<code>Mock()</code> and <code>call_args_list</code>.", "O(n)", "O(n)"),
  viz=(([{"id": 1, "email": "a@x", "due": 1, "paid": False}], 2)))


@B
def mock_calls(invoices, today):
    calls = []
    def fake_send(to, subject):
        calls.append((to, subject))
    remind_overdue(invoices, today, fake_send)
    return (len(calls), calls)


@O
def mock_calls(invoices, today):
    send = Mock()
    remind_overdue(invoices, today, send)
    return (send.call_count, [c.args for c in send.call_args_list])


Q(None, "Inject the Clock", "Easy", "Make time testable",
  "Code that calls <code>time.time()</code> inside is hard to test. Pass <code>now</code> in instead. Given sessions <code>(id, started_at, ttl)</code> and a list of 'now' values, return the expired session ids at each moment (expired when now ≥ start + ttl).",
  [(([("s1", 0, 30), ("s2", 10, 30), ("s3", 25, 5), ("s4", 40, 60)], [20, 30, 45, 120]), [[], ['s1', 's3'], ['s1', 's2', 's3'], ['s1', 's2', 's3', 's4']])],
  ("Nested loops.", "O(t · s)", "O(s)"),
  ("A comprehension per moment.", "O(t · s)", "O(s)"),
  viz=(([("a", 0, 5)], [4, 5])))


@B
def expired_at(sessions, moments):
    out = []
    for now in moments:
        gone = []
        for sid, start, ttl in sessions:
            if now >= start + ttl:
                gone.append(sid)
        out.append(gone)
    return out


@O
def expired_at(sessions, moments):
    return [[s for s, start, ttl in sessions if now >= start + ttl] for now in moments]


Q(None, "Line Coverage and Missing Lines", "Medium", "pytest --cov --cov-report=term-missing",
  "Given the executable line numbers of a file and the lines each test executed, return <code>(coverage % rounded to 1, missing lines as ranges)</code>, written like <code>'12-14'</code> or <code>'20'</code>. A range runs over consecutive <b>executable</b> lines — blank lines and comments in between don't break it, as in coverage.py.",
  [(([1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 14, 15, 16, 20], [[1, 2, 3, 5, 6], [1, 2, 3, 10, 11, 14], [1, 2, 7, 8]]), (71.4, ['12', '15-20']))],
  ("Union in a loop, then walk the missing lines.", "O(l + e)", "O(l)"),
  ("Set union and grouping consecutive runs.", "O(l log l)", "O(l)"),
  viz=(([1, 2, 3], [[1]])))


@B
def coverage(executable, runs):
    hit = []
    for r in runs:
        for line in r:
            if line not in hit:
                hit.append(line)
    missing = [l for l in executable if l not in hit]
    ranges, i = [], 0
    while i < len(missing):
        j = i
        while j + 1 < len(missing) and executable.index(missing[j + 1]) == executable.index(missing[j]) + 1:
            j += 1
        ranges.append(str(missing[i]) if i == j else f"{missing[i]}-{missing[j]}")
        i = j + 1
    covered = len(executable) - len(missing)
    return (round(covered / len(executable) * 100, 1), ranges)


@O
def coverage(executable, runs):
    hit = set().union(*runs)
    pos = {l: i for i, l in enumerate(executable)}
    missing = [l for l in executable if l not in hit]
    ranges = []
    for _, grp in itertools.groupby(missing, key=lambda l: pos[l] - missing.index(l)):
        g = list(grp)
        ranges.append(str(g[0]) if len(g) == 1 else f"{g[0]}-{g[-1]}")
    return (round(100 * (1 - len(missing) / len(executable)), 1), ranges)


Q(None, "Branch Coverage", "Easy", "Did both sides of each if run?",
  "Each decision point (an <code>if</code> line) has two outcomes. <code>taken</code> maps a decision line to the outcomes seen in the tests (<code>'T'</code> and/or <code>'F'</code>). Return <code>(branch coverage % rounded to 1, decisions with a missing outcome as (line, missing))</code>. 100% line coverage can still miss branches.",
  [(({12: ["T", "F"], 18: ["T"], 25: ["F"], 31: ["T", "F"], 40: []},), (60.0, [(18, ['F']), (25, ['T']), (40, ['T', 'F'])]))],
  ("Count outcomes in a loop.", "O(d)", "O(d)"),
  ("Set differences.", "O(d)", "O(d)"),
  viz=(({1: ["T"]},)))


@B
def branch_coverage(taken):
    total, hit, gaps = 0, 0, []
    for line, outs in taken.items():
        total += 2
        hit += len(set(outs))
        miss = [o for o in ["T", "F"] if o not in outs]
        if miss:
            gaps.append((line, miss))
    return (round(hit / total * 100, 1), gaps)


@O
def branch_coverage(taken):
    gaps = [(l, sorted({"T", "F"} - set(o), reverse=True)) for l, o in taken.items() if {"T", "F"} - set(o)]
    return (round(100 * sum(len(set(o)) for o in taken.values()) / (2 * len(taken)), 1), gaps)


Q(None, "Mutation Testing: Are Your Tests Any Good?", "Medium", "Tests that catch small bugs",
  "Mutation testing makes small changes (mutants) to the code and checks the tests catch them. The function is <code>original</code>, an expression in <code>age</code>; each mutant is another expression; tests are <code>(age, expected)</code>. A mutant is <b>killed</b> if any test's expected value differs from the mutant's result. Return <code>(killed mutants, survivors, mutation score %)</code> — survivors point at missing tests.",
  [(("age >= 18", ["age > 18", "age <= 18", "age >= 17", "age >= 19", "True"], [(30, True), (5, False)]), (['age <= 18', 'True'], ['age > 18', 'age >= 17', 'age >= 19'], 40.0)),
   (("age >= 18", ["age > 18", "age <= 18", "age >= 17", "age >= 19", "True"], [(30, True), (5, False), (18, True), (17, False)]), (['age > 18', 'age <= 18', 'age >= 17', 'age >= 19', 'True'], [], 100.0))],
  ("Evaluate every mutant on every test with eval.", "O(m · t)", "O(m)"),
  ("Same, with any() and a compiled expression.", "O(m · t)", "O(m)"),
  viz=(("age > 0", ["age >= 0"], [(1, True), (0, False)])))


@B
def mutation_score(original, mutants, tests):
    killed, survived = [], []
    for m in mutants:
        caught = False
        for age, want in tests:
            if eval(m, {"age": age}) != want:
                caught = True
        (killed if caught else survived).append(m)
    return (killed, survived, round(len(killed) / len(mutants) * 100, 1))


@O
def mutation_score(original, mutants, tests):
    code = {m: compile(m, "<mutant>", "eval") for m in mutants}
    killed = [m for m in mutants if any(eval(code[m], {"age": a}) != w for a, w in tests)]
    return (killed, [m for m in mutants if m not in killed], round(100 * len(killed) / len(mutants), 1))


Q(None, "Find the Flaky Tests", "Easy", "Same code, different result",
  "Runs are <code>(commit, test, outcome)</code>. A test is flaky if it both passed and failed on the <b>same</b> commit. Return the flaky tests (sorted) and, for each, the fraction of its runs that failed (rounded to 2).",
  [(([("c1", "test_login", "pass"), ("c1", "test_login", "fail"), ("c1", "test_cart", "pass"), ("c2", "test_cart", "fail"), ("c2", "test_cart", "fail"), ("c2", "test_search", "pass"), ("c2", "test_search", "fail"), ("c3", "test_search", "pass"), ("c3", "test_login", "pass")],), [('test_login', 0.33), ('test_search', 0.33)])],
  ("Nested dicts of outcome sets.", "O(r)", "O(r)"),
  ("<code>defaultdict(set)</code> keyed by (commit, test).", "O(r)", "O(r)"),
  viz=(([("c", "t", "pass"), ("c", "t", "fail")],)))


@B
def flaky_tests(runs):
    outcomes, totals, fails = {}, {}, {}
    for c, t, o in runs:
        outcomes.setdefault((c, t), set()).add(o)
        totals[t] = totals.get(t, 0) + 1
        fails[t] = fails.get(t, 0) + (o == "fail")
    flaky = sorted({t for (c, t), s in outcomes.items() if len(s) == 2})
    return [(t, round(fails[t] / totals[t], 2)) for t in flaky]


@O
def flaky_tests(runs):
    seen, per = defaultdict(set), defaultdict(list)
    for c, t, o in runs:
        seen[c, t].add(o)
        per[t].append(o == "fail")
    return [(t, round(sum(per[t]) / len(per[t]), 2)) for t in sorted({t for (_, t), s in seen.items() if len(s) == 2})]


def fails_property(xs):
    # The bug: a function that breaks when the list has 2+ items adding up to more than 10.
    return len(xs) >= 2 and sum(xs) > 10


Q(None, "Shrink a Failing Example", "Hard", "Property-based testing (Hypothesis)",
  "Hypothesis finds a random input that breaks a property, then <b>shrinks</b> it to the simplest failing input. Starting from <code>example</code> (which fails <code>fails_property</code>), repeat until nothing changes: try deleting each element (first to last); keep a deletion if the result still fails. Then try replacing each element with half its value (integer division), keeping it if it still fails. Return the shrunk list.",
  [(([7, 3, 12, 9, 1, 30, 4],), [15, 0]), (([50, 50],), [6, 6])],
  ("Rebuild lists by hand in nested loops.", "O(n² · v)", "O(n)"),
  ("The same passes, with slicing.", "O(n² · v)", "O(n)"),
  viz=(([6, 6, 1],)))


@B
def shrink(example):
    xs = list(example)
    changed = True
    while changed:
        changed = False
        i = 0
        while i < len(xs):
            trial = xs[:i] + xs[i + 1:]
            if fails_property(trial):
                xs = trial
                changed = True
            else:
                i += 1
        for i in range(len(xs)):
            trial = list(xs)
            trial[i] = xs[i] // 2
            if trial[i] != xs[i] and fails_property(trial):
                xs = trial
                changed = True
    return xs


@O
def shrink(example):
    xs, changed = list(example), True
    while changed:
        changed, i = False, 0
        while i < len(xs):
            if fails_property(xs[:i] + xs[i + 1:]):
                xs, changed = xs[:i] + xs[i + 1:], True
            else:
                i += 1
        for i, v in enumerate(xs):
            t = xs[:i] + [v // 2] + xs[i + 1:]
            if v // 2 != v and fails_property(t):
                xs, changed = t, True
    return xs


Q(None, "Boundary Values", "Easy", "Bugs live at the edges",
  "For each valid range <code>(lo, hi)</code> (inclusive), return the boundary test inputs: lo − 1, lo, lo + 1, hi − 1, hi, hi + 1 (sorted, without duplicates).",
  [(([(18, 65), (1, 1), (0, 2)],), [[17, 18, 19, 64, 65, 66], [0, 1, 2], [-1, 0, 1, 2, 3]])],
  ("Build a list and dedupe by hand.", "O(r)", "O(r)"),
  ("A sorted set per range.", "O(r)", "O(r)"),
  viz=(([(1, 3)],)))


@B
def boundaries(ranges):
    out = []
    for lo, hi in ranges:
        vals = []
        for v in [lo - 1, lo, lo + 1, hi - 1, hi, hi + 1]:
            if v not in vals:
                vals.append(v)
        out.append(sorted(vals))
    return out


@O
def boundaries(ranges):
    return [sorted({lo - 1, lo, lo + 1, hi - 1, hi, hi + 1}) for lo, hi in ranges]


def shipping_band(kg):
    if kg <= 0:
        return "invalid"
    if kg <= 1:
        return "letter"
    if kg <= 5:
        return "parcel"
    if kg <= 30:
        return "heavy"
    return "freight"


Q(None, "Equivalence Partitions", "Easy", "One test per kind of input",
  "Inputs that behave the same belong to one partition; one test per partition is enough (plus boundaries). Using <code>shipping_band</code>, return which bands the given test weights cover and which bands are missing (from <code>invalid, letter, parcel, heavy, freight</code>).",
  [(([0.5, 2, 3, 4.9, 12],), (['letter', 'parcel', 'heavy'], ['invalid', 'freight']))],
  ("Loop and collect into a list.", "O(n)", "O(1)"),
  ("Set operations.", "O(n)", "O(1)"),
  viz=(([1, 50],)))


@B
def partitions(weights):
    bands = ["invalid", "letter", "parcel", "heavy", "freight"]
    covered = []
    for w in weights:
        b = shipping_band(w)
        if b not in covered:
            covered.append(b)
    return ([b for b in bands if b in covered], [b for b in bands if b not in covered])


@O
def partitions(weights):
    bands = ["invalid", "letter", "parcel", "heavy", "freight"]
    got = set(map(shipping_band, weights))
    return ([b for b in bands if b in got], [b for b in bands if b not in got])


Q(None, "Run Only the Affected Tests", "Medium", "Fast feedback in big repos",
  "<code>imports</code> maps each module (and test file) to the modules it imports. Given the changed modules, return the test files (names starting with <code>test_</code>) that import a changed module directly or indirectly, sorted.",
  [(({"test_api.py": ["api", "auth"], "test_models.py": ["models"], "test_utils.py": ["utils"], "api": ["models", "utils"], "auth": ["utils"], "models": ["db"], "db": [], "utils": [], "cli": ["api"]}, ["db"]), ['test_api.py', 'test_models.py']),
   (({"test_api.py": ["api", "auth"], "test_models.py": ["models"], "test_utils.py": ["utils"], "api": ["models", "utils"], "auth": ["utils"], "models": ["db"], "db": [], "utils": [], "cli": ["api"]}, ["auth"]), ['test_api.py'])],
  ("For each test, DFS through its imports.", "O(t · (n + e))", "O(n)"),
  ("Reverse the graph once and BFS from the changes.", "O(n + e)", "O(n + e)"),
  viz=(({"test_a.py": ["a"], "a": []}, ["a"])))


@B
def affected_tests(imports, changed):
    out = []
    for t in imports:
        if not t.startswith("test_"):
            continue
        seen, stack = set(), list(imports[t])
        while stack:
            m = stack.pop()
            if m not in seen:
                seen.add(m)
                stack += imports.get(m, [])
        if seen & set(changed):
            out.append(t)
    return sorted(out)


@O
def affected_tests(imports, changed):
    rev = defaultdict(list)
    for m, deps in imports.items():
        for d in deps:
            rev[d].append(m)
    seen, stack = set(changed), list(changed)
    while stack:
        for up in rev[stack.pop()]:
            if up not in seen:
                seen.add(up)
                stack.append(up)
    return sorted(m for m in seen if m.startswith("test_"))


Q(None, "Check the Test Pyramid", "Easy", "Many fast tests, few slow ones",
  "Given counts and average seconds for <code>unit</code>, <code>integration</code> and <code>e2e</code> tests, return <code>(total minutes rounded to 1, % of tests that are unit rounded to 1, shape)</code> where shape is <code>'pyramid'</code> if unit > integration > e2e, <code>'ice cream cone'</code> if e2e is the largest group, else <code>'diamond'</code>.",
  [(({"unit": (1200, 0.02), "integration": (150, 0.8), "e2e": (20, 12.0)},), (6.4, 87.6, 'pyramid')), (({"unit": (40, 0.05), "integration": (60, 1.5), "e2e": (300, 20.0)},), (101.5, 10.0, 'ice cream cone')), (({"unit": (100, 0.02), "integration": (400, 0.5), "e2e": (30, 9.0)},), (7.9, 18.9, 'diamond'))],
  ("Step-by-step arithmetic and if/elif.", "O(1)", "O(1)"),
  ("Same, compact.", "O(1)", "O(1)"),
  viz=(({"unit": (10, 0.1), "integration": (5, 1.0), "e2e": (1, 5.0)},)))


@B
def pyramid(suite):
    u, i, e = suite["unit"][0], suite["integration"][0], suite["e2e"][0]
    seconds = 0
    for n, t in suite.values():
        seconds += n * t
    if u > i > e:
        shape = "pyramid"
    elif e >= u and e >= i:
        shape = "ice cream cone"
    else:
        shape = "diamond"
    return (round(seconds / 60, 1), round(u / (u + i + e) * 100, 1), shape)


@O
def pyramid(suite):
    u, i, e = (suite[k][0] for k in ("unit", "integration", "e2e"))
    shape = "pyramid" if u > i > e else "ice cream cone" if e >= max(u, i) else "diamond"
    return (round(sum(n * t for n, t in suite.values()) / 60, 1), round(100 * u / (u + i + e), 1), shape)


Q(None, "Snapshot Testing", "Medium", "Catch unexpected output changes",
  "Compare the current output with the stored snapshot (nested dicts) and return sorted differences as <code>(path, kind)</code> where path is dot-separated and kind is <code>'added'</code>, <code>'removed'</code> or <code>'changed'</code>.",
  [(({"user": {"id": 7, "name": "Asha", "roles": ["admin"]}, "plan": "pro", "limits": {"api": 1000}}, {"user": {"id": 7, "name": "Asha K", "roles": ["admin"], "email": "a@x.com"}, "plan": "pro", "limits": {}}), [('limits.api', 'removed'), ('user.email', 'added'), ('user.name', 'changed')])],
  ("Recursive comparison building a list.", "O(n)", "O(d)"),
  ("Recursion over the union of keys.", "O(n)", "O(d)"),
  viz=(({"a": 1}, {"a": 2})))


@B
def snapshot_diff(old, new):
    out = []
    def walk(a, b, prefix):
        for k in a:
            p = prefix + k
            if k not in b:
                out.append((p, "removed"))
            elif isinstance(a[k], dict) and isinstance(b[k], dict):
                walk(a[k], b[k], p + ".")
            elif a[k] != b[k]:
                out.append((p, "changed"))
        for k in b:
            if k not in a:
                out.append((prefix + k, "added"))
    walk(old, new, "")
    return sorted(out)


@O
def snapshot_diff(old, new):
    def walk(a, b, pre):
        for k in a.keys() | b.keys():
            p = pre + k
            if k not in b:
                yield (p, "removed")
            elif k not in a:
                yield (p, "added")
            elif isinstance(a[k], dict) and isinstance(b[k], dict):
                yield from walk(a[k], b[k], p + ".")
            elif a[k] != b[k]:
                yield (p, "changed")
    return sorted(walk(old, new, ""))


Q(None, "Spot Test Smells", "Medium", "Read tests with the ast module",
  "Parse each test's source with <code>ast</code> and report, per test function, the smells: <code>'no assert'</code> (no <code>assert</code> statement and no <code>pytest.raises</code>), <code>'sleeps'</code> (calls <code>time.sleep</code> or <code>sleep</code>), <code>'prints'</code> (calls <code>print</code>). Return <code>(test name, sorted smells)</code> only for tests with smells.",
  [((["def test_total():\n    assert total([1, 2]) == 3\n", "def test_slow_job():\n    start_job()\n    time.sleep(5)\n    print(status())\n", "def test_raises():\n    with pytest.raises(ValueError):\n        parse('x')\n", "def test_nothing():\n    result = compute()\n"],), [('test_slow_job', ['no assert', 'prints', 'sleeps']), ('test_nothing', ['no assert'])])],
  ("Walk the tree checking node types one by one.", "O(n)", "O(n)"),
  ("Collect called names once with a comprehension.", "O(n)", "O(n)"),
  viz=((["def test_a():\n    print(1)\n"],)))


def called_name(node):
    f = node.func
    return f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")


@B
def test_smells(sources):
    out = []
    for src in sources:
        fn = ast.parse(src).body[0]
        has_assert = has_raises = sleeps = prints = False
        for node in ast.walk(fn):
            if isinstance(node, ast.Assert):
                has_assert = True
            if isinstance(node, ast.Call):
                name = called_name(node)
                if name == "raises":
                    has_raises = True
                if name == "sleep":
                    sleeps = True
                if name == "print":
                    prints = True
        smells = []
        if not (has_assert or has_raises):
            smells.append("no assert")
        if prints:
            smells.append("prints")
        if sleeps:
            smells.append("sleeps")
        if smells:
            out.append((fn.name, smells))
    return out


@O
def test_smells(sources):
    out = []
    for src in sources:
        fn = ast.parse(src).body[0]
        nodes = list(ast.walk(fn))
        calls = {called_name(n) for n in nodes if isinstance(n, ast.Call)}
        checks = {"no assert": not any(isinstance(n, ast.Assert) for n in nodes) and "raises" not in calls,
                  "sleeps": "sleep" in calls, "prints": "print" in calls}
        smells = sorted(k for k, bad in checks.items() if bad)
        if smells:
            out.append((fn.name, smells))
    return out


Q(None, "Write the Summary Line", "Easy", "What pytest prints at the end",
  "Given test outcomes and the total seconds, return pytest's summary line, e.g. <code>'1 failed, 12 passed, 2 skipped in 3.42s'</code>: counts in the order failed, passed, skipped, xfailed, xpassed, error (pluralised to <code>errors</code> when more than one), omitting zeros, seconds to 2 decimals.",
  [((["passed"] * 12 + ["failed", "skipped", "skipped"], 3.4219), '1 failed, 12 passed, 2 skipped in 3.42s'), ((["passed", "error", "error", "xfailed"], 0.5), '1 passed, 1 xfailed, 2 errors in 0.50s')],
  ("Count each outcome with a loop.", "O(n)", "O(1)"),
  ("<code>Counter</code> and a join.", "O(n)", "O(1)"),
  viz=((["passed"], 0.01)))


@B
def summary_line(outcomes, seconds):
    order = ["failed", "passed", "skipped", "xfailed", "xpassed", "error"]
    parts = []
    for o in order:
        n = 0
        for x in outcomes:
            if x == o:
                n += 1
        if n:
            word = "errors" if o == "error" and n > 1 else o
            parts.append(f"{n} {word}")
    return ", ".join(parts) + f" in {seconds:.2f}s"


@O
def summary_line(outcomes, seconds):
    c = Counter(outcomes)
    word = lambda o: "errors" if o == "error" and c[o] > 1 else o
    return ", ".join(f"{c[o]} {word(o)}" for o in ["failed", "passed", "skipped", "xfailed", "xpassed", "error"] if c[o]) + f" in {seconds:.2f}s"


Q(None, "Should You Retry Flaky Tests?", "Medium", "Odds of a red build",
  "Each of <code>n</code> flaky tests fails at random with probability <code>p</code> per run. Return <code>(chance the build fails with no retries, chance it fails when each test may be retried up to r times)</code>, as % rounded to 2. Retries hide flakiness — fix the root cause, but they buy time.",
  [((20, 0.02, 2), (33.24, 0.02)), ((200, 0.01, 1), (86.6, 1.98))],
  ("Loop multiplying pass chances.", "O(n)", "O(1)"),
  ("Closed form with powers.", "O(1)", "O(1)"),
  viz=((5, 0.1, 1)))


@B
def flaky_odds(n, p, r):
    pass_once, pass_retry = 1.0, 1.0
    for _ in range(n):
        pass_once *= 1 - p
        pass_retry *= 1 - p ** (r + 1)
    return (round((1 - pass_once) * 100, 2), round((1 - pass_retry) * 100, 2))


@O
def flaky_odds(n, p, r):
    return (round(100 * (1 - (1 - p) ** n), 2), round(100 * (1 - (1 - p ** (r + 1)) ** n), 2))


Q(None, "Find the Slowest Tests", "Easy", "pytest --durations=3",
  "Given <code>(test, seconds)</code>, return the <code>k</code> slowest tests (ties by name) and the share of total time they take (% rounded to 1).",
  [(([("test_login", 0.12), ("test_export_pdf", 8.4), ("test_search", 0.9), ("test_db_migration", 14.2), ("test_cart", 0.05), ("test_email", 3.1)], 3), ([('test_db_migration', 14.2), ('test_export_pdf', 8.4), ('test_email', 3.1)], 96.0))],
  ("Sort everything.", "O(n log n)", "O(n)"),
  ("<code>heapq.nlargest</code>.", "O(n log k)", "O(k)"),
  viz=(([("a", 1.0), ("b", 2.0)], 1)))


@B
def slowest(durations, k):
    top = sorted(durations, key=lambda d: (-d[1], d[0]))[:k]
    total = 0
    for _, s in durations:
        total += s
    share = 0
    for _, s in top:
        share += s
    return (top, round(share / total * 100, 1))


@O
def slowest(durations, k):
    import heapq
    top = heapq.nsmallest(k, durations, key=lambda d: (-d[1], d[0]))
    return (top, round(100 * sum(s for _, s in top) / sum(s for _, s in durations), 1))
