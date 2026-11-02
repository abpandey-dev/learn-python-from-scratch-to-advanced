from lib import *

LESSON("Basics", "Binary numbers", """
<p>Computers store numbers in <b>base 2</b>: each digit (a <b>bit</b>) is 0 or 1, and each position is worth double the one to its right.</p>
<div class="pic">bit position:   3   2   1   0
worth:          8   4   2   1
13 in binary:   1   1   0   1     → 8 + 4 + 1 = 13</div>
<p>To convert a number to binary, repeatedly divide by 2; the remainders, read from last to first, are the bits. In Python: <code>bin(13)</code> → <code>'0b1101'</code>, <code>int('1101', 2)</code> → 13, <code>format(13, '08b')</code> → <code>'00001101'</code>.</p>
<p>An n-bit number ranges from 0 to 2ⁿ − 1, so 32 bits hold about 4 billion values.</p>
""", practice=[191])


@LD
def to_binary_lesson():
    n = 13
    bits, x = [], n
    while x:
        bits.append(x % 2)
        T(f"{x} ÷ 2 = {x // 2}, remainder {x % 2} → next bit (right to left)", V(number=x, remainder=x % 2), A("bits so far (lowest first)", bits, hl=[len(bits) - 1]))
        x //= 2
    T(f"Read the remainders backwards: {n} = {''.join(map(str, reversed(bits)))}", BITS(str(n), n, 4, ok=[i for i in range(4) if n >> i & 1]))
    return bits


LESSON("Basics", "The six operators", """
<table>
<tr><th>Op</th><th>Name</th><th>Rule per bit</th><th>5 (0101) with 3 (0011)</th></tr>
<tr><td><code>&amp;</code></td><td>AND</td><td>1 if both are 1</td><td>0001 = 1</td></tr>
<tr><td><code>|</code></td><td>OR</td><td>1 if either is 1</td><td>0111 = 7</td></tr>
<tr><td><code>^</code></td><td>XOR</td><td>1 if they differ</td><td>0110 = 6</td></tr>
<tr><td><code>~</code></td><td>NOT</td><td>flip every bit</td><td><code>~5 = −6</code> in Python</td></tr>
<tr><td><code>&lt;&lt;</code></td><td>left shift</td><td>move bits left, add 0s</td><td><code>5 &lt;&lt; 1</code> = 1010 = 10</td></tr>
<tr><td><code>&gt;&gt;</code></td><td>right shift</td><td>move bits right, drop the last</td><td><code>5 &gt;&gt; 1</code> = 0010 = 2</td></tr>
</table>
<p><code>x &lt;&lt; k</code> multiplies by 2ᵏ and <code>x &gt;&gt; k</code> divides by 2ᵏ (rounding down). The topic's quick-reference animation steps through all of these.</p>
""")


LESSON("Core", "Working with one bit", """
<p>Build a <b>mask</b> with a single 1 at position i: <code>1 &lt;&lt; i</code>. Then:</p>
<table>
<tr><th>Goal</th><th>Code</th></tr>
<tr><td>read bit i</td><td><code>(n &gt;&gt; i) &amp; 1</code></td></tr>
<tr><td>set bit i to 1</td><td><code>n | (1 &lt;&lt; i)</code></td></tr>
<tr><td>clear bit i to 0</td><td><code>n &amp; ~(1 &lt;&lt; i)</code></td></tr>
<tr><td>toggle bit i</td><td><code>n ^ (1 &lt;&lt; i)</code></td></tr>
<tr><td>lowest set bit only</td><td><code>n &amp; -n</code></td></tr>
<tr><td>remove lowest set bit</td><td><code>n &amp; (n - 1)</code></td></tr>
</table>
<p><code>n &amp; (n − 1)</code> works because subtracting 1 flips the lowest 1 to 0 and every 0 below it to 1; the AND clears them all. It counts set bits in as many steps as there are 1s, and <code>n &amp; (n − 1) == 0</code> means n is a power of two.</p>
""", practice=[191, 231, 342, 338])


@LD
def single_bit_lesson():
    n, i = 0b1010, 2
    T(f"Start with n = {n}; we'll work on bit {i}", BITS("n", n, 4, hl=[i]), BITS("mask 1 << 2", 1 << i, 4, ok=[i]))
    T(f"Read: (n >> {i}) & 1 = {(n >> i) & 1}", BITS("n", n, 4, hl=[i]), V(bit=(n >> i) & 1))
    s = n | (1 << i)
    T("Set: n | mask turns bit 2 on", BITS("n | mask", s, 4, ok=[i]))
    c = s & ~(1 << i)
    T("Clear: n & ~mask turns it off again", BITS("n & ~mask", c, 4, hl=[i]))
    t = n ^ (1 << 1)
    T("Toggle bit 1: n ^ (1 << 1) flips just that bit", BITS("n", n, 4, hl=[1]), BITS("n ^ (1 << 1)", t, 4, hl=[1]))
    return t


