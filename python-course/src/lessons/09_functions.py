from lib import *

LESSON("Basics", "Why functions?", """
<p>A <b>function</b> is a named block of code you can run whenever you need it. It lets you write something once and reuse it, give a clear name to a step, and test pieces separately.</p>
<pre><code class="py">def greet(name):            # define: def + name + (parameters) + colon
    message = "Hi " + name  # the indented body
    return message          # send a value back

text = greet("Ana")         # call: run the body with name = "Ana"
print(text)</code></pre>
<p>Defining a function doesn't run it. The body runs only when you <b>call</b> it. In the animation, watch the <b>call stack</b> appear when <code>greet</code> starts and disappear when it returns.</p>
""", practice=["Circle Area (return, don't print)"])


@LD
def why_demo():
    def greet(name):
        message = "Hi " + name
        return message

    first = greet("Ana")
    second = greet("Ben")
    print(first, "|", second)


LESSON("Basics", "Parameters, arguments and return", """
<p><b>Parameters</b> are the names in the definition; <b>arguments</b> are the values you pass in a call.</p>
<ul>
<li><b>Positional</b>: matched by order — <code>area(3, 4)</code>.</li>
<li><b>Keyword</b>: matched by name — <code>area(h=4, w=3)</code>.</li>
<li><b>Default values</b>: <code>def area(w, h=1)</code> makes h optional.</li>
</ul>
<p><code>return</code> ends the function and sends a value back. A function without <code>return</code> (or with a bare <code>return</code>) gives back <code>None</code>. Return several values as a tuple: <code>return lo, hi</code>.</p>
<div class="warn"><code>print</code> shows a value; <code>return</code> hands it back to the caller. A function that only prints can't be used in a calculation.</div>
""", practice=["Greeting With a Default", "Validate an Order"])


@LD
def params_demo():
    def area(w, h=1):
        return w * h

    def shout(text):
        print(text.upper())

    a = area(3)
    b = area(3, 4)
    c = area(h=5, w=2)
    result = shout("hello")
    print(a, b, c, result)


LESSON("Core", "Flexible arguments: *args and **kwargs", """
<pre><code class="py">def total(*nums):            # nums is a tuple of all positional args
    return sum(nums)
total(1, 2, 3)

def profile(**info):         # info is a dict of all keyword args
    return info
profile(name="Ana", age=21)

def f(a, b=2, *args, key=None, **kwargs): ...   # the full order</code></pre>
<p>The stars also work in calls: <code>total(*my_list)</code> spreads a list into arguments and <code>profile(**my_dict)</code> spreads a dict into keyword arguments.</p>
""", practice=["Sum Any Number of Values", "Keyword Arguments to Text"])


@LD
def args_demo():
    def total(*nums):
        return sum(nums)

    def profile(**info):
        return ", ".join(f"{k}={v}" for k, v in info.items())

    values = [4, 5, 6]
    print(total(1, 2), total(*values))
    print(profile(name="Ana", city="Pune"))


LESSON("Core", "Scope: where variables live", """
<p>Variables created inside a function are <b>local</b>: they exist only while the function runs and are invisible outside. Variables created at the top of a file are <b>global</b>.</p>
<p>Python looks up a name in this order — <b>LEGB</b>: <b>L</b>ocal → <b>E</b>nclosing function → <b>G</b>lobal → <b>B</b>uilt-in.</p>
<pre><code class="py">count = 0
def bump():
    global count    # needed to ASSIGN to a global inside a function
    count += 1</code></pre>
<p>Prefer passing values in and returning results over using <code>global</code>. <code>nonlocal</code> does the same for a variable of an enclosing function.</p>
""")


@LD
def scope_demo():
    def outer():
        x = "enclosing"

        def inner():
            y = "local"
            return x + " + " + y

        return inner()

    result = outer()
    print(result)


LESSON("Core", "Functions are values: lambda, map, closures", """
<p>A function is an object like any other: you can store it in a variable, put it in a dict, or pass it to another function.</p>
<pre><code class="py">square = lambda x: x * x            # a small unnamed function
sorted(words, key=len)              # pass a function as an argument
list(map(square, [1, 2, 3]))        # [1, 4, 9]
ops = {"double": lambda x: 2 * x}   # functions in a dict</code></pre>
<p>A <b>closure</b> is an inner function that remembers variables of the function that created it:</p>
<pre><code class="py">def make_multiplier(k):
    def times(x):
        return x * k       # k is remembered
    return times
triple = make_multiplier(3)
triple(5)                  # 15</code></pre>
""", practice=["Apply an Operation by Name", "Scale With a Closure", "Sort by Last Letter"])


@LD
def closure_demo():
    def make_multiplier(k):
        def times(x):
            return x * k
        return times

    triple = make_multiplier(3)
    double = make_multiplier(2)
    print(triple(5), double(5), sorted(["kiwi", "fig", "banana"], key=len))


LESSON("Advanced", "Recursion", """
<p>A <b>recursive</b> function calls itself on a smaller problem. Every recursive function needs:</p>
<ol>
<li>a <b>base case</b> that answers directly (stops the recursion), and</li>
<li>a <b>recursive case</b> that moves toward the base case.</li>
</ol>
<pre><code class="py">def factorial(n):
    if n &lt;= 1:                   # base case
        return 1
    return n * factorial(n - 1)  # smaller problem</code></pre>
<p>Watch the call stack in the animation: each call waits for the one above it, then they return one by one. Python's default limit is about 1000 nested calls (<code>RecursionError</code>).</p>
""", practice=["Factorial with Recursion", "Sum of Digits, Recursively", "Reverse a String, Recursively", "Palindrome, Recursively", "Countdown List, Recursively", "GCD, Recursively", "Binary String, Recursively"])


@LD
def recursion_demo():
    def factorial(n):
        if n <= 1:
            return 1
        return n * factorial(n - 1)

    print(factorial(4))


LESSON("Advanced", "Making recursion fast: memoisation", """
<p>Some recursions solve the same sub-problem many times. <code>fib(5)</code> calls <code>fib(3)</code> twice and <code>fib(2)</code> three times; for <code>fib(40)</code> it's hundreds of millions of calls.</p>
<p><b>Memoisation</b> stores each answer the first time and reuses it:</p>
<pre><code class="py">from functools import lru_cache

@lru_cache(maxsize=None)     # a decorator that adds a cache
def fib(n):
    return n if n &lt; 2 else fib(n - 1) + fib(n - 2)</code></pre>
<p>This turns exponential time into linear time. It is the bridge to <b>dynamic programming</b>, covered in the DSA handbook.</p>
""", practice=["n-th Fibonacci Number", "Climbing Stairs", "Fast Power", "Tower of Hanoi Moves", "Flatten Any Depth"])


@LD
def memo_demo():
    memo = {}

    def fib(n):
        if n < 2:
            return n
        if n not in memo:
            memo[n] = fib(n - 1) + fib(n - 2)
        return memo[n]

    print(fib(6), memo)
