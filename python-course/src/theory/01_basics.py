from lib import *

THEORY("What is Python?", """
<p><b>Python</b> is a high-level, general-purpose programming language created by Guido van Rossum and first released in 1991. It is known for code that reads almost like English.</p>
<h4>Key features</h4>
<ul>
<li><b>High-level</b> — you don't manage memory or hardware details.</li>
<li><b>Interpreted</b> — code runs line by line through the Python interpreter; no separate compile step for you.</li>
<li><b>Dynamically typed</b> — you don't declare types; each value carries its own type.</li>
<li><b>Strongly typed</b> — Python won't silently mix incompatible types (<code>"5" + 3</code> is an error).</li>
<li><b>Multi-paradigm</b> — supports procedural, object-oriented and functional styles.</li>
<li><b>Huge standard library</b> — "batteries included", plus hundreds of thousands of packages on PyPI.</li>
</ul>
<h4>Where it's used</h4>
<p>Web development (Django, Flask, FastAPI), data analysis (pandas), machine learning and AI (PyTorch, scikit-learn), automation and scripting, testing, scientific computing.</p>
""")

THEORY("How Python runs your code", """
<ol>
<li>You write source code in a <code>.py</code> file (or type it into the interactive shell / REPL).</li>
<li>The interpreter (<b>CPython</b>, the standard one) compiles it to <b>bytecode</b> (<code>.pyc</code>), a simpler instruction format.</li>
<li>The <b>Python Virtual Machine</b> executes the bytecode one instruction at a time.</li>
</ol>
<p>Errors come in two kinds: <b>syntax errors</b> are found before anything runs (e.g. a missing colon); <b>runtime errors (exceptions)</b> happen while running (e.g. dividing by zero).</p>
<p>Ways to run Python: the REPL (<code>python3</code> then type lines), a script (<code>python3 app.py</code>), notebooks (Jupyter), or an IDE such as VS Code or PyCharm.</p>
""")

THEORY("Syntax rules", """
<ul>
<li><b>Indentation is part of the syntax.</b> Blocks (inside <code>if</code>, loops, functions) are marked by indenting — 4 spaces by convention — not by braces.</li>
<li>One statement per line normally. A line ends the statement; no semicolon needed.</li>
<li><b>Comments</b> start with <code>#</code>. Multi-line explanations at the top of a function use a <b>docstring</b> <code>&quot;&quot;&quot;…&quot;&quot;&quot;</code>.</li>
<li>Python is <b>case-sensitive</b>: <code>print</code> works, <code>Print</code> doesn't.</li>
<li>Long expressions can continue on the next line inside brackets <code>( )</code>, <code>[ ]</code>, <code>{ }</code>.</li>
</ul>
""")

THEORY("Variables and identifiers", """
<p>A <b>variable</b> is a name bound to an object in memory. It is created the first time you assign to it.</p>
<h4>Identifier rules</h4>
<ul>
<li>May contain letters, digits and underscores; must not start with a digit.</li>
<li>Must not be a <b>keyword</b>: <code>False None True and as assert async await break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield</code>.</li>
<li>Case-sensitive.</li>
</ul>
<h4>Conventions (PEP 8)</h4>
<table>
<tr><th>Kind</th><th>Style</th><th>Example</th></tr>
<tr><td>variables, functions</td><td>snake_case</td><td><code>total_price</code></td></tr>
<tr><td>constants</td><td>UPPER_CASE</td><td><code>MAX_SIZE</code></td></tr>
<tr><td>classes</td><td>PascalCase</td><td><code>BankAccount</code></td></tr>
<tr><td>"private" / internal</td><td>leading underscore</td><td><code>_cache</code></td></tr>
</table>
<p><b>Multiple assignment</b>: <code>a, b = 1, 2</code>; <b>chained</b>: <code>x = y = 0</code>; <b>augmented</b>: <code>x += 1</code>.</p>
""")

THEORY("Built-in data types", """
<table>
<tr><th>Category</th><th>Type</th><th>Example</th><th>Mutable?</th></tr>
<tr><td rowspan="3">Numeric</td><td><code>int</code></td><td><code>42</code> (unlimited size)</td><td>no</td></tr>
<tr><td><code>float</code></td><td><code>3.14</code> (64-bit decimal)</td><td>no</td></tr>
<tr><td><code>complex</code></td><td><code>2 + 3j</code></td><td>no</td></tr>
<tr><td>Text</td><td><code>str</code></td><td><code>"hello"</code></td><td>no</td></tr>
<tr><td>Boolean</td><td><code>bool</code></td><td><code>True</code>, <code>False</code></td><td>no</td></tr>
<tr><td>None</td><td><code>NoneType</code></td><td><code>None</code></td><td>no</td></tr>
<tr><td rowspan="3">Sequence</td><td><code>list</code></td><td><code>[1, 2, 3]</code></td><td><b>yes</b></td></tr>
<tr><td><code>tuple</code></td><td><code>(1, 2, 3)</code></td><td>no</td></tr>
<tr><td><code>range</code></td><td><code>range(5)</code></td><td>no</td></tr>
<tr><td>Mapping</td><td><code>dict</code></td><td><code>{"a": 1}</code></td><td><b>yes</b></td></tr>
<tr><td rowspan="2">Set</td><td><code>set</code></td><td><code>{1, 2}</code></td><td><b>yes</b></td></tr>
<tr><td><code>frozenset</code></td><td><code>frozenset({1, 2})</code></td><td>no</td></tr>
</table>
<p>Floats are stored in binary, so some decimals are approximate: <code>0.1 + 0.2</code> is <code>0.30000000000000004</code>. Use <code>round()</code> for display, or the <code>decimal</code> module for money.</p>
""")

