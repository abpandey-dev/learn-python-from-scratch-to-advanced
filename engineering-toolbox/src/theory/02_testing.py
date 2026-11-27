from lib import *

THEORY("Kinds of tests", """
<table>
<tr><th>Kind</th><th>Checks</th><th>Speed</th></tr>
<tr><td>Unit</td><td>one function or class, dependencies faked</td><td>milliseconds</td></tr>
<tr><td>Integration</td><td>your code with a real database, queue or service</td><td>seconds</td></tr>
<tr><td>End-to-end</td><td>the whole system through its UI or API</td><td>seconds to minutes</td></tr>
<tr><td>Contract</td><td>that two services still agree on an API</td><td>fast</td></tr>
<tr><td>Regression</td><td>a bug that happened once never returns</td><td>any</td></tr>
</table>
""")

THEORY("Test doubles", """
<table>
<tr><th>Double</th><th>What it does</th></tr>
<tr><td>Stub</td><td>returns canned answers</td></tr>
<tr><td>Mock</td><td>records calls so you can assert on them</td></tr>
<tr><td>Fake</td><td>a working lightweight version (in-memory database)</td></tr>
<tr><td>Spy</td><td>wraps the real thing and records calls</td></tr>
</table>
""")

FAQ("What makes a good unit test?", "<p>Fast, independent, repeatable, tests one behaviour, has a clear name that says what should happen, and fails with a message that explains why.</p>")
FAQ("When should you mock?", "<p>At boundaries you don't control or that are slow or non-deterministic: network, payment providers, email, time, randomness. Don't mock the code you're testing, and prefer fakes for complex dependencies.</p>")
FAQ("Is 100% coverage worth it?", "<p>Not as a goal. Coverage finds untested code; it doesn't prove the tests check the right things. Aim high on critical logic and use mutation testing to judge test quality.</p>")
FAQ("How do you deal with flaky tests?", "<p>Detect them from run history, quarantine so they don't block merges, then fix the root cause: shared state, test order, real time, network or races.</p>")
FAQ("What is TDD?", "<p>Test-driven development: write a failing test, write the simplest code to pass it, then refactor. It forces clear interfaces and gives you tests for free.</p>")
FAQ("How do you test code that calls an external API?", "<p>Unit tests with a stub or mock of the client; a few integration tests against a sandbox or a recorded response (e.g. VCR); and contract tests so you notice when the API changes.</p>")
