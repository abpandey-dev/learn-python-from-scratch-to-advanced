from lib import *

TOPIC(
    id="stack-queue", title="Stack & Queue", glyph="LIFO",
    blurb="Last-in-first-out for matching and 'next greater' questions; first-in-first-out for order.",
    demo_title="Monotonic stack: next greater element for every index",
    theory="""
<h3>What it is</h3>
<p>A <b>stack</b> only lets you touch the top: <code>push</code> and <code>pop</code> in O(1), last in → first out. In Python a plain <code>list</code> is a stack (<code>append</code> / <code>pop</code>). A <b>queue</b> is first in → first out; use <code>collections.deque</code> (<code>append</code> / <code>popleft</code>), never <code>list.pop(0)</code>, which is O(n).</p>
<h3>Where stacks show up</h3>
<table>
<tr><th>Signal</th><th>Technique</th></tr>
<tr><td>Brackets, nested structure, "undo"</td><td>push openers, pop on closers</td></tr>
<tr><td>Expression evaluation (RPN, calculator)</td><td>operand stack, apply operators on pop</td></tr>
<tr><td>"Next / previous greater or smaller"</td><td><b>monotonic stack</b></td></tr>
<tr><td>Largest rectangle, sum of subarray minimums</td><td>monotonic stack gives each bar's left and right limit</td></tr>
<tr><td>Remove characters to make something smallest</td><td>greedy pop while the top is worse</td></tr>
</table>
<h3>Monotonic stack, in one sentence</h3>
<p>Keep the stack sorted (say decreasing). When a new value is bigger than the top, the top has just found its <b>next greater element</b> — pop it and record the answer. Each index is pushed once and popped once, so the whole pass is O(n).</p>
<pre><code class="py">res = [-1] * len(a)
stack = []                      # indices, values decreasing
for i, x in enumerate(a):
    while stack and a[stack[-1]] &lt; x:
        res[stack.pop()] = x    # x is the next greater for that index
    stack.append(i)</code></pre>
<h3>Common mistakes</h3>
<ul>
<li>Popping from an empty stack — always check <code>if stack</code> first.</li>
<li>Storing values when you need indices (widths, distances need indices).</li>
<li>Strict vs non-strict comparison with duplicates: in "sum of subarray minimums" one side must use <code>&lt;</code> and the other <code>&lt;=</code> to avoid double-counting.</li>
</ul>
""")


@D
def next_greater_demo():
    a = [2, 1, 2, 4, 3]
    res = [-1] * len(a)
    stack = []
    for i, x in enumerate(a):
        while stack and a[stack[-1]] < x:
            j = stack.pop()
            res[j] = x
            T(f"{x} > {a[j]} → next greater of index {j} is {x}", A("a", a, hl=[i], ok=[j], i=i), S("stack (indices)", stack), A("res", res, ok=[j]), at="prev")
        stack.append(i)
        T(f"Push index {i}", A("a", a, hl=[i], i=i), S("stack (indices)", stack, hl=[len(stack) - 1]), A("res", res), at="prev")
    return res


# 1 ---------------------------------------------------------------
Q(20, "Valid Parentheses", "Easy", "Matching stack",
  "Given a string of <code>()[]{}</code>, return <code>True</code> if every bracket is closed by the same type in the right order.",
  [(("()[]{}",), True), (("(]",), False), (("([])",), True), (("([)]",), False)],
  ("Repeatedly delete adjacent pairs (), [] and {} until nothing changes; valid if the string becomes empty.", "O(n²)", "O(n)"),
  ("Push every opener. On a closer, the top of the stack must be its matching opener; pop it. Valid if the stack ends empty.", "O(n)", "O(n)"),
  viz=("{[()]}(]",))


@B
def is_valid(s):
    prev = None
    while prev != s:
        prev = s
        s = s.replace("()", "").replace("[]", "").replace("{}", "")
    return s == ""


@O
def is_valid(s):
    pair = {")": "(", "]": "[", "}": "{"}
    stack = []
    for i, ch in enumerate(s):
        if ch in pair:
            T(f"'{ch}' must match the top '{stack[-1] if stack else '∅'}'", A("s", s, hl=[i], i=i), S("stack", stack, hl=[len(stack) - 1]))
            if not stack or stack.pop() != pair[ch]:
                return False
        else:
            stack.append(ch)
            T(f"Push opener '{ch}'", A("s", s, hl=[i], i=i), S("stack", stack), at="prev")
    return not stack


