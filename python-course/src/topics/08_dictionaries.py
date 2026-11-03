from lib import *

TOPIC(
    id="dictionaries", title="Dictionaries", glyph="{k: v}",
    blurb="Key → value maps: lookups, updates, counting, grouping, nesting and dict comprehensions.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">ages = {"ana": 21, "ben": 25}
ages["cy"] = 30               # add / update
ages["ana"]                   # 21 (KeyError if missing)
ages.get("zed", 0)            # 0 — default instead of an error
del ages["ben"]; ages.pop("cy", None)
for name, age in ages.items(): ...
counts[x] = counts.get(x, 0) + 1          # counting
groups.setdefault(key, []).append(item)  # grouping
{k: v for k, v in pairs if v &gt; 0}       # dict comprehension
from collections import Counter, defaultdict</code></pre>
<ul><li>Keys must be unique and hashable; values can be anything.</li><li>Dicts remember insertion order (Python 3.7+).</li></ul>
""")


Q(None, "Word Frequency", "Easy", "Counting with a dict",
  "Return a dict mapping each word (lower-cased) to how many times it appears.",
  [(("the cat the hat",), {"the": 2, "cat": 1, "hat": 1}), (("",), {})],
  ("For each word, count it again with <code>list.count</code> (scans the whole list each time).", "O(n²)", "O(n)"),
  ("One pass: <code>counts[w] = counts.get(w, 0) + 1</code>.", "O(n)", "O(k)"),
  viz=("to be or not to be",))


@B
def word_freq(text):
    words = text.lower().split()
    result = {}
    for w in words:
        result[w] = words.count(w)
    return result


@O
def word_freq(text):
    counts = {}
    for w in text.lower().split():
        counts[w] = counts.get(w, 0) + 1
    return counts


Q(None, "Character Frequency", "Easy", "Counter",
  "Return a dict of character → count for the letters of <code>word</code>.",
  [(("hello",), {"h": 1, "e": 1, "l": 2, "o": 1}), (("",), {})],
  ("Check whether the key exists with <code>in</code> and branch.", "O(n)", "O(k)"),
  ("<code>collections.Counter</code> does the counting.", "O(n)", "O(k)"),
  viz=("hello",))


@B
def char_freq(word):
    counts = {}
    for ch in word:
        if ch in counts:
            counts[ch] = counts[ch] + 1
        else:
            counts[ch] = 1
    return counts


@O
def char_freq(word):
    from collections import Counter
    return dict(Counter(word))


Q(None, "Invert a Dictionary", "Easy", "Dict comprehension",
  "Swap keys and values (all values are unique).",
  [(({"a": 1, "b": 2},), {1: "a", 2: "b"}), (({},), {})],
  ("Loop over keys and look each value up.", "O(n)", "O(n)"),
  ("<code>{v: k for k, v in d.items()}</code>.", "O(n)", "O(n)"),
  viz=({"a": 1, "b": 2, "c": 3},))


@B
def invert(d):
    result = {}
    for key in d:
        value = d[key]
        result[value] = key
    return result


@O
def invert(d):
    return {v: k for k, v in d.items()}


Q(None, "Merge Dicts, Adding Values", "Medium", "Merging",
  "Merge two dicts of item → quantity; when a key is in both, add the quantities.",
  [(({"a": 1, "b": 2}, {"b": 3, "c": 4}), {"a": 1, "b": 5, "c": 4}), (({}, {"x": 1}), {"x": 1})],
  ("Copy the first dict, then for each key of the second check whether it exists.", "O(m + n)", "O(m + n)"),
  ("Copy, then <code>result[k] = result.get(k, 0) + v</code> — no branch needed. (<code>Counter(a) + Counter(b)</code> works too.)", "O(m + n)", "O(m + n)"),
  viz=({"a": 1, "b": 2}, {"b": 3, "c": 4}))


@B
def merge_add(a, b):
    result = {}
    for k in a:
        result[k] = a[k]
    for k in b:
        if k in result:
            result[k] = result[k] + b[k]
        else:
            result[k] = b[k]
    return result


@O
def merge_add(a, b):
    result = dict(a)
    for k, v in b.items():
        result[k] = result.get(k, 0) + v
    return result


Q(None, "Safe Lookup", "Easy", "get() with a default",
  "Return the price of <code>item</code> from the price dict, or 0 if it isn't there.",
  [(({"pen": 10, "ink": 25}, "ink"), 25), (({"pen": 10}, "cap"), 0)],
  ("Check with <code>in</code> first, then index.", "O(1)", "O(1)"),
  ("<code>prices.get(item, 0)</code>.", "O(1)", "O(1)"))


@B
def price_of(prices, item):
    if item in prices:
        return prices[item]
    else:
        return 0


@O
def price_of(prices, item):
    return prices.get(item, 0)


Q(None, "Group Words by First Letter", "Medium", "setdefault / defaultdict",
  "Return a dict mapping each first letter to the list of words starting with it, in original order.",
  [((["apple", "bat", "avocado", "ball"],), {"a": ["apple", "avocado"], "b": ["bat", "ball"]}), (([],), {})],
  ("Check if the key exists; create the list if not; then append.", "O(n)", "O(n)"),
  ("<code>groups.setdefault(key, []).append(word)</code> in one line.", "O(n)", "O(n)"),
  viz=(["apple", "bat", "avocado", "ball"],))


@B
def group_by_letter(words):
    groups = {}
    for w in words:
        first = w[0]
        if first not in groups:
            groups[first] = []
        groups[first].append(w)
    return groups


@O
def group_by_letter(words):
    groups = {}
    for w in words:
        groups.setdefault(w[0], []).append(w)
    return groups


Q(None, "Group Anagrams", "Medium", "Tuple / sorted keys",
  "Group words that are anagrams of each other. Return the groups as lists, in order of first appearance.",
  [((["eat", "tea", "tan", "ate", "nat", "bat"],), [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]), ((["a"],), [["a"]])],
  ("Compare each word with the first word of every existing group by sorting both.", "O(n² · k log k)", "O(n)"),
  ("Use the sorted letters as a dict key; all anagrams share it.", "O(n · k log k)", "O(n)"),
  viz=(["eat", "tea", "tan", "ate"],))


@B
def group_anagrams(words):
    groups = []
    for w in words:
        for g in groups:
            if sorted(g[0]) == sorted(w):
                g.append(w)
                break
        else:
            groups.append([w])
    return groups


@O
def group_anagrams(words):
    groups = {}
    for w in words:
        groups.setdefault("".join(sorted(w)), []).append(w)
    return list(groups.values())


Q(None, "Most Common Word", "Easy", "max with key",
  "Return the most frequent word (lower-cased). On a tie, return the one that appears first.",
  [(("Bob hit a ball the hit BALL flew",), "hit"), (("one",), "one")],
  ("Count every word with list.count and keep the best.", "O(n²)", "O(n)"),
  ("Count once into a dict, then <code>max(counts, key=counts.get)</code>.", "O(n)", "O(k)"))


@B
def most_common_word(text):
    words = text.lower().split()
    best, best_count = None, 0
    for w in words:
        c = words.count(w)
        if c > best_count:
            best, best_count = w, c
    return best


@O
def most_common_word(text):
    counts = {}
    for w in text.lower().split():
        counts[w] = counts.get(w, 0) + 1
    return max(counts, key=counts.get)


Q(None, "Pass or Fail Report", "Easy", "Dict comprehension",
  "Given name → marks, return name → 'pass' (marks ≥ 40) or 'fail'.",
  [(({"ana": 72, "ben": 35},), {"ana": "pass", "ben": "fail"}), (({},), {})],
  ("Loop over keys and fill a new dict with if/else.", "O(n)", "O(n)"),
  ("A dict comprehension with a conditional expression.", "O(n)", "O(n)"))


@B
def report(marks):
    result = {}
    for name in marks:
        if marks[name] >= 40:
            result[name] = "pass"
        else:
            result[name] = "fail"
    return result


@O
def report(marks):
    return {name: "pass" if m >= 40 else "fail" for name, m in marks.items()}


Q(None, "Sort by Value", "Medium", "sorted on items()",
  "Return the keys sorted by their values from highest to lowest (ties keep insertion order).",
  [(({"a": 3, "b": 9, "c": 5},), ["b", "c", "a"]), (({"x": 1, "y": 1},), ["x", "y"])],
  ("Repeatedly find and remove the key with the largest value.", "O(n²)", "O(n)"),
  ("<code>sorted(d, key=d.get, reverse=True)</code> — Python's sort is stable, so ties keep their order.", "O(n log n)", "O(n)"))


@B
def keys_by_value(d):
    remaining = dict(d)
    order = []
    while remaining:
        best = None
        for k in remaining:
            if best is None or remaining[k] > remaining[best]:
                best = k
        order.append(best)
        del remaining[best]
    return order


@O
def keys_by_value(d):
    return sorted(d, key=d.get, reverse=True)


Q(None, "Election Winner", "Easy", "Counting votes",
  "Each vote is a candidate's name. Return the candidate with the most votes (first to reach the top count wins a tie).",
  [((["ana", "ben", "ana", "cy", "ben", "ana"],), "ana"), ((["x"],), "x")],
  ("Make a list of candidates, count each one by scanning the votes.", "O(n · c)", "O(c)"),
  ("Count in one pass with a dict, then take the max by count.", "O(n)", "O(c)"),
  viz=(["ana", "ben", "ana", "cy", "ben"],))


@B
def winner(votes):
    candidates = []
    for v in votes:
        if v not in candidates:
            candidates.append(v)
    best, best_count = None, -1
    for c in candidates:
        n = votes.count(c)
        if n > best_count:
            best, best_count = c, n
    return best


@O
def winner(votes):
    tally = {}
    for v in votes:
        tally[v] = tally.get(v, 0) + 1
    return max(tally, key=tally.get)


Q(None, "Read a Nested Setting", "Medium", "Nested dicts",
  "<code>config</code> is a dict of dicts. Return <code>config[section][key]</code>, or <code>None</code> if either level is missing.",
  [(({"db": {"port": 5432}}, "db", "port"), 5432), (({"db": {}}, "db", "host"), None), (({}, "web", "port"), None)],
  ("Check each level with <code>in</code> before indexing.", "O(1)", "O(1)"),
  ("Chain <code>get</code> calls with an empty dict as the first default.", "O(1)", "O(1)"))


@B
def setting(config, section, key):
    if section in config:
        inner = config[section]
        if key in inner:
            return inner[key]
    return None


@O
def setting(config, section, key):
    return config.get(section, {}).get(key)


Q(None, "Two Lists to a Dict", "Easy", "dict(zip())",
  "Build a dict from a list of keys and a list of values of the same length.",
  [((["a", "b"], [1, 2]), {"a": 1, "b": 2}), (([], []), {})],
  ("Loop over indices.", "O(n)", "O(n)"),
  ("<code>dict(zip(keys, values))</code>.", "O(n)", "O(n)"))


@B
def to_dict(keys, values):
    result = {}
    for i in range(len(keys)):
        result[keys[i]] = values[i]
    return result


@O
def to_dict(keys, values):
    return dict(zip(keys, values))


Q(None, "Filter by Value", "Easy", "Comprehension with a condition",
  "Return only the items whose value is at least <code>minimum</code>.",
  [(({"a": 5, "b": 1, "c": 8}, 5), {"a": 5, "c": 8}), (({"a": 1}, 9), {})],
  ("Loop and copy the items that pass.", "O(n)", "O(n)"),
  ("<code>{k: v for k, v in d.items() if v &gt;= minimum}</code>.", "O(n)", "O(n)"))


@B
def filter_values(d, minimum):
    result = {}
    for k in d:
        if d[k] >= minimum:
            result[k] = d[k]
    return result


@O
def filter_values(d, minimum):
    return {k: v for k, v in d.items() if v >= minimum}


Q(None, "Key With the Largest Value", "Easy", "max(d, key=d.get)",
  "Return the key whose value is largest (first one on ties).",
  [(({"a": 3, "b": 9, "c": 9},), "b"), (({"x": -1},), "x")],
  ("Loop over the items keeping the best key.", "O(n)", "O(1)"),
  ("<code>max(d, key=d.get)</code>.", "O(n)", "O(1)"))


@B
def key_of_max(d):
    best = None
    for k in d:
        if best is None or d[k] > d[best]:
            best = k
    return best


@O
def key_of_max(d):
    return max(d, key=d.get)


Q(None, "Total of All Values", "Easy", "values()",
  "Return the sum of all values in a dict of numbers.",
  [(({"a": 3, "b": 4},), 7), (({},), 0)],
  ("Loop over keys and add <code>d[k]</code>.", "O(n)", "O(1)"),
  ("<code>sum(d.values())</code>.", "O(n)", "O(1)"))


@B
def total_values(d):
    total = 0
    for k in d:
        total += d[k]
    return total


@O
def total_values(d):
    return sum(d.values())


Q(None, "Roman to Integer", "Medium", "Lookup table",
  "Convert a Roman numeral (I, V, X, L, C, D, M) to an integer, e.g. 'MCMXCIV' → 1994.",
  [(("III",), 3), (("LVIII",), 58), (("MCMXCIV",), 1994)],
  ("Handle every special pair (IV, IX, XL, XC, CD, CM) with if statements while scanning.", "O(n)", "O(1)"),
  ("Look up values in a dict; subtract a symbol when a bigger one follows it.", "O(n)", "O(1)"),
  viz=("XIV",))


@B
def roman(s):
    total = 0
    i = 0
    pairs = {"IV": 4, "IX": 9, "XL": 40, "XC": 90, "CD": 400, "CM": 900}
    singles = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    while i < len(s):
        if s[i:i + 2] in pairs:
            total += pairs[s[i:i + 2]]
            i += 2
        else:
            total += singles[s[i]]
            i += 1
    return total


@O
def roman(s):
    value = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    for i, ch in enumerate(s):
        if i + 1 < len(s) and value[ch] < value[s[i + 1]]:
            total -= value[ch]
        else:
            total += value[ch]
    return total


Q(None, "First Repeated Word", "Easy", "Seen set / dict",
  "Return the first word that appears a second time, or None.",
  [(("he had had quite enough",), "had"), (("all different here",), None)],
  ("For each word, check whether it appears earlier in the list.", "O(n²)", "O(n)"),
  ("Remember words in a set as you go.", "O(n)", "O(n)"),
  viz=("to be or not to be",))


@B
def first_repeat(text):
    words = text.split()
    for i in range(len(words)):
        if words[i] in words[:i]:
            return words[i]
    return None


@O
def first_repeat(text):
    seen = set()
    for w in text.split():
        if w in seen:
            return w
        seen.add(w)
    return None


Q(None, "Total per Category", "Easy", "Summing into a dict",
  "<code>items</code> is a list of (category, amount). Return category → total amount.",
  [(([("food", 5), ("bus", 2), ("food", 3)],), {"food": 8, "bus": 2}), (([],), {})],
  ("Check for the key each time and branch.", "O(n)", "O(k)"),
  ("<code>defaultdict(int)</code> starts every new total at 0.", "O(n)", "O(k)"),
  viz=([("food", 5), ("bus", 2), ("food", 3)],))


@B
def per_category(items):
    totals = {}
    for pair in items:
        cat = pair[0]
        amount = pair[1]
        if cat in totals:
            totals[cat] += amount
        else:
            totals[cat] = amount
    return totals


@O
def per_category(items):
    from collections import defaultdict
    totals = defaultdict(int)
    for cat, amount in items:
        totals[cat] += amount
    return dict(totals)


Q(None, "Word Pattern", "Medium", "Two-way mapping",
  "Return True if the words follow the letter pattern exactly, e.g. 'abba' and 'dog cat cat dog' → True; each letter maps to one word and each word to one letter.",
  [(("abba", "dog cat cat dog"), True), (("abba", "dog cat cat fish"), False), (("aaaa", "dog cat cat dog"), False), (("ab", "dog dog"), False)],
  ("Compare every pair of positions: same letter must mean same word and vice versa.", "O(n²)", "O(1)"),
  ("Keep two dicts (letter → word, word → letter) and check them in one pass.", "O(n)", "O(n)"),
  viz=("abba", "dog cat cat dog"))


@B
def follows_pattern(pattern, text):
    words = text.split()
    if len(words) != len(pattern):
        return False
    for i in range(len(pattern)):
        for j in range(len(pattern)):
            if (pattern[i] == pattern[j]) != (words[i] == words[j]):
                return False
    return True


@O
def follows_pattern(pattern, text):
    words = text.split()
    if len(words) != len(pattern):
        return False
    to_word, to_letter = {}, {}
    for p, w in zip(pattern, words):
        if to_word.setdefault(p, w) != w or to_letter.setdefault(w, p) != p:
            return False
    return True
