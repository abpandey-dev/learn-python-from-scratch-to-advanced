from lib import *

TOPIC(
    id="two-pointers", title="Two Pointers", glyph="i→ ←j",
    blurb="Two indices walking toward each other or in the same direction to replace a nested loop.",
    demo_title="Opposite ends on a sorted array: move the pointer that can fix the sum",
    theory="""
<h3>What it is</h3>
<p>Instead of trying every pair with two nested loops, keep two indices and move <b>one of them</b> each step based on what you see. Every move rules out a whole row of pairs at once, so O(n²) pairs are checked in O(n) steps.</p>
<h3>The three shapes</h3>
<table>
<tr><th>Shape</th><th>How pointers move</th><th>Typical problems</th></tr>
<tr><td><b>Opposite ends</b></td><td><code>l = 0, r = n − 1</code>, move inward</td><td>pair sum in sorted array, palindrome, container with most water</td></tr>
<tr><td><b>Same direction (read / write)</b></td><td><code>r</code> scans every element, <code>w</code> marks where the next kept item goes</td><td>remove duplicates, remove element, move zeroes</td></tr>
<tr><td><b>Two sequences</b></td><td>one pointer per array, advance the smaller</td><td>merge sorted arrays, is-subsequence, intersection</td></tr>
</table>
<h3>Spot the pattern</h3>
<ul>
<li>The input is <b>sorted</b> (or you can sort it) and you need a pair / triple with some sum → opposite ends.</li>
<li>"Do it <b>in place</b>" or "return the new length" → read/write pointers.</li>
<li>Something is <b>symmetric</b> (palindrome, reverse) → opposite ends swapping or comparing.</li>
<li>3Sum / 4Sum → fix one (or two) elements with a loop, two-pointer the rest.</li>
</ul>
<h3>Template: opposite ends</h3>
<pre><code class="py">l, r = 0, len(a) - 1
while l &lt; r:
    s = a[l] + a[r]
    if s == target: return [l, r]
    if s &lt; target: l += 1   # need bigger → drop the smallest
    else:          r -= 1   # need smaller → drop the largest</code></pre>
<h3>Why it's correct</h3>
<p>In a sorted array, if <code>a[l] + a[r]</code> is too small then <code>a[l]</code> with <i>any</i> element left of <code>r</code> is also too small, so <code>l</code> can never be part of an answer — it is safe to discard it. The same argument works for <code>r</code> when the sum is too big.</p>
<h3>Common mistakes</h3>
<ul>
<li>Forgetting to skip duplicates in 3Sum, producing the same triple twice.</li>
<li>Using <code>l &lt;= r</code> when the two pointers must be different elements.</li>
<li>Using opposite-end pointers on an unsorted array — the "safe to discard" argument needs order.</li>
</ul>
""")


@D
def pair_sum_demo():
    a, target = [1, 3, 4, 6, 8, 11], 10
    l, r = 0, len(a) - 1
    while l < r:
        total = a[l] + a[r]
        T(f"a[l] + a[r] = {a[l]} + {a[r]} = {total} vs target {target}", A("a", a, hl=[l, r], l=l, r=r), V(sum=total))
        if total == target:
            T("Found the pair", A("a", a, ok=[l, r], l=l, r=r))
            return [l, r]
        if total < target:
            l += 1
        else:
            r -= 1


# 1 ---------------------------------------------------------------
Q(125, "Valid Palindrome", "Easy", "Opposite ends",
  "After lower-casing and dropping every non-alphanumeric character, does <code>s</code> read the same forwards and backwards?",
  [(("A man, a plan, a canal: Panama",), True), (("race a car",), False), ((" ",), True)],
  ("Build the cleaned string and compare it with its reverse.", "O(n)", "O(n)"),
  ("Two pointers from both ends skip non-alphanumeric characters and compare letters case-insensitively — no extra string needed.", "O(n)", "O(1)"),
  viz=("Ab,c;bA",))


@B
def is_palindrome(s):
    clean = [c.lower() for c in s if c.isalnum()]
    return clean == clean[::-1]


@O
def is_palindrome(s):
    l, r = 0, len(s) - 1
    while l < r:
        while l < r and not s[l].isalnum():
            l += 1
        while l < r and not s[r].isalnum():
            r -= 1
        T(f"Compare '{s[l]}' and '{s[r]}'", A("s", s, hl=[l, r], l=l, r=r))
        if s[l].lower() != s[r].lower():
            return False
        l, r = l + 1, r - 1
    T("Pointers met — it is a palindrome", A("s", s, ok=range(len(s))))
    return True


