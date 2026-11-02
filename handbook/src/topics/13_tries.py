from lib import *

TOPIC(
    id="tries", title="Tries", glyph="a→p→p",
    blurb="Prefix trees: share common prefixes so insert, search and 'starts with' cost O(length of the word).",
    demo_title="Inserting words into a trie: shared prefixes share nodes",
    theory="""
<h3>What it is</h3>
<p>A <b>trie</b> (prefix tree) stores strings character by character. Each node has up to one child per possible next character, and a flag marking "a word ends here". Words that share a prefix share the same path, so <code>"app"</code>, <code>"apple"</code> and <code>"apply"</code> use one chain of nodes for <code>a → p → p</code>.</p>
<pre><code class="py">class TrieNode:
    def __init__(self):
        self.children = {}   # char -> TrieNode
        self.end = False     # a word ends at this node</code></pre>
<p>In Python you can also use nested dicts: <code>node = node.setdefault(ch, {})</code> and mark word ends with a special key such as <code>"$"</code>.</p>
<h3>Costs (L = word length)</h3>
<table>
<tr><th>Operation</th><th>Trie</th><th>Hash set of words</th><th>Sorted list</th></tr>
<tr><td>Insert a word</td><td>O(L)</td><td>O(L)</td><td>O(n) shift</td></tr>
<tr><td>Exact search</td><td>O(L)</td><td>O(L)</td><td>O(L log n)</td></tr>
<tr><td>Any word with prefix p?</td><td><b>O(|p|)</b></td><td>O(n · |p|)</td><td>O(|p| log n)</td></tr>
<tr><td>All words with prefix p</td><td>O(|p| + output)</td><td>O(n · L)</td><td>O(|p| log n + output)</td></tr>
</table>
<h3>Spot the pattern</h3>
<ul>
<li>Many lookups by <b>prefix</b>: autocomplete, search suggestions, "starts with", replace with the shortest root.</li>
<li><b>Many words at once</b> on a grid or a stream (Word Search II, Stream of Characters): one trie lets a single search follow all words together and stop as soon as no word matches.</li>
<li>Suffix questions → build the trie from <b>reversed</b> words.</li>
<li>Maximum XOR → a <b>binary trie</b> of numbers' bits, from the highest bit down; at each bit try to go the opposite way.</li>
<li>Wildcards like <code>.</code> → DFS into every child at that position.</li>
</ul>
<h3>Template</h3>
<pre><code class="py">root = {}
def insert(word):
    node = root
    for ch in word:
        node = node.setdefault(ch, {})
    node["$"] = True

def starts_with(prefix):
    node = root
    for ch in prefix:
        if ch not in node:
            return False
        node = node[ch]
    return True</code></pre>
<h3>Common mistakes</h3>
<ul>
<li>Treating "the path exists" as "the word exists" — you must check the end flag.</li>
<li>Forgetting to remove or mark found words in Word Search II, so the same word is reported twice.</li>
<li>Memory: a trie of n words can have up to total-length nodes. Store a small counter or word on the node instead of copying lists.</li>
</ul>
""")


@D
def trie_demo():
    root = {}
    for w in ["app", "apple", "apt", "bat"]:
        node, path = root, []
        for ch in w:
            node = node.setdefault(ch, {})
            path.append(node)
        node["$"] = True
        T(f"Insert '{w}' — ◎ marks where a word ends", TRIE("trie", root, hl=path), at="prev")
    node, path = root, []
    for ch in "ap":
        node = node[ch]
        path.append(node)
    T("Prefix 'ap' exists → 'app', 'apple' and 'apt' all start with it", TRIE("trie", root, ok=path))
    return root


# 1 ---------------------------------------------------------------
Q(208, "Implement Trie (Prefix Tree)", "Medium", "Trie node class",
  "Implement <code>insert(word)</code>, <code>search(word)</code> (exact match) and <code>startsWith(prefix)</code>.",
  [(((), [("insert", ("apple",)), ("search", ("apple",)), ("search", ("app",)), ("startsWith", ("app",)), ("insert", ("app",)), ("search", ("app",))]), [None, True, False, True, None, True])],
  ("Keep a list of words; search and startsWith scan every word.", "O(n · L) per query", "O(total length)"),
  ("A tree of nodes, one edge per character. Walk or create one node per character; the end flag separates full words from prefixes.", "O(L) per operation", "O(total length)"),
  design=True, viz=((), [("insert", ("car",)), ("insert", ("cat",)), ("insert", ("can",)), ("search", ("ca",)), ("startsWith", ("ca",)), ("search", ("cat",))]))


