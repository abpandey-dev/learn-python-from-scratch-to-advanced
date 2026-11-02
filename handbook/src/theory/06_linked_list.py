from lib import *

THEORY("Definition", """
<p>A <b>linked list</b> is a linear data structure in which elements, called <b>nodes</b>, are not stored contiguously. Each node contains <b>data</b> and a <b>reference (pointer)</b> to the next node. The first node is the <b>head</b>; the last node points to <code>None</code> (null).</p>
<div class="pic">head → [10 | •] → [20 | •] → [30 | None]</div>
<p>The list is accessed only through the head, and elements are reached by following pointers one by one (<b>sequential access</b>).</p>
""")

THEORY("Types of linked lists", """
<table>
<tr><th>Type</th><th>Each node has</th><th>Picture</th><th>Use</th></tr>
<tr><td><b>Singly linked</b></td><td>data, next</td><td><code>A → B → C → None</code></td><td>stacks, simple lists, most interview problems</td></tr>
<tr><td><b>Doubly linked</b></td><td>data, prev, next</td><td><code>None ⇄ A ⇄ B ⇄ C ⇄ None</code></td><td>LRU cache, browser history, deque</td></tr>
<tr><td><b>Circular singly</b></td><td>data, next; last → head</td><td><code>A → B → C → A</code></td><td>round-robin scheduling, circular buffers</td></tr>
<tr><td><b>Circular doubly</b></td><td>prev, next; ends connected</td><td>ring both ways</td><td>Fibonacci heaps, music playlists on repeat</td></tr>
</table>
<p>A <b>sentinel</b> (dummy) node is an extra node that never holds real data, placed at the head (and/or tail) to remove special cases for empty lists and head changes.</p>
""")

THEORY("Operations and their complexity", """
<table>
<tr><th>Operation</th><th>Singly</th><th>Doubly</th><th>How</th></tr>
<tr><td>Access k-th element</td><td>O(k)</td><td>O(k)</td><td>walk from head</td></tr>
<tr><td>Search for a value</td><td>O(n)</td><td>O(n)</td><td>walk and compare</td></tr>
<tr><td>Insert at head</td><td>O(1)</td><td>O(1)</td><td><code>new.next = head; head = new</code></td></tr>
<tr><td>Insert at tail</td><td>O(n), O(1) with tail pointer</td><td>O(1) with tail</td><td>link from the tail</td></tr>
<tr><td>Insert after a given node</td><td>O(1)</td><td>O(1)</td><td><code>x.next = p.next; p.next = x</code></td></tr>
<tr><td>Delete head</td><td>O(1)</td><td>O(1)</td><td><code>head = head.next</code></td></tr>
<tr><td>Delete a given node</td><td>O(n) (need the previous node)</td><td><b>O(1)</b></td><td>doubly: <code>node.prev.next = node.next</code></td></tr>
<tr><td>Reverse</td><td>O(n)</td><td>O(n)</td><td>flip pointers in one pass</td></tr>
</table>
<p>Space: O(n) for the nodes, plus one pointer per node (two for doubly linked).</p>
""")

THEORY("Linked list vs array", """
<table>
<tr><th></th><th>Array</th><th>Linked list</th></tr>
<tr><td>Memory layout</td><td>contiguous</td><td>scattered nodes</td></tr>
<tr><td>Access by index</td><td>O(1)</td><td>O(n)</td></tr>
<tr><td>Insert/delete at front</td><td>O(n)</td><td>O(1)</td></tr>
<tr><td>Insert/delete in middle (node known)</td><td>O(n)</td><td>O(1)</td></tr>
<tr><td>Size</td><td>fixed or amortised resize</td><td>grows one node at a time</td></tr>
<tr><td>Extra memory</td><td>spare capacity</td><td>pointer(s) per element</td></tr>
<tr><td>Cache performance</td><td>excellent</td><td>poor (pointer chasing)</td></tr>
<tr><td>Binary search</td><td>yes</td><td>not efficiently</td></tr>
</table>
""")

THEORY("Advantages, disadvantages and applications", """
<div class="two">
<div class="pro"><h5>Advantages</h5><ul><li>Dynamic size, no reallocation</li><li>O(1) insert/delete at the head or next to a known node</li><li>No large contiguous block of memory needed</li><li>Easy to splice, split and merge lists</li></ul></div>
<div class="con"><h5>Disadvantages</h5><ul><li>No random access; O(n) to reach an element</li><li>Extra memory for pointers</li><li>Poor cache locality → slower traversal than arrays</li><li>Pointer bugs: lost nodes, accidental cycles</li></ul></div>
</div>
<h4>Applications</h4>
<ul>
<li>Implementing stacks, queues and deques.</li>
<li>Hash table chaining (each bucket is a list).</li>
<li>LRU caches (hash map + doubly linked list).</li>
<li>Adjacency lists for graphs.</li>
<li>Undo history, music playlists, image viewers (next/previous).</li>
<li>Memory allocators' free lists; polynomial arithmetic.</li>
</ul>
""")

THEORY("Key techniques (summary)", """
<table>
<tr><th>Technique</th><th>Solves</th></tr>
<tr><td>Dummy head</td><td>any problem where the head may change</td></tr>
<tr><td>Fast &amp; slow pointers</td><td>middle node, cycle detection, cycle start, palindrome check</td></tr>
<tr><td>Gap pointers</td><td>n-th node from the end in one pass</td></tr>
<tr><td>In-place reversal</td><td>reverse list / sub-list / k-groups</td></tr>
<tr><td>Split + merge</td><td>merge sort on lists, reorder list</td></tr>
<tr><td>Hash map of nodes</td><td>copying lists with random pointers, intersection (O(n) space)</td></tr>
</table>
""")

FAQ("Array vs linked list — when would you choose a linked list?", "<p>When you insert/delete at the front or in the middle often and rarely need access by index, or when the size changes unpredictably. For most other cases arrays win because of O(1) indexing and cache locality.</p>")
FAQ("How do you detect a cycle in a linked list?", "<p>Floyd's tortoise and hare: slow moves 1 step, fast moves 2. If they ever meet, there is a cycle; if fast reaches None, there isn't. O(n) time, O(1) space. (A visited set also works with O(n) space.)</p>")
FAQ("How do you find where a cycle starts?", "<p>After slow and fast meet, move one pointer back to head and advance both one step at a time. They meet at the cycle's entrance. Reason: the distance from head to the entrance equals the distance from the meeting point to the entrance (mod the cycle length).</p>")
FAQ("Why is deleting a node O(1) in a doubly linked list but O(n) in a singly linked list?", "<p>Deletion needs the previous node to reconnect pointers. A doubly linked node stores <code>prev</code> directly; a singly linked list must walk from the head to find it.</p>")
FAQ("What is a dummy (sentinel) node?", "<p>A placeholder node before the real head. It guarantees every real node has a predecessor, so inserting or deleting at the head needs no special case. Return <code>dummy.next</code> at the end.</p>")
FAQ("How would you reverse a linked list? Iterative vs recursive?", "<p>Iterative: keep prev, cur, nxt and flip <code>cur.next = prev</code> while walking — O(n) time, O(1) space. Recursive: reverse the rest, then set <code>head.next.next = head</code>, <code>head.next = None</code> — O(n) time, O(n) stack space.</p>")
FAQ("Why does an LRU cache use a doubly linked list?", "<p>It needs to move a recently used item to the front and remove the least recently used item from the back, both in O(1). A doubly linked list allows O(1) removal of any node given a reference (from the hash map), which a singly linked list or array can't.</p>")
