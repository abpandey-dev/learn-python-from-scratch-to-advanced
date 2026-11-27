from lib import *

LESSON("Basics", "Your first pytest tests", """
<p>A test is a function whose name starts with <code>test_</code>, in a file named <code>test_*.py</code>. Inside, <b>arrange</b> the inputs, <b>act</b> by calling the code, and <b>assert</b> the result. pytest rewrites <code>assert</code> so failures show both values.</p>
<pre><code class="py"># app/pricing.py
def total(prices, discount=0.0):
    return round(sum(prices) * (1 - discount), 2)

# tests/test_pricing.py
import pytest
from app.pricing import total

def test_total_no_discount():
    assert total([10.0, 5.5]) == 15.5

def test_total_with_discount():
    assert total([10.0, 10.0], discount=0.1) == pytest.approx(18.0)

@pytest.mark.parametrize("prices, expected", [([], 0), ([1], 1), ([0.1, 0.2], 0.3)])
def test_total_cases(prices, expected):
    assert total(prices) == pytest.approx(expected)

def test_negative_discount_rejected():
    with pytest.raises(ValueError):
        total([1], discount=-0.5)</code></pre>
<pre><code class="py">pip install pytest
pytest -q                 # run everything
pytest tests/test_pricing.py::test_total_cases -v</code></pre>
""", practice=["Compare Floats Like pytest.approx", "Parametrize: Generate Test Ids", "Write the Summary Line", "Boundary Values", "Equivalence Partitions"])

LESSON("Core", "Fixtures, mocks and testable code", """
<p><b>Fixtures</b> provide what tests need (a temporary folder, a database, an app client) and clean up afterwards; <code>yield</code> splits setup from teardown. Pick the scope by cost: <code>function</code> (fresh each test), <code>module</code>, or <code>session</code>.</p>
<pre><code class="py">@pytest.fixture(scope="module")
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    yield conn            # tests run here
    conn.close()          # teardown

def test_insert(db, tmp_path):            # tmp_path is a built-in fixture
    db.execute("INSERT INTO users VALUES (1, 'Asha')")
    assert db.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 1</code></pre>
<p>Replace slow or external things (email, payments, HTTP, the clock) with <b>test doubles</b>. The easiest code to test takes its dependencies as arguments (<b>dependency injection</b>) instead of creating them inside.</p>
<pre><code class="py">from unittest.mock import Mock
def test_reminders_sent():
    send = Mock()
    remind_overdue(invoices, today=20, send_email=send)
    send.assert_called_once_with("a@x.com", "Invoice 1 is overdue")

def test_api(monkeypatch):                 # or patch where it's used
    monkeypatch.setattr("app.client.requests.get", lambda url, timeout: FakeResponse(200))</code></pre>
""", practice=["Fixture Setup and Teardown Order", "How Often Does Each Fixture Run?", "Mock a Dependency and Check the Calls", "Inject the Clock"])

LESSON("Core", "How good are your tests?", """
<ul>
<li><b>Line coverage</b> shows code never run by any test. <b>Branch coverage</b> also checks both sides of each <code>if</code>. Use coverage to find gaps — 100% doesn't mean correct.</li>
<li><b>Mutation testing</b> (mutmut) changes your code in small ways; a surviving mutant is a bug your tests wouldn't catch.</li>
<li><b>Property-based testing</b> (Hypothesis) generates many inputs and shrinks a failure to the smallest example.</li>
<li><b>Snapshot tests</b> catch unexpected changes in large outputs — review snapshot updates carefully.</li>
</ul>
<pre><code class="py">pip install pytest-cov hypothesis
pytest --cov=app --cov-branch --cov-report=term-missing

from hypothesis import given, strategies as st
@given(st.lists(st.integers()))
def test_sort_is_idempotent(xs):
    assert sorted(sorted(xs)) == sorted(xs)</code></pre>
""", practice=["Line Coverage and Missing Lines", "Branch Coverage", "Mutation Testing: Are Your Tests Any Good?", "Shrink a Failing Example", "Snapshot Testing"])

LESSON("Advanced", "Keeping a test suite fast and trustworthy", """
<ul>
<li>Follow the <b>test pyramid</b>: many fast unit tests, fewer integration tests, a handful of end-to-end tests.</li>
<li><b>Flaky tests</b> destroy trust. Find them from history, quarantine them, and fix the cause (time, ordering, shared state, network) — retries only hide it.</li>
<li>In big repos, run only the tests <b>affected</b> by a change on each push, and everything nightly.</li>
<li>Watch the slowest tests (<code>pytest --durations=10</code>) and run in parallel with <code>pytest -n auto</code> (pytest-xdist).</li>
<li>Avoid test smells: no asserts, sleeps, prints, tests that depend on each other's order.</li>
</ul>
""", practice=["Find the Flaky Tests", "Should You Retry Flaky Tests?", "Run Only the Affected Tests", "Check the Test Pyramid", "Find the Slowest Tests", "Spot Test Smells"])