# 2 ---------------------------------------------------------------
Q(155, "Min Stack", "Medium", "Stack of (value, min)",
  "Design a stack with <code>push</code>, <code>pop</code>, <code>top</code> and <code>getMin</code>, all in O(1).",
  [(((), [("push", (-2,)), ("push", (0,)), ("push", (-3,)), ("getMin", ()), ("pop", ()), ("top", ()), ("getMin", ())]), [None, None, None, -3, None, 0, -2])],
  ("Plain list; getMin scans the whole stack.", "getMin O(n)", "O(n)"),
  ("Store each value with the minimum of the stack at that moment. The min is always at the top, and popping restores the previous min automatically.", "O(1) every op", "O(n)"),
  design=True, viz=((), [("push", (5,)), ("push", (3,)), ("push", (7,)), ("push", (2,)), ("getMin", ()), ("pop", ()), ("getMin", ())]))


@B
class MinStack:
    def __init__(self):
        self.st = []

    def push(self, val):
        self.st.append(val)

    def pop(self):
        self.st.pop()

    def top(self):
        return self.st[-1]

    def getMin(self):
        return min(self.st)


@O
class MinStack:
    def __init__(self):
        self.st = []  # (value, min so far)

    def push(self, val):
        low = min(val, self.st[-1][1]) if self.st else val
        self.st.append((val, low))
        T(f"push({val}) → store ({val}, min {low})", S("stack (value, min)", [f"{v}, {m}" for v, m in self.st], hl=[len(self.st) - 1]), at="prev")

    def pop(self):
        self.st.pop()
        T("pop() — the previous min is back on top", S("stack (value, min)", [f"{v}, {m}" for v, m in self.st]), at="prev")

    def top(self):
        return self.st[-1][0]

    def getMin(self):
        T(f"getMin() = {self.st[-1][1]} straight from the top", S("stack (value, min)", [f"{v}, {m}" for v, m in self.st], hl=[len(self.st) - 1]))
        return self.st[-1][1]


# 3 ---------------------------------------------------------------
Q(150, "Evaluate Reverse Polish Notation", "Medium", "Operand stack",
  "Evaluate an expression in Reverse Polish Notation (operators come after operands). Division truncates toward zero.",
  [((["2", "1", "+", "3", "*"],), 9), ((["4", "13", "5", "/", "+"],), 6), ((["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"],), 22)],
  ("Repeatedly find the first operator, apply it to the two tokens before it, and splice the result back into the list.", "O(n²)", "O(n)"),
  ("Push numbers. On an operator, pop b then a, push a op b. The last value is the answer.", "O(n)", "O(n)"))


@B
def eval_rpn(tokens):
    tokens = list(tokens)
    while len(tokens) > 1:
        for i, t in enumerate(tokens):
            if t in "+-*/" and len(t) == 1:
                a, b = int(tokens[i - 2]), int(tokens[i - 1])
                v = a + b if t == "+" else a - b if t == "-" else a * b if t == "*" else int(a / b)
                tokens[i - 2:i + 1] = [str(v)]
                break
    return int(tokens[0])


@O
def eval_rpn(tokens):
    stack = []
    for i, t in enumerate(tokens):
        if t in ("+", "-", "*", "/"):
            b, a = stack.pop(), stack.pop()
            if t == "+":
                stack.append(a + b)
            elif t == "-":
                stack.append(a - b)
            elif t == "*":
                stack.append(a * b)
            else:
                stack.append(int(a / b))
            T(f"'{t}': pop {b} and {a}, push {a} {t} {b} = {stack[-1]}", A("tokens", tokens, hl=[i], i=i), S("stack", stack, hl=[len(stack) - 1]), at="prev")
        else:
            stack.append(int(t))
            T(f"Number {t} → push", A("tokens", tokens, hl=[i], i=i), S("stack", stack), at="prev")
    return stack[0]


