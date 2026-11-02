from lib import *

TOPIC(
    id="bits", title="Bit Manipulation", glyph="0101",
    blurb="Work on the binary digits directly: XOR cancelling, n & (n − 1), masks and per-bit counting.",
    demo_title="The core moves on two numbers: AND, OR, XOR, shifts and n & (n − 1)",
    theory="""
<h3>What it is</h3>
<p>Every integer is stored in binary. Bit manipulation answers questions by looking at, or changing, individual bits in O(1) — no loops over values, no extra memory. Bit 0 is the rightmost (worth 1), bit i is worth 2<sup>i</sup>.</p>
<h3>Operators</h3>
<table>
<tr><th>Operator</th><th>Meaning</th><th>Example (6 = 110, 3 = 011)</th></tr>
<tr><td><code>a &amp; b</code></td><td>1 where both are 1</td><td><code>110 &amp; 011 = 010</code> (2)</td></tr>
<tr><td><code>a | b</code></td><td>1 where either is 1</td><td><code>110 | 011 = 111</code> (7)</td></tr>
<tr><td><code>a ^ b</code></td><td>1 where they differ</td><td><code>110 ^ 011 = 101</code> (5)</td></tr>
<tr><td><code>~a</code></td><td>flip every bit (= −a − 1 in Python)</td><td><code>~6 = −7</code></td></tr>
<tr><td><code>a &lt;&lt; k</code>, <code>a &gt;&gt; k</code></td><td>multiply / floor-divide by 2<sup>k</sup></td><td><code>6 &lt;&lt; 1 = 12</code>, <code>6 &gt;&gt; 1 = 3</code></td></tr>
</table>
<h3>Tricks you'll use constantly</h3>
<table>
<tr><th>Expression</th><th>Does</th></tr>
<tr><td><code>(n &gt;&gt; i) &amp; 1</code></td><td>read bit i</td></tr>
<tr><td><code>n | (1 &lt;&lt; i)</code> / <code>n &amp; ~(1 &lt;&lt; i)</code> / <code>n ^ (1 &lt;&lt; i)</code></td><td>set / clear / toggle bit i</td></tr>
<tr><td><code>n &amp; (n − 1)</code></td><td>clear the lowest set bit (0 ⇔ n is a power of two)</td></tr>
<tr><td><code>n &amp; −n</code></td><td>keep only the lowest set bit</td></tr>
<tr><td><code>x ^ x = 0</code>, <code>x ^ 0 = x</code></td><td>pairs cancel out — the "single number" trick</td></tr>
<tr><td><code>for mask in range(1 &lt;&lt; n)</code></td><td>loop over every subset of n items</td></tr>
</table>
<h3>Spot the pattern</h3>
<ul>
<li>"Every element appears twice except one" → XOR everything.</li>
<li>"Count set bits", "power of two" → <code>n &amp; (n − 1)</code>.</li>
<li>"Add / divide without + or /" → XOR is addition without carry, AND shifted left is the carry; division by doubling shifts.</li>
<li>"Sum over all pairs" of something bitwise → count each bit independently (ones × zeros).</li>
<li>Subarray XOR → prefix XOR: <code>xor(i..j) = pre[j + 1] ^ pre[i]</code>.</li>
</ul>
<h3>Python gotchas</h3>
<ul>
<li>Python ints have no fixed width, so negatives have infinitely many leading 1s. For 32-bit problems mask with <code>&amp; 0xFFFFFFFF</code> and convert back: <code>x if x &lt; 2**31 else x − 2**32</code>.</li>
<li><code>bin(n).count("1")</code> and <code>n.bit_count()</code> exist, but interviewers usually want you to show the loop.</li>
<li>Operator precedence: <code>a &amp; b == c</code> means <code>a &amp; (b == c)</code> — use brackets.</li>
</ul>
""")


