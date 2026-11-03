from lib import *

THEORY("Definitions", """
<p>An <b>operator</b> is a symbol (or keyword) that performs an operation on values called <b>operands</b>. In <code>3 + 4</code>, <code>+</code> is the operator and 3 and 4 are operands.</p>
<p>An <b>expression</b> is any combination of values, variables, operators and function calls that Python can <b>evaluate</b> to produce a single value: <code>price * qty + tax</code>. A <b>statement</b> is a complete instruction, such as an assignment <code>total = price * qty</code>.</p>
<p>Operators are <b>unary</b> (one operand: <code>-x</code>, <code>not x</code>) or <b>binary</b> (two operands: <code>a + b</code>). Python also has a <b>ternary</b> conditional expression: <code>a if cond else b</code>.</p>
""")

THEORY("Categories of operators", """
<table>
<tr><th>Category</th><th>Operators</th><th>Result</th></tr>
<tr><td>Arithmetic</td><td><code>+ - * / // % **</code></td><td>number</td></tr>
<tr><td>Comparison (relational)</td><td><code>== != &lt; &gt; &lt;= &gt;=</code></td><td>bool</td></tr>
<tr><td>Logical</td><td><code>and or not</code></td><td>one of the operands (truthy/falsy)</td></tr>
<tr><td>Assignment</td><td><code>= += -= *= /= //= %= **= &amp;= |= ^= &lt;&lt;= &gt;&gt;=</code>, walrus <code>:=</code></td><td>— (statement)</td></tr>
<tr><td>Identity</td><td><code>is</code>, <code>is not</code></td><td>bool</td></tr>
<tr><td>Membership</td><td><code>in</code>, <code>not in</code></td><td>bool</td></tr>
<tr><td>Bitwise</td><td><code>&amp; | ^ ~ &lt;&lt; &gt;&gt;</code></td><td>int</td></tr>
</table>
<p>The <b>walrus operator</b> <code>:=</code> (Python 3.8+) assigns inside an expression: <code>if (n := len(data)) &gt; 10:</code>.</p>
""")

THEORY("Division in detail", """
<table>
<tr><th>Expression</th><th>Result</th><th>Rule</th></tr>
<tr><td><code>7 / 2</code></td><td>3.5</td><td><b>true division</b>, always float</td></tr>
<tr><td><code>6 / 2</code></td><td>3.0</td><td>still a float</td></tr>
<tr><td><code>7 // 2</code></td><td>3</td><td><b>floor division</b>: rounds toward −∞</td></tr>
<tr><td><code>-7 // 2</code></td><td>−4</td><td>floor, not truncation</td></tr>
<tr><td><code>7 % 2</code></td><td>1</td><td>remainder</td></tr>
<tr><td><code>-7 % 2</code></td><td>1</td><td>result has the sign of the divisor</td></tr>
<tr><td><code>7.5 // 2</code></td><td>3.0</td><td>float in → float out</td></tr>
<tr><td><code>1 / 0</code></td><td>ZeroDivisionError</td><td>also for // and %</td></tr>
</table>
<p>Identity that always holds: <code>a == (a // b) * b + (a % b)</code>. <code>divmod(a, b)</code> returns <code>(a // b, a % b)</code>.</p>
""")

THEORY("Precedence and associativity", """
<table>
<tr><th>Priority</th><th>Operators</th><th>Associativity</th></tr>
<tr><td>1 (highest)</td><td><code>( )</code></td><td>—</td></tr>
<tr><td>2</td><td><code>**</code></td><td>right to left</td></tr>
<tr><td>3</td><td><code>+x -x ~x</code></td><td>right to left</td></tr>
<tr><td>4</td><td><code>* / // %</code></td><td>left to right</td></tr>
<tr><td>5</td><td><code>+ -</code></td><td>left to right</td></tr>
<tr><td>6</td><td><code>&lt;&lt; &gt;&gt;</code></td><td>left to right</td></tr>
<tr><td>7</td><td><code>&amp;</code></td><td>left to right</td></tr>
<tr><td>8</td><td><code>^</code></td><td>left to right</td></tr>
<tr><td>9</td><td><code>|</code></td><td>left to right</td></tr>
<tr><td>10</td><td>comparisons, <code>is</code>, <code>in</code></td><td>chained</td></tr>
<tr><td>11</td><td><code>not</code></td><td>—</td></tr>
<tr><td>12</td><td><code>and</code></td><td>left to right</td></tr>
<tr><td>13</td><td><code>or</code></td><td>left to right</td></tr>
<tr><td>14 (lowest)</td><td><code>if … else</code>, <code>lambda</code>, <code>:=</code></td><td>—</td></tr>
</table>
<p><b>Associativity</b> decides the order among operators of equal priority: <code>10 - 4 - 3</code> = (10 − 4) − 3 = 3, but <code>2 ** 3 ** 2</code> = 2 ** (3 ** 2) = 512.</p>
""")

