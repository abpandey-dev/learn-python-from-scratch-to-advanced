from lib import *

TOPIC(
    id="linked-list", title="Linked List", glyph="○→○→",
    blurb="Nodes joined by pointers — master dummy heads, fast/slow pointers and in-place reversal.",
    demo_title="Reversing a list in place with prev / cur / nxt",
    theory="""
<h3>What it is</h3>
<p>A <b>linked list</b> is a chain of nodes; each node holds a value and a pointer to the <code>next</code> node. There's no index: reaching the k-th node takes k steps. In exchange, inserting or removing a node you already hold is O(1) — you just re-point arrows.</p>
<pre><code class="py">class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next</code></pre>
<h3>Costs</h3>
<table>
<tr><th>Operation</th><th>Linked list</th><th>Array</th></tr>
<tr><td>Access k-th element</td><td>O(k)</td><td>O(1)</td></tr>
<tr><td>Insert / delete after a known node</td><td>O(1)</td><td>O(n)</td></tr>
<tr><td>Insert at head</td><td>O(1)</td><td>O(n)</td></tr>
</table>
<h3>The five techniques</h3>
<ul>
<li><b>Dummy head</b> — <code>dummy = ListNode(0, head)</code> removes special cases when the head itself might change (merge, delete, partition).</li>
<li><b>Fast &amp; slow pointers</b> — fast moves 2, slow moves 1. Finds the middle, detects cycles (they meet), and finds the cycle start.</li>
<li><b>Gap pointers</b> — move one pointer n steps ahead, then move both: the slow one stops n from the end.</li>
<li><b>In-place reversal</b> — <code>prev, cur = None, head</code>; repeatedly flip <code>cur.next</code> to <code>prev</code>.</li>
<li><b>Split &amp; merge</b> — find the middle, reverse or sort the halves, weave them together (reorder list, palindrome, merge sort).</li>
</ul>
<h3>Template: reverse</h3>
<pre><code class="py">prev, cur = None, head
while cur:
    nxt = cur.next     # 1. save the rest
    cur.next = prev    # 2. flip the arrow
    prev, cur = cur, nxt  # 3. step forward
return prev</code></pre>
<h3>Common mistakes</h3>
<ul>
<li>Losing the rest of the list by overwriting <code>cur.next</code> before saving it.</li>
<li>Checking <code>fast.next.next</code> without first checking <code>fast</code> and <code>fast.next</code>.</li>
<li>Forgetting to cut the tail (<code>tail.next = None</code>) after rearranging, creating an accidental cycle.</li>
</ul>
""")

L1 = lambda a: (mk_list(a[0]),)


@D
def reverse_demo():
    head = mk_list([1, 2, 3, 4])
    prev, cur = None, head
    T("Start: prev = None, cur = head", L("list", head, cur=cur), L("reversed so far", prev))
    while cur:
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
        T(f"Flip {prev.val}'s arrow back, step forward", L("rest", cur, cur=cur), L("reversed so far", prev, prev=prev), at="prev")
    return prev


# 1 ---------------------------------------------------------------
Q(206, "Reverse Linked List", "Easy", "In-place reversal",
  "Reverse a singly linked list and return the new head.",
  [(([1, 2, 3, 4, 5],), [5, 4, 3, 2, 1]), (([1, 2],), [2, 1]), (([],), [])],
  ("Copy the values into an array and build a new list from the back.", "O(n)", "O(n)"),
  ("Walk the list once with prev / cur and point each node back at prev.", "O(n)", "O(1)"),
  prep=L1, post=list_arr)


@B
def reverse_list(head):
    vals = []
    while head:
        vals.append(head.val)
        head = head.next
    dummy = cur = ListNode()
    for v in reversed(vals):
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


