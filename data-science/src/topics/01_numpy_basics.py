from lib import *
import numpy as np

TOPIC(
    id="numpy-basics", title="NumPy Basics", glyph="ndarray",
    blurb="Arrays: creating them, their shape and dtype, indexing, slicing, reshaping and fancy indexing.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">import numpy as np
a = np.array([1, 2, 3])            # from a list
np.zeros(3), np.ones((2, 3)), np.full(4, 7)
np.arange(0, 10, 2)                # like range → array([0, 2, 4, 6, 8])
np.linspace(0, 1, 5)               # 5 evenly spaced numbers
np.eye(3)                          # identity matrix
a.shape, a.ndim, a.size, a.dtype   # (3,), 1, 3, int64
m[1, 2], m[:, 0], m[:2, :2]        # row 1 col 2, first column, top-left block
a[a &gt; 1]                           # boolean mask
a[[0, 2]]                          # fancy indexing
a.reshape(3, 1), m.ravel(), a.astype(float)</code></pre>
<p>Slices are <b>views</b> (share memory); use <code>.copy()</code> for an independent array.</p>
""")


Q(None, "Double Every Number", "Easy", "Vectorised arithmetic",
  "Given a list of numbers, return every number doubled.",
  [(([1, 2, 3],), [2, 4, 6]), (([],), []), (([-1.5, 4],), [-3.0, 8])],
  ("A Python loop that multiplies each item and appends it.", "O(n) — interpreted loop", "O(n)"),
  ("Turn the list into an array; <code>arr * 2</code> multiplies every element at once in fast compiled code.", "O(n) — vectorised", "O(n)"),
  viz=([1, 2, 3, 4],))


@B
def double(nums):
    out = []
    for x in nums:
        out.append(x * 2)
    return out


@O
def double(nums):
    arr = np.array(nums)
    return arr * 2


Q(None, "Shape and Size", "Easy", "shape · size · ndim",
  "Given a rectangular nested list (a table), return <code>(rows, columns, total_items)</code>.",
  [(([[1, 2, 3], [4, 5, 6]],), (2, 3, 6)), (([[7]],), (1, 1, 1))],
  ("Count rows with len, columns with len of the first row, multiply.", "O(1)", "O(1)"),
  ("<code>arr.shape</code> is (rows, cols) and <code>arr.size</code> is the total.", "O(n) to build", "O(n)"))


@B
def shape_size(table):
    rows = len(table)
    cols = len(table[0])
    total = rows * cols
    return (rows, cols, total)


@O
def shape_size(table):
    arr = np.array(table)
    rows, cols = arr.shape
    return (rows, cols, arr.size)


Q(None, "Evenly Spaced Numbers", "Easy", "linspace",
  "Return <code>n</code> numbers evenly spaced from <code>start</code> to <code>stop</code> (both included), rounded to 2 decimals.",
  [((0, 1, 5), [0.0, 0.25, 0.5, 0.75, 1.0]), ((10, 20, 3), [10.0, 15.0, 20.0])],
  ("Work out the step (stop − start) / (n − 1) and add it in a loop.", "O(n)", "O(n)"),
  ("<code>np.linspace(start, stop, n)</code> does exactly this.", "O(n)", "O(n)"))


@B
def spaced(start, stop, n):
    step = (stop - start) / (n - 1)
    out = []
    for i in range(n):
        out.append(round(start + i * step, 2))
    return out


@O
def spaced(start, stop, n):
    return np.linspace(start, stop, n).round(2)


Q(None, "Identity Matrix", "Easy", "np.eye",
  "Return the n × n identity matrix (1 on the diagonal, 0 elsewhere) as integers.",
  [((3,), [[1, 0, 0], [0, 1, 0], [0, 0, 1]]), ((1,), [[1]])],
  ("Nested loops: 1 when row == column.", "O(n²)", "O(n²)"),
  ("<code>np.eye(n, dtype=int)</code>.", "O(n²)", "O(n²)"),
  viz=(3,))


@B
def identity(n):
    rows = []
    for r in range(n):
        row = []
        for c in range(n):
            row.append(1 if r == c else 0)
        rows.append(row)
    return rows


@O
def identity(n):
    return np.eye(n, dtype=int)


Q(None, "Read One Cell", "Easy", "2-D indexing",
  "Return the value at row <code>r</code>, column <code>c</code> of a table.",
  [(([[1, 2], [3, 4]], 1, 0), 3), (([[5, 6, 7]], 0, 2), 7)],
  ("Index twice: <code>table[r][c]</code>.", "O(1)", "O(1)"),
  ("NumPy takes both indices at once: <code>arr[r, c]</code>.", "O(1)", "O(n) to build"))


@B
def cell(table, r, c):
    row = table[r]
    return row[c]


@O
def cell(table, r, c):
    arr = np.array(table)
    return arr[r, c]


Q(None, "Last Column", "Easy", "Column slicing",
  "Return the last column of a table as a list.",
  [(([[1, 2, 3], [4, 5, 6]],), [3, 6]), (([[9]],), [9])],
  ("Loop over rows and take each row's last item.", "O(rows)", "O(rows)"),
  ("<code>arr[:, -1]</code> — all rows, last column.", "O(rows)", "O(rows)"),
  viz=([[1, 2, 3], [4, 5, 6], [7, 8, 9]],))


@B
def last_column(table):
    col = []
    for row in table:
        col.append(row[-1])
    return col


@O
def last_column(table):
    arr = np.array(table)
    return arr[:, -1]


Q(None, "Reverse an Array", "Easy", "Slicing with step −1",
  "Return the numbers in reverse order.",
  [(([1, 2, 3],), [3, 2, 1]), (([],), [])],
  ("Loop from the last index down to 0.", "O(n)", "O(n)"),
  ("<code>arr[::-1]</code> — a reversed view, no copying loop.", "O(1) view", "O(1)"))


@B
def reverse(nums):
    out = []
    for i in range(len(nums) - 1, -1, -1):
        out.append(nums[i])
    return out


@O
def reverse(nums):
    return np.array(nums)[::-1]


Q(None, "Every Second Element", "Easy", "Step slicing",
  "Return the elements at positions 0, 2, 4, …",
  [(([10, 11, 12, 13, 14],), [10, 12, 14]), (([5],), [5])],
  ("Loop over indices with a step of 2.", "O(n)", "O(n)"),
  ("<code>arr[::2]</code>.", "O(1) view", "O(1)"))


@B
def every_second(nums):
    out = []
    for i in range(0, len(nums), 2):
        out.append(nums[i])
    return out


@O
def every_second(nums):
    return np.array(nums)[::2]


Q(None, "Top-Left Block", "Easy", "2-D slicing",
  "Return the top-left k × k block of a table.",
  [(([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2), [[1, 2], [4, 5]]), (([[1, 2], [3, 4]], 1), [[1]])],
  ("Nested loops over the first k rows and columns.", "O(k²)", "O(k²)"),
  ("<code>arr[:k, :k]</code>.", "O(1) view", "O(1)"),
  viz=([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2))


@B
def top_left(table, k):
    block = []
    for r in range(k):
        row = []
        for c in range(k):
            row.append(table[r][c])
        block.append(row)
    return block


@O
def top_left(table, k):
    arr = np.array(table)
    return arr[:k, :k]


Q(None, "Count Values Above a Threshold", "Easy", "Boolean arrays",
  "Return how many numbers are greater than <code>t</code>.",
  [(([3, 8, 1, 9, 5], 4), 3), (([1, 2], 10), 0)],
  ("Loop and count.", "O(n)", "O(1)"),
  ("<code>arr &gt; t</code> gives an array of True/False; <code>.sum()</code> counts the Trues.", "O(n)", "O(n)"),
  viz=([3, 8, 1, 9, 5], 4))


@B
def count_above(nums, t):
    count = 0
    for x in nums:
        if x > t:
            count += 1
    return count


@O
def count_above(nums, t):
    arr = np.array(nums)
    mask = arr > t
    return mask.sum()


Q(None, "Replace Negatives With Zero", "Easy", "np.where",
  "Return the numbers with every negative value replaced by 0.",
  [(([3, -1, 4, -5],), [3, 0, 4, 0]), (([],), [])],
  ("Loop with an if.", "O(n)", "O(n)"),
  ("<code>np.where(arr &lt; 0, 0, arr)</code> picks 0 where the condition holds, otherwise the value. (<code>np.maximum(arr, 0)</code> also works.)", "O(n)", "O(n)"),
  viz=([3, -1, 4, -5],))


@B
def no_negatives(nums):
    out = []
    for x in nums:
        if x < 0:
            out.append(0)
        else:
            out.append(x)
    return out


@O
def no_negatives(nums):
    arr = np.array(nums)
    return np.where(arr < 0, 0, arr)


Q(None, "Floats to Whole Numbers", "Easy", "astype",
  "Convert decimal numbers to whole numbers by dropping the decimals (2.9 → 2, −2.9 → −2).",
  [(([2.9, -2.9, 5.0],), [2, -2, 5]), (([0.5],), [0])],
  ("Call <code>int()</code> on each number.", "O(n)", "O(n)"),
  ("<code>arr.astype(int)</code> converts the whole array's dtype (truncating toward zero).", "O(n)", "O(n)"))


@B
def to_ints(nums):
    out = []
    for x in nums:
        out.append(int(x))
    return out


@O
def to_ints(nums):
    return np.array(nums).astype(int)


Q(None, "Flatten a Table", "Easy", "ravel / flatten",
  "Turn a 2-D table into one flat list, row by row.",
  [(([[1, 2], [3, 4], [5, 6]],), [1, 2, 3, 4, 5, 6])],
  ("Two nested loops.", "O(n)", "O(n)"),
  ("<code>arr.ravel()</code> (a view when possible) or <code>arr.flatten()</code> (always a copy).", "O(n)", "O(n)"),
  viz=([[1, 2], [3, 4], [5, 6]],))


@B
def flatten(table):
    flat = []
    for row in table:
        for x in row:
            flat.append(x)
    return flat


@O
def flatten(table):
    return np.array(table).ravel()


Q(None, "Reshape Into Rows", "Easy", "reshape",
  "Arrange a flat list of numbers into a table with <code>rows</code> rows (it always divides evenly).",
  [(([1, 2, 3, 4, 5, 6], 2), [[1, 2, 3], [4, 5, 6]]), (([1, 2, 3, 4], 4), [[1], [2], [3], [4]])],
  ("Compute the row length and slice the list row by row.", "O(n)", "O(n)"),
  ("<code>arr.reshape(rows, -1)</code>; −1 tells NumPy to work out the column count.", "O(1) view", "O(1)"),
  viz=([1, 2, 3, 4, 5, 6], 2))


@B
def reshape_rows(nums, rows):
    cols = len(nums) // rows
    table = []
    for r in range(rows):
        table.append(nums[r * cols:(r + 1) * cols])
    return table


@O
def reshape_rows(nums, rows):
    return np.array(nums).reshape(rows, -1)


Q(None, "Stack Two Rows", "Easy", "vstack / hstack",
  "Put two equal-length lists on top of each other as a 2-row table.",
  [(([1, 2, 3], [4, 5, 6]), [[1, 2, 3], [4, 5, 6]])],
  ("Build a list containing copies of both lists.", "O(n)", "O(n)"),
  ("<code>np.vstack([a, b])</code> stacks vertically (<code>hstack</code> joins side by side).", "O(n)", "O(n)"))


@B
def stack_rows(a, b):
    return [list(a), list(b)]


@O
def stack_rows(a, b):
    return np.vstack([a, b])


Q(None, "Main Diagonal", "Easy", "np.diag",
  "Return the values on the main diagonal of a square table.",
  [(([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [1, 5, 9]), (([[4]],), [4])],
  ("Loop i and take <code>table[i][i]</code>.", "O(n)", "O(n)"),
  ("<code>np.diag(arr)</code> (also <code>arr.diagonal()</code>).", "O(n)", "O(n)"),
  viz=([[1, 2, 3], [4, 5, 6], [7, 8, 9]],))


@B
def diagonal(table):
    out = []
    for i in range(len(table)):
        out.append(table[i][i])
    return out


@O
def diagonal(table):
    return np.diag(np.array(table))


Q(None, "Position of the Largest Value", "Easy", "argmax",
  "Return the index of the largest number (first one on ties).",
  [(([4, 9, 2, 9],), 1), (([-3, -1],), 1)],
  ("Track the best index in a loop.", "O(n)", "O(1)"),
  ("<code>arr.argmax()</code>.", "O(n)", "O(n)"),
  viz=([4, 9, 2, 9],))


@B
def argmax(nums):
    best = 0
    for i in range(1, len(nums)):
        if nums[i] > nums[best]:
            best = i
    return best


@O
def argmax(nums):
    return np.array(nums).argmax()


Q(None, "Unique Values and Their Counts", "Medium", "np.unique",
  "Return <code>(sorted unique values, how many times each appears)</code>.",
  [(([3, 1, 3, 2, 1, 3],), ([1, 2, 3], [2, 1, 3])), (([5],), ([5], [1]))],
  ("Count with a dict, then sort the keys.", "O(n log n)", "O(n)"),
  ("<code>np.unique(arr, return_counts=True)</code> returns both arrays.", "O(n log n)", "O(n)"),
  viz=([3, 1, 3, 2, 1, 3],))


@B
def unique_counts(nums):
    counts = {}
    for x in nums:
        counts[x] = counts.get(x, 0) + 1
    values = sorted(counts)
    return (values, [counts[v] for v in values])


@O
def unique_counts(nums):
    values, counts = np.unique(nums, return_counts=True)
    return (values, counts)


Q(None, "Pick Items by Position", "Easy", "Fancy indexing",
  "Return the items at the given list of positions, in that order.",
  [(([10, 20, 30, 40], [3, 0, 3]), [40, 10, 40]), (([5, 6], []), [])],
  ("Loop over the positions.", "O(k)", "O(k)"),
  ("Index with a list of positions: <code>arr[positions]</code>.", "O(k)", "O(k)"))


@B
def pick(nums, positions):
    out = []
    for p in positions:
        out.append(nums[p])
    return out


@O
def pick(nums, positions):
    return np.array(nums)[np.array(positions, dtype=int)]


Q(None, "Checkerboard", "Medium", "Index arithmetic",
  "Return an n × n checkerboard of 0s and 1s with 0 in the top-left corner.",
  [((3,), [[0, 1, 0], [1, 0, 1], [0, 1, 0]]), ((1,), [[0]])],
  ("Nested loops with (row + col) % 2.", "O(n²)", "O(n²)"),
  ("<code>np.indices((n, n)).sum(axis=0) % 2</code> builds every row+col sum at once.", "O(n²)", "O(n²)"),
  viz=(4,))


@B
def checkerboard(n):
    board = []
    for r in range(n):
        board.append([(r + c) % 2 for c in range(n)])
    return board


@O
def checkerboard(n):
    rows, cols = np.indices((n, n))
    return (rows + cols) % 2
