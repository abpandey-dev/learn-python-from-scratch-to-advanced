from lib import *

THEORY("Definition", """
<p><b>Binary search</b> is a <b>divide-and-conquer</b> search algorithm that finds a target in a <b>sorted</b> sequence by repeatedly comparing it with the middle element and discarding the half that cannot contain it.</p>
<p>More generally, binary search finds the boundary of any <b>monotonic predicate</b> — a yes/no function over an ordered range whose answers look like <code>F F F … F T T … T</code>.</p>
""")

THEORY("Algorithm (iterative)", """
<ol>
<li>Set <code>low = 0</code>, <code>high = n − 1</code>.</li>
<li>While <code>low ≤ high</code>:
  <ol type="a"><li><code>mid = low + (high − low) // 2</code></li>
  <li>If <code>a[mid] == target</code> → return mid.</li>
  <li>If <code>a[mid] &lt; target</code> → <code>low = mid + 1</code> (search the right half).</li>
  <li>Else → <code>high = mid − 1</code> (search the left half).</li></ol></li>
<li>Return −1 (not found).</li>
</ol>
<p><b>Invariant</b>: if the target exists, it is always within <code>[low, high]</code>. Each iteration shrinks the range while keeping the invariant, so when the range is empty the target doesn't exist.</p>
<p>The <code>low + (high − low) // 2</code> form avoids integer overflow in fixed-width languages (Java, C++); in Python <code>(low + high) // 2</code> is fine.</p>
""")

THEORY("Complexity derivation", """
<p>After k comparisons, the remaining range has about n / 2ᵏ elements. The search stops when that reaches 1:</p>
<div class="pic">n / 2ᵏ = 1   →   2ᵏ = n   →   k = log₂ n</div>
<table>
<tr><th>Case</th><th>Time</th><th>Space</th></tr>
<tr><td>Best (target at the first mid)</td><td>O(1)</td><td rowspan="3">O(1) iterative, O(log n) recursive (call stack)</td></tr>
<tr><td>Average</td><td>O(log n)</td></tr>
<tr><td>Worst</td><td>O(log n)</td></tr>
</table>
<p>Recurrence for the recursive version: <code>T(n) = T(n/2) + O(1)</code>, which solves to O(log n).</p>
""")

THEORY("Variants", """
<table>
<tr><th>Variant</th><th>Finds</th><th>Python</th></tr>
<tr><td>Exact search</td><td>any index of target</td><td>—</td></tr>
<tr><td><b>Lower bound</b></td><td>first index with a[i] ≥ x (insertion point)</td><td><code>bisect.bisect_left(a, x)</code></td></tr>
<tr><td><b>Upper bound</b></td><td>first index with a[i] &gt; x</td><td><code>bisect.bisect_right(a, x)</code></td></tr>
<tr><td>Count of x</td><td>upper − lower</td><td><code>bisect_right − bisect_left</code></td></tr>
<tr><td>Rotated array search</td><td>target in a rotated sorted array</td><td>check which half is sorted</td></tr>
<tr><td>Peak / bitonic</td><td>a local maximum</td><td>follow the rising slope</td></tr>
<tr><td><b>Search on the answer</b></td><td>smallest/largest feasible value</td><td>binary search a value range with a feasibility check</td></tr>
<tr><td>Real-valued (bisection)</td><td>roots, square roots</td><td>fixed number of iterations</td></tr>
</table>
""")

THEORY("Binary search vs linear search", """
<table>
<tr><th></th><th>Linear search</th><th>Binary search</th></tr>
<tr><td>Requirement</td><td>none</td><td>sorted data (or monotonic predicate)</td></tr>
<tr><td>Time</td><td>O(n)</td><td>O(log n)</td></tr>
<tr><td>Data structure</td><td>array or linked list</td><td>random-access structure (array); not a linked list</td></tr>
<tr><td>Best for</td><td>small or unsorted data, single search</td><td>large sorted data, many searches</td></tr>
</table>
<p>If you search only once in unsorted data, sorting first (O(n log n)) costs more than a linear scan. Binary search pays off with repeated queries.</p>
""")

THEORY("Advantages, disadvantages and applications", """
<div class="two">
<div class="pro"><h5>Advantages</h5><ul><li>Extremely fast: 30 steps for a billion elements</li><li>O(1) extra space</li><li>Generalises to any monotonic decision problem</li></ul></div>
<div class="con"><h5>Disadvantages</h5><ul><li>Needs sorted data and random access</li><li>Keeping data sorted under inserts costs O(n) per insert in an array (use a balanced BST instead)</li><li>Off-by-one errors are easy to make</li></ul></div>
</div>
<h4>Applications</h4>
<ul>
<li>Searching in sorted databases and indexes; <code>git bisect</code> to find the commit that introduced a bug.</li>
<li>Dictionary / phone book lookup; autocomplete over a sorted word list.</li>
<li>Numerical methods (bisection method for equation roots).</li>
<li>Capacity planning: minimum servers / bandwidth / speed that meets a deadline.</li>
</ul>
""")

FAQ("Why does binary search need a sorted array?", "<p>Discarding half depends on knowing every element on one side of mid is smaller (or larger) than the target. Without sorted order, comparing with mid gives no information about the rest.</p>")
FAQ("Can binary search be used on a linked list?", "<p>Technically yes, but reaching the middle node takes O(n), so total time is O(n) — no better than linear search. Binary search needs O(1) random access.</p>")
FAQ("What is the time complexity and why?", "<p>O(log n): each comparison halves the remaining range, so after k steps n / 2ᵏ elements remain; k = log₂ n steps reduce it to one.</p>")
FAQ("What is 'binary search on the answer'?", "<p>When the answer lies in a range and feasibility is monotonic (if x works, every larger x works), binary search over candidate answers, checking each with a feasibility function. Cost: O(log(range) × cost of the check).</p>")
FAQ("How do you avoid infinite loops?", "<p>Make sure the range shrinks every iteration. With <code>lo = mid</code> use the upper middle <code>(lo + hi + 1) // 2</code>; with <code>hi = mid</code> use the lower middle. Pick one template (closed or half-open) and stay consistent.</p>")
FAQ("Recursive or iterative binary search?", "<p>Both are O(log n) time. Iterative uses O(1) space; recursive uses O(log n) stack space. Iterative is preferred in practice.</p>")