# 4 ---------------------------------------------------------------
Q(739, "Daily Temperatures", "Medium", "Monotonic stack",
  "For each day, return how many days until a warmer temperature (0 if never).",
  [(([73, 74, 75, 71, 69, 72, 76, 73],), [1, 1, 4, 2, 1, 1, 0, 0]), (([30, 40, 50, 60],), [1, 1, 1, 0]), (([30, 60, 90],), [1, 1, 0])],
  ("For each day, scan forward until a warmer day.", "O(n²)", "O(1) extra"),
  ("Stack of indices with decreasing temperatures. A warmer day pops every colder index and sets its wait to i − index.", "O(n)", "O(n)"),
  viz=([73, 74, 75, 71, 69, 72, 76],))


@B
def daily_temperatures(temps):
    res = [0] * len(temps)
    for i in range(len(temps)):
        for j in range(i + 1, len(temps)):
            if temps[j] > temps[i]:
                res[i] = j - i
                break
    return res


@O
def daily_temperatures(temps):
    res = [0] * len(temps)
    stack = []  # indices, temperatures decreasing
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            res[j] = i - j
            T(f"{t} is warmer than day {j} ({temps[j]}) → wait {i - j}", A("temps", temps, hl=[i], ok=[j], i=i), S("stack", stack), A("res", res, ok=[j]), at="prev")
        stack.append(i)
    return res


# 5 ---------------------------------------------------------------
Q(496, "Next Greater Element I", "Easy", "Monotonic stack + map",
  "<code>nums1</code> is a subset of <code>nums2</code>. For each x in nums1, return the first greater number to the right of x in nums2, or −1.",
  [(([4, 1, 2], [1, 3, 4, 2]), [-1, 3, -1]), (([2, 4], [1, 2, 3, 4]), [3, -1])],
  ("For each x, find it in nums2 and scan right.", "O(n · m)", "O(1)"),
  ("One monotonic-stack pass over nums2 records next greater for every value in a dict; then look each x up.", "O(n + m)", "O(m)"))


@B
def next_greater_element(nums1, nums2):
    res = []
    for x in nums1:
        j = nums2.index(x)
        res.append(next((y for y in nums2[j + 1:] if y > x), -1))
    return res


@O
def next_greater_element(nums1, nums2):
    nxt, stack = {}, []
    for i, x in enumerate(nums2):
        while stack and stack[-1] < x:
            nxt[stack.pop()] = x
        stack.append(x)
        T(f"After {x}: known next-greater values", A("nums2", nums2, hl=[i], i=i), S("stack", stack), M("next", nxt), at="prev")
    return [nxt.get(x, -1) for x in nums1]


# 6 ---------------------------------------------------------------
Q(503, "Next Greater Element II", "Medium", "Monotonic stack · circular",
  "<code>nums</code> is circular. For every element return the next greater number going around, or −1.",
  [(([1, 2, 1],), [2, -1, 2]), (([1, 2, 3, 4, 3],), [2, 3, 4, -1, 4])],
  ("For each i, check the next n − 1 elements with wrap-around.", "O(n²)", "O(1) extra"),
  ("Run the monotonic stack over 2n steps using index i % n, so elements near the end can see the beginning.", "O(n)", "O(n)"))


@B
def next_greater_elements(nums):
    n, res = len(nums), []
    for i in range(n):
        res.append(next((nums[(i + d) % n] for d in range(1, n) if nums[(i + d) % n] > nums[i]), -1))
    return res


@O
def next_greater_elements(nums):
    n = len(nums)
    res, stack = [-1] * n, []
    for k in range(2 * n):
        i = k % n
        while stack and nums[stack[-1]] < nums[i]:
            res[stack.pop()] = nums[i]
        if k < n:
            stack.append(i)
        T(f"Step {k} (index {i}{', second lap' if k >= n else ''})", A("nums", nums, hl=[i], i=i), S("stack", stack), A("res", res), at="prev")
    return res


# 7 ---------------------------------------------------------------
Q(84, "Largest Rectangle in Histogram", "Hard", "Monotonic stack · widths",
  "Given bar heights of width 1, return the area of the largest rectangle in the histogram.",
  [(([2, 1, 5, 6, 2, 3],), 10), (([2, 4],), 4)],
  ("For each bar, expand left and right while bars are at least as tall.", "O(n²)", "O(1)"),
  ("Keep indices with increasing heights. When a shorter bar arrives, each popped bar's rectangle ends here and starts just after the new stack top — compute its area then.", "O(n)", "O(n)"))


@B
def largest_rectangle_area(heights):
    best = 0
    for i, h in enumerate(heights):
        l = r = i
        while l > 0 and heights[l - 1] >= h:
            l -= 1
        while r < len(heights) - 1 and heights[r + 1] >= h:
            r += 1
        best = max(best, h * (r - l + 1))
    return best


