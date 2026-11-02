from lib import *

LESSON("Basics", "Tree vocabulary", """
<p>A <b>tree</b> is a set of nodes where each node has one parent (except the <b>root</b>) and any number of children. In a <b>binary tree</b> each node has at most two: <code>left</code> and <code>right</code>.</p>
<div class="pic">        1          ← root (depth 0)
       / \\
      2   3        ← depth 1
     / \\   \\
    4   5   6      ← leaves (no children), depth 2       height = 3 levels</div>
<ul>
<li><b>Leaf</b>: a node with no children.</li>
<li><b>Depth</b> of a node: edges from the root to it. <b>Height</b> of a tree: number of levels (or edges on the longest root-to-leaf path — check which one the problem means).</li>
<li><b>Subtree</b>: a node together with everything below it. Every subtree is itself a tree — this is why recursion fits trees so well.</li>
<li><b>Balanced</b>: height is about log₂ n. A <b>skewed</b> tree is basically a linked list with height n.</li>
</ul>
<p>LeetCode writes trees as level-order lists with <code>None</code> for gaps: <code>[1, 2, 3, 4, 5, None, 6]</code>.</p>
""")


@LD
def build_tree_lesson():
    vals = [1, 2, 3, 4, 5, None, 6]
    root = TreeNode(vals[0])
    queue, i = [root], 1
    T("Root from vals[0]", A("level-order input", vals, ok=[0]), TR("tree", root, hl=[root]))
    while queue and i < len(vals):
        node = queue.pop(0)
        for side in ("left", "right"):
            if i < len(vals) and vals[i] is not None:
                child = TreeNode(vals[i])
                setattr(node, side, child)
                queue.append(child)
                T(f"vals[{i}] = {vals[i]} becomes the {side} child of {node.val}", A("level-order input", vals, ok=range(i + 1), hl=[i]), TR("tree", root, hl=[child]))
            i += 1
    return root


LESSON("Basics", "Recursion on trees", """
<p>Nearly every tree solution has the same shape:</p>
<pre><code class="py">def solve(node):
    if node is None:          # 1. base case: empty tree
        return BASE
    left = solve(node.left)   # 2. trust recursion for the children
    right = solve(node.right)
    return combine(node.val, left, right)   # 3. combine</code></pre>
<p>Example — maximum depth: base is 0, combine is <code>1 + max(left, right)</code>. Count nodes: <code>1 + left + right</code>. Sum: <code>node.val + left + right</code>.</p>
<h4>The three DFS orders</h4>
<p>"Visiting" a node means doing your work there. Doing it before the children is <b>preorder</b>, between them <b>inorder</b>, after them <b>postorder</b>. Each tree node is visited once → O(n) time, O(h) stack space.</p>
<div class="tip">Don't trace the whole recursion in your head. Assume the calls on the children return correct answers and only check the combine step and the base case.</div>
""", practice=[94, 104, 226, 100, 101])


LESSON("Core", "Breadth-first search: level by level", """
<p>DFS dives deep first. <b>BFS</b> visits all nodes at depth 0, then depth 1, then depth 2 … using a <b>queue</b>.</p>
<pre><code class="py">from collections import deque
q = deque([root])
while q:
    level = []
    for _ in range(len(q)):     # exactly the nodes of this level
        node = q.popleft()
        level.append(node.val)
        if node.left:  q.append(node.left)
        if node.right: q.append(node.right)
    print(level)</code></pre>
<p>The <code>for _ in range(len(q))</code> trick separates levels. Use BFS for anything "per level": level order, right side view (last of each level), zigzag, minimum depth (first leaf found).</p>
""", practice=[102, 199, 103])


@LD
def bfs_tree_lesson():
    from collections import deque
    root = mk_tree([3, 9, 20, None, None, 15, 7])
    q, levels = deque([root]), []
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        levels.append(level)
        T(f"Level {len(levels) - 1}: {level}; the queue now holds the next level", TR("tree", root, hl=level, ok=[v for lv in levels[:-1] for v in lv]), A("queue", [n.val for n in q]), V(levels=levels), at="prev")
    return levels


