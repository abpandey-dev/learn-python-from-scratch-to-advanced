from lib import *

LESSON("Basics", "Subarrays, and why brute force wastes work", """
<p>A <b>subarray</b> (or substring) is a <i>contiguous</i> piece: <code>[3, 1, 4]</code> inside <code>[2, 3, 1, 4, 5]</code>. An array of n elements has about n²/2 subarrays.</p>
<p>Brute force recomputes each one from scratch. But neighbouring windows overlap almost completely:</p>
<div class="pic">[2, 3, 1, 4, 5]
 └──┬──┘           window 0..2  sum = 6
    └──┬──┘        window 1..3  sum = 6 − 2 + 4 = 8</div>
<p>A <b>sliding window</b> reuses the overlap: when the window moves one step, <b>add</b> the element that enters and <b>remove</b> the one that leaves. Each step is O(1), so the whole scan is O(n).</p>
""", practice=[643, 1456])


@LD
def fixed_window_lesson():
    nums, k = [2, 3, 1, 4, 5, 1], 3
    total = sum(nums[:k])
    best = total
    T(f"First window sum = {total}", A("nums", nums, hl=range(k)), V(sum=total, best=best))
    for r in range(k, len(nums)):
        total += nums[r] - nums[r - k]
        best = max(best, total)
        T(f"Slide: +{nums[r]} enters, −{nums[r - k]} leaves → {total}", A("nums", nums, hl=range(r - k + 1, r + 1), bad=[r - k], r=r), V(sum=total, best=best), at="prev")
    return best


LESSON("Core", "Variable-size window: expand, then shrink", """
<p>When the window size isn't fixed, use two pointers <code>l</code> and <code>r</code>:</p>
<ol>
<li>Move <code>r</code> forward one step and add <code>a[r]</code> to the window.</li>
<li><b>While</b> the window breaks the rule, remove <code>a[l]</code> and move <code>l</code> forward.</li>
<li>Now the window is valid — update the answer.</li>
</ol>
<pre><code class="py">l = 0
for r in range(len(a)):
    add(a[r])
    while invalid():
        remove(a[l]); l += 1
    best = max(best, r - l + 1)</code></pre>
<p>It's still O(n): <code>l</code> and <code>r</code> each move forward at most n times in total, even though there's a loop inside a loop.</p>
<div class="tip">It only works when the rule is <b>monotonic</b>: shrinking a bad window can make it good, and growing a good window can only make it worse (or vice versa). Positive numbers with "sum ≥ target" qualify; negative numbers don't.</div>
""", practice=[209, 3, 1004, 904, 1493, 1838])


@LD
def variable_window_lesson():
    nums, target = [2, 3, 1, 2, 4, 3], 7
    l = total = 0
    best = float("inf")
    for r, x in enumerate(nums):
        total += x
        T(f"Expand: add {x} → sum {total}", A("nums", nums, hl=range(l, r + 1), l=l, r=r), V(sum=total, best=best))
        while total >= target:
            best = min(best, r - l + 1)
            T(f"Sum {total} ≥ {target}: record length {r - l + 1}, then shrink", A("nums", nums, ok=range(l, r + 1), l=l, r=r), V(sum=total, best=best))
            total -= nums[l]
            l += 1
    return best


LESSON("Core", "Windows that count characters", """
<p>Many string problems ask about the <i>letters</i> inside a window. Keep a count dict for the window and update it as letters enter and leave.</p>
<ul>
<li><b>Permutation / anagram in a string</b>: fixed window of length |p|; compare its counts with p's counts.</li>
<li><b>Minimum window substring</b>: expand until every needed letter is covered, then shrink while still covered. Track <code>have</code> (letters whose count is satisfied) vs <code>need</code> so the check is O(1), not a full dict comparison.</li>
<li><b>Longest repeating replacement</b>: window is valid if <code>length − (count of its most common letter) ≤ k</code>.</li>
</ul>
<div class="warn">When a count drops to 0, delete the key (<code>del count[c]</code>) if you use <code>len(count)</code> as "number of distinct letters".</div>
""", practice=[567, 438, 76, 424, 1358])


LESSON("Advanced", "Counting subarrays: the atMost trick", """
<p>"How many subarrays have <b>exactly</b> K distinct values / K odd numbers / sum K?" is hard to do with one window, because a valid window can become invalid and valid again.</p>
<p>"<b>At most</b> K" is easy: for each <code>r</code>, after shrinking, every start from <code>l</code> to <code>r</code> gives a valid subarray ending at <code>r</code> — that's <code>r − l + 1</code> new subarrays.</p>
<pre><code class="py">exactly(K) = atMost(K) − atMost(K − 1)</code></pre>
<p>This one identity solves a whole family of problems in O(n).</p>
""", practice=[992, 930, 1248])


@LD
def at_most_lesson():
    nums, k = [1, 2, 1, 3], 2

    def at_most(k):
        count, l, total = {}, 0, 0
        for r, x in enumerate(nums):
            count[x] = count.get(x, 0) + 1
            while len(count) > k:
                count[nums[l]] -= 1
                if count[nums[l]] == 0:
                    del count[nums[l]]
                l += 1
            total += r - l + 1
            T(f"atMost({k}): subarrays ending at {r} are those starting at {l}..{r} → +{r - l + 1}", A("nums", nums, hl=range(l, r + 1), l=l, r=r), V(total=total), at="prev")
        return total

    return at_most(k) - at_most(k - 1)


LESSON("Advanced", "Window maximum with a monotonic deque", """
<p>Keeping the <b>max</b> of a sliding window is harder than keeping a sum — when the max leaves, what's the next max? Recomputing is O(k) per step.</p>
<p>Keep a <code>deque</code> of indices whose values are <b>decreasing</b> from front to back:</p>
<ul>
<li>Before adding <code>i</code>, pop from the back every index whose value ≤ <code>a[i]</code>. They can never be a max again — <code>a[i]</code> is newer and at least as big.</li>
<li>Pop the front if it has left the window.</li>
<li>The front is always the window max.</li>
</ul>
<p>Each index enters and leaves the deque once → O(n) total. The same idea (a monotonic structure) returns in the Stack topic.</p>
""", practice=[239, 219])