@O
def largest_rectangle_area(heights):
    stack, best = [], 0  # indices, heights increasing
    for i in range(len(heights) + 1):
        h = heights[i] if i < len(heights) else 0
        while stack and heights[stack[-1]] >= h:
            top = stack.pop()
            left = stack[-1] + 1 if stack else 0
            area = heights[top] * (i - left)
            best = max(best, area)
            T(f"Bar {heights[top]} spans {left}..{i - 1}: area {area}", A("heights", heights, hl=range(left, i), ok=[top], i=i if i < len(heights) else None), S("stack", stack), V(best=best), at="prev")
        stack.append(i)
    return best


# 8 ---------------------------------------------------------------
Q(853, "Car Fleet", "Medium", "Sort + stack of arrival times",
  "Cars drive toward <code>target</code>; a faster car that catches a slower one joins its fleet. Return the number of fleets that arrive.",
  [((12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]), 3), ((10, [3], [3]), 1), ((100, [0, 2, 4], [4, 2, 1]), 1)],
  ("Simulate time step by step, merging cars that meet.", "O(n · T)", "O(n)"),
  ("Sort by position, closest to target first. A car's arrival time ≤ the fleet ahead's time means it merges; otherwise it starts a new fleet.", "O(n log n)", "O(n)"))


@B
def car_fleet(target, position, speed):
    cars = sorted(zip(position, speed), reverse=True)
    fleets = 0
    times = [(target - p) / s for p, s in cars]
    for i in range(len(times)):
        if all(times[i] > times[j] for j in range(i)):
            fleets += 1
    return fleets


@O
def car_fleet(target, position, speed):
    cars = sorted(zip(position, speed), reverse=True)
    stack = []
    for p, s in cars:
        t = (target - p) / s
        if not stack or t > stack[-1]:
            stack.append(t)
        T(f"Car at {p} arrives at t = {t:.2f}; {'new fleet' if stack[-1] == t else 'catches the fleet ahead'}", S("fleet arrival times", [f"{x:.2f}" for x in stack]), V(position=p, speed=s), at="prev")
    return len(stack)


# 9 ---------------------------------------------------------------
Q(735, "Asteroid Collision", "Medium", "Stack simulation",
  "Positive asteroids move right, negative move left. When two meet, the smaller explodes (both if equal). Return the survivors.",
  [(([5, 10, -5],), [5, 10]), (([8, -8],), []), (([10, 2, -5],), [10]), (([-2, -1, 1, 2],), [-2, -1, 1, 2])],
  ("Repeatedly scan for a right-mover directly followed by a left-mover and resolve that collision.", "O(n²)", "O(n)"),
  ("Stack of survivors. A left-mover fights the right-movers on top of the stack until it dies or no right-mover remains.", "O(n)", "O(n)"),
  viz=([5, 10, -5, -12, 3],))


@B
def asteroid_collision(asteroids):
    a = list(asteroids)
    changed = True
    while changed:
        changed = False
        for i in range(len(a) - 1):
            if a[i] > 0 > a[i + 1]:
                if abs(a[i]) == abs(a[i + 1]):
                    del a[i:i + 2]
                elif abs(a[i]) > abs(a[i + 1]):
                    del a[i + 1]
                else:
                    del a[i]
                changed = True
                break
    return a


@O
def asteroid_collision(asteroids):
    stack = []
    for i, x in enumerate(asteroids):
        alive = True
        while alive and x < 0 and stack and stack[-1] > 0:
            T(f"{x} meets {stack[-1]}", A("asteroids", asteroids, hl=[i], i=i), S("stack", stack, hl=[len(stack) - 1]))
            if stack[-1] < -x:
                stack.pop()
            elif stack[-1] == -x:
                stack.pop()
                alive = False
            else:
                alive = False
        if alive:
            stack.append(x)
        T(f"After asteroid {x}", A("asteroids", asteroids, hl=[i], i=i), S("stack", stack), at="prev")
    return stack