# 2 ---------------------------------------------------------------
Q(167, "Two Sum II - Input Array Is Sorted", "Medium", "Opposite ends",
  "<code>numbers</code> is sorted ascending. Return the 1-based indices of the two numbers that add up to <code>target</code>, using O(1) extra space.",
  [(([2, 7, 11, 15], 9), [1, 2]), (([2, 3, 4], 6), [1, 3]), (([-1, 0], -1), [1, 2])],
  ("Try every pair.", "O(n²)", "O(1)"),
  ("Start at both ends. Sum too small → move l right; too big → move r left. Sorting guarantees we never skip the answer.", "O(n)", "O(1)"),
  viz=([1, 2, 4, 6, 9, 12], 8))


@B
def two_sum_sorted(numbers, target):
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == target:
                return [i + 1, j + 1]


@O
def two_sum_sorted(numbers, target):
    l, r = 0, len(numbers) - 1
    while l < r:
        total = numbers[l] + numbers[r]
        T(f"{numbers[l]} + {numbers[r]} = {total}", A("numbers", numbers, hl=[l, r], l=l, r=r), V(target=target, sum=total))
        if total == target:
            return [l + 1, r + 1]
        if total < target:
            l += 1
        else:
            r -= 1


# 3 ---------------------------------------------------------------
Q(15, "3Sum", "Medium", "Sort + two pointers",
  "Return every unique triplet <code>[a, b, c]</code> from <code>nums</code> with a + b + c = 0.",
  [(([-1, 0, 1, 2, -1, -4],), [[-1, -1, 2], [-1, 0, 1]]), (([0, 1, 1],), []), (([0, 0, 0],), [[0, 0, 0]])],
  ("Try every triple i &lt; j &lt; k and collect sorted triples in a set.", "O(n³)", "O(n)"),
  ("Sort. Fix nums[i] and find pairs summing to −nums[i] with two pointers on the rest. Skip equal neighbours so each triplet appears once.", "O(n²)", "O(1) extra"),
  norm=lambda r: sorted(sorted(x) for x in r))


@B
def three_sum(nums):
    n, res = len(nums), set()
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    res.add(tuple(sorted((nums[i], nums[j], nums[k]))))
    return [list(t) for t in res]


@O
def three_sum(nums):
    nums.sort()
    res = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        l, r = i + 1, len(nums) - 1
        while l < r:
            total = nums[i] + nums[l] + nums[r]
            T(f"Fix {nums[i]}: {nums[i]} + {nums[l]} + {nums[r]} = {total}", A("nums", nums, hl=[l, r], ok=[i], i=i, l=l, r=r), V(found=res))
            if total < 0:
                l += 1
            elif total > 0:
                r -= 1
            else:
                res.append([nums[i], nums[l], nums[r]])
                while l < r and nums[l] == nums[l + 1]:
                    l += 1
                l, r = l + 1, r - 1
    return res


# 4 ---------------------------------------------------------------
Q(11, "Container With Most Water", "Medium", "Opposite ends · greedy",
  "Line i has height <code>height[i]</code>. Pick two lines that, with the x-axis, hold the most water and return that area.",
  [(([1, 8, 6, 2, 5, 4, 8, 3, 7],), 49), (([1, 1],), 1)],
  ("Try every pair of lines.", "O(n²)", "O(1)"),
  ("Start with the widest pair. The shorter line limits the area, and moving the taller one inward can only shrink it — so always move the shorter line.", "O(n)", "O(1)"))


@B
def max_area(height):
    best = 0
    for i in range(len(height)):
        for j in range(i + 1, len(height)):
            best = max(best, (j - i) * min(height[i], height[j]))
    return best


@O
def max_area(height):
    l, r, best = 0, len(height) - 1, 0
    while l < r:
        area = (r - l) * min(height[l], height[r])
        best = max(best, area)
        T(f"width {r - l} × min({height[l]}, {height[r]}) = {area}. Move the shorter line.", A("height", height, hl=[l, r], l=l, r=r), V(area=area, best=best), at="prev")
        if height[l] < height[r]:
            l += 1
        else:
            r -= 1
    return best


