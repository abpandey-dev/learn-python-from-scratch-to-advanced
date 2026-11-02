from lib import *

TOPIC(
    id="trees", title="Trees & BST", glyph="△",
    blurb="Recursion on left and right subtrees, BFS by level, and the ordering rule of binary search trees.",
    demo_title="DFS orders: the same tree visited preorder, inorder, postorder",
    theory="""
<h3>What it is</h3>
<p>A <b>binary tree</b> is a node with up to two children, <code>left</code> and <code>right</code>, each itself a binary tree. Almost every tree problem is solved by asking: <i>if I already knew the answer for my left and right subtrees, how would I combine them?</i></p>
<pre><code class="py">class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right</code></pre>
<p>A <b>binary search tree (BST)</b> adds a rule: everything in the left subtree is smaller than the node, everything in the right is larger. So an inorder walk gives sorted order, and search takes O(h) where h is the height (log n if balanced, n if it degenerates into a line).</p>
<h3>Traversals</h3>
<table>
<tr><th>Order</th><th>Visit</th><th>Used for</th></tr>
<tr><td>Preorder</td><td>node, left, right</td><td>copying / serialising a tree, path from root</td></tr>
<tr><td>Inorder</td><td>left, node, right</td><td>BST → sorted order, k-th smallest, validate BST</td></tr>
<tr><td>Postorder</td><td>left, right, node</td><td>heights, diameters, anything that needs children first</td></tr>
<tr><td>Level order (BFS)</td><td>row by row with a queue</td><td>levels, right side view, min depth, zigzag</td></tr>
</table>
<h3>Spot the pattern</h3>
<ul>
<li>"Height / depth / diameter / balanced / max path" → postorder DFS that <b>returns</b> one value and updates a global best.</li>
<li>"Per level" → BFS with <code>for _ in range(len(queue))</code>.</li>
<li>"Root-to-node path" or "carry info downward" (max so far, bounds) → pass it as a parameter.</li>
<li>BST + "find / k-th / validate / LCA" → use the ordering to go left or right only.</li>
</ul>
<h3>Template: postorder that returns height</h3>
<pre><code class="py">def height(node):
    if not node:
        return 0
    l, r = height(node.left), height(node.right)
    # combine here: update a global answer with l, r
    return 1 + max(l, r)</code></pre>
<h3>Common mistakes</h3>
<ul>
<li>Validating a BST only against the direct parent instead of the full (low, high) range.</li>
<li>Forgetting the <code>None</code> base case.</li>
<li>Deep recursion on skewed trees: Python's default limit is 1000 frames — use an explicit stack if n can be large.</li>
</ul>
""")

T1 = lambda a: (mk_tree(a[0]),)


@D
def traversal_demo():
    root = mk_tree([1, 2, 3, 4, 5, None, 6])
    pre, ino, post = [], [], []

    def dfs(node):
        if not node:
            return
        pre.append(node.val)
        dfs(node.left)
        ino.append(node.val)
        dfs(node.right)
        post.append(node.val)
        T(f"Leaving {node.val}: it is added to postorder last", TR("tree", root, hl=[node], ok=[v for v in post]), A("preorder", pre), A("inorder", ino), A("postorder", post, hl=[len(post) - 1]), at="prev")

    dfs(root)
    return pre, ino, post


# 1 ---------------------------------------------------------------
Q(94, "Binary Tree Inorder Traversal", "Easy", "Iterative stack",
  "Return the inorder traversal (left, node, right) of a binary tree.",
  [(([1, None, 2, 3],), [1, 3, 2]), (([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9],), [4, 2, 6, 5, 7, 1, 3, 9, 8]), (([],), [])],
  ("Recursive DFS: visit left, record the node, visit right.", "O(n)", "O(h) call stack"),
  ("Same order with an explicit stack: push the whole left spine, pop and record, then move to the right child. (Morris traversal reaches O(1) space.)", "O(n)", "O(h)"),
  prep=T1, viz=([4, 2, 6, 1, 3, 5],))


