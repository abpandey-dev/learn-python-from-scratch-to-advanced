from lib import *

THEORY("Definition", """
<p><b>Control flow</b> is the order in which a program's statements run. By default it is <b>sequential</b> (top to bottom). <b>Conditional statements</b> (also called <b>selection</b> or <b>decision-making</b> statements) let the program choose which block to run based on a <b>condition</b> — an expression that evaluates to True or False.</p>
<p>The three basic control structures of structured programming are <b>sequence</b>, <b>selection</b> (if) and <b>iteration</b> (loops).</p>
""")

THEORY("Forms of the if statement", """
<table>
<tr><th>Form</th><th>Syntax</th><th>Runs</th></tr>
<tr><td>Simple if</td><td><code>if cond:</code> block</td><td>block only when cond is truthy</td></tr>
<tr><td>if–else</td><td><code>if cond:</code> A <code>else:</code> B</td><td>exactly one of A, B</td></tr>
<tr><td>if–elif–else ladder</td><td><code>if c1:</code> A <code>elif c2:</code> B … <code>else:</code> Z</td><td>the first block whose condition is truthy, else Z</td></tr>
<tr><td>Nested if</td><td>an if inside another block</td><td>inner test only when the outer one passes</td></tr>
<tr><td>Conditional expression</td><td><code>x if cond else y</code></td><td>an <b>expression</b> that gives a value</td></tr>
<tr><td>match–case</td><td><code>match value:</code> <code>case pattern:</code></td><td>the first matching case</td></tr>
</table>
<p>A block can't be empty; use <code>pass</code> as a placeholder.</p>
""")

THEORY("How a condition is evaluated", """
<ol>
<li>The expression after <code>if</code>/<code>elif</code> is evaluated.</li>
<li>The result is converted to bool using <b>truthiness</b> (the same as <code>bool(value)</code>).</li>
<li>If True, the block runs and the rest of the ladder is skipped. If False, Python moves to the next <code>elif</code>, then <code>else</code>.</li>
</ol>
<p>Falsy values: <code>False, None, 0, 0.0, "", [], (), {}, set(), range(0)</code>. Everything else is truthy, including <code>"0"</code>, <code>"False"</code> and <code>[0]</code>.</p>
<p>Because <code>and</code>/<code>or</code> short-circuit, parts of a condition may never run: <code>if x != 0 and 10 / x &gt; 1</code> is safe.</p>
""")

THEORY("Indentation and blocks", """
<p>Python uses <b>indentation</b> instead of braces to define a block. All statements in the same block must be indented by the same amount (PEP 8: 4 spaces, never mix tabs and spaces).</p>
<pre><code class="py">if x &gt; 0:
    print("positive")     # inside the if
    x -= 1                # inside the if
print("always")           # outside</code></pre>
<p>Errors: <code>IndentationError: expected an indented block</code>, <code>unexpected indent</code>, and <code>SyntaxError: expected ':'</code>.</p>
""")

THEORY("match-case in detail", """
<table>
<tr><th>Pattern</th><th>Example</th><th>Matches</th></tr>
<tr><td>Literal</td><td><code>case 404:</code></td><td>the exact value</td></tr>
<tr><td>OR pattern</td><td><code>case "y" | "yes":</code></td><td>any alternative</td></tr>
<tr><td>Capture</td><td><code>case x:</code></td><td>anything, binds it to x</td></tr>
<tr><td>Wildcard</td><td><code>case _:</code></td><td>anything (default)</td></tr>
<tr><td>Sequence</td><td><code>case [first, *rest]:</code></td><td>lists/tuples by shape</td></tr>
<tr><td>Mapping</td><td><code>case {"type": "click", "x": x}:</code></td><td>dicts with those keys</td></tr>
<tr><td>Class</td><td><code>case Point(x=0, y=0):</code></td><td>objects by type and attributes</td></tr>
<tr><td>Guard</td><td><code>case n if n &lt; 0:</code></td><td>pattern plus an extra condition</td></tr>
</table>
<p>Unlike C's <code>switch</code>, there is no fall-through: only the first matching case runs.</p>
""")

THEORY("Good practices and common mistakes", """
<ul>
<li>Order an elif ladder from the most restrictive condition to the least.</li>
<li>Prefer <code>if x:</code> / <code>if not items:</code> over <code>if x == True:</code> / <code>if len(items) == 0:</code>.</li>
<li>Compare with None using <code>is</code>: <code>if result is None:</code>.</li>
<li>Avoid deep nesting — use guard clauses (early <code>return</code>) and combined conditions.</li>
<li>Replace long value-to-value ladders with a dict or tuple lookup.</li>
<li>Mistake: <code>if x = 5:</code> (assignment) instead of <code>if x == 5:</code> — a SyntaxError in Python.</li>
<li>Mistake: <code>if x == 1 or 2:</code> is always true (it means <code>(x == 1) or 2</code>). Write <code>if x in (1, 2):</code>.</li>
</ul>
""")

FAQ("What is the difference between if–elif and multiple ifs?", "<p>In an if–elif ladder at most one block runs: once a condition is true the rest are skipped. With separate ifs every condition is checked independently and several blocks can run.</p>")
FAQ("Does Python have a switch statement?", "<p>Since Python 3.10 it has <code>match</code>–<code>case</code>, which is more powerful than a classic switch (it matches structure and captures values). Before that, people used if–elif ladders or dict lookups.</p>")
FAQ("What is a ternary operator in Python?", "<p>The conditional expression <code>a if condition else b</code>. It evaluates to a when the condition is true and b otherwise, and can be used inside other expressions.</p>")
FAQ("Why is <code>if x == 1 or 2:</code> always true?", "<p>It is parsed as <code>(x == 1) or 2</code>, and 2 is truthy. Use <code>x == 1 or x == 2</code> or <code>x in (1, 2)</code>.</p>")
FAQ("What does <code>pass</code> do?", "<p>Nothing. It's a placeholder where Python requires a statement but you have nothing to run yet, such as an empty if block.</p>")
FAQ("Which values are falsy?", "<p><code>False</code>, <code>None</code>, numeric zero (<code>0</code>, <code>0.0</code>, <code>0j</code>), and empty collections (<code>''</code>, <code>[]</code>, <code>()</code>, <code>{}</code>, <code>set()</code>, <code>range(0)</code>). Objects can define their own truthiness with <code>__bool__</code> or <code>__len__</code>.</p>")