# 5 ---------------------------------------------------------------
Q(42, "Trapping Rain Water", "Hard", "Opposite ends · running max",
  "Given bar heights, compute how much rain water is trapped between the bars.",
  [(([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],), 6), (([4, 2, 0, 3, 2, 5],), 9)],
  ("For each bar, scan left and right for the tallest walls; water above it is min(leftMax, rightMax) − height.", "O(n²)", "O(1)"),
  ("Move the pointer with the smaller running max. That side's water is fully decided by its own max, because the other side is known to be at least as tall.", "O(n)", "O(1)"),
  viz=([3, 0, 2, 0, 4, 1, 2],))


@B
def trap(height):
    water = 0
    for i in range(len(height)):
        left = max(height[:i + 1])
        right = max(height[i:])
        water += min(left, right) - height[i]
    return water


@O
def trap(height):
    l, r = 0, len(height) - 1
    lmax = rmax = water = 0
    while l < r:
        if height[l] < height[r]:
            lmax = max(lmax, height[l])
            water += lmax - height[l]
            T(f"Left side: water at {l} = lmax {lmax} − {height[l]} = {lmax - height[l]}", A("height", height, hl=[l], l=l, r=r), V(lmax=lmax, rmax=rmax, water=water), at="prev")
            l += 1
        else:
            rmax = max(rmax, height[r])
            water += rmax - height[r]
            T(f"Right side: water at {r} = rmax {rmax} − {height[r]} = {rmax - height[r]}", A("height", height, hl=[r], l=l, r=r), V(lmax=lmax, rmax=rmax, water=water), at="prev")
            r -= 1
    return water


# 6 ---------------------------------------------------------------
Q(26, "Remove Duplicates from Sorted Array", "Easy", "Read / write",
  "Remove duplicates from sorted <code>nums</code> in place so each value appears once, and return the count k of unique values (the first k slots hold them).",
  [(([1, 1, 2],), 2), (([0, 0, 1, 1, 1, 2, 2, 3, 3, 4],), 5)],
  ("Copy unique values into a new list, write them back, return its length.", "O(n)", "O(n)"),
  ("w points at the last unique value written. When nums[r] differs from nums[w], it's new: write it at w + 1.", "O(n)", "O(1)"),
  viz=([0, 0, 1, 1, 1, 2, 2, 3],))


@B
def remove_duplicates(nums):
    uniq = []
    for x in nums:
        if not uniq or uniq[-1] != x:
            uniq.append(x)
    nums[:len(uniq)] = uniq
    return len(uniq)


@O
def remove_duplicates(nums):
    w = 0
    for r in range(1, len(nums)):
        if nums[r] != nums[w]:
            w += 1
            nums[w] = nums[r]
        T(f"r = {r}: nums[{r}] = {nums[r]}. Unique values so far: {w + 1}", A("nums", nums, ok=range(w + 1), hl=[r], w=w, r=r), at="prev")
    return w + 1