# 10 --------------------------------------------------------------
Q(394, "Decode String", "Medium", "Stack of (string, count)",
  "Decode strings like <code>3[a2[c]]</code> → <code>accaccacc</code>: <code>k[s]</code> means s repeated k times.",
  [(("3[a]2[bc]",), "aaabcbc"), (("3[a2[c]]",), "accaccacc"), (("2[abc]3[cd]ef",), "abcabccdcdcdef")],
  ("Repeatedly find an innermost k[...] with a regex and expand it.", "O(n · output)", "O(output)"),
  ("Scan once. On '[' push (current string, k) and start fresh; on ']' pop and set cur = prev + cur × k.", "O(output)", "O(n)"),
  viz=("2[a3[b]]c",))


@B
def decode_string(s):
    import re
    pat = re.compile(r"(\d+)\[([a-z]*)\]")
    while "[" in s:
        s = pat.sub(lambda m: m.group(2) * int(m.group(1)), s)
    return s


@O
def decode_string(s):
    stack, cur, k = [], "", 0
    for i, ch in enumerate(s):
        if ch.isdigit():
            k = k * 10 + int(ch)
        elif ch == "[":
            stack.append((cur, k))
            cur, k = "", 0
            T("'[' → save (string so far, repeat count) and start fresh", A("s", s, hl=[i], i=i), S("stack", [f"'{a}', {b}" for a, b in stack]), V(cur=cur), at="prev")
        elif ch == "]":
            prev, times = stack.pop()
            cur = prev + cur * times
            T(f"']' → cur = prev + cur × {times}", A("s", s, hl=[i], i=i), S("stack", [f"'{a}', {b}" for a, b in stack]), V(cur=cur), at="prev")
        else:
            cur += ch
    return cur


# 11 --------------------------------------------------------------
Q(71, "Simplify Path", "Medium", "Stack of directories",
  "Convert a Unix absolute path to its canonical form (resolve <code>.</code>, <code>..</code> and repeated slashes).",
  [(("/home/",), "/home"), (("/home//foo/",), "/home/foo"), (("/a/./b/../../c/",), "/c"), (("/../",), "/")],
  ("Repeatedly apply string rewrites (remove '/./', collapse '//', remove 'dir/..') until stable.", "O(n²)", "O(n)"),
  ("Split on '/'. Push names, pop on '..', ignore '' and '.'. Join the stack.", "O(n)", "O(n)"),
  viz=("/a/./b/../../c/d/",))


@B
def simplify_path(path):
    import re
    p = path + "/"
    prev = None
    while prev != p:
        prev = p
        p = re.sub(r"/+", "/", p)
        p = p.replace("/./", "/")
        p = re.sub(r"/(?!\.\./)[^/]+/\.\./", "/", p, count=1)
        p = re.sub(r"^/\.\./", "/", p)
    return p.rstrip("/") or "/"


@O
def simplify_path(path):
    stack = []
    parts = path.split("/")
    for i, part in enumerate(parts):
        if part == "..":
            if stack:
                stack.pop()
        elif part and part != ".":
            stack.append(part)
        T(f"Part '{part}'", A("parts", parts, hl=[i], i=i), S("stack", stack), at="prev")
    return "/" + "/".join(stack)


# 12 --------------------------------------------------------------
Q(402, "Remove K Digits", "Medium", "Monotonic stack · greedy",
  "Remove <code>k</code> digits from the number string <code>num</code> to make it as small as possible.",
  [(("1432219", 3), "1219"), (("10200", 1), "200"), (("10", 2), "0")],
  ("Try every way to remove k digits and keep the smallest.", "O(C(n, k) · n)", "O(n)"),
  ("A smaller digit should come as early as possible: while the stack top is bigger than the next digit and removals remain, pop it. Trim leftovers from the end and strip leading zeros.", "O(n)", "O(n)"))


@B
def remove_kdigits(num, k):
    from itertools import combinations
    best = None
    for keep in combinations(range(len(num)), len(num) - k):
        s = "".join(num[i] for i in keep).lstrip("0") or "0"
        if best is None or (len(s), s) < (len(best), best):
            best = s
    return best or "0"


@O
def remove_kdigits(num, k):
    stack = []
    for i, d in enumerate(num):
        while k and stack and stack[-1] > d:
            stack.pop()
            k -= 1
        stack.append(d)
        T(f"Digit {d}: pop bigger digits on top while removals remain", A("num", num, hl=[i], i=i), S("stack", stack), V(k_left=k), at="prev")
    stack = stack[:len(stack) - k] if k else stack
    return "".join(stack).lstrip("0") or "0"