@B
def inorder_traversal(root):
    res = []

    def dfs(node):
        if node:
            dfs(node.left)
            res.append(node.val)
            dfs(node.right)
    dfs(root)
    return res


@O
def inorder_traversal(root):
    res, stack, cur = [], [], root
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        res.append(cur.val)
        T(f"Pop {cur.val} and record it, then go right", TR("tree", root, hl=[cur], ok=res), S("stack", [n.val for n in stack]), A("res", res), at="prev")
        cur = cur.right
    return res


# 2 ---------------------------------------------------------------
Q(104, "Maximum Depth of Binary Tree", "Easy", "Postorder height",
  "Return the number of nodes on the longest root-to-leaf path.",
  [(([3, 9, 20, None, None, 15, 7],), 3), (([1, None, 2],), 2), (([],), 0)],
  ("List every root-to-leaf path and take the longest.", "O(n · h)", "O(n · h)"),
  ("depth(node) = 1 + max(depth(left), depth(right)); an empty tree has depth 0.", "O(n)", "O(h)"),
  prep=T1)


@B
def max_depth(root):
    paths = []

    def walk(node, path):
        if not node:
            return
        path = path + [node.val]
        if not node.left and not node.right:
            paths.append(path)
        walk(node.left, path)
        walk(node.right, path)
    walk(root, [])
    return max((len(p) for p in paths), default=0)


@O
def max_depth(root):
    def depth(node):
        if not node:
            return 0
        d = 1 + max(depth(node.left), depth(node.right))
        T(f"depth({node.val}) = {d}", TR("tree", root, hl=[node]), at="prev")
        return d
    return depth(root)


# 3 ---------------------------------------------------------------
Q(226, "Invert Binary Tree", "Easy", "Swap children recursively",
  "Mirror a binary tree: swap every node's left and right children.",
  [(([4, 2, 7, 1, 3, 6, 9],), [4, 7, 2, 9, 6, 3, 1]), (([2, 1, 3],), [2, 3, 1]), (([],), [])],
  ("Build a brand-new mirrored copy of the tree.", "O(n)", "O(n) new nodes"),
  ("At every node swap left and right, then invert both subtrees in place.", "O(n)", "O(h)"),
  prep=T1, post=tree_arr)


@B
def invert_tree(root):
    if not root:
        return None
    return TreeNode(root.val, invert_tree(root.right), invert_tree(root.left))


@O
def invert_tree(root):
    top = root

    def inv(node):
        if not node:
            return
        node.left, node.right = node.right, node.left
        T(f"Swap the children of {node.val}", TR("tree", top, hl=[node]), at="prev")
        inv(node.left)
        inv(node.right)
    inv(root)
    return root


# 4 ---------------------------------------------------------------
Q(100, "Same Tree", "Easy", "Parallel recursion",
  "Return <code>True</code> if two binary trees have the same shape and values.",
  [(([1, 2, 3], [1, 2, 3]), True), (([1, 2], [1, None, 2]), False), (([1, 2, 1], [1, 1, 2]), False)],
  ("Serialise both trees with None markers and compare the strings.", "O(n)", "O(n)"),
  ("Recurse on both trees together: both empty → True; one empty or values differ → False; else compare left with left and right with right.", "O(n)", "O(h)"),
  prep=lambda a: (mk_tree(a[0]), mk_tree(a[1])), viz=([1, 2, 3, 4], [1, 2, 3, 5]))


@B
def is_same_tree(p, q):
    def ser(n):
        return "#" if not n else f"({n.val},{ser(n.left)},{ser(n.right)})"
    return ser(p) == ser(q)


@O
def is_same_tree(p, q):
    rp, rq = p, q

    def same(a, b):
        if not a and not b:
            return True
        if not a or not b or a.val != b.val:
            T(f"Mismatch: {a.val if a else 'None'} vs {b.val if b else 'None'}", TR("p", rp, hl=[a] if a else []), TR("q", rq, hl=[b] if b else []))
            return False
        T(f"Both {a.val} — compare children", TR("p", rp, ok=[a]), TR("q", rq, ok=[b]))
        return same(a.left, b.left) and same(a.right, b.right)
    return same(p, q)


