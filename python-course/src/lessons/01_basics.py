from lib import *

LESSON("Basics", "Your first program", """
<p>A <b>program</b> is a list of instructions the computer follows <b>from top to bottom</b>, one line at a time. Python reads your code, and runs each line in order.</p>
<p>The first instruction everyone learns is <code>print</code>. It shows a value on the screen:</p>
<pre><code class="py">print("Hello, world!")
print(2 + 3)</code></pre>
<p>Text must be inside quotes (<code>"…"</code> or <code>'…'</code>) — that's a <b>string</b>. Numbers don't need quotes. Python works out <code>2 + 3</code> first and prints <code>5</code>.</p>
<div class="tip">How to read the animations: the <b>highlighted line is the one about to run</b>. Press ▶ or the → key to run it. The black box shows everything printed so far.</div>
<p>Lines starting with <code>#</code> are <b>comments</b>. Python ignores them; they're notes for humans.</p>
""")


@LD
def first_program():
    # Python runs these lines from top to bottom
    print("Hello, world!")
    print(2 + 3)
    print("2 + 3")
    print("Python", "is", "fun")


LESSON("Basics", "Variables: names for values", """
<p>A <b>variable</b> is a name that points to a value, so you can use it later. You create one with <code>=</code>, the <b>assignment</b> operator:</p>
<pre><code class="py">age = 20        # read it as: "age now refers to 20"
age = age + 1   # take the current value, add 1, store it back</code></pre>
<p><code>=</code> does <b>not</b> mean "equals" like in maths. It means "compute the right side, then make the name on the left point to the result". That's why <code>age = age + 1</code> makes sense.</p>
<p>Rules for names: letters, digits and underscores; can't start with a digit; case matters (<code>score</code> ≠ <code>Score</code>). Use clear names like <code>total_price</code>, not <code>tp</code>.</p>
""", practice=["Swap Two Variables", "Rectangle Area and Perimeter"])


@LD
def variables_demo():
    score = 10
    bonus = 5
    score = score + bonus
    score = score * 2
    name = "Mira"
    print(name, "scored", score)


LESSON("Basics", "Data types", """
<p>Every value has a <b>type</b>, which decides what you can do with it.</p>
<table>
<tr><th>Type</th><th>Meaning</th><th>Examples</th></tr>
<tr><td><code>int</code></td><td>whole numbers</td><td><code>7</code>, <code>-3</code>, <code>1_000_000</code></td></tr>
<tr><td><code>float</code></td><td>decimal numbers</td><td><code>3.14</code>, <code>-0.5</code>, <code>2.0</code></td></tr>
<tr><td><code>str</code></td><td>text</td><td><code>"hi"</code>, <code>'42'</code>, <code>""</code></td></tr>
<tr><td><code>bool</code></td><td>yes / no</td><td><code>True</code>, <code>False</code></td></tr>
<tr><td><code>NoneType</code></td><td>"no value"</td><td><code>None</code></td></tr>
</table>
<p>Ask Python for a type with <code>type(value)</code>. Note that <code>"42"</code> (a str) and <code>42</code> (an int) are different: <code>"42" + "1"</code> is <code>"421"</code>, while <code>42 + 1</code> is <code>43</code>.</p>
<p>Python is <b>dynamically typed</b>: a variable can refer to an int now and a str later. The <i>value</i> has a type; the name doesn't.</p>
""", practice=["Name of a Value's Type", "Is It Truthy?", "Count the True Values"])


@LD
def types_demo():
    a = 42
    b = 3.5
    c = "42"
    d = True
    e = None
    print(type(a), type(b), type(c), type(d), type(e))
    print(a + 1, c + "1")


LESSON("Core", "Converting between types, and input()", """
<p>You can convert values with the type's name used as a function:</p>
<pre><code class="py">int("42")      # 42        text → whole number
float("3.5")   # 3.5
str(10)        # "10"      number → text
int(3.99)      # 3         cuts off the decimals (doesn't round)
bool(0)        # False     0, "", [], None are False; most else True</code></pre>
<p><code>input("question")</code> pauses the program, lets the user type, and returns what they typed — <b>always as a str</b>. So for numbers you convert:</p>
<pre><code class="py">age = int(input("How old are you? "))
print("Next year you'll be", age + 1)</code></pre>
<div class="warn"><code>int("3.5")</code> and <code>int("hello")</code> raise a <code>ValueError</code>. Later you'll learn to handle that with <code>try</code>/<code>except</code>.</div>
<p>Python also converts <b>automatically</b> in a few safe cases (<b>implicit conversion</b>): <code>3 + 2.5</code> gives the float <code>5.5</code>.</p>
""", practice=["Add Two Numbers Given as Text", "Is It a Whole Number String?", "Sum of Digits", "Last Digit"])