THEORY("Truthiness and short-circuit evaluation", """
<p>Any value can be used where a bool is expected. <b>Falsy</b> values: <code>False</code>, <code>None</code>, <code>0</code>, <code>0.0</code>, <code>""</code>, <code>[]</code>, <code>()</code>, <code>{}</code>, <code>set()</code>, <code>range(0)</code>. Everything else is <b>truthy</b>.</p>
<ul>
<li><code>x and y</code>: if x is falsy, returns x (y is never evaluated); otherwise returns y.</li>
<li><code>x or y</code>: if x is truthy, returns x (y is never evaluated); otherwise returns y.</li>
<li><code>not x</code>: always returns a bool.</li>
</ul>
<p>Short-circuiting lets you guard expressions: <code>if user and user.is_admin</code> never touches <code>user.is_admin</code> when user is None.</p>
""")

THEORY("Operators on other types", """
<table>
<tr><th>Expression</th><th>Result</th><th>Meaning</th></tr>
<tr><td><code>"ab" + "cd"</code></td><td>"abcd"</td><td>concatenation</td></tr>
<tr><td><code>"ab" * 3</code></td><td>"ababab"</td><td>repetition</td></tr>
<tr><td><code>[1, 2] + [3]</code></td><td>[1, 2, 3]</td><td>list concatenation</td></tr>
<tr><td><code>"a" &lt; "b"</code></td><td>True</td><td>strings compare alphabetically (by Unicode code)</td></tr>
<tr><td><code>[1, 2] == [1, 2]</code></td><td>True</td><td>element-wise equality</td></tr>
<tr><td><code>{1, 2} | {2, 3}</code></td><td>{1, 2, 3}</td><td>set union</td></tr>
<tr><td><code>"5" + 3</code></td><td>TypeError</td><td>no implicit str/int mixing</td></tr>
</table>
<p>This works because operators call <b>special methods</b>: <code>a + b</code> calls <code>a.__add__(b)</code>. Your own classes can define them (<b>operator overloading</b>, see the OOP topic).</p>
""")

FAQ("What is the difference between <code>/</code> and <code>//</code>?", "<p><code>/</code> is true division and always returns a float (7 / 2 = 3.5). <code>//</code> is floor division: it rounds the result down toward negative infinity (7 // 2 = 3, −7 // 2 = −4).</p>")
FAQ("What does the % operator return for negative numbers?", "<p>In Python the result takes the sign of the divisor, so −7 % 3 = 2 and 7 % −3 = −2. This keeps <code>a == (a // b) * b + a % b</code> true.</p>")
FAQ("What is short-circuit evaluation?", "<p><code>and</code> and <code>or</code> evaluate left to right and stop as soon as the result is known: <code>False and …</code> never evaluates the right side; <code>True or …</code> neither.</p>")
FAQ("What does <code>x or y</code> return?", "<p>Not necessarily a bool: it returns x if x is truthy, otherwise y. That's why <code>name or 'Guest'</code> gives a default.</p>")
FAQ("Does Python have <code>++</code> and <code>--</code>?", "<p>No. Use <code>x += 1</code> and <code>x -= 1</code>. <code>++x</code> is valid syntax but just means +(+x), which doesn't change x.</p>")
FAQ("What is <code>2 ** 3 ** 2</code>?", "<p>512. The power operator is right-associative, so it's 2 ** (3 ** 2) = 2 ** 9.</p>")
FAQ("What is the walrus operator?", "<p><code>:=</code>, the assignment expression (Python 3.8+). It assigns a value and returns it in one expression, e.g. <code>while (line := f.readline()):</code>.</p>")