@D
def bits_demo():
    a, b = 6, 3
    T("Two numbers in binary", BITS("a", a, 4), BITS("b", b, 4))
    T("a & b keeps bits set in both", BITS("a", a, 4), BITS("b", b, 4), BITS("a & b", a & b, 4, ok=[1]))
    T("a | b keeps bits set in either", BITS("a", a, 4), BITS("b", b, 4), BITS("a | b", a | b, 4, ok=[0, 1, 2]))
    T("a ^ b keeps bits that differ", BITS("a", a, 4), BITS("b", b, 4), BITS("a ^ b", a ^ b, 4, ok=[0, 2]))
    T("a << 1 doubles, a >> 1 halves", BITS("a", a, 4), BITS("a << 1", a << 1, 4), BITS("a >> 1", a >> 1, 4))
    n = 12
    T("n & (n − 1) clears the lowest set bit", BITS("n", n, 4, hl=[2]), BITS("n − 1", n - 1, 4), BITS("n & (n − 1)", n & (n - 1), 4, ok=[3]))
    return a ^ b


# 1 ---------------------------------------------------------------
Q(136, "Single Number", "Easy", "XOR cancels pairs",
  "Every element appears twice except one. Find it in O(n) time and O(1) space.",
  [(([2, 2, 1],), 1), (([4, 1, 2, 1, 2],), 4), (([1],), 1)],
  ("Count occurrences in a dict and return the value seen once.", "O(n)", "O(n)"),
  ("XOR all numbers: x ^ x = 0 and 0 ^ y = y, and order doesn't matter, so every pair cancels and only the single number is left.", "O(n)", "O(1)"))


@B
def single_number(nums):
    count = {}
    for x in nums:
        count[x] = count.get(x, 0) + 1
    return next(x for x, c in count.items() if c == 1)


@O
def single_number(nums):
    acc = 0
    for i, x in enumerate(nums):
        acc ^= x
        T(f"acc ^= {x} → {acc}", A("nums", nums, hl=[i], i=i), BITS("x", x, 4), BITS("acc", acc, 4), at="prev")
    return acc


# 2 ---------------------------------------------------------------
Q(137, "Single Number II", "Medium", "Count bits mod 3 (ones / twos)",
  "Every element appears three times except one, which appears once. Find it in O(1) extra space.",
  [(([2, 2, 3, 2],), 3), (([0, 1, 0, 1, 0, 1, 99],), 99), (([-2, -2, 1, -2],), 1), (([-4, -4, -4, -7],), -7)],
  ("Count occurrences in a dict.", "O(n)", "O(n)"),
  ("For each bit, the number of times it is set across all numbers, mod 3, is that bit of the answer. 'ones' and 'twos' track bits seen once or twice (mod 3) for all bit positions at once.", "O(n)", "O(1)"),
  viz=([5, 3, 5, 5],))


@B
def single_number_ii(nums):
    count = {}
    for x in nums:
        count[x] = count.get(x, 0) + 1
    return next(x for x, c in count.items() if c == 1)


@O
def single_number_ii(nums):
    ones = twos = 0
    for i, x in enumerate(nums):
        ones = (ones ^ x) & ~twos
        twos = (twos ^ x) & ~ones
        T(f"After {x}: bits seen once (mod 3) in ones, twice in twos", A("nums", nums, hl=[i], i=i), BITS("x", x, 4), BITS("ones", ones, 4), BITS("twos", twos, 4), at="prev")
    return ones


# 3 ---------------------------------------------------------------
Q(260, "Single Number III", "Medium", "XOR, then split by a differing bit",
  "Exactly two elements appear once; all others appear twice. Return the two, in any order.",
  [(([1, 2, 1, 3, 2, 5],), [3, 5]), (([-1, 0],), [-1, 0]), (([0, 1],), [1, 0])],
  ("Count occurrences in a dict.", "O(n)", "O(n)"),
  ("XOR everything to get a ^ b. Any set bit of it (take the lowest, d = x &amp; −x) is where a and b differ. XOR the numbers with that bit set and those without separately — each group holds one answer.", "O(n)", "O(1)"),
  norm=sorted)


@B
def single_number_iii(nums):
    count = {}
    for x in nums:
        count[x] = count.get(x, 0) + 1
    return [x for x, c in count.items() if c == 1]


@O
def single_number_iii(nums):
    both = 0
    for x in nums:
        both ^= x
    low = both & -both
    a = b = 0
    for x in nums:
        if x & low:
            a ^= x
        else:
            b ^= x
    T(f"a ^ b = {both}; split on bit value {low}", BITS("a ^ b", both, 4, ok=[low.bit_length() - 1]), A("group with the bit", [x for x in nums if x & low]), A("group without", [x for x in nums if not x & low]), V(a=a, b=b), at="prev")
    return [a, b]


