from lib import *

TOPIC(
    id="conditions", title="Conditions (if / elif / else)", glyph="if ?",
    blurb="Make decisions: if, elif, else, nested conditions, the one-line conditional and match-case.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">if marks &gt;= 90:
    grade = "A"
elif marks &gt;= 75:          # checked only if the first was False
    grade = "B"
else:                      # runs when nothing above matched
    grade = "C"

label = "even" if n % 2 == 0 else "odd"     # conditional expression

match command:             # Python 3.10+
    case "start": ...
    case "stop" | "quit": ...
    case _: ...            # default</code></pre>
<ul>
<li>The colon <code>:</code> and the <b>indentation</b> (4 spaces) are required.</li>
<li>Only the <b>first</b> true branch of an if/elif chain runs.</li>
<li>Order elif branches from most specific to least specific.</li>
</ul>
""")


Q(None, "Positive, Negative or Zero", "Easy", "if / elif / else",
  "Return <code>'positive'</code>, <code>'negative'</code> or <code>'zero'</code> for the number <code>n</code>.",
  [((5,), "positive"), ((-2,), "negative"), ((0,), "zero")],
  ("Three separate if statements, each with its own return.", "O(1)", "O(1)"),
  ("One if/elif/else chain — exactly one branch runs.", "O(1)", "O(1)"),
  viz=(-2,))


@B
def sign_word(n):
    if n > 0:
        return "positive"
    if n < 0:
        return "negative"
    if n == 0:
        return "zero"


@O
def sign_word(n):
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    else:
        return "zero"


Q(None, "Grade From Marks", "Easy", "elif chain",
  "Marks 90+ → 'A', 75–89 → 'B', 60–74 → 'C', 40–59 → 'D', below 40 → 'F'.",
  [((95,), "A"), ((75,), "B"), ((61,), "C"), ((40,), "D"), ((12,), "F")],
  ("Write each band with both lower and upper limits.", "O(1)", "O(1)"),
  ("Check from the top down: each elif already knows the higher bands failed, so only lower limits are needed. A table of cut-offs makes it data-driven.", "O(1)", "O(1)"),
  viz=(61,))


@B
def grade(marks):
    if marks >= 90:
        return "A"
    if marks >= 75 and marks < 90:
        return "B"
    if marks >= 60 and marks < 75:
        return "C"
    if marks >= 40 and marks < 60:
        return "D"
    return "F"


@O
def grade(marks):
    for cutoff, letter in [(90, "A"), (75, "B"), (60, "C"), (40, "D")]:
        if marks >= cutoff:
            return letter
    return "F"


Q(None, "Ticket Price by Age", "Easy", "Ranges",
  "Under 5 → 0, 5–17 → 50, 18–59 → 100, 60 and above → 60. Return the price.",
  [((3,), 0), ((12,), 50), ((30,), 100), ((65,), 60)],
  ("Separate if statements, each checking a full range with <code>and</code>.", "O(1)", "O(1)"),
  ("An elif chain in increasing order needs only one comparison per branch.", "O(1)", "O(1)"))


@B
def ticket(age):
    price = 0
    if age < 5:
        price = 0
    if age >= 5 and age <= 17:
        price = 50
    if age >= 18 and age <= 59:
        price = 100
    if age >= 60:
        price = 60
    return price


@O
def ticket(age):
    if age < 5:
        return 0
    elif age < 18:
        return 50
    elif age < 60:
        return 100
    return 60


Q(None, "Larger of Two", "Easy", "Conditional expression",
  "Return the larger of <code>a</code> and <code>b</code>.",
  [((3, 8), 8), ((9, 2), 9), ((4, 4), 4)],
  ("A full if/else statement.", "O(1)", "O(1)"),
  ("The one-line conditional expression <code>a if a &gt;= b else b</code> (or simply <code>max</code>).", "O(1)", "O(1)"))


@B
def larger(a, b):
    if a >= b:
        result = a
    else:
        result = b
    return result


@O
def larger(a, b):
    return a if a >= b else b


Q(None, "Triangle Type", "Medium", "Combined conditions",
  "Given three side lengths, return <code>'invalid'</code> if they can't form a triangle, else <code>'equilateral'</code>, <code>'isosceles'</code> or <code>'scalene'</code>.",
  [((3, 3, 3), "equilateral"), ((3, 3, 5), "isosceles"), ((3, 4, 5), "scalene"), ((1, 2, 3), "invalid")],
  ("Check validity with three separate comparisons, then count equal pairs with ifs.", "O(1)", "O(1)"),
  ("Sort the sides so validity is one test (a + b &gt; c), then the number of distinct sides tells the type.", "O(1)", "O(1)"))


@B
def triangle(a, b, c):
    if a + b <= c:
        return "invalid"
    if a + c <= b:
        return "invalid"
    if b + c <= a:
        return "invalid"
    if a == b and b == c:
        return "equilateral"
    if a == b or b == c or a == c:
        return "isosceles"
    return "scalene"


@O
def triangle(a, b, c):
    x, y, z = sorted((a, b, c))
    if x + y <= z:
        return "invalid"
    return {1: "equilateral", 2: "isosceles", 3: "scalene"}[len({a, b, c})]


Q(None, "Vowel or Consonant", "Easy", "in operator",
  "For a single letter, return <code>'vowel'</code> or <code>'consonant'</code> (case doesn't matter).",
  [(("a",), "vowel"), (("E",), "vowel"), (("z",), "consonant")],
  ("Compare with each vowel using <code>or</code>.", "O(1)", "O(1)"),
  ("Lower-case it and test membership: <code>ch in 'aeiou'</code>.", "O(1)", "O(1)"))


@B
def vowel_or_consonant(ch):
    ch = ch.lower()
    if ch == "a" or ch == "e" or ch == "i" or ch == "o" or ch == "u":
        return "vowel"
    return "consonant"


@O
def vowel_or_consonant(ch):
    return "vowel" if ch.lower() in "aeiou" else "consonant"


Q(None, "Day Name", "Easy", "elif chain vs lookup",
  "Return the day name for numbers 1–7 (1 = 'Monday'); otherwise return <code>'invalid'</code>.",
  [((1,), "Monday"), ((7,), "Sunday"), ((9,), "invalid")],
  ("Seven if/elif branches.", "O(1)", "O(1)"),
  ("Store the names in a tuple and index it — a lookup replaces the whole chain.", "O(1)", "O(1)"),
  viz=(5,))


@B
def day_name(n):
    if n == 1:
        return "Monday"
    elif n == 2:
        return "Tuesday"
    elif n == 3:
        return "Wednesday"
    elif n == 4:
        return "Thursday"
    elif n == 5:
        return "Friday"
    elif n == 6:
        return "Saturday"
    elif n == 7:
        return "Sunday"
    return "invalid"


@O
def day_name(n):
    days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    return days[n - 1] if 1 <= n <= 7 else "invalid"


Q(None, "BMI Category", "Easy", "Float conditions",
  "BMI = weight / height². Below 18.5 → 'under', below 25 → 'normal', below 30 → 'over', else 'obese'.",
  [((50, 1.8), "under"), ((70, 1.75), "normal"), ((85, 1.75), "over"), ((110, 1.7), "obese")],
  ("Compute BMI and test full ranges.", "O(1)", "O(1)"),
  ("Ordered elif chain with only upper limits.", "O(1)", "O(1)"))


@B
def bmi_category(weight, height):
    bmi = weight / (height * height)
    if bmi < 18.5:
        return "under"
    if bmi >= 18.5 and bmi < 25:
        return "normal"
    if bmi >= 25 and bmi < 30:
        return "over"
    return "obese"


@O
def bmi_category(weight, height):
    bmi = weight / height ** 2
    if bmi < 18.5:
        return "under"
    elif bmi < 25:
        return "normal"
    elif bmi < 30:
        return "over"
    return "obese"


Q(None, "Simple Calculator", "Medium", "match-case",
  "Given <code>a</code>, an operator string (<code>'+'</code>, <code>'-'</code>, <code>'*'</code>, <code>'/'</code>) and <code>b</code>, return the result, or <code>None</code> for an unknown operator or division by zero.",
  [((6, "+", 3), 9), ((6, "/", 3), 2.0), ((6, "/", 0), None), ((6, "%", 3), None)],
  ("An if/elif chain comparing the operator.", "O(1)", "O(1)"),
  ("A <code>match</code> statement reads like a table of cases; a guard (<code>if b != 0</code>) handles division by zero.", "O(1)", "O(1)"))


@B
def calc(a, op, b):
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        if b == 0:
            return None
        return a / b
    else:
        return None


@O
def calc(a, op, b):
    match op:
        case "+":
            return a + b
        case "-":
            return a - b
        case "*":
            return a * b
        case "/" if b != 0:
            return a / b
        case _:
            return None


Q(None, "Quadrant of a Point", "Easy", "Nested conditions",
  "Return 1, 2, 3 or 4 for the quadrant of (x, y), or 0 if it lies on an axis.",
  [((3, 4), 1), ((-3, 4), 2), ((-1, -1), 3), ((2, -5), 4), ((0, 7), 0)],
  ("Nested if: first on x, then on y.", "O(1)", "O(1)"),
  ("Handle the axis case first (guard clause), then one flat chain using <code>and</code>.", "O(1)", "O(1)"))


@B
def quadrant(x, y):
    if x > 0:
        if y > 0:
            return 1
        elif y < 0:
            return 4
        else:
            return 0
    elif x < 0:
        if y > 0:
            return 2
        elif y < 0:
            return 3
        else:
            return 0
    else:
        return 0


@O
def quadrant(x, y):
    if x == 0 or y == 0:
        return 0
    if x > 0:
        return 1 if y > 0 else 4
    return 2 if y > 0 else 3


Q(None, "Shopping Discount", "Easy", "Tiers",
  "Purchases of 5000+ get 20% off, 2000+ get 10% off, 1000+ get 5% off. Return the final amount.",
  [((6000,), 4800.0), ((2500,), 2250.0), ((1000,), 950.0), ((500,), 500.0)],
  ("Compute the discount percent with ifs, then apply it.", "O(1)", "O(1)"),
  ("Walk a list of (threshold, percent) tiers from the top.", "O(tiers)", "O(1)"))


@B
def discounted(amount):
    percent = 0
    if amount >= 1000:
        percent = 5
    if amount >= 2000:
        percent = 10
    if amount >= 5000:
        percent = 20
    return amount - amount * percent / 100


@O
def discounted(amount):
    for threshold, percent in [(5000, 20), (2000, 10), (1000, 5)]:
        if amount >= threshold:
            return amount * (1 - percent / 100)
    return float(amount)


Q(None, "Can It Be a Triangle?", "Easy", "and",
  "Return True if three positive lengths can form a triangle (each pair sums to more than the third).",
  [((3, 4, 5), True), ((1, 1, 3), False), ((5, 5, 5), True)],
  ("Three ifs, returning False on any failure.", "O(1)", "O(1)"),
  ("Only the largest side can break the rule: sum of all &gt; 2 × max.", "O(1)", "O(1)"))


@B
def can_be_triangle(a, b, c):
    if a + b <= c:
        return False
    if a + c <= b:
        return False
    if b + c <= a:
        return False
    return True


@O
def can_be_triangle(a, b, c):
    return a + b + c > 2 * max(a, b, c)


Q(None, "Electricity Bill", "Medium", "Slabs",
  "First 100 units cost 5 each, the next 100 cost 7 each, anything above 200 costs 10 each. Return the bill.",
  [((50,), 250), ((150,), 850), ((250,), 1700), ((0,), 0)],
  ("Branch on which slab the total falls into and write the full sum for each case.", "O(1)", "O(1)"),
  ("Charge each slab for the units that fall inside it with min/max — no special cases.", "O(slabs)", "O(1)"))


@B
def bill(units):
    if units <= 100:
        return units * 5
    elif units <= 200:
        return 100 * 5 + (units - 100) * 7
    else:
        return 100 * 5 + 100 * 7 + (units - 200) * 10


@O
def bill(units):
    total = 0
    for start, end, price in [(0, 100, 5), (100, 200, 7), (200, float("inf"), 10)]:
        if units > start:
            total += (min(units, end) - start) * price
    return int(total)


Q(None, "Rock Paper Scissors", "Medium", "Conditions vs lookup",
  "Return <code>'p1'</code>, <code>'p2'</code> or <code>'draw'</code> for moves 'rock', 'paper', 'scissors'.",
  [(("rock", "scissors"), "p1"), (("rock", "paper"), "p2"), (("paper", "paper"), "draw"), (("scissors", "paper"), "p1")],
  ("Check every winning combination for player 1 with if statements.", "O(1)", "O(1)"),
  ("Store what each move beats in a dict; then the logic is two lines.", "O(1)", "O(1)"))


@B
def rps(p1, p2):
    if p1 == p2:
        return "draw"
    if p1 == "rock" and p2 == "scissors":
        return "p1"
    if p1 == "scissors" and p2 == "paper":
        return "p1"
    if p1 == "paper" and p2 == "rock":
        return "p1"
    return "p2"


@O
def rps(p1, p2):
    beats = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
    if p1 == p2:
        return "draw"
    return "p1" if beats[p1] == p2 else "p2"


Q(None, "Greeting by Hour", "Easy", "Chained comparisons",
  "For an hour 0–23 return 'morning' (5–11), 'afternoon' (12–16), 'evening' (17–20) or 'night'.",
  [((8,), "morning"), ((13,), "afternoon"), ((19,), "evening"), ((2,), "night"), ((23,), "night")],
  ("Ranges written with <code>and</code>.", "O(1)", "O(1)"),
  ("Chained comparisons read like the specification.", "O(1)", "O(1)"))


@B
def greeting(hour):
    if hour >= 5 and hour <= 11:
        return "morning"
    if hour >= 12 and hour <= 16:
        return "afternoon"
    if hour >= 17 and hour <= 20:
        return "evening"
    return "night"


@O
def greeting(hour):
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    return "night"


Q(None, "Sort Three Numbers", "Medium", "Swaps with if",
  "Return <code>(a, b, c)</code> in increasing order.",
  [((3, 1, 2), (1, 2, 3)), ((5, 5, 1), (1, 5, 5)), ((1, 2, 3), (1, 2, 3))],
  ("Three compare-and-swap steps (a tiny sorting network).", "O(1)", "O(1)"),
  ("<code>sorted()</code> returns a sorted list; convert it to a tuple.", "O(1)", "O(1)"))


@B
def sort3(a, b, c):
    if a > b:
        a, b = b, a
    if b > c:
        b, c = c, b
    if a > b:
        a, b = b, a
    return a, b, c


@O
def sort3(a, b, c):
    return tuple(sorted((a, b, c)))


Q(None, "Strong Password", "Medium", "Conditions with any()",
  "A password is strong if it has at least 8 characters, a digit, an uppercase letter and a lowercase letter. Return True or False.",
  [(("Secret123",), True), (("secret123",), False), (("Sh0rt",), False), (("NoDigitsHere",), False)],
  ("Loop once, setting a flag for each kind of character, then check all flags.", "O(n)", "O(1)"),
  ("<code>any()</code> with a generator tests 'is there at least one…' in one expression each.", "O(n)", "O(1)"),
  viz=("Ab3cdefg",))


@B
def strong(password):
    has_digit = False
    has_upper = False
    has_lower = False
    for ch in password:
        if ch.isdigit():
            has_digit = True
        if ch.isupper():
            has_upper = True
        if ch.islower():
            has_lower = True
    if len(password) >= 8 and has_digit and has_upper and has_lower:
        return True
    return False


@O
def strong(password):
    return (len(password) >= 8
            and any(c.isdigit() for c in password)
            and any(c.isupper() for c in password)
            and any(c.islower() for c in password))


Q(None, "Character Type", "Easy", "str methods in conditions",
  "Return 'upper', 'lower', 'digit', 'space' or 'other' for a single character.",
  [(("A",), "upper"), (("q",), "lower"), (("7",), "digit"), ((" ",), "space"), (("#",), "other")],
  ("Compare against character ranges like 'A' &lt;= ch &lt;= 'Z'.", "O(1)", "O(1)"),
  ("Use the string methods isupper / islower / isdigit / isspace.", "O(1)", "O(1)"))


@B
def char_type(ch):
    if "A" <= ch <= "Z":
        return "upper"
    if "a" <= ch <= "z":
        return "lower"
    if "0" <= ch <= "9":
        return "digit"
    if ch == " " or ch == "\t" or ch == "\n":
        return "space"
    return "other"


@O
def char_type(ch):
    if ch.isupper():
        return "upper"
    elif ch.islower():
        return "lower"
    elif ch.isdigit():
        return "digit"
    elif ch.isspace():
        return "space"
    return "other"


Q(None, "Days in a Month", "Medium", "Conditions + lookup",
  "Return the number of days in <code>month</code> (1–12) of <code>year</code>, handling leap years.",
  [((2, 2024), 29), ((2, 2023), 28), ((4, 2023), 30), ((12, 2023), 31)],
  ("Group the months in if/elif and test leap-year rules for February.", "O(1)", "O(1)"),
  ("A tuple of month lengths plus one leap-year adjustment.", "O(1)", "O(1)"))


@B
def days_in_month(month, year):
    if month == 2:
        if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
            return 29
        return 28
    elif month == 4 or month == 6 or month == 9 or month == 11:
        return 30
    else:
        return 31


@O
def days_in_month(month, year):
    leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    days = (31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    return days[month - 1]


Q(None, "Next Traffic Light", "Easy", "Lookup instead of if",
  "Return the next colour: green → yellow → red → green.",
  [(("green",), "yellow"), (("yellow",), "red"), (("red",), "green")],
  ("An if/elif for each colour.", "O(1)", "O(1)"),
  ("A dict maps each colour to the next one.", "O(1)", "O(1)"))


@B
def next_light(colour):
    if colour == "green":
        return "yellow"
    elif colour == "yellow":
        return "red"
    else:
        return "green"


@O
def next_light(colour):
    return {"green": "yellow", "yellow": "red", "red": "green"}[colour]
