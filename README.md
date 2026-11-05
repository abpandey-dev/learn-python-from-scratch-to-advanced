# Learn Python: From Scratch to Advanced

A complete, interactive path for learning Python: a beginner course from the first line of code, Python for data science (NumPy, pandas, Matplotlib, Seaborn, statistics), the math behind data science and machine learning, machine learning from scratch, a DSA interview handbook, and an in-browser IDE. Every lesson and answer can be watched running line by line, with the data drawn as pictures and a plain-English explanation of each step.

**Live site:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/

## [Python IDE](ide/) — write and run Python in the browser

**Open it:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ide/

- Real Python 3.12 running in the browser (Pyodide) — nothing to install. NumPy, pandas, Matplotlib, Seaborn and scikit-learn load on first import, and charts appear under the output.
- Editor with syntax highlighting, auto-indent, bracket matching and Ctrl/⌘ + Enter to run.
- An **Input** box feeds `input()`, errors point to the line with a beginner-friendly hint, and **Stop** ends infinite loops.
- **Visualize** runs your own code step by step: every variable, list, dict, object, the call stack and the printed output.
- Every practice question has **Solve it yourself**: it opens a starter function and a **Check** button that runs the question's tests. Every answer and lesson example has **Open in editor**.
- **Share** copies a link that contains your code.

## [Python from Scratch](python-course/) — 12 topics · 240 practice questions

A full course for someone writing their first line of Python. Each topic has a **Theory** tab (definitions, rules, tables, common mistakes and theory questions with answers), **Lessons** from the basics to advanced use, and **20 practice questions**, each answered twice — a brute-force "long way" and an optimal "Pythonic way". Every lesson example and every answer can be watched **running line by line**: variables, objects, the call stack and printed output update at each step, like Python Tutor.

**Open it:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/python-course/ · [Full question list](python-course/README.md)

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

## [Python for Data Science](data-science/) — 8 topics · 160 practice questions

The next step after the Python course: the libraries data analysts use every day. Each topic has a **Theory** tab, **Lessons** from basics to advanced, and **20 practice questions**. Every question is answered twice — a **brute-force answer in plain Python** (loops and lists, so you see what the library does for you) and an **optimal answer using the library** — and both can be watched running line by line, with arrays and DataFrames shown as tables and every chart drawn as an image. Chart questions are checked by inspecting the figure (number of bars, titles, labels, colours).

**Open it:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/ · [Full question list](data-science/README.md)

| # | Topic | Covers |
|---|---|---|
| 1 | NumPy Basics | creating arrays, shape and dtype, indexing, slicing, reshaping, fancy indexing |
| 2 | NumPy Operations | vectorised maths, axes, broadcasting, matrix algebra, numeric recipes |
| 3 | Pandas Basics | Series, DataFrames, selecting with loc / iloc, filtering, sorting, new columns |
| 4 | Data Cleaning with Pandas | missing values, duplicates, types, text, dates, outliers |
| 5 | Grouping, Merging & Reshaping | groupby, merge, concat, pivot tables, melt, rolling windows |
| 6 | Matplotlib | line, bar, scatter, histogram, pie, box; labels, legends, subplots |
| 7 | Seaborn | distributions, categorical plots, relationships, heat maps, figure-level grids |
| 8 | Statistics for Data Analysis | mean / median / spread, outliers, correlation, regression, probability, confidence intervals |

The IDE loads NumPy, pandas, Matplotlib and Seaborn automatically when your code imports them, shows the charts you draw, and checks data-science answers too.

## [Math for Data Science & Machine Learning](math/) — 10 topics · 200 practice questions

The math that data science and ML are built on, taught from zero for someone who has never studied math (or forgot it all). Topics go in order, each using only what came before. Every idea is explained in plain words with a picture first, then the formula, then where it is used in ML. Each topic has a **Theory** tab, **Lessons** from basics to advanced with graphs, and **20 practice questions**. Each question is solved twice: **by hand** in plain Python, showing every step as you would on paper, and **with NumPy or a formula**. Both versions can be watched running line by line.

**Open it:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/ · [Full question list](math/README.md)