@B
class Trie:
    def __init__(self):
        self.words = []

    def insert(self, word):
        self.words.append(word)

    def search(self, word):
        return word in self.words

    def startsWith(self, prefix):
        return any(w.startswith(prefix) for w in self.words)


@O
class Trie:
    class Node:
        def __init__(self):
            self.children, self.end = {}, False

    def __init__(self):
        self.root = self.Node()

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, self.Node())
        node.end = True
        T(f"insert('{word}')", TRIE("trie", self.root, hl=[node]), at="prev")

    def _walk(self, s):
        node, path = self.root, []
        for ch in s:
            if ch not in node.children:
                return None, path
            node = node.children[ch]
            path.append(node)
        return node, path

    def search(self, word):
        node, path = self._walk(word)
        T(f"search('{word}') → path {'found' if node else 'missing'}, end flag {bool(node and node.end)}", TRIE("trie", self.root, ok=path if node and node.end else [], hl=path if not (node and node.end) else []))
        return bool(node and node.end)

    def startsWith(self, prefix):
        node, path = self._walk(prefix)
        T(f"startsWith('{prefix}') → {node is not None}", TRIE("trie", self.root, ok=path if node else [], hl=path if not node else []))
        return node is not None


# 2 ---------------------------------------------------------------
Q(211, "Design Add and Search Words Data Structure", "Medium", "Trie + DFS on '.'",
  "Support <code>addWord(word)</code> and <code>search(word)</code>, where '.' in the search matches any single letter.",
  [(((), [("addWord", ("bad",)), ("addWord", ("dad",)), ("addWord", ("mad",)), ("search", ("pad",)), ("search", ("bad",)), ("search", (".ad",)), ("search", ("b..",))]), [None, None, None, False, True, True, True])],
  ("Store words in a list; compare every word of the same length letter by letter.", "O(n · L) per search", "O(total length)"),
  ("Store words in a trie. Normal letters follow one edge; '.' tries every child with DFS. Paths that don't exist are dropped immediately.", "O(L) without dots, O(26^dots · L) worst", "O(total length)"),
  design=True)


@B
class WordDictionary:
    def __init__(self):
        self.words = []

    def addWord(self, word):
        self.words.append(word)

    def search(self, word):
        return any(len(w) == len(word) and all(p in (".", c) for p, c in zip(word, w)) for w in self.words)


