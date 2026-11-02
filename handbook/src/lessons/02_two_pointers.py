from lib import *

LESSON("Basics", "Why two pointers beat two loops", """
<p>The obvious way to look at pairs is two nested loops: for every <code>i</code>, try every <code>j</code>. With n = 10,000 that's 50 million pairs — <b>O(n²)</b>.</p>
<p>Two pointers keep two indices and move <b>one</b> of them each step, based on what they see. Each move throws away many pairs at once, so the total work is about n steps — <b>O(n)</b>.</p>
<div class="pic">brute force : (0,1) (0,2) (0,3) … (1,2) (1,3) …   ~ n²/2 checks
two pointers: l →            ← r                   ~ n checks</div>
<p>The simplest example is checking a palindrome: compare the first and last character, then move both inward.</p>
<pre><code class="py">l, r = 0, len(s) - 1
while l &lt; r:
    if s[l] != s[r]:
        return False
    l, r = l + 1, r - 1
return True</code></pre>
""", practice=[125, 344, 345])


@LD
def palindrome_lesson():
    s = "racecar"
    l, r = 0, len(s) - 1
    while l < r:
        T(f"s[{l}] = '{s[l]}' and s[{r}] = '{s[r]}' {'match' if s[l] == s[r] else 'differ'}", A("s", s, hl=[l, r], ok=list(range(l)) + list(range(r + 1, len(s))), l=l, r=r))
        if s[l] != s[r]:
            return False
        l, r = l + 1, r - 1
    T("Pointers met in the middle → palindrome", A("s", s, ok=range(len(s))))
    return True


LESSON("Core", "Opposite ends on a sorted array", """
<p>When the array is <b>sorted</b>, put <code>l</code> at the smallest value and <code>r</code> at the largest, and look at <code>a[l] + a[r]</code>:</p>
<ul>
<li><b>Too small?</b> <code>a[l]</code> paired with anything is too small too (everything else is ≤ a[r]). So <code>a[l]</code> is useless — move <code>l</code> right.</li>
<li><b>Too big?</b> By the same logic <code>a[r]</code> is useless — move <code>r</code> left.</li>
<li><b>Equal?</b> Found it.</li>
</ul>
<p>That argument — "this element can never be part of an answer, so drop it" — is what makes two pointers correct. Keep it in mind; interviewers ask "why does this work?".</p>
<p><b>Container with most water</b> uses the same shape with a different rule: the shorter wall limits the area, and moving the taller wall can never help, so always move the shorter one.</p>
<p><b>3Sum</b>: sort, fix one number with a loop, and run the pair search on the rest. Skip equal neighbours to avoid duplicate triples. O(n²) instead of O(n³).</p>
""", practice=[167, 11, 15, 16, 977, 881])


LESSON("Core", "Read and write pointers (in place)", """
<p>Both pointers move in the <b>same direction</b>. The reader <code>r</code> visits every element; the writer <code>w</code> marks where the next element you want to keep goes.</p>
<pre><code class="py">w = 0
for r in range(len(nums)):
    if keep(nums[r]):
        nums[w] = nums[r]
        w += 1
return w            # first w slots hold the kept elements</code></pre>
<p>This removes items or duplicates in place using O(1) extra memory. Elements before <code>w</code> are always "done".</p>
""", practice=[26, 27, 905])


@LD
def read_write_lesson():
    nums, val = [3, 2, 2, 3, 4, 3, 5], 3
    w = 0
    for r in range(len(nums)):
        if nums[r] != val:
            nums[w] = nums[r]
            w += 1
            T(f"Keep {nums[r]} → copy to slot {w - 1}", A("nums", nums, ok=range(w), hl=[r], w=w, r=r), at="prev")
        else:
            T(f"Skip {val}", A("nums", nums, ok=range(w), bad=[r], w=w, r=r))
    return w


LESSON("Core", "One pointer per sequence", """
<p>With two sorted lists (or strings), give each its own pointer and always advance the one that is "behind". This is the <b>merge</b> step of merge sort.</p>
<pre><code class="py">i = j = 0
out = []
while i &lt; len(a) and j &lt; len(b):
    if a[i] &lt;= b[j]:
        out.append(a[i]); i += 1
    else:
        out.append(b[j]); j += 1
out += a[i:] + b[j:]</code></pre>
<p>Variations: <b>is-subsequence</b> (advance in s only on a match), <b>intersection</b> (advance both on equal), and merging <b>from the back</b> when the first array has spare room at its end.</p>
""", practice=[88, 392, 350, 844])


@LD
def merge_lesson():
    a, b = [1, 4, 7], [2, 3, 8, 9]
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
        T(f"Take the smaller head → {out[-1]}", A("a", a, ok=range(i), i=i if i < len(a) else None), A("b", b, ok=range(j), j=j if j < len(b) else None), A("out", out), at="prev")
    out += a[i:] + b[j:]
    T("One list is empty → append the rest of the other", A("out", out, ok=range(len(out))))
    return out


LESSON("Advanced", "Harder two-pointer problems", """
<h4>k-Sum</h4>
<p>4Sum = two nested loops + the two-pointer pair search, O(n³). In general k-Sum costs O(n^(k−1)). Always sort first and skip duplicates at <b>every</b> level.</p>
<h4>Trapping rain water</h4>
<p>Water above bar i = <code>min(tallest on left, tallest on right) − height[i]</code>. With two pointers, keep <code>lmax</code> and <code>rmax</code>. Whichever side has the smaller max is the limiting side, so its water is already known — compute it and move that pointer. O(n) time, O(1) space.</p>
<h4>When two pointers is the wrong tool</h4>
<ul>
<li>The array is not sorted and you can't sort it (you need original indices) → use a hash map.</li>
<li>You need <b>contiguous</b> ranges with a condition → that's a sliding window (next topic), a close cousin.</li>
</ul>
""", practice=[18, 42, 680, 151])
