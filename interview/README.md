# Interview Prep

5 topics · theory with 61 theory questions · 33 lessons from basics to advanced · 100 interview questions · SQL, advanced Python, classic algorithms, statistics and ML system design, with a step-by-step and an efficient answer for each.

**Live site:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/

Every solution is run against its test cases by `build.py` before the site is generated, and each animation is recorded from a real run of the code you see.

## Topics

- [SQL for Interviews](#sql-for-interviews) — The SQL that interviews ask: joins, GROUP BY and HAVING, subqueries, CTEs and window functions, including second-highest salary, top N per group, running totals and finding gaps.
- [Advanced Python](#advanced-python) — The Python that separates seniors: closures and late binding, decorators, generators and iterators, context managers, copying, the MRO, dataclasses, standard-library tools, and concurrency concepts.
- [Classic Algorithms](#classic-algorithms) — The algorithms interviewers ask you to write from memory: sorting, inversions, KMP, Rabin-Karp, union-find, Fenwick and segment trees, shortest paths, knapsack, topological order and designing data structures.
- [Statistics & A/B Testing](#statistics-a-b-testing) — What data-science interviews ask: confidence intervals, z and t tests, sample size, multiple testing, Bayes base rates, Simpson's paradox, and the pandas behind retention, funnels and top-N reports.
- [ML System Design](#ml-system-design) — How to answer 'design a recommender, fraud or RAG system': a repeatable framework, back-of-envelope sizing, data and label problems, online vs offline metrics, serving trade-offs and monitoring.

## SQL for Interviews

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Filter and Sort](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/sql/filter-and-sort) | Easy | WHERE, ORDER BY |
| 2 | [Count per Group](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/sql/count-per-group) | Easy | GROUP BY |
| 3 | [Groups Above a Limit](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/sql/groups-above-a-limit) | Easy | HAVING |
| 4 | [Inner Join](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/sql/inner-join) | Easy | JOIN |
| 5 | [Rows With No Match](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/sql/rows-with-no-match) | Easy | LEFT JOIN ... IS NULL |
| 6 | [Employee and Their Manager](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/sql/employee-and-their-manager) | Medium | Self join |
| 7 | [Second Highest Salary](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/sql/second-highest-salary) | Medium | The classic |
| 8 | [Find Duplicates](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/sql/find-duplicates) | Easy | GROUP BY + HAVING |
| 9 | [Keep the First of Each Duplicate](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/sql/keep-the-first-of-each-duplicate) | Medium | De-duplicating |
| 10 | [Above the Department Average](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/sql/above-the-department-average) | Medium | Correlated subquery vs window |
| 11 | [Rank Salaries](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/sql/rank-salaries) | Medium | ROW_NUMBER, RANK, DENSE_RANK |
| 12 | [Top Earner per Department](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/sql/top-earner-per-department) | Medium | Top N per group |
| 13 | [Top 2 Distinct Salaries per Department](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/sql/top-2-distinct-salaries-per-department) | Hard | DENSE_RANK |
| 14 | [Running Total](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/sql/running-total) | Medium | SUM OVER |
| 15 | [Month-Over-Month Change](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/sql/month-over-month-change) | Hard | LAG |
| 16 | [Share of Total](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/sql/share-of-total) | Medium | Percent of the whole |
| 17 | [Pivot With CASE](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/sql/pivot-with-case) | Medium | Rows to columns |
| 18 | [Consecutive Login Streaks](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/sql/consecutive-login-streaks) | Hard | Gaps and islands |
| 19 | [Walk the Org Chart](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/sql/walk-the-org-chart) | Hard | Recursive CTE |
| 20 | [COUNT and NULL](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/sql/count-and-null) | Easy | A favourite trick question |

## Advanced Python

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Mutable Default Argument](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/python-advanced/mutable-default-argument) | Easy | The classic trap |
| 2 | [Late-Binding Closures](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/python-advanced/late-binding-closures) | Medium | The loop variable trap |
| 3 | [A Closure With State](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/python-advanced/a-closure-with-state) | Easy | nonlocal |
| 4 | [Count-Calls Decorator](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/python-advanced/count-calls-decorator) | Easy | Your first decorator |
| 5 | [Why functools.wraps Matters](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/python-advanced/why-functools-wraps-matters) | Easy | Keeping the name |
| 6 | [Memoize Decorator](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/python-advanced/memoize-decorator) | Medium | Build lru_cache yourself |
| 7 | [Decorator With Arguments](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/python-advanced/decorator-with-arguments) | Medium | Three levels of functions |
| 8 | [Generator Pipeline](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/python-advanced/generator-pipeline) | Medium | Lazy steps |
| 9 | [Sliding Window Generator](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/python-advanced/sliding-window-generator) | Medium | Streams of any length |
| 10 | [Flatten With yield from](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/python-advanced/flatten-with-yield-from) | Medium | Recursive generators |
| 11 | [Build an Iterator](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/python-advanced/build-an-iterator) | Medium | __iter__ and __next__ |
| 12 | [A Context Manager](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/python-advanced/a-context-manager) | Medium | __enter__ and __exit__ |
| 13 | [Shallow vs Deep Copy](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/python-advanced/shallow-vs-deep-copy) | Easy | Aliasing bugs |
| 14 | [Method Resolution Order](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/python-advanced/method-resolution-order) | Medium | Diamond inheritance |
| 15 | [__eq__ and __hash__](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/python-advanced/eq-and-hash) | Medium | Objects in sets |
| 16 | [LRU Cache With OrderedDict](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/python-advanced/lru-cache-with-ordereddict) | Medium | Stdlib power |
| 17 | [Group Consecutive Runs](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/python-advanced/group-consecutive-runs) | Easy | itertools.groupby |
| 18 | [Top K With the Standard Library](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/python-advanced/top-k-with-the-standard-library) | Easy | Counter, heapq |
| 19 | [Coroutines by Hand](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/python-advanced/coroutines-by-hand) | Hard | What async does underneath |
| 20 | [Keep a List Sorted](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/python-advanced/keep-a-list-sorted) | Easy | bisect |

## Classic Algorithms

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Merge Sort](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/dsa-classics/merge-sort) | Medium | Divide and conquer |
| 2 | [Quick Sort](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/dsa-classics/quick-sort) | Medium | Partition |
| 3 | [Heap Sort](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/dsa-classics/heap-sort) | Medium | Sift down |
| 4 | [Counting Sort](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/dsa-classics/counting-sort) | Easy | Beat O(n log n) |
| 5 | [Count Inversions](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/dsa-classics/count-inversions) | Hard | Merge sort's bonus |
| 6 | [Substring Search With KMP](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/dsa-classics/substring-search-with-kmp) | Hard | Never look back |
| 7 | [All Matches With a Rolling Hash](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/dsa-classics/all-matches-with-a-rolling-hash) | Hard | Rabin-Karp |
| 8 | [Union-Find](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/dsa-classics/union-find) | Medium | Who's connected? |
| 9 | [Fenwick Tree](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/dsa-classics/fenwick-tree) | Hard | Prefix sums with updates |
| 10 | [Segment Tree: Range Minimum](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/dsa-classics/segment-tree-range-minimum) | Hard | Any range, with updates |
| 11 | [LFU Cache](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/dsa-classics/lfu-cache) | Hard | A harder LRU |
| 12 | [Time-Based Key-Value Store](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/dsa-classics/time-based-key-value-store) | Medium | Binary search on history |
| 13 | [Design a Hash Map](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/dsa-classics/design-a-hash-map) | Medium | How dict works |
| 14 | [Insert, Delete, Random in O(1)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/dsa-classics/insert-delete-random-in-o-1) | Medium | List plus dictionary |
| 15 | [Bellman-Ford](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/dsa-classics/bellman-ford) | Medium | Negative edges |
| 16 | [Floyd-Warshall](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/dsa-classics/floyd-warshall) | Medium | All pairs |
| 17 | [0/1 Knapsack](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/dsa-classics/0-1-knapsack) | Medium | The DP you must know |
| 18 | [Longest Common Substring](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/dsa-classics/longest-common-substring) | Medium | Contiguous, unlike subsequence |
| 19 | [Alien Dictionary](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/dsa-classics/alien-dictionary) | Hard | Topological sort |
| 20 | [Weighted Random Pick](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/dsa-classics/weighted-random-pick) | Medium | Prefix sums + binary search |

## Statistics & A/B Testing

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Standard Error of a Proportion](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/stats-ab/standard-error-of-a-proportion) | Easy | How noisy is a rate? |
| 2 | [95% Confidence Interval](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/stats-ab/95-confidence-interval) | Easy | A range, not a point |
| 3 | [CI of a Mean](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/stats-ab/ci-of-a-mean) | Easy | Using the sample |
| 4 | [Two-Proportion z-Test](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/stats-ab/two-proportion-z-test) | Medium | The A/B test |
| 5 | [Sample Size for an A/B Test](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/stats-ab/sample-size-for-an-a-b-test) | Medium | Before you run it |
| 6 | [Welch's t Statistic](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/stats-ab/welchs-t-statistic) | Medium | Comparing two means |
| 7 | [Chi-Square for a 2×2 Table](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/stats-ab/chi-square-for-a-2-2-table) | Medium | Independent? |
| 8 | [Bonferroni and False Positives](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/stats-ab/bonferroni-and-false-positives) | Easy | Testing many things |
| 9 | [Bayes: The Rare-Disease Test](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/stats-ab/bayes-the-rare-disease-test) | Easy | Base rates |
| 10 | [Simpson's Paradox](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/stats-ab/simpsons-paradox) | Medium | Aggregates can flip |
| 11 | [Bootstrap a Median](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/stats-ab/bootstrap-a-median) | Medium | When there's no neat formula |
| 12 | [Expected Value of a Bet](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/stats-ab/expected-value-of-a-bet) | Easy | Should you play? |
| 13 | [Correlation by Hand](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/stats-ab/correlation-by-hand) | Easy | Pearson's r |
| 14 | [Sample Ratio Mismatch](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/stats-ab/sample-ratio-mismatch) | Medium | Is the split broken? |
| 15 | [Funnel Conversion](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/stats-ab/funnel-conversion) | Medium | pandas |
| 16 | [Cohort Retention](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/stats-ab/cohort-retention) | Hard | A real analytics task |
| 17 | [Top N per Group in pandas](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/stats-ab/top-n-per-group-in-pandas) | Medium | SQL's RANK, in pandas |
| 18 | [Percent of Group Total](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/stats-ab/percent-of-group-total) | Medium | transform |
| 19 | [Rolling Average](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/stats-ab/rolling-average) | Easy | Smoothing a metric |
| 20 | [Margin of Error vs Sample Size](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/stats-ab/margin-of-error-vs-sample-size) | Easy | Quadruple the data, halve the error |

## ML System Design

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Requests per Second](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/ml-system-design/requests-per-second) | Easy | Back of the envelope |
| 2 | [Embedding Storage](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/ml-system-design/embedding-storage) | Easy | Will it fit in memory? |
| 3 | [Latency Budget](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/ml-system-design/latency-budget) | Easy | Where the time goes |
| 4 | [How Many Servers?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/ml-system-design/how-many-servers) | Easy | Capacity |
| 5 | [Cache Effect on Traffic](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/ml-system-design/cache-effect-on-traffic) | Easy | Reducing load |
| 6 | [Split by Time](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/ml-system-design/split-by-time) | Easy | Prevent leakage |
| 7 | [Spot Feature Leakage](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/ml-system-design/spot-feature-leakage) | Medium | Too good to be true |
| 8 | [Target Encoding Without Leakage](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/ml-system-design/target-encoding-without-leakage) | Hard | Only use the past |
| 9 | [Feature Hashing](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/ml-system-design/feature-hashing) | Easy | Huge vocabularies in fixed space |
| 10 | [Correct for Negative Downsampling](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/ml-system-design/correct-for-negative-downsampling) | Medium | Calibrated probabilities |
| 11 | [Expected Calibration Error](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/ml-system-design/expected-calibration-error) | Medium | Do probabilities mean what they say? |
| 12 | [Pick a Threshold by Cost](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/ml-system-design/pick-a-threshold-by-cost) | Medium | Connect ML to money |
| 13 | [Lift at the Top](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/ml-system-design/lift-at-the-top) | Easy | When you can only review some |
| 14 | [Training vs Serving Skew](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/ml-system-design/training-vs-serving-skew) | Medium | The silent bug |
| 15 | [Canary Decision](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/ml-system-design/canary-decision) | Medium | Roll out safely |
| 16 | [When to Retrain](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/ml-system-design/when-to-retrain) | Easy | Triggers, not a habit |
| 17 | [Recommendation: Two-Stage Funnel](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/ml-system-design/recommendation-two-stage-funnel) | Medium | Retrieve, then rank |
| 18 | [Batch or Real Time?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/ml-system-design/batch-or-real-time) | Medium | A cost and freshness call |
| 19 | [RAG Assistant Budget](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/ml-system-design/rag-assistant-budget) | Easy | An LLM system design staple |
| 20 | [Position Bias Correction](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/#/q/ml-system-design/position-bias-correction) | Medium | Clicks depend on where it was shown |

## Build

```bash
python3 handbook/build.py --book interview
```

Sources live in `interview/src/`: `topics/` (questions and solutions), `lessons/` and `theory/`.