# 5 ---------------------------------------------------------------
Q(101, "Symmetric Tree", "Easy", "Mirror recursion",
  "Return <code>True</code> if the tree is a mirror of itself around its centre.",
  [(([1, 2, 2, 3, 4, 4, 3],), True), (([1, 2, 2, None, 3, None, 3],), False)],
  ("Make an inverted copy and check it equals the original.", "O(n)", "O(n)"),
  ("Compare the left subtree with the right subtree mirrored: outer pair (a.left, b.right) and inner pair (a.right, b.left).", "O(n)", "O(h)"),
  prep=T1)


@B
def is_symmetric(root):
    def mirror(n):
        return None if not n else TreeNode(n.val, mirror(n.right), mirror(n.left))

    def same(a, b):
        if not a or not b:
            return a is b
        return a.val == b.val and same(a.left, b.left) and same(a.right, b.right)
    return same(root, mirror(root))


@O
def is_symmetric(root):
    def mirror(a, b):
        if not a or not b:
            return a is b
        T(f"Compare {a.val} with its mirror {b.val}", TR("tree", root, hl=[a, b]))
        return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)
    return mirror(root.left, root.right)


# 6 ---------------------------------------------------------------
Q(102, "Binary Tree Level Order Traversal", "Medium", "BFS by level",
  "Return the node values level by level, left to right.",
  [(([3, 9, 20, None, None, 15, 7],), [[3], [9, 20], [15, 7]]), (([1],), [[1]]), (([],), [])],
  ("Find the height, then for each depth d run a DFS that collects nodes at depth d.", "O(n · h)", "O(h)"),
  ("BFS with a queue; process exactly len(queue) nodes per round — that's one level.", "O(n)", "O(w) — widest level"),
  prep=T1)


@B
def level_order(root):
    def height(n):
        return 0 if not n else 1 + max(height(n.left), height(n.right))

    def collect(n, d, out):
        if not n:
            return
        if d == 0:
            out.append(n.val)
        collect(n.left, d - 1, out)
        collect(n.right, d - 1, out)
    res = []
    for d in range(height(root)):
        row = []
        collect(root, d, row)
        res.append(row)
    return res


@O
def level_order(root):
    from collections import deque
    if not root:
        return []
    res, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        res.append(level)
        T(f"Level {len(res) - 1}: {level}", TR("tree", root, hl=level), A("queue (next level)", [n.val for n in q]), V(result=res), at="prev")
    return res


# 7 ---------------------------------------------------------------
Q(543, "Diameter of Binary Tree", "Easy", "Height + global best",
  "Return the number of edges on the longest path between any two nodes.",
  [(([1, 2, 3, 4, 5],), 3), (([1, 2],), 1)],
  ("For every node, compute left and right heights with separate calls.", "O(n²)", "O(h)"),
  ("One postorder pass: each node returns its height, and left + right height through it is a candidate diameter.", "O(n)", "O(h)"),
  prep=T1, viz=([1, 2, 3, 4, 5, None, None, 6, None, None, 7],))


@B
def diameter_of_binary_tree(root):
    def height(n):
        return 0 if not n else 1 + max(height(n.left), height(n.right))

    def best(n):
        if not n:
            return 0
        return max(height(n.left) + height(n.right), best(n.left), best(n.right))
    return best(root)


@O
def diameter_of_binary_tree(root):
    best = 0

    def height(node):
        nonlocal best
        if not node:
            return 0
        l, r = height(node.left), height(node.right)
        best = max(best, l + r)
        T(f"At {node.val}: left height {l} + right height {r} = {l + r}", TR("tree", root, hl=[node]), V(best=best), at="prev")
        return 1 + max(l, r)

    height(root)
    return best


