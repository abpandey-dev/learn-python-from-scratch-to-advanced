from lib import *

THEORY("Definition", """
<p>The <b>two-pointer technique</b> is an algorithm design method that uses two indices (pointers) moving through a sequence — toward each other, in the same direction, or over two different sequences — to solve a problem in a single pass. It is not a data structure but a <b>traversal strategy</b>.</p>
<p>Its purpose is to reduce problems that naively examine all pairs, O(n²), to O(n) (or O(n log n) including a sort), with O(1) extra space.</p>
""")

THEORY("Types of two-pointer traversal", """
<table>
<tr><th>Type</th><th>Start</th><th>Movement</th><th>Typical use</th></tr>
<tr><td><b>Opposite direction (converging)</b></td><td><code>l = 0</code>, <code>r = n − 1</code></td><td>move inward until they meet</td><td>pair sum in sorted array, palindromes, reversing, container with most water</td></tr>
<tr><td><b>Same direction (fast/slow, read/write)</b></td><td>both at 0</td><td>reader always advances; writer advances on a kept element</td><td>remove duplicates, remove element, partitioning</td></tr>
<tr><td><b>Two sequences</b></td><td>one pointer at the start of each</td><td>advance the pointer at the smaller element</td><td>merging sorted arrays, intersection, subsequence check</td></tr>
<tr><td><b>Fixed loop + inner pair</b></td><td>outer index i, pair l, r after it</td><td>converge for each i</td><td>3Sum, 3Sum closest, 4Sum</td></tr>
</table>
""")

THEORY("Why it is correct: the elimination argument", """
<p>For converging pointers on a sorted array searching for <code>a[l] + a[r] = target</code>:</p>
<ul>
<li>If <code>a[l] + a[r] &lt; target</code>: for every <code>k ≤ r</code>, <code>a[l] + a[k] ≤ a[l] + a[r] &lt; target</code>. So index <code>l</code> cannot be in any valid pair with the remaining elements → <b>safe to discard l</b>.</li>
<li>If the sum is greater, the symmetric argument discards <code>r</code>.</li>
</ul>
<p>Each step permanently removes one index from consideration, so at most n − 1 steps happen. This is called a <b>loop invariant</b>: "if a solution exists, it lies within [l, r]". The invariant holds at the start and after every step, so the algorithm never misses the answer.</p>
<p>For <b>container with most water</b>, the area is limited by the shorter line; moving the taller line inward can only shrink the width while the height stays capped, so the shorter line is discarded.</p>
""")

THEORY("Complexity", """
<table>
<tr><th>Problem</th><th>Brute force</th><th>Two pointers</th><th>Space</th></tr>
<tr><td>Pair with sum (sorted)</td><td>O(n²)</td><td>O(n)</td><td>O(1)</td></tr>
<tr><td>Pair with sum (unsorted)</td><td>O(n²)</td><td>O(n log n) sort + O(n)</td><td>O(1) (or hash map O(n) time)</td></tr>
<tr><td>3Sum</td><td>O(n³)</td><td>O(n²)</td><td>O(1) extra</td></tr>
<tr><td>k-Sum</td><td>O(nᵏ)</td><td>O(nᵏ⁻¹)</td><td>O(k) recursion</td></tr>
<tr><td>Merge two sorted arrays</td><td>O((m+n) log(m+n))</td><td>O(m + n)</td><td>O(1) if merged in place from the back</td></tr>
<tr><td>In-place removal</td><td>O(n) with extra list</td><td>O(n)</td><td>O(1)</td></tr>
</table>
""")

THEORY("Prerequisites, advantages and limitations", """
<div class="two">
<div class="pro"><h5>Advantages</h5><ul><li>Linear time instead of quadratic</li><li>Constant extra space — works in place</li><li>Short, easy-to-verify code</li></ul></div>
<div class="con"><h5>Limitations</h5><ul><li>Converging pointers need <b>sorted</b> data (or a similar monotonic property)</li><li>Sorting loses original indices — use a hash map if indices are required</li><li>Doesn't directly handle "count all pairs" with many duplicates without care</li></ul></div>
</div>
""")

THEORY("Applications", """
<ul>
<li>Merging step of <b>merge sort</b>; merging sorted files or database results.</li>
<li><b>Partitioning</b> in quicksort (Hoare / Lomuto schemes) and the Dutch national flag problem.</li>
<li>Palindrome checking, string reversal, removing characters in place.</li>
<li>Finding pairs/triples with a target sum in sorted data (finance, recommendation matching).</li>
<li>Fast/slow pointers on linked lists (cycle detection, middle element).</li>
</ul>
""")

FAQ("Two pointers or hash map for Two Sum?", "<p>Unsorted input that needs original indices → hash map, O(n) time, O(n) space. Sorted input (or indices not needed) → two pointers, O(n) time after sorting, O(1) space. Mention the trade-off.</p>")
FAQ("Why must the array be sorted for converging pointers?", "<p>The decision to discard l or r depends on knowing every element between them is between a[l] and a[r]. Without sorted order, a too-small sum doesn't prove a[l] is useless.</p>")
FAQ("How are duplicate triplets avoided in 3Sum?", "<p>Sort first. Skip the outer index when <code>nums[i] == nums[i−1]</code>, and after recording a triplet move <code>l</code> past all equal values (and r past equal values). Equal values at the same position would produce the same triplet.</p>")
FAQ("What is the difference between two pointers and sliding window?", "<p>Sliding window is a special case of same-direction two pointers where the elements <b>between</b> the pointers form a contiguous window whose state (sum, counts) you maintain. Generic two pointers usually only care about the two pointed elements.</p>")
FAQ("What does 'in place' mean?", "<p>The algorithm modifies the input structure itself and uses only O(1) extra memory (a few variables), rather than building a new array.</p>")