# 4 ---------------------------------------------------------------
Q(191, "Number of 1 Bits", "Easy", "n & (n − 1)",
  "Return the number of set bits in the binary form of a positive integer.",
  [((11,), 3), ((128,), 1), ((2147483645,), 30)],
  ("Check all 32 bit positions one by one.", "O(32)", "O(1)"),
  ("n &amp; (n − 1) removes the lowest set bit, so loop until n is 0 — only as many steps as there are 1s.", "O(set bits)", "O(1)"),
  viz=(44,))


@B
def hamming_weight(n):
    return sum((n >> i) & 1 for i in range(32))


@O
def hamming_weight(n):
    count = 0
    while n:
        T(f"n = {n}: clear its lowest set bit", BITS("n", n, 8, hl=[(n & -n).bit_length() - 1]), V(count=count))
        n &= n - 1
        count += 1
    return count


# 5 ---------------------------------------------------------------
Q(338, "Counting Bits", "Easy", "DP on i >> 1",
  "Return an array where ans[i] is the number of 1 bits in i, for every i from 0 to n.",
  [((2,), [0, 1, 1]), ((5,), [0, 1, 1, 2, 1, 2])],
  ("Count the bits of every i separately.", "O(n log n)", "O(1) extra"),
  ("i has the same bits as i >> 1 plus its last bit: ans[i] = ans[i >> 1] + (i &amp; 1).", "O(n)", "O(1) extra"),
  viz=(8,))


@B
def count_bits(n):
    return [bin(i).count("1") for i in range(n + 1)]


@O
def count_bits(n):
    ans = [0] * (n + 1)
    for i in range(1, n + 1):
        ans[i] = ans[i >> 1] + (i & 1)
        T(f"ans[{i}] = ans[{i >> 1}] + {i & 1} = {ans[i]}", BITS("i", i, 4), A("ans", ans, hl=[i >> 1], ok=[i], i=i), at="prev")
    return ans


# 6 ---------------------------------------------------------------
Q(190, "Reverse Bits", "Easy", "Swap halves with masks",
  "Reverse the bits of a 32-bit unsigned integer.",
  [((43261596,), 964176192), ((4294967293,), 3221225471)],
  ("Read the 32 bits one by one and build the result from the other end.", "O(32)", "O(1)"),
  ("Swap the two 16-bit halves, then the 8-bit halves inside each, then 4, 2 and 1 — five mask-and-shift steps.", "O(log 32) = 5 steps", "O(1)"),
  viz=(0b10110000000000000000000000000001,))


@B
def reverse_bits(n):
    res = 0
    for _ in range(32):
        res = (res << 1) | (n & 1)
        n >>= 1
    return res