# 8 ---------------------------------------------------------------
Q(110, "Balanced Binary Tree", "Easy", "Height or −1",
  "A tree is height-balanced if every node's subtrees differ in height by at most 1. Check it.",
  [(([3, 9, 20, None, None, 15, 7],), True), (([1, 2, 2, 3, 3, None, None, 4, 4],), False), (([],), True)],
  ("At every node compare the heights of both subtrees, computing heights from scratch.", "O(n²)", "O(h)"),
  ("Return the height bottom-up, or −1 as soon as any subtree is unbalanced — the −1 short-circuits upward.", "O(n)", "O(h)"),
  prep=T1)


@B
def is_balanced(root):
    def height(n):
        return 0 if not n else 1 + max(height(n.left), height(n.right))
    if not root:
        return True
    return abs(height(root.left) - height(root.right)) <= 1 and is_balanced(root.left) and is_balanced(root.right)


@O
def is_balanced(root):
    def check(node):
        if not node:
            return 0
        l, r = check(node.left), check(node.right)
        if l < 0 or r < 0 or abs(l - r) > 1:
            T(f"{node.val} is unbalanced (heights {l}, {r}) → −1", TR("tree", root, hl=[node]))
            return -1
        T(f"{node.val}: heights {l} and {r} → height {1 + max(l, r)}", TR("tree", root, ok=[node]))
        return 1 + max(l, r)
    return check(root) >= 0


# 9 ---------------------------------------------------------------
Q(572, "Subtree of Another Tree", "Easy", "Serialise + substring",
  "Return <code>True</code> if <code>subRoot</code> appears as a full subtree of <code>root</code>.",
  [(([3, 4, 5, 1, 2], [4, 1, 2]), True), (([3, 4, 5, 1, 2, None, None, None, None, 0], [4, 1, 2]), False)],
  ("For every node of root, check whether the tree starting there equals subRoot.", "O(m · n)", "O(h)"),
  ("Serialise both trees in preorder with markers for None and delimiters around values; subRoot is a subtree exactly when its string is a substring. (Use KMP for a guaranteed linear search.)", "O(m + n)", "O(m + n)"),
  prep=lambda a: (mk_tree(a[0]), mk_tree(a[1])))


@B
def is_subtree(root, sub):
    def same(a, b):
        if not a or not b:
            return a is b
        return a.val == b.val and same(a.left, b.left) and same(a.right, b.right)
    if not root:
        return False
    return same(root, sub) or is_subtree(root.left, sub) or is_subtree(root.right, sub)


@O
def is_subtree(root, sub):
    def ser(node, out):
        if not node:
            out.append("#")
            return
        out.append(f"^{node.val}")
        ser(node.left, out)
        ser(node.right, out)

    a, b = [], []
    ser(root, a)
    ser(sub, b)
    big, small = ",".join(a), ",".join(b)
    T("Preorder strings with # for None", TR("root", root), TR("subRoot", sub), V(root=big, subRoot=small, found=small in big))
    return small in big


