from lib import *

LESSON("Basics", "Nodes and pointers", """
<p>An array keeps items in neighbouring boxes. A <b>linked list</b> keeps each item in its own <b>node</b>, anywhere in memory, and each node stores a <b>pointer</b> (reference) to the next node.</p>
<div class="pic">head → [3 | •] → [7 | •] → [1 | •] → None
        val  next</div>
<pre><code class="py">class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next</code></pre>
<p>You only hold the <code>head</code>. To reach the k-th node you must walk k steps — there is no <code>list[k]</code>. In return, once you hold a node, inserting or removing next to it is O(1): just change arrows, nothing shifts.</p>
<pre><code class="py">cur = head
while cur:              # the standard walk
    print(cur.val)
    cur = cur.next</code></pre>
""", practice=[83])


@LD
def build_and_walk():
    vals = [3, 7, 1, 9]
    head = None
    for v in reversed(vals):
        head = ListNode(v, head)
        T(f"Create node {v} pointing to the old head", L("list", head, head=head), at="prev")
    cur, total = head, 0
    while cur:
        total += cur.val
        T(f"Walk: visit {cur.val}, running total {total}", L("list", head, cur=cur), V(total=total))
        cur = cur.next
    return total


LESSON("Basics", "Insert, delete and the dummy head", """
<p>To <b>insert</b> node <code>x</code> after node <code>p</code>: <code>x.next = p.next; p.next = x</code> (order matters — save the rest first).</p>
<p>To <b>delete</b> the node after <code>p</code>: <code>p.next = p.next.next</code>.</p>
<p>Both need the node <i>before</i> the target. But the head has no node before it, which forces special cases. The fix is a <b>dummy</b> node placed in front:</p>
<pre><code class="py">dummy = ListNode(0, head)
prev = dummy
while prev.next:
    if prev.next.val == target:
        prev.next = prev.next.next   # works even if head is deleted
    else:
        prev = prev.next
return dummy.next                    # the real (maybe new) head</code></pre>
<div class="tip">Whenever the head might change — merge, delete, partition, swap — start with a dummy.</div>
""", practice=[19, 86, 24])


@LD
def dummy_delete():
    head = mk_list([6, 2, 6, 3, 6])
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next:
        if prev.next.val == 6:
            T(f"prev.next is 6 → skip it (prev.next = prev.next.next)", L("list (with dummy 0)", dummy, hl=[prev.next], prev=prev))
            prev.next = prev.next.next
        else:
            prev = prev.next
            T("Keep this node, step forward", L("list (with dummy 0)", dummy, prev=prev), at="prev")
    return dummy.next


LESSON("Core", "Reversing a list", """
<p>Reversal is the most common linked-list operation. Walk the list and point each node <b>backwards</b>. You need three names:</p>
<ul>
<li><code>prev</code> — the already-reversed part (starts as <code>None</code>),</li>
<li><code>cur</code> — the node being flipped,</li>
<li><code>nxt</code> — saved before flipping, or the rest of the list is lost.</li>
</ul>
<pre><code class="py">prev, cur = None, head
while cur:
    nxt = cur.next
    cur.next = prev
    prev, cur = cur, nxt
return prev</code></pre>
<p>Reversing a <b>part</b> of the list (positions left..right, or groups of k) is the same loop plus reconnecting the reversed piece to what comes before and after it.</p>
""", practice=[206, 92, 25])


LESSON("Core", "Fast and slow pointers", """
<p>Move <code>slow</code> one step and <code>fast</code> two steps at a time.</p>
<ul>
<li><b>Middle</b>: when fast reaches the end, slow is in the middle.</li>
<li><b>Cycle</b>: if the list loops, fast eventually laps slow and they meet. If fast reaches <code>None</code>, there's no cycle. O(1) memory, unlike a visited set.</li>
<li><b>Cycle start</b>: after they meet, put one pointer back at head and move both one step at a time — they meet at the cycle's entrance (follows from the distances walked).</li>
<li><b>n-th from the end</b>: give one pointer an n-step head start, then move both; when the leader hits the end, the follower is n from the end.</li>
</ul>
<div class="warn">Always check <code>while fast and fast.next</code> before <code>fast.next.next</code>.</div>
""", practice=[876, 141, 142, 19])


@LD
def cycle_lesson():
    head = mk_list([1, 2, 3, 4, 5, 6], 2)
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        T("slow moves 1, fast moves 2", L("list (6 points back to 3)", head, slow=slow, fast=fast), at="prev")
        if slow is fast:
            T("They met → the list has a cycle", L("list (6 points back to 3)", head, hl=[slow], slow=slow, fast=fast))
            return True
    return False


LESSON("Core", "Merging and splitting", """
<ul>
<li><b>Merge two sorted lists</b>: a dummy and a <code>tail</code>; attach the smaller head each step, then attach whatever remains.</li>
<li><b>Partition</b>: build two separate chains (less / rest) with two dummies, then join them. Cut the last tail's <code>next</code> to avoid a cycle.</li>
<li><b>Merge k lists</b>: a min-heap of the current heads, O(N log k).</li>
<li><b>Sort a list</b>: merge sort — split at the middle with fast/slow, sort both halves, merge. O(n log n) with no random access needed.</li>
</ul>
""", practice=[21, 86, 23, 148, 328, 2])


LESSON("Advanced", "Combining techniques", """
<p>Harder problems chain the basic moves:</p>
<ul>
<li><b>Reorder list</b> (L0 → Ln → L1 → Ln−1 …) = find middle + reverse second half + weave the halves.</li>
<li><b>Palindrome list</b> = find middle + reverse second half + compare.</li>
<li><b>Rotate by k</b> = find length and tail, link tail to head (ring), cut at the right place.</li>
<li><b>Intersection of two lists</b> = pointer a walks A then B, pointer b walks B then A; both travel the same distance and meet at the junction.</li>
</ul>
<h4>LRU cache — the classic design question</h4>
<p>You need O(1) lookup <i>and</i> O(1) "move to most recent" <i>and</i> O(1) "remove least recent". A dict gives the lookup; a <b>doubly linked list</b> (each node has <code>prev</code> and <code>next</code>) gives O(1) removal from anywhere. The dict maps key → node; the list is ordered by recency, with sentinel head and tail nodes so there are no edge cases.</p>
""", practice=[143, 234, 61, 160, 146])
