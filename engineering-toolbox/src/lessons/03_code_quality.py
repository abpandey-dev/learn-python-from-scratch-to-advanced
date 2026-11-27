from lib import *
import ast

LESSON("Basics", "Why code quality tools exist", """
<p>Code is read far more often than it's written. Teams agree on a <b>style</b> (PEP 8, enforced by a formatter so nobody argues about it) and run a <b>linter</b> that finds likely bugs: unused imports, undefined names, mutable defaults, bare <code>except</code>. Reviewers can then spend their time on design instead of commas.</p>
<pre><code class="py">pip install ruff
ruff check .          # find problems
ruff check --fix .    # fix the safe ones automatically
ruff format .         # format the code

# pyproject.toml
[tool.ruff]
line-length = 88
[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]   # pycodestyle, pyflakes, isort, bugbear, pyupgrade
ignore = ["E501"]</code></pre>
""", practice=["Lines Too Long", "Whitespace Problems", "Check Naming Conventions", "Sort Imports Like isort", "Which Lint Rules Are On?", "Count Lines of Code"])

LESSON("Core", "How a linter reads your code", """
<p>Linters don't run your program. They parse it into an <b>abstract syntax tree</b> with <code>ast.parse</code> and look for patterns: an import whose name never appears, a default argument that's a list, an <code>except</code> whose body is just <code>pass</code>. You can write a custom check for your team in a few lines.</p>
""", practice=["Find Unused Imports", "Mutable Default Arguments", "Swallowed Exceptions", "Unreachable Code", "Shadowed Builtins", "Old-Style String Formatting", "Magic Numbers"])


@LD
def ast_demo():
    tree = ast.parse("import os\ndef add(item, items=[]):\n    items.append(item)\n    return items\n")
    print(ast.dump(tree.body[1].args.defaults[0]))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            print("function", node.name, "on line", node.lineno)


LESSON("Core", "Type hints and type checking", """
<p>Type hints document what a function expects and returns, power editor autocompletion, and let <b>mypy</b> or <b>pyright</b> catch bugs before running anything. They're ignored at runtime — use <b>pydantic</b> when you need to <i>validate</i> data at the edges (API requests, config files).</p>
<pre><code class="py">from dataclasses import dataclass

@dataclass
class Order:
    id: int
    amount: float
    note: str | None = None
    tags: list[str] = field(default_factory=list)

def total(orders: list[Order]) -> float:
    return sum(o.amount for o in orders)

total(["12.5"])   # mypy: Argument 1 has incompatible type "list[str]"

# runtime validation at the boundary
from pydantic import BaseModel
class OrderIn(BaseModel):
    id: int
    amount: float
OrderIn(id="7", amount="9.5")   # coerces to id=7, amount=9.5; invalid input raises</code></pre>
""", practice=["Type Hint Coverage", "Check Call Arguments Against Hints", "Docstring Coverage"])

LESSON("Advanced", "Keeping a codebase healthy", """
<ul>
<li><b>Complexity</b>: functions with many branches are hard to test — split them. Aim for cyclomatic complexity under ~10 and functions that fit on a screen.</li>
<li><b>Duplication</b>: extract repeated blocks into functions (but don't abstract too early — "rule of three").</li>
<li><b>Architecture rules</b>: enforce that low-level modules never import high-level ones, so the code stays layered.</li>
<li>Run all of it automatically with <b>pre-commit</b> locally and again in <b>CI</b>, so it never depends on memory.</li>
</ul>
<pre><code class="py"># .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks: [{id: ruff, args: [--fix]}, {id: ruff-format}]
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks: [{id: mypy}]</code></pre>
""", practice=["Cyclomatic Complexity", "Functions That Do Too Much", "Find Duplicated Code", "Enforce Architecture Layers"])
