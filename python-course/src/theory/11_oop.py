from lib import *

THEORY("Definition", """
<p><b>Object-oriented programming (OOP)</b> is a programming paradigm that organises software around <b>objects</b> — bundles of data (<b>attributes</b>, state) and behaviour (<b>methods</b>) — rather than around functions and logic alone.</p>
<ul>
<li>A <b>class</b> is a user-defined type: the blueprint describing what attributes and methods its objects have.</li>
<li>An <b>object</b> (instance) is a concrete value created from a class, with its own attribute values.</li>
<li>In Python <i>everything</i> is an object — ints, functions and classes themselves.</li>
</ul>
""")

THEORY("The four pillars", """
<table>
<tr><th>Pillar</th><th>Meaning</th><th>In Python</th></tr>
<tr><td><b>Encapsulation</b></td><td>bundle data with the methods that operate on it; restrict direct access</td><td>methods, <code>_internal</code> naming, <code>__name_mangling</code>, <code>@property</code></td></tr>
<tr><td><b>Abstraction</b></td><td>expose what an object does, hide how</td><td>clear public methods; abstract base classes (<code>abc.ABC</code>, <code>@abstractmethod</code>)</td></tr>
<tr><td><b>Inheritance</b></td><td>a class reuses and extends another (IS-A)</td><td><code>class Dog(Animal)</code>, <code>super()</code>, multiple inheritance with MRO</td></tr>
<tr><td><b>Polymorphism</b></td><td>one interface, many implementations</td><td>method overriding, duck typing, operator overloading</td></tr>
</table>
""")

THEORY("Class anatomy", """
<table>
<tr><th>Element</th><th>Description</th></tr>
<tr><td><code>__init__(self, …)</code></td><td>initialiser, runs after the object is created (the constructor proper is <code>__new__</code>)</td></tr>
<tr><td><code>self</code></td><td>reference to the current instance; first parameter of instance methods (a convention, not a keyword)</td></tr>
<tr><td>Instance attribute</td><td><code>self.x = …</code> — stored per object (in <code>obj.__dict__</code>)</td></tr>
<tr><td>Class attribute</td><td>assigned in the class body — shared by all instances</td></tr>
<tr><td>Instance method</td><td>receives <code>self</code></td></tr>
<tr><td><code>@classmethod</code></td><td>receives the class (<code>cls</code>); used for factory constructors</td></tr>
<tr><td><code>@staticmethod</code></td><td>receives nothing implicit; a namespaced helper</td></tr>
<tr><td><code>@property</code></td><td>method accessed like an attribute; optional setter with <code>@x.setter</code></td></tr>
</table>
<p>Attribute lookup on <code>obj.name</code>: the instance's <code>__dict__</code> first, then the class, then the parent classes in <b>MRO</b> (method resolution order, see <code>Class.__mro__</code>).</p>
""")

THEORY("Inheritance in detail", """
<table>
<tr><th>Type</th><th>Shape</th></tr>
<tr><td>Single</td><td>B(A)</td></tr>
<tr><td>Multilevel</td><td>C(B), B(A)</td></tr>
<tr><td>Hierarchical</td><td>B(A), C(A)</td></tr>
<tr><td>Multiple</td><td>C(A, B)</td></tr>
<tr><td>Hybrid</td><td>a combination (e.g. diamond: D(B, C), B(A), C(A))</td></tr>
</table>
<ul>
<li><b>Overriding</b>: a subclass defines a method with the same name; <code>super().method()</code> calls the parent's version.</li>
<li>Python resolves multiple inheritance with the <b>C3 linearisation</b> (MRO), so each class appears once in a predictable order.</li>
<li><code>isinstance(obj, Class)</code> and <code>issubclass(B, A)</code> test relationships.</li>
<li><b>Composition over inheritance</b>: prefer HAS-A relationships unless IS-A is genuinely true.</li>
</ul>
""")

THEORY("Polymorphism and duck typing", """
<p>Python is <b>duck-typed</b>: "if it walks like a duck and quacks like a duck, it's a duck". Code works with any object that has the needed methods, regardless of its class. That's why <code>len()</code> works on strings, lists and your own classes with <code>__len__</code>.</p>
<p>Python does not support method <b>overloading</b> by signature (defining the same method twice with different parameters). Use default values, <code>*args</code>, or <code>functools.singledispatch</code> instead.</p>
<h4>Common special methods</h4>
<p><code>__init__ __repr__ __str__ __eq__ __lt__ __hash__ __len__ __contains__ __getitem__ __setitem__ __iter__ __next__ __add__ __sub__ __mul__ __call__ __enter__ __exit__ __bool__</code></p>
<p>Rule: if you define <code>__eq__</code>, define <code>__hash__</code> too (or the objects become unhashable).</p>
""")

THEORY("Dataclasses and when to use OOP", """
<p><code>@dataclass</code> (Python 3.7+) generates <code>__init__</code>, <code>__repr__</code> and <code>__eq__</code> from annotated fields; options add ordering (<code>order=True</code>), immutability (<code>frozen=True</code>) and defaults.</p>
<pre><code class="py">from dataclasses import dataclass, field
@dataclass
class Item:
    name: str
    price: float = 0.0
    tags: list = field(default_factory=list)</code></pre>
<p>Use classes when data and the rules for changing it belong together, when you have many similar things, or when you need several interchangeable implementations. For a simple bag of data, a dict, tuple or dataclass is enough.</p>
""")

FAQ("Class vs object?", "<p>A class is the blueprint (a type); an object is an instance created from it, with its own attribute values.</p>")
FAQ("What is <code>self</code>?", "<p>The instance on which a method is called. Python passes it automatically: <code>obj.method(x)</code> is <code>Class.method(obj, x)</code>. The name is a convention.</p>")
FAQ("What does <code>__init__</code> do? Is it a constructor?", "<p>It initialises a newly created object's attributes. The object itself is created by <code>__new__</code> just before; in everyday speech <code>__init__</code> is called the constructor.</p>")
FAQ("Class attribute vs instance attribute?", "<p>A class attribute is defined in the class body and shared by all instances. An instance attribute is set on <code>self</code> and belongs to one object. Assigning <code>obj.attr = …</code> creates an instance attribute that hides the class one.</p>")
FAQ("@staticmethod vs @classmethod?", "<p>A classmethod receives the class as <code>cls</code> and can create instances (alternative constructors) or use class state. A staticmethod receives nothing automatically; it's just a function grouped inside the class.</p>")
FAQ("What are the four pillars of OOP?", "<p>Encapsulation, abstraction, inheritance and polymorphism.</p>")
FAQ("Does Python support private attributes?", "<p>Not strictly. <code>_name</code> signals 'internal'. <code>__name</code> triggers name mangling to <code>_Class__name</code>, which avoids accidental clashes in subclasses but can still be accessed.</p>")
FAQ("What is method overriding? Does Python support overloading?", "<p>Overriding: a subclass redefines a parent method. Python does not support overloading by parameter types/counts — the last definition wins — so use default arguments or *args.</p>")
FAQ("What is MRO?", "<p>Method Resolution Order: the order Python searches classes for an attribute, especially with multiple inheritance. It's computed with C3 linearisation and visible as <code>Class.__mro__</code>.</p>")
