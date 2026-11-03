from lib import *

TOPIC(
    id="tuples-sets", title="Tuples & Sets", glyph="( ) { }",
    blurb="Tuples: fixed records and unpacking. Sets: unique items, fast membership and set algebra.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">point = (3, 4)            # tuple — can't be changed
x, y = point              # unpacking
one = (5,)                # a 1-item tuple needs a comma
def stats(xs): return min(xs), max(xs)   # return a tuple

s = {1, 2, 3}             # set — unique, unordered
empty = set()             # NOT {} (that's an empty dict)
s.add(4); s.discard(9)
a | b, a &amp; b, a - b, a ^ b   # union, intersection, difference, symmetric difference
a &lt;= b                    # subset
x in s                    # O(1) membership</code></pre>
""")


Q(None, "Swap a Pair", "Easy", "Tuple unpacking",
  "Given a pair <code>(a, b)</code>, return <code>(b, a)</code>.",
  [(((1, 2),), (2, 1)), ((("x", "y"),), ("y", "x"))],
  ("Read each item by index and build a new tuple.", "O(1)", "O(1)"),
  ("Unpack into two names and pack them back the other way round.", "O(1)", "O(1)"))


@B
def swap_pair(pair):
    first = pair[0]
    second = pair[1]
    return (second, first)


@O
def swap_pair(pair):
    a, b = pair
    return b, a


Q(None, "Min and Max Together", "Easy", "Returning a tuple",
  "Return <code>(smallest, largest)</code> of a non-empty list.",
  [(([4, 1, 9, 3],), (1, 9)), (([5],), (5, 5))],
  ("One loop tracking both.", "O(n)", "O(1)"),
  ("Return <code>min(nums), max(nums)</code> — a tuple is created by the comma.", "O(n)", "O(1)"),
  viz=([4, 1, 9, 3],))


@B
def min_max(nums):
    lo = hi = nums[0]
    for x in nums:
        if x < lo:
            lo = x
        if x > hi:
            hi = x
    return (lo, hi)


@O
def min_max(nums):
    return min(nums), max(nums)


Q(None, "Describe a Record", "Easy", "Unpacking",
  "A record is <code>(name, age, city)</code>. Return <code>'NAME (AGE) from CITY'</code>.",
  [((("Ana", 21, "Pune"),), "Ana (21) from Pune"), ((("Li", 30, "Oslo"),), "Li (30) from Oslo")],
  ("Index each field: record[0], record[1], record[2].", "O(1)", "O(1)"),
  ("Unpack into meaningful names first — much easier to read.", "O(1)", "O(1)"))


@B
def describe(record):
    return record[0] + " (" + str(record[1]) + ") from " + record[2]


@O
def describe(record):
    name, age, city = record
    return f"{name} ({age}) from {city}"


Q(None, "Sort Pairs by Second Item", "Medium", "sorted with key",
  "Sort a list of (name, score) pairs by score, lowest first.",
  [(([("a", 3), ("b", 1), ("c", 2)],), [("b", 1), ("c", 2), ("a", 3)]), (([],), [])],
  ("Selection sort by hand comparing the second items.", "O(n²)", "O(n)"),
  ("<code>sorted(pairs, key=lambda p: p[1])</code>.", "O(n log n)", "O(n)"),
  viz=([("a", 3), ("b", 1), ("c", 2)],))


@B
def sort_by_score(pairs):
    items = pairs[:]
    for i in range(len(items)):
        smallest = i
        for j in range(i + 1, len(items)):
            if items[j][1] < items[smallest][1]:
                smallest = j
        items[i], items[smallest] = items[smallest], items[i]
    return items


@O
def sort_by_score(pairs):
    return sorted(pairs, key=lambda p: p[1])


Q(None, "Distance From Origin", "Easy", "Tuple unpacking · math",
  "Return the distance of point <code>(x, y)</code> from (0, 0), rounded to 2 decimals.",
  [(((3, 4),), 5.0), (((1, 1),), 1.41), (((0, 0),), 0.0)],
  ("Index the tuple and apply Pythagoras.", "O(1)", "O(1)"),
  ("Unpack the tuple straight into <code>math.hypot(*point)</code>.", "O(1)", "O(1)"))


@B
def from_origin(point):
    x = point[0]
    y = point[1]
    return round((x * x + y * y) ** 0.5, 2)


@O
def from_origin(point):
    import math
    return round(math.hypot(*point), 2)


Q(None, "Count in a Tuple", "Easy", "tuple.count",
  "Return how many times <code>value</code> appears in the tuple.",
  [(((1, 2, 1, 1), 1), 3), ((("a",), "b"), 0)],
  ("Loop and count.", "O(n)", "O(1)"),
  ("Tuples have <code>count</code> and <code>index</code> methods.", "O(n)", "O(1)"))


@B
def tuple_count(t, value):
    count = 0
    for x in t:
        if x == value:
            count += 1
    return count


@O
def tuple_count(t, value):
    return t.count(value)


Q(None, "Pair Up Two Lists", "Easy", "zip",
  "Return a list of pairs <code>(a[i], b[i])</code> for lists of equal length.",
  [((["x", "y"], [1, 2]), [("x", 1), ("y", 2)]), (([], []), [])],
  ("Loop over indices and build each tuple.", "O(n)", "O(n)"),
  ("<code>list(zip(a, b))</code>.", "O(n)", "O(n)"),
  viz=(["x", "y", "z"], [1, 2, 3]))


@B
def pair_up(a, b):
    pairs = []
    for i in range(len(a)):
        pairs.append((a[i], b[i]))
    return pairs


@O
def pair_up(a, b):
    return list(zip(a, b))


Q(None, "Unzip Pairs", "Medium", "zip(*pairs)",
  "Turn a list of pairs into two tuples: <code>[(1, 'a'), (2, 'b')] → ((1, 2), ('a', 'b'))</code>.",
  [(([(1, "a"), (2, "b")],), ((1, 2), ("a", "b"))), (([(5, 6)],), ((5,), (6,)))],
  ("Two loops collecting firsts and seconds, then convert to tuples.", "O(n)", "O(n)"),
  ("<code>zip(*pairs)</code> passes every pair as a separate argument, regrouping them by position.", "O(n)", "O(n)"),
  viz=([(1, "a"), (2, "b"), (3, "c")],))


@B
def unzip(pairs):
    firsts, seconds = [], []
    for p in pairs:
        firsts.append(p[0])
        seconds.append(p[1])
    return tuple(firsts), tuple(seconds)


@O
def unzip(pairs):
    firsts, seconds = zip(*pairs)
    return firsts, seconds


Q(None, "Distinct Cells Visited", "Medium", "Tuples in a set",
  "A robot starts at (0, 0) and follows moves 'U', 'D', 'L', 'R'. Return how many different cells it visits (including the start).",
  [(("URDL",), 4), (("RRRR",), 5), (("",), 1)],
  ("Keep a list of visited cells and check <code>in</code> before adding (each check scans the list).", "O(n²)", "O(n)"),
  ("Store the (x, y) tuples in a set — tuples are hashable, and duplicates disappear.", "O(n)", "O(n)"),
  viz=("URDLL",))


@B
def cells_visited(moves):
    x, y = 0, 0
    visited = [(0, 0)]
    for m in moves:
        if m == "U":
            y += 1
        elif m == "D":
            y -= 1
        elif m == "L":
            x -= 1
        else:
            x += 1
        if (x, y) not in visited:
            visited.append((x, y))
    return len(visited)


@O
def cells_visited(moves):
    step = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}
    x = y = 0
    seen = {(0, 0)}
    for m in moves:
        dx, dy = step[m]
        x, y = x + dx, y + dy
        seen.add((x, y))
    return len(seen)


Q(None, "Sum, Mean and Max", "Easy", "Returning several values",
  "Return <code>(total, mean, largest)</code> of a non-empty list; mean rounded to 2 decimals.",
  [(([2, 4, 9],), (15, 5.0, 9)), (([7],), (7, 7.0, 7))],
  ("One loop computing everything by hand.", "O(n)", "O(1)"),
  ("Use the built-ins and return a tuple.", "O(n)", "O(1)"))


@B
def stats(nums):
    total, largest = 0, nums[0]
    for x in nums:
        total += x
        if x > largest:
            largest = x
    return (total, round(total / len(nums), 2), largest)


@O
def stats(nums):
    total = sum(nums)
    return total, round(total / len(nums), 2), max(nums)


Q(None, "Count Unique Values", "Easy", "set()",
  "Return how many different values are in the list.",
  [(([1, 2, 2, 3, 3, 3],), 3), (([],), 0), ((["a", "A"],), 2)],
  ("Build a list of uniques, checking <code>in</code> each time.", "O(n²)", "O(n)"),
  ("A set keeps only unique values: <code>len(set(items))</code>.", "O(n)", "O(n)"),
  viz=([1, 2, 2, 3, 3, 3],))


@B
def unique_count(items):
    seen = []
    for x in items:
        if x not in seen:
            seen.append(x)
    return len(seen)


@O
def unique_count(items):
    return len(set(items))


Q(None, "Common Letters", "Easy", "Intersection",
  "Return the sorted list of letters that appear in both words.",
  [(("python", "typhoon"), ["h", "n", "o", "p", "t", "y"]), (("abc", "xyz"), [])],
  ("For each letter of the first word, scan the second; avoid duplicates.", "O(m · n)", "O(k)"),
  ("Intersect two sets: <code>set(a) &amp; set(b)</code>.", "O(m + n)", "O(k)"))


@B
def common_letters(a, b):
    result = []
    for ch in a:
        if ch in b and ch not in result:
            result.append(ch)
    return sorted(result)


@O
def common_letters(a, b):
    return sorted(set(a) & set(b))


Q(None, "Union of Two Lists", "Easy", "Union",
  "Return all values that appear in either list, sorted, without duplicates.",
  [(([3, 1, 2], [2, 5]), [1, 2, 3, 5]), (([], [1, 1]), [1])],
  ("Add both lists into a result, skipping values already present.", "O((m + n)²)", "O(m + n)"),
  ("<code>sorted(set(a) | set(b))</code>.", "O((m + n) log)", "O(m + n)"))


@B
def union(a, b):
    result = []
    for x in a + b:
        if x not in result:
            result.append(x)
    return sorted(result)


@O
def union(a, b):
    return sorted(set(a) | set(b))


Q(None, "In First List Only", "Easy", "Difference",
  "Return the sorted unique values that are in <code>a</code> but not in <code>b</code>.",
  [(([1, 2, 3, 4], [2, 4]), [1, 3]), (([1, 1], [1]), [])],
  ("For each value of a, scan b.", "O(m · n)", "O(m)"),
  ("<code>set(a) - set(b)</code>.", "O(m + n)", "O(m)"))


@B
def only_in_first(a, b):
    result = []
    for x in a:
        if x not in b and x not in result:
            result.append(x)
    return sorted(result)


@O
def only_in_first(a, b):
    return sorted(set(a) - set(b))


Q(None, "In Exactly One List", "Medium", "Symmetric difference",
  "Return the sorted values that appear in exactly one of the two lists.",
  [(([1, 2, 3], [2, 3, 4]), [1, 4]), (([1], [1]), [])],
  ("Check each value of a against b and each value of b against a.", "O(m · n)", "O(m + n)"),
  ("<code>set(a) ^ set(b)</code>.", "O(m + n)", "O(m + n)"))


@B
def exactly_one_list(a, b):
    result = []
    for x in a:
        if x not in b and x not in result:
            result.append(x)
    for x in b:
        if x not in a and x not in result:
            result.append(x)
    return sorted(result)


@O
def exactly_one_list(a, b):
    return sorted(set(a) ^ set(b))


Q(None, "Has Duplicates?", "Easy", "set size",
  "Return True if any value appears more than once.",
  [(([1, 2, 3, 1],), True), (([1, 2, 3],), False), (([],), False)],
  ("Compare every pair of items.", "O(n²)", "O(1)"),
  ("A set drops duplicates, so compare sizes.", "O(n)", "O(n)"),
  viz=([3, 1, 4, 1],))


@B
def has_duplicates(items):
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False


@O
def has_duplicates(items):
    return len(set(items)) != len(items)


Q(None, "Is It a Subset?", "Easy", "Subset test",
  "Return True if every value of <code>small</code> also appears in <code>big</code>.",
  [(([1, 2], [3, 2, 1]), True), (([1, 4], [1, 2, 3]), False), (([], [1]), True)],
  ("Check each value with <code>in</code> on the list.", "O(m · n)", "O(1)"),
  ("<code>set(small) &lt;= set(big)</code>.", "O(m + n)", "O(m + n)"))


@B
def is_subset(small, big):
    for x in small:
        if x not in big:
            return False
    return True


@O
def is_subset(small, big):
    return set(small) <= set(big)


Q(None, "Missing Numbers", "Medium", "Difference with a range",
  "<code>nums</code> should contain every number from 1 to n. Return the missing ones, sorted.",
  [(([4, 1, 2, 7], 7), [3, 5, 6]), (([1, 2, 3], 3), []), (([], 2), [1, 2])],
  ("For each number 1..n, search the list.", "O(n²)", "O(n)"),
  ("<code>set(range(1, n + 1)) - set(nums)</code>.", "O(n)", "O(n)"),
  viz=([4, 1, 2, 7], 7))


@B
def missing(nums, n):
    result = []
    for k in range(1, n + 1):
        if k not in nums:
            result.append(k)
    return result


@O
def missing(nums, n):
    return sorted(set(range(1, n + 1)) - set(nums))


Q(None, "Unique Words, Ignoring Case", "Easy", "Set comprehension",
  "Return how many different words are in the sentence, ignoring upper/lower case.",
  [(("The cat and the hat",), 4), (("a A a",), 1)],
  ("Keep a list of lower-cased words seen so far.", "O(n²)", "O(n)"),
  ("A set comprehension of lower-cased words.", "O(n)", "O(n)"))


@B
def unique_words(sentence):
    seen = []
    for w in sentence.split():
        w = w.lower()
        if w not in seen:
            seen.append(w)
    return len(seen)


@O
def unique_words(sentence):
    return len({w.lower() for w in sentence.split()})


Q(None, "Two Numbers Add Up", "Medium", "Set of seen values",
  "Return True if two different positions in the list add up to <code>target</code>.",
  [(([3, 8, 1, 5], 9), True), (([1, 2, 3], 10), False), (([4], 8), False), (([4, 4], 8), True)],
  ("Check every pair with nested loops.", "O(n²)", "O(1)"),
  ("Walk once; for each x ask whether target − x was already seen.", "O(n)", "O(n)"),
  viz=([3, 8, 1, 5], 9))


@B
def two_add_up(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return True
    return False


@O
def two_add_up(nums, target):
    seen = set()
    for x in nums:
        if target - x in seen:
            return True
        seen.add(x)
    return False