# 13 --------------------------------------------------------------
Q(901, "Online Stock Span", "Medium", "Monotonic stack · design",
  "For each new daily price, return the span: how many consecutive days (ending today) had price ≤ today's.",
  [(((), [("next", (100,)), ("next", (80,)), ("next", (60,)), ("next", (70,)), ("next", (60,)), ("next", (75,)), ("next", (85,))]), [1, 1, 1, 2, 1, 4, 6])],
  ("Store all prices; for each new price walk backwards while prices are ≤.", "O(n) per call", "O(n)"),
  ("Keep a stack of (price, span) with decreasing prices. A new price absorbs every smaller-or-equal entry, adding their spans.", "O(1) amortised", "O(n)"),
  design=True)


@B
class StockSpanner:
    def __init__(self):
        self.prices = []

    def next(self, price):
        self.prices.append(price)
        span = 0
        for p in reversed(self.prices):
            if p > price:
                break
            span += 1
        return span


@O
class StockSpanner:
    def __init__(self):
        self.stack = []  # (price, span)

    def next(self, price):
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]
        self.stack.append((price, span))
        T(f"next({price}) → span {span}", S("stack (price, span)", [f"{p}, {s}" for p, s in self.stack], hl=[len(self.stack) - 1]), at="prev")
        return span


# 14 --------------------------------------------------------------
Q(907, "Sum of Subarray Minimums", "Medium", "Monotonic stack · contribution",
  "Return the sum of min(sub) over every contiguous subarray, modulo 10⁹ + 7.",
  [(([3, 1, 2, 4],), 17), (([11, 81, 94, 43, 3],), 444)],
  ("Enumerate every subarray, tracking the running minimum.", "O(n²)", "O(1)"),
  ("Each arr[i] is the minimum of left[i] × right[i] subarrays, where left/right are distances to the previous smaller and next smaller-or-equal element. Find both with monotonic stacks.", "O(n)", "O(n)"))


@B
def sum_subarray_mins(arr):
    total = 0
    for i in range(len(arr)):
        low = arr[i]
        for j in range(i, len(arr)):
            low = min(low, arr[j])
            total += low
    return total % (10 ** 9 + 7)


@O
def sum_subarray_mins(arr):
    n = len(arr)
    left, right, stack = [0] * n, [0] * n, []
    for i in range(n):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        left[i] = i - stack[-1] if stack else i + 1
        stack.append(i)
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        right[i] = stack[-1] - i if stack else n - i
        stack.append(i)
    total = 0
    for i in range(n):
        total += arr[i] * left[i] * right[i]
        T(f"{arr[i]} is the min of {left[i]} × {right[i]} = {left[i] * right[i]} subarrays", A("arr", arr, hl=range(i - left[i] + 1, i + right[i]), ok=[i], i=i), A("left", left, hl=[i]), A("right", right, hl=[i]), V(total=total), at="prev")
    return total % (10 ** 9 + 7)


# 15 --------------------------------------------------------------
Q(232, "Implement Queue using Stacks", "Easy", "Two stacks · amortised",
  "Build a FIFO queue (<code>push</code>, <code>pop</code>, <code>peek</code>, <code>empty</code>) using only stack operations.",
  [(((), [("push", (1,)), ("push", (2,)), ("peek", ()), ("pop", ()), ("empty", ())]), [None, None, 1, 1, False])],
  ("One stack; to pop the oldest, move everything to a temp stack and back.", "pop O(n)", "O(n)"),
  ("Push onto 'in'. To pop or peek, if 'out' is empty pour all of 'in' into it — that reverses the order. Each element moves at most once.", "O(1) amortised", "O(n)"),
  design=True, viz=((), [("push", (1,)), ("push", (2,)), ("push", (3,)), ("pop", ()), ("push", (4,)), ("pop", ()), ("peek", ())]))


@B
class MyQueue:
    def __init__(self):
        self.st = []

    def push(self, x):
        self.st.append(x)

    def pop(self):
        tmp = []
        while self.st:
            tmp.append(self.st.pop())
        x = tmp.pop()
        while tmp:
            self.st.append(tmp.pop())
        return x

    def peek(self):
        return self.st[0]

    def empty(self):
        return not self.st


