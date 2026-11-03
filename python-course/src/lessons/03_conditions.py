from lib import *

LESSON("Basics", "The if statement", """
<p>Until now every line ran. An <code>if</code> statement runs a block of code <b>only when a condition is True</b>:</p>
<pre><code class="py">temperature = 35
if temperature &gt; 30:
    print("It's hot!")      # runs only if the condition is True
print("Done")               # always runs</code></pre>
<ul>
<li>The condition is followed by a <b>colon</b> <code>:</code>.</li>
<li>The lines that belong to the if are <b>indented</b> (4 spaces). That indented group is called a <b>block</b>.</li>
<li>The first line that is not indented is outside the if.</li>
</ul>
<div class="warn">IndentationError and "expected ':'" are the two most common beginner errors here.</div>
""", practice=["Positive, Negative or Zero"])


@LD
def if_demo():
    temperature = 35
    if temperature > 30:
        print("It's hot!")
    temperature = 20
    if temperature > 30:
        print("This line is skipped")
    print("Done")


LESSON("Basics", "if / else and if / elif / else", """
<p><code>else</code> gives the block to run when the condition is False. <code>elif</code> ("else if") adds more choices:</p>
<pre><code class="py">if marks &gt;= 90:
    grade = "A"
elif marks &gt;= 75:
    grade = "B"
else:
    grade = "C"</code></pre>
<p>Python checks the conditions <b>from top to bottom</b> and runs only the <b>first</b> one that is True; the rest are skipped. That's why the order matters: put the strictest condition first.</p>
""", practice=["Grade From Marks", "Ticket Price by Age", "Greeting by Hour", "BMI Category"])


@LD
def elif_demo():
    for marks in [95, 80, 52]:
        if marks >= 90:
            grade = "A"
        elif marks >= 75:
            grade = "B"
        else:
            grade = "C"
        print(marks, "->", grade)


LESSON("Core", "Combining conditions and nesting", """
<p>Use <code>and</code>, <code>or</code>, <code>not</code> to combine conditions, or put one if inside another (<b>nesting</b>):</p>
<pre><code class="py">if age &gt;= 18 and has_id:          # combined
    print("Welcome")

if age &gt;= 18:                     # nested
    if has_id:
        print("Welcome")
    else:
        print("Show your ID")</code></pre>
<p>Combined conditions keep code flat; nesting is useful when the inner choice has its own else. More than two levels of nesting usually means you should restructure — e.g. return early.</p>
""", practice=["Quadrant of a Point", "Triangle Type", "Can It Be a Triangle?", "Days in a Month"])


@LD
def nested_demo():
    age = 20
    has_id = False
    if age >= 18:
        if has_id:
            print("Welcome in")
        else:
            print("Adult, but show your ID")
    else:
        print("Too young")
    can_enter = age >= 18 and has_id
    print("can_enter =", can_enter)


LESSON("Core", "One-line conditionals and truthiness", """
<p>A <b>conditional expression</b> picks one of two values in a single line:</p>
<pre><code class="py">label = "even" if n % 2 == 0 else "odd"</code></pre>
<p>Read it as: <i>value_if_true</i> <b>if</b> <i>condition</i> <b>else</b> <i>value_if_false</i>.</p>
<p>A condition doesn't have to be a comparison. Any value works: empty strings, empty lists, 0 and None count as False; everything else counts as True.</p>
<pre><code class="py">name = ""
if not name:
    print("Please enter a name")</code></pre>
""", practice=["Larger of Two", "Vowel or Consonant"])


@LD
def ternary_demo():
    for n in [4, 7]:
        label = "even" if n % 2 == 0 else "odd"
        print(n, label)
    cart = []
    if not cart:
        print("Your cart is empty")
    cart.append("pen")
    if cart:
        print("Items:", len(cart))


LESSON("Advanced", "match-case (structural pattern matching)", """
<p>Python 3.10 added <code>match</code>, which compares one value against several <b>patterns</b>:</p>
<pre><code class="py">match command:
    case "start":
        ...
    case "stop" | "quit":        # either value
        ...
    case ("move", x, y):         # a tuple; x and y are captured
        ...
    case _:                      # anything else (default)
        ...</code></pre>
<p>Cases can have <b>guards</b>: <code>case "/" if b != 0:</code>. Patterns can also match lists, dicts and objects. For a few simple equality checks, if/elif is just as good.</p>
""", practice=["Simple Calculator"])


@LD
def match_demo():
    def describe(cmd):
        match cmd:
            case "start":
                return "starting"
            case "stop" | "quit":
                return "stopping"
            case ("move", x, y):
                return f"moving to {x},{y}"
            case _:
                return "unknown"

    for c in ["start", "quit", ("move", 3, 4), "jump"]:
        print(describe(c))


LESSON("Advanced", "Replacing long if-chains with data", """
<p>When every branch just maps an input to an output, a <b>lookup table</b> (tuple, list or dict) is shorter, faster to change and less error-prone than many elif lines:</p>
<pre><code class="py">days = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
name = days[n - 1]

beats = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
winner = "p1" if beats[p1] == p2 else "p2"</code></pre>
<p>Another clean style is the <b>guard clause</b>: handle the special or invalid case first and <code>return</code> immediately, so the main logic isn't nested.</p>
""", practice=["Day Name", "Rock Paper Scissors", "Next Traffic Light", "Shopping Discount", "Electricity Bill"])


@LD
def lookup_demo():
    def tier_discount(amount):
        for threshold, percent in [(5000, 20), (2000, 10), (1000, 5)]:
            if amount >= threshold:
                return percent
        return 0

    print(tier_discount(2500), tier_discount(300))
