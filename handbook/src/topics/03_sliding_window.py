from lib import *

TOPIC(
    id="sliding-window", title="Sliding Window", glyph="[l..r]",
    blurb="Grow a window on the right, shrink it on the left, and never re-scan what's inside.",
    demo_title="Variable window: longest substring without repeating characters",
    theory="""
<h3>What it is</h3>
<p>A <b>window</b> is a contiguous range <code>[l, r]</code> of an array or string. Instead of recomputing every subarray from scratch (O(n²) or worse), we move <code>r</code> forward one step at a time and only move <code>l</code> forward when the window breaks a rule. Each index enters and leaves the window once, so the whole scan is O(n).</p>
<h3>Two kinds of window</h3>
<table>
<tr><th>Kind</th><th>Rule</th><th>Example</th></tr>
<tr><td><b>Fixed size k</b></td><td>add <code>a[r]</code>, remove <code>a[r − k]</code></td><td>max average of size k, anagrams of p in s</td></tr>
<tr><td><b>Variable size</b></td><td>expand <code>r</code>; while invalid, shrink <code>l</code></td><td>longest substring without repeats, min window substring</td></tr>
</table>
<h3>Spot the pattern</h3>
<ul>
<li>"Longest / shortest <b>contiguous</b> subarray or substring such that …"</li>
<li>"Number of subarrays with at most / exactly K …" → <code>exactly(K) = atMost(K) − atMost(K − 1)</code>.</li>
<li>The condition is <b>monotonic</b>: if a window is valid, every smaller window inside it is valid too (or the reverse). That's what makes shrinking from the left safe.</li>
<li>Window max/min in O(1) per step → a monotonic deque.</li>
</ul>
<h3>Template: variable window</h3>
<pre><code class="py">l = 0
state = {}                  # counts, sum, … of the window
for r, x in enumerate(a):
    add x to state
    while window is invalid:
        remove a[l] from state
        l += 1
    best = max(best, r - l + 1)  # window [l, r] is valid here</code></pre>
<h3>Common mistakes</h3>
<ul>
<li>Using sliding window when values can be negative and the goal is a sum — shrinking is no longer safe; use prefix sums instead.</li>
<li>Updating the answer before the window is made valid again.</li>
<li>Forgetting to delete keys whose count drops to 0, so <code>len(counts)</code> is wrong.</li>
</ul>
""")


@D
def window_demo():
    s = "abcabb"
    last, l, best = {}, 0, 0
    for r, ch in enumerate(s):
        if ch in last and last[ch] >= l:
            T(f"'{ch}' repeats inside the window → move l past its last position", A("s", s, hl=range(l, r + 1), bad=[r, last[ch]], l=l, r=r), M("last", last))
            l = last[ch] + 1
        last[ch] = r
        best = max(best, r - l + 1)
        T(f"Window '{s[l:r + 1]}' is valid, length {r - l + 1}", A("s", s, ok=range(l, r + 1), l=l, r=r), M("last", last), V(best=best), at="prev")
    return best


# 1 ---------------------------------------------------------------
Q(3, "Longest Substring Without Repeating Characters", "Medium", "Variable window · last index",
  "Return the length of the longest substring of <code>s</code> with no repeated characters.",
  [(("abcabcbb",), 3), (("bbbbb",), 1), (("pwwkew",), 3), (("",), 0)],
  ("Check every substring for duplicates with a set.", "O(n³)", "O(min(n, σ))"),
  ("Grow r. Store each character's last index; if s[r] was seen inside the window, jump l to one past that index. Record r − l + 1.", "O(n)", "O(σ)"),
  viz=("pwwkew",))


@B
def length_of_longest_substring(s):
    best = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            if len(set(s[i:j + 1])) == j - i + 1:
                best = max(best, j - i + 1)
    return best


@O
def length_of_longest_substring(s):
    last = {}
    l = best = 0
    for r, ch in enumerate(s):
        if ch in last and last[ch] >= l:
            l = last[ch] + 1
        last[ch] = r
        best = max(best, r - l + 1)
        T(f"Window '{s[l:r + 1]}' has no repeats; best = {best}", A("s", s, hl=range(l, r + 1), l=l, r=r), M("last", last, hl=ch), V(best=best), at="prev")
    return best