@O
class MyQueue:
    def __init__(self):
        self.inp, self.out = [], []

    def push(self, x):
        self.inp.append(x)
        T(f"push({x}) onto 'in'", S("in", self.inp), S("out", self.out), at="prev")

    def _move(self):
        if not self.out:
            while self.inp:
                self.out.append(self.inp.pop())
            T("'out' was empty → pour 'in' into it (order reverses)", S("in", self.inp), S("out", self.out), at="prev")

    def pop(self):
        self._move()
        x = self.out.pop()
        T(f"pop() → {x} from the top of 'out'", S("in", self.inp), S("out", self.out), at="prev")
        return x

    def peek(self):
        self._move()
        return self.out[-1]

    def empty(self):
        return not self.inp and not self.out


# 16 --------------------------------------------------------------
Q(225, "Implement Stack using Queues", "Easy", "One queue · rotate",
  "Build a LIFO stack (<code>push</code>, <code>pop</code>, <code>top</code>, <code>empty</code>) using only queue operations.",
  [(((), [("push", (1,)), ("push", (2,)), ("top", ()), ("pop", ()), ("empty", ())]), [None, None, 2, 2, False])],
  ("Two queues; on pop, move all but the last element to the other queue.", "pop O(n)", "O(n)"),
  ("One queue. After appending x, rotate the queue len − 1 times so x comes to the front. Then pop and top are O(1).", "push O(n), pop O(1)", "O(n)"),
  design=True, viz=((), [("push", (1,)), ("push", (2,)), ("push", (3,)), ("pop", ()), ("top", ())]))


@B
class MyStack:
    def __init__(self):
        from collections import deque
        self.q = deque()

    def push(self, x):
        self.q.append(x)

    def pop(self):
        from collections import deque
        other = deque()
        while len(self.q) > 1:
            other.append(self.q.popleft())
        x = self.q.popleft()
        self.q = other
        return x

    def top(self):
        return self.q[-1]

    def empty(self):
        return not self.q


@O
class MyStack:
    def __init__(self):
        from collections import deque
        self.q = deque()

    def push(self, x):
        self.q.append(x)
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())
        T(f"push({x}) then rotate so {x} is at the front", A("queue (front → back)", list(self.q), hl=[0]), at="prev")

    def pop(self):
        x = self.q.popleft()
        T(f"pop() → {x} from the front", A("queue (front → back)", list(self.q)), at="prev")
        return x

    def top(self):
        return self.q[0]

    def empty(self):
        return not self.q


# 17 --------------------------------------------------------------
Q(227, "Basic Calculator II", "Medium", "Stack with deferred + and −",
  "Evaluate a string with non-negative integers, <code>+ - * /</code> and spaces. Division truncates toward zero.",
  [(("3+2*2",), 7), ((" 3/2 ",), 1), ((" 3+5 / 2 ",), 5)],
  ("Tokenise, then repeatedly resolve the first * or / pair in the list, then the + and − left to right.", "O(n²)", "O(n)"),
  ("Read number by number. Push it for +, push −it for −, and for * or / combine immediately with the stack top. The answer is the stack's sum.", "O(n)", "O(n)"),
  viz=("14-3*2+8/4",))


@B
def calculate(s):
    import re
    toks = re.findall(r"\d+|[+\-*/]", s)
    i = 1
    while i < len(toks):
        if toks[i] in "*/":
            a, b = int(toks[i - 1]), int(toks[i + 1])
            toks[i - 1:i + 2] = [str(a * b if toks[i] == "*" else int(a / b))]
        else:
            i += 2
    total = int(toks[0])
    for i in range(1, len(toks), 2):
        total += int(toks[i + 1]) if toks[i] == "+" else -int(toks[i + 1])
    return total


@O
def calculate(s):
    stack, num, op = [], 0, "+"
    for i, ch in enumerate(s + "+"):
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch in "+-*/":
            if op == "+":
                stack.append(num)
            elif op == "-":
                stack.append(-num)
            elif op == "*":
                stack.append(stack.pop() * num)
            else:
                stack.append(int(stack.pop() / num))
            T(f"Apply pending '{op}' to {num}", A("s", s, hl=[i] if i < len(s) else [], i=i), S("stack", stack, hl=[len(stack) - 1]), at="prev")
            op, num = ch, 0
    return sum(stack)


