from lib import *

LESSON("Basics", "The stack: last in, first out", """
<p>A <b>stack</b> is like a pile of plates: you only add to the top and take from the top. The last plate put on is the first one taken off — <b>LIFO</b>.</p>
<table>
<tr><th>Action</th><th>Python list</th><th>Cost</th></tr>
<tr><td>push x</td><td><code>st.append(x)</code></td><td>O(1)</td></tr>
<tr><td>pop the top</td><td><code>st.pop()</code></td><td>O(1)</td></tr>
<tr><td>look at the top</td><td><code>st[-1]</code></td><td>O(1)</td></tr>
<tr><td>is it empty?</td><td><code>not st</code></td><td>O(1)</td></tr>
</table>
<p>You already use one every day: the <b>call stack</b>. When a function calls another, Python pushes a frame; when it returns, the frame is popped. That's why recursion and stacks are interchangeable.</p>
""", practice=[1047])


@LD
def stack_lesson():
    st = []
    for op, x in [("push", 3), ("push", 8), ("push", 5), ("pop", None), ("push", 1), ("pop", None), ("pop", None)]:
        if op == "push":
            st.append(x)
            T(f"push({x}) — goes on top", S("stack", st, hl=[len(st) - 1]), at="prev")
        else:
            y = st.pop()
            T(f"pop() → {y}, the most recent item", S("stack", st), at="prev")
    return st


LESSON("Basics", "The queue: first in, first out", """
<p>A <b>queue</b> is a line at a ticket counter: join at the back, leave from the front — <b>FIFO</b>. Use <code>collections.deque</code>:</p>
<pre><code class="py">from collections import deque
q = deque()
q.append(x)      # join at the back   O(1)
q.popleft()      # leave the front    O(1)
q[0]             # peek the front     O(1)</code></pre>
<div class="warn">Don't use <code>list.pop(0)</code> as a queue — it shifts every element, O(n) per pop.</div>
<p>Queues are the heart of <b>BFS</b> (graphs and trees), task scheduling and anything processed "in arrival order".</p>
""", practice=[232, 225])


@LD
def queue_lesson():
    from collections import deque
    q = deque()
    for op, x in [("in", "A"), ("in", "B"), ("in", "C"), ("out", None), ("in", "D"), ("out", None)]:
        if op == "in":
            q.append(x)
            T(f"append('{x}') — joins at the back", A("queue (front → back)", list(q), hl=[len(q) - 1]), at="prev")
        else:
            y = q.popleft()
            T(f"popleft() → '{y}', who arrived first", A("queue (front → back)", list(q)), at="prev")
    return list(q)


LESSON("Core", "Matching and nesting", """
<p>Whenever things <b>open and close</b> — brackets, tags, folders, nested encodings — the most recently opened thing must close first. That's exactly LIFO.</p>
<pre><code class="py">pair = {')': '(', ']': '[', '}': '{'}
st = []
for ch in s:
    if ch in pair:                       # a closer
        if not st or st.pop() != pair[ch]:
            return False
    else:
        st.append(ch)                    # an opener
return not st                            # nothing left open</code></pre>
<p>Variations: <b>decode string</b> pushes (text so far, repeat count) at every <code>[</code>; <b>simplify path</b> pushes folder names and pops on <code>..</code>; <b>remove adjacent duplicates</b> uses the stack as the answer itself.</p>
""", practice=[20, 394, 71, 735, 32])


LESSON("Core", "Evaluating expressions", """
<p>Computers evaluate expressions with stacks.</p>
<ul>
<li><b>Reverse Polish notation</b> (<code>2 1 + 3 *</code>): numbers are pushed; an operator pops two numbers, applies itself, and pushes the result.</li>
<li><b>Infix with + − * /</b> (no brackets): * and / bind tighter, so do them immediately with the stack top; push +x or −x and sum the stack at the end.</li>
<li>With brackets, push the current result and sign at <code>(</code>, restore at <code>)</code>.</li>
</ul>
<div class="warn">Python's <code>//</code> rounds toward −∞. Problems usually want rounding toward 0: use <code>int(a / b)</code>.</div>
""", practice=[150, 227])


LESSON("Core", "Monotonic stack: next greater element", """
<p>"For each element, find the next element to the right that is greater" is O(n²) with two loops. A <b>monotonic stack</b> does it in O(n).</p>
<p>Keep a stack of indices whose values are <b>decreasing</b>. These are elements still waiting for a bigger value. When a new value arrives:</p>
<ol>
<li>While it is bigger than the value on top, pop the top — the new value is its answer.</li>
<li>Push the new index; it now waits too.</li>
</ol>
<p>Each index is pushed and popped once → O(n). Flip the comparison for "next smaller"; scan from the right for "previous greater"; loop twice for circular arrays.</p>
""", practice=[739, 496, 503, 901])


LESSON("Advanced", "Monotonic stack for ranges and contributions", """
<p>A monotonic stack can tell you, for every element, how far it extends left and right before hitting something smaller. That solves "range" problems:</p>
<ul>
<li><b>Largest rectangle in histogram</b>: when a bar is popped, the bar that popped it is its right limit and the new stack top is its left limit → width known, area known.</li>
<li><b>Sum of subarray minimums</b>: <code>arr[i]</code> is the minimum of <code>left[i] × right[i]</code> subarrays, so add <code>arr[i] × left[i] × right[i]</code>. Use <code>&lt;</code> on one side and <code>&lt;=</code> on the other so equal values aren't counted twice.</li>
<li><b>Remove K digits</b>: pop bigger digits while removals remain — a greedy that keeps the stack increasing.</li>
<li><b>Maximal rectangle</b>: run the histogram solution on every row.</li>
</ul>
""", practice=[84, 907, 402, 85, 853])


@LD
def histogram_lesson():
    heights = [2, 1, 5, 6, 2, 3]
    stack, best = [], 0
    for i in range(len(heights) + 1):
        h = heights[i] if i < len(heights) else 0
        while stack and heights[stack[-1]] >= h:
            top = stack.pop()
            left = stack[-1] + 1 if stack else 0
            best = max(best, heights[top] * (i - left))
            T(f"Pop bar {heights[top]}: it stretches from {left} to {i - 1} → area {heights[top] * (i - left)}", A("heights", heights, hl=range(left, i), ok=[top]), S("stack (indices)", stack), V(best=best), at="prev")
        stack.append(i)
    return best


LESSON("Advanced", "Designing with stacks and queues", """
<p>Design questions ask you to build a structure with given costs. Two tricks cover most of them:</p>
<ul>
<li><b>Store extra info with each item.</b> Min Stack pushes <code>(value, min so far)</code>; Stock Span pushes <code>(price, span)</code>.</li>
<li><b>Amortised analysis.</b> A queue from two stacks pours <code>in</code> into <code>out</code> only when <code>out</code> is empty. A single pop can cost O(n), but each element is moved at most once in its lifetime, so the <b>average</b> cost per operation is O(1).</li>
</ul>
<p>In an interview, state the cost of every method and say "amortised" when it applies.</p>
""", practice=[155, 232, 225, 901])
