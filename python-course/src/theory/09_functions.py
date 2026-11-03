from lib import *

THEORY("Definition", """
<p>A <b>function</b> is a named, reusable block of code that performs a specific task. It may take inputs (<b>parameters</b>) and may produce an output (<b>return value</b>).</p>
<ul>
<li><b>Built-in functions</b>: provided by Python — <code>print, len, sum, max, sorted, range, input</code> …</li>
<li><b>User-defined functions</b>: created with <code>def</code> (or <code>lambda</code>).</li>
<li><b>Methods</b>: functions that belong to an object — <code>"hi".upper()</code>.</li>
</ul>
<p>Benefits: <b>reuse</b> (write once), <b>abstraction</b> (hide details behind a name), <b>modularity</b> (split a program into parts), easier <b>testing</b> and <b>debugging</b>.</p>
""")

THEORY("Anatomy of a function", """
<pre><code class="py">def name(param1, param2=default) -&gt; ReturnType:   # header (signature)
    \"\"\"Docstring: what the function does.\"\"\"
    body                                          # indented statements
    return value                                  # optional</code></pre>
<ul>
<li><b>def</b> creates a function object and binds it to the name.</li>
<li>The <b>docstring</b> is available as <code>name.__doc__</code> and through <code>help(name)</code>.</li>
<li><b>Type hints</b> (<code>x: int</code>, <code>-&gt; str</code>) document types; Python does not enforce them at run time.</li>
<li>A function with no <code>return</code> returns <code>None</code>.</li>
</ul>
""")

THEORY("Parameters and arguments", """
<table>
<tr><th>Kind</th><th>Definition</th><th>Call</th></tr>
<tr><td>Positional</td><td><code>def f(a, b)</code></td><td><code>f(1, 2)</code></td></tr>
<tr><td>Keyword</td><td>same</td><td><code>f(b=2, a=1)</code></td></tr>
<tr><td>Default</td><td><code>def f(a, b=10)</code></td><td><code>f(1)</code></td></tr>
<tr><td>Variable positional</td><td><code>def f(*args)</code></td><td><code>f(1, 2, 3)</code> → args is a tuple</td></tr>
<tr><td>Variable keyword</td><td><code>def f(**kwargs)</code></td><td><code>f(x=1)</code> → kwargs is a dict</td></tr>
<tr><td>Keyword-only</td><td><code>def f(a, *, key)</code></td><td><code>f(1, key=2)</code></td></tr>
<tr><td>Positional-only</td><td><code>def f(a, /, b)</code></td><td><code>f(1, 2)</code> or <code>f(1, b=2)</code></td></tr>
</table>
<p>Order in a definition: positional-only, <code>/</code>, normal, <code>*args</code> (or <code>*</code>), keyword-only, <code>**kwargs</code>.</p>
<p><b>Argument passing</b>: Python passes <b>object references</b> ("call by sharing"). A function can mutate a mutable argument (a list), but reassigning the parameter doesn't affect the caller's variable.</p>
<p><b>Default values are evaluated once</b>, when the function is defined. A mutable default (<code>def f(x=[])</code>) is shared between calls — use <code>None</code> and create the list inside.</p>
""")

THEORY("Scope and namespaces", """
<p>A <b>namespace</b> maps names to objects. Scope decides which namespace a name is looked up in, following <b>LEGB</b>:</p>
<table>
<tr><th>Scope</th><th>Where</th></tr>
<tr><td><b>L</b>ocal</td><td>inside the current function</td></tr>
<tr><td><b>E</b>nclosing</td><td>inside any outer function (for nested functions)</td></tr>
<tr><td><b>G</b>lobal</td><td>top level of the module</td></tr>
<tr><td><b>B</b>uilt-in</td><td>Python's built-ins (<code>len</code>, <code>print</code> …)</td></tr>
</table>
<p>Assigning to a name inside a function makes it local unless declared <code>global</code> (module level) or <code>nonlocal</code> (enclosing function). Reading an outer name needs no declaration.</p>
""")

THEORY("First-class functions, lambdas, closures, decorators", """
<ul>
<li><b>First-class</b>: functions can be assigned, passed as arguments, returned and stored in data structures.</li>
<li><b>Higher-order function</b>: takes or returns a function — <code>map</code>, <code>filter</code>, <code>sorted(key=…)</code>.</li>
<li><b>Lambda</b>: <code>lambda params: expression</code> — an anonymous function limited to one expression.</li>
<li><b>Closure</b>: an inner function that remembers variables from its enclosing scope after the outer function has returned.</li>
<li><b>Decorator</b>: a function that takes a function and returns a new one, applied with <code>@decorator</code> above a definition. Examples: <code>@lru_cache</code>, <code>@property</code>, <code>@staticmethod</code>.</li>
</ul>
""")

THEORY("Recursion", """
<p><b>Recursion</b> is when a function calls itself. It needs a <b>base case</b> and a <b>recursive case</b> that progresses toward it.</p>
<ul>
<li>Each call gets its own <b>stack frame</b> (local variables). Depth is limited (<code>sys.getrecursionlimit()</code>, default 1000) → <code>RecursionError</code>.</li>
<li>Any recursion can be rewritten as a loop with an explicit stack; Python has no tail-call optimisation.</li>
<li>Running time is found with a recurrence: T(n) = T(n − 1) + O(1) → O(n); T(n) = 2T(n − 1) + O(1) → O(2ⁿ); T(n) = T(n/2) + O(1) → O(log n).</li>
<li><b>Memoisation</b> caches results of a pure recursive function so repeated sub-problems are computed once.</li>
</ul>
<p>Recursion fits naturally when the data is recursive: nested lists, trees, folders, expressions, divide and conquer.</p>
""")

FAQ("Parameter vs argument?", "<p>A parameter is the variable name in the function definition; an argument is the actual value passed when calling it.</p>")
FAQ("What does a function return if there is no return statement?", "<p><code>None</code>.</p>")
FAQ("What are *args and **kwargs?", "<p><code>*args</code> collects extra positional arguments into a tuple; <code>**kwargs</code> collects extra keyword arguments into a dict. The names are conventions; the stars matter.</p>")
FAQ("Why is <code>def f(x, items=[])</code> dangerous?", "<p>Default values are created once, when the function is defined, so every call shares the same list and changes accumulate. Use <code>items=None</code> and create a new list inside.</p>")
FAQ("Is Python pass-by-value or pass-by-reference?", "<p>Neither exactly — it's 'pass by object reference'. The function receives a reference to the same object: mutating a list affects the caller, but rebinding the parameter name does not.</p>")
FAQ("What is a lambda and when should you use it?", "<p>An anonymous one-expression function, e.g. <code>lambda x: x * 2</code>. Use it for short throwaway functions such as sort keys; use <code>def</code> for anything longer or reused.</p>")
FAQ("What is a closure?", "<p>A nested function that captures variables from its enclosing function's scope, keeping them alive after the outer function returns — e.g. a multiplier factory.</p>")
FAQ("What is the LEGB rule?", "<p>The order Python searches for a name: Local, Enclosing, Global, Built-in.</p>")
FAQ("Recursion vs iteration?", "<p>Recursion expresses self-similar problems elegantly but uses a stack frame per call and is limited in depth. Iteration uses constant stack space and is usually faster. Both can solve the same problems.</p>")