# 18 --------------------------------------------------------------
Q(1047, "Remove All Adjacent Duplicates In String", "Easy", "Stack as the result",
  "Repeatedly remove two adjacent equal letters until none remain; return the result.",
  [(("abbaca",), "ca"), (("azxxzy",), "ay")],
  ("Scan for an adjacent equal pair, delete it, and restart.", "O(n²)", "O(n)"),
  ("The stack holds the answer so far. If the next letter equals the top, pop (they cancel); otherwise push.", "O(n)", "O(n)"))


@B
def remove_duplicates_str(s):
    changed = True
    while changed:
        changed = False
        for i in range(len(s) - 1):
            if s[i] == s[i + 1]:
                s = s[:i] + s[i + 2:]
                changed = True
                break
    return s


@O
def remove_duplicates_str(s):
    stack = []
    for i, ch in enumerate(s):
        if stack and stack[-1] == ch:
            stack.pop()
            T(f"'{ch}' equals the top → both cancel", A("s", s, hl=[i], i=i), S("stack", stack), at="prev")
        else:
            stack.append(ch)
            T(f"Push '{ch}'", A("s", s, hl=[i], i=i), S("stack", stack), at="prev")
    return "".join(stack)


# 19 --------------------------------------------------------------
Q(85, "Maximal Rectangle", "Hard", "Histogram per row",
  "Given a binary matrix of '0' and '1', return the area of the largest rectangle containing only 1s.",
  [(([["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"], ["1", "1", "1", "1", "1"], ["1", "0", "0", "1", "0"]],), 6), (([["0"]],), 0), (([["1"]],), 1)],
  ("Try every top-left and bottom-right corner and check the rectangle is all 1s.", "O((mn)³)", "O(1)"),
  ("Treat each row as the base of a histogram: heights[c] = consecutive 1s ending at this row. Run Largest Rectangle in Histogram on every row.", "O(m · n)", "O(n)"))


@B
def maximal_rectangle(matrix):
    m, n, best = len(matrix), len(matrix[0]), 0
    for r1 in range(m):
        for c1 in range(n):
            for r2 in range(r1, m):
                for c2 in range(c1, n):
                    if all(matrix[r][c] == "1" for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)):
                        best = max(best, (r2 - r1 + 1) * (c2 - c1 + 1))
    return best


@O
def maximal_rectangle(matrix):
    n = len(matrix[0])
    heights, best = [0] * n, 0
    for r, row in enumerate(matrix):
        for c in range(n):
            heights[c] = heights[c] + 1 if row[c] == "1" else 0
        stack = []
        for i in range(n + 1):
            h = heights[i] if i < n else 0
            while stack and heights[stack[-1]] >= h:
                top = stack.pop()
                left = stack[-1] + 1 if stack else 0
                best = max(best, heights[top] * (i - left))
            stack.append(i)
        T(f"Row {r} as the floor → histogram {heights}; best so far {best}", G("matrix", matrix, hl=[(r, c) for c in range(n)]), A("heights", heights), V(best=best), at="prev")
    return best


# 20 --------------------------------------------------------------
Q(32, "Longest Valid Parentheses", "Hard", "Stack of indices",
  "Return the length of the longest well-formed parentheses substring.",
  [(("(()",), 2), ((")()())",), 4), (("",), 0)],
  ("Check every even-length substring for validity.", "O(n³)", "O(1)"),
  ("Stack of indices, seeded with −1 as the base. '(' pushes its index. ')' pops; if the stack is empty, this index becomes the new base, otherwise i − stack top is a valid length.", "O(n)", "O(n)"),
  viz=("()(())(",))


@B
def longest_valid_parentheses(s):
    def ok(t):
        bal = 0
        for c in t:
            bal += 1 if c == "(" else -1
            if bal < 0:
                return False
        return bal == 0
    best = 0
    for i in range(len(s)):
        for j in range(i + 2, len(s) + 1, 2):
            if ok(s[i:j]):
                best = max(best, j - i)
    return best


@O
def longest_valid_parentheses(s):
    stack, best = [-1], 0
    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                best = max(best, i - stack[-1])
        T(f"'{ch}' at {i}: valid run ends here of length {i - stack[-1] if ch == ')' and stack[-1] != i else 0}", A("s", s, hl=[i], ok=range(stack[-1] + 1, i + 1) if ch == ")" and stack[-1] != i else [], i=i), S("stack", stack), V(best=best), at="prev")
    return best
