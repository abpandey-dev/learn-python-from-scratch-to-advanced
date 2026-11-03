from lib import *

LESSON("Basics", "Arithmetic operators", """
<table>
<tr><th>Operator</th><th>Name</th><th>Example</th><th>Result</th></tr>
<tr><td><code>+</code></td><td>add</td><td><code>7 + 2</code></td><td>9</td></tr>
<tr><td><code>-</code></td><td>subtract</td><td><code>7 - 2</code></td><td>5</td></tr>
<tr><td><code>*</code></td><td>multiply</td><td><code>7 * 2</code></td><td>14</td></tr>
<tr><td><code>/</code></td><td>divide (always gives a float)</td><td><code>7 / 2</code></td><td>3.5</td></tr>
<tr><td><code>//</code></td><td>floor division (round down)</td><td><code>7 // 2</code></td><td>3</td></tr>
<tr><td><code>%</code></td><td>modulo (remainder)</td><td><code>7 % 2</code></td><td>1</td></tr>
<tr><td><code>**</code></td><td>power</td><td><code>7 ** 2</code></td><td>49</td></tr>
</table>
<p><code>//</code> and <code>%</code> are a pair: <code>a == (a // b) * b + a % b</code>. They answer "how many whole times does b fit?" and "what's left over?".</p>
<p>Uses of <code>%</code>: even/odd (<code>n % 2</code>), last digit (<code>n % 10</code>), wrapping around (<code>(i + 1) % 7</code> for days of the week).</p>
""", practice=["Even or Odd", "Ceiling Division", "Reverse a Number"])


