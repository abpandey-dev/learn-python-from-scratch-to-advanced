from lib import *
import heapq
import random
from collections import defaultdict, deque, OrderedDict


TOPIC(
    id="dsa-classics", title="Classic Algorithms", glyph="O(n log n)",
    blurb="The algorithms interviewers ask you to write from memory: sorting, inversions, KMP, Rabin-Karp, union-find, Fenwick and segment trees, shortest paths, knapsack, topological order and designing data structures.",
    theory="""
<h3>Cheat sheet</h3>
<table><tr><th>Algorithm</th><th>Time</th><th>Space</th><th>Note</th></tr>
<tr><td>Merge sort</td><td>O(n log n)</td><td>O(n)</td><td>stable; good for inversions</td></tr>
<tr><td>Quick sort</td><td>O(n log n) average, O(n²) worst</td><td>O(log n)</td><td>fast in practice, in place</td></tr>
<tr><td>Heap sort</td><td>O(n log n)</td><td>O(1)</td><td>not stable</td></tr>
<tr><td>Counting sort</td><td>O(n + k)</td><td>O(k)</td><td>small integer keys</td></tr>
<tr><td>KMP</td><td>O(n + m)</td><td>O(m)</td><td>guaranteed linear search</td></tr>
<tr><td>Union-find</td><td>≈ O(1) per op</td><td>O(n)</td><td>connectivity</td></tr>
<tr><td>Fenwick / segment tree</td><td>O(log n) per op</td><td>O(n)</td><td>range queries with updates</td></tr>
<tr><td>Dijkstra</td><td>O(E log V)</td><td>O(V)</td><td>no negative edges</td></tr>
<tr><td>Bellman-Ford</td><td>O(V·E)</td><td>O(V)</td><td>negative edges allowed</td></tr>
<tr><td>Floyd-Warshall</td><td>O(V³)</td><td>O(V²)</td><td>all pairs</td></tr></table>
""")


Q(None, "Merge Sort", "Medium", "Divide and conquer",
  "Sort a list without using built-in sorting.",
  [(([5, 2, 9, 1, 5, 6],), [1, 2, 5, 5, 6, 9]), (([],), []), (([2, 1],), [1, 2])],
  ("Insertion sort: simple, but quadratic.", "O(n²)", "O(1)"),
  ("Split in half, sort each half, then merge two sorted lists.", "O(n log n)", "O(n)"))


@B
def merge_sort(a):
    out = list(a)
    for i in range(1, len(out)):
        j = i
        while j > 0 and out[j - 1] > out[j]:
            out[j - 1], out[j] = out[j], out[j - 1]
            j -= 1
    return out


