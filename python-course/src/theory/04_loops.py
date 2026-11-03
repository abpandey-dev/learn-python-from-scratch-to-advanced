from lib import *

THEORY("Definition", """
<p>A <b>loop</b> (iteration statement) repeatedly executes a block of code. Each execution of the block is one <b>iteration</b>. Loops are one of the three basic control structures, together with sequence and selection.</p>
<ul>
<li>A <b>definite loop</b> runs a known number of times or over a known collection — Python's <code>for</code>.</li>
<li>An <b>indefinite loop</b> runs until a condition becomes false — Python's <code>while</code>.</li>
</ul>
""")

THEORY("The for loop", """
<pre><code class="py">for variable in iterable:
    block</code></pre>
<p>An <b>iterable</b> is any object that can give its items one at a time: str, list, tuple, dict (its keys), set, range, files, generators. On each iteration the next item is assigned to the loop variable.</p>
<p>Under the hood: Python calls <code>iter(iterable)</code> to get an <b>iterator</b>, then calls <code>next()</code> on it until it raises <code>StopIteration</code>.</p>
<h4>range(start, stop, step)</h4>
<ul>
<li>Produces integers from start (default 0) up to but <b>not including</b> stop, adding step (default 1).</li>
<li>A negative step counts down: <code>range(10, 0, -2)</code> → 10 8 6 4 2.</li>
<li><code>range</code> is lazy — it doesn't build a list, so <code>range(10**9)</code> uses almost no memory.</li>
<li><code>len(range(a, b, s))</code> = ⌈(b − a) / s⌉ when positive.</li>
</ul>
""")

THEORY("The while loop", """
<pre><code class="py">while condition:
    block</code></pre>
<p>The condition is checked <b>before</b> every iteration (an <b>entry-controlled</b> loop). If it is False at the start, the block never runs. Python has no do-while; emulate it with <code>while True:</code> … <code>if not condition: break</code>.</p>
<p>A loop whose condition never becomes False is an <b>infinite loop</b>. Sometimes that's intentional (servers, games, <code>while True</code> with a <code>break</code>), usually it's a bug: the loop variable isn't updated.</p>
""")

THEORY("Loop control statements", """
<table>
<tr><th>Statement</th><th>Effect</th></tr>
<tr><td><code>break</code></td><td>exits the innermost loop immediately</td></tr>
<tr><td><code>continue</code></td><td>skips the rest of the current iteration</td></tr>
<tr><td><code>pass</code></td><td>does nothing (placeholder)</td></tr>
<tr><td><code>else</code> clause</td><td>runs after the loop ends normally — not after <code>break</code></td></tr>
<tr><td><code>return</code></td><td>inside a function, leaves the loop and the function</td></tr>
</table>
<p><code>break</code> only leaves one level of nested loops. To leave several, put the loops in a function and <code>return</code>, or use a flag.</p>
""")

THEORY("Common loop patterns", """
<table>
<tr><th>Pattern</th><th>Shape</th></tr>
<tr><td>Accumulate</td><td><code>total = 0; for x in xs: total += x</code></td></tr>
<tr><td>Count</td><td><code>count = 0; for x in xs: if cond: count += 1</code></td></tr>
<tr><td>Find max/min</td><td><code>best = xs[0]; for x in xs: if x &gt; best: best = x</code></td></tr>
<tr><td>Search</td><td><code>for x in xs: if x == t: break</code> (+ else)</td></tr>
<tr><td>Filter / transform</td><td><code>out = []; for x in xs: if cond: out.append(f(x))</code></td></tr>
<tr><td>Digit processing</td><td><code>while n: d = n % 10; n //= 10</code></td></tr>
<tr><td>Two-variable update</td><td><code>a, b = b, a + b</code> (Fibonacci, GCD)</td></tr>
<tr><td>Nested (pairs / grids)</td><td><code>for i in …: for j in …:</code></td></tr>
</table>
""")

THEORY("Loops and running time", """
<p>The cost of a loop is (number of iterations) × (cost of the body). This is the start of <b>time complexity</b>:</p>
<table>
<tr><th>Loop shape</th><th>Iterations</th><th>Big-O</th></tr>
<tr><td>one loop over n items</td><td>n</td><td>O(n)</td></tr>
<tr><td>two nested loops over n</td><td>n × n</td><td>O(n²)</td></tr>
<tr><td>loop that halves n each time</td><td>log₂ n</td><td>O(log n)</td></tr>
<tr><td>loop up to √n</td><td>√n</td><td>O(√n)</td></tr>
</table>
<p>Hidden loops count too: <code>x in list</code>, <code>list.index</code>, <code>sum</code>, slicing and string concatenation in a loop are all O(n) each.</p>
""")

FAQ("What is the difference between for and while loops?", "<p><code>for</code> iterates over the items of an iterable — use it when the sequence or count is known. <code>while</code> repeats as long as a condition is true — use it when you can't know the number of iterations in advance.</p>")
FAQ("What does the else clause on a loop do?", "<p>It runs once after the loop finishes normally (the iterable is exhausted or the while condition becomes false). It is skipped if the loop exits with <code>break</code>. It's useful for search loops: 'not found'.</p>")
FAQ("break vs continue vs pass?", "<p><code>break</code> exits the loop. <code>continue</code> jumps to the next iteration. <code>pass</code> does nothing and just fills a required spot in the syntax.</p>")
FAQ("Is range(5) a list?", "<p>No. It's a lazy range object that produces numbers on demand and uses constant memory. Use <code>list(range(5))</code> if you really need a list.</p>")
FAQ("Why is modifying a list while iterating over it a problem?", "<p>The iterator walks by index; removing items shifts later items left so some are skipped, and appending can make the loop run forever. Iterate over a copy or build a new list instead.</p>")
FAQ("Does Python have a do-while loop?", "<p>No. Use <code>while True:</code> with the body first and <code>if not condition: break</code> at the end.</p>")
FAQ("How do you loop with an index in Python?", "<p>Use <code>enumerate</code>: <code>for i, x in enumerate(items):</code>. Use <code>range(len(items))</code> only when you really need to modify by index.</p>")
