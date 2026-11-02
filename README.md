# Python DSA Visualizer

Interactive, step-by-step lessons for learning data structures and algorithms in Python. Each lesson shows the data as clickable boxes, the Python code with the running line highlighted, and a plain-English explanation of every step.

**Live site:** https://abpandey-dev.github.io/python-dsa-visualizer/

## [DSA Interview Handbook](handbook/) — 14 topics · 280 questions

The 14 core DSA topics, each explained with an animated example, plus the **top 20 most-asked interview questions** for every topic. Each question has a brute-force solution, the optimal solution, time and space complexity, and a step-by-step animation of the optimal code running. Search by title, LeetCode number or pattern.

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

To view it locally, serve the folder (the page loads its data files lazily):

```bash
python3 -m http.server 8000
```

## Practice problems

LeetCode 53, 78, 136, 191, 231, 238, 268, 303 and 724.