@LD
def arithmetic_demo():
    a = 17
    b = 5
    print(a + b, a - b, a * b)
    print(a / b, a // b, a % b)
    print(2 ** 10)
    check = (a // b) * b + a % b
    print(check == a)


LESSON("Basics", "Comparison and logical operators", """
<p>Comparisons give a <b>bool</b> (True or False): <code>==</code> equal, <code>!=</code> not equal, <code>&lt;</code>, <code>&gt;</code>, <code>&lt;=</code>, <code>&gt;=</code>.</p>
<p>Logical operators combine bools:</p>
<table>
<tr><th>a</th><th>b</th><th>a and b</th><th>a or b</th><th>not a</th></tr>
<tr><td>True</td><td>True</td><td>True</td><td>True</td><td>False</td></tr>
<tr><td>True</td><td>False</td><td>False</td><td>True</td><td>False</td></tr>
<tr><td>False</td><td>True</td><td>False</td><td>True</td><td>True</td></tr>
<tr><td>False</td><td>False</td><td>False</td><td>False</td><td>True</td></tr>
</table>
<p>Python lets you <b>chain</b> comparisons like maths: <code>0 &lt;= score &lt;= 100</code>.</p>
""", practice=["Leap Year", "Within a Range", "Exactly One Is True", "FizzBuzz Word"])


@LD
def logic_demo():
    age = 19
    has_ticket = True
    is_adult = age >= 18
    can_enter = is_adult and has_ticket
    is_teen = 13 <= age <= 19
    print(is_adult, can_enter, is_teen, not can_enter)


LESSON("Core", "Assignment operators", """
<p>Updating a variable with itself is so common that Python has shortcuts:</p>
<table>
<tr><th>Shortcut</th><th>Same as</th></tr>
<tr><td><code>x += 3</code></td><td><code>x = x + 3</code></td></tr>
<tr><td><code>x -= 3</code></td><td><code>x = x - 3</code></td></tr>
<tr><td><code>x *= 3</code></td><td><code>x = x * 3</code></td></tr>
<tr><td><code>x /= 3</code></td><td><code>x = x / 3</code></td></tr>
<tr><td><code>x //= 3</code>, <code>x %= 3</code>, <code>x **= 3</code></td><td>same pattern</td></tr>
</table>
<p>They work on strings and lists too: <code>s += "!"</code>. Python has <b>no</b> <code>x++</code> — write <code>x += 1</code>.</p>
""", practice=["Sum From 1 to n", "Count Digits"])


@LD
def assign_demo():
    balance = 100
    balance += 50
    balance -= 30
    balance *= 2
    balance //= 3
    message = "Balance"
    message += ": " + str(balance)
    print(message)


LESSON("Core", "Order of operations (precedence)", """
<p>Like in maths, some operators go first. From highest to lowest:</p>
<ol>
<li><code>( )</code> brackets</li>
<li><code>**</code> power (right to left: <code>2 ** 3 ** 2</code> = 2 ** 9 = 512)</li>
<li>unary <code>-x</code>, <code>+x</code></li>
<li><code>* / // %</code></li>
<li><code>+ -</code></li>
<li>comparisons <code>== != &lt; &gt; &lt;= &gt;= is in</code></li>
<li><code>not</code></li>
<li><code>and</code></li>
<li><code>or</code></li>
</ol>
<p>Operators on the same level run left to right. <code>-2 ** 2</code> is <code>-4</code> because <code>**</code> beats unary minus.</p>
<div class="tip">Brackets cost nothing and make intent obvious. Use them whenever an expression mixes kinds of operators.</div>
""", practice=["Compound Interest", "Weekly Pay With Overtime"])


@LD
def precedence_demo():
    a = 2 + 3 * 4
    b = (2 + 3) * 4
    c = 2 ** 3 ** 2
    d = -2 ** 2
    e = 10 - 4 - 3
    f = True or False and False
    print(a, b, c, d, e, f)


LESSON("Advanced", "Short-circuit evaluation, identity and membership", """
<h4>Short-circuit</h4>
<p><code>and</code> stops at the first falsy value; <code>or</code> stops at the first truthy value — the rest isn't even evaluated. They also return one of the <b>operands</b>, not just True/False:</p>
<pre><code class="py">name = "" or "Guest"          # "Guest"
x = 0 and 10/0                # 0  (10/0 never runs)</code></pre>
<h4>Identity and membership</h4>
<ul>
<li><code>a is b</code> — the same object? Use it for <code>None</code>: <code>if x is None</code>.</li>
<li><code>x in collection</code> — is x inside a string, list, tuple, set or dict keys?</li>
</ul>
""", practice=["FizzBuzz Word", "Floats Almost Equal"])


@LD
def short_circuit_demo():
    name = ""
    shown = name or "Guest"
    count = 0
    safe = count != 0 and 100 / count > 5
    vowels = "aeiou"
    has_e = "e" in vowels
    x = None
    is_missing = x is None
    print(shown, safe, has_e, is_missing)


LESSON("Advanced", "Bitwise operators", """
<p>Bitwise operators work on the binary digits of integers:</p>
<table>
<tr><th>Op</th><th>Meaning</th><th><code>6</code> (110) with <code>3</code> (011)</th></tr>
<tr><td><code>&amp;</code></td><td>AND each bit</td><td>010 = 2</td></tr>
<tr><td><code>|</code></td><td>OR each bit</td><td>111 = 7</td></tr>
<tr><td><code>^</code></td><td>XOR each bit</td><td>101 = 5</td></tr>
<tr><td><code>~</code></td><td>flip all bits</td><td><code>~6</code> = −7</td></tr>
<tr><td><code>&lt;&lt;</code>, <code>&gt;&gt;</code></td><td>shift left / right</td><td><code>6 &lt;&lt; 1</code> = 12, <code>6 &gt;&gt; 1</code> = 3</td></tr>
</table>
<p>They're used for flags and permissions, fast checks like "power of two" (<code>n &amp; (n - 1) == 0</code>), and many puzzle questions. The DSA handbook has a full topic on them.</p>
""", practice=["Power of Two"])


@LD
def bitwise_demo():
    a = 6
    b = 3
    print(bin(a), bin(b))
    print(a & b, a | b, a ^ b)
    print(a << 1, a >> 1, ~a)
    n = 8
    print(n & (n - 1) == 0)
