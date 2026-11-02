from lib import *

THEORY("Definition", """
<p><b>Bit manipulation</b> is the act of using bitwise operators to read, set, clear or combine the individual binary digits (<b>bits</b>) of integers. Because processors execute bitwise operations in a single instruction, these techniques are extremely fast and memory-efficient.</p>
<p>A <b>bit</b> is 0 or 1. A <b>byte</b> is 8 bits. A <b>word</b> is the processor's natural integer size (32 or 64 bits). The <b>least significant bit (LSB)</b> is bit 0 (worth 1); the <b>most significant bit (MSB)</b> is the highest position.</p>
""")

THEORY("Number systems", """
<table>
<tr><th>System</th><th>Base</th><th>Digits</th><th>13 written as</th><th>Python</th></tr>
<tr><td>Binary</td><td>2</td><td>0–1</td><td>1101</td><td><code>0b1101</code>, <code>bin(13)</code></td></tr>
<tr><td>Octal</td><td>8</td><td>0–7</td><td>15</td><td><code>0o15</code>, <code>oct(13)</code></td></tr>
<tr><td>Decimal</td><td>10</td><td>0–9</td><td>13</td><td><code>13</code></td></tr>
<tr><td>Hexadecimal</td><td>16</td><td>0–9, A–F</td><td>D</td><td><code>0xD</code>, <code>hex(13)</code></td></tr>
</table>
<p><b>Binary → decimal</b>: sum bitᵢ × 2ⁱ. <b>Decimal → binary</b>: repeatedly divide by 2 and read the remainders bottom-up. Each hex digit is exactly 4 bits.</p>
""")

THEORY("Bitwise operators and truth table", """
<table>
<tr><th>A</th><th>B</th><th>A &amp; B</th><th>A | B</th><th>A ^ B</th></tr>
<tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>0</td><td>1</td><td>0</td><td>1</td><td>1</td></tr>
<tr><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td></tr>
<tr><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td></tr>
</table>
<table>
<tr><th>Operator</th><th>Name</th><th>Effect</th></tr>
<tr><td><code>~x</code></td><td>NOT</td><td>flips every bit; in two's complement <code>~x = −x − 1</code></td></tr>
<tr><td><code>x &lt;&lt; k</code></td><td>left shift</td><td>x × 2ᵏ</td></tr>
<tr><td><code>x &gt;&gt; k</code></td><td>right shift</td><td>⌊x / 2ᵏ⌋ (arithmetic shift keeps the sign for negatives)</td></tr>
</table>
<h4>Algebraic laws of XOR</h4>
<ul>
<li>Identity: <code>x ^ 0 = x</code>; self-inverse: <code>x ^ x = 0</code></li>
<li>Commutative and associative: order and grouping don't matter</li>
<li>Therefore <code>a ^ b ^ a = b</code>, and <code>a ^ b = c ⇔ a = b ^ c</code></li>
</ul>
""")

THEORY("Representing negative numbers", """
<table>
<tr><th>Scheme</th><th>−5 in 8 bits</th><th>Notes</th></tr>
<tr><td>Sign-magnitude</td><td>1000 0101</td><td>MSB is the sign; two zeros (+0, −0)</td></tr>
<tr><td>One's complement</td><td>1111 1010</td><td>flip all bits; still two zeros</td></tr>
<tr><td><b>Two's complement</b></td><td>1111 1011</td><td>flip all bits and add 1; one zero; used by all modern CPUs</td></tr>
</table>
<p>In n-bit two's complement the range is −2ⁿ⁻¹ … 2ⁿ⁻¹ − 1 (for 32 bits: −2,147,483,648 … 2,147,483,647). Addition and subtraction work the same for signed and unsigned values, which is why hardware uses it.</p>
<p><b>Overflow</b> happens when a result is outside the range and wraps around (e.g. 2³¹ − 1 + 1 becomes −2³¹ in 32 bits). Python integers are arbitrary precision and never overflow — mask with <code>&amp; 0xFFFFFFFF</code> to simulate 32-bit behaviour.</p>
""")

