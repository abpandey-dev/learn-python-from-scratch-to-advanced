from lib import *

LESSON("Basics", "Keys and values", """
<p>A list finds items by <b>position</b>. A <b>dictionary</b> (<code>dict</code>) finds them by a <b>key</b> you choose — like a real dictionary maps a word to its meaning.</p>
<pre><code class="py">phone = {"ana": "98450", "ben": "99001"}
phone["ana"]          # "98450"
phone["cy"] = "90000" # add a new pair
phone["ana"] = "11111" # update an existing key
len(phone)            # 3
"ben" in phone        # True — checks KEYS, not values</code></pre>
<p>Each entry is a <b>key: value</b> pair. Keys are unique (assigning to an existing key replaces its value) and must be unchangeable types like strings, numbers or tuples. Values can be anything.</p>
""", practice=["Two Lists to a Dict", "Safe Lookup"])


@LD
def dict_basics_demo():
    phone = {"ana": "98450", "ben": "99001"}
    phone["cy"] = "90000"
    phone["ana"] = "11111"
    has_ben = "ben" in phone
    print(phone["ana"], len(phone), has_ben)


LESSON("Basics", "Reading safely and removing", """
<p>Reading a key that doesn't exist raises <code>KeyError</code>. Safer options:</p>
<table>
<tr><th>Code</th><th>If the key is missing</th></tr>
<tr><td><code>d[key]</code></td><td>KeyError</td></tr>
<tr><td><code>d.get(key)</code></td><td>returns None</td></tr>
<tr><td><code>d.get(key, default)</code></td><td>returns default</td></tr>
<tr><td><code>if key in d:</code></td><td>check first</td></tr>
</table>
<p>Removing: <code>del d[key]</code> (KeyError if missing), <code>d.pop(key, default)</code> (removes and returns the value), <code>d.clear()</code>.</p>
""", practice=["Read a Nested Setting", "Safe Lookup"])


@LD
def get_demo():
    stock = {"pen": 10, "ink": 0}
    pens = stock.get("pen", 0)
    caps = stock.get("cap", 0)
    removed = stock.pop("ink", None)
    missing = stock.pop("glue", "not there")
    print(pens, caps, removed, missing, stock)


LESSON("Core", "Looping over a dictionary", """
<pre><code class="py">for name in marks:                 # keys
for m in marks.values():           # values
for name, m in marks.items():      # (key, value) pairs — most useful</code></pre>
<p><code>keys()</code>, <code>values()</code> and <code>items()</code> return live <b>views</b> that reflect later changes. Since Python 3.7, dicts keep keys in the order they were inserted.</p>
<div class="warn">Don't add or delete keys while looping over a dict — loop over <code>list(d)</code> instead.</div>
""", practice=["Total of All Values", "Key With the Largest Value", "Pass or Fail Report"])


@LD
def loop_dict_demo():
    marks = {"ana": 72, "ben": 35, "cy": 88}
    total = 0
    for name, m in marks.items():
        status = "pass" if m >= 40 else "fail"
        print(name, m, status)
        total += m
    print("average", round(total / len(marks), 1))


LESSON("Core", "Counting and grouping", """
<p>Two patterns cover most dictionary problems:</p>
<h4>Counting</h4>
<pre><code class="py">counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1</code></pre>
<h4>Grouping</h4>
<pre><code class="py">groups = {}
for w in words:
    groups.setdefault(w[0], []).append(w)</code></pre>
<p>The <code>collections</code> module makes them even shorter: <code>Counter(words)</code> counts, and <code>defaultdict(list)</code> creates an empty list the first time a key is used.</p>
""", practice=["Word Frequency", "Character Frequency", "Group Words by First Letter", "Group Anagrams", "Election Winner", "Total per Category"])


@LD
def counting_demo():
    words = ["red", "blue", "red", "green", "blue", "red"]
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    by_length = {}
    for w in words:
        by_length.setdefault(len(w), []).append(w)
    print(counts)
    print(by_length)


LESSON("Advanced", "Dict comprehensions and sorting", """
<pre><code class="py">squares = {n: n * n for n in range(5)}
passed = {name: m for name, m in marks.items() if m &gt;= 40}
inverted = {v: k for k, v in d.items()}</code></pre>
<p>Sorting a dict means sorting its keys or items:</p>
<pre><code class="py">sorted(d)                              # keys alphabetically
sorted(d, key=d.get, reverse=True)     # keys by value, highest first
sorted(d.items(), key=lambda kv: kv[1])# (key, value) pairs by value
max(d, key=d.get)                      # key with the largest value</code></pre>
<p>Merge dicts with <code>a | b</code> (Python 3.9+) or <code>{**a, **b}</code>; the right-hand side wins on shared keys.</p>
""", practice=["Invert a Dictionary", "Filter by Value", "Sort by Value", "Merge Dicts, Adding Values", "Most Common Word"])


@LD
def comprehension_demo():
    marks = {"ana": 72, "ben": 35, "cy": 88}
    passed = {n: m for n, m in marks.items() if m >= 40}
    ranking = sorted(marks, key=marks.get, reverse=True)
    best = max(marks, key=marks.get)
    merged = marks | {"dia": 91}
    print(passed, ranking, best, merged)


LESSON("Advanced", "Nested data and mappings", """
<p>Real data is often a dict of dicts or a list of dicts (this is what JSON looks like):</p>
<pre><code class="py">students = {
    "ana": {"age": 21, "skills": ["python", "sql"]},
    "ben": {"age": 25, "skills": ["java"]},
}
students["ana"]["skills"][0]                  # "python"
students.get("zed", {}).get("age")            # None, no error</code></pre>
<p>Dicts are also perfect as <b>lookup tables</b> (Roman numerals, prices) and for checking <b>one-to-one mappings</b> between two sequences (word patterns, isomorphic strings).</p>
""", practice=["Roman to Integer", "Word Pattern", "First Repeated Word"])


@LD
def nested_demo():
    students = {"ana": {"age": 21, "skills": ["python", "sql"]}, "ben": {"age": 25, "skills": ["java"]}}
    first_skill = students["ana"]["skills"][0]
    zed_age = students.get("zed", {}).get("age")
    students["ben"]["skills"].append("python")
    pythonistas = [name for name, info in students.items() if "python" in info["skills"]]
    print(first_skill, zed_age, pythonistas)