@O
class WordDictionary:
    def __init__(self):
        self.root = {}

    def addWord(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def search(self, word):
        hits = []

        def dfs(node, i, path):
            if i == len(word):
                if "$" in node:
                    hits.append(path)
                return "$" in node
            ch = word[i]
            if ch == ".":
                return any(dfs(child, i + 1, path + [child]) for k, child in node.items() if k != "$")
            return ch in node and dfs(node[ch], i + 1, path + [node[ch]])

        found = dfs(self.root, 0, [])
        T(f"search('{word}') → {found}", TRIE("trie", self.root, ok=hits[0] if hits else []))
        return found


# 3 ---------------------------------------------------------------
Q(212, "Word Search II", "Hard", "Trie-guided grid DFS",
  "Return every word from <code>words</code> that can be traced on the board through adjacent cells (each cell used once per word).",
  [(([["o", "a", "a", "n"], ["e", "t", "a", "e"], ["i", "h", "k", "r"], ["i", "f", "l", "v"]], ["oath", "pea", "eat", "rain"]), ["eat", "oath"]),
   (([["a", "b"], ["c", "d"]], ["abcb"]), [])],
  ("Run the single-word Word Search DFS separately for every word.", "O(W · m·n · 4ᴸ)", "O(L)"),
  ("Put all words in a trie. DFS once from each cell, moving down the trie as you go; stop the moment the path is not a prefix of any word. Remove words once found.", "O(m·n · 4ᴸ) but pruned by the trie", "O(total length)"),
  norm=sorted)


@B
def find_words(board, words):
    m, n = len(board), len(board[0])

    def exists(word):
        def dfs(r, c, i):
            if i == len(word):
                return True
            if not (0 <= r < m and 0 <= c < n) or board[r][c] != word[i]:
                return False
            ch, board[r][c] = board[r][c], "#"
            ok = any(dfs(r + dr, c + dc, i + 1) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            board[r][c] = ch
            return ok
        return any(dfs(r, c, 0) for r in range(m) for c in range(n))
    return [w for w in words if exists(w)]


@O
def find_words(board, words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = w
    m, n = len(board), len(board[0])
    found, path = [], []

    def dfs(r, c, parent):
        ch = board[r][c]
        node = parent.get(ch)
        if node is None:
            return
        path.append((r, c))
        if "$" in node:
            found.append(node.pop("$"))
            T(f"Found '{found[-1]}'", G("board", board, ok=path), V(found=found))
        board[r][c] = "#"
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and board[nr][nc] in node:
                dfs(nr, nc, node)
        board[r][c] = ch
        path.pop()
        if not node:
            parent.pop(ch)

    for r in range(m):
        for c in range(n):
            if board[r][c] in root:
                T(f"Start DFS at ({r},{c}) = '{board[r][c]}' — a first letter of some word", G("board", board, hl=[(r, c)]), V(found=found))
                dfs(r, c, root)
    return found


# 4 ---------------------------------------------------------------
Q(14, "Longest Common Prefix", "Easy", "Walk the single-child chain",
  "Return the longest common prefix of all strings, or <code>\"\"</code>.",
  [((["flower", "flow", "flight"],), "fl"), ((["dog", "racecar", "car"],), ""), ((["ab", "a"],), "a")],
  ("For every prefix length of the first word, test it against all words with startswith.", "O(m² · n)", "O(1)"),
  ("Insert every word into a trie, then walk from the root while the node has exactly one child and no word ends there.", "O(total length)", "O(total length)"))


@B
def longest_common_prefix(strs):
    best = ""
    for k in range(1, len(strs[0]) + 1):
        if all(s.startswith(strs[0][:k]) for s in strs):
            best = strs[0][:k]
    return best


@O
def longest_common_prefix(strs):
    root = {}
    for w in strs:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = True
    prefix, node, path = [], root, []
    while len(node) == 1 and "$" not in node:
        ch = next(iter(node))
        prefix.append(ch)
        node = node[ch]
        path.append(node)
    T(f"Walk while there is one branch and no word ends: '{''.join(prefix)}'", TRIE("trie", root, ok=path))
    return "".join(prefix)


# 5 ---------------------------------------------------------------
Q(648, "Replace Words", "Medium", "Shortest root in a trie",
  "Replace each word in <code>sentence</code> with the shortest root from <code>dictionary</code> that is its prefix.",
  [((["cat", "bat", "rat"], "the cattle was rattled by the battery"), "the cat was rat by the bat"), ((["a", "b", "c"], "aadsfasf absbs bbab cadsfafs"), "a a b c")],
  ("For every word, test every root with startswith and keep the shortest match.", "O(W · R · L)", "O(1)"),
  ("Insert roots into a trie. For each word, walk the trie letter by letter and stop at the first end flag — that's the shortest root.", "O(total length)", "O(roots' length)"))


@B
def replace_words(dictionary, sentence):
    out = []
    for w in sentence.split():
        roots = [r for r in dictionary if w.startswith(r)]
        out.append(min(roots, key=len) if roots else w)
    return " ".join(out)


@O
def replace_words(dictionary, sentence):
    root = {}
    for r in dictionary:
        node = root
        for ch in r:
            node = node.setdefault(ch, {})
        node["$"] = True
    out = []
    for w in sentence.split():
        node, path, rep = root, [], w
        for i, ch in enumerate(w):
            if ch not in node:
                break
            node = node[ch]
            path.append(node)
            if "$" in node:
                rep = w[:i + 1]
                break
        out.append(rep)
        T(f"'{w}' → '{rep}'", TRIE("roots", root, ok=path if rep != w else [], hl=path if rep == w else []), V(sentence=" ".join(out)), at="prev")
    return " ".join(out)


# 6 ---------------------------------------------------------------
Q(720, "Longest Word in Dictionary", "Medium", "DFS through end nodes only",
  "Return the longest word that can be built one letter at a time from other words in the list (ties → smallest lexicographically).",
  [((["w", "wo", "wor", "worl", "world"],), "world"), ((["a", "banana", "app", "appl", "ap", "apply", "apple"],), "apple")],
  ("For each word, check that every prefix is in a set.", "O(Σ L²)", "O(total length)"),
  ("Build a trie storing each word at its end node. DFS from the root but only step into children that end a word; the deepest (then smallest) word reached wins.", "O(total length)", "O(total length)"))


@B
def longest_word(words):
    s, best = set(words), ""
    for w in words:
        if all(w[:k] in s for k in range(1, len(w))):
            if len(w) > len(best) or (len(w) == len(best) and w < best):
                best = w
    return best


@O
def longest_word(words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = w
    best = ""

    def dfs(node, path):
        nonlocal best
        for ch in sorted(k for k in node if k != "$"):
            child = node[ch]
            if "$" in child:
                w = child["$"]
                if len(w) > len(best):
                    best = w
                    T(f"'{w}' can be built letter by letter → new best", TRIE("trie", root, ok=path + [child]), V(best=best))
                dfs(child, path + [child])

    dfs(root, [])
    return best


# 7 ---------------------------------------------------------------
Q(1268, "Search Suggestions System", "Medium", "Trie nodes keep top 3",
  "After each typed character of <code>searchWord</code>, return up to 3 lexicographically smallest products with that prefix.",
  [((["mobile", "mouse", "moneypot", "monitor", "mousepad"], "mouse"), [["mobile", "moneypot", "monitor"], ["mobile", "moneypot", "monitor"], ["mouse", "mousepad"], ["mouse", "mousepad"], ["mouse", "mousepad"]]),
   ((["havana"], "tatiana"), [[], [], [], [], [], [], []])],
  ("For each prefix, filter all products and sort them.", "O(L · n log n)", "O(n)"),
  ("Sort products, then insert them into a trie; each node keeps the first 3 products passing through it (they arrive in sorted order). Each keystroke is one step down the trie.", "O(n log n + total length)", "O(total length)"),
  viz=(["bags", "baggage", "banner", "box", "cloths"], "bags"))


@B
def suggested_products(products, search_word):
    res = []
    for k in range(1, len(search_word) + 1):
        p = search_word[:k]
        res.append(sorted(x for x in products if x.startswith(p))[:3])
    return res


@O
def suggested_products(products, search_word):
    root = {}
    for p in sorted(products):
        node = root
        for ch in p:
            node = node.setdefault(ch, {})
            node.setdefault("#", [])
            if len(node["#"]) < 3:
                node["#"].append(p)
    res, node = [], root
    for i, ch in enumerate(search_word):
        node = node.get(ch, {}) if node is not None else {}
        res.append(node.get("#", []))
        T(f"Typed '{search_word[:i + 1]}' → {res[-1]}", A("searchWord", search_word, ok=range(i + 1)), V(suggestions=res[-1]), at="prev")
    return res


# 8 ---------------------------------------------------------------
Q(421, "Maximum XOR of Two Numbers in an Array", "Medium", "Binary trie, greedy opposite bit",
  "Return the maximum of <code>nums[i] XOR nums[j]</code>.",
  [(([3, 10, 5, 25, 2, 8],), 28), (([14, 70, 53, 83, 49, 91, 36, 80, 92, 51, 66, 70],), 127)],
  ("XOR every pair.", "O(n²)", "O(1)"),
  ("Insert each number's bits (high to low) into a binary trie. For a number x, walk down choosing the opposite bit whenever it exists — each such bit adds 2^b to the XOR.", "O(n · B)", "O(n · B)"),
  viz=([3, 10, 5, 25],))


@B
def find_maximum_xor(nums):
    return max(a ^ b for a in nums for b in nums)


@O
def find_maximum_xor(nums):
    B = max(nums).bit_length()
    root = {}
    for x in nums:
        node = root
        for b in range(B - 1, -1, -1):
            node = node.setdefault((x >> b) & 1, {})
    best = 0
    for x in nums:
        node, cur, path = root, 0, []
        for b in range(B - 1, -1, -1):
            bit = (x >> b) & 1
            if 1 - bit in node:
                cur |= 1 << b
                node = node[1 - bit]
            else:
                node = node[bit]
            path.append(node)
        best = max(best, cur)
        T(f"Best partner for {x} gives XOR {cur}", BITS("x", x, B), TRIE("binary trie (high bit → low)", root, ok=path), V(xor=cur, best=best), at="prev")
    return best


# 9 ---------------------------------------------------------------
Q(677, "Map Sum Pairs", "Medium", "Trie with prefix totals",
  "<code>insert(key, val)</code> sets a key's value (overwriting). <code>sum(prefix)</code> returns the total value of keys starting with prefix.",
  [(((), [("insert", ("apple", 3)), ("sum", ("ap",)), ("insert", ("app", 2)), ("sum", ("ap",)), ("insert", ("apple", 2)), ("sum", ("ap",))]), [None, 3, None, 5, None, 4])],
  ("Keep a dict; sum scans every key with startswith.", "sum O(n · L)", "O(n · L)"),
  ("Each trie node stores the total of all keys below it. On insert, add the change (new − old value) to every node on the path; sum is one walk to the prefix node.", "O(L) per operation", "O(total length)"),
  design=True)


@B
class MapSum:
    def __init__(self):
        self.vals = {}

    def insert(self, key, val):
        self.vals[key] = val

    def sum(self, prefix):
        return sum(v for k, v in self.vals.items() if k.startswith(prefix))


@O
class MapSum:
    def __init__(self):
        self.root, self.vals = {"#": 0}, {}

    def insert(self, key, val):
        delta = val - self.vals.get(key, 0)
        self.vals[key] = val
        node = self.root
        for ch in key:
            node = node.setdefault(ch, {"#": 0})
            node["#"] += delta
        T(f"insert('{key}', {val}): add {delta:+d} along the path", M("values", self.vals, hl=key), at="prev")

    def sum(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node:
                return 0
            node = node[ch]
        T(f"sum('{prefix}') = total stored at the prefix node = {node['#']}", M("values", self.vals))
        return node["#"]


# 10 --------------------------------------------------------------
Q(745, "Prefix and Suffix Search", "Hard", "Trie of 'suffix#word'",
  "<code>WordFilter(words)</code>; <code>f(pref, suff)</code> returns the largest index of a word with that prefix and suffix, or −1.",
  [(((["apple"],), [("f", ("a", "e"))]), [0]), (((["apple", "ape", "apply"],), [("f", ("ap", "e")), ("f", ("ap", "y")), ("f", ("b", ""))]), [1, 2, -1])],
  ("For each query, scan words from the end and check startswith and endswith.", "O(n · L) per query", "O(1)"),
  ("For every word and every suffix s of it, insert s + '#' + word into one trie, storing the word's index on each node (later words overwrite). A query is one walk of suff + '#' + pref.", "O(n · L²) build, O(L) query", "O(n · L²)"),
  design=True)


@B
class WordFilter:
    def __init__(self, words):
        self.words = words

    def f(self, pref, suff):
        for i in range(len(self.words) - 1, -1, -1):
            if self.words[i].startswith(pref) and self.words[i].endswith(suff):
                return i
        return -1


@O
class WordFilter:
    def __init__(self, words):
        self.root = {}
        for i, w in enumerate(words):
            for k in range(len(w) + 1):
                node = self.root
                for ch in w[k:] + "#" + w:
                    node = node.setdefault(ch, {})
                    node["i"] = i
        T(f"Inserted every 'suffix#word' key for {len(words)} word(s)", A("keys for the last word", [w[k:] + "#" + w for k in range(len(w) + 1)]))

    def f(self, pref, suff):
        node = self.root
        for ch in suff + "#" + pref:
            if ch not in node:
                T(f"f('{pref}', '{suff}'): key '{suff}#{pref}' not in the trie → -1", V(key=suff + "#" + pref))
                return -1
            node = node[ch]
        T(f"f('{pref}', '{suff}'): walk '{suff}#{pref}' → index {node['i']}", V(key=suff + "#" + pref, index=node["i"]))
        return node["i"]


# 11 --------------------------------------------------------------
Q(1032, "Stream of Characters", "Hard", "Trie of reversed words",
  "<code>StreamChecker(words)</code>; each <code>query(letter)</code> returns whether some suffix of the letters seen so far is a word.",
  [(((["cd", "f", "kl"],), [("query", (c,)) for c in "abcdefghijkl"]), [False, False, False, True, False, True, False, False, False, False, False, True])],
  ("Keep the stream; on each query test every word with endswith.", "O(W · L) per query", "O(stream)"),
  ("Insert words reversed. On each query, walk the trie from the newest letter backwards; reaching an end flag means a word just finished. Only the last maxLen letters matter.", "O(L) per query", "O(total length)"),
  design=True, viz=(((["cd", "f", "kl"],), [("query", (c,)) for c in "acdfkl"])))


@B
class StreamChecker:
    def __init__(self, words):
        self.words, self.stream = words, ""

    def query(self, letter):
        self.stream += letter
        return any(self.stream.endswith(w) for w in self.words)


@O
class StreamChecker:
    def __init__(self, words):
        from collections import deque
        self.root = {}
        for w in words:
            node = self.root
            for ch in reversed(w):
                node = node.setdefault(ch, {})
            node["$"] = True
        self.recent = deque(maxlen=max(map(len, words)))

    def query(self, letter):
        self.recent.appendleft(letter)
        node, path = self.root, []
        for ch in self.recent:
            if ch not in node:
                break
            node = node[ch]
            path.append(node)
            if "$" in node:
                T(f"query('{letter}'): newest letters spell a word backwards → True", A("recent (newest first)", list(self.recent), ok=range(len(path))), TRIE("reversed words", self.root, ok=path))
                return True
        T(f"query('{letter}') → False", A("recent (newest first)", list(self.recent)), TRIE("reversed words", self.root, hl=path))
        return False


# 12 --------------------------------------------------------------
Q(472, "Concatenated Words", "Hard", "Trie + word-break DFS",
  "Return every word that is made of at least two shorter words from the list.",
  [((["cat", "cats", "catsdogcats", "dog", "dogcatsdog", "hippopotamuses", "rat", "ratcatdogcat"],), ["catsdogcats", "dogcatsdog", "ratcatdogcat"]), ((["cat", "dog", "catdog"],), ["catdog"])],
  ("For each word, try every way to split it into dictionary pieces (no memo).", "O(n · 2ᴸ)", "O(L)"),
  ("Put all words in a trie. For a word, walk the trie from position i; at every end flag, recurse from the next position. Memoise positions, and require at least two pieces.", "O(n · L²)", "O(total length)"),
  norm=sorted, viz=(["cat", "dog", "cats", "catsdog", "dogcat"],))


@B
def find_all_concatenated_words(words):
    s = set(words)

    def split(w, first):
        for k in range(1, len(w) + 1):
            if w[:k] in s and (k < len(w) or not first) and (k == len(w) or split(w[k:], False)):
                if not (first and k == len(w)):
                    return True
        return False
    return [w for w in words if w and split(w, True)]


@O
def find_all_concatenated_words(words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = True
    res = []
    for w in words:
        memo = {}

        def can(i, pieces):
            if i == len(w):
                return pieces >= 2
            if (i, pieces >= 1) in memo:
                return memo[(i, pieces >= 1)]
            node, ok = root, False
            for j in range(i, len(w)):
                node = node.get(w[j])
                if node is None:
                    break
                if "$" in node and can(j + 1, pieces + 1):
                    ok = True
                    break
            memo[(i, pieces >= 1)] = ok
            return ok

        if w and can(0, 0):
            res.append(w)
        T(f"'{w}' {'is' if res and res[-1] == w else 'is not'} built from shorter words", A("words", words, ok=[words.index(x) for x in res], hl=[words.index(w)]), V(result=res), at="prev")
    return res


# 13 --------------------------------------------------------------
Q(336, "Palindrome Pairs", "Hard", "Split each word, look up the reverse",
  "Return all pairs [i, j] (i ≠ j) such that <code>words[i] + words[j]</code> is a palindrome.",
  [((["abcd", "dcba", "lls", "s", "sssll"],), [[0, 1], [1, 0], [3, 2], [2, 4]]), ((["bat", "tab", "cat"],), [[0, 1], [1, 0]]), ((["a", ""],), [[0, 1], [1, 0]])],
  ("Concatenate every ordered pair and test it.", "O(n² · k)", "O(k)"),
  ("Split each word w into prefix + suffix at every position. If the prefix is a palindrome, reversed(suffix) placed before w works; if the suffix is a palindrome, reversed(prefix) placed after w works. Look the reverses up in a word → index map (a trie of reversed words gives the same bound).", "O(n · k²)", "O(n · k)"),
  norm=sorted)


@B
def palindrome_pairs(words):
    return [[i, j] for i in range(len(words)) for j in range(len(words)) if i != j and (words[i] + words[j]) == (words[i] + words[j])[::-1]]


@O
def palindrome_pairs(words):
    index = {w: i for i, w in enumerate(words)}
    res = []
    for i, w in enumerate(words):
        for j in range(len(w) + 1):
            pre, suf = w[:j], w[j:]
            if pre == pre[::-1] and suf[::-1] in index and index[suf[::-1]] != i:
                res.append([index[suf[::-1]], i])
                T(f"'{w}' = '{pre}' + '{suf}': '{pre}' is a palindrome, so '{suf[::-1]}' + '{w}' works", A("words", words, hl=[i], ok=[index[suf[::-1]]]), V(pairs=res))
            if j != len(w) and suf == suf[::-1] and pre[::-1] in index and index[pre[::-1]] != i:
                res.append([i, index[pre[::-1]]])
                T(f"'{w}' = '{pre}' + '{suf}': '{suf}' is a palindrome, so '{w}' + '{pre[::-1]}' works", A("words", words, hl=[i], ok=[index[pre[::-1]]]), V(pairs=res))
    return res


# 14 --------------------------------------------------------------
Q(1707, "Maximum XOR With an Element From Array", "Hard", "Offline queries + binary trie",
  "For each query [x, m], return the max of x XOR nums[j] over nums[j] ≤ m, or −1 if none.",
  [(([0, 1, 2, 3, 4], [[3, 1], [1, 3], [5, 6]]), [3, 3, 7]), (([5, 2, 4, 6, 6, 3], [[12, 4], [8, 1], [6, 3]]), [15, -1, 5])],
  ("For each query, scan every allowed number.", "O(n · q)", "O(1)"),
  ("Sort nums and sort queries by m. Before answering a query, insert every number ≤ m into a binary trie, then walk greedily toward opposite bits.", "O((n + q) · B + sorting)", "O(n · B)"))


@B
def maximize_xor(nums, queries):
    res = []
    for x, m in queries:
        ok = [x ^ v for v in nums if v <= m]
        res.append(max(ok) if ok else -1)
    return res


@O
def maximize_xor(nums, queries):
    nums = sorted(nums)
    B = max(max(nums), max(x for x, _ in queries)).bit_length()
    order = sorted(range(len(queries)), key=lambda q: queries[q][1])
    root, k, res = {}, 0, [-1] * len(queries)
    for qi in order:
        x, m = queries[qi]
        while k < len(nums) and nums[k] <= m:
            node = root
            for b in range(B - 1, -1, -1):
                node = node.setdefault((nums[k] >> b) & 1, {})
            k += 1
        if k:
            node, cur = root, 0
            for b in range(B - 1, -1, -1):
                bit = (x >> b) & 1
                if 1 - bit in node:
                    cur |= 1 << b
                    node = node[1 - bit]
                else:
                    node = node[bit]
            res[qi] = cur
        T(f"Query x = {x}, m = {m}: trie holds nums ≤ {m} → answer {res[qi]}", A("nums (sorted)", nums, ok=range(k)), TRIE("binary trie", root), A("answers", res, hl=[qi]), at="prev")
    return res


# 15 --------------------------------------------------------------
Q(2416, "Sum of Prefix Scores of Strings", "Hard", "Trie with pass counts",
  "The score of a string is how many words in the list start with it. For each word, return the sum of the scores of all its non-empty prefixes.",
  [((["abc", "ab", "bc", "b"],), [5, 4, 3, 2]), ((["abcd"],), [4])],
  ("For every prefix of every word, count words starting with it.", "O(n² · L²)", "O(1)"),
  ("Insert all words and count how many pass through each node. A word's answer is the sum of the counts along its path.", "O(total length)", "O(total length)"))


@B
def sum_prefix_scores(words):
    return [sum(sum(1 for x in words if x.startswith(w[:k])) for k in range(1, len(w) + 1)) for w in words]


@O
def sum_prefix_scores(words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {"#": 0})
            node["#"] += 1
    res = []
    for w in words:
        node, total, counts = root, 0, []
        for ch in w:
            node = node[ch]
            total += node["#"]
            counts.append(node["#"])
        res.append(total)
        T(f"'{w}': prefixes are shared by {counts} words → {total}", A("words", words, hl=[len(res) - 1]), A("answer", res, ok=[len(res) - 1]), at="prev")
    return res


# 16 --------------------------------------------------------------
Q(820, "Short Encoding of Words", "Medium", "Trie of reversed words, count leaves",
  "Encode words as one reference string like 'time#bell#' where each word is a suffix ending at a '#'. Return the shortest possible length.",
  [((["time", "me", "bell"],), 10), ((["t"],), 2)],
  ("Drop every word that is a suffix of another word (check all pairs); sum the rest with +1 each.", "O(n² · L)", "O(n)"),
  ("Insert reversed words into a trie. Only words ending at a leaf need their own '#'; the answer is Σ (depth + 1) over leaves.", "O(total length)", "O(total length)"))


@B
def minimum_length_encoding(words):
    s = set(words)
    keep = [w for w in s if not any(o != w and o.endswith(w) for o in s)]
    return sum(len(w) + 1 for w in keep)


@O
def minimum_length_encoding(words):
    root, ends = {}, {}
    for w in set(words):
        node = root
        for ch in reversed(w):
            node = node.setdefault(ch, {})
        ends[w] = node
    keep = [w for w, node in ends.items() if not node]
    T(f"Reversed-word trie: leaves are {sorted(keep)}", TRIE("reversed words", root, ok=[ends[w] for w in keep]), V(encoding="#".join(sorted(keep)) + "#"))
    return sum(len(w) + 1 for w in keep)


# 17 --------------------------------------------------------------
Q(386, "Lexicographical Numbers", "Medium", "Preorder walk of the digit trie",
  "Return 1..n in lexicographic order using O(n) time and O(1) extra space.",
  [((13,), [1, 10, 11, 12, 13, 2, 3, 4, 5, 6, 7, 8, 9]), ((2,), [1, 2])],
  ("Sort the numbers by their string form.", "O(n log n)", "O(n)"),
  ("The numbers form an implicit trie (children of x are 10x .. 10x + 9). Walk it in preorder: go to x · 10 if ≤ n; otherwise step to x + 1, climbing up while x ends in 9 or exceeds n.", "O(n)", "O(1)"),
  viz=(21,))


@B
def lexical_order(n):
    return sorted(range(1, n + 1), key=str)


@O
def lexical_order(n):
    res, x = [], 1
    for _ in range(n):
        res.append(x)
        if x * 10 <= n:
            x *= 10
            move = "go down to x × 10"
        else:
            while x % 10 == 9 or x + 1 > n:
                x //= 10
            x += 1
            move = "next sibling (climbing up if needed)"
        T(f"Output {res[-1]}, then {move} → {x}", A("result", res, ok=[len(res) - 1]), V(next=x), at="prev")
    return res


# 18 --------------------------------------------------------------
Q(440, "K-th Smallest in Lexicographical Order", "Hard", "Count subtree sizes, skip",
  "Return the k-th smallest number in lexicographic order among 1..n.",
  [((13, 2), 10), ((1, 1), 1), ((100, 10), 17)],
  ("Sort all numbers as strings and index.", "O(n log n)", "O(n)"),
  ("Stand on prefix p. Count how many numbers ≤ n start with p (level by level of the digit trie). If that's ≤ the remaining k, skip the whole subtree (p + 1); otherwise go down (p × 10).", "O(log² n)", "O(1)"))


@B
def find_kth_number(n, k):
    return int(sorted(map(str, range(1, n + 1)))[k - 1])


@O
def find_kth_number(n, k):
    def count(p):
        total, lo, hi = 0, p, p
        while lo <= n:
            total += min(hi, n) - lo + 1
            lo, hi = lo * 10, hi * 10 + 9
        return total

    cur, k = 1, k - 1
    while k:
        c = count(cur)
        T(f"Prefix {cur} has {c} number(s) ≤ {n}; {k} step(s) left", V(prefix=cur, subtree=c, k_left=k, action="skip subtree" if c <= k else "go down"))
        if c <= k:
            k -= c
            cur += 1
        else:
            k -= 1
            cur *= 10
    return cur


# 19 --------------------------------------------------------------
Q(1233, "Remove Sub-Folders from the Filesystem", "Medium", "Trie of path parts",
  "Remove every folder that is inside another folder in the list; return the rest.",
  [((["/a", "/a/b", "/c/d", "/c/d/e", "/c/f"],), ["/a", "/c/d", "/c/f"]), ((["/a", "/a/b/c", "/a/b/d"],), ["/a"]), ((["/a/b/c", "/a/b/ca", "/a/b/d"],), ["/a/b/c", "/a/b/ca", "/a/b/d"])],
  ("For each folder, check whether any other folder + '/' is its prefix.", "O(n² · L)", "O(1)"),
  ("Insert each folder's parts ('a', 'b', …) into a trie with an end flag. Then collect folders by DFS, stopping at the first end flag on each path.", "O(total length)", "O(total length)"),
  norm=sorted)


@B
def remove_subfolders(folder):
    return [f for f in folder if not any(g != f and f.startswith(g + "/") for g in folder)]


@O
def remove_subfolders(folder):
    root = {}
    for f in folder:
        node = root
        for part in f.split("/")[1:]:
            node = node.setdefault(part, {})
        node["$"] = True
    res = []

    def dfs(node, path):
        if "$" in node:
            res.append("/" + "/".join(path))
            return
        for part in node:
            dfs(node[part], path + [part])

    dfs(root, [])
    T("Folders are trie paths; stop at the first folder end on each path", TRIE("folder trie", root), A("kept", res))
    return res


# 20 --------------------------------------------------------------
Q(2185, "Counting Words With a Given Prefix", "Easy", "Trie with counts",
  "Return how many words in <code>words</code> start with <code>pref</code>.",
  [((["pay", "attention", "practice", "attend"], "at"), 2), ((["leetcode", "win", "loops", "success"], "code"), 0)],
  ("Call startswith on every word.", "O(n · |pref|)", "O(1)"),
  ("Build a trie with a pass count on every node, then walk the prefix and read the count. For one query this equals the scan; it wins when you answer many prefix queries.", "O(total length) build, O(|pref|) per query", "O(total length)"))


@B
def prefix_count(words, pref):
    return sum(w.startswith(pref) for w in words)


@O
def prefix_count(words, pref):
    root = {"#": 0}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {"#": 0})
            node["#"] += 1
    node, path = root, []
    for ch in pref:
        if ch not in node:
            T(f"'{pref}' leaves the trie → 0", A("pref", pref))
            return 0
        node = node[ch]
        path.append(node)
    T(f"{node['#']} word(s) pass through the node for '{pref}'", TRIE("trie", root, ok=path), V(count=node["#"]))
    return node["#"]
