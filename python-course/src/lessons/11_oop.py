from lib import *

LESSON("Basics", "Classes and objects", """
<p>So far data (variables) and actions (functions) lived separately. <b>Object-oriented programming</b> bundles them together. A <b>class</b> is a blueprint; an <b>object</b> (instance) is one thing built from it.</p>
<pre><code class="py">class Dog:                         # the blueprint
    def __init__(self, name):      # runs when a Dog is created
        self.name = name           # an attribute stored on this object
    def bark(self):                # a method: a function that belongs to the class
        return self.name + " says woof"

rex = Dog("Rex")                   # create an object
rex.bark()                         # "Rex says woof"</code></pre>
<p><code>self</code> is the object the method was called on. <code>rex.bark()</code> is really <code>Dog.bark(rex)</code>. In the animation, the box for <code>self</code> shows the object's attributes as they're set.</p>
""", practice=["Rectangle Class", "Click Counter"])


@LD
def class_demo():
    class Dog:
        def __init__(self, name):
            self.name = name
            self.tricks = []

        def learn(self, trick):
            self.tricks.append(trick)

    rex = Dog("Rex")
    rex.learn("sit")
    rex.learn("roll")
    fido = Dog("Fido")
    print(rex.name, rex.tricks, fido.tricks)


LESSON("Basics", "Methods that change an object's state", """
<p>An object remembers its attributes between method calls, so methods can update them. That's the main reason to use a class: the data and the rules for changing it stay together.</p>
<pre><code class="py">class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
    def deposit(self, amount):
        self.balance += amount
    def withdraw(self, amount):
        if amount &gt; self.balance:
            return False
        self.balance -= amount
        return True</code></pre>
<p>Each object has its <b>own</b> attributes: two accounts don't share a balance.</p>
""", practice=["Bank Account", "Student Average", "Shopping Cart", "Library Loans"])


@LD
def state_demo():
    class BankAccount:
        def __init__(self, balance=0):
            self.balance = balance

        def deposit(self, amount):
            self.balance += amount

        def withdraw(self, amount):
            if amount > self.balance:
                return False
            self.balance -= amount
            return True

    acc = BankAccount(100)
    acc.deposit(50)
    ok = acc.withdraw(500)
    print(acc.balance, ok)


LESSON("Core", "Class attributes, @classmethod and @staticmethod", """
<ul>
<li><b>Instance attributes</b> (<code>self.x</code>) belong to one object.</li>
<li><b>Class attributes</b> (written in the class body) are shared by all objects — e.g. a counter of instances.</li>
<li><code>@classmethod</code> receives the class (<code>cls</code>) instead of an object — used for alternative constructors like <code>Date.from_string("25-12-2024")</code>.</li>
<li><code>@staticmethod</code> receives neither — a plain helper that lives in the class's namespace.</li>
</ul>
""", practice=["Count Instances", "Date From Text"])


@LD
def class_attr_demo():
    class Robot:
        count = 0

        def __init__(self, name):
            self.name = name
            Robot.count += 1

        @classmethod
        def from_code(cls, code):
            return cls("R-" + code)

    a = Robot("Ava")
    b = Robot.from_code("42")
    print(Robot.count, b.name)


LESSON("Core", "Encapsulation and properties", """
<p><b>Encapsulation</b> means keeping an object's data valid by changing it only through its methods. Python has no truly private attributes; by convention a leading underscore (<code>self._age</code>) means "internal, don't touch from outside".</p>
<p>A <b>property</b> lets you compute or validate a value while still reading it like an attribute:</p>
<pre><code class="py">class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius
    @property
    def fahrenheit(self):              # read as t.fahrenheit (no brackets)
        return self.celsius * 9 / 5 + 32</code></pre>
""", practice=["Temperature With a Property", "Protected Age"])


@LD
def property_demo():
    class Temperature:
        def __init__(self, celsius):
            self.celsius = celsius

        @property
        def fahrenheit(self):
            return self.celsius * 9 / 5 + 32

    t = Temperature(25)
    before = t.fahrenheit
    t.celsius = 100
    after = t.fahrenheit
    print(before, after)


LESSON("Core", "Inheritance and polymorphism", """
<p><b>Inheritance</b>: a class can extend another, reusing its attributes and methods. The new class can <b>override</b> methods and call the parent's version with <code>super()</code>.</p>
<pre><code class="py">class Animal:
    def __init__(self, name): self.name = name
    def speak(self): return "..."
class Dog(Animal):                  # Dog IS-A Animal
    def speak(self): return "Woof"</code></pre>
<p><b>Polymorphism</b>: code that calls <code>animal.speak()</code> works for any animal, and each object answers in its own way — no if/elif on the type needed.</p>
<p><b>Composition</b> ("HAS-A") is the alternative: a Car <i>has</i> an Engine object. Prefer composition when the relationship isn't truly "is a kind of".</p>
""", practice=["Animal Sounds", "Total Area of Shapes", "Car With an Engine"])


@LD
def inheritance_demo():
    class Animal:
        def __init__(self, name):
            self.name = name

        def speak(self):
            return "..."

        def intro(self):
            return f"{self.name}: {self.speak()}"

    class Dog(Animal):
        def speak(self):
            return "Woof"

    class Cat(Animal):
        def speak(self):
            return "Meow"

    for pet in [Dog("Rex"), Cat("Tom"), Animal("Fish")]:
        print(pet.intro())


LESSON("Advanced", "Special (dunder) methods", """
<p>Methods with double underscores let your objects work with Python's built-in syntax:</p>
<table>
<tr><th>Method</th><th>Makes this work</th></tr>
<tr><td><code>__init__</code></td><td><code>Obj(args)</code> — set up a new object</td></tr>
<tr><td><code>__str__</code> / <code>__repr__</code></td><td><code>print(obj)</code> / how it looks in the shell and in lists</td></tr>
<tr><td><code>__eq__</code>, <code>__lt__</code></td><td><code>a == b</code>, <code>a &lt; b</code>, and therefore <code>sorted()</code></td></tr>
<tr><td><code>__add__</code>, <code>__mul__</code> …</td><td><code>a + b</code>, <code>a * b</code> (operator overloading)</td></tr>
<tr><td><code>__len__</code>, <code>__contains__</code></td><td><code>len(obj)</code>, <code>x in obj</code></td></tr>
<tr><td><code>__getitem__</code>, <code>__iter__</code></td><td><code>obj[i]</code>, <code>for x in obj</code></td></tr>
</table>
<p><code>@dataclass</code> writes <code>__init__</code>, <code>__repr__</code> and <code>__eq__</code> for you from type-annotated fields.</p>
""", practice=["Add Two Points", "Readable Object Text", "Playlist With len and in", "Sort Employees by Salary", "Equal Records"])


@LD
def dunder_demo():
    class Vector:
        def __init__(self, x, y):
            self.x, self.y = x, y

        def __add__(self, other):
            return Vector(self.x + other.x, self.y + other.y)

        def __eq__(self, other):
            return (self.x, self.y) == (other.x, other.y)

        def __repr__(self):
            return f"Vector({self.x}, {self.y})"

    v = Vector(1, 2) + Vector(3, 4)
    print(v, v == Vector(4, 6))
