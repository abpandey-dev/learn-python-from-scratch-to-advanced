from lib import *

THEORY("Definitions", """
<ul>
<li>An <b>error</b> is a problem in a program. <b>Syntax errors</b> are detected before the program runs; everything else happens at run time.</li>
<li>An <b>exception</b> is an object that represents a run-time error. When one is <b>raised</b>, normal execution stops and Python looks for a handler up the call stack; if none is found, the program terminates and prints a <b>traceback</b>.</li>
<li><b>Exception handling</b> is catching an exception with <code>try</code>/<code>except</code> and responding to it so the program can continue or fail gracefully.</li>
</ul>
""")

THEORY("The exception hierarchy", """
<div class="pic">BaseException
 ├── SystemExit, KeyboardInterrupt, GeneratorExit
 └── Exception
      ├── ArithmeticError → ZeroDivisionError, OverflowError
      ├── LookupError → IndexError, KeyError
      ├── ValueError → UnicodeError …
      ├── TypeError
      ├── NameError → UnboundLocalError
      ├── AttributeError
      ├── OSError → FileNotFoundError, PermissionError …
      ├── ImportError → ModuleNotFoundError
      ├── RuntimeError → RecursionError, NotImplementedError
      └── StopIteration …</div>
<p>An <code>except</code> clause catches the named class and all its subclasses: <code>except LookupError</code> catches both IndexError and KeyError. Your own exceptions should inherit from <code>Exception</code>, not BaseException.</p>
""")

THEORY("try statement semantics", """
<table>
<tr><th>Clause</th><th>Runs when</th></tr>
<tr><td><code>try</code></td><td>always first</td></tr>
<tr><td><code>except E [as e]</code></td><td>an exception of type E (or a subclass) was raised in try; the first matching clause wins</td></tr>
<tr><td><code>else</code></td><td>try finished <b>without</b> an exception</td></tr>
<tr><td><code>finally</code></td><td>always, last — even after return, break or an unhandled exception</td></tr>
</table>
<ul>
<li>Put the most specific exception classes first.</li>
<li>Keep the try block small — only the statement that can fail.</li>
<li><code>raise</code> with no argument inside an except re-raises the current exception.</li>
<li><code>raise NewError(...) from e</code> chains exceptions so the original cause is kept.</li>
<li>Python 3.11+ adds <code>ExceptionGroup</code> and <code>except*</code> for multiple simultaneous errors.</li>
</ul>
""")

THEORY("Raising and custom exceptions", """
<pre><code class="py">raise ValueError("price must be positive")

class AppError(Exception):
    \"\"\"Base class for this application's errors.\"\"\"

class InsufficientFunds(AppError):
    def __init__(self, needed):
        super().__init__(f"need {needed} more")
        self.needed = needed</code></pre>
<p><code>assert condition, "message"</code> raises AssertionError when the condition is false. Use it for internal sanity checks, not for validating user input (asserts can be disabled with <code>python -O</code>).</p>
""")

THEORY("LBYL vs EAFP", """
<table>
<tr><th></th><th>LBYL (look before you leap)</th><th>EAFP (easier to ask forgiveness)</th></tr>
<tr><td>Style</td><td><code>if key in d: x = d[key]</code></td><td><code>try: x = d[key] except KeyError: …</code></td></tr>
<tr><td>Pros</td><td>explicit; no exception overhead when failures are common</td><td>no duplicated checks; avoids race conditions (file deleted between check and use)</td></tr>
<tr><td>Typical in</td><td>C, Java</td><td>Python</td></tr>
</table>
""")

THEORY("File handling", """
<table>
<tr><th>Task</th><th>Code</th></tr>
<tr><td>Open safely</td><td><code>with open(path, mode, encoding="utf-8") as f:</code></td></tr>
<tr><td>Read all</td><td><code>f.read()</code></td></tr>
<tr><td>Read lines lazily</td><td><code>for line in f:</code></td></tr>
<tr><td>List of lines</td><td><code>f.readlines()</code> or <code>f.read().splitlines()</code></td></tr>
<tr><td>Write</td><td><code>f.write(text)</code>, <code>f.writelines(lines)</code>, <code>print(x, file=f)</code></td></tr>
<tr><td>Modes</td><td>r, w, a, x, + (read/write), b (binary), t (text, default)</td></tr>
<tr><td>Paths</td><td><code>pathlib.Path("data") / "file.txt"</code>, <code>.exists()</code>, <code>.read_text()</code></td></tr>
<tr><td>CSV / JSON</td><td><code>csv.reader</code>, <code>csv.DictReader</code>; <code>json.load</code>, <code>json.dump</code></td></tr>
</table>
<p>A <b>context manager</b> implements <code>__enter__</code> and <code>__exit__</code>; <code>with</code> guarantees <code>__exit__</code> runs, so resources are released. Without <code>with</code>, you must call <code>f.close()</code> yourself (in a finally block).</p>
""")

FAQ("Error vs exception?", "<p>'Error' is the general term for a problem. Syntax errors stop the program before it runs. Exceptions are run-time error objects that can be caught and handled with try/except.</p>")
FAQ("What is the difference between except and finally?", "<p><code>except</code> runs only when a matching exception occurs. <code>finally</code> always runs, whether or not an exception occurred, and is used for clean-up.</p>")
FAQ("When does the else block of a try run?", "<p>Only when the try block completes without raising an exception. It keeps success code out of the try block so its errors aren't caught by mistake.</p>")
FAQ("Why is a bare <code>except:</code> bad?", "<p>It catches everything, including KeyboardInterrupt, SystemExit and bugs like NameError, which hides real problems. Catch specific exceptions, or at least <code>except Exception</code>.</p>")
FAQ("How do you create a custom exception?", "<p>Subclass Exception: <code>class MyError(Exception): pass</code>, then <code>raise MyError('message')</code>.</p>")
FAQ("Why use <code>with open(...)</code>?", "<p>The with statement closes the file automatically when the block ends, even if an exception occurs, preventing leaked file handles and unflushed data.</p>")
FAQ("What does <code>raise ... from e</code> do?", "<p>It raises a new exception while recording the original as its cause (<code>__cause__</code>), so the traceback shows both.</p>")
FAQ("raise vs assert?", "<p><code>raise</code> signals an error condition you expect could happen (bad input). <code>assert</code> checks something that should always be true if the code is correct; asserts can be turned off with -O.</p>")