LESSON("Core", "XOR, the cancelling operator", """
<p>XOR has three properties that solve a whole class of problems:</p>
<ul>
<li><code>x ^ x = 0</code> — equal values cancel.</li>
<li><code>x ^ 0 = x</code> — zero changes nothing.</li>
<li>Order doesn't matter: <code>a ^ b ^ a = b</code>.</li>
</ul>
<p>So XOR-ing a list where everything appears twice except one value leaves exactly that value — O(n) time, O(1) memory. The same works for characters (find the extra letter) and for missing numbers (XOR indices with values).</p>
<p><b>Two</b> unique values? XOR all to get <code>a ^ b</code>; any 1-bit in it is a place where a and b differ. Split the numbers by that bit and XOR each group.</p>
<p><b>Three</b> copies of every value except one? Count each bit position modulo 3 (or use the compact <code>ones</code>/<code>twos</code> masks).</p>
""", practice=[136, 389, 260, 137])


LESSON("Core", "Counting and comparing bits", """
<ul>
<li><b>Hamming distance</b> between x and y = number of 1s in <code>x ^ y</code> (the differing positions).</li>
<li><b>Counting bits for 0..n</b>: <code>ans[i] = ans[i &gt;&gt; 1] + (i &amp; 1)</code> — i has i's bits shifted plus its last bit.</li>
<li><b>Bit flips to convert</b> start → goal = popcount(start ^ goal).</li>
<li><b>Minimum flips for a | b = c</b>: handle each bit position as a small case analysis.</li>
</ul>
<p>Python helpers: <code>bin(x).count("1")</code>, or <code>x.bit_count()</code> in Python 3.10+. In interviews, also show the <code>n &amp; (n − 1)</code> loop.</p>
""", practice=[461, 2220, 1318, 338])


LESSON("Advanced", "Negative numbers and arithmetic with bits", """
<h4>Two's complement</h4>
<p>Fixed-width integers store −x as <code>~x + 1</code> (flip all bits, add one). In 8 bits, −5 is <code>11111011</code>. The top bit acts as the sign.</p>
<p>Python integers have no fixed width — conceptually a negative has infinitely many leading 1s. For "32-bit" problems, keep values inside a mask <code>0xFFFFFFFF</code> and convert back at the end: <code>x if x &lt; 2**31 else x - 2**32</code>.</p>
<h4>Adding without +</h4>
<p><code>a ^ b</code> adds without carrying; <code>(a &amp; b) &lt;&lt; 1</code> is the carry. Repeat until there is no carry.</p>
<h4>Dividing without /</h4>
<p>Subtract the biggest <code>divisor &lt;&lt; k</code> that fits, add <code>1 &lt;&lt; k</code> to the quotient, repeat — O(log² n) instead of O(quotient).</p>
<h4>Reversing bits</h4>
<p>Swap halves with masks: 16-bit halves, then bytes, then nibbles, pairs and single bits — 5 steps for 32 bits.</p>
""", practice=[371, 29, 190])


@LD
def twos_complement_lesson():
    x, W = 5, 8
    T(f"{x} in {W} bits", BITS(str(x), x, W))
    flipped = ~x & 0xFF
    T("Flip every bit (~x)", BITS("~5 (8 bits)", flipped, W))
    neg = (flipped + 1) & 0xFF
    T("Add 1 → this bit pattern means −5", BITS("−5 (8 bits)", neg, W, ok=[7]))
    back = neg - 256 if neg >= 128 else neg
    T(f"Read back as signed: top bit set, so {neg} − 256 = {back}", V(unsigned=neg, signed=back))
    return back


LESSON("Advanced", "Per-bit thinking, prefix XOR and subsets", """
<h4>Count each bit separately</h4>
<p>For "sum over all pairs" questions, bits don't affect each other. Total Hamming distance: if k numbers have bit b set, that bit differs in <code>k × (n − k)</code> pairs. Sum over the 32 bits → O(32n) instead of O(n²).</p>
<h4>Prefix XOR</h4>
<p>Like prefix sums: <code>pre[i]</code> = XOR of the first i values, and <code>xor(l..r) = pre[r + 1] ^ pre[l]</code> because the shared part cancels. A range XOR is 0 exactly when two prefixes are equal.</p>
<h4>Masks as subsets</h4>
<p>An n-bit mask picks a subset of n items: bit i set = item i included. <code>for mask in range(1 &lt;&lt; n)</code> visits all 2ⁿ subsets — the basis of bitmask DP.</p>
<h4>Common prefix</h4>
<p>AND of a whole range keeps only the common binary prefix of its ends. Gray code <code>i ^ (i &gt;&gt; 1)</code> changes one bit per step.</p>
""", practice=[477, 1863, 1310, 1442, 201, 89])
