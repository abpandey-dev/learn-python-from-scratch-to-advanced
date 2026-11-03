from lib import *

THEORY("Definition", """
<p>A <b>string</b> is an <b>immutable sequence of Unicode characters</b>. In Python its type is <code>str</code>. There is no separate character type — a single character is a string of length 1.</p>
<p>As a <b>sequence</b>, a string supports indexing, slicing, <code>len()</code>, iteration, membership (<code>in</code>), concatenation (<code>+</code>) and repetition (<code>*</code>).</p>
""")

THEORY("Creating strings and escape sequences", """
<table>
<tr><th>Literal</th><th>Use</th></tr>
<tr><td><code>'text'</code>, <code>"text"</code></td><td>identical; pick the one that avoids escaping quotes inside</td></tr>
<tr><td><code>&#39;&#39;&#39;text&#39;&#39;&#39;</code>, <code>&quot;&quot;&quot;text&quot;&quot;&quot;</code></td><td>multi-line strings, docstrings</td></tr>
<tr><td><code>r"C:\\path"</code></td><td>raw string — backslashes are literal (regex, Windows paths)</td></tr>
<tr><td><code>f"Hi {name}"</code></td><td>formatted string literal (f-string)</td></tr>
<tr><td><code>b"bytes"</code></td><td>bytes, not text (binary data)</td></tr>
</table>
<table>
<tr><th>Escape</th><th>Meaning</th></tr>
<tr><td><code>\\n</code></td><td>new line</td></tr>
<tr><td><code>\\t</code></td><td>tab</td></tr>
<tr><td><code>\\\\</code></td><td>backslash</td></tr>
<tr><td><code>\\'</code> <code>\\"</code></td><td>quote</td></tr>
<tr><td><code>\\u20B9</code></td><td>Unicode character (₹)</td></tr>
</table>
""")

THEORY("Indexing and slicing rules", """
<ul>
<li>Positive indices run 0 … len − 1 from the left; negative indices run −1 … −len from the right.</li>
<li><code>s[i]</code> outside the range raises <code>IndexError</code>.</li>
<li><code>s[start:stop:step]</code> returns a new string with characters from start up to (not including) stop.</li>
<li>Missing start/stop default to the ends; missing step defaults to 1.</li>
<li>Out-of-range slice bounds are clipped, never an error.</li>
<li>A negative step walks backwards; then the defaults are reversed: <code>s[::-1]</code> is the reverse.</li>
<li><code>s[:k] + s[k:] == s</code> for any k.</li>
</ul>
""")

THEORY("Immutability", """
<p>Once created, a string object can never change. Assignment to an index (<code>s[0] = 'x'</code>) raises <code>TypeError</code>, and methods like <code>upper()</code> or <code>replace()</code> return <b>new</b> strings.</p>
<h4>Why immutable?</h4>
<ul>
<li>Strings can be <b>dictionary keys</b> and set members (their hash never changes).</li>
<li>They are safe to share between variables and threads.</li>
<li>Python can reuse identical small strings (<b>interning</b>).</li>
</ul>
<h4>Consequence</h4>
<p>Repeated <code>s += piece</code> in a loop may copy the string every time — O(n²) in total. The idiom is to collect pieces in a list and call <code>"".join(pieces)</code> once — O(n).</p>
""")

THEORY("Methods by category", """
<table>
<tr><th>Category</th><th>Methods</th></tr>
<tr><td>Case</td><td><code>lower upper title capitalize swapcase casefold</code></td></tr>
<tr><td>Whitespace</td><td><code>strip lstrip rstrip</code></td></tr>
<tr><td>Search</td><td><code>find rfind index rindex count startswith endswith</code>, operator <code>in</code></td></tr>
<tr><td>Replace / split / join</td><td><code>replace split rsplit splitlines partition join</code></td></tr>
<tr><td>Tests (return bool)</td><td><code>isdigit isnumeric isalpha isalnum isspace isupper islower istitle</code></td></tr>
<tr><td>Alignment</td><td><code>center ljust rjust zfill</code></td></tr>
<tr><td>Encoding</td><td><code>encode</code> (str → bytes); <code>bytes.decode</code></td></tr>
</table>
<p><code>find</code> returns −1 when not found; <code>index</code> raises <code>ValueError</code>. Built-ins that work on strings: <code>len, ord, chr, str, sorted, reversed, min, max</code>.</p>
""")

THEORY("String comparison and Unicode", """
<p>Strings compare <b>lexicographically</b> by Unicode code points, character by character: <code>"apple" &lt; "banana"</code>, <code>"Zebra" &lt; "apple"</code> (uppercase codes 65–90 come before lowercase 97–122), and <code>"app" &lt; "apple"</code> (a prefix is smaller).</p>
<p>For case-insensitive comparison use <code>a.casefold() == b.casefold()</code>. Python 3 strings are Unicode, so they hold any language: <code>len("नमस्ते")</code> counts code points.</p>
""")

FAQ("Why are strings immutable in Python?", "<p>So their hash value never changes (making them usable as dict keys and set items), so they can be shared safely, and so Python can optimise memory by reusing them.</p>")
FAQ("find() vs index()?", "<p>Both return the first position of a substring. <code>find</code> returns −1 if it's missing; <code>index</code> raises <code>ValueError</code>.</p>")
FAQ("How do you reverse a string?", "<p><code>s[::-1]</code>, or <code>''.join(reversed(s))</code>.</p>")
FAQ("Why use join instead of + in a loop?", "<p>Each <code>+</code> creates a new string and copies the old content, so building a string of n pieces costs O(n²). <code>''.join(list)</code> computes the final size once and copies each piece once — O(n).</p>")
FAQ("What is the difference between split() and split(' ')?", "<p><code>split()</code> splits on any run of whitespace and drops empty pieces at the ends. <code>split(' ')</code> splits on every single space, so double spaces produce empty strings.</p>")
FAQ("What does <code>s[::-1]</code> mean?", "<p>A slice from the end to the start with step −1 — every character in reverse order.</p>")
FAQ("isdigit vs isnumeric vs isdecimal?", "<p>All test for number characters. <code>isdecimal</code> is strictest (0–9 and other decimal digits), <code>isdigit</code> also accepts superscripts like ², and <code>isnumeric</code> also accepts fractions and numerals like ½ or Ⅻ. For simple input checks <code>isdigit</code> is usual.</p>")