| # | Topic | Covers | Used in ML for |
|---|---|---|---|
| 1 | Numbers & Arithmetic | fractions, percentages, powers, roots, primes, rounding, Σ notation | reading every formula |
| 2 | Algebra & Equations | expressions, linear and quadratic equations, polynomials, systems, sequences | rearranging models and losses |
| 3 | Functions & Graphs | lines and slope, parabolas, exponentials, logarithms, sigmoid, ReLU | models as functions, activations |
| 4 | Vectors | length, distance, dot product, cosine similarity, projection | data points, embeddings, k-NN |
| 5 | Matrices | multiplication, determinant, inverse, solving systems, rank | datasets, neural-network layers, regression |
| 6 | Eigenvectors, PCA & SVD | eigenvalues, power iteration, PCA, SVD, Markov chains, PageRank | dimensionality reduction, recommenders |
| 7 | Calculus: Derivatives & Integrals | limits, derivative rules, chain rule, max/min, Newton's method, integrals | the slope that training follows |
| 8 | Gradients & Optimisation | partial derivatives, gradient, gradient descent, backpropagation, convexity | how every model is trained |
| 9 | Probability | counting, conditional probability, Bayes, independence, expected value | reasoning under uncertainty, Naive Bayes |
| 10 | Distributions & Information | binomial, Poisson, normal, CLT, entropy, cross-entropy, KL, softmax, log-loss, MLE | loss functions and probabilistic models |

## [Machine Learning from Scratch](ml/) — 10 topics · 200 practice questions

Learn how machine learning works by building every algorithm yourself, then using scikit-learn. Each topic has a **Theory** tab, **9–12 detailed lessons** that work real examples by hand, step by step, and **20 practice questions**. Each question is answered twice: **from scratch** in plain Python and NumPy, and **with scikit-learn** (or NumPy and SciPy where the library has no direct function). Both can be watched running line by line. Take the Math course first if vectors and derivatives are new.

**Open it:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/ · [Full question list](ml/README.md)

| # | Topic | Covers |
|---|---|---|
| 1 | ML Basics & Data Preparation | splits, baselines, scaling, encoding, imputation, feature selection |
| 2 | Linear Regression | least squares, gradient descent, metrics, polynomial features, Ridge, Lasso, Elastic Net |
| 3 | Logistic Regression & Classification | sigmoid, log-loss, Newton's method, boundaries, softmax, perceptron |
| 4 | Model Evaluation & Validation | confusion matrix, precision, recall, F1, ROC, PR, cross-validation |
| 5 | k-NN, Naive Bayes & SVM | neighbours, Laplace smoothing, margins, hinge loss, kernels |
| 6 | Decision Trees | Gini, entropy, best splits, growing and stopping, importances |
| 7 | Ensembles | voting, bagging, random forests, gradient boosting, AdaBoost, stacking |
| 8 | Clustering & Unsupervised Learning | k-means, silhouette, hierarchical, DBSCAN, PCA |
| 9 | Tuning, Pipelines & Regularisation | grid search, validation and learning curves, ColumnTransformer, leakage |
| 10 | Neural Networks | forward pass, backpropagation, SGD, momentum, Adam, dropout, MLPs |

## [DSA Interview Handbook](handbook/) — 14 topics · 280 questions

The 14 core DSA topics. Each topic has a **Theory** tab (definition, types, operations and their cost, pros and cons, applications, comparisons, and theory questions with model answers), a **Lessons** tab that teaches it from scratch to advanced in 5–8 short animated lessons, a one-card **Quick reference**, and the **top 20 most-asked interview questions**. Each question has a brute-force solution, the optimal solution, time and space complexity, and a step-by-step animation of the optimal code running. Search by title, LeetCode number or pattern.

**Open it:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/ · [Full question list](handbook/README.md)

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

The data-science, math and ML books need NumPy, pandas, Matplotlib, Seaborn and scikit-learn installed:

```bash
python3 handbook/build.py --book data-science
```

```bash
python3 handbook/build.py --book math
```

```bash
python3 handbook/build.py --book ml
```

To view it locally, serve the folder (the page loads its data files lazily):

```bash
python3 -m http.server 8000
```

## Practice problems

LeetCode 53, 78, 136, 191, 231, 238, 268, 303 and 724.