@LD
def conversion_demo():
    typed = "25"
    age = int(typed)
    next_year = age + 1
    price = float("19.99")
    label = "Age: " + str(age)
    print(label, "| next year:", next_year, "| price:", price)
    print(int(3.99), bool(0), bool("0"))


LESSON("Core", "Printing nicely with f-strings", """
<p>An <b>f-string</b> is a string with an <code>f</code> before the quote. Anything inside <code>{ }</code> is calculated and placed into the text:</p>
<pre><code class="py">name, price, qty = "pen", 12.5, 3
print(f"{qty} {name}s cost {price * qty}")      # 3 pens cost 37.5
print(f"{price:.2f}")                            # 12.50  (2 decimals)
print(f"{7:03}")                                 # 007    (pad with zeros)
print(f"{'left':&lt;8}|{'right':&gt;8}")              # align in 8 characters</code></pre>
<p><code>print</code> also has two useful options: <code>sep</code> (what goes between values, default a space) and <code>end</code> (what goes at the end, default a new line).</p>
""", practice=["Full Name", "Format Money", "Seconds to Clock Time"])


@LD
def fstring_demo():
    item = "notebook"
    price = 45.5
    qty = 3
    total = price * qty
    print(f"{qty} x {item} = {total}")
    print(f"Total with 2 decimals: {total:.2f}")
    print("a", "b", "c", sep="-")
    print("no new line", end="! ")
    print("done")


LESSON("Advanced", "How Python stores values", """
<p>In Python, every value is an <b>object</b> living in memory, and a variable is a <b>label</b> attached to an object. <code>x = 5</code> creates (or reuses) the object 5 and sticks the label <code>x</code> on it.</p>
<ul>
<li><code>id(x)</code> gives the object's identity (like an address).</li>
<li><code>x is y</code> asks "same object?"; <code>x == y</code> asks "same value?".</li>
<li><b>Immutable</b> types (int, float, str, bool, tuple) can't be changed in place — "changing" them makes a new object.</li>
<li><b>Mutable</b> types (list, dict, set) can be changed in place, so two labels on the same list both see the change. You'll meet this again in the Lists topic.</li>
</ul>
<p>This "labels on objects" model explains most surprises beginners hit later.</p>
""")


@LD
def labels_demo():
    a = 10
    b = a
    a = a + 1
    print("a =", a, "b =", b)
    x = [1, 2]
    y = x
    y.append(3)
    print("x =", x, "y =", y, "same object?", x is y)


LESSON("Advanced", "Reading the practice answers", """
<p>Each practice answer is written as a small <b>function</b>, so the site can test it automatically:</p>
<pre><code class="py">def c_to_f(celsius):        # a recipe called c_to_f that takes one input
    return celsius * 9 / 5 + 32   # the answer it gives back</code></pre>
<p>For now read <code>def name(inputs):</code> as "a recipe with these inputs" and <code>return</code> as "give back this answer". You'll learn functions properly in topic 9. In a real script you'd use it like this:</p>
<pre><code class="py">temp = float(input("Celsius: "))
print(c_to_f(temp))</code></pre>
<p>For every question you'll see two answers:</p>
<ul>
<li><b>Brute force — the long way</b>: every step written out. Easy to follow; often longer or slower.</li>
<li><b>Optimal — the Pythonic way</b>: shorter, clearer or faster, using Python's built-in tools.</li>
</ul>
<p>Both are shown running line by line. Try the question yourself first!</p>
""", practice=["Celsius to Fahrenheit", "Greeting From Input", "Bill Split With Tip"])


@LD
def program_demo():
    def c_to_f(celsius):
        return celsius * 9 / 5 + 32

    temps = [0, 37, 100]
    for t in temps:
        print(t, "C =", c_to_f(t), "F")
