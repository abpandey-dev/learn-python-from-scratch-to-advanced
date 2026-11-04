from lib import *
import numpy as np

TOPIC(
    id="numpy-ops", title="NumPy Operations", glyph="a + b",
    blurb="Vectorised maths, aggregation along axes, broadcasting, matrix algebra and common numeric recipes.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">a + b, a * b, a ** 2, np.sqrt(a), np.exp(a)   # element-wise
a.sum(), a.mean(), a.std(), a.min(), a.max(), a.argmax()
m.sum(axis=0)        # down the rows → one value per column
m.mean(axis=1)       # across columns → one value per row
m + row              # broadcasting: row added to every row
a @ b, m @ v         # dot product / matrix multiplication
np.cumsum(a), np.diff(a), np.clip(a, lo, hi), np.sort(a), a.argsort()
np.linalg.solve(A, b), np.linalg.inv(A)</code></pre>
""")


Q(None, "Add Two Lists Element by Element", "Easy", "Element-wise +",
  "Return [a[0] + b[0], a[1] + b[1], …].",
  [(([1, 2, 3], [10, 20, 30]), [11, 22, 33]), (([], []), [])],
  ("Loop over the indices.", "O(n)", "O(n)"),
  ("Arrays add element by element: <code>np.array(a) + np.array(b)</code>.", "O(n) vectorised", "O(n)"))


@B
def add_lists(a, b):
    out = []
    for i in range(len(a)):
        out.append(a[i] + b[i])
    return out


@O
def add_lists(a, b):
    return np.array(a) + np.array(b)


Q(None, "Dot Product", "Easy", "@ / np.dot",
  "Return the dot product Σ a[i] × b[i].",
  [(([1, 2, 3], [4, 5, 6]), 32), (([2], [5]), 10)],
  ("Multiply pairs in a loop and add.", "O(n)", "O(1)"),
  ("<code>np.dot(a, b)</code> or <code>a @ b</code>.", "O(n)", "O(n)"),
  viz=([1, 2, 3], [4, 5, 6]))


@B
def dot(a, b):
    total = 0
    for x, y in zip(a, b):
        total += x * y
    return total


@O
def dot(a, b):
    return np.array(a) @ np.array(b)


Q(None, "Mean and Standard Deviation", "Easy", "Aggregations",
  "Return <code>(mean, standard deviation)</code> rounded to 2 decimals (population std).",
  [(([2, 4, 4, 4, 5, 5, 7, 9],), (5.0, 2.0)), (([10, 10],), (10.0, 0.0))],
  ("Compute the mean, then the average squared distance from it, then the square root.", "O(n)", "O(1)"),
  ("<code>arr.mean()</code> and <code>arr.std()</code>.", "O(n)", "O(n)"),
  viz=([2, 4, 4, 4, 5, 5, 7, 9],))


@B
def mean_std(nums):
    mean = sum(nums) / len(nums)
    squares = 0
    for x in nums:
        squares += (x - mean) ** 2
    std = (squares / len(nums)) ** 0.5
    return (round(mean, 2), round(std, 2))


@O
def mean_std(nums):
    arr = np.array(nums)
    return (round(arr.mean(), 2), round(arr.std(), 2))


Q(None, "Scale to 0–1 (Min-Max)", "Easy", "Vectorised formula",
  "Rescale numbers so the smallest becomes 0 and the largest 1: (x − min) / (max − min), rounded to 2 decimals.",
  [(([10, 20, 15, 30],), [0.0, 0.5, 0.25, 1.0]), (([5, 7],), [0.0, 1.0])],
  ("Find min and max, then apply the formula in a loop.", "O(n)", "O(n)"),
  ("Write the formula once on the whole array.", "O(n)", "O(n)"),
  viz=([10, 20, 15, 30],))


@B
def min_max_scale(nums):
    lo, hi = min(nums), max(nums)
    out = []
    for x in nums:
        out.append(round((x - lo) / (hi - lo), 2))
    return out


@O
def min_max_scale(nums):
    a = np.array(nums, dtype=float)
    return ((a - a.min()) / (a.max() - a.min())).round(2)


Q(None, "Z-Scores", "Medium", "Standardisation",
  "Return each value's z-score (x − mean) / std, rounded to 2 decimals.",
  [(([2, 4, 4, 4, 5, 5, 7, 9],), [-1.5, -0.5, -0.5, -0.5, 0.0, 0.0, 1.0, 2.0])],
  ("Compute mean and std by hand, then loop.", "O(n)", "O(n)"),
  ("<code>(a - a.mean()) / a.std()</code>.", "O(n)", "O(n)"),
  viz=([2, 4, 4, 4, 5, 5, 7, 9],))


@B
def z_scores(nums):
    n = len(nums)
    mean = sum(nums) / n
    std = (sum((x - mean) ** 2 for x in nums) / n) ** 0.5
    return [round((x - mean) / std, 2) for x in nums]


@O
def z_scores(nums):
    a = np.array(nums, dtype=float)
    return ((a - a.mean()) / a.std()).round(2)


Q(None, "Row Totals", "Easy", "sum(axis=1)",
  "Return the sum of each row of a table.",
  [(([[1, 2, 3], [4, 5, 6]],), [6, 15]), (([[7]],), [7])],
  ("Loop over rows and add each row.", "O(n)", "O(rows)"),
  ("<code>m.sum(axis=1)</code> adds across the columns.", "O(n)", "O(rows)"),
  viz=([[1, 2, 3], [4, 5, 6]],))


@B
def row_totals(table):
    out = []
    for row in table:
        total = 0
        for x in row:
            total += x
        out.append(total)
    return out


@O
def row_totals(table):
    return np.array(table).sum(axis=1)


Q(None, "Column Averages", "Easy", "mean(axis=0)",
  "Return the average of each column, rounded to 2 decimals.",
  [(([[1, 2], [3, 5], [5, 8]],), [3.0, 5.0]), (([[4, 9]],), [4.0, 9.0])],
  ("Loop over columns, then rows.", "O(n)", "O(cols)"),
  ("<code>m.mean(axis=0)</code> averages down the rows.", "O(n)", "O(cols)"),
  viz=([[1, 2], [3, 5], [5, 8]],))


@B
def column_means(table):
    cols = len(table[0])
    out = []
    for c in range(cols):
        total = 0
        for row in table:
            total += row[c]
        out.append(round(total / len(table), 2))
    return out


@O
def column_means(table):
    return np.array(table).mean(axis=0).round(2)


Q(None, "Add a Row to Every Row", "Medium", "Broadcasting",
  "Add the list <code>row</code> to every row of <code>table</code>.",
  [(([[1, 2], [3, 4]], [10, 100]), [[11, 102], [13, 104]])],
  ("Nested loops adding row[c] to every cell.", "O(n)", "O(n)"),
  ("Broadcasting stretches the 1-D row across all rows: <code>m + row</code>.", "O(n)", "O(n)"),
  viz=([[1, 2], [3, 4], [5, 6]], [10, 100]))


@B
def add_row(table, row):
    out = []
    for r in table:
        out.append([r[c] + row[c] for c in range(len(row))])
    return out


@O
def add_row(table, row):
    return np.array(table) + np.array(row)


Q(None, "Multiplication Table", "Easy", "Outer product",
  "Return the n × n table where cell (i, j) = (i + 1) × (j + 1).",
  [((3,), [[1, 2, 3], [2, 4, 6], [3, 6, 9]])],
  ("Nested loops.", "O(n²)", "O(n²)"),
  ("Broadcast a column against a row: <code>col * row</code> (or <code>np.outer</code>).", "O(n²)", "O(n²)"),
  viz=(4,))


@B
def times_table(n):
    return [[(i + 1) * (j + 1) for j in range(n)] for i in range(n)]


@O
def times_table(n):
    v = np.arange(1, n + 1)
    return v[:, np.newaxis] * v


Q(None, "Matrix Multiplication", "Medium", "@ operator",
  "Multiply matrix A (m × k) by matrix B (k × n).",
  [(([[1, 2], [3, 4]], [[5, 6], [7, 8]]), [[19, 22], [43, 50]]), (([[1, 2, 3]], [[1], [1], [1]]), [[6]])],
  ("Three nested loops: row of A times column of B.", "O(m·k·n) in Python", "O(m·n)"),
  ("<code>A @ B</code> — optimised BLAS code.", "O(m·k·n) in C", "O(m·n)"))


@B
def matmul(A, B):
    m, k, n = len(A), len(B), len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for t in range(k):
                C[i][j] += A[i][t] * B[t][j]
    return C


@O
def matmul(A, B):
    return np.array(A) @ np.array(B)


Q(None, "Transpose", "Easy", ".T",
  "Swap rows and columns.",
  [(([[1, 2, 3], [4, 5, 6]],), [[1, 4], [2, 5], [3, 6]])],
  ("Nested loops reading down each column.", "O(n)", "O(n)"),
  ("<code>m.T</code> — a view, no copying.", "O(1)", "O(1)"))


@B
def transpose(table):
    return [[table[r][c] for r in range(len(table))] for c in range(len(table[0]))]


@O
def transpose(table):
    return np.array(table).T


Q(None, "Running Total", "Easy", "cumsum",
  "Return the running totals of the numbers.",
  [(([1, 2, 3, 4],), [1, 3, 6, 10]), (([],), [])],
  ("Keep a total and append it each step.", "O(n)", "O(n)"),
  ("<code>np.cumsum</code>.", "O(n)", "O(n)"),
  viz=([1, 2, 3, 4],))


@B
def running_total(nums):
    out, total = [], 0
    for x in nums:
        total += x
        out.append(total)
    return out


@O
def running_total(nums):
    return np.cumsum(nums)


Q(None, "Moving Average", "Medium", "cumsum trick / convolve",
  "Return the average of every window of k consecutive numbers, rounded to 2 decimals.",
  [(([1, 2, 3, 4, 5], 2), [1.5, 2.5, 3.5, 4.5]), (([10, 20, 30], 3), [20.0])],
  ("Average each window from scratch.", "O(n·k)", "O(n)"),
  ("<code>np.convolve(a, np.ones(k) / k, mode='valid')</code> slides the window for you.", "O(n·k) in C", "O(n)"),
  viz=([1, 2, 3, 4, 5], 2))


@B
def moving_average(nums, k):
    out = []
    for i in range(len(nums) - k + 1):
        window = nums[i:i + k]
        out.append(round(sum(window) / k, 2))
    return out


@O
def moving_average(nums, k):
    return np.convolve(nums, np.ones(k) / k, mode="valid").round(2)


Q(None, "Clip to a Range", "Easy", "np.clip",
  "Limit every number to the range [lo, hi].",
  [(([-5, 3, 12, 7], 0, 10), [0, 3, 10, 7])],
  ("min/max per element in a loop.", "O(n)", "O(n)"),
  ("<code>np.clip(arr, lo, hi)</code>.", "O(n)", "O(n)"),
  viz=([-5, 3, 12, 7], 0, 10))


@B
def clip(nums, lo, hi):
    return [max(lo, min(x, hi)) for x in nums]


@O
def clip(nums, lo, hi):
    return np.clip(nums, lo, hi)


Q(None, "Keep the Even Numbers", "Easy", "Mask filtering",
  "Return only the even numbers.",
  [(([1, 2, 3, 4, 6],), [2, 4, 6]), (([1, 3],), [])],
  ("Loop with an if.", "O(n)", "O(n)"),
  ("<code>a[a % 2 == 0]</code>.", "O(n)", "O(n)"),
  viz=([1, 2, 3, 4, 6],))


@B
def evens(nums):
    return [x for x in nums if x % 2 == 0]


@O
def evens(nums):
    a = np.array(nums, dtype=int)
    return a[a % 2 == 0]


Q(None, "Day-to-Day Percent Change", "Medium", "np.diff",
  "Given daily prices, return the percent change from each day to the next, rounded to 1 decimal.",
  [(([100, 110, 99],), [10.0, -10.0]), (([50, 50],), [0.0])],
  ("Loop over neighbouring pairs.", "O(n)", "O(n)"),
  ("<code>np.diff(p) / p[:-1] * 100</code> — every pair at once.", "O(n)", "O(n)"),
  viz=([100, 110, 99, 121],))


@B
def pct_change(prices):
    out = []
    for i in range(1, len(prices)):
        out.append(round((prices[i] - prices[i - 1]) / prices[i - 1] * 100, 1))
    return out


@O
def pct_change(prices):
    p = np.array(prices, dtype=float)
    return (np.diff(p) / p[:-1] * 100).round(1)


Q(None, "Distance Matrix", "Hard", "Broadcasting in 2-D",
  "Given points (x, y), return the matrix of distances between every pair, rounded to 2 decimals.",
  [(([[0, 0], [3, 4], [6, 8]],), [[0.0, 5.0, 10.0], [5.0, 0.0, 5.0], [10.0, 5.0, 0.0]])],
  ("Two nested loops computing each distance.", "O(n²) in Python", "O(n²)"),
  ("Broadcast points against themselves: <code>P[:, None, :] − P[None, :, :]</code>, then take the norm along the last axis.", "O(n²) in C", "O(n²)"),
  viz=([[0, 0], [3, 4], [6, 8]],))


@B
def distances(points):
    n = len(points)
    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            D[i][j] = round((dx * dx + dy * dy) ** 0.5, 2)
    return D


@O
def distances(points):
    P = np.array(points, dtype=float)
    diff = P[:, np.newaxis, :] - P[np.newaxis, :, :]
    return np.sqrt((diff ** 2).sum(axis=-1)).round(2)


Q(None, "Solve Two Equations", "Medium", "np.linalg.solve",
  "Solve a·x + b·y = e and c·x + d·y = f. Input is [[a, b], [c, d]] and [e, f]; return [x, y] rounded to 2 decimals.",
  [(([[2, 1], [1, 3]], [3, 5]), [0.8, 1.4]), (([[1, 0], [0, 1]], [4, 7]), [4.0, 7.0])],
  ("Cramer's rule with determinants by hand.", "O(1) for 2×2", "O(1)"),
  ("<code>np.linalg.solve(A, b)</code> works for any size n × n system.", "O(n³)", "O(n²)"))


@B
def solve2(A, b):
    (a1, b1), (c1, d1) = A
    e, f = b
    det = a1 * d1 - b1 * c1
    x = (e * d1 - b1 * f) / det
    y = (a1 * f - e * c1) / det
    return [round(x, 2), round(y, 2)]


@O
def solve2(A, b):
    return np.linalg.solve(np.array(A, dtype=float), np.array(b, dtype=float)).round(2)


Q(None, "Count Each Value", "Easy", "np.bincount",
  "Dice rolls are numbers 1–6. Return how many times each face 1…6 appeared.",
  [(([1, 6, 6, 2, 1, 6],), [2, 1, 0, 0, 0, 3]), (([],), [0, 0, 0, 0, 0, 0])],
  ("A list of 6 counters updated in a loop.", "O(n)", "O(1)"),
  ("<code>np.bincount(rolls, minlength=7)[1:]</code>.", "O(n)", "O(1)"),
  viz=([1, 6, 6, 2, 1, 6, 3],))


@B
def face_counts(rolls):
    counts = [0] * 6
    for r in rolls:
        counts[r - 1] += 1
    return counts


@O
def face_counts(rolls):
    return np.bincount(np.array(rolls, dtype=int), minlength=7)[1:]


Q(None, "Sort Rows by a Column", "Medium", "argsort",
  "Sort the rows of a table by the values in column <code>c</code> (ascending).",
  [(([[3, 9], [1, 7], [2, 8]], 0), [[1, 7], [2, 8], [3, 9]]), (([[5, 1], [4, 2]], 1), [[5, 1], [4, 2]])],
  ("<code>sorted(table, key=lambda row: row[c])</code>.", "O(n log n)", "O(n)"),
  ("<code>m[m[:, c].argsort()]</code> — argsort gives the row order, fancy indexing applies it.", "O(n log n)", "O(n)"),
  viz=([[3, 9], [1, 7], [2, 8]], 0))


@B
def sort_rows(table, c):
    return sorted(table, key=lambda row: row[c])


@O
def sort_rows(table, c):
    m = np.array(table)
    order = m[:, c].argsort(kind="stable")
    return m[order]