THEORY("Type conversion", """
<p><b>Implicit conversion</b> (coercion) — Python converts automatically when it's safe: <code>int + float → float</code>, <code>True + 1 → 2</code>.</p>
<p><b>Explicit conversion</b> (casting) — you call the type:</p>
<table>
<tr><th>Call</th><th>Result</th><th>Notes</th></tr>
<tr><td><code>int("42")</code></td><td>42</td><td>text must be a whole number</td></tr>
<tr><td><code>int(3.99)</code></td><td>3</td><td>truncates toward zero</td></tr>
<tr><td><code>float("2.5")</code></td><td>2.5</td><td></td></tr>
<tr><td><code>str(100)</code></td><td>"100"</td><td>anything can become text</td></tr>
<tr><td><code>bool(x)</code></td><td>True/False</td><td>False for 0, 0.0, "", [], {}, set(), None</td></tr>
<tr><td><code>list("abc")</code></td><td>['a', 'b', 'c']</td><td>any iterable</td></tr>
<tr><td><code>round(2.675, 2)</code></td><td>2.67</td><td>banker's rounding and float precision</td></tr>
</table>
""")

THEORY("Input and output", """
<ul>
<li><code>print(*values, sep=" ", end="\\n")</code> — writes values separated by <code>sep</code> and followed by <code>end</code>.</li>
<li><code>input(prompt)</code> — shows the prompt, waits for a line from the keyboard, returns it as a <b>str</b> without the newline.</li>
<li>String formatting: f-strings <code>f"{x:.2f}"</code> (modern, preferred), <code>"{} {}".format(a, b)</code>, and the old <code>"%d" % n</code> style.</li>
</ul>
<table>
<tr><th>Format spec</th><th>Meaning</th><th>Example → output</th></tr>
<tr><td><code>:.2f</code></td><td>2 decimal places</td><td><code>f"{3.14159:.2f}"</code> → 3.14</td></tr>
<tr><td><code>:05</code></td><td>pad to width 5 with zeros</td><td><code>f"{42:05}"</code> → 00042</td></tr>
<tr><td><code>:,</code></td><td>thousands separator</td><td><code>f"{1234567:,}"</code> → 1,234,567</td></tr>
<tr><td><code>:&gt;8</code> / <code>:&lt;8</code> / <code>:^8</code></td><td>right / left / centre in 8 chars</td><td><code>f"{'hi':^8}"</code> → "   hi   "</td></tr>
<tr><td><code>:%</code></td><td>percentage</td><td><code>f"{0.256:.1%}"</code> → 25.6%</td></tr>
</table>
""")

FAQ("Is Python compiled or interpreted?", "<p>Both, technically. CPython compiles source to bytecode, then interprets that bytecode in a virtual machine. Because the compilation is automatic and hidden, Python is usually called an interpreted language.</p>")
FAQ("What does 'dynamically typed' mean?", "<p>Types belong to values, not to variable names, and are checked while the program runs. The same name can refer to an int and later a string. In statically typed languages (Java, C) you declare a variable's type up front.</p>")
FAQ("What is the difference between <code>=</code> and <code>==</code>?", "<p><code>=</code> assigns: it binds a name to a value. <code>==</code> compares two values and gives True or False.</p>")
FAQ("What is the difference between <code>is</code> and <code>==</code>?", "<p><code>==</code> checks equal values; <code>is</code> checks that both names refer to the very same object. Use <code>is</code> only for singletons like <code>None</code> (<code>x is None</code>).</p>")
FAQ("Mutable vs immutable — give examples.", "<p>Mutable objects can be changed in place: list, dict, set. Immutable objects can't: int, float, str, bool, tuple, frozenset. 'Changing' an immutable value really creates a new object.</p>")
FAQ("Why does <code>0.1 + 0.2</code> not equal <code>0.3</code>?", "<p>Floats are stored in binary, and 0.1 has no exact binary representation, so tiny rounding errors appear. Compare floats with <code>math.isclose()</code> and use <code>decimal.Decimal</code> for exact money calculations.</p>")
FAQ("What type does <code>input()</code> return?", "<p>Always <code>str</code>. Convert it with <code>int()</code> or <code>float()</code> when you need a number.</p>")
FAQ("What is None?", "<p>A special value of type NoneType meaning 'no value'. Functions without a <code>return</code> give back None. Test for it with <code>is None</code>.</p>")
