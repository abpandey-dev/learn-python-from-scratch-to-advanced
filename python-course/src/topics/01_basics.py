from lib import *

TOPIC(
    id="basics", title="Python Basics", glyph="x = 5",
    blurb="Your first programs: print, variables, data types, type conversion and input.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">print("Hello")            # show text
name = "Asha"             # create a variable (a name for a value)
age = 21                  # int      (whole number)
height = 1.62             # float    (decimal number)
is_student = True         # bool     (True / False)
nothing = None            # NoneType (no value)
type(age)                 # &lt;class 'int'&gt;
int("42"), float("3.5"), str(10), bool(0)   # conversions
x = input("Your name: ")  # input always gives a str
print(f"{name} is {age}") # f-string: values inside text</code></pre>
<h3>Rules for variable names</h3>
<ul>
<li>Letters, digits and <code>_</code> only; cannot start with a digit.</li>
<li>Case-sensitive: <code>age</code> and <code>Age</code> are different.</li>
<li>Can't be a keyword (<code>if</code>, <code>for</code>, <code>class</code> …).</li>
<li>Style: <code>snake_case</code> for variables and functions.</li>
</ul>
<h3>Common mistakes</h3>
<ul>
<li><code>"5" + 3</code> → TypeError. Convert first: <code>int("5") + 3</code>.</li>
<li>Forgetting that <code>input()</code> returns text.</li>
<li>Using <code>=</code> (assign) when you mean <code>==</code> (compare).</li>
</ul>
""")


# 1 ---------------------------------------------------------------
Q(None, "Swap Two Variables", "Easy", "Variables · tuple assignment",
  "Given two values <code>a</code> and <code>b</code>, swap them and return <code>(a, b)</code>.",
  [((3, 7), (7, 3)), (("x", "y"), ("y", "x"))],
  ("Use a third, temporary variable to hold one value while you overwrite it.", "O(1)", "O(1)"),
  ("Python can assign several names at once: <code>a, b = b, a</code> builds the pair (b, a) first, then unpacks it.", "O(1)", "O(1)"))


@B
def swap(a, b):
    temp = a
    a = b
    b = temp
    return a, b


@O
def swap(a, b):
    a, b = b, a
    return a, b


# 2 ---------------------------------------------------------------
Q(None, "Celsius to Fahrenheit", "Easy", "Arithmetic · float",
  "Convert a temperature in Celsius to Fahrenheit using F = C × 9/5 + 32. Return the result rounded to 1 decimal place.",
  [((100,), 212.0), ((0,), 32.0), ((36.6,), 97.9), ((-40,), -40.0)],
  ("Do each part of the formula in its own variable so every step is visible.", "O(1)", "O(1)"),
  ("Write the whole formula in one expression and round it.", "O(1)", "O(1)"))


@B
def c_to_f(celsius):
    times = celsius * 9
    divided = times / 5
    fahrenheit = divided + 32
    result = round(fahrenheit, 1)
    return result


@O
def c_to_f(celsius):
    return round(celsius * 9 / 5 + 32, 1)


# 3 ---------------------------------------------------------------
Q(None, "Rectangle Area and Perimeter", "Easy", "Variables · returning two values",
  "Given the <code>length</code> and <code>width</code> of a rectangle, return <code>(area, perimeter)</code>.",
  [((5, 3), (15, 16)), ((2.5, 4), (10.0, 13.0))],
  ("Add up the four sides one by one for the perimeter.", "O(1)", "O(1)"),
  ("Use the formulas area = l × w and perimeter = 2 × (l + w), and return both as a tuple.", "O(1)", "O(1)"))


@B
def rectangle(length, width):
    area = length * width
    perimeter = 0
    perimeter = perimeter + length
    perimeter = perimeter + width
    perimeter = perimeter + length
    perimeter = perimeter + width
    return area, perimeter


@O
def rectangle(length, width):
    return length * width, 2 * (length + width)


# 4 ---------------------------------------------------------------
Q(None, "Add Two Numbers Given as Text", "Easy", "Type conversion",
  "<code>a</code> and <code>b</code> are numbers written as strings, like <code>\"12\"</code>. Return their sum as an int.",
  [(("12", "30"), 42), (("-5", "5"), 0), (("007", "3"), 10)],
  ("Convert each string digit by digit: multiply the running number by 10 and add the next digit.", "O(d) — d digits", "O(1)"),
  ("<code>int()</code> converts a numeric string to an integer in one call.", "O(d)", "O(1)"),
  viz=("12", "30"))


@B
def add_text(a, b):
    def to_int(s):
        sign = 1
        if s[0] == "-":
            sign = -1
            s = s[1:]
        number = 0
        for ch in s:
            number = number * 10 + (ord(ch) - ord("0"))
        return sign * number
    return to_int(a) + to_int(b)


@O
def add_text(a, b):
    return int(a) + int(b)


# 5 ---------------------------------------------------------------
Q(None, "Name of a Value's Type", "Easy", "Data types · type()",
  "Return the name of the type of <code>value</code> as a string: <code>'int'</code>, <code>'float'</code>, <code>'str'</code>, <code>'bool'</code>, <code>'list'</code> or <code>'NoneType'</code>.",
  [((5,), "int"), ((2.5,), "float"), (("hi",), "str"), ((True,), "bool"), ((None,), "NoneType"), (([1],), "list")],
  ("Check each possible type with <code>isinstance</code>, one after another. Check bool before int, because True is also an int.", "O(1)", "O(1)"),
  ("<code>type(value)</code> gives the class; its <code>__name__</code> is the name as text.", "O(1)", "O(1)"))


@B
def type_name(value):
    if value is None:
        return "NoneType"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    if isinstance(value, list):
        return "list"
    return "unknown"


@O
def type_name(value):
    return type(value).__name__


# 6 ---------------------------------------------------------------
Q(None, "Minutes to Hours and Minutes", "Easy", "// and %",
  "Convert a number of <code>minutes</code> into <code>(hours, minutes_left)</code>.",
  [((135,), (2, 15)), ((59,), (0, 59)), ((120,), (2, 0))],
  ("Take away 60 minutes at a time, counting the hours.", "O(minutes / 60)", "O(1)"),
  ("Floor division <code>//</code> gives the whole hours and modulo <code>%</code> gives what's left; <code>divmod</code> does both.", "O(1)", "O(1)"))


@B
def to_hours(minutes):
    hours = 0
    while minutes >= 60:
        minutes = minutes - 60
        hours = hours + 1
    return hours, minutes


@O
def to_hours(minutes):
    return divmod(minutes, 60)


# 7 ---------------------------------------------------------------
Q(None, "Sum of Digits", "Easy", "// and % · str",
  "Return the sum of the digits of a non-negative integer <code>n</code>.",
  [((123,), 6), ((9045,), 18), ((0,), 0)],
  ("Repeatedly take the last digit with <code>% 10</code> and remove it with <code>// 10</code>.", "O(d)", "O(1)"),
  ("Turn the number into a string, convert each character back to int, and add them with <code>sum</code>.", "O(d)", "O(d)"),
  viz=(9045,))


@B
def digit_sum(n):
    total = 0
    while n > 0:
        last = n % 10
        total = total + last
        n = n // 10
    return total


@O
def digit_sum(n):
    return sum(int(d) for d in str(n))


# 8 ---------------------------------------------------------------
Q(None, "Last Digit", "Easy", "% operator",
  "Return the last digit of an integer (ignore the sign).",
  [((1234,), 4), ((-87,), 7), ((5,), 5)],
  ("Convert to a string, drop a leading minus, and read the last character.", "O(d)", "O(d)"),
  ("<code>abs(n) % 10</code> is the remainder after dividing by 10 — exactly the last digit.", "O(1)", "O(1)"))


@B
def last_digit(n):
    text = str(n)
    if text[0] == "-":
        text = text[1:]
    last_char = text[len(text) - 1]
    return int(last_char)


@O
def last_digit(n):
    return abs(n) % 10


# 9 ---------------------------------------------------------------
Q(None, "Average of Three Numbers", "Easy", "Arithmetic",
  "Return the average of <code>a</code>, <code>b</code> and <code>c</code>, rounded to 2 decimals.",
  [((1, 2, 3), 2.0), ((10, 20, 25), 18.33), ((-1, 0, 1), 0.0)],
  ("Add the numbers one at a time into a total, count them, then divide.", "O(1)", "O(1)"),
  ("Put them in a list and use <code>sum(nums) / len(nums)</code> — the same code works for any amount of numbers.", "O(n)", "O(n)"))


@B
def average3(a, b, c):
    total = 0
    total = total + a
    total = total + b
    total = total + c
    count = 3
    avg = total / count
    return round(avg, 2)


@O
def average3(a, b, c):
    nums = [a, b, c]
    return round(sum(nums) / len(nums), 2)


# 10 --------------------------------------------------------------
Q(None, "Is It Truthy?", "Easy", "bool · truthiness",
  "Return <code>True</code> if <code>value</code> counts as true in an <code>if</code>, else <code>False</code>. Empty things, 0 and None are false.",
  [((0,), False), ((7,), True), (("",), False), (("0",), True), (([],), False), ((None,), False)],
  ("Check each kind of 'empty' value by hand.", "O(1)", "O(1)"),
  ("<code>bool(value)</code> applies Python's truthiness rules directly.", "O(1)", "O(1)"))


@B
def is_truthy(value):
    if value is None:
        return False
    if value == 0:
        return False
    if value == "" or value == [] or value == {} or value == ():
        return False
    return True


@O
def is_truthy(value):
    return bool(value)


# 11 --------------------------------------------------------------
Q(None, "Full Name", "Easy", "String joining · f-strings",
  "Return the full name made of <code>first</code> and <code>last</code> with one space between, e.g. <code>'Ada Lovelace'</code>.",
  [(("Ada", "Lovelace"), "Ada Lovelace"), (("Ravi", "K"), "Ravi K")],
  ("Glue the pieces together with <code>+</code>.", "O(n)", "O(n)"),
  ("An f-string puts values straight into the text: <code>f\"{first} {last}\"</code>.", "O(n)", "O(n)"))


@B
def full_name(first, last):
    result = first
    result = result + " "
    result = result + last
    return result


@O
def full_name(first, last):
    return f"{first} {last}"


# 12 --------------------------------------------------------------
Q(None, "Seconds to Clock Time", "Medium", "divmod · formatting",
  "Convert <code>seconds</code> into a string <code>'HH:MM:SS'</code> with two digits each.",
  [((3725,), "01:02:05"), ((59,), "00:00:59"), ((86399,), "23:59:59")],
  ("Compute hours, minutes and seconds step by step and add a leading zero by hand when a part is below 10.", "O(1)", "O(1)"),
  ("Use <code>divmod</code> twice and the format spec <code>:02</code> to pad with zeros.", "O(1)", "O(1)"))


@B
def clock(seconds):
    hours = seconds // 3600
    seconds = seconds - hours * 3600
    minutes = seconds // 60
    seconds = seconds - minutes * 60
    parts = []
    for part in [hours, minutes, seconds]:
        if part < 10:
            parts.append("0" + str(part))
        else:
            parts.append(str(part))
    return parts[0] + ":" + parts[1] + ":" + parts[2]


@O
def clock(seconds):
    minutes, s = divmod(seconds, 60)
    h, m = divmod(minutes, 60)
    return f"{h:02}:{m:02}:{s:02}"


# 13 --------------------------------------------------------------
Q(None, "Format Money", "Easy", "Format specifiers",
  "Return <code>amount</code> as text with exactly 2 decimal places, e.g. <code>5 → '5.00'</code>, <code>3.14159 → '3.14'</code>.",
  [((5,), "5.00"), ((3.14159,), "3.14"), ((2.5,), "2.50")],
  ("Round, convert to text, then add missing zeros after the dot by hand.", "O(1)", "O(1)"),
  ("The format spec <code>:.2f</code> means 'float with 2 decimals'.", "O(1)", "O(1)"))


@B
def money(amount):
    text = str(round(float(amount), 2))
    whole, dot, frac = text.partition(".")
    while len(frac) < 2:
        frac = frac + "0"
    return whole + "." + frac


@O
def money(amount):
    return f"{amount:.2f}"


# 14 --------------------------------------------------------------
Q(None, "Count the True Values", "Easy", "bool is a kind of int",
  "Given three booleans, return how many are <code>True</code>.",
  [((True, False, True), 2), ((False, False, False), 0), ((True, True, True), 3)],
  ("Check each one with <code>if</code> and add 1.", "O(1)", "O(1)"),
  ("True behaves like 1 and False like 0, so <code>sum</code> counts them.", "O(1)", "O(1)"))


@B
def count_true(a, b, c):
    count = 0
    if a:
        count = count + 1
    if b:
        count = count + 1
    if c:
        count = count + 1
    return count


@O
def count_true(a, b, c):
    return sum([a, b, c])


# 15 --------------------------------------------------------------
Q(None, "Distance Between Two Points", "Easy", "math module",
  "Return the straight-line distance between points (x1, y1) and (x2, y2), rounded to 2 decimals.",
  [((0, 0, 3, 4), 5.0), ((1, 1, 4, 5), 5.0), ((-1, 2, 2, -2), 5.0), ((0, 0, 1, 1), 1.41)],
  ("Compute the differences, square them, add, and take the square root with <code>** 0.5</code>.", "O(1)", "O(1)"),
  ("<code>math.dist</code> (or <code>math.hypot</code>) does the Pythagoras formula for you.", "O(1)", "O(1)"))


@B
def distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    square_sum = dx * dx + dy * dy
    root = square_sum ** 0.5
    return round(root, 2)


@O
def distance(x1, y1, x2, y2):
    import math
    return round(math.dist((x1, y1), (x2, y2)), 2)


# 16 --------------------------------------------------------------
Q(None, "Quotient and Remainder", "Easy", "divmod",
  "For positive integers <code>a</code> and <code>b</code>, return <code>(a // b, a % b)</code> without using <code>//</code> or <code>%</code> in the long way.",
  [((17, 5), (3, 2)), ((20, 4), (5, 0)), ((3, 7), (0, 3))],
  ("Subtract b from a repeatedly, counting how many times it fits.", "O(a / b)", "O(1)"),
  ("<code>divmod(a, b)</code> returns both at once.", "O(1)", "O(1)"))


@B
def quot_rem(a, b):
    count = 0
    while a >= b:
        a = a - b
        count = count + 1
    return count, a


@O
def quot_rem(a, b):
    return divmod(a, b)


# 17 --------------------------------------------------------------
Q(None, "Kilometres to Miles", "Easy", "Constants · rounding",
  "Convert kilometres to miles (1 km = 0.621371 miles), rounded to 2 decimals.",
  [((10,), 6.21), ((42.195,), 26.22), ((0,), 0.0)],
  ("Store the factor in a variable, multiply, then round in a separate step.", "O(1)", "O(1)"),
  ("Use a named constant in capitals and one expression.", "O(1)", "O(1)"))


@B
def km_to_miles(km):
    factor = 0.621371
    miles = km * factor
    rounded = round(miles, 2)
    return rounded


@O
def km_to_miles(km):
    MILES_PER_KM = 0.621371
    return round(km * MILES_PER_KM, 2)


# 18 --------------------------------------------------------------
Q(None, "Is It a Whole Number String?", "Easy", "str methods · conversion",
  "Return <code>True</code> if the text is a whole number made only of digits (like <code>'2024'</code>), else <code>False</code>.",
  [(("2024",), True), (("12a",), False), (("",), False), (("3.5",), False)],
  ("Check every character is between '0' and '9', and that the text isn't empty.", "O(n)", "O(1)"),
  ("<code>str.isdigit()</code> does exactly this check (it's False for an empty string).", "O(n)", "O(1)"))


@B
def is_whole_number(text):
    if text == "":
        return False
    for ch in text:
        if ch < "0" or ch > "9":
            return False
    return True


@O
def is_whole_number(text):
    return text.isdigit()


# 19 --------------------------------------------------------------
Q(None, "Greeting From Input", "Easy", "input() · f-strings",
  "A program reads a name and an age with <code>input()</code>. Write the function that builds the reply: given <code>name</code> and <code>age_text</code> (both strings), return <code>'Hi NAME, next year you will be AGE+1'</code>.",
  [(("Asha", "20"), "Hi Asha, next year you will be 21"), (("Li", "9"), "Hi Li, next year you will be 10")],
  ("Convert the age, add one, convert back to text, and join the pieces with <code>+</code>.", "O(1)", "O(1)"),
  ("An f-string can contain the calculation directly.", "O(1)", "O(1)"))


@B
def greet(name, age_text):
    age = int(age_text)
    next_age = age + 1
    next_age_text = str(next_age)
    return "Hi " + name + ", next year you will be " + next_age_text


@O
def greet(name, age_text):
    return f"Hi {name}, next year you will be {int(age_text) + 1}"


# 20 --------------------------------------------------------------
Q(None, "Bill Split With Tip", "Medium", "Expressions · rounding",
  "A bill of <code>total</code> is shared by <code>people</code> with a <code>tip_percent</code> tip. Return each person's share rounded to 2 decimals.",
  [((100, 4, 10), 27.5), ((59.99, 3, 15), 23.0), ((80, 2, 0), 40.0)],
  ("Compute the tip, the new total and the share in separate steps.", "O(1)", "O(1)"),
  ("One expression: total × (1 + tip/100) ÷ people.", "O(1)", "O(1)"))


@B
def split_bill(total, people, tip_percent):
    tip = total * tip_percent / 100
    with_tip = total + tip
    share = with_tip / people
    return round(share, 2)


@O
def split_bill(total, people, tip_percent):
    return round(total * (1 + tip_percent / 100) / people, 2)
