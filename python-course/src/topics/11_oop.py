from lib import *
from dataclasses import dataclass

TOPIC(
    id="oop", title="Object-Oriented Programming", glyph="class",
    blurb="Model things as objects: classes, attributes, methods, encapsulation, inheritance, polymorphism and special methods.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">class Account:
    bank = "PyBank"                 # class attribute (shared)
    def __init__(self, owner, balance=0):
        self.owner = owner          # instance attributes
        self._balance = balance     # "internal" by convention
    def deposit(self, amount):      # method
        self._balance += amount
    @property
    def balance(self): return self._balance
    def __repr__(self): return f"Account({self.owner!r})"

class Savings(Account):             # inheritance
    def deposit(self, amount):      # overriding
        super().deposit(amount * 1.01)

from dataclasses import dataclass
@dataclass
class Point: x: int; y: int</code></pre>
""")


# ---- design questions: tests are (constructor args, [(method, args), ...]) → list of results

Q(None, "Rectangle Class", "Easy", "Attributes and methods",
  "Create a <code>Rectangle(width, height)</code> class with methods <code>area()</code> and <code>perimeter()</code>.",
  [(((3, 4), [("area", ()), ("perimeter", ())]), [12, 14]), (((5, 5), [("area", ())]), [25])],
  ("Store the values and compute everything step by step inside each method.", "O(1)", "O(1)"),
  ("A <code>@dataclass</code> writes <code>__init__</code> for you; methods are one line each.", "O(1)", "O(1)"),
  design=True)


@B
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        result = self.width * self.height
        return result

    def perimeter(self):
        result = 0
        result = result + self.width + self.width
        result = result + self.height + self.height
        return result


@O
@dataclass
class Rectangle:
    width: float
    height: float

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


Q(None, "Bank Account", "Easy", "Methods that change state",
  "<code>BankAccount(balance)</code> with <code>deposit(x)</code>, <code>withdraw(x)</code> (returns False and changes nothing if funds are insufficient, else True) and <code>get_balance()</code>.",
  [(((100,), [("deposit", (50,)), ("withdraw", (30,)), ("withdraw", (500,)), ("get_balance", ())]), [None, True, False, 120])],
  ("Keep a list of every transaction and recompute the balance from it each time.", "O(t) per call", "O(t)"),
  ("Store the current balance and update it directly.", "O(1)", "O(1)"),
  design=True)


@B
class BankAccount:
    def __init__(self, balance):
        self.transactions = [balance]

    def deposit(self, x):
        self.transactions.append(x)

    def withdraw(self, x):
        if sum(self.transactions) < x:
            return False
        self.transactions.append(-x)
        return True

    def get_balance(self):
        return sum(self.transactions)


@O
class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def deposit(self, x):
        self.balance += x

    def withdraw(self, x):
        if x > self.balance:
            return False
        self.balance -= x
        return True

    def get_balance(self):
        return self.balance


Q(None, "Click Counter", "Easy", "Instance state",
  "<code>Counter()</code> with <code>click()</code> (adds 1 and returns the new count), <code>reset()</code> and <code>value()</code>.",
  [(((), [("click", ()), ("click", ()), ("value", ()), ("reset", ()), ("click", ())]), [1, 2, 2, None, 1])],
  ("Store every click in a list; the count is its length.", "O(1)", "O(clicks)"),
  ("Store just the number.", "O(1)", "O(1)"),
  design=True)


@B
class Counter:
    def __init__(self):
        self.clicks = []

    def click(self):
        self.clicks.append(1)
        return len(self.clicks)

    def reset(self):
        self.clicks = []

    def value(self):
        return len(self.clicks)


@O
class Counter:
    def __init__(self):
        self.count = 0

    def click(self):
        self.count += 1
        return self.count

    def reset(self):
        self.count = 0

    def value(self):
        return self.count


Q(None, "Student Average", "Easy", "Lists inside objects",
  "<code>Student(name)</code> with <code>add_mark(m)</code> and <code>average()</code> (rounded to 2 decimals; 0 if no marks).",
  [((("Ana",), [("add_mark", (80,)), ("add_mark", (91,)), ("average", ())]), [None, None, 85.5]), ((("Ben",), [("average", ())]), [0])],
  ("Keep a running total and a count, and divide with an if-check.", "O(1)", "O(1)"),
  ("Keep the marks list; <code>average</code> uses sum/len with a guard.", "O(n)", "O(n)"),
  design=True)


@B
class Student:
    def __init__(self, name):
        self.name = name
        self.total = 0
        self.count = 0

    def add_mark(self, m):
        self.total = self.total + m
        self.count = self.count + 1

    def average(self):
        if self.count == 0:
            return 0
        return round(self.total / self.count, 2)


@O
class Student:
    def __init__(self, name):
        self.name = name
        self.marks = []

    def add_mark(self, m):
        self.marks.append(m)

    def average(self):
        return round(sum(self.marks) / len(self.marks), 2) if self.marks else 0


Q(None, "Temperature With a Property", "Medium", "@property",
  "<code>Temperature(celsius)</code>. Reading <code>fahrenheit</code> converts; setting <code>celsius</code> updates it. Use methods <code>get_f()</code> and <code>set_c(c)</code> in the tests.",
  [(((100,), [("get_f", ()), ("set_c", (0,)), ("get_f", ())]), [212.0, None, 32.0])],
  ("Store both values and keep them in sync by hand in every setter.", "O(1)", "O(1)"),
  ("Store only Celsius and compute Fahrenheit with a <code>@property</code> — the two can never disagree.", "O(1)", "O(1)"),
  design=True)


@B
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius
        self.fahrenheit = celsius * 9 / 5 + 32

    def set_c(self, c):
        self.celsius = c
        self.fahrenheit = c * 9 / 5 + 32

    def get_f(self):
        return self.fahrenheit


@O
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def fahrenheit(self):
        return self.celsius * 9 / 5 + 32

    def set_c(self, c):
        self.celsius = c

    def get_f(self):
        return self.fahrenheit


Q(None, "Simple Stack Class", "Easy", "Wrapping a list",
  "<code>Stack()</code> with <code>push(x)</code>, <code>pop()</code> (None if empty), <code>peek()</code> and <code>is_empty()</code>.",
  [(((), [("push", (1,)), ("push", (2,)), ("peek", ()), ("pop", ()), ("pop", ()), ("pop", ()), ("is_empty", ())]), [None, None, 2, 2, 1, None, True])],
  ("Track the size in a separate counter and insert at the front of the list.", "O(n) push", "O(n)"),
  ("Use the end of a list: append and pop are O(1).", "O(1)", "O(n)"),
  design=True)


@B
class Stack:
    def __init__(self):
        self.items = []
        self.size = 0

    def push(self, x):
        self.items.insert(0, x)
        self.size += 1

    def pop(self):
        if self.size == 0:
            return None
        self.size -= 1
        return self.items.pop(0)

    def peek(self):
        return self.items[0] if self.size else None

    def is_empty(self):
        return self.size == 0


@O
class Stack:
    def __init__(self):
        self.items = []

    def push(self, x):
        self.items.append(x)

    def pop(self):
        return self.items.pop() if self.items else None

    def peek(self):
        return self.items[-1] if self.items else None

    def is_empty(self):
        return not self.items


Q(None, "Simple Queue Class", "Medium", "deque inside a class",
  "<code>Queue()</code> with <code>enqueue(x)</code>, <code>dequeue()</code> (None if empty) and <code>size()</code>.",
  [(((), [("enqueue", ("a",)), ("enqueue", ("b",)), ("dequeue", ()), ("size", ()), ("dequeue", ()), ("dequeue", ())]), [None, None, "a", 1, "b", None])],
  ("A list with <code>pop(0)</code>, which shifts every item.", "O(n) dequeue", "O(n)"),
  ("<code>collections.deque</code> removes from the front in O(1).", "O(1)", "O(n)"),
  design=True)


@B
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, x):
        self.items.append(x)

    def dequeue(self):
        if len(self.items) == 0:
            return None
        return self.items.pop(0)

    def size(self):
        return len(self.items)


@O
class Queue:
    def __init__(self):
        from collections import deque
        self.items = deque()

    def enqueue(self, x):
        self.items.append(x)

    def dequeue(self):
        return self.items.popleft() if self.items else None

    def size(self):
        return len(self.items)


Q(None, "Shopping Cart", "Medium", "Objects holding dicts",
  "<code>Cart()</code> with <code>add(item, price, qty=1)</code>, <code>remove(item)</code> and <code>total()</code> (rounded to 2 decimals). Adding an item again increases its quantity.",
  [(((), [("add", ("pen", 10, 2)), ("add", ("ink", 25)), ("add", ("pen", 10)), ("total", ()), ("remove", ("ink",)), ("total", ())]), [None, None, None, 55, None, 30])],
  ("Store a list of (item, price) entries, one per unit, and scan it for removal and totals.", "O(n) per call", "O(units)"),
  ("Store item → [price, qty] in a dict.", "O(1) add/remove, O(k) total", "O(k)"),
  design=True)


@B
class Cart:
    def __init__(self):
        self.units = []

    def add(self, item, price, qty=1):
        for _ in range(qty):
            self.units.append((item, price))

    def remove(self, item):
        self.units = [u for u in self.units if u[0] != item]

    def total(self):
        t = 0
        for name, price in self.units:
            t += price
        return round(t, 2)


@O
class Cart:
    def __init__(self):
        self.items = {}

    def add(self, item, price, qty=1):
        old_qty = self.items.get(item, [price, 0])[1]
        self.items[item] = [price, old_qty + qty]

    def remove(self, item):
        self.items.pop(item, None)

    def total(self):
        return round(sum(p * q for p, q in self.items.values()), 2)


Q(None, "Library Loans", "Medium", "Sets inside objects",
  "<code>Library(books)</code> with <code>borrow(title)</code> (True if available, then it's out), <code>give_back(title)</code> and <code>available()</code> (sorted list).",
  [(((["Dune", "Emma"],), [("borrow", ("Dune",)), ("borrow", ("Dune",)), ("available", ()), ("give_back", ("Dune",)), ("available", ())]), [True, False, ["Emma"], None, ["Dune", "Emma"]])],
  ("A list of [title, is_out] pairs, scanned on every call.", "O(n) per call", "O(n)"),
  ("Two sets: the books on the shelf and the books out.", "O(1) borrow/return", "O(n)"),
  design=True)


@B
class Library:
    def __init__(self, books):
        self.books = [[b, False] for b in books]

    def borrow(self, title):
        for entry in self.books:
            if entry[0] == title and not entry[1]:
                entry[1] = True
                return True
        return False

    def give_back(self, title):
        for entry in self.books:
            if entry[0] == title:
                entry[1] = False

    def available(self):
        return sorted(e[0] for e in self.books if not e[1])


@O
class Library:
    def __init__(self, books):
        self.shelf = set(books)
        self.out = set()

    def borrow(self, title):
        if title not in self.shelf:
            return False
        self.shelf.remove(title)
        self.out.add(title)
        return True

    def give_back(self, title):
        if title in self.out:
            self.out.remove(title)
            self.shelf.add(title)

    def available(self):
        return sorted(self.shelf)


Q(None, "Protected Age", "Medium", "Encapsulation and validation",
  "<code>Person(name, age)</code> with <code>set_age(a)</code> that only accepts 0–150 (returns True/False) and <code>get_age()</code>.",
  [((("Ana", 20), [("set_age", (21,)), ("set_age", (-5,)), ("get_age", ())]), [True, False, 21])],
  ("Public attribute plus a separate validate function called from the setter.", "O(1)", "O(1)"),
  ("Keep the value in <code>_age</code> (internal by convention) and guard every change in one method.", "O(1)", "O(1)"),
  design=True)


@B
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def valid(self, a):
        if a < 0:
            return False
        if a > 150:
            return False
        return True

    def set_age(self, a):
        ok = self.valid(a)
        if ok:
            self.age = a
        return ok

    def get_age(self):
        return self.age


@O
class Person:
    def __init__(self, name, age):
        self.name = name
        self._age = age

    def set_age(self, a):
        if not 0 <= a <= 150:
            return False
        self._age = a
        return True

    def get_age(self):
        return self._age


Q(None, "Playlist With len and in", "Medium", "Special methods",
  "<code>Playlist()</code> with <code>add(song)</code>, <code>count()</code> (number of songs) and <code>has(song)</code>. The optimal answer makes <code>len(p)</code> and <code>song in p</code> work too.",
  [(((), [("add", ("Hey",)), ("add", ("Yo",)), ("count", ()), ("has", ("Yo",)), ("has", ("Ok",))]), [None, None, 2, True, False])],
  ("Ordinary methods only.", "O(n) has", "O(n)"),
  ("Define <code>__len__</code> and <code>__contains__</code> so the object behaves like a built-in collection.", "O(n) has", "O(n)"),
  design=True)


@B
class Playlist:
    def __init__(self):
        self.songs = []

    def add(self, song):
        self.songs.append(song)

    def count(self):
        n = 0
        for _ in self.songs:
            n += 1
        return n

    def has(self, song):
        for s in self.songs:
            if s == song:
                return True
        return False


@O
class Playlist:
    def __init__(self):
        self.songs = []

    def add(self, song):
        self.songs.append(song)

    def __len__(self):
        return len(self.songs)

    def __contains__(self, song):
        return song in self.songs

    def count(self):
        return len(self)

    def has(self, song):
        return song in self


# ---- function questions that use classes inside

Q(None, "Add Two Points", "Medium", "Operator overloading",
  "Given two points as tuples, return their sum as a tuple — using a Point class in both answers.",
  [(((1, 2), (3, 4)), (4, 6)), (((0, 0), (-1, 5)), (-1, 5))],
  ("A class with an <code>add</code> method you call by name.", "O(1)", "O(1)"),
  ("Define <code>__add__</code> so <code>p + q</code> works.", "O(1)", "O(1)"))


@B
def add_points(a, b):
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def add(self, other):
            return Point(self.x + other.x, self.y + other.y)

    p = Point(*a).add(Point(*b))
    return (p.x, p.y)


@O
def add_points(a, b):
    class Point:
        def __init__(self, x, y):
            self.x, self.y = x, y

        def __add__(self, other):
            return Point(self.x + other.x, self.y + other.y)

    p = Point(*a) + Point(*b)
    return (p.x, p.y)


Q(None, "Readable Object Text", "Easy", "__str__ / __repr__",
  "Return the text of a Book object as <code>'TITLE by AUTHOR'</code>.",
  [(("Dune", "Herbert"), "Dune by Herbert")],
  ("A <code>describe()</code> method you have to remember to call.", "O(1)", "O(1)"),
  ("Define <code>__str__</code> so <code>str(book)</code> and <code>print(book)</code> just work.", "O(1)", "O(1)"))


@B
def book_text(title, author):
    class Book:
        def __init__(self, title, author):
            self.title = title
            self.author = author

        def describe(self):
            return self.title + " by " + self.author

    return Book(title, author).describe()


@O
def book_text(title, author):
    class Book:
        def __init__(self, title, author):
            self.title, self.author = title, author

        def __str__(self):
            return f"{self.title} by {self.author}"

    return str(Book(title, author))


Q(None, "Total Area of Shapes", "Medium", "Inheritance and polymorphism",
  "Given shapes like ('circle', r) and ('square', s), return the total area rounded to 2 decimals.",
  [(([("circle", 1), ("square", 2)],), 7.14), (([],), 0)],
  ("One function with an if/elif on the shape type.", "O(n)", "O(1)"),
  ("A base class Shape with subclasses that each define <code>area()</code>; the loop just calls <code>area()</code> on every object.", "O(n)", "O(n)"),
  viz=([("circle", 1), ("square", 2)],))


@B
def total_area(shapes):
    total = 0
    for kind, size in shapes:
        if kind == "circle":
            total += 3.141592653589793 * size * size
        elif kind == "square":
            total += size * size
    return round(total, 2)


@O
def total_area(shapes):
    import math

    class Shape:
        def area(self):
            raise NotImplementedError

    class Circle(Shape):
        def __init__(self, r):
            self.r = r

        def area(self):
            return math.pi * self.r ** 2

    class Square(Shape):
        def __init__(self, s):
            self.s = s

        def area(self):
            return self.s ** 2

    kinds = {"circle": Circle, "square": Square}
    objects = [kinds[k](size) for k, size in shapes]
    return round(sum(shape.area() for shape in objects), 2)


Q(None, "Animal Sounds", "Easy", "Method overriding",
  "Given animal names ('dog', 'cat', 'cow'), return the list of their sounds ('Woof', 'Meow', 'Moo').",
  [((["dog", "cat", "cow"],), ["Woof", "Meow", "Moo"]), (([],), [])],
  ("An if/elif chain on the name.", "O(n)", "O(n)"),
  ("Each subclass overrides <code>speak()</code>; the caller doesn't care which animal it has.", "O(n)", "O(n)"),
  viz=(["dog", "cat"],))


@B
def sounds(names):
    out = []
    for n in names:
        if n == "dog":
            out.append("Woof")
        elif n == "cat":
            out.append("Meow")
        elif n == "cow":
            out.append("Moo")
    return out


@O
def sounds(names):
    class Animal:
        sound = "..."

        def speak(self):
            return self.sound

    class Dog(Animal):
        sound = "Woof"

    class Cat(Animal):
        sound = "Meow"

    class Cow(Animal):
        sound = "Moo"

    kinds = {"dog": Dog, "cat": Cat, "cow": Cow}
    return [kinds[n]().speak() for n in names]


Q(None, "Count Instances", "Medium", "Class attributes",
  "Create <code>n</code> Robot objects and return how many were created, counted by the class itself.",
  [((3,), 3), ((0,), 0)],
  ("A counter variable outside the class, incremented by hand after each creation.", "O(n)", "O(1)"),
  ("A class attribute shared by all instances, incremented in <code>__init__</code>.", "O(n)", "O(1)"),
  viz=(2,))


@B
def robots_made(n):
    class Robot:
        def __init__(self, serial):
            self.serial = serial

    made = 0
    for i in range(n):
        Robot(i)
        made += 1
    return made


@O
def robots_made(n):
    class Robot:
        count = 0

        def __init__(self):
            Robot.count += 1

    for _ in range(n):
        Robot()
    return Robot.count


Q(None, "Sort Employees by Salary", "Medium", "__lt__ for sorting",
  "Given (name, salary) pairs, return the names sorted by salary using Employee objects.",
  [(([("ana", 50), ("ben", 30), ("cy", 40)],), ["ben", "cy", "ana"])],
  ("Pass a key function that reads the attribute.", "O(n log n)", "O(n)"),
  ("Define <code>__lt__</code> so the objects themselves know how to compare; then plain <code>sorted()</code> works.", "O(n log n)", "O(n)"))


@B
def by_salary(pairs):
    class Employee:
        def __init__(self, name, salary):
            self.name = name
            self.salary = salary

    staff = [Employee(n, s) for n, s in pairs]
    staff.sort(key=lambda e: e.salary)
    return [e.name for e in staff]


@O
def by_salary(pairs):
    class Employee:
        def __init__(self, name, salary):
            self.name, self.salary = name, salary

        def __lt__(self, other):
            return self.salary < other.salary

    return [e.name for e in sorted(Employee(n, s) for n, s in pairs)]


Q(None, "Date From Text", "Medium", "@classmethod constructors",
  "Parse 'DD-MM-YYYY' into a Date object and return (year, month, day).",
  [(("25-12-2024",), (2024, 12, 25)), (("01-01-2000",), (2000, 1, 1))],
  ("Parse outside the class, then call the normal constructor.", "O(1)", "O(1)"),
  ("An alternative constructor <code>Date.from_string(text)</code> as a <code>@classmethod</code>.", "O(1)", "O(1)"))


@B
def parse_date(text):
    class Date:
        def __init__(self, day, month, year):
            self.day, self.month, self.year = day, month, year

    parts = text.split("-")
    d = Date(int(parts[0]), int(parts[1]), int(parts[2]))
    return (d.year, d.month, d.day)


@O
def parse_date(text):
    class Date:
        def __init__(self, day, month, year):
            self.day, self.month, self.year = day, month, year

        @classmethod
        def from_string(cls, s):
            day, month, year = map(int, s.split("-"))
            return cls(day, month, year)

    d = Date.from_string(text)
    return (d.year, d.month, d.day)


Q(None, "Car With an Engine", "Medium", "Composition",
  "A Car has an Engine. Return the messages from starting the car twice: ['Engine started', 'Already running'].",
  [((), ["Engine started", "Already running"])],
  ("One big class that tracks the engine state with its own flags.", "O(1)", "O(1)"),
  ("Composition: Car holds an Engine object and delegates <code>start()</code> to it — each class has one job.", "O(1)", "O(1)"))


@B
def start_twice():
    class Car:
        def __init__(self):
            self.engine_on = False

        def start(self):
            if self.engine_on:
                return "Already running"
            self.engine_on = True
            return "Engine started"

    car = Car()
    return [car.start(), car.start()]


@O
def start_twice():
    class Engine:
        def __init__(self):
            self.running = False

        def start(self):
            if self.running:
                return "Already running"
            self.running = True
            return "Engine started"

    class Car:
        def __init__(self):
            self.engine = Engine()

        def start(self):
            return self.engine.start()

    car = Car()
    return [car.start(), car.start()]


Q(None, "Equal Records", "Easy", "@dataclass equality",
  "Return True if two (name, id) records describe the same person, comparing objects with ==.",
  [((("Ana", 1), ("Ana", 1)), True), ((("Ana", 1), ("Ana", 2)), False)],
  ("A plain class: == compares identity, so define <code>__eq__</code> by hand.", "O(1)", "O(1)"),
  ("<code>@dataclass</code> generates <code>__init__</code>, <code>__repr__</code> and <code>__eq__</code> automatically.", "O(1)", "O(1)"))


@B
def same_person(a, b):
    class Record:
        def __init__(self, name, ident):
            self.name = name
            self.ident = ident

        def __eq__(self, other):
            return self.name == other.name and self.ident == other.ident

    return Record(*a) == Record(*b)


@O
def same_person(a, b):
    from dataclasses import dataclass

    @dataclass
    class Record:
        name: str
        ident: int

    return Record(*a) == Record(*b)