# 2 ---------------------------------------------------------------
Q(424, "Longest Repeating Character Replacement", "Medium", "Variable window · max count",
  "You may replace at most <code>k</code> characters of <code>s</code>. Return the length of the longest substring of one repeated letter you can get.",
  [(("ABAB", 2), 4), (("AABABBA", 1), 4)],
  ("For every substring, cost = length − count of its most common letter; keep the longest with cost ≤ k.", "O(n²)", "O(σ)"),
  ("Slide a window keeping letter counts and the highest count seen. If length − maxCount &gt; k, too many letters need replacing → shrink once from the left.", "O(n)", "O(σ)"))


@B
def character_replacement(s, k):
    best = 0
    for i in range(len(s)):
        count = {}
        for j in range(i, len(s)):
            count[s[j]] = count.get(s[j], 0) + 1
            if j - i + 1 - max(count.values()) <= k:
                best = max(best, j - i + 1)
    return best


@O
def character_replacement(s, k):
    count, l, maxf, best = {}, 0, 0, 0
    for r, ch in enumerate(s):
        count[ch] = count.get(ch, 0) + 1
        maxf = max(maxf, count[ch])
        if r - l + 1 - maxf > k:
            count[s[l]] -= 1
            l += 1
        best = max(best, r - l + 1)
        T(f"Window length {r - l + 1}, most common letter appears {maxf}× → replace {r - l + 1 - maxf} ≤ k", A("s", s, hl=range(l, r + 1), l=l, r=r), M("count", count), V(best=best), at="prev")
    return best


# 3 ---------------------------------------------------------------
Q(567, "Permutation in String", "Medium", "Fixed window · counts",
  "Return <code>True</code> if some permutation of <code>s1</code> appears as a substring of <code>s2</code>.",
  [(("ab", "eidbaooo"), True), (("ab", "eidboaoo"), False)],
  ("For every window of length |s1| in s2, sort it and compare to sorted(s1).", "O(n · m log m)", "O(m)"),
  ("Keep a fixed window of length |s1| sliding over s2 with letter counts. Compare the 26-count arrays (or track how many letters match) after each slide.", "O(n)", "O(1)"),
  viz=("abc", "ebcbaco"))


@B
def check_inclusion(s1, s2):
    m, target = len(s1), sorted(s1)
    return any(sorted(s2[i:i + m]) == target for i in range(len(s2) - m + 1))


@O
def check_inclusion(s1, s2):
    m = len(s1)
    if m > len(s2):
        return False
    need, win = [0] * 26, [0] * 26
    for ch in s1:
        need[ord(ch) - 97] += 1
    for r, ch in enumerate(s2):
        win[ord(ch) - 97] += 1
        if r >= m:
            win[ord(s2[r - m]) - 97] -= 1
        l = max(0, r - m + 1)
        T(f"Window '{s2[l:r + 1]}' — same letter counts as '{s1}'? {win == need}", A("s2", s2, hl=range(l, r + 1), l=l, r=r), at="prev")
        if win == need:
            return True
    return False


# 4 ---------------------------------------------------------------
Q(76, "Minimum Window Substring", "Hard", "Variable window · need / have",
  "Return the shortest substring of <code>s</code> containing every character of <code>t</code> (with multiplicity), or <code>\"\"</code>.",
  [(("ADOBECODEBANC", "ABC"), "BANC"), (("a", "a"), "a"), (("a", "aa"), "")],
  ("Check every substring of s for containing t's counts.", "O(n² · σ)", "O(σ)"),
  ("Expand r until the window covers t (have == need). Then shrink l as long as it still covers, recording the smallest. Track how many distinct letters are satisfied so the check is O(1).", "O(n + m)", "O(σ)"),
  viz=("ADOBECODEBANC", "ABC"))


@B
def min_window(s, t):
    from collections import Counter
    need, best = Counter(t), ""
    for i in range(len(s)):
        for j in range(i, len(s)):
            if not need - Counter(s[i:j + 1]):
                if not best or j - i + 1 < len(best):
                    best = s[i:j + 1]
                break
    return best


