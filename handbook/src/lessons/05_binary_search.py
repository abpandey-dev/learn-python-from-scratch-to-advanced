from lib import *

LESSON("Basics", "The guessing game", """
<p>"I'm thinking of a number from 1 to 100." If you guess 1, 2, 3, … it can take 100 guesses. If you always guess the <b>middle</b> and I say "higher" or "lower", every guess throws away half of what's left:</p>
<div class="pic">100 → 50 → 25 → 13 → 7 → 4 → 2 → 1      at most 7 guesses</div>
<p>That's <b>binary search</b>. The number of steps is how many times you can halve n: <b>log₂ n</b>.</p>
<table><tr><th>n</th><td>1,000</td><td>1,000,000</td><td>1,000,000,000</td></tr><tr><th>steps</th><td>10</td><td>20</td><td>30</td></tr></table>
<p>The only requirement: when you look at the middle, you must be able to say <b>which half can't contain the answer</b>. Sorted order gives you that.</p>
""")


@LD
def guessing_lesson():
    secret = 37
    lo, hi, guesses = 1, 100, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        guesses += 1
        if mid == secret:
            T(f"Guess #{guesses}: {mid} — correct!", V(lo=lo, hi=hi, guess=mid, answer="correct"))
            return guesses
        T(f"Guess #{guesses}: {mid} is too {'low' if mid < secret else 'high'} → keep {'the upper' if mid < secret else 'the lower'} half", V(lo=lo, hi=hi, guess=mid, remaining=(hi - mid) if mid < secret else (mid - lo)))
        if mid < secret:
            lo = mid + 1
        else:
            hi = mid - 1


LESSON("Core", "Two templates: exact match and first-true", """
<h4>1. Exact match (closed range)</h4>
<pre><code class="py">lo, hi = 0, len(a) - 1
while lo &lt;= hi:
    mid = (lo + hi) // 2
    if a[mid] == target: return mid
    if a[mid] &lt; target: lo = mid + 1
    else:                hi = mid - 1
return -1</code></pre>
<h4>2. First index where a condition is true (half-open)</h4>
<p>Think of the array as answers to a yes/no question that look like <code>F F F T T T</code>. Find the first T.</p>
<pre><code class="py">lo, hi = 0, len(a)          # answer is somewhere in [lo, hi]
while lo &lt; hi:
    mid = (lo + hi) // 2
    if ok(mid): hi = mid    # mid could be the answer
    else:       lo = mid + 1
return lo</code></pre>
<p>With <code>ok(i) = a[i] &gt;= x</code> this is <b>lower bound</b> (first position ≥ x, Python's <code>bisect_left</code>). With <code>a[i] &gt; x</code> it's <b>upper bound</b> (<code>bisect_right</code>). First and last position of x = these two.</p>
<div class="tip">Template 2 is the one to master. Almost every binary search problem can be phrased as "find the first true".</div>
""", practice=[704, 35, 34, 1539])


@LD
def bounds_lesson():
    a, x = [1, 3, 3, 3, 5, 8], 3
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        T(f"Lower bound: is a[{mid}] = {a[mid]} ≥ {x}? {a[mid] >= x}", A("a", a, hl=range(lo, hi), lo=lo, mid=mid, hi=hi), A("a[i] ≥ 3 ?", ["T" if v >= x else "F" for v in a]))
        if a[mid] >= x:
            hi = mid
        else:
            lo = mid + 1
    T(f"First index with a[i] ≥ {x} is {lo}", A("a", a, ok=[lo]), A("a[i] ≥ 3 ?", ["T" if v >= x else "F" for v in a], ok=[lo]))
    return lo


LESSON("Core", "Arrays that are only partly sorted", """
<p>Binary search doesn't need a fully sorted array — it needs a way to discard half.</p>
<ul>
<li><b>Rotated sorted array</b> (<code>[4,5,6,7,0,1,2]</code>): at any mid, at least one half is properly sorted. Check whether the target lies inside that sorted half's range; if yes go there, else go to the other half.</li>
<li><b>Minimum of a rotated array</b>: compare <code>a[mid]</code> with <code>a[hi]</code>. Bigger → the drop is to the right.</li>
<li><b>Peak element</b>: if <code>a[mid] &lt; a[mid + 1]</code> you're walking uphill, so a peak exists to the right.</li>
<li><b>Duplicates</b> can hide which half is sorted; when <code>a[lo] == a[mid] == a[hi]</code>, shrink both ends by one (worst case becomes O(n)).</li>
</ul>
""", practice=[33, 153, 162, 81, 540])


LESSON("Advanced", "Binary search on the answer", """
<p>The most powerful use of binary search isn't on an array at all — it's on the <b>answer</b>.</p>
<p>Example: "What's the slowest eating speed that finishes all bananas in h hours?" Speeds 1, 2, 3, … give answers that look like <code>no no no yes yes yes</code> — once a speed works, every faster speed works too. That's a monotonic yes/no question, so binary search the speed.</p>
<ol>
<li>Find the smallest and largest possible answer (<code>lo</code>, <code>hi</code>).</li>
<li>Write <code>feasible(x)</code> — usually a simple greedy O(n) check.</li>
<li>Binary search for the first feasible x (or last, for "maximise").</li>
</ol>
<p>Total cost: O(n · log(range)). Signals: "minimise the maximum", "maximise the minimum", "smallest capacity / speed / days such that…".</p>
""", practice=[875, 1011, 410, 1482, 1283, 1552])


@LD
def answer_space_lesson():
    piles, h = [3, 6, 7, 11], 8
    hours = lambda k: sum((p + k - 1) // k for p in piles)
    table = [hours(k) <= h for k in range(1, max(piles) + 1)]
    lo, hi = 1, max(piles)
    while lo < hi:
        k = (lo + hi) // 2
        T(f"Speed {k}: needs {hours(k)} h → {'fits' if hours(k) <= h else 'too slow'}", A("speed 1..11 fits in 8 h?", ["T" if x else "F" for x in table], hl=range(lo - 1, hi), ok=[k - 1] if hours(k) <= h else [], bad=[] if hours(k) <= h else [k - 1]), V(lo=lo, hi=hi, k=k))
        if hours(k) <= h:
            hi = k
        else:
            lo = k + 1
    T(f"Slowest speed that fits: {lo}", A("speed 1..11 fits in 8 h?", ["T" if x else "F" for x in table], ok=[lo - 1]))
    return lo


LESSON("Advanced", "Tricky cases", """
<ul>
<li><b>Infinite loops</b>: if you ever write <code>lo = mid</code>, round the middle up: <code>mid = (lo + hi + 1) // 2</code>. Otherwise with <code>hi = lo + 1</code> you stay stuck.</li>
<li><b>Overflow</b>: in Java/C++ write <code>lo + (hi − lo) / 2</code>. Python ints don't overflow, but say it in interviews.</li>
<li><b>2-D matrix</b>: if rows continue each other, treat it as one sorted list (<code>k → (k // n, k % n)</code>). If only rows and columns are sorted, start at the top-right corner and step left or down — O(m + n).</li>
<li><b>Two sorted arrays (median)</b>: binary search the <i>cut</i> in the smaller array so that the left parts together hold half the elements and everything on the left ≤ everything on the right.</li>
<li><b>Square roots and real numbers</b>: search the value range; for decimals, loop a fixed number of times instead of <code>lo &lt; hi</code>.</li>
</ul>
""", practice=[69, 74, 240, 4, 658])
