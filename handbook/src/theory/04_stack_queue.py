from lib import *

THEORY("Definition", """
<p>A <b>stack</b> is a linear <b>abstract data type (ADT)</b> that follows the <b>LIFO</b> principle — Last In, First Out. Elements are added (<b>push</b>) and removed (<b>pop</b>) only at one end, called the <b>top</b>.</p>
<p>A <b>queue</b> is a linear ADT that follows the <b>FIFO</b> principle — First In, First Out. Elements are added at the <b>rear</b> (<b>enqueue</b>) and removed from the <b>front</b> (<b>dequeue</b>).</p>
<p>An ADT describes <i>what</i> operations exist, not <i>how</i> they are stored. Both can be implemented with an array or a linked list.</p>
""")

THEORY("Stack operations", """
<table>
<tr><th>Operation</th><th>Meaning</th><th>Python (<code>list</code>)</th><th>Time</th></tr>
<tr><td>push(x)</td><td>add x on top</td><td><code>st.append(x)</code></td><td>O(1) amortised</td></tr>
<tr><td>pop()</td><td>remove and return the top</td><td><code>st.pop()</code></td><td>O(1)</td></tr>
<tr><td>peek() / top()</td><td>read the top</td><td><code>st[-1]</code></td><td>O(1)</td></tr>
<tr><td>isEmpty()</td><td>no elements?</td><td><code>not st</code></td><td>O(1)</td></tr>
<tr><td>size()</td><td>number of elements</td><td><code>len(st)</code></td><td>O(1)</td></tr>
</table>
<p><b>Stack overflow</b>: pushing onto a full fixed-size stack (or recursion too deep). <b>Stack underflow</b>: popping from an empty stack.</p>
""")

THEORY("Queue operations and types", """
<table>
<tr><th>Operation</th><th>Python (<code>collections.deque</code>)</th><th>Time</th></tr>
<tr><td>enqueue(x)</td><td><code>q.append(x)</code></td><td>O(1)</td></tr>
<tr><td>dequeue()</td><td><code>q.popleft()</code></td><td>O(1)</td></tr>
<tr><td>front()</td><td><code>q[0]</code></td><td>O(1)</td></tr>
<tr><td>rear()</td><td><code>q[-1]</code></td><td>O(1)</td></tr>
</table>
<h4>Types of queue</h4>
<table>
<tr><th>Type</th><th>Description</th></tr>
<tr><td><b>Simple queue</b></td><td>insert at rear, delete at front</td></tr>
<tr><td><b>Circular queue</b></td><td>a fixed array where the rear wraps around to index 0, reusing freed slots: <code>rear = (rear + 1) % capacity</code></td></tr>
<tr><td><b>Deque</b> (double-ended)</td><td>insert and delete at both ends in O(1)</td></tr>
<tr><td><b>Priority queue</b></td><td>removes the highest-priority element first (implemented with a heap — see the Heap topic)</td></tr>
<tr><td><b>Monotonic queue / stack</b></td><td>kept in sorted order by popping elements that break it; used for window max and next-greater problems</td></tr>
</table>
""")

THEORY("Implementations", """
<table>
<tr><th>Implementation</th><th>Stack</th><th>Queue</th></tr>
<tr><td>Dynamic array</td><td>push/pop at the end: O(1)</td><td>dequeue at index 0 shifts everything: O(n) — use a circular buffer instead</td></tr>
<tr><td>Circular array</td><td>—</td><td>front and rear indices wrap with <code>% capacity</code>: O(1), fixed size</td></tr>
<tr><td>Linked list</td><td>push/pop at the head: O(1)</td><td>enqueue at tail, dequeue at head: O(1)</td></tr>
<tr><td>Two stacks</td><td>—</td><td>amortised O(1) (pour 'in' into 'out' when 'out' is empty)</td></tr>
</table>
<p>In Python use <code>list</code> for stacks and <code>collections.deque</code> for queues. <code>queue.Queue</code> is for thread-safe producer/consumer code and is slower.</p>
""")

THEORY("Advantages and disadvantages", """
<div class="two">
<div class="pro"><h5>Advantages</h5><ul><li>All core operations O(1)</li><li>Natural model for nesting (stack) and fairness/order (queue)</li><li>Simple to implement and reason about</li></ul></div>
<div class="con"><h5>Disadvantages</h5><ul><li>No random access or search (O(n))</li><li>Fixed-size array versions can overflow</li><li>Only the ends are accessible</li></ul></div>
</div>
""")

THEORY("Applications", """
<div class="two">
<div><h5>Stack</h5><ul><li>Function call stack and recursion</li><li>Undo / redo in editors, browser back button</li><li>Balanced parentheses, HTML/XML tag matching</li><li>Expression evaluation and infix → postfix conversion</li><li>Depth-first search, backtracking</li><li>Monotonic stack: stock span, histogram area</li></ul></div>
<div><h5>Queue</h5><ul><li>CPU and printer scheduling, task queues</li><li>Breadth-first search</li><li>Buffers: keyboard input, IO, streaming</li><li>Message queues between services (Kafka, RabbitMQ)</li><li>Handling requests in arrival order (web servers, call centres)</li></ul></div>
</div>
""")

THEORY("Expression notations", """
<table>
<tr><th>Notation</th><th>Example for (2 + 3) × 4</th><th>Note</th></tr>
<tr><td>Infix</td><td><code>(2 + 3) * 4</code></td><td>operator between operands; needs brackets and precedence</td></tr>
<tr><td>Prefix (Polish)</td><td><code>* + 2 3 4</code></td><td>operator first; no brackets needed</td></tr>
<tr><td>Postfix (Reverse Polish)</td><td><code>2 3 + 4 *</code></td><td>operator last; evaluated left to right with one stack</td></tr>
</table>
<p>The <b>shunting-yard algorithm</b> converts infix to postfix with an operator stack, respecting precedence and brackets.</p>
""")

FAQ("Stack vs queue — what's the difference?", "<p>A stack removes the most recently added element (LIFO); a queue removes the oldest (FIFO). Stack: one open end. Queue: insert at one end, remove at the other.</p>")
FAQ("Why not use a Python list as a queue?", "<p><code>list.pop(0)</code> shifts every remaining element: O(n). <code>collections.deque.popleft()</code> is O(1) because deque is a doubly-linked block structure.</p>")
FAQ("What is a circular queue and why use it?", "<p>A fixed-size array queue where indices wrap around with modulo. It reuses slots freed at the front, so a simple array queue doesn't run out of space while elements are still free at the start.</p>")
FAQ("How do you implement a queue using two stacks? What's the complexity?", "<p>Push to stack <code>in</code>. For pop/peek, if <code>out</code> is empty, move all of <code>in</code> into <code>out</code> (reversing the order), then pop from <code>out</code>. Each element is moved at most once, so operations are amortised O(1).</p>")
FAQ("What is a monotonic stack?", "<p>A stack kept in increasing or decreasing order by popping elements that would break the order before pushing. Each pop answers a 'next greater/smaller' question for the popped element. O(n) total.</p>")
FAQ("How is recursion related to the stack?", "<p>Each function call pushes a frame (arguments, local variables, return address) onto the call stack; returning pops it. Any recursive algorithm can be rewritten with an explicit stack, which also avoids recursion-depth limits.</p>")