@O
def min_window(s, t):
    need = {}
    for ch in t:
        need[ch] = need.get(ch, 0) + 1
    have, required = 0, len(need)
    win, l, best = {}, 0, (float("inf"), 0, 0)
    for r, ch in enumerate(s):
        win[ch] = win.get(ch, 0) + 1
        if ch in need and win[ch] == need[ch]:
            have += 1
        while have == required:
            if r - l + 1 < best[0]:
                best = (r - l + 1, l, r)
            T(f"Window '{s[l:r + 1]}' covers '{t}' → try shrinking from the left", A("s", s, hl=range(l, r + 1), ok=range(best[1], best[2] + 1), l=l, r=r), V(have=have, required=required, best=s[best[1]:best[2] + 1]))
            win[s[l]] -= 1
            if s[l] in need and win[s[l]] < need[s[l]]:
                have -= 1
            l += 1
    return "" if best[0] == float("inf") else s[best[1]:best[2] + 1]


# 5 ---------------------------------------------------------------
Q(239, "Sliding Window Maximum", "Hard", "Monotonic deque",
  "Return the maximum of every window of size <code>k</code> as it slides across <code>nums</code>.",
  [(([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7]), (([1], 1), [1])],
  ("Compute max() of every window.", "O(n · k)", "O(1) extra"),
  ("Keep a deque of indices whose values are decreasing. Pop smaller values from the back before pushing (they can never be a max again); pop the front when it leaves the window. The front is always the max.", "O(n)", "O(k)"))


@B
def max_sliding_window(nums, k):
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]


@O
def max_sliding_window(nums, k):
    from collections import deque
    dq, res = deque(), []
    for r, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(r)
        if dq[0] <= r - k:
            dq.popleft()
        if r >= k - 1:
            res.append(nums[dq[0]])
        T(f"Deque (indices, values decreasing): front {dq[0]} → max {nums[dq[0]]}", A("nums", nums, hl=range(max(0, r - k + 1), r + 1), ok=[dq[0]], r=r), A("deque", [f"{i}:{nums[i]}" for i in dq]), A("res", res), at="prev")
    return res


# 6 ---------------------------------------------------------------
Q(209, "Minimum Size Subarray Sum", "Medium", "Variable window · sum",
  "All values are positive. Return the length of the shortest subarray with sum ≥ <code>target</code>, or 0.",
  [((7, [2, 3, 1, 2, 4, 3]), 2), ((4, [1, 4, 4]), 1), ((11, [1, 1, 1, 1, 1, 1, 1, 1]), 0)],
  ("Fix a start and extend until the sum reaches target.", "O(n²)", "O(1)"),
  ("Add nums[r] to the window sum. While the sum is at least target, record the length and drop nums[l]. Positive numbers make shrinking safe.", "O(n)", "O(1)"))


@B
def min_sub_array_len(target, nums):
    best = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total >= target:
                if not best or j - i + 1 < best:
                    best = j - i + 1
                break
    return best


@O
def min_sub_array_len(target, nums):
    l = total = 0
    best = float("inf")
    for r, x in enumerate(nums):
        total += x
        while total >= target:
            best = min(best, r - l + 1)
            T(f"Sum {total} ≥ {target}: length {r - l + 1}. Shrink.", A("nums", nums, hl=range(l, r + 1), l=l, r=r), V(sum=total, best=best))
            total -= nums[l]
            l += 1
    return 0 if best == float("inf") else best


