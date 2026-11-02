from lib import *

THEORY("Definition", """
<p>The <b>sliding window technique</b> processes a contiguous range <code>[l, r]</code> of an array or string — the <b>window</b> — and moves it across the input, updating a summary of the window (sum, counts, max) <b>incrementally</b> instead of recomputing it from scratch.</p>
<p>Each element enters the window once (when <code>r</code> passes it) and leaves once (when <code>l</code> passes it), giving O(n) total time for problems that naively take O(n²) or O(n · k).</p>
""")

THEORY("Types of windows", """
<table>
<tr><th>Type</th><th>Size</th><th>Movement rule</th><th>Examples</th></tr>
<tr><td><b>Fixed-size</b></td><td>always k</td><td>add a[r], remove a[r − k]</td><td>max sum / average of size k, anagram search, vowels in substring</td></tr>
<tr><td><b>Variable-size (longest)</b></td><td>changes</td><td>expand r; shrink l while invalid; record after shrinking</td><td>longest substring without repeats, max consecutive ones with k flips</td></tr>
<tr><td><b>Variable-size (shortest)</b></td><td>changes</td><td>expand r; while valid, record then shrink</td><td>minimum size subarray sum, minimum window substring</td></tr>
<tr><td><b>Counting</b></td><td>changes</td><td>after shrinking, add r − l + 1</td><td>subarrays with at most / exactly K …</td></tr>
</table>
""")

THEORY("When the technique applies: monotonicity", """
<p>Shrinking from the left is only correct if the window's validity is <b>monotonic</b>:</p>
<ul>
<li>If window [l, r] is <b>invalid</b> because it is "too much", then every larger window [l', r] with l' &lt; l is also invalid. So once we move l forward we never need to move it back.</li>
<li>Example: with <b>non-negative</b> numbers, "sum ≤ k" is monotonic — removing elements can only reduce the sum.</li>
<li>Counter-example: with <b>negative</b> numbers, removing an element can <i>increase</i> the sum, so the window cannot decide when to shrink. Use <b>prefix sums + hash map</b> instead (Subarray Sum Equals K).</li>
</ul>
""")

THEORY("Complexity analysis", """
<p>A variable window has a <code>while</code> loop inside a <code>for</code> loop, which looks like O(n²). It is O(n) because <code>l</code> only increases and never exceeds n, so the inner loop runs at most n times <b>in total</b> across the whole algorithm (aggregate / amortised analysis).</p>
<table>
<tr><th>Window state</th><th>Update per step</th><th>Space</th></tr>
<tr><td>sum / count of a condition</td><td>O(1)</td><td>O(1)</td></tr>
<tr><td>character counts</td><td>O(1)</td><td>O(σ), σ = alphabet size</td></tr>
<tr><td>max / min</td><td>O(1) amortised with a monotonic deque</td><td>O(k)</td></tr>
<tr><td>median</td><td>O(log k) with two heaps</td><td>O(k)</td></tr>
</table>
""")

THEORY("Advantages and limitations", """
<div class="two">
<div class="pro"><h5>Advantages</h5><ul><li>Turns O(n²) / O(nk) into O(n)</li><li>Single pass; works on streams</li><li>Small memory: only the window's summary</li></ul></div>
<div class="con"><h5>Limitations</h5><ul><li>Only for <b>contiguous</b> ranges (not subsequences)</li><li>Needs a monotonic validity condition</li><li>"Exactly K" needs the atMost(K) − atMost(K−1) trick</li></ul></div>
</div>
""")

THEORY("Applications", """
<ul>
<li><b>Networking</b>: TCP's sliding window controls how many packets are in flight.</li>
<li><b>Rate limiting</b>: count requests in the last 60 seconds.</li>
<li><b>Signal processing / finance</b>: moving averages, rolling max/min of prices.</li>
<li><b>Text processing</b>: finding the shortest snippet containing all search keywords.</li>
<li><b>Monitoring</b>: alerts when the error count in the last N events crosses a threshold.</li>
</ul>
""")

FAQ("How is a sliding window O(n) when it has a nested loop?", "<p>Each pointer moves only forward and at most n steps. The inner <code>while</code> loop's total iterations across the entire run are bounded by n, so the total work is O(2n) = O(n).</p>")
FAQ("Why doesn't sliding window work with negative numbers for 'sum = k'?", "<p>With negatives, shrinking the window doesn't reliably decrease the sum and expanding doesn't reliably increase it, so there's no correct rule for when to move l. Prefix sums with a hash map of counts solve it in O(n).</p>")
FAQ("When do you update the answer — before or after shrinking?", "<p>For the <b>longest</b> valid window, shrink until valid, then update. For the <b>shortest</b> valid window, update while it is still valid, then shrink.</p>")
FAQ("How do you count subarrays with exactly K distinct elements?", "<p>Counting with 'at most K' is easy: after shrinking, every start between l and r is valid, adding r − l + 1. Then exactly(K) = atMost(K) − atMost(K − 1).</p>")
FAQ("How do you keep the maximum of a sliding window in O(1)?", "<p>A monotonic deque of indices with decreasing values: pop smaller values from the back before pushing, pop the front when it leaves the window. The front is the max. Each index is pushed and popped once.</p>")