@O
def reverse_bits(n):
    n = ((n >> 16) | (n << 16)) & 0xFFFFFFFF
    T("Swap the 16-bit halves", BITS("n", n, 32), at="prev")
    n = ((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8)
    T("Swap bytes inside each half", BITS("n", n, 32), at="prev")
    n = ((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4)
    T("Swap 4-bit groups", BITS("n", n, 32), at="prev")
    n = ((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2)
    T("Swap 2-bit pairs", BITS("n", n, 32), at="prev")
    n = ((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1)
    T("Swap neighbouring bits — fully reversed", BITS("n", n, 32), at="prev")
    return n


# 7 ---------------------------------------------------------------
Q(231, "Power of Two", "Easy", "Exactly one set bit",
  "Return <code>True</code> if n is a power of two.",
  [((1,), True), ((16,), True), ((3,), False), ((0,), False), ((-16,), False)],
  ("Divide by 2 while even; it's a power of two if you reach 1.", "O(log n)", "O(1)"),
  ("A power of two has exactly one set bit, so n &gt; 0 and n &amp; (n − 1) == 0.", "O(1)", "O(1)"),
  viz=(16,))


@B
def is_power_of_two(n):
    if n <= 0:
        return False
    while n % 2 == 0:
        n //= 2
    return n == 1


@O
def is_power_of_two(n):
    T(f"n & (n − 1) = {n & (n - 1) if n > 0 else 'n/a'}", BITS("n", n, 8), BITS("n − 1", n - 1, 8), BITS("n & (n − 1)", n & (n - 1), 8))
    return n > 0 and n & (n - 1) == 0


# 8 ---------------------------------------------------------------
Q(342, "Power of Four", "Easy", "One bit, on an even position",
  "Return <code>True</code> if n is a power of four.",
  [((16,), True), ((5,), False), ((1,), True), ((8,), False)],
  ("Divide by 4 while divisible; check you reach 1.", "O(log n)", "O(1)"),
  ("It must be a power of two, and its single bit must be at an even position: n &amp; 0x55555555 ≠ 0 (mask 0101…0101).", "O(1)", "O(1)"),
  viz=(64,))


@B
def is_power_of_four(n):
    if n <= 0:
        return False
    while n % 4 == 0:
        n //= 4
    return n == 1


@O
def is_power_of_four(n):
    T("One set bit, and it must line up with the 0101… mask", BITS("n", n, 8), BITS("mask 0x55", 0x55, 8, ok=[0, 2, 4, 6]))
    return n > 0 and n & (n - 1) == 0 and n & 0x55555555 != 0


# 9 ---------------------------------------------------------------
Q(371, "Sum of Two Integers", "Medium", "XOR = sum without carry, AND = carry",
  "Return a + b without using + or −.",
  [((1, 2), 3), ((2, 3), 5), ((-2, 3), 1), ((-5, -7), -12)],
  ("Ripple-carry adder: add bit by bit over all 32 positions with a carry bit.", "O(32)", "O(1)"),
  ("a ^ b adds without carrying; (a &amp; b) &lt;&lt; 1 is the carry. Repeat until the carry is 0, masking to 32 bits for Python's unbounded ints.", "O(32) worst, usually fewer", "O(1)"),
  viz=(13, 11))


@B
def get_sum(a, b):
    MASK = 0xFFFFFFFF
    a, b = a & MASK, b & MASK
    res, carry = 0, 0
    for i in range(32):
        x, y = (a >> i) & 1, (b >> i) & 1
        res |= (x ^ y ^ carry) << i
        carry = (x & y) | (carry & (x ^ y))
    return res if res < 2 ** 31 else res - 2 ** 32


@O
def get_sum(a, b):
    MASK = 0xFFFFFFFF
    a, b = a & MASK, b & MASK
    while b:
        a, b = (a ^ b) & MASK, ((a & b) << 1) & MASK
        T("a = sum without carry, b = the carries shifted left", BITS("a", a, 8), BITS("b (carry)", b, 8), at="prev")
    return a if a < 2 ** 31 else a - 2 ** 32


# 10 --------------------------------------------------------------
Q(201, "Bitwise AND of Numbers Range", "Medium", "Common binary prefix",
  "Return the AND of every number from <code>left</code> to <code>right</code> inclusive.",
  [((5, 7), 4), ((0, 0), 0), ((1, 1000), 0), ((26, 30), 24)],
  ("AND all numbers in the range one by one.", "O(right − left)", "O(1)"),
  ("Any bit that changes somewhere in the range becomes 0. The result is the common prefix of left and right: shift both right until they're equal, then shift back.", "O(log right)", "O(1)"),
  viz=(26, 30))


@B
def range_bitwise_and(left, right):
    res = left
    for x in range(left + 1, right + 1):
        res &= x
    return res


@O
def range_bitwise_and(left, right):
    shift = 0
    while left != right:
        T(f"{left} ≠ {right}: drop the last bit of both", BITS("left", left, 5), BITS("right", right, 5), V(shift=shift))
        left >>= 1
        right >>= 1
        shift += 1
    T(f"Common prefix {left}; shift back by {shift}", BITS("prefix", left << shift, 5), V(shift=shift))
    return left << shift


# 11 --------------------------------------------------------------
Q(461, "Hamming Distance", "Easy", "Popcount of XOR",
  "Return the number of bit positions where x and y differ.",
  [((1, 4), 2), ((3, 1), 1)],
  ("Format both as 32-character binary strings and compare characters.", "O(32)", "O(32)"),
  ("x ^ y has a 1 exactly where they differ; count its bits with n &amp; (n − 1).", "O(differing bits)", "O(1)"),
  viz=(9, 14))


@B
def hamming_distance(x, y):
    a, b = format(x, "032b"), format(y, "032b")
    return sum(p != q for p, q in zip(a, b))


@O
def hamming_distance(x, y):
    d, count = x ^ y, 0
    T("x ^ y marks the differing bits", BITS("x", x, 4), BITS("y", y, 4), BITS("x ^ y", d, 4, ok=[i for i in range(4) if d >> i & 1]))
    while d:
        d &= d - 1
        count += 1
    return count


# 12 --------------------------------------------------------------
Q(477, "Total Hamming Distance", "Medium", "Count each bit: ones × zeros",
  "Return the sum of Hamming distances between all pairs of numbers.",
  [(([4, 14, 2],), 6), (([4, 14, 4],), 4)],
  ("Compute the Hamming distance of every pair.", "O(n² · 32)", "O(1)"),
  ("Look at one bit at a time: if k numbers have it set, it contributes k × (n − k) differing pairs.", "O(32 · n)", "O(1)"))


@B
def total_hamming_distance(nums):
    return sum(bin(nums[i] ^ nums[j]).count("1") for i in range(len(nums)) for j in range(i + 1, len(nums)))


@O
def total_hamming_distance(nums):
    n, total = len(nums), 0
    for b in range(32):
        k = sum((x >> b) & 1 for x in nums)
        total += k * (n - k)
        if b < 4:
            T(f"Bit {b}: {k} set × {n - k} unset = {k * (n - k)} pairs", A("bit " + str(b) + " of each", [(x >> b) & 1 for x in nums]), V(total=total), at="prev")
    return total


# 13 --------------------------------------------------------------
Q(1863, "Sum of All Subset XOR Totals", "Easy", "Each bit is in half the subsets",
  "Return the sum of the XOR of every subset of <code>nums</code>.",
  [(([1, 3],), 6), (([5, 1, 6],), 28), (([3, 4, 5, 6, 7, 8],), 480)],
  ("Enumerate all 2ⁿ subsets with a bitmask and XOR each.", "O(n · 2ⁿ)", "O(1)"),
  ("A bit that appears in any number is set in the XOR of exactly half of all subsets. So the answer is (OR of all numbers) × 2ⁿ⁻¹.", "O(n)", "O(1)"))


@B
def subset_xor_sum(nums):
    total = 0
    for mask in range(1 << len(nums)):
        x = 0
        for i, v in enumerate(nums):
            if mask >> i & 1:
                x ^= v
        total += x
    return total


@O
def subset_xor_sum(nums):
    acc = 0
    for x in nums:
        acc |= x
    T(f"OR of all = {acc}; each of its bits is on in half of the 2^{len(nums)} subsets", BITS("OR", acc, 4), V(answer=acc << (len(nums) - 1)))
    return acc << (len(nums) - 1)


# 14 --------------------------------------------------------------
Q(389, "Find the Difference", "Easy", "XOR all characters",
  "<code>t</code> is <code>s</code> shuffled with one extra letter. Return that letter.",
  [(("abcd", "abcde"), "e"), (("", "y"), "y")],
  ("Count letters of both strings and find the one with a higher count in t.", "O(n)", "O(σ)"),
  ("XOR the codes of every character in s and t; matching letters cancel, leaving the extra one.", "O(n)", "O(1)"))


@B
def find_the_difference(s, t):
    from collections import Counter
    return next(iter(Counter(t) - Counter(s)))


@O
def find_the_difference(s, t):
    acc = 0
    for ch in s + t:
        acc ^= ord(ch)
        T(f"XOR in '{ch}'", A("s + t", s + t), V(acc=acc, char=chr(acc) if acc else "-"), at="prev")
    return chr(acc)


# 15 --------------------------------------------------------------
Q(29, "Divide Two Integers", "Medium", "Subtract shifted divisors",
  "Divide without *, / or %, truncating toward zero. Clamp the result to 32-bit signed range.",
  [((10, 3), 3), ((7, -3), -2), ((1, 1), 1), ((-100, 7), -14)],
  ("Subtract the divisor repeatedly and count.", "O(quotient)", "O(1)"),
  ("Subtract the largest divisor × 2ᵏ that still fits (found by shifting left), add 2ᵏ to the quotient, and repeat on the remainder. Handle the sign separately and clamp −2³¹ / −1.", "O(log² n)", "O(1)"),
  viz=(100, 7))


@B
def divide(dividend, divisor):
    neg = (dividend < 0) != (divisor < 0)
    a, b, q = abs(dividend), abs(divisor), 0
    while a >= b:
        a -= b
        q += 1
    q = -q if neg else q
    return max(-2 ** 31, min(2 ** 31 - 1, q))


@O
def divide(dividend, divisor):
    if dividend == -2 ** 31 and divisor == -1:
        return 2 ** 31 - 1
    neg = (dividend < 0) != (divisor < 0)
    a, b, q = abs(dividend), abs(divisor), 0
    while a >= b:
        k = 0
        while a >= b << (k + 1):
            k += 1
        a -= b << k
        q += 1 << k
        T(f"Largest fit: {b} × 2^{k} = {b << k}; remainder {a}", V(remainder=a, quotient=q, chunk=b << k), at="prev")
    return -q if neg else q


# 16 --------------------------------------------------------------
Q(1318, "Minimum Flips to Make a OR b Equal to c", "Medium", "Per-bit cases",
  "Return the fewest single-bit flips in a and b so that a | b == c.",
  [((2, 6, 5), 3), ((4, 2, 7), 1), ((1, 2, 3), 0)],
  ("Compare padded binary strings of a, b and c position by position.", "O(32)", "O(32)"),
  ("If c's bit is 1 and both are 0 → 1 flip. If c's bit is 0 → flip every 1 in a and b. In masks: popcount((a | b) ^ c) + popcount(a &amp; b &amp; ~c).", "O(1) with popcount", "O(1)"))


@B
def min_flips(a, b, c):
    x, y, z = format(a, "032b"), format(b, "032b"), format(c, "032b")
    flips = 0
    for p, q, r in zip(x, y, z):
        if r == "1":
            flips += p == "0" and q == "0"
        else:
            flips += (p == "1") + (q == "1")
    return flips


@O
def min_flips(a, b, c):
    wrong = (a | b) ^ c
    double = a & b & ~c
    T("Bits where a | b disagrees with c, plus bits where both a and b must be cleared", BITS("a", a, 4), BITS("b", b, 4), BITS("c", c, 4), BITS("(a|b) ^ c", wrong, 4), BITS("a & b & ~c", double & 0xF, 4))
    return bin(wrong).count("1") + bin(double).count("1")


# 17 --------------------------------------------------------------
Q(2220, "Minimum Bit Flips to Convert Number", "Easy", "Popcount of XOR",
  "Return the minimum number of bit flips to turn <code>start</code> into <code>goal</code>.",
  [((10, 7), 3), ((3, 4), 3)],
  ("Compare both numbers bit by bit over 32 positions.", "O(32)", "O(1)"),
  ("Bits that differ must be flipped: count the 1s in start ^ goal.", "O(differing bits)", "O(1)"))


@B
def min_bit_flips(start, goal):
    return sum(((start >> i) & 1) != ((goal >> i) & 1) for i in range(32))


@O
def min_bit_flips(start, goal):
    d, count = start ^ goal, 0
    T("start ^ goal marks every bit to flip", BITS("start", start, 4), BITS("goal", goal, 4), BITS("start ^ goal", d, 4, ok=[i for i in range(4) if d >> i & 1]))
    while d:
        d &= d - 1
        count += 1
    return count


# 18 --------------------------------------------------------------
Q(1442, "Count Triplets That Can Form Two Arrays of Equal XOR", "Medium", "Prefix XOR + index sums",
  "Count triplets i &lt; j ≤ k where XOR(arr[i..j−1]) == XOR(arr[j..k]).",
  [(([2, 3, 1, 6, 7],), 4), (([1, 1, 1, 1, 1],), 10)],
  ("Try every (i, j, k) and compute both XORs.", "O(n³)", "O(1)"),
  ("Both halves are equal exactly when XOR(arr[i..k]) = 0, i.e. pre[i] == pre[k + 1]; then every j in (i, k] works, giving k − i triplets. Keep, per prefix value, how many times it appeared and the sum of their indices.", "O(n)", "O(n)"))


@B
def count_triplets(arr):
    n, count = len(arr), 0
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j, n):
                a = b = 0
                for t in range(i, j):
                    a ^= arr[t]
                for t in range(j, k + 1):
                    b ^= arr[t]
                count += a == b
    return count


@O
def count_triplets(arr):
    cnt, idx_sum = {0: 1}, {0: 0}
    pre = ans = 0
    for k, x in enumerate(arr):
        pre ^= x
        ans += cnt.get(pre, 0) * k - idx_sum.get(pre, 0)
        cnt[pre] = cnt.get(pre, 0) + 1
        idx_sum[pre] = idx_sum.get(pre, 0) + k + 1
        T(f"prefix XOR through index {k} = {pre}; earlier equal prefixes add their k − i", A("arr", arr, hl=[k], i=k), M("count of prefix", cnt, hl=pre), V(answer=ans), at="prev")
    return ans


# 19 --------------------------------------------------------------
Q(1310, "XOR Queries of a Subarray", "Medium", "Prefix XOR",
  "For each query [l, r], return arr[l] ^ … ^ arr[r].",
  [(([1, 3, 4, 8], [[0, 1], [1, 2], [0, 3], [3, 3]]), [2, 7, 14, 8]), (([4, 8, 2, 10], [[2, 3], [1, 3], [0, 0], [0, 3]]), [8, 0, 4, 4])],
  ("XOR the range from scratch for each query.", "O(n · q)", "O(1)"),
  ("pre[i] = XOR of the first i elements. Since x ^ x = 0, xor(l..r) = pre[r + 1] ^ pre[l].", "O(n + q)", "O(n)"))


@B
def xor_queries(arr, queries):
    res = []
    for l, r in queries:
        x = 0
        for i in range(l, r + 1):
            x ^= arr[i]
        res.append(x)
    return res


@O
def xor_queries(arr, queries):
    pre = [0]
    for x in arr:
        pre.append(pre[-1] ^ x)
    T("Prefix XOR: pre[i] = arr[0] ^ … ^ arr[i − 1]", A("arr", arr), A("pre", pre))
    res = []
    for l, r in queries:
        res.append(pre[r + 1] ^ pre[l])
        T(f"[{l}, {r}] → pre[{r + 1}] ^ pre[{l}] = {pre[r + 1]} ^ {pre[l]} = {res[-1]}", A("arr", arr, hl=range(l, r + 1)), A("pre", pre, ok=[l, r + 1]), A("answers", res), at="prev")
    return res


# 20 --------------------------------------------------------------
Q(89, "Gray Code", "Medium", "i ^ (i >> 1)",
  "Return any sequence of all 2ⁿ n-bit numbers starting at 0 where consecutive numbers (including last → first) differ by exactly one bit.",
  [((2,), [0, 1, 3, 2]), ((1,), [0, 1]), ((3,), [0, 1, 3, 2, 6, 7, 5, 4])],
  ("Backtracking: from the current number try flipping each bit to an unused number until all 2ⁿ are used.", "O(n · 2ⁿ) with backtracking, can be worse", "O(2ⁿ)"),
  ("The i-th Gray code is i ^ (i &gt;&gt; 1): moving from i to i + 1 changes this value in exactly one bit.", "O(2ⁿ)", "O(1) extra"),
  check=lambda a, out: len(out) == 1 << a[0] and out[0] == 0 and len(set(out)) == len(out) and all(bin(out[i] ^ out[(i + 1) % len(out)]).count("1") == 1 for i in range(len(out))))


@B
def gray_code(n):
    seq, used = [0], {0}

    def go():
        if len(seq) == 1 << n:
            return True
        for b in range(n):
            nxt = seq[-1] ^ (1 << b)
            if nxt not in used:
                used.add(nxt)
                seq.append(nxt)
                if go():
                    return True
                seq.pop()
                used.remove(nxt)
        return False
    go()
    return seq


@O
def gray_code(n):
    res = []
    for i in range(1 << n):
        res.append(i ^ (i >> 1))
        T(f"i = {i} → {i} ^ {i >> 1} = {res[-1]}", BITS("gray", res[-1], n, hl=[((res[-1] ^ res[-2]).bit_length() - 1)] if i else []), A("sequence", res, ok=[i]), at="prev")
    return res
