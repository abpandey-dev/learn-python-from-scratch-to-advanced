from lib import *

THEORY("Definition", """
<p>A <b>trie</b> (pronounced "try", from re<b>trie</b>val), also called a <b>prefix tree</b> or <b>digital tree</b>, is a tree-based data structure for storing a set of strings where each edge represents one character and each path from the root spells a prefix. Strings with a common prefix share the nodes of that prefix.</p>
<p>Each node holds a map (or array) of <b>children</b> and a boolean <b>end-of-word</b> marker. The root represents the empty string.</p>
""")

THEORY("Structure and properties", """
<ul>
<li>The root is empty; each child edge is labelled by a character.</li>
<li>A word is present only if its path exists <b>and</b> the last node is marked as end-of-word ("app" may exist as a prefix of "apple" without being a word).</li>
<li>The depth of a node equals the length of the prefix it represents.</li>
<li>Maximum children per node = alphabet size σ (26 for lowercase letters, 2 for a binary trie).</li>
<li>Total nodes ≤ total number of characters inserted + 1.</li>
<li>An inorder-like DFS visiting children in sorted order lists the words in <b>lexicographic order</b>.</li>
</ul>
<h4>Child storage choices</h4>
<table>
<tr><th>Children as</th><th>Lookup</th><th>Memory</th></tr>
<tr><td>fixed array of size σ</td><td>O(1)</td><td>σ pointers per node (wasteful when sparse)</td></tr>
<tr><td>hash map (Python dict)</td><td>O(1) average</td><td>proportional to actual children</td></tr>
<tr><td>sorted list / BST</td><td>O(log σ)</td><td>compact, ordered</td></tr>
</table>
""")

THEORY("Operations and complexity", """
<p>L = length of the word or prefix, N = number of words.</p>
<table>
<tr><th>Operation</th><th>Steps</th><th>Time</th></tr>
<tr><td>Insert</td><td>walk/create one node per character, mark the last</td><td>O(L)</td></tr>
<tr><td>Search (exact)</td><td>walk the path, check end marker</td><td>O(L)</td></tr>
<tr><td>startsWith (prefix)</td><td>walk the path only</td><td>O(L)</td></tr>
<tr><td>Delete</td><td>unmark end; remove nodes bottom-up that have no children and aren't ends</td><td>O(L)</td></tr>
<tr><td>List all words with prefix</td><td>walk to the prefix node, DFS below it</td><td>O(L + size of output)</td></tr>
</table>
<p>Space: O(total characters × child-pointer cost) in the worst case (no shared prefixes).</p>
""")

THEORY("Variants", """
<table>
<tr><th>Variant</th><th>Idea</th><th>Use</th></tr>
<tr><td><b>Compressed trie / radix tree (Patricia)</b></td><td>merge chains of single-child nodes into one edge labelled with a string</td><td>IP routing tables, memory-efficient dictionaries</td></tr>
<tr><td><b>Suffix trie / suffix tree</b></td><td>a trie of all suffixes of a text</td><td>substring search, longest repeated substring</td></tr>
<tr><td><b>Binary (bitwise) trie</b></td><td>children are bits 0/1 from the most significant bit</td><td>maximum XOR queries, IP prefix matching</td></tr>
<tr><td><b>Ternary search tree</b></td><td>each node has less / equal / greater children</td><td>space-efficient alternative to tries</td></tr>
<tr><td><b>Aho–Corasick automaton</b></td><td>trie of patterns plus failure links</td><td>search many patterns in a text at once (antivirus, grep -F)</td></tr>
</table>
""")

THEORY("Trie vs hash set vs BST", """
<table>
<tr><th></th><th>Trie</th><th>Hash set of strings</th><th>Balanced BST of strings</th></tr>
<tr><td>Insert / search</td><td>O(L)</td><td>O(L) average (hashing)</td><td>O(L log N)</td></tr>
<tr><td>Prefix query</td><td><b>O(L)</b></td><td>O(N · L)</td><td>O(L log N)</td></tr>
<tr><td>Sorted iteration</td><td>yes</td><td>no</td><td>yes</td></tr>
<tr><td>Worst case</td><td>no hash collisions</td><td>O(N) on collisions</td><td>guaranteed</td></tr>
<tr><td>Memory</td><td>high (many nodes)</td><td>low</td><td>medium</td></tr>
</table>
""")

THEORY("Advantages, disadvantages and applications", """
<div class="two">
<div class="pro"><h5>Advantages</h5><ul><li>Prefix queries in O(L), independent of the number of words</li><li>Shared prefixes are stored once</li><li>Words come out in lexicographic order</li><li>No hash collisions</li></ul></div>
<div class="con"><h5>Disadvantages</h5><ul><li>High memory use: many nodes and child maps</li><li>Slower than a hash set for plain exact lookups in practice</li><li>Pointer-heavy, poor cache locality</li></ul></div>
</div>
<h4>Applications</h4>
<ul>
<li>Autocomplete and search suggestions (search engines, IDEs, phone keyboards).</li>
<li>Spell checkers and word games (Boggle, Scrabble solvers).</li>
<li>IP routing: longest-prefix match on binary tries.</li>
<li>T9 predictive text; dictionary compression.</li>
<li>Multi-pattern text search (Aho–Corasick).</li>
</ul>
""")

FAQ("What is a trie and why use it over a hash map?", "<p>A tree that stores strings character by character with shared prefixes. A hash map answers exact lookups but needs O(N · L) to find all keys with a given prefix; a trie answers prefix queries in O(L).</p>")
FAQ("What is the time complexity of trie insert and search?", "<p>O(L), where L is the length of the word — independent of how many words are stored.</p>")
FAQ("How do you tell a stored word from a stored prefix?", "<p>Each node has an end-of-word flag set on the last node of every inserted word. <code>search</code> requires the flag; <code>startsWith</code> only requires the path to exist.</p>")
FAQ("How do you delete a word from a trie?", "<p>Unset the end flag on its last node, then walk back up removing nodes that have no children and aren't the end of another word.</p>")
FAQ("What is a binary trie used for?", "<p>Storing numbers bit by bit from the highest bit. To maximise XOR with a query number, greedily follow the opposite bit at each level — O(bits) per query.</p>")
FAQ("What is a compressed trie (radix tree)?", "<p>A trie where chains of nodes with a single child are merged into one edge labelled by a substring. It keeps the same queries with far fewer nodes.</p>")
