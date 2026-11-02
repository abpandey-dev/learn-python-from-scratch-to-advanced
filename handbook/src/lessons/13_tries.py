from lib import *

LESSON("Basics", "Why tries exist", """
<p>Suppose you store 100,000 words and the user types "app". To list words starting with "app", a set or list must check <b>every</b> word. Sorting helps a little. A <b>trie</b> answers in time proportional to the length of "app" — independent of how many words you stored.</p>
<p>It does this by storing words <b>letter by letter</b> in a tree. Words with the same beginning share the same path:</p>
<div class="pic">root
 └ a
   └ p
     └ p ◎          "app" ends here
       └ l
         ├ e ◎      "apple"
         └ y ◎      "apply"</div>
<p>Each node is just "a dict of children + a flag that says a word ends here".</p>
""")


LESSON("Core", "Building insert, search and startsWith", """
<pre><code class="py">class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.end = True

    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.end     # path AND end flag

    def startsWith(self, prefix):
        return self._walk(prefix) is not None    # path only</code></pre>
<p>Every operation is O(L), L = length of the word. Memory is up to the total number of letters inserted.</p>
<div class="tip">In Python, nested dicts are a shorter trie: <code>node = node.setdefault(ch, {})</code>, and <code>node["$"] = True</code> marks a word end.</div>
""", practice=[208, 14, 2185])


@LD
def search_vs_prefix():
    root = {}
    for w in ["car", "card", "care", "cat"]:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = True
    T("Trie of car, card, care, cat (◎ = word ends)", TRIE("trie", root))
    for q in ["car", "ca", "cap"]:
        node, path = root, []
        for ch in q:
            if ch not in node:
                node = None
                break
            node = node[ch]
            path.append(node)
        found = node is not None and "$" in node
        T(f"'{q}': path {'exists' if node is not None else 'breaks'}; search → {found}, startsWith → {node is not None}", TRIE("trie", root, ok=path if found else [], hl=path if not found else []))
    return root


LESSON("Core", "Storing extra data on nodes", """
<p>A node can hold more than a flag. Choose what to store from what the question asks:</p>
<table>
<tr><th>Store on each node</th><th>Answers</th></tr>
<tr><td>count of words passing through</td><td>"how many words start with p", prefix scores</td></tr>
<tr><td>running total of values</td><td>map sum pairs</td></tr>
<tr><td>the first 3 words (inserted in sorted order)</td><td>search suggestions / autocomplete</td></tr>
<tr><td>the full word at its end node</td><td>word search II, longest word, replace words</td></tr>
<tr><td>largest index</td><td>prefix and suffix search</td></tr>
</table>
<p>Then a query is a single walk down the prefix, reading what's stored — no further search.</p>
""", practice=[2416, 677, 1268, 648, 720])


LESSON("Core", "Tries + DFS", """
<p>Because a trie is a tree, you can DFS it, and you can DFS <b>something else</b> (a grid, a string) while walking the trie at the same time.</p>
<ul>
<li><b>Wildcard search</b> ('.' matches anything): at a '.', try every child.</li>
<li><b>Word Search II</b>: put all words in a trie, DFS the grid once; each grid step moves one level down the trie, and you stop the moment the current letters aren't a prefix of any word. Much faster than searching each word separately.</li>
<li><b>Concatenated words / word break</b>: from position i, walk the trie; every end flag is a possible place to cut and recurse.</li>
</ul>
<div class="tip">In Word Search II remove (or mark) a word once found, and delete trie branches that become empty — it prunes later searches.</div>
""", practice=[211, 212, 472])


LESSON("Advanced", "Reversed tries and binary tries", """
<h4>Suffix questions → reverse the words</h4>
<p>A trie built from <b>reversed</b> words answers "does the stream end with a word?" (stream of characters) and "which words are suffixes of others?" (short encoding).</p>
<h4>Binary trie for XOR</h4>
<p>Insert each number's bits from the highest bit down, so the trie has only 0/1 children. To maximise <code>x XOR y</code>, walk the trie for x and at each bit take the <b>opposite</b> child if it exists — a 1 in a high bit beats everything below it. O(B) per query, B = number of bits.</p>
<p>With limits (only numbers ≤ m), sort numbers and queries and insert numbers as the limit grows — an <b>offline</b> query trick.</p>
""", practice=[1032, 820, 745, 421, 1707])


@LD
def binary_trie_lesson():
    nums = [3, 10, 5]
    B = 4
    root = {}
    for x in nums:
        node = root
        for b in range(B - 1, -1, -1):
            node = node.setdefault((x >> b) & 1, {})
        T(f"Insert {x} = {x:04b} bit by bit (high → low)", BITS("x", x, B), TRIE("binary trie", root), at="prev")
    x, node, cur, path = 5, root, 0, []
    for b in range(B - 1, -1, -1):
        bit = (x >> b) & 1
        if 1 - bit in node:
            cur |= 1 << b
            node = node[1 - bit]
        else:
            node = node[bit]
        path.append(node)
        T(f"Bit {b} of {x} is {bit}: prefer the opposite branch → XOR so far {cur}", BITS("x", x, B, hl=[b]), TRIE("binary trie", root, ok=path), at="prev")
    return cur


LESSON("Advanced", "Implicit tries", """
<p>Sometimes the trie is never built. The numbers 1..n in <b>lexicographic</b> (dictionary) order are a preorder walk of a digit trie where the children of x are 10x … 10x + 9.</p>
<ul>
<li><b>Lexicographical numbers</b>: walk that tree with arithmetic — go down (×10) if possible, else go to the next sibling (+1), climbing up past 9s.</li>
<li><b>k-th lexicographical number</b>: count how many numbers ≤ n are in the subtree of a prefix (level by level). If the count fits in k, skip the whole subtree; otherwise go down. O(log² n).</li>
</ul>
<p>Folder paths are also a trie of parts (<code>/a/b/c</code> → a → b → c): remove sub-folders by stopping at the first folder end.</p>
""", practice=[386, 440, 1233])