# 7 ---------------------------------------------------------------
Q(88, "Merge Sorted Array", "Easy", "Fill from the back",
  "Merge sorted <code>nums2</code> (n items) into sorted <code>nums1</code>, which has m items followed by n spare zeros. Modify nums1 in place.",
  [(([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3), [1, 2, 2, 3, 5, 6]), (([1], 1, [], 0), [1]), (([0], 0, [1], 1), [1])],
  ("Copy nums2 into the spare slots and sort.", "O((m+n) log(m+n))", "O(1)"),
  ("Fill nums1 from the end: compare the largest remaining of each array and place the bigger at position k. Nothing useful gets overwritten.", "O(m + n)", "O(1)"),
  inplace=0)


@B
def merge(nums1, m, nums2, n):
    nums1[m:] = nums2
    nums1.sort()


@O
def merge(nums1, m, nums2, n):
    i, j, k = m - 1, n - 1, m + n - 1
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        T(f"Place the larger tail value at k = {k}", A("nums1", nums1, ok=range(k, m + n), i=i if i >= 0 else None, k=k), A("nums2", nums2, j=j if j >= 0 else None), at="prev")
        k -= 1


# 8 ---------------------------------------------------------------
Q(977, "Squares of a Sorted Array", "Easy", "Opposite ends",
  "Given sorted <code>nums</code> (may contain negatives), return the squares of each number, sorted.",
  [(([-4, -1, 0, 3, 10],), [0, 1, 9, 16, 100]), (([-7, -3, 2, 3, 11],), [4, 9, 9, 49, 121])],
  ("Square everything, then sort.", "O(n log n)", "O(n)"),
  ("The largest square is at one of the two ends. Compare |nums[l]| and |nums[r]|, write the bigger square at the back of the result, and move that pointer.", "O(n)", "O(n) output"))


@B
def sorted_squares(nums):
    return sorted(x * x for x in nums)


@O
def sorted_squares(nums):
    n = len(nums)
    res = [0] * n
    l, r = 0, n - 1
    for k in range(n - 1, -1, -1):
        if abs(nums[l]) > abs(nums[r]):
            res[k] = nums[l] ** 2
            l += 1
        else:
            res[k] = nums[r] ** 2
            r -= 1
        T(f"Bigger square goes to res[{k}]", A("nums", nums, l=l, r=r), A("res", res, ok=range(k, n), k=k), at="prev")
    return res


# 9 ---------------------------------------------------------------
Q(344, "Reverse String", "Easy", "Opposite ends · swap",
  "Reverse a list of characters in place.",
  [((["h", "e", "l", "l", "o"],), ["o", "l", "l", "e", "h"]), ((["H", "a", "n", "n", "a", "h"],), ["h", "a", "n", "n", "a", "H"])],
  ("Build a reversed copy and write it back.", "O(n)", "O(n)"),
  ("Swap s[l] and s[r], then move both pointers inward until they meet.", "O(n)", "O(1)"),
  inplace=0,
  viz=(list("abcdef"),))


@B
def reverse_string(s):
    s[:] = [s[i] for i in range(len(s) - 1, -1, -1)]


@O
def reverse_string(s):
    l, r = 0, len(s) - 1
    while l < r:
        s[l], s[r] = s[r], s[l]
        T(f"Swap positions {l} and {r}", A("s", s, hl=[l, r], l=l, r=r), at="prev")
        l, r = l + 1, r - 1


# 10 --------------------------------------------------------------
Q(18, "4Sum", "Medium", "Sort + two loops + two pointers",
  "Return all unique quadruplets in <code>nums</code> that sum to <code>target</code>.",
  [(([1, 0, -1, 0, -2, 2], 0), [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]), (([2, 2, 2, 2, 2], 8), [[2, 2, 2, 2]])],
  ("Try every 4-element combination and keep unique sorted ones.", "O(n⁴)", "O(n)"),
  ("Sort. Two nested loops fix a and b; two pointers find c + d = target − a − b. Skip duplicates at every level.", "O(n³)", "O(1) extra"),
  norm=lambda r: sorted(sorted(x) for x in r), viz=([2, -1, 0, 1, -2, 0], 0))


@B
def four_sum(nums, target):
    from itertools import combinations
    return [list(c) for c in {tuple(sorted(c)) for c in combinations(nums, 4) if sum(c) == target}]


@O
def four_sum(nums, target):
    nums.sort()
    n, res = len(nums), []
    for a in range(n - 3):
        if a > 0 and nums[a] == nums[a - 1]:
            continue
        for b in range(a + 1, n - 2):
            if b > a + 1 and nums[b] == nums[b - 1]:
                continue
            l, r = b + 1, n - 1
            while l < r:
                total = nums[a] + nums[b] + nums[l] + nums[r]
                T(f"{nums[a]} + {nums[b]} + {nums[l]} + {nums[r]} = {total}", A("nums", nums, ok=[a, b], hl=[l, r], a=a, b=b, l=l, r=r), V(found=res))
                if total < target:
                    l += 1
                elif total > target:
                    r -= 1
                else:
                    res.append([nums[a], nums[b], nums[l], nums[r]])
                    while l < r and nums[l] == nums[l + 1]:
                        l += 1
                    l, r = l + 1, r - 1
    return res


# 11 --------------------------------------------------------------
Q(16, "3Sum Closest", "Medium", "Sort + two pointers",
  "Find three integers in <code>nums</code> whose sum is closest to <code>target</code> and return that sum.",
  [(([-1, 2, 1, -4], 1), 2), (([0, 0, 0], 1), 0)],
  ("Try every triple and keep the closest sum.", "O(n³)", "O(1)"),
  ("Sort, fix one element, and move two pointers toward the target sum, tracking the closest seen.", "O(n²)", "O(1)"),
  viz=([-4, -1, 1, 2, 5], 3))


@B
def three_sum_closest(nums, target):
    best = nums[0] + nums[1] + nums[2]
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                s = nums[i] + nums[j] + nums[k]
                if abs(s - target) < abs(best - target):
                    best = s
    return best


@O
def three_sum_closest(nums, target):
    nums.sort()
    best = nums[0] + nums[1] + nums[2]
    for i in range(len(nums) - 2):
        l, r = i + 1, len(nums) - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if abs(s - target) < abs(best - target):
                best = s
            T(f"sum {s}, closest so far {best}", A("nums", nums, ok=[i], hl=[l, r], i=i, l=l, r=r), V(target=target, best=best), at="prev")
            if s < target:
                l += 1
            elif s > target:
                r -= 1
            else:
                return s
    return best


# 12 --------------------------------------------------------------
Q(680, "Valid Palindrome II", "Easy", "Opposite ends · one skip",
  "Return <code>True</code> if <code>s</code> can become a palindrome after deleting at most one character.",
  [(("aba",), True), (("abca",), True), (("abc",), False)],
  ("Try deleting each character and check if the rest is a palindrome.", "O(n²)", "O(n)"),
  ("Compare from both ends. At the first mismatch, the only options are skipping s[l] or skipping s[r] — check each remaining middle once.", "O(n)", "O(1)"),
  viz=("racecbar",))


@B
def valid_palindrome(s):
    if s == s[::-1]:
        return True
    for i in range(len(s)):
        t = s[:i] + s[i + 1:]
        if t == t[::-1]:
            return True
    return False


@O
def valid_palindrome(s):
    def is_pal(l, r):
        while l < r:
            if s[l] != s[r]:
                return False
            l, r = l + 1, r - 1
        return True

    l, r = 0, len(s) - 1
    while l < r:
        T(f"Compare '{s[l]}' and '{s[r]}'", A("s", s, hl=[l, r], l=l, r=r))
        if s[l] != s[r]:
            T(f"Mismatch → try skipping s[{l}] or s[{r}]", A("s", s, bad=[l, r], l=l, r=r))
            return is_pal(l + 1, r) or is_pal(l, r - 1)
        l, r = l + 1, r - 1
    return True


# 13 --------------------------------------------------------------
Q(392, "Is Subsequence", "Easy", "Two sequences",
  "Return <code>True</code> if <code>s</code> can be formed by deleting some characters of <code>t</code> without reordering.",
  [(("abc", "ahbgdc"), True), (("axc", "ahbgdc"), False), (("", "abc"), True)],
  ("Try every subset of positions of t (2^|t| options).", "O(2^m · n)", "O(m)"),
  ("Walk t with pointer j; advance i in s whenever the characters match. s is a subsequence if i reaches the end.", "O(m)", "O(1)"))


@B
def is_subsequence(s, t):
    from itertools import combinations
    return any("".join(c) == s for c in combinations(t, len(s)))


@O
def is_subsequence(s, t):
    i = 0
    for j, ch in enumerate(t):
        if i < len(s) and s[i] == ch:
            T(f"t[{j}] = '{ch}' matches s[{i}] → advance i", A("s", s, ok=range(i + 1), i=i), A("t", t, hl=[j], j=j))
            i += 1
        else:
            T(f"t[{j}] = '{ch}' doesn't match", A("s", s, ok=range(i), i=i), A("t", t, j=j))
    return i == len(s)


# 14 --------------------------------------------------------------
Q(27, "Remove Element", "Easy", "Read / write",
  "Remove every occurrence of <code>val</code> from <code>nums</code> in place and return how many elements remain.",
  [(([3, 2, 2, 3], 3), 2), (([0, 1, 2, 2, 3, 0, 4, 2], 2), 5)],
  ("Build a filtered copy and write it back.", "O(n)", "O(n)"),
  ("Write pointer w: copy every element that is not val to nums[w] and advance w.", "O(n)", "O(1)"))


@B
def remove_element(nums, val):
    keep = [x for x in nums if x != val]
    nums[:len(keep)] = keep
    return len(keep)


@O
def remove_element(nums, val):
    w = 0
    for r in range(len(nums)):
        if nums[r] != val:
            nums[w] = nums[r]
            w += 1
        T(f"nums[{r}] = {nums[r]} {'≠' if nums[r] != val else '='} {val}", A("nums", nums, ok=range(w), hl=[r], w=w, r=r), at="prev")
    return w


# 15 --------------------------------------------------------------
Q(881, "Boats to Save People", "Medium", "Sort + greedy pairing",
  "Each boat carries at most two people and at most <code>limit</code> weight. Return the minimum number of boats.",
  [(([1, 2], 3), 1), (([3, 2, 2, 1], 3), 3), (([3, 5, 3, 4], 5), 4)],
  ("Try every way to pair people (exponential).", "O(n!)", "O(n)"),
  ("Sort. The heaviest person always takes a boat; pair them with the lightest if they fit together. Move the pointers inward.", "O(n log n)", "O(1)"),
  viz=([3, 2, 5, 1, 4], 6))


@B
def num_rescue_boats(people, limit):
    from functools import lru_cache
    people = tuple(sorted(people))

    @lru_cache(None)
    def go(rest):
        if not rest:
            return 0
        first, others = rest[0], rest[1:]
        best = 1 + go(others)
        for i in range(len(others)):
            if first + others[i] <= limit:
                best = min(best, 1 + go(others[:i] + others[i + 1:]))
        return best
    return go(people)


@O
def num_rescue_boats(people, limit):
    people.sort()
    l, r, boats = 0, len(people) - 1, 0
    while l <= r:
        pair = l < r and people[l] + people[r] <= limit
        T(f"Heaviest {people[r]}{' + lightest ' + str(people[l]) + ' fit together' if pair else ' goes alone'}", A("people", people, hl=[l, r] if pair else [r], l=l, r=r), V(boats=boats + 1))
        if people[l] + people[r] <= limit:
            l += 1
        r -= 1
        boats += 1
    return boats


# 16 --------------------------------------------------------------
Q(844, "Backspace String Compare", "Easy", "Two pointers from the back",
  "<code>#</code> means backspace. Return <code>True</code> if <code>s</code> and <code>t</code> are equal after typing them into empty editors.",
  [(("ab#c", "ad#c"), True), (("ab##", "c#d#"), True), (("a#c", "b"), False)],
  ("Simulate both strings with a stack and compare.", "O(n + m)", "O(n + m)"),
  ("Walk both strings from the end, counting pending backspaces to skip characters; compare the next real characters.", "O(n + m)", "O(1)"))


@B
def backspace_compare(s, t):
    def build(x):
        st = []
        for c in x:
            if c == "#":
                if st:
                    st.pop()
            else:
                st.append(c)
        return st
    return build(s) == build(t)


@O
def backspace_compare(s, t):
    def next_char(x, i):
        skip = 0
        while i >= 0:
            if x[i] == "#":
                skip += 1
            elif skip:
                skip -= 1
            else:
                break
            i -= 1
        return i

    i, j = len(s) - 1, len(t) - 1
    while True:
        i, j = next_char(s, i), next_char(t, j)
        T(f"Next real characters: {s[i] if i >= 0 else '∅'} vs {t[j] if j >= 0 else '∅'}", A("s", s, hl=[i], i=i if i >= 0 else None), A("t", t, hl=[j], j=j if j >= 0 else None))
        if i < 0 or j < 0:
            return i < 0 and j < 0
        if s[i] != t[j]:
            return False
        i, j = i - 1, j - 1


# 17 --------------------------------------------------------------
Q(905, "Sort Array By Parity", "Easy", "Partition",
  "Move all even numbers before all odd numbers (any order inside each group).",
  [(([3, 1, 2, 4],), [2, 4, 3, 1]), (([0],), [0])],
  ("Return evens + odds as two new lists.", "O(n)", "O(n)"),
  ("Partition in place: l looks for an odd from the left, r for an even from the right; swap them.", "O(n)", "O(1)"),
  check=lambda a, out: sorted(out) == sorted(a[0]) and all(x % 2 == 0 for x in out[:sum(1 for y in out if y % 2 == 0)]),
  viz=([3, 1, 2, 4, 7, 6],))


@B
def sort_array_by_parity(nums):
    return [x for x in nums if x % 2 == 0] + [x for x in nums if x % 2]


@O
def sort_array_by_parity(nums):
    l, r = 0, len(nums) - 1
    while l < r:
        if nums[l] % 2 > nums[r] % 2:
            nums[l], nums[r] = nums[r], nums[l]
            T("Odd on the left, even on the right → swap", A("nums", nums, hl=[l, r], l=l, r=r), at="prev")
        if nums[l] % 2 == 0:
            l += 1
        if nums[r] % 2 == 1:
            r -= 1
        T("Advance pointers past correctly placed numbers", A("nums", nums, ok=list(range(l)) + list(range(r + 1, len(nums))), l=l, r=r))
    return nums


# 18 --------------------------------------------------------------
Q(350, "Intersection of Two Arrays II", "Easy", "Sort + two sequences",
  "Return the intersection of two arrays, where each element appears as many times as it shows in both.",
  [(([1, 2, 2, 1], [2, 2]), [2, 2]), (([4, 9, 5], [9, 4, 9, 8, 4]), [4, 9])],
  ("For each element of nums1, search and remove a match in a copy of nums2.", "O(n · m)", "O(m)"),
  ("Sort both, then walk them together: equal → take it and advance both; otherwise advance the smaller.", "O(n log n + m log m)", "O(1) extra"),
  norm=sorted)


@B
def intersect(nums1, nums2):
    rest, res = list(nums2), []
    for x in nums1:
        if x in rest:
            rest.remove(x)
            res.append(x)
    return res


@O
def intersect(nums1, nums2):
    nums1.sort()
    nums2.sort()
    i = j = 0
    res = []
    while i < len(nums1) and j < len(nums2):
        T(f"{nums1[i]} vs {nums2[j]}", A("nums1", nums1, hl=[i], i=i), A("nums2", nums2, hl=[j], j=j), A("res", res))
        if nums1[i] == nums2[j]:
            res.append(nums1[i])
            i, j = i + 1, j + 1
        elif nums1[i] < nums2[j]:
            i += 1
        else:
            j += 1
    return res


# 19 --------------------------------------------------------------
Q(151, "Reverse Words in a String", "Medium", "Reverse twice",
  "Reverse the order of words in <code>s</code>. Words are separated by one or more spaces; return them joined by single spaces.",
  [(("the sky is blue",), "blue is sky the"), (("  hello world  ",), "world hello"), (("a good   example",), "example good a")],
  ("Split on spaces, reverse the list, join.", "O(n)", "O(n)"),
  ("Without split: reverse the whole character list, then reverse each word back, then compact the spaces with a write pointer. This is the in-place version asked in follow-ups.", "O(n)", "O(1) extra for a mutable string"),
  viz=("the sky  blue",))


@B
def reverse_words(s):
    return " ".join(s.split()[::-1])


@O
def reverse_words(s):
    a = list(s)

    def rev(l, r):
        while l < r:
            a[l], a[r] = a[r], a[l]
            l, r = l + 1, r - 1

    rev(0, len(a) - 1)
    T("1) Reverse every character", A("a", a))
    n, i = len(a), 0
    while i < n:
        if a[i] == " ":
            i += 1
            continue
        j = i
        while j < n and a[j] != " ":
            j += 1
        rev(i, j - 1)
        T(f"2) Reverse the word at {i}..{j - 1} back", A("a", a, ok=range(i, j), i=i, j=j), at="prev")
        i = j
    w = 0
    for r in range(n):
        if a[r] != " " or (w > 0 and a[w - 1] != " "):
            a[w] = a[r]
            w += 1
    if w > 0 and a[w - 1] == " ":
        w -= 1
    T("3) Squeeze extra spaces with a write pointer", A("a", a[:w], ok=range(w)))
    return "".join(a[:w])


# 20 --------------------------------------------------------------
Q(345, "Reverse Vowels of a String", "Easy", "Opposite ends · swap",
  "Reverse only the vowels (a, e, i, o, u in either case) of <code>s</code>.",
  [(("IceCreAm",), "AceCreIm"), (("leetcode",), "leotcede")],
  ("Collect the vowels, then rebuild the string taking vowels from the end of that list.", "O(n)", "O(n)"),
  ("Two pointers move inward, each stopping at a vowel; swap them.", "O(n)", "O(n) for the list copy, O(1) extra otherwise"))


@B
def reverse_vowels(s):
    vow = [c for c in s if c in "aeiouAEIOU"]
    return "".join(vow.pop() if c in "aeiouAEIOU" else c for c in s)


@O
def reverse_vowels(s):
    a = list(s)
    l, r = 0, len(a) - 1
    while l < r:
        while l < r and a[l] not in "aeiouAEIOU":
            l += 1
        while l < r and a[r] not in "aeiouAEIOU":
            r -= 1
        a[l], a[r] = a[r], a[l]
        T(f"Swap vowels at {l} and {r}", A("a", a, hl=[l, r], l=l, r=r), at="prev")
        l, r = l + 1, r - 1
    return "".join(a)
