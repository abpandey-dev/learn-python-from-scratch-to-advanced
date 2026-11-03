# Python DSA Visualizer

Interactive, step-by-step lessons for learning data structures and algorithms in Python. Each lesson shows the data as clickable boxes, the Python code with the running line highlighted, and a plain-English explanation of every step.

**Live site:** https://abpandey-dev.github.io/python-dsa-visualizer/

## [Python IDE](ide/) — write and run Python in the browser

**Open it:** https://abpandey-dev.github.io/python-dsa-visualizer/ide/

- Real Python 3.12 running in the browser (Pyodide) — nothing to install.
- Editor with syntax highlighting, auto-indent, bracket matching and Ctrl/⌘ + Enter to run.
- An **Input** box feeds `input()`, errors point to the line with a beginner-friendly hint, and **Stop** ends infinite loops.
- **Visualize** runs your own code step by step: every variable, list, dict, object, the call stack and the printed output.
- Every practice question has **Solve it yourself**: it opens a starter function and a **Check** button that runs the question's tests. Every answer and lesson example has **Open in editor**.
- **Share** copies a link that contains your code.

## [Python from Scratch](python-course/) — 12 topics · 240 practice questions

A full course for someone writing their first line of Python. Each topic has a **Theory** tab (definitions, rules, tables, common mistakes and theory questions with answers), **Lessons** from the basics to advanced use, and **20 practice questions**, each answered twice — a brute-force "long way" and an optimal "Pythonic way". Every lesson example and every answer can be watched **running line by line**: variables, objects, the call stack and printed output update at each step, like Python Tutor.

**Open it:** https://abpandey-dev.github.io/python-dsa-visualizer/python-course/ · [Full question list](python-course/README.md)

| # | Topic | Covers |
|---|---|---|
| 1 | Python Basics | print, variables, data types, type conversion, input |
| 2 | Operators & Expressions | arithmetic, comparison, logical, assignment, precedence, bitwise |
| 3 | Conditions | if / elif / else, nesting, conditional expressions, match-case |
| 4 | Loops | for, range, while, break / continue / else, nested loops |
| 5 | Strings | indexing, slicing, methods, immutability, formatting |
| 6 | Lists | methods, aliasing and copying, sorting, 2-D lists |
| 7 | Tuples & Sets | unpacking, hashability, set operations |
| 8 | Dictionaries | lookups, counting, grouping, nesting, comprehensions |
| 9 | Functions & Recursion | parameters, *args/**kwargs, scope, lambdas, closures, recursion, memoisation |
| 10 | Comprehensions, Iterators & Generators | comprehensions, built-ins, iterator protocol, yield, itertools |
| 11 | Object-Oriented Programming | classes, properties, inheritance, polymorphism, dunder methods, dataclasses |
| 12 | Errors, Exceptions & Files | try / except / else / finally, custom exceptions, files, context managers |

## [DSA Interview Handbook](handbook/) — 14 topics · 280 questions

The 14 core DSA topics. Each topic has a **Theory** tab (definition, types, operations and their cost, pros and cons, applications, comparisons, and theory questions with model answers), a **Lessons** tab that teaches it from scratch to advanced in 5–8 short animated lessons, a one-card **Quick reference**, and the **top 20 most-asked interview questions**. Each question has a brute-force solution, the optimal solution, time and space complexity, and a step-by-step animation of the optimal code running. Search by title, LeetCode number or pattern.

**Open it:** https://abpandey-dev.github.io/python-dsa-visualizer/handbook/ · [Full question list](handbook/README.md)

| # | Topic | Covers |
|---|---|---|
| 1 | Arrays & Hashing | hash maps, prefix sums, Kadane, in-place tricks |
| 2 | Two Pointers | opposite ends, read/write pointers, 3Sum |
| 3 | Sliding Window | fixed and variable windows, monotonic deque |
| 4 | Stack & Queue | matching, monotonic stack, design problems |
| 5 | Binary Search | on arrays, rotated arrays, on the answer |
| 6 | Linked List | dummy head, fast/slow, reversal, LRU cache |
| 7 | Trees & BST | DFS orders, BFS levels, BST rules, path sums |
| 8 | Heap / Priority Queue | top-k, two heaps, scheduling |
| 9 | Recursion & Backtracking | subsets, permutations, N-Queens, Sudoku |
| 10 | Graphs | BFS/DFS, topological sort, union-find, Dijkstra, MST |
| 11 | Dynamic Programming | 1-D, knapsack, two strings, grid, interval |
| 12 | Greedy & Intervals | merge, schedule, sweep line, two-pass |
| 13 | Tries | prefix trees, autocomplete, Word Search II, binary XOR tries |
| 14 | Bit Manipulation | XOR tricks, n & (n − 1), masks, prefix XOR |

## Lessons

### [Python Array Lab](array-lab.html)

| Level | Topic |
|---|---|
| Basic | Indexing and negative indexes |
| Basic | Slicing (`start:stop:step`) |
| Core | Subarray vs subsequence, listing every subarray |
| Core | Prefix sum and range sum in one subtraction |
| Core | Suffix sum |
| Advanced | Product of array except self |
| Advanced | Maximum subarray sum (Kadane's algorithm) |

### [Python Bit Lab](bit-lab.html)

| Level | Topic |
|---|---|
| Basic | Binary numbers and decimal-to-binary conversion |
| Basic | AND, OR, XOR with truth tables |
| Basic | Left shift, right shift and NOT |
| Core | Check, set, clear and toggle bit `i` |
| Core | `n & (n - 1)` tricks and counting set bits |
| Advanced | XOR single number |
| Advanced | Generating all subsets with bitmasks |

## Run locally

Every lesson page is a single HTML file with no build step. Open `index.html` in a browser.

The handbook is generated from the Python sources in `handbook/src/topics/`. `build.py` runs every brute-force and optimal solution against its tests, records the optimal run as animation frames, and writes `handbook/data/`:

```bash
python3 handbook/build.py
```

```bash
python3 handbook/build.py --book python-course
```

To view it locally, serve the folder (the page loads its data files lazily):

```bash
python3 -m http.server 8000
```

## Practice problems

LeetCode 53, 78, 136, 191, 231, 238, 268, 303 and 724.
