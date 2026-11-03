from lib import *

TOPIC(
    id="exceptions", title="Errors, Exceptions & Files", glyph="try:",
    blurb="Handle things that go wrong with try / except / else / finally, raise your own errors, and read and write files safely.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">try:
    n = int(text)
except ValueError:            # handle one kind of error
    n = 0
except (TypeError, KeyError) as e:
    print("problem:", e)
else:                         # runs only if no exception happened
    print("parsed", n)
finally:                      # always runs (clean-up)
    print("done")

raise ValueError("age must be positive")
class InsufficientFunds(Exception): pass

with open("notes.txt") as f:  # file closes automatically
    for line in f: ...
with open("out.txt", "w") as f:
    f.write("hello\\n")</code></pre>
""")


def F(text):
    import io
    return io.StringIO(text)


Q(None, "Safe Division", "Easy", "ZeroDivisionError",
  "Return a / b, or None if b is zero.",
  [((10, 2), 5.0), ((1, 0), None), ((-9, 3), -3.0)],
  ("Look before you leap (LBYL): check b before dividing.", "O(1)", "O(1)"),
  ("Easier to ask forgiveness (EAFP): try the division and catch <code>ZeroDivisionError</code>.", "O(1)", "O(1)"),
  viz=(1, 0))


@B
def safe_divide(a, b):
    if b == 0:
        return None
    return a / b


@O
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


Q(None, "Parse a Number or Use a Default", "Easy", "ValueError",
  "Convert <code>text</code> to an int; if it isn't a valid integer return <code>default</code>.",
  [(("42", 0), 42), (("4x", -1), -1), ((" -7 ", 0), -7), (("", 5), 5)],
  ("Check the characters yourself (strip, optional sign, all digits).", "O(n)", "O(1)"),
  ("Just call <code>int()</code> and catch <code>ValueError</code> — int already knows every rule.", "O(n)", "O(1)"),
  viz=("4x", -1))


@B
def to_int(text, default):
    t = text.strip()
    if t.startswith("-") or t.startswith("+"):
        digits = t[1:]
    else:
        digits = t
    if digits == "" or not digits.isdigit():
        return default
    return int(t)


@O
def to_int(text, default):
    try:
        return int(text)
    except ValueError:
        return default


Q(None, "Safe List Access", "Easy", "IndexError",
  "Return <code>items[i]</code>, or <code>default</code> if i is out of range.",
  [(([1, 2, 3], 1, None), 2), (([1, 2, 3], 9, "none"), "none"), (([1, 2, 3], -1, 0), 3)],
  ("Check the index range (including negative indices) first.", "O(1)", "O(1)"),
  ("Try the index and catch <code>IndexError</code>.", "O(1)", "O(1)"))


@B
def item_or(items, i, default):
    if -len(items) <= i < len(items):
        return items[i]
    return default


@O
def item_or(items, i, default):
    try:
        return items[i]
    except IndexError:
        return default


Q(None, "Safe Dictionary Lookup", "Easy", "KeyError",
  "Return the phone number for <code>name</code>, or 'unknown' if the name isn't in the book.",
  [(({"ana": "123", "ben": "456"}, "ben"), "456"), (({"ana": "123"}, "cy"), "unknown")],
  ("Catch <code>KeyError</code> around the lookup.", "O(1)", "O(1)"),
  ("For a simple default, <code>dict.get</code> is clearer than any exception handling.", "O(1)", "O(1)"))


@B
def phone_of(book, name):
    try:
        return book[name]
    except KeyError:
        return "unknown"


@O
def phone_of(book, name):
    return book.get(name, "unknown")


Q(None, "Sum the Valid Numbers", "Medium", "Skipping bad input",
  "Given strings, return the sum of those that are valid numbers (ints or floats) and how many were skipped: <code>(total, skipped)</code>.",
  [((["3", "x", "2.5", "", "-1"],), (4.5, 2)), (([],), (0, 0))],
  ("A hand-written validity check for every string before converting.", "O(n · L)", "O(1)"),
  ("Try <code>float()</code> on each and count the <code>ValueError</code>s.", "O(n · L)", "O(1)"),
  viz=(["3", "x", "2.5"],))


@B
def sum_valid(texts):
    total, skipped = 0, 0
    for t in texts:
        body = t[1:] if t[:1] in "+-" else t
        if body.replace(".", "", 1).isdigit():
            total += float(t)
        else:
            skipped += 1
    return total, skipped


@O
def sum_valid(texts):
    total, skipped = 0, 0
    for t in texts:
        try:
            total += float(t)
        except ValueError:
            skipped += 1
    return total, skipped


Q(None, "Validate an Age", "Medium", "raise and except",
  "Return 'ok' for an age 0–150, otherwise the error message: 'age must be a number', 'age cannot be negative' or 'age is unrealistic'.",
  [((25,), "ok"), (("x",), "age must be a number"), ((-3,), "age cannot be negative"), ((200,), "age is unrealistic")],
  ("Return a message from each if branch.", "O(1)", "O(1)"),
  ("A checker <b>raises</b> ValueError with the message; the caller catches it and reads <code>str(e)</code>. This separates detecting a problem from deciding what to do about it.", "O(1)", "O(1)"))


@B
def check_age(age):
    if not isinstance(age, (int, float)):
        return "age must be a number"
    if age < 0:
        return "age cannot be negative"
    if age > 150:
        return "age is unrealistic"
    return "ok"


@O
def check_age(age):
    def validate(a):
        if not isinstance(a, (int, float)):
            raise TypeError("age must be a number")
        if a < 0:
            raise ValueError("age cannot be negative")
        if a > 150:
            raise ValueError("age is unrealistic")

    try:
        validate(age)
    except (TypeError, ValueError) as e:
        return str(e)
    return "ok"


Q(None, "Custom Exception: Insufficient Funds", "Medium", "Defining exceptions",
  "Withdraw <code>amount</code> from <code>balance</code>: return the new balance, or 'insufficient funds' / 'invalid amount' (amount ≤ 0).",
  [((100, 30), 70), ((100, 300), "insufficient funds"), ((100, 0), "invalid amount")],
  ("Return special strings straight from the withdraw logic.", "O(1)", "O(1)"),
  ("Define <code>class InsufficientFunds(Exception)</code>; raise it in the logic and catch it at the edge.", "O(1)", "O(1)"))


@B
def withdraw(balance, amount):
    if amount <= 0:
        return "invalid amount"
    if amount > balance:
        return "insufficient funds"
    return balance - amount


@O
def withdraw(balance, amount):
    class InsufficientFunds(Exception):
        pass

    def take(bal, amt):
        if amt <= 0:
            raise ValueError("invalid amount")
        if amt > bal:
            raise InsufficientFunds("insufficient funds")
        return bal - amt

    try:
        return take(balance, amount)
    except (InsufficientFunds, ValueError) as e:
        return str(e)


Q(None, "Clean-up With finally", "Medium", "finally",
  "Simulate opening a resource, processing <code>value</code> (dividing 100 by it) and closing. Return the log, e.g. ['open', 'result 50.0', 'close'] or ['open', 'error', 'close'] — 'close' must always happen.",
  [((2,), ["open", "result 50.0", "close"]), ((0,), ["open", "error", "close"])],
  ("Write 'close' in every branch by hand (easy to forget one).", "O(1)", "O(1)"),
  ("<code>finally</code> runs no matter what — success, error or return.", "O(1)", "O(1)"),
  viz=(0,))


@B
def with_cleanup(value):
    log = ["open"]
    if value == 0:
        log.append("error")
        log.append("close")
        return log
    log.append(f"result {100 / value}")
    log.append("close")
    return log


@O
def with_cleanup(value):
    log = ["open"]
    try:
        log.append(f"result {100 / value}")
    except ZeroDivisionError:
        log.append("error")
    finally:
        log.append("close")
    return log


Q(None, "Success Message With else", "Easy", "try / except / else",
  "Return 'got N' if text is an integer N, else 'bad input'.",
  [(("12",), "got 12"), (("1.5",), "bad input")],
  ("Put the success code inside try as well.", "O(1)", "O(1)"),
  ("Keep only the risky call in <code>try</code>; success code goes in <code>else</code>, so its own errors aren't accidentally caught.", "O(1)", "O(1)"))


@B
def describe_input(text):
    try:
        n = int(text)
        message = "got " + str(n)
        return message
    except ValueError:
        return "bad input"


@O
def describe_input(text):
    try:
        n = int(text)
    except ValueError:
        return "bad input"
    else:
        return f"got {n}"


Q(None, "First Valid Attempt", "Medium", "Retry loop",
  "A user typed several attempts. Return <code>(number, attempts_used)</code> for the first valid integer, or <code>(None, len(attempts))</code>.",
  [((["abc", "", "7", "9"],), (7, 3)), ((["x"],), (None, 1))],
  ("Validate each attempt by hand with string checks.", "O(n · L)", "O(1)"),
  ("Loop over the attempts with <code>enumerate</code>; return from inside <code>try</code> on success.", "O(n · L)", "O(1)"),
  viz=(["abc", "", "7"],))


@B
def first_valid(attempts):
    count = 0
    for a in attempts:
        count += 1
        s = a.strip()
        if s and (s.isdigit() or (s[0] == "-" and s[1:].isdigit())):
            return int(s), count
    return None, count


@O
def first_valid(attempts):
    for used, a in enumerate(attempts, start=1):
        try:
            return int(a), used
        except ValueError:
            continue
    return None, len(attempts)


Q(None, "Several Kinds of Error", "Medium", "Multiple except blocks",
  "Return <code>int(items[i])</code>, or 'missing' if i is out of range, or 'not a number' if the item can't be converted.",
  [((["5", "x"], 0), 5), ((["5", "x"], 1), "not a number"), ((["5"], 4), "missing")],
  ("Check the index, then check the text, each with its own if.", "O(L)", "O(1)"),
  ("One try with two <code>except</code> blocks, one per error type.", "O(L)", "O(1)"))


@B
def item_as_int(items, i):
    if i >= len(items) or i < -len(items):
        return "missing"
    text = items[i].strip()
    if not text.lstrip("-").isdigit():
        return "not a number"
    return int(text)


@O
def item_as_int(items, i):
    try:
        return int(items[i])
    except IndexError:
        return "missing"
    except ValueError:
        return "not a number"


Q(None, "Square Root of a Negative", "Easy", "Raising errors",
  "Return the square root rounded to 3 decimals, or the message 'negative input' — the optimal answer raises and catches ValueError.",
  [((16,), 4.0), ((2,), 1.414), ((-4,), "negative input")],
  ("Return the message from an if branch.", "O(1)", "O(1)"),
  ("<code>math.sqrt</code> already raises ValueError for negatives; catch it.", "O(1)", "O(1)"))


@B
def root(x):
    if x < 0:
        return "negative input"
    return round(x ** 0.5, 3)


@O
def root(x):
    import math
    try:
        return round(math.sqrt(x), 3)
    except ValueError:
        return "negative input"


Q(None, "Count Lines in a File", "Easy", "Iterating a file",
  "<code>text</code> is the content of a file. Count its lines (simulated with io.StringIO, which behaves like an open file).",
  [(("a\nb\nc\n",), 3), (("",), 0), (("one line",), 1)],
  ("Read every line into a list with <code>readlines()</code> and take its length.", "O(n)", "O(n)"),
  ("Iterate the file object directly — one line at a time, no list in memory.", "O(n)", "O(1)"))


@B
def count_lines(text):
    f = F(text)
    lines = f.readlines()
    f.close()
    return len(lines)


@O
def count_lines(text):
    with F(text) as f:
        return sum(1 for _ in f)


Q(None, "Words in a File", "Easy", "Reading text",
  "Return the number of words in the file content.",
  [(("hello world\nhow are you\n",), 5), (("",), 0)],
  ("Read line by line and split each line, adding the counts.", "O(n)", "O(line)"),
  ("Read the whole file and split once.", "O(n)", "O(n)"))


@B
def words_in_file(text):
    count = 0
    f = F(text)
    for line in f:
        count += len(line.split())
    f.close()
    return count


@O
def words_in_file(text):
    with F(text) as f:
        return len(f.read().split())


Q(None, "Totals From CSV", "Medium", "csv module",
  "The file has lines 'name,amount'. Return the total amount per name, skipping lines whose amount isn't a number.",
  [(("ana,10\nben,5\nana,2.5\ncy,oops\n",), {"ana": 12.5, "ben": 5.0}), (("",), {})],
  ("Split each line on ',' by hand.", "O(n)", "O(k)"),
  ("<code>csv.reader</code> handles quoting and commas; <code>try/except</code> skips bad amounts.", "O(n)", "O(k)"),
  viz=("ana,10\nben,x\nana,2\n",))


@B
def csv_totals(text):
    totals = {}
    for line in text.split("\n"):
        if line == "":
            continue
        parts = line.split(",")
        name, amount = parts[0], parts[1]
        if amount.replace(".", "", 1).isdigit():
            totals[name] = totals.get(name, 0) + float(amount)
    return totals


@O
def csv_totals(text):
    import csv
    totals = {}
    with F(text) as f:
        for name, amount in csv.reader(f):
            try:
                totals[name] = totals.get(name, 0) + float(amount)
            except ValueError:
                continue
    return totals


Q(None, "Write Lines, Read Them Back", "Easy", "Writing files",
  "Write each item on its own line to a (simulated) file, then return the file's full content.",
  [((["a", "b"],), "a\nb\n"), (([],), "")],
  ("Call <code>write</code> twice per item (text, then newline).", "O(n)", "O(n)"),
  ("<code>writelines</code> with a generator, inside a <code>with</code> block.", "O(n)", "O(n)"))


@B
def write_lines(items):
    import io
    f = io.StringIO()
    for item in items:
        f.write(item)
        f.write("\n")
    content = f.getvalue()
    f.close()
    return content


@O
def write_lines(items):
    import io
    with io.StringIO() as f:
        f.writelines(f"{item}\n" for item in items)
        return f.getvalue()


Q(None, "Longest Line", "Easy", "max over a file",
  "Return the longest line of the file without its newline ('' for an empty file).",
  [(("hi\nhello\nhey\n",), "hello"), (("",), "")],
  ("Track the longest while reading line by line.", "O(n)", "O(line)"),
  ("<code>max</code> over the stripped lines with <code>key=len</code> and a default.", "O(n)", "O(line)"))


@B
def longest_line(text):
    best = ""
    f = F(text)
    for line in f:
        line = line.rstrip("\n")
        if len(line) > len(best):
            best = line
    f.close()
    return best


@O
def longest_line(text):
    with F(text) as f:
        return max((line.rstrip("\n") for line in f), key=len, default="")


Q(None, "Make Your Own Context Manager", "Hard", "__enter__ / __exit__",
  "Return the log of entering, doing the work and leaving a 'session', where leaving must happen even if the work fails: e.g. ['enter', 'work ok', 'exit'] or ['enter', 'exit', 'handled'].",
  [((False,), ["enter", "work ok", "exit"]), ((True,), ["enter", "exit", "handled"])],
  ("try/finally written out by hand around the work.", "O(1)", "O(1)"),
  ("<code>contextlib.contextmanager</code> turns a generator into a <code>with</code>-able object; the code after <code>yield</code> always runs.", "O(1)", "O(1)"),
  viz=(True,))


@B
def session_log(fail):
    log = ["enter"]
    try:
        try:
            if fail:
                raise RuntimeError("boom")
            log.append("work ok")
        finally:
            log.append("exit")
    except RuntimeError:
        log.append("handled")
    return log


@O
def session_log(fail):
    from contextlib import contextmanager
    log = []

    @contextmanager
    def session():
        log.append("enter")
        try:
            yield
        finally:
            log.append("exit")

    try:
        with session():
            if fail:
                raise RuntimeError("boom")
            log.append("work ok")
    except RuntimeError:
        log.append("handled")
    return log


Q(None, "Read key=value Settings", "Medium", "Unpacking errors",
  "Parse lines like 'port=8080' into a dict, skipping blank lines, comments (#) and malformed lines.",
  [(("port=8080\n# note\nbad line\nhost=local\n\n",), {"port": "8080", "host": "local"}), (("",), {})],
  ("Check for '=' and comments with ifs, then split.", "O(n)", "O(k)"),
  ("<code>partition('=')</code> splits once; skip lines where the separator is missing.", "O(n)", "O(k)"))


@B
def read_settings(text):
    result = {}
    for line in text.split("\n"):
        line = line.strip()
        if line == "" or line[0] == "#":
            continue
        if "=" not in line:
            continue
        index = line.index("=")
        result[line[:index].strip()] = line[index + 1:].strip()
    return result


@O
def read_settings(text):
    result = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition("=")
        if sep:
            result[key.strip()] = value.strip()
    return result


Q(None, "Parse JSON Safely", "Medium", "json + JSONDecodeError",
  "Parse a JSON text and return its 'name' field, or 'invalid json' / 'no name'.",
  [(('{"name": "Ana", "age": 21}',), "Ana"), (('{"age": 21}',), "no name"), (("{oops",), "invalid json")],
  ("Check that the text looks like an object, then parse it.", "O(n)", "O(n)"),
  ("Let <code>json.loads</code> decide and catch <code>json.JSONDecodeError</code>; <code>dict.get</code> handles the missing key.", "O(n)", "O(n)"))


@B
def json_name(text):
    import json
    t = text.strip()
    if not (t.startswith("{") and t.endswith("}")):
        return "invalid json"
    data = json.loads(t)
    if "name" in data:
        return data["name"]
    return "no name"


@O
def json_name(text):
    import json
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return "invalid json"
    return data.get("name", "no name")