@O
def merge_sort(a):
    if len(a) <= 1:
        return list(a)
    mid = len(a) // 2
    left, right = merge_sort(a[:mid]), merge_sort(a[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    return out + left[i:] + right[j:]


Q(None, "Quick Sort", "Medium", "Partition",
  "Sort a list using partitioning around a pivot.",
  [(([3, 6, 1, 8, 2, 9, 2],), [1, 2, 2, 3, 6, 8, 9]), (([1],), [1])],
  ("Simple version: build new lists around a pivot. Easy to explain, but uses extra memory.", "O(n log n) average", "O(n)"),
  ("In place, using Lomuto partition with a middle pivot, swapping it to the end first.", "O(n log n) average", "O(log n)"))


@B
def quick_sort(a):
    if len(a) <= 1:
        return list(a)
    pivot = a[len(a) // 2]
    less = [x for x in a if x < pivot]
    same = [x for x in a if x == pivot]
    more = [x for x in a if x > pivot]
    return quick_sort(less) + same + quick_sort(more)


@O
def quick_sort(a):
    a = list(a)

    def sort(lo, hi):
        if lo >= hi:
            return
        mid = (lo + hi) // 2
        a[mid], a[hi] = a[hi], a[mid]
        store = lo
        for i in range(lo, hi):
            if a[i] < a[hi]:
                a[i], a[store] = a[store], a[i]
                store += 1
        a[store], a[hi] = a[hi], a[store]
        sort(lo, store - 1)
        sort(store + 1, hi)
    sort(0, len(a) - 1)
    return a


Q(None, "Heap Sort", "Medium", "Sift down",
  "Sort using a heap you maintain yourself, in the list.",
  [(([4, 10, 3, 5, 1],), [1, 3, 4, 5, 10])],
  ("Use <code>heapq</code>: push all, pop all.", "O(n log n)", "O(n)"),
  ("Build a max-heap in place, then repeatedly swap the top to the end and sift down.", "O(n log n)", "O(1)"))


@B
def heap_sort(a):
    h = list(a)
    heapq.heapify(h)
    return [heapq.heappop(h) for _ in range(len(h))]


@O
def heap_sort(a):
    a = list(a)

    def sift(i, n):
        while 2 * i + 1 < n:
            c = 2 * i + 1
            if c + 1 < n and a[c + 1] > a[c]:
                c += 1
            if a[i] >= a[c]:
                break
            a[i], a[c] = a[c], a[i]
            i = c
    for i in range(len(a) // 2 - 1, -1, -1):
        sift(i, len(a))
    for end in range(len(a) - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift(0, end)
    return a


Q(None, "Counting Sort", "Easy", "Beat O(n log n)",
  "Sort non-negative integers no larger than k.",
  [(([3, 1, 2, 1, 0], 3), [0, 1, 1, 2, 3])],
  ("Comparison sort; ignores the small range.", "O(n log n)", "O(n)"),
  ("Count each value, then write them out in order.", "O(n + k)", "O(k)"),
  names=["a", "k"])


@B
def counting_sort(a, k):
    return sorted(a)


@O
def counting_sort(a, k):
    counts = [0] * (k + 1)
    for x in a:
        counts[x] += 1
    out = []
    for value, c in enumerate(counts):
        out += [value] * c
    return out


Q(None, "Count Inversions", "Hard", "Merge sort's bonus",
  "Count pairs i &lt; j with a[i] &gt; a[j].",
  [(([2, 4, 1, 3, 5],), 3), (([5, 4, 3, 2, 1],), 10), (([1, 2],), 0)],
  ("Check every pair.", "O(n²)", "O(1)"),
  ("During merging, when a right element goes first, it forms an inversion with everything left in the left half.", "O(n log n)", "O(n)"))


@B
def inversions(a):
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])


@O
def inversions(a):
    def solve(x):
        if len(x) <= 1:
            return x, 0
        left, lc = solve(x[:len(x) // 2])
        right, rc = solve(x[len(x) // 2:])
        out, i, j, count = [], 0, 0, lc + rc
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                out.append(left[i])
                i += 1
            else:
                count += len(left) - i
                out.append(right[j])
                j += 1
        return out + left[i:] + right[j:], count
    return solve(a)[1]


Q(None, "Substring Search With KMP", "Hard", "Never look back",
  "Return the first index of pattern in text, or −1, without built-in find.",
  [(("abxabcabcaby", "abcaby"), 6), (("aaaa", "b"), -1), (("abc", ""), 0)],
  ("Try every start position.", "O(n·m)", "O(1)"),
  ("Pre-compute the longest prefix that's also a suffix, so a mismatch skips what's already matched.", "O(n + m)", "O(m)"),
  names=["text", "pattern"])


@B
def find_first(text, pattern):
    for i in range(len(text) - len(pattern) + 1):
        j = 0
        while j < len(pattern) and text[i + j] == pattern[j]:
            j += 1
        if j == len(pattern):
            return i
    return -1


@O
def find_first(text, pattern):
    if not pattern:
        return 0
    lps = [0] * len(pattern)
    k = 0
    for i in range(1, len(pattern)):
        while k and pattern[i] != pattern[k]:
            k = lps[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        lps[i] = k
    k = 0
    for i, ch in enumerate(text):
        while k and ch != pattern[k]:
            k = lps[k - 1]
        if ch == pattern[k]:
            k += 1
        if k == len(pattern):
            return i - k + 1
    return -1


Q(None, "All Matches With a Rolling Hash", "Hard", "Rabin-Karp",
  "Return all start positions of pattern in text.",
  [(("abababa", "aba"), [0, 2, 4]), (("abc", "d"), [])],
  ("Compare a slice at every position.", "O(n·m)", "O(m)"),
  ("Update a window's hash in O(1); compare the actual text only when hashes match.", "O(n + m) expected", "O(1)"),
  names=["text", "pattern"])


@B
def all_matches(text, pattern):
    m = len(pattern)
    return [i for i in range(len(text) - m + 1) if text[i:i + m] == pattern]


@O
def all_matches(text, pattern):
    base, mod = 256, 1_000_000_007
    m, n = len(pattern), len(text)
    if m > n:
        return []
    top = pow(base, m - 1, mod)
    p = w = 0
    for i in range(m):
        p = (p * base + ord(pattern[i])) % mod
        w = (w * base + ord(text[i])) % mod
    out = []
    for i in range(n - m + 1):
        if w == p and text[i:i + m] == pattern:
            out.append(i)
        if i + m < n:
            w = ((w - ord(text[i]) * top) * base + ord(text[i + m])) % mod
    return out


Q(None, "Union-Find", "Medium", "Who's connected?",
  "Build a class with find(x) and union(a, b), where union returns True if it merged two groups, and count() returns the number of groups.",
  [(((4,), [("union", (0, 1)), ("union", (1, 0)), ("union", (2, 3)), ("count", ()), ("union", (1, 2)), ("count", ())]), [True, False, True, 2, True, 1])],
  ("Label each item with a group id; a union relabels a whole group.", "O(n) per union", "O(n)"),
  ("Parents with path compression and union by size: nearly constant.", "≈ O(1) per op", "O(n)"),
  design=True)


@B
class UnionFind:
    def __init__(self, n):
        self.group = list(range(n))

    def find(self, x):
        return self.group[x]

    def union(self, a, b):
        ga, gb = self.group[a], self.group[b]
        if ga == gb:
            return False
        self.group = [ga if g == gb else g for g in self.group]
        return True

    def count(self):
        return len(set(self.group))


@O
class UnionFind:
    def __init__(self, n):
        self.parent, self.size, self.groups = list(range(n)), [1] * n, n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        self.groups -= 1
        return True

    def count(self):
        return self.groups


Q(None, "Fenwick Tree", "Hard", "Prefix sums with updates",
  "Build a class with add(i, delta) and prefix(i), the sum of the first i values.",
  [(((5,), [("add", (0, 3)), ("add", (2, 4)), ("prefix", (1,)), ("prefix", (3,)), ("add", (1, 2)), ("prefix", (3,))]), [None, None, 3, 7, None, 9])],
  ("A plain array: fast add, slow prefix.", "O(n) per prefix", "O(n)"),
  ("Each index covers a range given by its lowest set bit, i &amp; −i.", "O(log n) per op", "O(n)"),
  design=True)


@B
class Fenwick:
    def __init__(self, n):
        self.a = [0] * n

    def add(self, i, delta):
        self.a[i] += delta

    def prefix(self, i):
        return sum(self.a[:i])


@O
class Fenwick:
    def __init__(self, n):
        self.tree = [0] * (n + 1)

    def add(self, i, delta):
        i += 1
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & -i

    def prefix(self, i):
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & -i
        return total


Q(None, "Segment Tree: Range Minimum", "Hard", "Any range, with updates",
  "Build a class from a list, with update(i, value) and query(lo, hi) for the minimum of a[lo..hi] inclusive.",
  [((([5, 2, 6, 3],), [("query", (0, 3)), ("query", (2, 3)), ("update", (1, 9)), ("query", (0, 1))]), [2, 3, None, 5])],
  ("Scan the range on each query.", "O(n) per query", "O(n)"),
  ("A binary tree stored in an array, where each node holds the minimum of its range.", "O(log n) per op", "O(n)"),
  design=True)


@B
class RangeMin:
    def __init__(self, a):
        self.a = list(a)

    def update(self, i, value):
        self.a[i] = value

    def query(self, lo, hi):
        return min(self.a[lo:hi + 1])


@O
class RangeMin:
    def __init__(self, a):
        self.n = len(a)
        self.t = [0] * self.n + list(a)
        for i in range(self.n - 1, 0, -1):
            self.t[i] = min(self.t[2 * i], self.t[2 * i + 1])

    def update(self, i, value):
        i += self.n
        self.t[i] = value
        while i > 1:
            i //= 2
            self.t[i] = min(self.t[2 * i], self.t[2 * i + 1])

    def query(self, lo, hi):
        lo += self.n
        hi += self.n + 1
        best = float("inf")
        while lo < hi:
            if lo & 1:
                best = min(best, self.t[lo])
                lo += 1
            if hi & 1:
                hi -= 1
                best = min(best, self.t[hi])
            lo //= 2
            hi //= 2
        return best


Q(None, "LFU Cache", "Hard", "A harder LRU",
  "Build get(key) and put(key, value) with a capacity. Evict the least frequently used key; ties go to the least recently used.",
  [(((2,), [("put", (1, 1)), ("put", (2, 2)), ("get", (1,)), ("put", (3, 3)), ("get", (2,)), ("get", (3,)), ("get", (1,))]), [None, None, 1, None, -1, 3, 1])],
  ("Scan all keys to find the eviction.", "O(c) per eviction", "O(c)"),
  ("A group of ordered dictionaries per frequency, plus the current minimum frequency.", "O(1) per op", "O(c)"),
  design=True)


@B
class LFUCache:
    def __init__(self, capacity):
        self.capacity, self.time = capacity, 0
        self.data = {}

    def get(self, key):
        if key not in self.data:
            return -1
        value, freq, _ = self.data[key]
        self.time += 1
        self.data[key] = (value, freq + 1, self.time)
        return value

    def put(self, key, value):
        self.time += 1
        if key in self.data:
            self.data[key] = (value, self.data[key][1] + 1, self.time)
            return None
        if len(self.data) == self.capacity:
            del self.data[min(self.data, key=lambda k: self.data[k][1:])]
        self.data[key] = (value, 1, self.time)
        return None


@O
class LFUCache:
    def __init__(self, capacity):
        self.capacity, self.low = capacity, 0
        self.values, self.freq = {}, {}
        self.groups = defaultdict(OrderedDict)

    def _bump(self, key):
        f = self.freq[key]
        del self.groups[f][key]
        if not self.groups[f] and self.low == f:
            self.low = f + 1
        self.freq[key] = f + 1
        self.groups[f + 1][key] = None

    def get(self, key):
        if key not in self.values:
            return -1
        self._bump(key)
        return self.values[key]

    def put(self, key, value):
        if key in self.values:
            self.values[key] = value
            self._bump(key)
            return None
        if len(self.values) == self.capacity:
            old, _ = self.groups[self.low].popitem(last=False)
            del self.values[old], self.freq[old]
        self.values[key], self.freq[key], self.low = value, 1, 1
        self.groups[1][key] = None
        return None


Q(None, "Time-Based Key-Value Store", "Medium", "Binary search on history",
  "Build set(key, value, t) and get(key, t), which returns the value with the largest time ≤ t, or an empty string.",
  [(((), [("set", ("a", "x", 1)), ("set", ("a", "y", 4)), ("get", ("a", 3)), ("get", ("a", 4)), ("get", ("a", 0)), ("get", ("b", 1))]), [None, None, 'x', 'y', '', ''])],
  ("Scan the key's whole history.", "O(n) per get", "O(n)"),
  ("Times only increase, so history is sorted: binary search it.", "O(log n) per get", "O(n)"),
  design=True)


@B
class TimeMap:
    def __init__(self):
        self.data = {}

    def set(self, key, value, t):
        self.data.setdefault(key, []).append((t, value))

    def get(self, key, t):
        best = ""
        for when, value in self.data.get(key, []):
            if when <= t:
                best = value
        return best


@O
class TimeMap:
    def __init__(self):
        self.data = defaultdict(list)

    def set(self, key, value, t):
        self.data[key].append((t, value))

    def get(self, key, t):
        history = self.data.get(key, [])
        lo, hi = 0, len(history)
        while lo < hi:
            mid = (lo + hi) // 2
            if history[mid][0] <= t:
                lo = mid + 1
            else:
                hi = mid
        return history[lo - 1][1] if lo else ""


Q(None, "Design a Hash Map", "Medium", "How dict works",
  "Build put(key, value), get(key) (−1 if missing) and remove(key), without using a dict.",
  [(((), [("put", (1, 10)), ("put", (2, 20)), ("get", (1,)), ("get", (3,)), ("put", (2, 30)), ("get", (2,)), ("remove", (2,)), ("get", (2,))]), [None, None, 10, -1, None, 30, None, -1])],
  ("A list of pairs, scanned each time.", "O(n) per op", "O(n)"),
  ("Buckets indexed by hash, doubling when they get too full.", "O(1) average", "O(n)"),
  design=True)


@B
class MyHashMap:
    def __init__(self):
        self.items = []

    def put(self, key, value):
        self.remove(key)
        self.items.append([key, value])

    def get(self, key):
        for k, v in self.items:
            if k == key:
                return v
        return -1

    def remove(self, key):
        self.items = [p for p in self.items if p[0] != key]


@O
class MyHashMap:
    def __init__(self):
        self.size, self.buckets = 0, [[] for _ in range(8)]

    def _bucket(self, key):
        return self.buckets[hash(key) % len(self.buckets)]

    def put(self, key, value):
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self.size += 1
        if self.size > 2 * len(self.buckets):
            old = self.buckets
            self.buckets = [[] for _ in range(2 * len(old))]
            for b in old:
                for k, v in b:
                    self._bucket(k).append([k, v])

    def get(self, key):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return -1

    def remove(self, key):
        bucket = self._bucket(key)
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                bucket.pop(i)
                self.size -= 1
                return


Q(None, "Insert, Delete, Random in O(1)", "Medium", "List plus dictionary",
  "Build insert(x) and remove(x), each returning whether it changed anything, and contains(x). (A real get_random would use random.choice on the list.)",
  [(((), [("insert", (1,)), ("insert", (1,)), ("insert", (2,)), ("remove", (1,)), ("contains", (1,)), ("remove", (5,)), ("contains", (2,))]), [True, False, True, True, False, False, True])],
  ("A list alone: fast random choice, slow membership and removal.", "O(n) per op", "O(n)"),
  ("A dictionary from value to index. To remove, swap with the last item, then pop.", "O(1) per op", "O(n)"),
  design=True)


@B
class RandomizedSet:
    def __init__(self):
        self.items = []

    def insert(self, x):
        if x in self.items:
            return False
        self.items.append(x)
        return True

    def remove(self, x):
        if x not in self.items:
            return False
        self.items.remove(x)
        return True

    def contains(self, x):
        return x in self.items


@O
class RandomizedSet:
    def __init__(self):
        self.items, self.where = [], {}

    def insert(self, x):
        if x in self.where:
            return False
        self.where[x] = len(self.items)
        self.items.append(x)
        return True

    def remove(self, x):
        if x not in self.where:
            return False
        i, last = self.where.pop(x), self.items.pop()
        if i < len(self.items):
            self.items[i] = last
            self.where[last] = i
        return True

    def contains(self, x):
        return x in self.where


Q(None, "Bellman-Ford", "Medium", "Negative edges",
  "Return shortest distances from source 0 through edges (u, v, w), with None for unreachable. If a negative cycle is reachable, return 'negative cycle'.",
  [((4, [(0, 1, 4), (0, 2, 5), (1, 2, -3), (2, 3, 2)]), [0, 4, 1, 3]), ((3, [(0, 1, 1), (1, 2, -2), (2, 1, 1)]), 'negative cycle'), ((3, [(1, 2, 1)]), [0, None, None])],
  ("Relax all edges V times; a change on the last round means a negative cycle.", "O(V·E)", "O(V)"),
  ("The same, stopping early when a round changes nothing.", "O(V·E), often less", "O(V)"),
  names=["n", "edges"])


@B
def bellman_ford(n, edges):
    inf = float("inf")
    d = [inf] * n
    d[0] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    for u, v, w in edges:
        if d[u] + w < d[v]:
            return "negative cycle"
    return [None if x == inf else x for x in d]


@O
def bellman_ford(n, edges):
    inf = float("inf")
    d = [inf] * n
    d[0] = 0
    for _ in range(n):
        changed = False
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
                changed = True
        if not changed:
            return [None if x == inf else x for x in d]
    return "negative cycle"


Q(None, "Floyd-Warshall", "Medium", "All pairs",
  "Return the n × n table of shortest distances for directed edges (u, v, w), with None for unreachable.",
  [((3, [(0, 1, 4), (1, 2, 1), (0, 2, 7)]), [[0, 4, 5], [None, 0, 1], [None, None, 0]])],
  ("Run Bellman-Ford from each start.", "O(V²·E)", "O(V²)"),
  ("For each middle node k, try improving every path via k.", "O(V³)", "O(V²)"),
  names=["n", "edges"])


@B
def all_pairs(n, edges):
    out = []
    for s in range(n):
        d = [float("inf")] * n
        d[s] = 0
        for _ in range(n - 1):
            for u, v, w in edges:
                d[v] = min(d[v], d[u] + w)
        out.append([None if x == float("inf") else x for x in d])
    return out


@O
def all_pairs(n, edges):
    inf = float("inf")
    d = [[0 if i == j else inf for j in range(n)] for i in range(n)]
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    return [[None if x == inf else x for x in row] for row in d]


Q(None, "0/1 Knapsack", "Medium", "The DP you must know",
  "Return the maximum value that fits in the capacity, using each item once.",
  [(([1, 3, 4, 5], [1, 4, 5, 7], 7), 9), (([2], [3], 1), 0)],
  ("Recursion: take or skip each item.", "O(2ⁿ)", "O(n)"),
  ("One DP row, filled right to left, so each item is used once.", "O(n·C)", "O(C)"),
  names=["weights", "values", "capacity"])


@B
def knapsack(weights, values, capacity):
    def best(i, room):
        if i == len(weights):
            return 0
        skip = best(i + 1, room)
        if weights[i] > room:
            return skip
        return max(skip, values[i] + best(i + 1, room - weights[i]))
    return best(0, capacity)


@O
def knapsack(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for room in range(capacity, w - 1, -1):
            dp[room] = max(dp[room], dp[room - w] + v)
    return dp[capacity]


Q(None, "Longest Common Substring", "Medium", "Contiguous, unlike subsequence",
  "Return the length of the longest substring appearing in both strings.",
  [(("abcdxyz", "xyzabcd"), 4), (("abc", "def"), 0)],
  ("Try every start pair and extend.", "O(n·m·min)", "O(1)"),
  ("DP: dp[j] = dp_prev[j−1] + 1 if the characters match, else 0.", "O(n·m)", "O(m)"),
  names=["a", "b"])


@B
def common_substring(a, b):
    best = 0
    for i in range(len(a)):
        for j in range(len(b)):
            k = 0
            while i + k < len(a) and j + k < len(b) and a[i + k] == b[j + k]:
                k += 1
            best = max(best, k)
    return best


@O
def common_substring(a, b):
    prev, best = [0] * (len(b) + 1), 0
    for ch in a:
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if ch == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                best = max(best, cur[j])
        prev = cur
    return best


Q(None, "Alien Dictionary", "Hard", "Topological sort",
  "Words are sorted in an alien alphabet. Return its letter order (smallest letter first among those available), or '' if inconsistent.",
  [((["wrt", "wrf", "er", "ett", "rftt"],), 'wertf'), ((["z", "x", "z"],), ''), ((["abc", "ab"],), '')],
  ("DFS on the graph, with colours for cycles, trying letters in order.", "O(C)", "O(1) alphabet"),
  ("Kahn's algorithm with a min-heap, removing letters with nothing before them.", "O(C log A)", "O(A)"))


@B
def alien_order(words):
    letters = sorted(set("".join(words)))
    before = {c: set() for c in letters}
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                before[y].add(x)
                break
        else:
            if len(a) > len(b):
                return ""
    out = []
    while letters:
        ready = [c for c in letters if not before[c] - set(out)]
        if not ready:
            return ""
        out.append(ready[0])
        letters.remove(ready[0])
    return "".join(out)


@O
def alien_order(words):
    after = {c: set() for w in words for c in w}
    indegree = {c: 0 for c in after}
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                if y not in after[x]:
                    after[x].add(y)
                    indegree[y] += 1
                break
        else:
            if len(a) > len(b):
                return ""
    ready = [c for c in indegree if indegree[c] == 0]
    heapq.heapify(ready)
    out = []
    while ready:
        c = heapq.heappop(ready)
        out.append(c)
        for d in after[c]:
            indegree[d] -= 1
            if indegree[d] == 0:
                heapq.heappush(ready, d)
    return "".join(out) if len(out) == len(after) else ""


Q(None, "Weighted Random Pick", "Medium", "Prefix sums + binary search",
  "Given weights and a number r in [0, total), return the chosen index. (Real code would draw r at random.)",
  [(([1, 3, 2], 0), 0), (([1, 3, 2], 3.5), 1), (([1, 3, 2], 5.9), 2)],
  ("Walk the weights, subtracting.", "O(n) per pick", "O(1)"),
  ("Precompute prefix sums, then binary search.", "O(log n) per pick", "O(n)"),
  names=["weights", "r"])


@B
def weighted_pick(weights, r):
    for i, w in enumerate(weights):
        if r < w:
            return i
        r -= w
    return len(weights) - 1


@O
def weighted_pick(weights, r):
    import bisect
    import itertools
    return bisect.bisect_right(list(itertools.accumulate(weights)), r)
