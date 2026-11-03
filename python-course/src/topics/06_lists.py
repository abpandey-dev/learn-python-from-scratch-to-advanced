from lib import *

TOPIC(
    id="lists", title="Lists", glyph="[1, 2]",
    blurb="Ordered, changeable collections: indexing, methods, slicing, copying, sorting and lists of lists.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">nums = [3, 1, 4]
nums.append(1)        # [3, 1, 4, 1]
nums.insert(0, 9)     # [9, 3, 1, 4, 1]
nums.remove(1)        # removes the first 1
x = nums.pop()        # removes and returns the last item
nums.sort()           # sorts in place, returns None
new = sorted(nums)    # returns a new sorted list
nums.index(4), nums.count(1), len(nums), 4 in nums
copy = nums[:]        # or nums.copy() / list(nums)
grid = [[0] * 3 for _ in range(2)]   # 2 x 3, rows independent</code></pre>
<ul>
<li>Lists are <b>mutable</b>: <code>b = a</code> makes two names for one list.</li>
<li><code>append</code>/<code>pop()</code> at the end are fast; <code>insert(0, x)</code>/<code>pop(0)</code> are slow.</li>
</ul>
""")


Q(None, "Sum of a List", "Easy", "Accumulator vs sum()",
  "Return the sum of the numbers in a list.",
  [(([4, 8, 15],), 27), (([],), 0), (([-2, 2],), 0)],
  ("Loop over indices and add.", "O(n)", "O(1)"),
  ("The built-in <code>sum()</code>.", "O(n)", "O(1)"),
  viz=([4, 8, 15],))


@B
def list_sum(nums):
    total = 0
    for i in range(len(nums)):
        total = total + nums[i]
    return total


@O
def list_sum(nums):
    return sum(nums)


Q(None, "Average of a List", "Easy", "sum / len",
  "Return the average of a list rounded to 2 decimals, or 0 for an empty list.",
  [(([2, 4, 9],), 5.0), (([1, 2],), 1.5), (([],), 0)],
  ("Count and add in one loop.", "O(n)", "O(1)"),
  ("<code>sum(nums) / len(nums)</code> with an empty-list guard.", "O(n)", "O(1)"))


@B
def average(nums):
    total, count = 0, 0
    for x in nums:
        total += x
        count += 1
    if count == 0:
        return 0
    return round(total / count, 2)


@O
def average(nums):
    return round(sum(nums) / len(nums), 2) if nums else 0


Q(None, "Remove Duplicates, Keep Order", "Easy", "in vs dict",
  "Return a new list with duplicates removed, keeping the first occurrence of each value in order.",
  [(([3, 1, 3, 2, 1],), [3, 1, 2]), (([],), []), ((["a", "a"],), ["a"])],
  ("Append each value if it's not already in the result list (each <code>in</code> scans the list).", "O(n²)", "O(n)"),
  ("<code>dict.fromkeys</code> keeps the first occurrence and insertion order; checking a dict is O(1).", "O(n)", "O(n)"),
  viz=([3, 1, 3, 2, 1],))


@B
def dedupe(items):
    result = []
    for x in items:
        if x not in result:
            result.append(x)
    return result


@O
def dedupe(items):
    return list(dict.fromkeys(items))


Q(None, "Second Largest", "Medium", "One pass",
  "Return the second largest distinct value, or None if it doesn't exist.",
  [(([4, 9, 2, 9, 7],), 7), (([5, 5],), None), (([1, 2],), 1)],
  ("Remove duplicates, sort, take the second from the end.", "O(n log n)", "O(n)"),
  ("Track the largest and second largest in one pass.", "O(n)", "O(1)"),
  viz=([4, 9, 2, 9, 7],))


@B
def second_largest(nums):
    unique = sorted(set(nums))
    if len(unique) < 2:
        return None
    return unique[-2]


@O
def second_largest(nums):
    first = second = None
    for x in nums:
        if first is None or x > first:
            first, second = x, first
        elif x != first and (second is None or x > second):
            second = x
    return second


Q(None, "Reverse a List in Place", "Easy", "Swapping",
  "Reverse the list <b>in place</b> (change the given list) and return it.",
  [(([1, 2, 3, 4],), [4, 3, 2, 1]), (([7],), [7]), (([],), [])],
  ("Swap the first and last, then move inward, with explicit indices.", "O(n)", "O(1)"),
  ("<code>items.reverse()</code> does exactly this.", "O(n)", "O(1)"),
  viz=([1, 2, 3, 4, 5],))


@B
def reverse_in_place(items):
    i, j = 0, len(items) - 1
    while i < j:
        temp = items[i]
        items[i] = items[j]
        items[j] = temp
        i += 1
        j -= 1
    return items


@O
def reverse_in_place(items):
    items.reverse()
    return items


Q(None, "Rotate Right by k", "Medium", "Slicing",
  "Return a new list rotated right by k: [1,2,3,4,5], k=2 → [4,5,1,2,3].",
  [(([1, 2, 3, 4, 5], 2), [4, 5, 1, 2, 3]), (([1, 2, 3], 4), [3, 1, 2]), (([], 3), [])],
  ("Move the last item to the front, k times.", "O(n · k)", "O(n)"),
  ("Two slices: the last k items followed by the rest (k taken modulo the length).", "O(n)", "O(n)"),
  viz=([1, 2, 3, 4, 5], 2))


@B
def rotate(items, k):
    result = items[:]
    for _ in range(k):
        if result:
            last = result.pop()
            result.insert(0, last)
    return result


@O
def rotate(items, k):
    if not items:
        return []
    k %= len(items)
    return items[-k:] + items[:-k] if k else items[:]


Q(None, "Merge Two Sorted Lists", "Medium", "Two indices",
  "Merge two sorted lists into one sorted list.",
  [(([1, 4, 7], [2, 3, 8]), [1, 2, 3, 4, 7, 8]), (([], [1]), [1]), (([1, 1], [1]), [1, 1, 1])],
  ("Join them and sort the result.", "O((m+n) log(m+n))", "O(m+n)"),
  ("Walk both lists with two indices, always taking the smaller head.", "O(m + n)", "O(m+n)"),
  viz=([1, 4, 7], [2, 3, 8]))


@B
def merge_sorted(a, b):
    merged = a + b
    merged.sort()
    return merged


@O
def merge_sorted(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    return out + a[i:] + b[j:]


Q(None, "Flatten a List of Lists", "Easy", "Nested loops vs comprehension",
  "Turn <code>[[1, 2], [3], [4, 5]]</code> into <code>[1, 2, 3, 4, 5]</code>.",
  [(([[1, 2], [3], [4, 5]],), [1, 2, 3, 4, 5]), (([[], [1]],), [1])],
  ("Two nested loops appending each item.", "O(total)", "O(total)"),
  ("A nested list comprehension reads in the same order as the loops.", "O(total)", "O(total)"),
  viz=([[1, 2], [3], [4, 5]],))


@B
def flatten(grid):
    flat = []
    for row in grid:
        for x in row:
            flat.append(x)
    return flat


@O
def flatten(grid):
    return [x for row in grid for x in row]


Q(None, "Count Occurrences", "Easy", "count()",
  "Return how many times <code>value</code> appears in the list.",
  [(([1, 2, 1, 1], 1), 3), ((["a", "b"], "c"), 0)],
  ("Loop and count matches.", "O(n)", "O(1)"),
  ("<code>items.count(value)</code>.", "O(n)", "O(1)"))


@B
def occurrences(items, value):
    count = 0
    for x in items:
        if x == value:
            count += 1
    return count


@O
def occurrences(items, value):
    return items.count(value)


Q(None, "Common Elements", "Medium", "Nested loop vs set",
  "Return the values that appear in both lists, without duplicates, in the order they appear in <code>a</code>.",
  [(([1, 2, 3, 2, 4], [2, 4, 6]), [2, 4]), (([1, 2], [3]), [])],
  ("For each item of a, scan b; also check the result to avoid duplicates.", "O(m · n)", "O(k)"),
  ("Put b in a set for O(1) lookups and track what you've already added.", "O(m + n)", "O(n)"),
  viz=([1, 2, 3, 2, 4], [2, 4, 6]))


@B
def common(a, b):
    result = []
    for x in a:
        for y in b:
            if x == y and x not in result:
                result.append(x)
    return result


@O
def common(a, b):
    in_b, seen, result = set(b), set(), []
    for x in a:
        if x in in_b and x not in seen:
            seen.add(x)
            result.append(x)
    return result


Q(None, "Move Zeros to the End", "Medium", "In-place write index",
  "Move every 0 to the end of the list in place, keeping the order of the other numbers. Return the list.",
  [(([0, 1, 0, 3, 12],), [1, 3, 12, 0, 0]), (([0],), [0]), (([1, 2],), [1, 2])],
  ("Count the zeros, remove them one by one with <code>remove</code>, then append that many zeros.", "O(n²)", "O(1)"),
  ("A write index copies every non-zero forward, then fill the rest with zeros.", "O(n)", "O(1)"),
  viz=([0, 1, 0, 3, 12],))


@B
def move_zeros(nums):
    zeros = nums.count(0)
    for _ in range(zeros):
        nums.remove(0)
    for _ in range(zeros):
        nums.append(0)
    return nums


@O
def move_zeros(nums):
    w = 0
    for x in nums:
        if x != 0:
            nums[w] = x
            w += 1
    for i in range(w, len(nums)):
        nums[i] = 0
    return nums


Q(None, "Split Into Chunks", "Easy", "Slicing with a step",
  "Split a list into pieces of size k (the last piece may be shorter).",
  [(([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]]), (([], 3), []), (([1, 2], 5), [[1, 2]])],
  ("Collect items into a current chunk; when it's full, store it and start a new one.", "O(n)", "O(n)"),
  ("Slices <code>items[i:i + k]</code> for i in <code>range(0, n, k)</code>.", "O(n)", "O(n)"),
  viz=([1, 2, 3, 4, 5], 2))


@B
def chunks(items, k):
    result, current = [], []
    for x in items:
        current.append(x)
        if len(current) == k:
            result.append(current)
            current = []
    if current:
        result.append(current)
    return result


@O
def chunks(items, k):
    return [items[i:i + k] for i in range(0, len(items), k)]


Q(None, "Running Total", "Easy", "Prefix sums",
  "Return the running totals: [1, 2, 3, 4] → [1, 3, 6, 10].",
  [(([1, 2, 3, 4],), [1, 3, 6, 10]), (([5],), [5]), (([],), [])],
  ("For each position, sum the slice up to it from scratch.", "O(n²)", "O(n)"),
  ("Keep one running total and append it each step (or <code>itertools.accumulate</code>).", "O(n)", "O(n)"),
  viz=([1, 2, 3, 4],))


@B
def running_total(nums):
    result = []
    for i in range(len(nums)):
        result.append(sum(nums[:i + 1]))
    return result


@O
def running_total(nums):
    result, total = [], 0
    for x in nums:
        total += x
        result.append(total)
    return result


Q(None, "Transpose a Matrix", "Medium", "Lists of lists · zip",
  "Swap rows and columns: [[1, 2, 3], [4, 5, 6]] → [[1, 4], [2, 5], [3, 6]].",
  [(([[1, 2, 3], [4, 5, 6]],), [[1, 4], [2, 5], [3, 6]]), (([[1]],), [[1]])],
  ("Build each new row by walking down a column with nested loops.", "O(m · n)", "O(m · n)"),
  ("<code>zip(*matrix)</code> pairs up the columns.", "O(m · n)", "O(m · n)"),
  viz=([[1, 2, 3], [4, 5, 6]],))


@B
def transpose(matrix):
    rows, cols = len(matrix), len(matrix[0])
    result = []
    for c in range(cols):
        new_row = []
        for r in range(rows):
            new_row.append(matrix[r][c])
        result.append(new_row)
    return result


@O
def transpose(matrix):
    return [list(col) for col in zip(*matrix)]


Q(None, "Product of a List", "Easy", "math.prod",
  "Return the product of all numbers (1 for an empty list).",
  [(([2, 3, 4],), 24), (([],), 1), (([5, 0, 2],), 0)],
  ("Multiply in a loop.", "O(n)", "O(1)"),
  ("<code>math.prod(nums)</code>.", "O(n)", "O(1)"))


@B
def product(nums):
    result = 1
    for x in nums:
        result *= x
    return result


@O
def product(nums):
    import math
    return math.prod(nums)


Q(None, "Remove Every Copy of a Value", "Easy", "remove() vs comprehension",
  "Return a new list without any occurrence of <code>value</code>.",
  [(([1, 2, 1, 3, 1], 1), [2, 3]), (([2], 1), [2])],
  ("Copy the list and call <code>remove</code> while the value is still in it (each call scans).", "O(n²)", "O(n)"),
  ("Keep only the other values with a comprehension.", "O(n)", "O(n)"),
  viz=([1, 2, 1, 3, 1], 1))


@B
def without(items, value):
    result = items[:]
    while value in result:
        result.remove(value)
    return result


@O
def without(items, value):
    return [x for x in items if x != value]


Q(None, "Index of the Maximum", "Easy", "max with key",
  "Return the index of the largest value (first one if repeated).",
  [(([3, 9, 2, 9],), 1), (([5],), 0), (([-1, -3],), 0)],
  ("Track the best index while looping.", "O(n)", "O(1)"),
  ("<code>max(range(len(nums)), key=nums.__getitem__)</code>, or <code>nums.index(max(nums))</code>.", "O(n)", "O(1)"),
  viz=([3, 9, 2, 9],))


@B
def argmax(nums):
    best = 0
    for i in range(1, len(nums)):
        if nums[i] > nums[best]:
            best = i
    return best


@O
def argmax(nums):
    return nums.index(max(nums))


Q(None, "Is the List Sorted?", "Easy", "Neighbour pairs",
  "Return True if the list is in non-decreasing order.",
  [(([1, 2, 2, 5],), True), (([3, 1],), False), (([],), True)],
  ("Sort a copy and compare.", "O(n log n)", "O(n)"),
  ("Every neighbour pair must be in order; <code>all</code> stops at the first bad pair.", "O(n)", "O(1)"),
  viz=([1, 2, 5, 4],))


@B
def is_sorted(nums):
    return nums == sorted(nums)


@O
def is_sorted(nums):
    return all(nums[i] <= nums[i + 1] for i in range(len(nums) - 1))


Q(None, "Separate Evens and Odds", "Easy", "Building two lists",
  "Return <code>(evens, odds)</code> keeping the original order in each.",
  [(([1, 2, 3, 4, 5],), ([2, 4], [1, 3, 5])), (([],), ([], []))],
  ("Two separate loops, one per list.", "O(n)", "O(n)"),
  ("One loop that appends to the right list.", "O(n)", "O(n)"),
  viz=([1, 2, 3, 4, 5],))


@B
def split_parity(nums):
    evens = []
    for x in nums:
        if x % 2 == 0:
            evens.append(x)
    odds = []
    for x in nums:
        if x % 2 != 0:
            odds.append(x)
    return evens, odds


@O
def split_parity(nums):
    evens, odds = [], []
    for x in nums:
        (evens if x % 2 == 0 else odds).append(x)
    return evens, odds


Q(None, "Shopping Cart Total", "Easy", "List of pairs",
  "<code>cart</code> is a list of (price, quantity) pairs. Return the total cost rounded to 2 decimals.",
  [(([(2.5, 4), (10, 1)],), 20.0), (([],), 0), (([(0.99, 3)],), 2.97)],
  ("Loop with indices into each pair.", "O(n)", "O(1)"),
  ("Unpack each pair in a generator inside <code>sum</code>.", "O(n)", "O(1)"),
  viz=([(2.5, 4), (10, 1)],))


@B
def cart_total(cart):
    total = 0
    for i in range(len(cart)):
        price = cart[i][0]
        qty = cart[i][1]
        total += price * qty
    return round(total, 2)


@O
def cart_total(cart):
    return round(sum(price * qty for price, qty in cart), 2)