LESSON("Core", "Bottom-up: return a value, update a global", """
<p>Some answers don't pass through the root. <b>Diameter</b>: the longest path may go through any node. Solve with a postorder DFS that <b>returns</b> one thing (height) and <b>updates</b> another (best answer):</p>
<pre><code class="py">best = 0
def height(node):
    nonlocal best
    if not node: return 0
    l, r = height(node.left), height(node.right)
    best = max(best, l + r)        # path that bends at this node
    return 1 + max(l, r)           # what the parent can use</code></pre>
<p>The same split solves <b>balanced tree</b> (return height or −1) and <b>max path sum</b> (return the best one-sided chain, record the best two-sided path).</p>
""", practice=[543, 110, 124])


LESSON("Core", "Top-down: pass information down", """
<p>Sometimes a node needs to know about its <b>ancestors</b>. Pass that info as a parameter:</p>
<ul>
<li><b>Good nodes</b>: pass the largest value seen on the path from the root.</li>
<li><b>Validate BST</b>: pass the allowed range <code>(low, high)</code>; going left sets <code>high = node.val</code>, going right sets <code>low = node.val</code>.</li>
<li><b>Path sums</b>: pass the remaining target.</li>
</ul>
<p>Bottom-up = "children tell the parent". Top-down = "parent tells the children". Some problems use both.</p>
""", practice=[1448, 98])


LESSON("Core", "Binary search trees", """
<p>A <b>BST</b> keeps one rule at every node: all values in the left subtree are smaller, all in the right subtree are larger.</p>
<ul>
<li><b>Search / insert</b>: compare with the node and go left or right — O(h), which is O(log n) when balanced.</li>
<li><b>Inorder traversal gives sorted order.</b> So "k-th smallest" = the k-th inorder visit; "validate" = inorder values strictly increasing.</li>
<li><b>LCA in a BST</b>: walk from the root; if both targets are smaller go left, if both larger go right, otherwise you're at the split point — the answer.</li>
</ul>
<div class="warn">Checking only <code>node.left.val &lt; node.val &lt; node.right.val</code> is not enough — a value deep in the left subtree can still be too big. Use ranges.</div>
""", practice=[235, 230, 98])


@LD
def bst_lesson():
    root = None
    for v in [8, 3, 10, 1, 6, 14, 4]:
        if root is None:
            root = TreeNode(v)
        else:
            node = root
            while True:
                side = "left" if v < node.val else "right"
                nxt = getattr(node, side)
                if nxt is None:
                    setattr(node, side, TreeNode(v))
                    break
                node = nxt
        T(f"Insert {v}: go left if smaller, right if larger", TR("BST", root, hl=[v]))
    node, path = root, []
    while node and node.val != 4:
        path.append(node)
        node = node.left if 4 < node.val else node.right
    T("Search 4: only one path is checked — O(height)", TR("BST", root, hl=path, ok=[node]))
    return root


LESSON("Advanced", "Building, serialising and ancestors", """
<ul>
<li><b>Build from preorder + inorder</b>: preorder's first value is the root; its position in inorder splits left and right subtrees. A dict of inorder positions makes it O(n).</li>
<li><b>Serialise</b>: preorder with a marker (<code>#</code>) for every missing child is enough to rebuild the exact tree.</li>
<li><b>LCA in a general tree</b>: each call returns p or q if found below. The first node that gets an answer from both sides is the LCA.</li>
<li><b>Flatten / rewire in place</b>: find the rightmost node of the left subtree, hang the right subtree there, move left to right (Morris-style, O(1) space).</li>
<li><b>Subtree check</b>: serialise both trees and use substring search.</li>
</ul>
<div class="tip">Python's recursion limit is about 1000. For trees that could be 10⁵ deep, write the DFS with an explicit stack.</div>
""", practice=[105, 297, 236, 114, 572])
