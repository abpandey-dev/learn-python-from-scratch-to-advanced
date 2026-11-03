from lib import *

LESSON("Basics", "Creating strings", """
<p>A <b>string</b> (<code>str</code>) is a sequence of characters. You can write one with single, double or triple quotes:</p>
<pre><code class="py">a = 'single'
b = "double — can contain 'single' quotes"
c = &quot;&quot;&quot;triple quotes
span several lines&quot;&quot;&quot;</code></pre>
<p><b>Escape sequences</b> put special characters inside a string: <code>\\n</code> new line, <code>\\t</code> tab, <code>\\\\</code> a backslash, <code>\\"</code> a quote. A <b>raw string</b> <code>r"C:\\new"</code> keeps backslashes as they are.</p>
<p><code>len(s)</code> gives the number of characters. <code>+</code> joins strings and <code>*</code> repeats them.</p>
""")


@LD
def creating_demo():
    first = "Py"
    second = 'thon'
    word = first + second
    line = "-" * 10
    size = len(word)
    print(word, size)
    print(line)
    print("Tab:\tafter tab\nNew line")


LESSON("Basics", "Indexing and slicing", """
<p>Each character has a position. Python counts from 0 at the left, and from −1 at the right:</p>
<div class="pic"> P   y   t   h   o   n
 0   1   2   3   4   5
-6  -5  -4  -3  -2  -1</div>
<p><code>s[i]</code> gets one character. <code>s[start:stop:step]</code> gets a <b>slice</b> — stop is not included, and any part can be left out:</p>
<table>
<tr><th>Slice</th><th>Result for "Python"</th></tr>
<tr><td><code>s[0:2]</code></td><td>'Py'</td></tr>
<tr><td><code>s[2:]</code></td><td>'thon'</td></tr>
<tr><td><code>s[:-1]</code></td><td>'Pytho'</td></tr>
<tr><td><code>s[::2]</code></td><td>'Pto'</td></tr>
<tr><td><code>s[::-1]</code></td><td>'nohtyP'</td></tr>
</table>
<p><code>s[10]</code> raises IndexError, but slices never do: <code>s[2:100]</code> just stops at the end.</p>
""", practice=["Reverse a String", "Palindrome Word", "Mask a Card Number"])


@LD
def slicing_demo():
    s = "Python"
    first = s[0]
    last = s[-1]
    middle = s[1:4]
    every_second = s[::2]
    backwards = s[::-1]
    print(first, last, middle, every_second, backwards)


LESSON("Core", "Strings are immutable", """
<p>You can't change a character inside a string: <code>s[0] = "J"</code> raises <code>TypeError</code>. Every "change" creates a <b>new</b> string:</p>
<pre><code class="py">s = "Python"
s = "J" + s[1:]       # a new string "Jython"; the name s now points to it
t = s.upper()         # s is unchanged; t is a new string</code></pre>
<p>Because of this, building a string with <code>+=</code> in a long loop copies it again and again. Collect pieces in a list and join once at the end:</p>
<pre><code class="py">parts = []
for x in data:
    parts.append(str(x))
result = ",".join(parts)</code></pre>
""", practice=["Remove Vowels", "Replace Spaces", "Only Digits"])


@LD
def immutable_demo():
    s = "Python"
    t = s.upper()
    s = "J" + s[1:]
    parts = []
    for n in [1, 2, 3]:
        parts.append(str(n))
    joined = "-".join(parts)
    print(s, t, joined)


