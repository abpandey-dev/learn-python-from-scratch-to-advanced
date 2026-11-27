# Learn Python: From Scratch to Advanced

A complete, interactive path for learning Python: a beginner course from the first line of code, Python for data science (NumPy, pandas, Matplotlib, Seaborn, statistics, SQL, hypothesis testing, business KPIs, time series, Polars and DuckDB), the math behind data science and machine learning, machine learning from scratch, deep learning and LLMs, AI engineering (MCP, agents, context engineering, evals, fine-tuning, serving, vector databases, LangChain and LlamaIndex), system design (caching, sharding, queues, rate limiting, chat, feeds), an engineering toolbox (Git, pytest, linting and type hints, packaging, Linux, logging, Docker, CI/CD), interview prep, behavioural interview prep, a DSA interview handbook, teacher-style Jupyter notebooks, and an in-browser IDE. Every lesson and answer can be watched running line by line, with the data drawn as pictures and a plain-English explanation of each step.

**Live site:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/

**Companion course:** [Data Engineering from Scratch to Advanced](https://github.com/abpandey-dev/data-engineering-from-scratch-to-advanced) covers big data (Spark, Airflow, Kafka, lakehouses, dbt, cloud) and has a [SQL IDE](https://abpandey-dev.github.io/data-engineering-from-scratch-to-advanced/ide/sql.html) with automatically checked questions.

## [Teacher's Notebooks](notebooks/) — 106 notebooks · 736 lessons · 2,120 questions

Every course below as Jupyter notebooks, explained the way a teacher would. Open any of them in Google Colab with nothing to install. Each has lessons with worked numbers, practice cells that check your answer, hints and two answers hidden until you want them, advice on explaining each answer aloud, and interview questions to practise. **[Start here](notebooks/00_START_HERE.ipynb)**, or see the [full list](notebooks/README.md).

## [Industry Projects](projects/) — 10 end-to-end portfolio projects

Turn the courses into portfolio work. Each project is a notebook (open it in Colab, nothing to install) with a business brief, realistic data, 6–8 milestones whose answers are **checked automatically**, hints, a hidden reference solution, a report template, resume bullets and the interview questions you'll be asked about it.

**Open it:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/projects/

| # | Project | Role | Skills |
|---|---|---|---|
| 1 | Retail Sales Analysis & Forecast | Data Analyst | cleaning, KPIs, SQL, Pareto, cohort retention, forecast backtesting |
| 2 | Checkout Redesign: A/B Test Readout | Product Analyst | sample ratio mismatch, funnel, z-test, CI, segments, guardrails, power |
| 3 | Predict Churn for a Subscription App | Data Scientist | pipelines, logistic regression vs boosting, cost-based threshold, drivers |
| 4 | Predictive Maintenance from Sensor Data | ML Engineer | label engineering, rolling features, time split, alert policy, business case |
| 5 | "You Might Also Like": A Store Recommender | ML Engineer | item-based CF, TF-IDF for new items, hybrid, hit rate, coverage |
| 6 | Fair Credit-Risk Scoring | Data Scientist | calibration, approval policy, fairness audit, reason codes, counterfactuals |
| 7 | Ship It: Serve and Monitor the Churn Model | MLOps | joblib pipeline, request validation, FastAPI, Docker, batch scoring, PSI drift |
| 8 | Customer-Support Assistant with RAG | AI Engineer | chunking, BM25 from scratch, retrieval evaluation, grounded prompts, Claude API |
| 9 | Multi-Agent Support Analyst over an MCP Server | AI Engineer | your own MCP server (JSON-RPC, tools/list, tools/call), orchestrator, research, writer and reviewer agents, citations, tracing, Claude tool use |
| 10 | Fine-Tune With LoRA: Adapt a Model to a New Domain | AI / ML Engineer | data cleaning and leakage, LoRA from scratch, full fine-tuning comparison, forgetting, adapter merging, rank sweep, QLoRA with PEFT/TRL |

## [Python IDE](ide/) — write and run Python in the browser

**Open it:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ide/

- Real Python 3.12 running in the browser (Pyodide) — nothing to install. NumPy, pandas, Matplotlib, Seaborn and scikit-learn load on first import, and charts appear under the output.
- Editor with syntax highlighting, auto-indent, bracket matching and Ctrl/⌘ + Enter to run.
- An **Input** box feeds `input()`, errors point to the line with a beginner-friendly hint, and **Stop** ends infinite loops.
- **Visualize** runs your own code step by step: every variable, list, dict, object, the call stack and the printed output.
- Every practice question has **Solve it yourself**: it opens a starter function and a **Check** button that runs the question's tests. Every answer and lesson example has **Open in editor**.
- **Share** copies a link that contains your code.

## [Python from Scratch](python-course/) — 13 topics · 260 practice questions

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
| 13 | Modules, Packages, APIs & JSON | imports, packages, pip and virtual environments, JSON, URLs, status codes, pagination, retries, rate limits, caching |

## [Python for Data Science](data-science/) — 13 topics · 260 practice questions

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
| 9 | SQL from Python | sqlite3, safe parameters, joins, GROUP BY / HAVING, subqueries, window functions, dates, upserts, transactions, indexes, read_sql / to_sql |
| 10 | Hypothesis Testing & Inference | p-values, z and t tests, paired and Welch tests, chi-square, ANOVA, Mann–Whitney, permutation tests, bootstrap, power, sample size, multiple testing |
| 11 | EDA, Business KPIs & Storytelling | profiling, skew, Excel → pandas (VLOOKUP, pivot tables, SUMIFS, IF), funnels, cohorts, churn, ARPU, LTV, DAU/MAU, explaining a change, charts that tell a story |
| 12 | Time Series & Forecasting | resampling, lags, rolling and exponential averages, seasonality, autocorrelation, baselines, smoothing, AR models, walk-forward validation, anomalies |
| 13 | Polars & DuckDB | Polars expressions, lazy queries, window functions with `over`, joins and anti joins, pivot, rolling, strings, explode; DuckDB SQL on DataFrames, HAVING, running totals and LAG, QUALIFY, FILTER, ASOF joins, gap-filled dates |

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

## [Machine Learning from Scratch](ml/) — 13 topics · 260 practice questions

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
| 11 | Recommender Systems | popularity, cosine and Pearson similarity, user- and item-based CF, TF-IDF content, matrix factorisation, basket rules, cold start, NDCG |
| 12 | Explainability, Fairness & Imbalanced Data | linear contributions, Shapley values, permutation importance, partial dependence, counterfactuals, fairness metrics, calibration, class weights, thresholds, privacy |
| 13 | MLOps: Deploying & Monitoring Models | experiment tracking, model registry, data gates, serialisation, request validation, canary and shadow releases, latency, point-in-time joins, PSI and KS drift, retraining |

## [Deep Learning & LLMs](deep-learning/) — 10 topics · 200 practice questions

See inside modern AI by building it, then learn to build real products with it. Each topic has a **Theory** tab, **detailed lessons** that work real numbers by hand and explain why, and **20 practice questions**, each answered **step by step** in plain Python and again **the efficient way**, both of which you can watch run line by line. Everything you can run works in the browser with NumPy. PyTorch and Claude API code appears in the lessons as text, because neither can run in the browser IDE.

**Open it:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/ · [Full question list](deep-learning/README.md)

| # | Topic | Covers |
|---|---|---|
| 1 | Tensors & Layers | shapes, broadcasting, dense layers, activations, parameter counts, initialisation |
| 2 | Training Deep Networks | losses, backpropagation, optimisers, schedules, normalisation, dropout, clipping |
| 3 | Convolutional Networks | convolution by hand, stride, padding, pooling, receptive fields, residual blocks |
| 4 | RNNs & Sequences | RNN, LSTM and GRU cells, vanishing gradients, masks, teacher forcing |
| 5 | Tokens & Embeddings | tokenising, BPE, TF-IDF, embedding tables, skip-gram, positional encoding |
| 6 | Attention & Transformers | scaled dot-product attention, masks, multi-head attention, the transformer block |
| 7 | Language Models | bigrams, perplexity, next-token loss, temperature, top-k, top-p, beam search, KV cache |
| 8 | Building With LLMs | prompts, costs, context limits, structured output, retries, streaming, tool calling, caching, the Claude API |
| 9 | RAG & Retrieval | chunking, BM25, vector search, approximate indexes, fusion, MMR, re-ranking, recall, MRR, nDCG |
| 10 | Agents, Evals & Production | agent loops, guard rails, evaluation, fair comparison, latency, cost, safety, quantisation, LoRA, drift |

## [AI Engineering](ai-engineering/) — 10 topics · 200 practice questions

The skills current AI Engineer roles ask for, built from scratch so nothing is a black box, with the matching real SDK and library code in every lesson. Each topic has a **Theory** tab, **lessons** and **20 practice questions**, answered step by step and again the efficient way. Model calls are simulated with small deterministic stand-ins, so everything runs in the browser with no API key.

**Open it:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/ · [Full question list](ai-engineering/README.md)

| # | Topic | Covers |
|---|---|---|
| 1 | MCP: Connecting AI to Tools and Data | JSON-RPC, stdio, initialize, tools/resources/prompts, input schemas, isError, pagination, permissions, MCP → Claude tools |
| 2 | Agents & Multi-Agent Orchestration | the agent loop, routers, planning and fan-out, orchestrator–workers, handoffs, shared state, evaluator loops, budgets, graph workflows |
| 3 | Context Engineering & Agent Memory | token budgets, trimming and compaction, prompt-cache ordering, lost in the middle, tool-result clearing, long-term memory and recall |
| 4 | Reasoning Models & Test-Time Compute | thinking cost and latency, effort levels, self-consistency, best-of-N, pass@k, process vs outcome checks, routing |
| 5 | Serving LLMs: Inference Optimisation | weight and KV-cache memory, continuous batching, prefill/decode, speculative decoding, quantisation, paged KV, self-host vs API |
| 6 | Observability, Tracing & Evals in Production | spans and self time, cost per feature, redaction, LLM-as-judge, kappa, pairwise bias, faithfulness, release gates |
| 7 | Fine-Tuning in Practice: LoRA, QLoRA & DPO | LoRA maths and merging, training memory, chat templates and loss masking, packing, data cleaning, DPO, forgetting |
| 8 | Multimodal AI: Images, Documents & Speech | image tokens and patches, image blocks, OCR reading order, invoice validation, WER, subtitles, CLIP-style labels, voice latency |
| 9 | Shipping AI Products | streaming (SSE), structured output, retries and fallbacks, coding-agent edits and sandboxing, guardrails, budgets, launch checklist |
| 10 | Vector Databases & AI Frameworks | metrics and normalisation, IVF, product and int8 quantization, HNSW search, post-filtering, segments, memory sizing, sharded and hybrid search, metadata filters, SQL vector search, embedding and semantic caches, model migration, LangChain-style chains, recursive splitting, prompt templates, retrievers |

## [System Design](system-design/) — 10 topics · 200 practice questions

What backend and senior interviews test, with every building block simulated in plain Python so you can watch it behave: an LRU cache evicting, a consistent-hash ring moving keys, a token bucket refilling, a Raft vote, a Kafka consumer crashing and redelivering. Each topic has a **Theory** tab, **lessons** that walk through full designs, and **20 practice questions**, answered step by step and again the efficient way.

**Open it:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/system-design/ · [Full question list](system-design/README.md)

| # | Topic | Covers |
|---|---|---|
| 1 | Requirements & Back-of-the-Envelope Estimation | the interview framework, QPS and peaks, storage, bandwidth, latency numbers, availability, servers, cache and shard counts |
| 2 | Load Balancing, Routing & CDNs | round robin, weighted, least connections, power of two choices, consistent hashing, health checks, DNS, CDNs, regions, autoscaling, deploys |
| 3 | Caching | LRU, LFU, TTL, cache-aside, write-through/back, stampedes, jitter, cache keys, invalidation, hot keys, sizing, HTTP caching |
| 4 | Databases, Replication & Sharding | choosing a database, indexes, LSM trees, replication lag, quorums, read repair, hash vs range sharding, shard keys, locking |
| 5 | Consistency & Distributed Systems | CAP/PACELC, Lamport and vector clocks, CRDTs, idempotency, 2PC vs sagas, majorities, Raft voting, leases, fencing, gossip, Merkle trees |
| 6 | Queues & Streams | backlogs, Kafka partitions and consumer groups, lag, at-least-once, backoff and jitter, DLQs, backpressure, outbox, windows, watermarks |
| 7 | APIs & Rate Limiting | fixed/sliding window, token and leaky bucket, pagination, idempotency keys, status codes, ETags, circuit breakers, gateways, webhooks |
| 8 | URL Shortener & ID Generation | base62, hashing and collisions, ticket ranges, key-generation service, Snowflake IDs, ULIDs, birthday paradox, Bloom filters |
| 9 | News Feed, Chat & Notifications | fan-out on write vs read, celebrities, ranking, chat sequencing, unread counts, presence, routing, digests, quiet hours |
| 10 | Search, Storage, Reliability & the Interview | inverted index, TF-IDF, autocomplete, geohash, chunked uploads, erasure coding, SLOs, burn rates, retry storms, DR, the 45-minute plan |

## [Engineering Toolbox](engineering-toolbox/) — 8 topics · 160 practice questions

The tools every engineering job assumes on day one, and that take-home assignments quietly check. Each question rebuilds one idea a tool relies on — a Git blob hash, a merge base, a pytest fixture order, an unused-import check with `ast`, a dependency resolver, a cron schedule, a Prometheus histogram, a Docker layer cache, a GitHub Actions matrix — and every lesson shows the real commands. Each topic has a **Theory** tab, **lessons** and **20 practice questions**, answered step by step and again the efficient way.

**Open it:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/engineering-toolbox/ · [Full question list](engineering-toolbox/README.md)

| # | Topic | Covers |
|---|---|---|
| 1 | Git: From Commits to Pull Requests | blob hashes, history, merge base, fast-forward, diffs, three-way merge, .gitignore, conventional commits, bisect, rebase, cherry-pick, blame, branch protection, secret scanning |
| 2 | Testing With pytest | approx, parametrize, fixtures and scopes, mocks, line and branch coverage, mutation testing, flaky tests, property-based shrinking, affected tests, snapshots, test smells |
| 3 | Code Quality, Linting & Type Hints | linters built with `ast`: unused imports, complexity, naming, mutable defaults, swallowed errors, docstring and type-hint coverage, import sorting, duplicates, layer rules |
| 4 | Packages, Versions & Environments | version ordering, specifiers, dependency resolution, pyproject.toml, markers, wheel tags, lockfile diffs, vulnerabilities, config precedence, .env files, PATH |
| 5 | The Command Line & Linux | permissions and chmod, globs, paths, argparse, exit codes, grep/cut/sort/uniq, cron, du, find, log parsing, variable expansion, processes and signals, quoting |
| 6 | Logging, Metrics & Errors in Production | levels and formats, JSON logs, rotation, request tracing, redaction, retries, exception chaining, Prometheus histograms and rates, health checks, feature flags, alerts |
| 7 | Docker & Containers | image references, layer caching, multi-stage builds, .dockerignore, Dockerfile linting, compose order and variables, restart policies, volumes, Kubernetes QoS and probes |
| 8 | CI/CD With GitHub Actions | matrices, job graphs, path filters, caching, concurrency, step conditions, check status, workflow validation, sharding, changelogs, environments, DORA, least privilege |

## [Interview Prep](interview/) — 5 topics · 100 practice questions

The interview topics the other courses leave out. Each topic has a **Theory** tab, detailed **lessons** with worked examples, and **20 practice questions**, each answered step by step and again the efficient way.

**Open it:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/interview/ · [Full question list](interview/README.md)

| # | Topic | Covers |
|---|---|---|
| 1 | SQL for Interviews | joins, GROUP BY, second-highest salary, window functions, gaps and islands, recursive CTEs, indexes |
| 2 | Advanced Python | closures, decorators, generators, context managers, the MRO, the standard library, the GIL and asyncio |
| 3 | Classic Algorithms | sorting, inversions, KMP, union-find, Fenwick and segment trees, LFU cache, shortest paths, knapsack |
| 4 | Statistics & A/B Testing | confidence intervals, z and t tests, sample size, peeking, Bayes, Simpson's paradox, funnels and retention |
| 5 | ML System Design | a design framework, sizing, leakage, calibration, recommender, fraud and LLM assistant walkthroughs, rollout |

## [Behavioural Interviews](behavioural/) — a guide, 66 questions and a practice drill

The rounds that often decide the offer and the level. What interviewers score, the STAR method with a weak and a strong answer side by side, "tell me about yourself" for freshers, career switchers and experienced engineers, how to build a story bank, the project deep dive, tricky questions (weakness, failure, gaps, why leaving), questions to ask, salary and offers, role-specific questions for software, data and ML/AI engineers, and a two-week plan. The web page has a **timed practice drill** with a self-scoring checklist.

**Open it:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/behavioural/ · [Read on GitHub](behavioural/README.md)

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
