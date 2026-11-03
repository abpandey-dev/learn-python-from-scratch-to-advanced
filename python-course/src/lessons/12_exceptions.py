from lib import *

LESSON("Basics", "Errors are normal", """
<p>Programs meet bad situations: a user types "abc" where a number is expected, a file is missing, a list is shorter than you thought. Python reports these as <b>exceptions</b>. If nobody handles one, the program stops with a <b>traceback</b>:</p>
<pre><code class="py">Traceback (most recent call last):
  File "app.py", line 3, in &lt;module&gt;
    age = int(input("Age: "))
ValueError: invalid literal for int() with base 10: 'abc'</code></pre>
<p>Read a traceback from the <b>bottom</b>: the last line names the error type and message; the lines above show where it happened.</p>
<table>
<tr><th>Error</th><th>Typical cause</th></tr>
<tr><td><code>SyntaxError</code></td><td>code isn't valid Python (missing colon, bracket)</td></tr>
<tr><td><code>NameError</code></td><td>using a name that doesn't exist (typo)</td></tr>
<tr><td><code>TypeError</code></td><td>wrong type, e.g. <code>"5" + 3</code></td></tr>
<tr><td><code>ValueError</code></td><td>right type, bad value, e.g. <code>int("abc")</code></td></tr>
<tr><td><code>IndexError</code> / <code>KeyError</code></td><td>list index / dict key doesn't exist</td></tr>
<tr><td><code>ZeroDivisionError</code></td><td>dividing by zero</td></tr>
<tr><td><code>FileNotFoundError</code></td><td>opening a file that isn't there</td></tr>
<tr><td><code>AttributeError</code></td><td>object has no such attribute/method</td></tr>
</table>
""")


LESSON("Basics", "try and except", """
<p>Put risky code inside <code>try</code>. If an exception happens, Python jumps to a matching <code>except</code> block instead of crashing:</p>
<pre><code class="py">try:
    age = int(text)
except ValueError:
    age = 0
    print("Not a number, using 0")</code></pre>
<p>Catch <b>specific</b> exceptions. A bare <code>except:</code> also catches typos and Ctrl+C, hiding real bugs.</p>
<p>Two styles: <b>LBYL</b> ("look before you leap": check with if first) and <b>EAFP</b> ("easier to ask forgiveness than permission": just try it and handle the error). EAFP is the usual Python style.</p>
""", practice=["Safe Division", "Parse a Number or Use a Default", "Safe List Access", "Safe Dictionary Lookup", "Square Root of a Negative"])


@LD
def try_demo():
    results = []
    for text in ["42", "abc", "7"]:
        try:
            n = int(text)
            results.append(n)
        except ValueError:
            print("skipping", repr(text))
    print(results)


LESSON("Core", "else, finally and several excepts", """
<pre><code class="py">try:
    value = int(items[i])
except IndexError:
    print("no such position")
except ValueError as e:          # 'as e' gives you the exception object
    print("bad number:", e)
else:
    print("got", value)           # only when NO exception happened
finally:
    print("this always runs")     # clean-up: close files, release locks</code></pre>
<p>Order: try → (one matching except, or else) → finally. <code>finally</code> runs even if the try block returns or an unhandled error is on its way out.</p>
""", practice=["Several Kinds of Error", "Success Message With else", "Clean-up With finally", "Sum the Valid Numbers", "First Valid Attempt"])


@LD
def full_try_demo():
    log = []
    for value in [4, 0]:
        try:
            result = 100 / value
        except ZeroDivisionError as e:
            log.append(f"error: {e}")
        else:
            log.append(f"result {result}")
        finally:
            log.append("finished")
    print(log)


LESSON("Core", "Raising your own errors", """
<p>When your function gets input it can't handle, <b>raise</b> an exception instead of returning a strange value:</p>
<pre><code class="py">def set_age(age):
    if age &lt; 0:
        raise ValueError("age cannot be negative")</code></pre>
<p>You can define your own exception types by subclassing <code>Exception</code>:</p>
<pre><code class="py">class InsufficientFunds(Exception):
    pass

raise InsufficientFunds("balance too low")</code></pre>
<p>This separates <b>detecting</b> a problem (deep inside your logic) from <b>deciding what to do</b> about it (at the top, near the user).</p>
""", practice=["Validate an Age", "Custom Exception: Insufficient Funds"])


@LD
def raise_demo():
    class InsufficientFunds(Exception):
        pass

    def withdraw(balance, amount):
        if amount > balance:
            raise InsufficientFunds(f"need {amount - balance} more")
        return balance - amount

    try:
        left = withdraw(100, 30)
        left = withdraw(left, 500)
    except InsufficientFunds as e:
        print("Sorry:", e, "| balance still", left)


LESSON("Core", "Reading and writing files", """
<p><code>open(path, mode)</code> returns a file object. Always use it in a <code>with</code> block — the file is closed automatically, even if an error happens.</p>
<table>
<tr><th>Mode</th><th>Meaning</th></tr>
<tr><td><code>"r"</code></td><td>read text (default); error if missing</td></tr>
<tr><td><code>"w"</code></td><td>write text; creates or <b>empties</b> the file</td></tr>
<tr><td><code>"a"</code></td><td>append to the end</td></tr>
<tr><td><code>"x"</code></td><td>create; error if it exists</td></tr>
<tr><td><code>"b"</code> (add to others)</td><td>binary, e.g. <code>"rb"</code> for images</td></tr>
</table>
<pre><code class="py">with open("notes.txt", encoding="utf-8") as f:
    for line in f:                 # one line at a time — memory friendly
        print(line.rstrip("\\n"))

with open("out.txt", "w", encoding="utf-8") as f:
    f.write("first line\\n")</code></pre>
<p>Other reads: <code>f.read()</code> (everything as one string), <code>f.readline()</code>, <code>f.readlines()</code> (list of lines). The practice questions use <code>io.StringIO</code>, an in-memory file that behaves exactly like an open text file, so they can run anywhere.</p>
""", practice=["Count Lines in a File", "Words in a File", "Longest Line", "Write Lines, Read Them Back"])


@LD
def file_demo():
    import io
    fake_file = io.StringIO("apples 3\npears 5\nplums 2\n")
    total = 0
    with fake_file as f:
        for line in f:
            name, qty = line.split()
            total += int(qty)
    print("total fruit:", total)


LESSON("Advanced", "Context managers and structured data files", """
<p>A <b>context manager</b> is any object usable with <code>with</code>: it runs set-up code on entry (<code>__enter__</code>) and clean-up on exit (<code>__exit__</code>), even after an error. Files, locks and database connections are context managers. The easiest way to write your own:</p>
<pre><code class="py">from contextlib import contextmanager
@contextmanager
def timer():
    start = time.time()
    try:
        yield                      # the with-block runs here
    finally:
        print(time.time() - start)</code></pre>
<p>For structured files use the standard library instead of splitting by hand: <code>csv</code> for comma-separated data, <code>json</code> for JSON (<code>json.load</code>, <code>json.dump</code>, catching <code>json.JSONDecodeError</code>), and <code>pathlib.Path</code> for working with paths.</p>
""", practice=["Make Your Own Context Manager", "Totals From CSV", "Parse JSON Safely", "Read key=value Settings"])


@LD
def contextmanager_demo():
    from contextlib import contextmanager
    log = []

    @contextmanager
    def session(name):
        log.append("open " + name)
        try:
            yield name.upper()
        finally:
            log.append("close " + name)

    try:
        with session("db") as s:
            log.append("using " + s)
            raise RuntimeError("lost connection")
    except RuntimeError as e:
        log.append("handled: " + str(e))
    print(log)