LESSON("Core", "The most useful string methods", """
<table>
<tr><th>Method</th><th>Does</th><th>Example → result</th></tr>
<tr><td><code>lower()</code> / <code>upper()</code></td><td>change case</td><td><code>"Hi".upper()</code> → 'HI'</td></tr>
<tr><td><code>title()</code> / <code>capitalize()</code></td><td>capital first letters</td><td><code>"a b".title()</code> → 'A B'</td></tr>
<tr><td><code>strip()</code></td><td>remove spaces at both ends</td><td><code>"  x ".strip()</code> → 'x'</td></tr>
<tr><td><code>split(sep)</code></td><td>cut into a list</td><td><code>"a,b".split(",")</code> → ['a', 'b']</td></tr>
<tr><td><code>sep.join(list)</code></td><td>glue a list together</td><td><code>"-".join(["a","b"])</code> → 'a-b'</td></tr>
<tr><td><code>replace(old, new)</code></td><td>replace all</td><td><code>"aa".replace("a","b")</code> → 'bb'</td></tr>
<tr><td><code>find(sub)</code></td><td>first index, or −1</td><td><code>"hello".find("l")</code> → 2</td></tr>
<tr><td><code>count(sub)</code></td><td>occurrences</td><td><code>"hello".count("l")</code> → 2</td></tr>
<tr><td><code>startswith</code> / <code>endswith</code></td><td>prefix / suffix test</td><td><code>"a.py".endswith(".py")</code> → True</td></tr>
<tr><td><code>isdigit</code>, <code>isalpha</code>, <code>isalnum</code>, <code>isspace</code></td><td>what kind of characters</td><td><code>"42".isdigit()</code> → True</td></tr>
</table>
""", practice=["Capitalise Each Word", "Count Words", "Count a Character", "Swap Case", "Title Initials"])


@LD
def methods_demo():
    raw = "  Learn Python, Have Fun  "
    clean = raw.strip()
    lower = clean.lower()
    words = lower.split(", ")
    joined = " | ".join(words)
    where = clean.find("Python")
    print(clean)
    print(words, joined, where)


LESSON("Core", "Working character by character", """
<p>Each character has a number, its <b>Unicode code point</b>: <code>ord("a")</code> is 97, and <code>chr(97)</code> is "a". Letters are consecutive, so arithmetic on codes lets you shift letters (Caesar cipher) or find a letter's position (<code>ord(c) − ord("a")</code>).</p>
<p>Characters compare by their codes, so <code>"a" &lt; "b"</code> and <code>"Z" &lt; "a"</code> (all capitals come before lower case).</p>
<p>Counting characters is a very common task — a dict (or <code>collections.Counter</code>) of character → count solves anagrams, most frequent and first unique character.</p>
""", practice=["Caesar Cipher", "Anagram Check", "Most Frequent Character", "First Non-Repeating Character", "Is It a Pangram?"])


@LD
def char_codes_demo():
    word = "abc"
    codes = [ord(c) for c in word]
    shifted = "".join(chr(code + 1) for code in codes)
    counts = {}
    for ch in "banana":
        counts[ch] = counts.get(ch, 0) + 1
    print(codes, shifted, counts)


LESSON("Advanced", "Formatting text", """
<p>f-strings support a <b>format specification</b> after a colon: <code>{value:fill align width .precision type}</code>.</p>
<table>
<tr><th>Spec</th><th>Meaning</th><th>Result</th></tr>
<tr><td><code>f"{3.14159:.2f}"</code></td><td>2 decimals</td><td>3.14</td></tr>
<tr><td><code>f"{42:5}"</code></td><td>width 5 (numbers align right)</td><td>"   42"</td></tr>
<tr><td><code>f"{'hi':*^8}"</code></td><td>centre in 8, fill with *</td><td>***hi***</td></tr>
<tr><td><code>f"{1234567:,}"</code></td><td>thousands separator</td><td>1,234,567</td></tr>
<tr><td><code>f"{0.075:.1%}"</code></td><td>percentage</td><td>7.5%</td></tr>
<tr><td><code>f"{255:b} {255:x}"</code></td><td>binary / hex</td><td>11111111 ff</td></tr>
<tr><td><code>f"{x=}"</code></td><td>debug: name and value</td><td>x=5</td></tr>
</table>
<p>Grouping repeated characters (run-length encoding) and validating text are classic exercises that combine loops, conditions and methods.</p>
""", practice=["Centre a Title", "Compress Repeated Letters", "Valid Username", "Longest Word"])


@LD
def format_demo():
    items = [("Pen", 1.5), ("Notebook", 12.25)]
    for name, price in items:
        print(f"{name:<10}|{price:>8.2f}")
    total = sum(p for _, p in items)
    print(f"{'TOTAL':*^18}")
    print(f"{total=}", f"{0.075:.1%}")
