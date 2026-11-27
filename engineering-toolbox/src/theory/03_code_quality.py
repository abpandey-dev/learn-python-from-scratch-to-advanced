from lib import *

THEORY("Common rule families", """
<table>
<tr><th>Prefix</th><th>From</th><th>Catches</th></tr>
<tr><td>E / W</td><td>pycodestyle</td><td>style and whitespace</td></tr>
<tr><td>F</td><td>pyflakes</td><td>unused imports, undefined names</td></tr>
<tr><td>I</td><td>isort</td><td>import order</td></tr>
<tr><td>B</td><td>flake8-bugbear</td><td>likely bugs (mutable defaults, loop variable capture)</td></tr>
<tr><td>UP</td><td>pyupgrade</td><td>old syntax that has a modern form</td></tr>
<tr><td>S</td><td>bandit</td><td>security issues</td></tr>
</table>
""")

FAQ("Why use a formatter like Black or ruff format?", "<p>It removes style debates and noisy diffs: everyone's code looks the same, and reviews focus on logic.</p>")
FAQ("Do type hints make Python slower?", "<p>No. They're not enforced at runtime; they're read by type checkers and editors. Use pydantic or explicit checks where runtime validation matters.</p>")
FAQ("What's wrong with a mutable default argument?", "<p>The default object is created once when the function is defined and shared by every call, so changes leak between calls. Use <code>None</code> and create the list inside.</p>")
FAQ("What is cyclomatic complexity?", "<p>The number of independent paths through a function: 1 plus the number of decision points. It's roughly the minimum number of tests needed to cover every branch.</p>")
FAQ("Why is a bare except bad?", "<p>It also catches KeyboardInterrupt and SystemExit and hides bugs. Catch the specific exceptions you can handle, and log or re-raise the rest.</p>")
FAQ("How do you introduce linting to an old codebase?", "<p>Add the formatter in one commit, enable a small rule set, auto-fix, then add rules gradually; lint only changed files in CI at first if the backlog is large.</p>")
