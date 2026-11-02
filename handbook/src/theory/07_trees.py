from lib import *

THEORY("Definition", """
<p>A <b>tree</b> is a <b>non-linear, hierarchical</b> data structure made of nodes connected by edges, with one special node called the <b>root</b> and <b>no cycles</b>. Every node except the root has exactly one parent.</p>
<p>A <b>binary tree</b> is a tree in which each node has at most two children, called the <b>left child</b> and the <b>right child</b>.</p>
<p>A <b>binary search tree (BST)</b> is a binary tree where, for every node, all keys in its left subtree are smaller and all keys in its right subtree are larger than the node's key.</p>
""")

THEORY("Terminology", """
<table>
<tr><th>Term</th><th>Meaning</th></tr>
<tr><td>Root</td><td>top node, no parent</td></tr>
<tr><td>Parent / child</td><td>a node directly above / below another</td></tr>
<tr><td>Siblings</td><td>nodes with the same parent</td></tr>
<tr><td>Leaf (external node)</td><td>node with no children</td></tr>
<tr><td>Internal node</td><td>node with at least one child</td></tr>
<tr><td>Edge</td><td>connection between parent and child</td></tr>
<tr><td>Path</td><td>sequence of nodes connected by edges</td></tr>
<tr><td>Depth of a node</td><td>number of edges from the root to it (root has depth 0)</td></tr>
<tr><td>Height of a node</td><td>edges on the longest path from it down to a leaf (leaf has height 0)</td></tr>
<tr><td>Height of the tree</td><td>height of the root</td></tr>
<tr><td>Level</td><td>all nodes at the same depth</td></tr>
<tr><td>Degree</td><td>number of children of a node</td></tr>
<tr><td>Subtree</td><td>a node and all its descendants</td></tr>
<tr><td>Ancestor / descendant</td><td>nodes on the path above / below</td></tr>
</table>
""")

THEORY("Types of binary trees", """
<table>
<tr><th>Type</th><th>Definition</th></tr>
<tr><td><b>Full (strict)</b></td><td>every node has 0 or 2 children</td></tr>
<tr><td><b>Complete</b></td><td>all levels full except possibly the last, which is filled from the left (heaps are complete)</td></tr>
<tr><td><b>Perfect</b></td><td>all internal nodes have 2 children and all leaves are at the same level</td></tr>
<tr><td><b>Balanced</b></td><td>for every node, left and right subtree heights differ by at most 1 (height O(log n))</td></tr>
<tr><td><b>Degenerate (skewed)</b></td><td>every node has one child — effectively a linked list (height n − 1)</td></tr>
</table>
<h4>Self-balancing BSTs</h4>
<p>Plain BSTs can degenerate to O(n). <b>AVL trees</b> (strict balance by rotations) and <b>Red–Black trees</b> (looser colour rules, used in Java's <code>TreeMap</code> and C++ <code>std::map</code>) keep height O(log n) after every insert and delete. Also: B-trees / B+ trees for databases and file systems, tries for strings, segment trees for range queries.</p>
""")

THEORY("Important properties", """
<ul>
<li>A tree with <b>n</b> nodes has exactly <b>n − 1</b> edges.</li>
<li>Maximum nodes at level i (root at level 0): <b>2ⁱ</b>.</li>
<li>Maximum nodes in a binary tree of height h: <b>2ʰ⁺¹ − 1</b> (a perfect tree).</li>
<li>Minimum height of a binary tree with n nodes: <b>⌈log₂(n + 1)⌉ − 1</b>.</li>
<li>In a full binary tree, leaves = internal nodes + 1.</li>
<li>In a complete binary tree stored in an array, the children of index i are <b>2i + 1</b> and <b>2i + 2</b>, and the parent is <b>(i − 1) // 2</b>.</li>
<li>Number of structurally different binary trees with n nodes is the Catalan number C(n) = (2n)! / ((n + 1)! n!).</li>
</ul>
""")