@O
def reverse_list(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
        T(f"Node {prev.val} now points back; move on", L("remaining", cur, cur=cur), L("reversed", prev, prev=prev), at="prev")
    return prev


# 2 ---------------------------------------------------------------
Q(21, "Merge Two Sorted Lists", "Easy", "Dummy head · splice",
  "Merge two sorted linked lists into one sorted list by splicing their nodes.",
  [(([1, 2, 4], [1, 3, 4]), [1, 1, 2, 3, 4, 4]), (([], []), []), (([], [0]), [0])],
  ("Collect all values, sort them, build a new list.", "O((m+n) log(m+n))", "O(m + n)"),
  ("A dummy node and a tail pointer. Attach the smaller head each step; when one list runs out, attach the rest of the other.", "O(m + n)", "O(1)"),
  prep=lambda a: (mk_list(a[0]), mk_list(a[1])), post=list_arr)


@B
def merge_two_lists(l1, l2):
    vals = []
    for node in (l1, l2):
        while node:
            vals.append(node.val)
            node = node.next
    dummy = cur = ListNode()
    for v in sorted(vals):
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


@O
def merge_two_lists(l1, l2):
    dummy = tail = ListNode()
    while l1 and l2:
        if l1.val <= l2.val:
            tail.next, l1 = l1, l1.next
        else:
            tail.next, l2 = l2, l2.next
        tail = tail.next
        T(f"Attach {tail.val}", L("merged", dummy.next, tail=tail), L("l1", l1, l1=l1), L("l2", l2, l2=l2), at="prev")
    tail.next = l1 or l2
    return dummy.next


# 3 ---------------------------------------------------------------
Q(141, "Linked List Cycle", "Easy", "Fast & slow",
  "Return <code>True</code> if the list has a cycle (some node's next points back to an earlier node).",
  [(([3, 2, 0, -4], 1), True), (([1, 2], 0), True), (([1], -1), False)],
  ("Store every visited node in a set; a repeat means a cycle.", "O(n)", "O(n)"),
  ("Floyd: slow moves 1, fast moves 2. If there's a cycle fast laps slow and they meet; otherwise fast hits None.", "O(n)", "O(1)"),
  prep=lambda a: (mk_list(a[0], a[1]),), names=("head", "pos"))


@B
def has_cycle(head):
    seen = set()
    while head:
        if head in seen:
            return True
        seen.add(head)
        head = head.next
    return False


@O
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        T("slow +1, fast +2", L("list", head, slow=slow, fast=fast), at="prev")
        if slow is fast:
            T("They met → cycle", L("list", head, hl=[slow], slow=slow, fast=fast))
            return True
    return False


# 4 ---------------------------------------------------------------
Q(142, "Linked List Cycle II", "Medium", "Floyd · find the entrance",
  "Return the node where the cycle begins, or <code>None</code>. (The answer shown is that node's value.)",
  [(([3, 2, 0, -4], 1), 2), (([1, 2], 0), 1), (([1], -1), None)],
  ("Walk with a set; the first node seen twice is the entrance.", "O(n)", "O(n)"),
  ("After slow and fast meet, restart one pointer at head and move both by 1. The distance math (a = k·c − b) makes them meet exactly at the cycle entrance.", "O(n)", "O(1)"),
  prep=lambda a: (mk_list(a[0], a[1]),), post=lambda n: n.val if n else None, names=("head", "pos"),
  viz=([1, 2, 3, 4, 5, 6], 2))


@B
def detect_cycle(head):
    seen = set()
    while head:
        if head in seen:
            return head
        seen.add(head)
        head = head.next
    return None


@O
def detect_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        T("Phase 1: slow +1, fast +2", L("list", head, slow=slow, fast=fast), at="prev")
        if slow is fast:
            break
    else:
        return None
    p = head
    while p is not slow:
        p, slow = p.next, slow.next
        T("Phase 2: from head and from the meeting point, both +1", L("list", head, p=p, slow=slow), at="prev")
    T(f"They meet at {p.val}: the cycle entrance", L("list", head, hl=[p], entrance=p))
    return p


# 5 ---------------------------------------------------------------
Q(876, "Middle of the Linked List", "Easy", "Fast & slow",
  "Return the middle node (the second middle if there are two). Shown as the list from that node.",
  [(([1, 2, 3, 4, 5],), [3, 4, 5]), (([1, 2, 3, 4, 5, 6],), [4, 5, 6])],
  ("Count the length, then walk length // 2 steps.", "O(n) — two passes", "O(1)"),
  ("When fast (2 steps) reaches the end, slow (1 step) is in the middle.", "O(n) — one pass", "O(1)"),
  prep=L1, post=list_arr)


@B
def middle_node(head):
    n, cur = 0, head
    while cur:
        n, cur = n + 1, cur.next
    for _ in range(n // 2):
        head = head.next
    return head


@O
def middle_node(head):
    slow = fast = head
    T("Both start at head", L("list", head, slow=slow, fast=fast))
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        T("slow +1, fast +2", L("list", head, slow=slow, fast=fast), at="prev")
    return slow


# 6 ---------------------------------------------------------------
Q(19, "Remove Nth Node From End of List", "Medium", "Gap pointers",
  "Remove the n-th node from the end and return the head.",
  [(([1, 2, 3, 4, 5], 2), [1, 2, 3, 5]), (([1], 1), []), (([1, 2], 1), [1])],
  ("Count the length L, then remove node L − n from the front.", "O(n) — two passes", "O(1)"),
  ("Move fast n steps ahead of slow (both start at a dummy). Move both until fast is at the last node; slow.next is the node to delete.", "O(n) — one pass", "O(1)"),
  prep=lambda a: (mk_list(a[0]), a[1]), post=list_arr)


@B
def remove_nth_from_end(head, n):
    length, cur = 0, head
    while cur:
        length, cur = length + 1, cur.next
    dummy = ListNode(0, head)
    cur = dummy
    for _ in range(length - n):
        cur = cur.next
    cur.next = cur.next.next
    return dummy.next


@O
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    slow = fast = dummy
    for _ in range(n):
        fast = fast.next
    T(f"fast is {n} node(s) ahead of slow", L("list (with dummy 0)", dummy, slow=slow, fast=fast))
    while fast.next:
        slow, fast = slow.next, fast.next
        T("Move both by one", L("list (with dummy 0)", dummy, slow=slow, fast=fast), at="prev")
    T(f"slow.next ({slow.next.val}) is n-th from the end → skip it", L("list (with dummy 0)", dummy, hl=[slow.next], slow=slow))
    slow.next = slow.next.next
    return dummy.next


# 7 ---------------------------------------------------------------
Q(143, "Reorder List", "Medium", "Middle + reverse + weave",
  "Reorder L0 → L1 → … → Ln into L0 → Ln → L1 → Ln−1 → … in place.",
  [(([1, 2, 3, 4],), [1, 4, 2, 3]), (([1, 2, 3, 4, 5],), [1, 5, 2, 4, 3])],
  ("Put the nodes in an array and relink them with two indices from both ends.", "O(n)", "O(n)"),
  ("Find the middle, reverse the second half, then alternately take a node from each half.", "O(n)", "O(1)"),
  prep=L1, post=list_arr, inplace=0)


@B
def reorder_list(head):
    nodes = []
    while head:
        nodes.append(head)
        head = head.next
    i, j = 0, len(nodes) - 1
    while i < j:
        nodes[i].next = nodes[j]
        i += 1
        if i == j:
            break
        nodes[j].next = nodes[i]
        j -= 1
    nodes[i].next = None


@O
def reorder_list(head):
    slow = fast = head
    while fast.next and fast.next.next:
        slow, fast = slow.next, fast.next.next
    second, slow.next = slow.next, None
    T("1) Split at the middle", L("first half", head), L("second half", second))
    prev = None
    while second:
        second.next, prev, second = prev, second, second.next
    second = prev
    T("2) Reverse the second half", L("first half", head), L("second half", second), at="prev")
    first = head
    while second:
        n1, n2 = first.next, second.next
        first.next, second.next = second, n1
        first, second = n1, n2
        T("3) Weave one node from each half", L("result", head, hl=[first] if first else []), L("left in second half", second), at="prev")


# 8 ---------------------------------------------------------------
Q(234, "Palindrome Linked List", "Easy", "Reverse the second half",
  "Return <code>True</code> if the list's values read the same forwards and backwards.",
  [(([1, 2, 2, 1],), True), (([1, 2],), False), (([1, 2, 3, 2, 1],), True)],
  ("Copy values to an array and compare it with its reverse.", "O(n)", "O(n)"),
  ("Find the middle, reverse the second half, compare the halves node by node.", "O(n)", "O(1)"),
  prep=L1,
  viz=([1, 2, 3, 3, 2, 1],))


@B
def is_palindrome_list(head):
    vals = []
    while head:
        vals.append(head.val)
        head = head.next
    return vals == vals[::-1]


@O
def is_palindrome_list(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    prev = None
    while slow:
        slow.next, prev, slow = prev, slow, slow.next
    a, b = head, prev
    while b:
        T(f"Compare {a.val} and {b.val}", L("front", head, a=a), L("reversed back half", prev, b=b))
        if a.val != b.val:
            return False
        a, b = a.next, b.next
    return True


# 9 ---------------------------------------------------------------
Q(160, "Intersection of Two Linked Lists", "Easy", "Switch heads",
  "Two lists may merge into a shared tail. Return the first shared node (shown by value), or <code>None</code>.",
  [(([4, 1], [5, 6, 1], [8, 4, 5]), 8), (([1, 9, 1], [3], [2, 4]), 2), (([2, 6, 4], [1, 5], []), None)],
  ("Put every node of A in a set, then walk B until a node is in the set.", "O(m + n)", "O(m)"),
  ("Pointer a walks A then B; pointer b walks B then A. Both travel m + n steps, so they line up at the intersection (or both reach None).", "O(m + n)", "O(1)"),
  prep=lambda a: _shared(*a), post=lambda n: n.val if n else None, names=("onlyA", "onlyB", "shared"))


def _shared(a, b, common):
    tail = mk_list(common)

    def build(vals):
        if not vals:
            return tail
        head = mk_list(vals)
        cur = head
        while cur.next:
            cur = cur.next
        cur.next = tail
        return head
    return build(a), build(b)


@B
def get_intersection_node(head_a, head_b):
    seen = set()
    while head_a:
        seen.add(head_a)
        head_a = head_a.next
    while head_b:
        if head_b in seen:
            return head_b
        head_b = head_b.next
    return None


@O
def get_intersection_node(head_a, head_b):
    a, b = head_a, head_b
    while a is not b:
        T(f"a at {a.val if a else 'None'}, b at {b.val if b else 'None'}", L("A", head_a, a=a), L("B", head_b, b=b))
        a = a.next if a else head_b
        b = b.next if b else head_a
    T(f"Same node: {a.val if a else 'None'}", L("A", head_a, hl=[a], a=a), L("B", head_b, hl=[b], b=b))
    return a


# 10 --------------------------------------------------------------
Q(2, "Add Two Numbers", "Medium", "Digit-by-digit with carry",
  "Two non-negative numbers are stored as lists of digits in reverse order. Return their sum as a list in the same format.",
  [(([2, 4, 3], [5, 6, 4]), [7, 0, 8]), (([0], [0]), [0]), (([9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9]), [8, 9, 9, 9, 0, 0, 0, 1])],
  ("Convert both lists to integers, add, convert back. (Overflows in languages with fixed-size ints.)", "O(m + n)", "O(m + n)"),
  ("Add digit by digit like on paper, carrying into the next node.", "O(max(m, n))", "O(1) extra"),
  prep=lambda a: (mk_list(a[0]), mk_list(a[1])), post=list_arr)


@B
def add_two_numbers(l1, l2):
    def to_int(node):
        n, place = 0, 1
        while node:
            n += node.val * place
            node, place = node.next, place * 10
        return n
    total = to_int(l1) + to_int(l2)
    dummy = cur = ListNode()
    for d in reversed(str(total)):
        cur.next = ListNode(int(d))
        cur = cur.next
    return dummy.next


@O
def add_two_numbers(l1, l2):
    dummy = tail = ListNode()
    carry = 0
    while l1 or l2 or carry:
        total = (l1.val if l1 else 0) + (l2.val if l2 else 0) + carry
        carry, digit = divmod(total, 10)
        tail.next = ListNode(digit)
        tail = tail.next
        T(f"{total} → write {digit}, carry {carry}", L("l1", l1, l1=l1), L("l2", l2, l2=l2), L("sum", dummy.next, tail=tail), at="prev")
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    return dummy.next


# 11 --------------------------------------------------------------
Q(146, "LRU Cache", "Medium", "Hash map + doubly linked list",
  "Design a cache of fixed <code>capacity</code> with O(1) <code>get</code> and <code>put</code>; when full, evict the least recently used key.",
  [(((2,), [("put", (1, 1)), ("put", (2, 2)), ("get", (1,)), ("put", (3, 3)), ("get", (2,)), ("put", (4, 4)), ("get", (1,)), ("get", (3,)), ("get", (4,))]), [None, None, 1, None, -1, None, -1, 3, 4])],
  ("Keep a list of (key, value) in recency order; every get/put searches and moves items.", "O(n) per op", "O(n)"),
  ("A dict maps key → node in a doubly linked list ordered by recency. get moves the node to the front; put inserts at the front and evicts the node before the tail sentinel.", "O(1) per op", "O(capacity)"),
  design=True)


@B
class LRUCache:
    def __init__(self, capacity):
        self.cap, self.items = capacity, []  # most recent last

    def get(self, key):
        for i, (k, v) in enumerate(self.items):
            if k == key:
                self.items.append(self.items.pop(i))
                return v
        return -1

    def put(self, key, value):
        for i, (k, _) in enumerate(self.items):
            if k == key:
                self.items.pop(i)
                break
        self.items.append((key, value))
        if len(self.items) > self.cap:
            self.items.pop(0)


@O
class LRUCache:
    class Node:
        def __init__(self, key=0, val=0):
            self.key, self.val, self.prev, self.next = key, val, None, None

    def __init__(self, capacity):
        self.cap, self.map = capacity, {}
        self.head, self.tail = self.Node(), self.Node()  # sentinels
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _add_front(self, node):
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _order(self):
        out, cur = [], self.head.next
        while cur is not self.tail:
            out.append(f"{cur.key}:{cur.val}")
            cur = cur.next
        return out

    def get(self, key):
        if key not in self.map:
            T(f"get({key}) → miss, -1", A("recency (most → least)", self._order()), M("map", {k: "node" for k in self.map}))
            return -1
        node = self.map[key]
        self._remove(node)
        self._add_front(node)
        T(f"get({key}) → {node.val}; move it to the front", A("recency (most → least)", self._order(), hl=[0]), M("map", {k: "node" for k in self.map}, hl=key), at="prev")
        return node.val

    def put(self, key, value):
        if key in self.map:
            self._remove(self.map[key])
        node = self.Node(key, value)
        self.map[key] = node
        self._add_front(node)
        if len(self.map) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]
            T(f"Over capacity → evict least recent key {lru.key}", A("recency (most → least)", self._order(), hl=[0]), M("map", {k: "node" for k in self.map}), at="prev")
        T(f"put({key}, {value}) at the front", A("recency (most → least)", self._order(), hl=[0]), M("map", {k: "node" for k in self.map}, hl=key), at="prev")


# 12 --------------------------------------------------------------
Q(23, "Merge k Sorted Lists", "Hard", "Min-heap of heads",
  "Merge <code>k</code> sorted linked lists into one sorted list.",
  [(([[1, 4, 5], [1, 3, 4], [2, 6]],), [1, 1, 2, 3, 4, 4, 5, 6]), (([],), []), (([[]],), [])],
  ("Merge the lists one by one into a growing result.", "O(k · N)", "O(1)"),
  ("Push every list's head into a min-heap. Pop the smallest node, append it, push its next. The heap never holds more than k nodes.", "O(N log k)", "O(k)"),
  prep=lambda a: ([mk_list(x) for x in a[0]],), post=list_arr)


@B
def merge_k_lists(lists):
    def merge(a, b):
        dummy = t = ListNode()
        while a and b:
            if a.val <= b.val:
                t.next, a = a, a.next
            else:
                t.next, b = b, b.next
            t = t.next
        t.next = a or b
        return dummy.next
    res = None
    for l in lists:
        res = merge(res, l)
    return res


@O
def merge_k_lists(lists):
    import heapq
    heap = [(node.val, i, node) for i, node in enumerate(lists) if node]
    heapq.heapify(heap)
    dummy = tail = ListNode()
    while heap:
        val, i, node = heapq.heappop(heap)
        tail.next = node
        tail = node
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
        T(f"Pop smallest head {val} (from list {i})", A("heap (values)", sorted(v for v, _, _ in heap)), L("merged", dummy.next, tail=tail), at="prev")
    return dummy.next


# 13 --------------------------------------------------------------
Q(25, "Reverse Nodes in k-Group", "Hard", "Reverse in chunks",
  "Reverse the nodes k at a time; a final group shorter than k stays as is.",
  [(([1, 2, 3, 4, 5], 2), [2, 1, 4, 3, 5]), (([1, 2, 3, 4, 5], 3), [3, 2, 1, 4, 5])],
  ("Copy values to an array, reverse each full chunk, rebuild.", "O(n)", "O(n)"),
  ("For each group: check k nodes exist, reverse them in place, and connect the previous group's tail to the new group head.", "O(n)", "O(1)"),
  prep=lambda a: (mk_list(a[0]), a[1]), post=list_arr, viz=([1, 2, 3, 4, 5, 6, 7], 3))


@B
def reverse_k_group(head, k):
    vals = []
    while head:
        vals.append(head.val)
        head = head.next
    for i in range(0, len(vals) - len(vals) % k, k):
        vals[i:i + k] = vals[i:i + k][::-1]
    return mk_list(vals)


@O
def reverse_k_group(head, k):
    dummy = ListNode(0, head)
    group_prev = dummy
    while True:
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if not kth:
                return dummy.next
        group_next = kth.next
        prev, cur = group_next, group_prev.next
        while cur is not group_next:
            cur.next, prev, cur = prev, cur, cur.next
        first = group_prev.next
        group_prev.next = kth
        group_prev = first
        T(f"Reversed a group of {k}; it now starts with {kth.val}", L("list", dummy.next, hl=[kth], group_end=first), at="prev")


# 14 --------------------------------------------------------------
Q(61, "Rotate List", "Medium", "Close the ring, cut",
  "Rotate the list to the right by <code>k</code> places.",
  [(([1, 2, 3, 4, 5], 2), [4, 5, 1, 2, 3]), (([0, 1, 2], 4), [2, 0, 1])],
  ("Move the last node to the front, k times.", "O(n · k)", "O(1)"),
  ("Find length n and the tail, link tail to head to make a ring, then cut after node n − k % n − 1.", "O(n)", "O(1)"),
  prep=lambda a: (mk_list(a[0]), a[1]), post=list_arr)


@B
def rotate_right(head, k):
    if not head or not head.next:
        return head
    for _ in range(k):
        prev, cur = None, head
        while cur.next:
            prev, cur = cur, cur.next
        prev.next, cur.next, head = None, head, cur
    return head


@O
def rotate_right(head, k):
    if not head:
        return head
    n, tail = 1, head
    while tail.next:
        n, tail = n + 1, tail.next
    k %= n
    if k == 0:
        return head
    tail.next = head
    T(f"Length {n}; link the tail to the head to make a ring", L("ring", head, tail=tail))
    new_tail = head
    for _ in range(n - k - 1):
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None
    T(f"Cut after {new_tail.val}; {new_head.val} is the new head", L("rotated", new_head, head=new_head, tail=new_tail), at="prev")
    return new_head


# 15 --------------------------------------------------------------
Q(83, "Remove Duplicates from Sorted List", "Easy", "Skip equal neighbours",
  "Delete duplicates from a sorted list so each value appears once.",
  [(([1, 1, 2],), [1, 2]), (([1, 1, 2, 3, 3],), [1, 2, 3])],
  ("Collect unique values and rebuild the list.", "O(n)", "O(n)"),
  ("While cur.next has the same value as cur, bypass it.", "O(n)", "O(1)"),
  prep=L1, post=list_arr,
  viz=([1, 1, 2, 3, 3, 3, 4],))


@B
def delete_duplicates(head):
    vals = []
    while head:
        if not vals or vals[-1] != head.val:
            vals.append(head.val)
        head = head.next
    return mk_list(vals)


@O
def delete_duplicates(head):
    cur = head
    while cur and cur.next:
        if cur.next.val == cur.val:
            T(f"Next node repeats {cur.val} → bypass it", L("list", head, hl=[cur.next], cur=cur))
            cur.next = cur.next.next
        else:
            cur = cur.next
    return head


# 16 --------------------------------------------------------------
Q(328, "Odd Even Linked List", "Medium", "Two chains",
  "Group the nodes at odd positions first, then the even positions, keeping relative order.",
  [(([1, 2, 3, 4, 5],), [1, 3, 5, 2, 4]), (([2, 1, 3, 5, 6, 4, 7],), [2, 3, 6, 7, 1, 5, 4])],
  ("Collect values by position parity and rebuild.", "O(n)", "O(n)"),
  ("Build the odd chain and even chain at the same time by skipping every other node, then attach the even chain after the odd tail.", "O(n)", "O(1)"),
  prep=L1, post=list_arr,
  viz=([1, 2, 3, 4, 5, 6, 7],))


@B
def odd_even_list(head):
    vals, i = [[], []], 0
    while head:
        vals[i % 2].append(head.val)
        head, i = head.next, i + 1
    return mk_list(vals[0] + vals[1])


@O
def odd_even_list(head):
    if not head:
        return head
    odd, even = head, head.next
    even_head = even
    while even and even.next:
        odd.next = even.next
        odd = odd.next
        even.next = odd.next
        even = even.next
        T("Extend both chains by one", L("odd chain", head, odd=odd), L("even chain", even_head, even=even), at="prev")
    odd.next = even_head
    return head


# 17 --------------------------------------------------------------
Q(148, "Sort List", "Medium", "Merge sort on a list",
  "Sort a linked list in O(n log n) time.",
  [(([4, 2, 1, 3],), [1, 2, 3, 4]), (([-1, 5, 3, 4, 0],), [-1, 0, 3, 4, 5]), (([],), [])],
  ("Copy values out, sort, write them back.", "O(n log n)", "O(n)"),
  ("Merge sort: split at the middle with fast/slow, sort each half recursively, merge the two sorted halves.", "O(n log n)", "O(log n) recursion"),
  prep=L1, post=list_arr, viz=([5, 2, 7, 1, 3],))


@B
def sort_list(head):
    vals = []
    cur = head
    while cur:
        vals.append(cur.val)
        cur = cur.next
    return mk_list(sorted(vals))


@O
def sort_list(head):
    if not head or not head.next:
        return head
    slow, fast = head, head.next
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    right, slow.next = slow.next, None
    T("Split into two halves", L("left", head), L("right", right))
    a, b = sort_list(head), sort_list(right)
    dummy = tail = ListNode()
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    T("Merge two sorted halves", L("merged", dummy.next), at="prev")
    return dummy.next


# 18 --------------------------------------------------------------
Q(24, "Swap Nodes in Pairs", "Medium", "Pointer rewiring",
  "Swap every two adjacent nodes (change the links, not the values).",
  [(([1, 2, 3, 4],), [2, 1, 4, 3]), (([],), []), (([1, 2, 3],), [2, 1, 3])],
  ("Swap values in place — not allowed by the problem — or rebuild from an array.", "O(n)", "O(n)"),
  ("With a dummy before the head, for each pair a → b: prev → b, b → a, a → rest. Then prev = a.", "O(n)", "O(1)"),
  prep=L1, post=list_arr,
  viz=([1, 2, 3, 4, 5, 6],))


@B
def swap_pairs(head):
    vals = []
    while head:
        vals.append(head.val)
        head = head.next
    for i in range(0, len(vals) - 1, 2):
        vals[i], vals[i + 1] = vals[i + 1], vals[i]
    return mk_list(vals)


@O
def swap_pairs(head):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next and prev.next.next:
        a, b = prev.next, prev.next.next
        prev.next, a.next, b.next = b, b.next, a
        prev = a
        T(f"Swapped {a.val} and {b.val}", L("list", dummy.next, hl=[a, b], prev=prev), at="prev")
    return dummy.next


# 19 --------------------------------------------------------------
Q(92, "Reverse Linked List II", "Medium", "Reverse a sub-range",
  "Reverse the nodes from position <code>left</code> to <code>right</code> (1-indexed) in one pass.",
  [(([1, 2, 3, 4, 5], 2, 4), [1, 4, 3, 2, 5]), (([5], 1, 1), [5])],
  ("Copy values, reverse the slice, rebuild.", "O(n)", "O(n)"),
  ("Walk to the node before 'left'. Then repeatedly take the node after the current sub-list tail and move it to the front of the sub-list (head insertion), right − left times.", "O(n)", "O(1)"),
  prep=lambda a: (mk_list(a[0]), a[1], a[2]), post=list_arr, viz=([1, 2, 3, 4, 5, 6], 2, 5))


@B
def reverse_between(head, left, right):
    vals = []
    while head:
        vals.append(head.val)
        head = head.next
    vals[left - 1:right] = vals[left - 1:right][::-1]
    return mk_list(vals)


@O
def reverse_between(head, left, right):
    dummy = ListNode(0, head)
    before = dummy
    for _ in range(left - 1):
        before = before.next
    cur = before.next
    for _ in range(right - left):
        move = cur.next
        cur.next = move.next
        move.next = before.next
        before.next = move
        T(f"Move {move.val} to the front of the sub-list", L("list", dummy.next, hl=[move], before=before if before is not dummy else None, cur=cur), at="prev")
    return dummy.next


# 20 --------------------------------------------------------------
Q(86, "Partition List", "Medium", "Two dummy lists",
  "Put all nodes with value &lt; <code>x</code> before nodes ≥ x, keeping the original order within each part.",
  [(([1, 4, 3, 2, 5, 2], 3), [1, 2, 2, 4, 3, 5]), (([2, 1], 2), [1, 2])],
  ("Collect the two groups of values and rebuild.", "O(n)", "O(n)"),
  ("Append each node to a 'less' list or a 'rest' list (each with a dummy head), then join less → rest and cut the tail.", "O(n)", "O(1)"),
  prep=lambda a: (mk_list(a[0]), a[1]), post=list_arr)


@B
def partition(head, x):
    lo, hi = [], []
    while head:
        (lo if head.val < x else hi).append(head.val)
        head = head.next
    return mk_list(lo + hi)


@O
def partition(head, x):
    less = lt = ListNode()
    rest = rt = ListNode()
    while head:
        if head.val < x:
            lt.next, lt = head, head
        else:
            rt.next, rt = head, head
        nxt = head.next
        head.next = None
        T(f"{lt.val if lt is head else rt.val} goes to {'less' if lt is head else 'rest'}", L("less", less.next), L("rest", rest.next), at="prev")
        head = nxt
    lt.next = rest.next
    return less.next