# 7 ---------------------------------------------------------------
Q(1004, "Max Consecutive Ones III", "Medium", "Variable window · budget",
  "<code>nums</code> is binary. You may flip at most <code>k</code> zeros. Return the longest run of 1s possible.",
  [(([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2), 6), (([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3), 10)],
  ("For every subarray count its zeros; keep the longest with ≤ k zeros.", "O(n²)", "O(1)"),
  ("The window may contain at most k zeros. Expand r; when zeros exceed k, move l until one zero leaves.", "O(n)", "O(1)"),
  viz=([1, 0, 1, 1, 0, 0, 1, 1, 0, 1], 2))


@B
def longest_ones(nums, k):
    best = 0
    for i in range(len(nums)):
        zeros = 0
        for j in range(i, len(nums)):
            zeros += nums[j] == 0
            if zeros > k:
                break
            best = max(best, j - i + 1)
    return best


@O
def longest_ones(nums, k):
    l = zeros = best = 0
    for r, x in enumerate(nums):
        zeros += x == 0
        while zeros > k:
            zeros -= nums[l] == 0
            l += 1
        best = max(best, r - l + 1)
        T(f"Window has {zeros} zero(s) ≤ k = {k}, length {r - l + 1}", A("nums", nums, hl=range(l, r + 1), l=l, r=r), V(zeros=zeros, best=best), at="prev")
    return best


# 8 ---------------------------------------------------------------
Q(904, "Fruit Into Baskets", "Medium", "At most 2 distinct",
  "Walking right, you pick one fruit from every tree but your two baskets each hold one fruit type. Return the most fruit you can collect — the longest subarray with at most 2 distinct values.",
  [(([1, 2, 1],), 3), (([0, 1, 2, 2],), 3), (([1, 2, 3, 2, 2],), 4)],
  ("For every start, extend until a third type appears.", "O(n²)", "O(1)"),
  ("Window with a count map; when it holds 3 types, shrink from the left until a type's count reaches 0 and is removed.", "O(n)", "O(1)"),
  viz=([3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4],))


@B
def total_fruit(fruits):
    best = 0
    for i in range(len(fruits)):
        kinds = set()
        for j in range(i, len(fruits)):
            kinds.add(fruits[j])
            if len(kinds) > 2:
                break
            best = max(best, j - i + 1)
    return best


@O
def total_fruit(fruits):
    count, l, best = {}, 0, 0
    for r, f in enumerate(fruits):
        count[f] = count.get(f, 0) + 1
        while len(count) > 2:
            count[fruits[l]] -= 1
            if count[fruits[l]] == 0:
                del count[fruits[l]]
            l += 1
        best = max(best, r - l + 1)
        T(f"Types in basket: {list(count)}; window length {r - l + 1}", A("fruits", fruits, hl=range(l, r + 1), l=l, r=r), M("count", count), V(best=best), at="prev")
    return best


# 9 ---------------------------------------------------------------
Q(643, "Maximum Average Subarray I", "Easy", "Fixed window · sum",
  "Return the maximum average of any contiguous subarray of length <code>k</code>.",
  [(([1, 12, -5, -6, 50, 3], 4), 12.75), (([5], 1), 5.0)],
  ("Sum every window of length k from scratch.", "O(n · k)", "O(1)"),
  ("Keep the window sum: add the new element, subtract the one that falls out.", "O(n)", "O(1)"))


@B
def find_max_average(nums, k):
    return max(sum(nums[i:i + k]) for i in range(len(nums) - k + 1)) / k


@O
def find_max_average(nums, k):
    total = best = sum(nums[:k])
    T(f"First window sum = {total}", A("nums", nums, hl=range(k)), V(sum=total, best=best))
    for r in range(k, len(nums)):
        total += nums[r] - nums[r - k]
        best = max(best, total)
        T(f"+{nums[r]} −{nums[r - k]} → sum {total}", A("nums", nums, hl=range(r - k + 1, r + 1), r=r), V(sum=total, best=best), at="prev")
    return best / k


# 10 --------------------------------------------------------------
Q(438, "Find All Anagrams in a String", "Medium", "Fixed window · counts",
  "Return every start index in <code>s</code> where an anagram of <code>p</code> begins.",
  [(("cbaebabacd", "abc"), [0, 6]), (("abab", "ab"), [0, 1, 2])],
  ("Sort each window of length |p| and compare with sorted p.", "O(n · m log m)", "O(m)"),
  ("Slide a window of length |p| with a 26-count array and compare with p's counts at each step.", "O(n)", "O(1)"))


@B
def find_anagrams(s, p):
    m, key = len(p), sorted(p)
    return [i for i in range(len(s) - m + 1) if sorted(s[i:i + m]) == key]


@O
def find_anagrams(s, p):
    m, res = len(p), []
    need, win = [0] * 26, [0] * 26
    for ch in p:
        need[ord(ch) - 97] += 1
    for r, ch in enumerate(s):
        win[ord(ch) - 97] += 1
        if r >= m:
            win[ord(s[r - m]) - 97] -= 1
        if r >= m - 1 and win == need:
            res.append(r - m + 1)
        T(f"Window '{s[max(0, r - m + 1):r + 1]}'", A("s", s, hl=range(max(0, r - m + 1), r + 1), ok=res, r=r), A("res", res), at="prev")
    return res


# 11 --------------------------------------------------------------
Q(992, "Subarrays with K Different Integers", "Hard", "exactly = atMost(k) − atMost(k−1)",
  "Return the number of subarrays with exactly <code>k</code> distinct integers.",
  [(([1, 2, 1, 2, 3], 2), 7), (([1, 2, 1, 3, 4], 3), 3)],
  ("Enumerate every subarray and count its distinct values.", "O(n²)", "O(n)"),
  ("Counting 'at most k distinct' is easy with a window: each r adds r − l + 1 subarrays. Exactly k = atMost(k) − atMost(k − 1).", "O(n)", "O(n)"))


@B
def subarrays_with_k_distinct(nums, k):
    count = 0
    for i in range(len(nums)):
        seen = set()
        for j in range(i, len(nums)):
            seen.add(nums[j])
            count += len(seen) == k
    return count


@O
def subarrays_with_k_distinct(nums, k):
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
            T(f"atMost({k}): {r - l + 1} subarrays end at {r}", A("nums", nums, hl=range(l, r + 1), l=l, r=r), M("count", count), V(total=total), at="prev")
        return total
    return at_most(k) - at_most(k - 1)


# 12 --------------------------------------------------------------
Q(1358, "Number of Substrings Containing All Three Characters", "Medium", "Variable window · count starts",
  "<code>s</code> contains only a, b and c. Count the substrings that contain at least one of each.",
  [(("abcabc",), 10), (("aaacb",), 3), (("abc",), 1)],
  ("Check every substring.", "O(n²)", "O(1)"),
  ("For each r, shrink l while the window still has all three. Every start before l then works with this r, so add l.", "O(n)", "O(1)"))


@B
def number_of_substrings(s):
    count = 0
    for i in range(len(s)):
        seen = set()
        for j in range(i, len(s)):
            seen.add(s[j])
            count += len(seen) == 3
    return count


@O
def number_of_substrings(s):
    cnt = {"a": 0, "b": 0, "c": 0}
    l = total = 0
    for r, ch in enumerate(s):
        cnt[ch] += 1
        while all(cnt.values()):
            cnt[s[l]] -= 1
            l += 1
        total += l
        T(f"Substrings ending at {r} with a, b, c: starts 0..{l - 1} → +{l}", A("s", s, hl=range(l, r + 1), ok=range(l), l=l, r=r), M("count", cnt), V(total=total), at="prev")
    return total


# 13 --------------------------------------------------------------
Q(1423, "Maximum Points You Can Obtain from Cards", "Medium", "Window on the complement",
  "Take exactly <code>k</code> cards, each from the left or right end of the row. Maximise the total points.",
  [(([1, 2, 3, 4, 5, 6, 1], 3), 12), (([2, 2, 2], 2), 4), (([9, 7, 7, 9, 7, 7, 9], 7), 55)],
  ("Try taking i from the left and k − i from the right for every i, summing each time.", "O(k²)", "O(1)"),
  ("The cards you leave are a contiguous window of n − k. Minimise that window's sum with a fixed sliding window; answer = total − min.", "O(n)", "O(1)"))


@B
def max_score(card_points, k):
    best = 0
    for i in range(k + 1):
        best = max(best, sum(card_points[:i]) + sum(card_points[len(card_points) - (k - i):]))
    return best


@O
def max_score(card_points, k):
    n = len(card_points)
    w = n - k
    total = sum(card_points)
    cur = low = sum(card_points[:w])
    lo_l = 0
    T(f"Leave a window of {w} cards; its sum is {cur}", A("cards", card_points, hl=range(w)), V(total=total, window=cur))
    for r in range(w, n):
        cur += card_points[r] - card_points[r - w]
        if cur < low:
            low, lo_l = cur, r - w + 1
        T(f"Window {r - w + 1}..{r} sums to {cur}; smallest so far {low}", A("cards", card_points, hl=range(r - w + 1, r + 1), r=r), V(window=cur, smallest=low, answer=total - low), at="prev")
    return total - low


# 14 --------------------------------------------------------------
Q(219, "Contains Duplicate II", "Easy", "Window as a set",
  "Return <code>True</code> if two equal values sit at most <code>k</code> indices apart.",
  [(([1, 2, 3, 1], 3), True), (([1, 0, 1, 1], 1), True), (([1, 2, 3, 1, 2, 3], 2), False)],
  ("Compare each element with the next k elements.", "O(n · k)", "O(1)"),
  ("Keep a set of the last k values. If nums[i] is in it, a close duplicate exists; otherwise add it and evict nums[i − k].", "O(n)", "O(k)"))


@B
def contains_nearby_duplicate(nums, k):
    for i in range(len(nums)):
        for j in range(i + 1, min(len(nums), i + k + 1)):
            if nums[i] == nums[j]:
                return True
    return False


@O
def contains_nearby_duplicate(nums, k):
    window = set()
    for i, x in enumerate(nums):
        T(f"Is {x} among the last {k} values?", A("nums", nums, hl=range(max(0, i - k), i), i=i), M("window", window))
        if x in window:
            return True
        window.add(x)
        if len(window) > k:
            window.remove(nums[i - k])
    return False


# 15 --------------------------------------------------------------
Q(930, "Binary Subarrays With Sum", "Medium", "atMost trick on 0/1",
  "Count subarrays of binary <code>nums</code> whose sum equals <code>goal</code>.",
  [(([1, 0, 1, 0, 1], 2), 4), (([0, 0, 0, 0, 0], 0), 15)],
  ("Sum every subarray.", "O(n²)", "O(1)"),
  ("Count subarrays with sum ≤ goal using a window (r − l + 1 per step), then exactly(goal) = atMost(goal) − atMost(goal − 1).", "O(n)", "O(1)"))


@B
def num_subarrays_with_sum(nums, goal):
    count = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            count += total == goal
    return count


@O
def num_subarrays_with_sum(nums, goal):
    def at_most(g):
        if g < 0:
            return 0
        l = total = count = 0
        for r, x in enumerate(nums):
            total += x
            while total > g:
                total -= nums[l]
                l += 1
            count += r - l + 1
            T(f"atMost({g}): window sum {total}, +{r - l + 1}", A("nums", nums, hl=range(l, r + 1), l=l, r=r), V(count=count), at="prev")
        return count
    return at_most(goal) - at_most(goal - 1)


# 16 --------------------------------------------------------------
Q(1248, "Count Number of Nice Subarrays", "Medium", "atMost trick",
  "A subarray is nice if it contains exactly <code>k</code> odd numbers. Count them.",
  [(([1, 1, 2, 1, 1], 3), 2), (([2, 4, 6], 1), 0), (([2, 2, 2, 1, 2, 2, 1, 2, 2, 2], 2), 16)],
  ("Count odds in every subarray.", "O(n²)", "O(1)"),
  ("Same idea as binary subarrays: treat odd as 1, even as 0, and use atMost(k) − atMost(k − 1).", "O(n)", "O(1)"))


@B
def number_of_subarrays(nums, k):
    count = 0
    for i in range(len(nums)):
        odd = 0
        for j in range(i, len(nums)):
            odd += nums[j] % 2
            count += odd == k
    return count


@O
def number_of_subarrays(nums, k):
    def at_most(k):
        l = odd = count = 0
        for r, x in enumerate(nums):
            odd += x % 2
            while odd > k:
                odd -= nums[l] % 2
                l += 1
            count += r - l + 1
            T(f"atMost({k}) odds: window has {odd}, +{r - l + 1}", A("nums", nums, hl=range(l, r + 1), l=l, r=r), V(count=count), at="prev")
        return count
    return at_most(k) - at_most(k - 1)


# 17 --------------------------------------------------------------
Q(1456, "Maximum Number of Vowels in a Substring of Given Length", "Medium", "Fixed window · count",
  "Return the most vowels in any substring of <code>s</code> of length <code>k</code>.",
  [(("abciiidef", 3), 3), (("aeiou", 2), 2), (("leetcode", 3), 2)],
  ("Count vowels in every window from scratch.", "O(n · k)", "O(1)"),
  ("Slide a window of length k: +1 if the entering char is a vowel, −1 if the leaving one was.", "O(n)", "O(1)"))


@B
def max_vowels(s, k):
    return max(sum(c in "aeiou" for c in s[i:i + k]) for i in range(len(s) - k + 1))


@O
def max_vowels(s, k):
    cur = best = 0
    for r, ch in enumerate(s):
        cur += ch in "aeiou"
        if r >= k:
            cur -= s[r - k] in "aeiou"
        best = max(best, cur)
        T(f"Window '{s[max(0, r - k + 1):r + 1]}' has {cur} vowel(s)", A("s", s, hl=range(max(0, r - k + 1), r + 1), r=r), V(vowels=cur, best=best), at="prev")
    return best


# 18 --------------------------------------------------------------
Q(1052, "Grumpy Bookstore Owner", "Medium", "Fixed window · extra gain",
  "In minute i, <code>customers[i]</code> arrive; they're unhappy if <code>grumpy[i] = 1</code>. The owner can stay calm for one stretch of <code>minutes</code>. Maximise satisfied customers.",
  [(([1, 0, 1, 2, 1, 1, 7, 5], [0, 1, 0, 1, 0, 1, 0, 1], 3), 16), (([1], [0], 1), 1)],
  ("Try each calm window and recount all satisfied customers.", "O(n · m)", "O(1)"),
  ("Customers in non-grumpy minutes are always happy. The calm window only adds customers in grumpy minutes, so find the window of length minutes with the largest such sum.", "O(n)", "O(1)"))


@B
def max_satisfied(customers, grumpy, minutes):
    best, n = 0, len(customers)
    for s in range(n - minutes + 1):
        total = sum(customers[i] for i in range(n) if not grumpy[i] or s <= i < s + minutes)
        best = max(best, total)
    return best


@O
def max_satisfied(customers, grumpy, minutes):
    base = sum(c for c, g in zip(customers, grumpy) if not g)
    extra = best = 0
    for r in range(len(customers)):
        extra += customers[r] * grumpy[r]
        if r >= minutes:
            extra -= customers[r - minutes] * grumpy[r - minutes]
        best = max(best, extra)
        T(f"Calm window ending at {r} rescues {extra} customers", A("customers", customers, hl=range(max(0, r - minutes + 1), r + 1), r=r), A("grumpy", grumpy, bad=[i for i, g in enumerate(grumpy) if g]), V(base=base, extra=extra, best=best), at="prev")
    return base + best


# 19 --------------------------------------------------------------
Q(1493, "Longest Subarray of 1's After Deleting One Element", "Medium", "At most one zero",
  "Delete exactly one element from binary <code>nums</code>. Return the longest run of 1s left.",
  [(([1, 1, 0, 1],), 3), (([0, 1, 1, 1, 0, 1, 1, 0, 1],), 5), (([1, 1, 1],), 2)],
  ("Delete each index in turn and measure the longest run.", "O(n²)", "O(n)"),
  ("Longest window with at most one zero, minus one (the deleted element).", "O(n)", "O(1)"))


@B
def longest_subarray(nums):
    best = 0
    for d in range(len(nums)):
        rest, run = nums[:d] + nums[d + 1:], 0
        for x in rest:
            run = run + 1 if x else 0
            best = max(best, run)
    return best


@O
def longest_subarray(nums):
    l = zeros = best = 0
    for r, x in enumerate(nums):
        zeros += x == 0
        while zeros > 1:
            zeros -= nums[l] == 0
            l += 1
        best = max(best, r - l)
        T(f"Window {l}..{r} has {zeros} zero(s); after deleting one element: {r - l}", A("nums", nums, hl=range(l, r + 1), l=l, r=r), V(best=best), at="prev")
    return best


# 20 --------------------------------------------------------------
Q(1838, "Frequency of the Most Frequent Element", "Medium", "Sort + window cost",
  "In one operation you add 1 to any element. With at most <code>k</code> operations, return the highest possible frequency of one value.",
  [(([1, 2, 4], 5), 3), (([1, 4, 8, 13], 5), 2), (([3, 9, 6], 2), 1)],
  ("For each target value, greedily raise the closest smaller values.", "O(n²)", "O(1)"),
  ("Sort. In window [l, r] raise everything to nums[r]; cost = nums[r] · len − windowSum. Shrink while cost &gt; k.", "O(n log n)", "O(1)"))


@B
def max_frequency(nums, k):
    nums = sorted(nums)
    best = 1
    for r in range(len(nums)):
        budget, l = k, r
        while l > 0 and budget >= nums[r] - nums[l - 1]:
            budget -= nums[r] - nums[l - 1]
            l -= 1
        best = max(best, r - l + 1)
    return best


@O
def max_frequency(nums, k):
    nums.sort()
    l = total = best = 0
    for r, x in enumerate(nums):
        total += x
        while x * (r - l + 1) - total > k:
            total -= nums[l]
            l += 1
        best = max(best, r - l + 1)
        T(f"Raise window to {x}: cost {x} × {r - l + 1} − {total} = {x * (r - l + 1) - total} ≤ {k}", A("nums", nums, hl=range(l, r + 1), l=l, r=r), V(best=best), at="prev")
    return best