THEORY("Traversals", """
<table>
<tr><th>Traversal</th><th>Order</th><th>For tree [1, 2, 3, 4, 5]</th><th>Uses</th></tr>
<tr><td><b>Preorder</b> (DFS)</td><td>Root, Left, Right</td><td>1 2 4 5 3</td><td>copy / serialise a tree, prefix expressions</td></tr>
<tr><td><b>Inorder</b> (DFS)</td><td>Left, Root, Right</td><td>4 2 5 1 3</td><td>sorted order of a BST, infix expressions</td></tr>
<tr><td><b>Postorder</b> (DFS)</td><td>Left, Right, Root</td><td>4 5 2 3 1</td><td>delete a tree, compute heights/sizes, postfix expressions</td></tr>
<tr><td><b>Level order</b> (BFS)</td><td>level by level, left to right</td><td>1 2 3 4 5</td><td>shortest depth, per-level problems</td></tr>
</table>
<p>All traversals are O(n) time. DFS uses O(h) space (recursion stack); BFS uses O(w) space (widest level). <b>Morris traversal</b> does inorder in O(1) space by temporarily rewiring right pointers.</p>
<p>A tree can be uniquely rebuilt from <b>inorder + preorder</b> or <b>inorder + postorder</b> (with distinct values), but not from preorder + postorder alone.</p>
""")

THEORY("BST operations and complexity", """
<table>
<tr><th>Operation</th><th>Balanced BST</th><th>Skewed BST</th><th>How</th></tr>
<tr><td>Search</td><td>O(log n)</td><td>O(n)</td><td>go left if smaller, right if larger</td></tr>
<tr><td>Insert</td><td>O(log n)</td><td>O(n)</td><td>search for the spot, attach a new leaf</td></tr>
<tr><td>Delete</td><td>O(log n)</td><td>O(n)</td><td>leaf: remove; one child: link child to parent; two children: replace with inorder successor (smallest in right subtree), then delete that</td></tr>
<tr><td>Min / max</td><td>O(log n)</td><td>O(n)</td><td>leftmost / rightmost node</td></tr>
<tr><td>Inorder (sorted output)</td><td>O(n)</td><td>O(n)</td><td>left, node, right</td></tr>
</table>
""")

THEORY("Advantages and applications", """
<div class="two">
<div class="pro"><h5>Advantages</h5><ul><li>Represents hierarchies naturally</li><li>Balanced BSTs: O(log n) search, insert, delete <i>and</i> sorted order</li><li>Range queries, floor/ceiling, k-th smallest</li></ul></div>
<div class="con"><h5>Disadvantages</h5><ul><li>Unbalanced BSTs degrade to O(n)</li><li>Balancing logic (AVL, Red–Black) is complex</li><li>More memory than arrays (two pointers per node)</li></ul></div>
</div>
<h4>Applications</h4>
<ul>
<li>File systems and folder hierarchies; the HTML DOM; organisation charts.</li>
<li>Database indexes (B-trees, B+ trees).</li>
<li>Sorted maps and sets (<code>TreeMap</code>, <code>std::map</code>).</li>
<li>Expression trees and syntax trees in compilers.</li>
<li>Decision trees in machine learning; Huffman coding trees in compression.</li>
<li>Heaps (priority queues) and tries (autocomplete).</li>
</ul>
""")

FAQ("What's the difference between a binary tree and a BST?", "<p>A binary tree only limits each node to two children. A BST adds the ordering rule: left subtree keys &lt; node &lt; right subtree keys, at every node. That rule enables O(h) search.</p>")
FAQ("Depth vs height?", "<p>Depth of a node is measured from the root down to the node; height is measured from the node down to its deepest leaf. The root has depth 0; leaves have height 0. The tree's height is the root's height.</p>")
FAQ("Complete vs full vs perfect binary tree?", "<p>Full: every node has 0 or 2 children. Complete: all levels filled except possibly the last, which is filled left to right. Perfect: full and all leaves at the same depth (2ʰ⁺¹ − 1 nodes).</p>")
FAQ("Why does inorder traversal of a BST give sorted output?", "<p>Inorder visits the left subtree (all smaller keys), then the node, then the right subtree (all larger keys). Applied recursively, every key is output after all smaller keys and before all larger ones.</p>")
FAQ("DFS vs BFS on trees — when to use which?", "<p>DFS (recursion) for problems about paths, subtrees and anything computed from children (height, diameter). BFS (queue) for level-based questions (level order, right view, minimum depth). Memory: DFS O(h), BFS O(w).</p>")
FAQ("What is the worst-case time of BST search and how is it avoided?", "<p>O(n) when the tree is skewed (e.g., inserting sorted data). Self-balancing trees — AVL or Red–Black — rotate nodes after updates to keep the height O(log n).</p>")
FAQ("How do you delete a node with two children from a BST?", "<p>Replace its key with its inorder successor (the minimum of its right subtree) — or predecessor — then delete that successor node, which has at most one child.</p>")
FAQ("Can a tree be rebuilt from its preorder and inorder traversals?", "<p>Yes, if keys are distinct: preorder's first element is the root; its position in inorder splits the left and right subtrees; recurse. Preorder + postorder alone is ambiguous when nodes have one child.</p>")