# 10 --------------------------------------------------------------
Q(235, "Lowest Common Ancestor of a Binary Search Tree", "Medium", "BST split point",
  "Return the lowest node in the BST that has both <code>p</code> and <code>q</code> as descendants (a node counts as its own descendant).",
  [(([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 8), 6), (([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 4), 2), (([2, 1], 2, 1), 2)],
  ("Use the general binary-tree LCA that ignores the ordering and searches both sides.", "O(n)", "O(h)"),
  ("Walk from the root: both values smaller → go left; both larger → go right; otherwise this node is where they split — the LCA.", "O(h)", "O(1)"),
  prep=lambda a: _lca_prep(a), names=("root", "p", "q"), post=lambda n: n.val,
  viz=([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 3, 5))


@B
def lca_bst(root, p, q):
    def lca(n):
        if not n or n.val in (p.val, q.val):
            return n
        l, r = lca(n.left), lca(n.right)
        return n if l and r else l or r
    return lca(root)


@O
def lca_bst(root, p, q):
    node = root
    while node:
        T(f"At {node.val}: p = {p.val}, q = {q.val}", TR("tree", root, hl=[node], ok=[p.val, q.val]))
        if p.val < node.val and q.val < node.val:
            node = node.left
        elif p.val > node.val and q.val > node.val:
            node = node.right
        else:
            return node


# 11 --------------------------------------------------------------
Q(236, "Lowest Common Ancestor of a Binary Tree", "Medium", "Postorder report-up",
  "Return the lowest common ancestor of nodes <code>p</code> and <code>q</code> in a binary tree (no ordering).",
  [(([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 5, 1), 3), (([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 5, 4), 5), (([1, 2], 1, 2), 1)],
  ("Record the root-to-p and root-to-q paths, then take the last node they share.", "O(n)", "O(n)"),
  ("Each call returns p or q if it finds one below it. The first node that gets a non-empty answer from both sides is the LCA.", "O(n)", "O(h)"),
  prep=lambda a: _lca_prep(a), names=("root", "p", "q"), post=lambda n: n.val,
  viz=([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 7, 8))


def _lca_prep(a):
    root = mk_tree(a[0])
    return root, find(root, a[1]), find(root, a[2])


@B
def lowest_common_ancestor(root, p, q):
    def path(n, target, acc):
        if not n:
            return False
        acc.append(n)
        if n is target or path(n.left, target, acc) or path(n.right, target, acc):
            return True
        acc.pop()
        return False
    a, b = [], []
    path(root, p, a)
    path(root, q, b)
    i = 0
    while i < min(len(a), len(b)) and a[i] is b[i]:
        i += 1
    return a[i - 1]


@O
def lowest_common_ancestor(root, p, q):
    top = root

    def lca(node):
        if not node or node is p or node is q:
            return node
        left, right = lca(node.left), lca(node.right)
        T(f"At {node.val}: left reports {left.val if left else 'None'}, right reports {right.val if right else 'None'}", TR("tree", top, hl=[node], ok=[p, q]), at="prev")
        if left and right:
            return node
        return left or right
    return lca(root)


# 12 --------------------------------------------------------------
Q(98, "Validate Binary Search Tree", "Medium", "Bounds passed down",
  "Return <code>True</code> if the tree is a valid BST (strictly smaller on the left, strictly larger on the right, all the way down).",
  [(([2, 1, 3],), True), (([5, 1, 4, None, None, 3, 6],), False), (([5, 4, 6, None, None, 3, 7],), False)],
  ("For every node, check that all values in its left subtree are smaller and all in its right are larger.", "O(n²)", "O(h)"),
  ("Pass an allowed (low, high) range down: going left tightens high to the node's value, going right tightens low.", "O(n)", "O(h)"),
  prep=T1)


@B
def is_valid_bst(root):
    def vals(n):
        return [] if not n else vals(n.left) + [n.val] + vals(n.right)
    if not root:
        return True
    if any(v >= root.val for v in vals(root.left)) or any(v <= root.val for v in vals(root.right)):
        return False
    return is_valid_bst(root.left) and is_valid_bst(root.right)


@O
def is_valid_bst(root):
    def ok(node, low, high):
        if not node:
            return True
        good = low < node.val < high
        T(f"{node.val} must be in ({low}, {high}) → {'OK' if good else 'violates'}", TR("tree", root, hl=[] if good else [node], ok=[node] if good else []))
        if not good:
            return False
        return ok(node.left, low, node.val) and ok(node.right, node.val, high)
    return ok(root, float("-inf"), float("inf"))


# 13 --------------------------------------------------------------
Q(230, "Kth Smallest Element in a BST", "Medium", "Inorder with early stop",
  "Return the k-th smallest value (1-indexed) in a BST.",
  [(([3, 1, 4, None, 2], 1), 1), (([5, 3, 6, 2, 4, None, None, 1], 3), 3)],
  ("Collect the full inorder list and index it.", "O(n)", "O(n)"),
  ("Iterative inorder visits values in sorted order; stop at the k-th pop.", "O(h + k)", "O(h)"),
  prep=lambda a: (mk_tree(a[0]), a[1]),
  viz=([5, 3, 6, 2, 4, None, None, 1], 4))


@B
def kth_smallest(root, k):
    def ino(n):
        return [] if not n else ino(n.left) + [n.val] + ino(n.right)
    return ino(root)[k - 1]


@O
def kth_smallest(root, k):
    stack, cur, count = [], root, 0
    while True:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        count += 1
        T(f"Inorder visit #{count}: {cur.val}", TR("tree", root, hl=[cur]), V(k=k, count=count), at="prev")
        if count == k:
            return cur.val
        cur = cur.right


# 14 --------------------------------------------------------------
Q(199, "Binary Tree Right Side View", "Medium", "DFS right-first by depth",
  "Return the values visible from the right side, top to bottom.",
  [(([1, 2, 3, None, 5, None, 4],), [1, 3, 4]), (([1, 2, 3, 4, None, None, None, 5],), [1, 3, 4, 5]), (([],), [])],
  ("Level-order traversal storing every level, then take each level's last value.", "O(n)", "O(n)"),
  ("DFS visiting right before left; the first node reached at each new depth is the visible one.", "O(n)", "O(h)"),
  prep=T1)


@B
def right_side_view(root):
    levels, q = [], [root] if root else []
    while q:
        levels.append([n.val for n in q])
        q = [c for n in q for c in (n.left, n.right) if c]
    return [lv[-1] for lv in levels]


@O
def right_side_view(root):
    res = []

    def dfs(node, depth):
        if not node:
            return
        if depth == len(res):
            res.append(node.val)
            T(f"First node at depth {depth} (coming from the right): {node.val}", TR("tree", root, hl=[node], ok=res), A("view", res), at="prev")
        dfs(node.right, depth + 1)
        dfs(node.left, depth + 1)

    dfs(root, 0)
    return res


# 15 --------------------------------------------------------------
Q(105, "Construct Binary Tree from Preorder and Inorder Traversal", "Medium", "Split by root index",
  "Build the tree from its preorder and inorder traversals (values are unique).",
  [(([3, 9, 20, 15, 7], [9, 3, 15, 20, 7]), [3, 9, 20, None, None, 15, 7]), (([-1], [-1]), [-1])],
  ("Take preorder[0] as the root, search for it in inorder to split, and slice lists for each side.", "O(n²)", "O(n²) slices"),
  ("Same split, but look up the root's inorder index in a dict and recurse on index ranges instead of slices.", "O(n)", "O(n)"),
  post=tree_arr)


@B
def build_tree(preorder, inorder):
    if not preorder:
        return None
    root = TreeNode(preorder[0])
    i = inorder.index(preorder[0])
    root.left = build_tree(preorder[1:i + 1], inorder[:i])
    root.right = build_tree(preorder[i + 1:], inorder[i + 1:])
    return root


@O
def build_tree(preorder, inorder):
    where = {v: i for i, v in enumerate(inorder)}
    pre = iter(preorder)
    holder = {}

    def build(lo, hi):
        if lo > hi:
            return None
        val = next(pre)
        node = TreeNode(val)
        holder.setdefault("root", node)
        T(f"Root {val} splits inorder[{lo}..{hi}] at index {where[val]}", A("inorder", inorder, hl=range(lo, hi + 1), ok=[where[val]]), TR("built so far", holder["root"], hl=[node]), at="prev")
        node.left = build(lo, where[val] - 1)
        node.right = build(where[val] + 1, hi)
        return node

    return build(0, len(inorder) - 1)


# 16 --------------------------------------------------------------
Q(124, "Binary Tree Maximum Path Sum", "Hard", "Gain returned up, best through node",
  "A path goes along parent–child edges and need not pass through the root. Return the largest sum of node values on any non-empty path.",
  [(([1, 2, 3],), 6), (([-10, 9, 20, None, None, 15, 7],), 42), (([-3],), -3)],
  ("Treat every node as the top of the path and compute the best downward chains from it with separate calls.", "O(n²)", "O(h)"),
  ("Each call returns the best chain going down from the node (dropping negative branches). The path through the node is val + left gain + right gain; keep the max.", "O(n)", "O(h)"),
  prep=T1)


@B
def max_path_sum(root):
    def down(n):
        return 0 if not n else max(0, n.val + max(down(n.left), down(n.right)))

    def best(n):
        if not n:
            return float("-inf")
        through = n.val + down(n.left) + down(n.right)
        return max(through, best(n.left), best(n.right))
    return best(root)


@O
def max_path_sum(root):
    best = float("-inf")

    def gain(node):
        nonlocal best
        if not node:
            return 0
        l = max(gain(node.left), 0)
        r = max(gain(node.right), 0)
        best = max(best, node.val + l + r)
        T(f"Path through {node.val}: {node.val} + {l} + {r} = {node.val + l + r}", TR("tree", root, hl=[node]), V(best=best, returns_up=node.val + max(l, r)), at="prev")
        return node.val + max(l, r)

    gain(root)
    return best


# 17 --------------------------------------------------------------
Q(297, "Serialize and Deserialize Binary Tree", "Hard", "Preorder with null markers",
  "Design <code>serialize(root) → str</code> and <code>deserialize(str) → root</code> so that the tree round-trips exactly.",
  [(([1, 2, 3, None, None, 4, 5],), [1, 2, 3, None, None, 4, 5]), (([],), []), (([1, None, 2, None, 3],), [1, None, 2, None, 3])],
  ("Store the tree as an array using heap positions (children of i at 2i+1, 2i+2). A skewed tree of n nodes needs about 2ⁿ slots.", "O(2ⁿ) worst", "O(2ⁿ) worst"),
  ("Preorder walk writing '#' for every missing child. Reading tokens back in the same order rebuilds the tree, since each '#' tells us where a subtree ends.", "O(n)", "O(n)"),
  runner=lambda cls, a: tree_arr(cls().deserialize(cls().serialize(mk_tree(a[0])))), names=("root",))


@B
class Codec:
    def serialize(self, root):
        slots = {}

        def put(n, i):
            if n:
                slots[i] = n.val
                put(n.left, 2 * i + 1)
                put(n.right, 2 * i + 2)
        put(root, 0)
        size = max(slots) + 1 if slots else 0
        return ",".join(str(slots[i]) if i in slots else "#" for i in range(size))

    def deserialize(self, data):
        if not data:
            return None
        vals = data.split(",")

        def get(i):
            if i >= len(vals) or vals[i] == "#":
                return None
            return TreeNode(int(vals[i]), get(2 * i + 1), get(2 * i + 2))
        return get(0)


@O
class Codec:
    def serialize(self, root):
        out = []

        def dfs(node):
            if not node:
                out.append("#")
                return
            out.append(str(node.val))
            T(f"Write {node.val}", TR("tree", root, hl=[node]), A("tokens", out, hl=[len(out) - 1]), at="prev")
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ",".join(out)

    def deserialize(self, data):
        tokens = iter(data.split(","))

        def build():
            t = next(tokens)
            if t == "#":
                return None
            node = TreeNode(int(t))
            node.left = build()
            node.right = build()
            return node
        root = build()
        T("Rebuilt by reading the tokens in the same preorder", TR("rebuilt", root), V(data=data))
        return root


# 18 --------------------------------------------------------------
Q(103, "Binary Tree Zigzag Level Order Traversal", "Medium", "BFS + direction flag",
  "Return the level order traversal, alternating left→right and right→left.",
  [(([3, 9, 20, None, None, 15, 7],), [[3], [20, 9], [15, 7]]), (([1],), [[1]]), (([],), [])],
  ("Plain level order, then reverse every odd level afterwards.", "O(n)", "O(n)"),
  ("BFS per level, building each level in a deque: append right on even levels, append left on odd levels.", "O(n)", "O(w)"),
  prep=T1, viz=([1, 2, 3, 4, 5, 6, 7],))


@B
def zigzag_level_order(root):
    levels, q = [], [root] if root else []
    while q:
        levels.append([n.val for n in q])
        q = [c for n in q for c in (n.left, n.right) if c]
    return [lv if i % 2 == 0 else lv[::-1] for i, lv in enumerate(levels)]


@O
def zigzag_level_order(root):
    from collections import deque
    if not root:
        return []
    res, q, ltr = [], deque([root]), True
    while q:
        level = deque()
        for _ in range(len(q)):
            node = q.popleft()
            if ltr:
                level.append(node.val)
            else:
                level.appendleft(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        res.append(list(level))
        T(f"Level {len(res) - 1} read {'left → right' if ltr else 'right → left'}: {list(level)}", TR("tree", root, hl=list(level)), V(result=res), at="prev")
        ltr = not ltr
    return res


# 19 --------------------------------------------------------------
Q(1448, "Count Good Nodes in Binary Tree", "Medium", "Carry the max downward",
  "A node is good if no node on the path from the root to it has a greater value. Count good nodes.",
  [(([3, 1, 4, 3, None, 1, 5],), 4), (([3, 3, None, 4, 2],), 3), (([1],), 1)],
  ("For each node, find its root path again and check the maximum on it.", "O(n · h)", "O(h)"),
  ("DFS passing the largest value seen so far on the path; a node is good if its value ≥ that max.", "O(n)", "O(h)"),
  prep=T1)


@B
def good_nodes(root):
    count = 0

    def visit(n, path):
        nonlocal count
        if not n:
            return
        if all(v <= n.val for v in path):
            count += 1
        visit(n.left, path + [n.val])
        visit(n.right, path + [n.val])
    visit(root, [])
    return count


@O
def good_nodes(root):
    good = []

    def dfs(node, high):
        if not node:
            return 0
        is_good = node.val >= high
        if is_good:
            good.append(node)
        T(f"{node.val} vs path max {high} → {'good' if is_good else 'not good'}", TR("tree", root, hl=[node], ok=good), V(good=len(good)))
        high = max(high, node.val)
        return is_good + dfs(node.left, high) + dfs(node.right, high)

    return dfs(root, root.val)


# 20 --------------------------------------------------------------
Q(114, "Flatten Binary Tree to Linked List", "Medium", "Rewire in place (Morris style)",
  "Flatten the tree in place into a 'linked list' along right pointers in preorder; all left pointers become None.",
  [(([1, 2, 5, 3, 4, None, 6],), [1, None, 2, None, 3, None, 4, None, 5, None, 6]), (([],), []), (([0],), [0])],
  ("Record the preorder nodes in a list, then relink them one after another.", "O(n)", "O(n)"),
  ("For each node with a left child: find the rightmost node of the left subtree, hang the right subtree there, move the left subtree to the right. Then step right.", "O(n)", "O(1)"),
  prep=T1, post=tree_arr, inplace=0)


@B
def flatten(root):
    order = []

    def pre(n):
        if n:
            order.append(n)
            pre(n.left)
            pre(n.right)
    pre(root)
    for a, b in zip(order, order[1:]):
        a.left, a.right = None, b
    if order:
        order[-1].left = order[-1].right = None


@O
def flatten(root):
    cur = root
    while cur:
        if cur.left:
            tail = cur.left
            while tail.right:
                tail = tail.right
            tail.right = cur.right
            cur.right, cur.left = cur.left, None
            T(f"At {cur.val}: hang its right subtree under {tail.val}, then move the left subtree to the right", TR("tree", root, hl=[cur], ok=[tail]), at="prev")
        cur = cur.right