THEORY("Standard bit tricks", """
<table>
<tr><th>Task</th><th>Expression</th></tr>
<tr><td>Check if bit i is set</td><td><code>(n &gt;&gt; i) &amp; 1</code> or <code>n &amp; (1 &lt;&lt; i) != 0</code></td></tr>
<tr><td>Set / clear / toggle bit i</td><td><code>n | (1 &lt;&lt; i)</code> / <code>n &amp; ~(1 &lt;&lt; i)</code> / <code>n ^ (1 &lt;&lt; i)</code></td></tr>
<tr><td>Is n even?</td><td><code>n &amp; 1 == 0</code></td></tr>
<tr><td>Is n a power of 2?</td><td><code>n &gt; 0 and n &amp; (n − 1) == 0</code></td></tr>
<tr><td>Clear lowest set bit</td><td><code>n &amp; (n − 1)</code></td></tr>
<tr><td>Isolate lowest set bit</td><td><code>n &amp; −n</code></td></tr>
<tr><td>Count set bits (Kernighan)</td><td><code>while n: n &amp;= n − 1; count += 1</code></td></tr>
<tr><td>Mask of the lowest k bits</td><td><code>(1 &lt;&lt; k) − 1</code></td></tr>
<tr><td>Swap without temp</td><td><code>a ^= b; b ^= a; a ^= b</code></td></tr>
<tr><td>Iterate all subsets of n items</td><td><code>for mask in range(1 &lt;&lt; n)</code></td></tr>
<tr><td>Iterate submasks of mask</td><td><code>s = mask; while s: …; s = (s − 1) &amp; mask</code></td></tr>
</table>
""")

THEORY("Advantages, disadvantages and applications", """
<div class="two">
<div class="pro"><h5>Advantages</h5><ul><li>Single-instruction speed</li><li>Compact storage: 64 booleans in one integer (bitsets)</li><li>Elegant O(1)-space solutions (XOR tricks)</li></ul></div>
<div class="con"><h5>Disadvantages</h5><ul><li>Hard to read; easy to make precedence mistakes</li><li>Sign and overflow behaviour differs between languages</li><li>Gains are often irrelevant next to algorithmic improvements</li></ul></div>
</div>
<h4>Applications</h4>
<ul>
<li>Permissions and feature flags (Unix file modes like <code>0o755</code>).</li>
<li>Bitsets / Bloom filters for compact membership tests.</li>
<li>Graphics: colours packed as 0xRRGGBB; masks and blending.</li>
<li>Networking: IP subnet masks, checksums, protocol headers.</li>
<li>Cryptography and hashing (XOR, rotations, shifts).</li>
<li>Compression and error-detecting codes (parity, Hamming codes, Gray codes in encoders).</li>
<li>Bitmask DP and subset enumeration in algorithms.</li>
</ul>
""")

FAQ("How do you check whether a number is a power of two?", "<p><code>n &gt; 0 and n &amp; (n − 1) == 0</code>. A power of two has exactly one set bit; subtracting 1 turns it off and sets all lower bits, so the AND is 0.</p>")
FAQ("Why does <code>n &amp; (n − 1)</code> remove the lowest set bit?", "<p>Subtracting 1 flips the lowest 1-bit to 0 and every 0-bit below it to 1, leaving higher bits unchanged. ANDing with n keeps the higher bits and clears everything from the lowest set bit down.</p>")
FAQ("What is two's complement and why is it used?", "<p>Negative x is stored as (bitwise NOT of x) + 1. It has a single zero and lets the same adder circuit handle signed and unsigned arithmetic, so CPUs use it universally.</p>")
FAQ("How do you find the element that appears once when every other appears twice?", "<p>XOR all elements. Equal pairs cancel to 0 (x ^ x = 0), and 0 ^ y = y, leaving the unique element. O(n) time, O(1) space.</p>")
FAQ("Left shift vs right shift?", "<p><code>x &lt;&lt; k</code> moves bits left, filling with zeros — multiplies by 2ᵏ. <code>x &gt;&gt; k</code> moves bits right — floor-divides by 2ᵏ. Arithmetic right shift copies the sign bit; logical right shift (Java's <code>&gt;&gt;&gt;</code>) fills with zeros.</p>")
FAQ("How do you count set bits efficiently?", "<p>Brian Kernighan's loop (<code>n &amp;= n − 1</code> until 0) runs once per set bit. Built-ins: <code>bin(n).count('1')</code> or <code>n.bit_count()</code>. For 0..n, use DP: <code>bits[i] = bits[i &gt;&gt; 1] + (i &amp; 1)</code>.</p>")
FAQ("Why do Python bit problems sometimes need <code>&amp; 0xFFFFFFFF</code>?", "<p>Python ints are unbounded, so negatives behave as if they had infinitely many leading 1s and loops like carry propagation never terminate. Masking to 32 bits simulates fixed-width integers; convert back with <code>x − 2**32</code> when the top bit is set.</p>")
