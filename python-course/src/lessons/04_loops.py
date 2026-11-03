from lib import *

LESSON("Basics", "Why loops?", """
<p>Printing the numbers 1 to 5 by hand needs 5 lines. Printing 1 to 1,000 would need 1,000 lines. A <b>loop</b> repeats a block of code for you.</p>
<pre><code class="py">for i in range(1, 6):
    print(i)</code></pre>
<p>Each repetition is called an <b>iteration</b>. The variable <code>i</code> is the <b>loop variable</b>; it takes the next value each time round.</p>
<p>Python has two loops: <code>for</code> (go through a known sequence of values) and <code>while</code> (keep going as long as a condition is true).</p>
""", practice=["Multiplication Table", "Countdown"])


@LD
def first_loop():
    for i in range(1, 6):
        print("Round", i)
    print("Loop finished")


LESSON("Basics", "for loops and range()", """
<p><code>range</code> produces a sequence of whole numbers. The <b>stop value is never included</b>.</p>
<table>
<tr><th>Call</th><th>Gives</th></tr>
<tr><td><code>range(5)</code></td><td>0 1 2 3 4</td></tr>
<tr><td><code>range(2, 6)</code></td><td>2 3 4 5</td></tr>
<tr><td><code>range(0, 10, 3)</code></td><td>0 3 6 9</td></tr>
<tr><td><code>range(5, 0, -1)</code></td><td>5 4 3 2 1</td></tr>
</table>
<p>A <code>for</code> loop can also walk through any <b>sequence</b> directly — the characters of a string, the items of a list:</p>
<pre><code class="py">for ch in "cat":
    print(ch)          # c, a, t
for fruit in ["apple", "kiwi"]:
    print(fruit)</code></pre>
""", practice=["Sum of Even Numbers", "Count Vowels"])


@LD
def range_demo():
    evens = []
    for n in range(0, 10, 2):
        evens.append(n)
    print(evens)
    for ch in "cat":
        print(ch.upper())


LESSON("Core", "Accumulators and counters", """
<p>Most loops build up an answer. Create the variable <b>before</b> the loop, update it <b>inside</b>:</p>
<pre><code class="py">total = 0               # sum accumulator starts at 0
count = 0               # counter starts at 0
product = 1             # product accumulator starts at 1
best = items[0]         # running maximum starts at the first item
for x in items:
    total += x
    if x &gt; 0:
        count += 1
    product *= x
    if x &gt; best:
        best = x</code></pre>
<div class="warn">Putting <code>total = 0</code> inside the loop resets it every round — a classic bug.</div>
""", practice=["Factorial", "Largest in a List", "Count Vowels", "Sum of Even Numbers"])


@LD
def accumulator_demo():
    marks = [72, 45, 90, 38]
    total = 0
    passed = 0
    best = marks[0]
    for m in marks:
        total += m
        if m >= 40:
            passed += 1
        if m > best:
            best = m
    print("total", total, "passed", passed, "best", best)


LESSON("Core", "while loops", """
<p>A <code>while</code> loop repeats <b>as long as its condition is True</b>. Use it when you don't know in advance how many rounds you need.</p>
<pre><code class="py">n = 1234
digits = 0
while n &gt; 0:
    n //= 10
    digits += 1</code></pre>
<p>Something inside the loop must eventually make the condition False. If not, you get an <b>infinite loop</b> (stop it with Ctrl + C).</p>
<p>Rule of thumb: <b>for</b> when you're walking through items or a fixed count; <b>while</b> when you're waiting for something to happen.</p>
""", practice=["Collatz Steps", "Greatest Common Divisor", "Digital Root"])


@LD
def while_demo():
    n = 1234
    digits = 0
    while n > 0:
        n //= 10
        digits += 1
    print("digits:", digits)


LESSON("Core", "break, continue and loop-else", """
<ul>
<li><code>break</code> — leave the loop immediately.</li>
<li><code>continue</code> — skip the rest of this round and start the next one.</li>
<li><code>else</code> after a loop — runs only if the loop finished <b>without</b> a <code>break</code>. Handy for "search, and report if not found".</li>
</ul>
<pre><code class="py">for n in numbers:
    if n &lt; 0:
        continue          # ignore negatives
    if n == target:
        print("found")
        break             # stop searching
else:
    print("not found")    # only if no break happened</code></pre>
""", practice=["First Position of a Value", "Sum Skipping Negatives", "Is It Prime?", "Smallest Divisor"])


@LD
def break_continue_demo():
    numbers = [4, -2, 7, 9, 3]
    target = 9
    for n in numbers:
        if n < 0:
            continue
        if n == target:
            print("found", n)
            break
        print("checked", n)
    else:
        print("not found")


LESSON("Advanced", "Nested loops and patterns", """
<p>A loop inside a loop: the inner loop runs <b>completely</b> for every round of the outer loop. With outer size n and inner size m, the body runs n × m times.</p>
<pre><code class="py">for row in range(1, 4):
    line = ""
    for col in range(row):
        line += "*"
    print(line)
# *
# **
# ***</code></pre>
<p>Nested loops are used for grids, tables, comparing every pair, and printing patterns. Be careful with big inputs: two nested loops over 10,000 items is 100 million steps.</p>
""", practice=["Star Triangle", "Pairs With a Given Sum", "Primes Up To n"])


@LD
def nested_demo():
    for row in range(1, 4):
        line = ""
        for col in range(1, 4):
            line += str(row * col) + " "
        print(line)


LESSON("Advanced", "Pythonic looping", """
<p>Python has tools that remove index bookkeeping:</p>
<table>
<tr><th>Instead of</th><th>Write</th></tr>
<tr><td><code>for i in range(len(xs)): x = xs[i]</code></td><td><code>for x in xs:</code></td></tr>
<tr><td>a separate counter</td><td><code>for i, x in enumerate(xs):</code></td></tr>
<tr><td>indexing two lists</td><td><code>for a, b in zip(xs, ys):</code></td></tr>
<tr><td>looping backwards with indices</td><td><code>for x in reversed(xs):</code></td></tr>
<tr><td>loop + append</td><td><code>[f(x) for x in xs]</code> (comprehension)</td></tr>
<tr><td>loop + total</td><td><code>sum(...)</code>, <code>max(...)</code>, <code>any(...)</code>, <code>all(...)</code></td></tr>
</table>
<div class="warn">Don't add or remove items from a list while looping over it — loop over a copy (<code>for x in xs[:]</code>) or build a new list.</div>
""", practice=["Armstrong Number", "Fibonacci Sequence", "Perfect Number"])


@LD
def pythonic_demo():
    names = ["Ana", "Ben", "Cy"]
    scores = [88, 92, 79]
    for i, name in enumerate(names, start=1):
        print(i, name)
    for name, score in zip(names, scores):
        print(name, score)
    print(sum(scores), max(scores), any(s > 90 for s in scores))
