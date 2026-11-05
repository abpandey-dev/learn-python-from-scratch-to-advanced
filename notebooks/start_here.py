"""The contents of notebooks/00_START_HERE.ipynb."""
CELLS = [
("md", """# Start here

Hello, and welcome. I'll be your teacher for this course.

This set of notebooks takes you from your first line of Python to machine learning, LLMs and interview practice. Nothing assumes you already know it, and you don't need to install anything: open a notebook in Google Colab, and run the first cell.

**In this notebook:** how to study so that it sticks, which path to follow for your goal, how to solve a problem you've never seen, and how to tell which technique a question is asking for.

### A straight answer about "cracking any interview"

**No course can honestly promise that**, and you should be wary of any that does. Here's what's true:

| This course covers well | You still need to do this yourself |
|---|---|
| Python, DSA patterns, SQL, statistics, ML, deep learning and LLMs | **Practise until you're quick.** Reading an answer isn't the same as producing one under pressure |
| Over 1,300 questions with hints, tested answers and explanations | **Mock interviews with a real person,** because explaining while being watched is its own skill |
| ML and LLM system design | **General backend system design** (scaling a chat app, say), covered here only for ML systems |
| A method for unseen problems | **Behavioural preparation** using your own stories, and **company-specific research** |

Do the work below and you'll be well prepared for most Python, data and ML interviews. You also won't need another site for practice questions until you've finished these, and that's a lot of practice.
"""),
("md", """## How to study, so it actually sticks

Reading feels productive, but most of it fades within days. These habits are what work:

1. **Try before you look.** Struggling for 15 to 25 minutes, even if you fail, makes the answer stick far better than reading it straight away.
2. **Open one hint at a time.** Each hint you don't open is practice you got.
3. **Type the code, never paste it.** Then change something and predict the result.
4. **Come back later.** Redo a question 3 days later, and again after 2 weeks, from a blank cell. This is the most effective habit on this list.
5. **Explain it aloud.** If you can't explain it simply to an imaginary friend, you've found exactly what to review.
6. **Keep a mistakes list.** Write one line for each question you missed, saying *why*. Review that list, rather than the questions you got right.

**A good daily session (about 90 minutes):** 15 minutes redoing old questions, 30 on a lesson, 45 on new questions."""),
("md", """## Choose your path

| Your goal | Follow these, in order | Rough time at 1 to 2 hours a day |
|---|---|---|
| **Complete beginner** | Python → DSA basics | 8 to 12 weeks |
| **Software engineer interviews** | Python → DSA → Classic Algorithms → Advanced Python → SQL | 10 to 14 weeks |
| **Data analyst or data scientist** | Python → Data Science → SQL → Statistics & A/B Testing → Math → ML | 12 to 16 weeks |
| **ML engineer** | Python → Math → Data Science → ML → Deep Learning → DSA → ML System Design | 16 to 24 weeks |
| **AI / LLM engineer** | Python → ML basics → Deep Learning & LLMs → Advanced Python → ML System Design → DSA | 14 to 20 weeks |

These times are rough guides, so go at your own pace. Moving on when you can tick a notebook's checklist **without looking** matters more than sticking to the calendar.

Find every notebook in the [full list](README.md)."""),
("md", """## How to solve a problem you've never seen

Use these six steps every time, until they're automatic. Interviewers are judging this process as much as the final answer.

| Step | What to do | Why |
|---|---|---|
| **1. Clarify** | Restate it. Ask about size, empty input, duplicates, negatives | Solves the right problem, and shows maturity |
| **2. Example** | Work a small case by hand | Often reveals the method |
| **3. Simple solution** | Say the obvious approach and its cost | You always have something; it's a baseline to beat |
| **4. Improve** | Where's the repeated work? What structure removes it? | This is the actual test |
| **5. Code** | Write it, talking as you go. Use clear names | Shows how you'd work on a team |
| **6. Test** | Trace your example, then try edge cases | Find your own bug before they do |

### Worked example: Two Sum

*Given a list and a target, return the positions of two numbers adding up to the target.*

1. **Clarify:** "Exactly one answer? Can I use the same element twice? Could the input be empty?"
2. **Example:** `[2, 7, 11, 15]`, target 9: 2 + 7 works, so positions 0 and 1.
3. **Simple:** "Check every pair. That's O(n²) time, and O(1) space."
4. **Improve:** "For each number, I'm searching for its partner. Searching is the repeated work. A dictionary finds things in O(1), so I'll remember what I've seen."
5. **Code:** below.
6. **Test:** "On 2: partner 7 isn't seen yet, so store it. On 7: partner 2 is at position 0. Done. It's O(n) time and O(n) space, and I've traded memory for speed."

Run the cell, then try your own inputs."""),
("code", """def two_sum(nums, target):
    seen = {}                         # value -> position
    for i, x in enumerate(nums):
        partner = target - x
        if partner in seen:
            return [seen[partner], i]
        seen[x] = i
    return []                         # say what happens when there's no answer


print(two_sum([2, 7, 11, 15], 9))
print(two_sum([3, 3], 6))
print(two_sum([1, 2], 10))"""),
("md", """**What if you get stuck?** It happens to everyone, and it's fine to say so. Say what you've tried, and why it doesn't work. Try a smaller input, try sorting, or ask yourself which data structure would make the slow part fast. A good hint, taken well, is often a good interview."""),
("md", """## Which technique is this question asking for?

Questions don't name their technique, but they leave clues. This table is worth learning by heart.

| If you see… | Think of… | Notebook |
|---|---|---|
| "Find a pair", "seen before", counting | Hash map | [Arrays](06-dsa-interview/01_arrays.ipynb) |
| Sorted array, pairs, in-place | Two pointers | [Two Pointers](06-dsa-interview/02_two-pointers.ipynb) |
| "Longest or shortest substring or subarray" | Sliding window | [Sliding Window](06-dsa-interview/03_sliding-window.ipynb) |
| Matching brackets, "next greater" | Stack | [Stack & Queue](06-dsa-interview/04_stack-queue.ipynb) |
| Sorted input, "minimum that works" | Binary search | [Binary Search](06-dsa-interview/05_binary-search.ipynb) |
| Linked list, cycle, middle | Fast and slow pointers | [Linked List](06-dsa-interview/06_linked-list.ipynb) |
| Tree, hierarchy | DFS, or BFS by level | [Trees](06-dsa-interview/07_trees.ipynb) |
| "Top k", "kth", stream of numbers | Heap | [Heap](06-dsa-interview/08_heap.ipynb) |
| "All combinations or permutations" | Backtracking | [Backtracking](06-dsa-interview/09_backtracking.ipynb) |
| Grid, connections, dependencies | BFS, DFS, topological sort | [Graphs](06-dsa-interview/10_graphs.ipynb) |
| "How many ways", "minimum cost", choices | Dynamic programming | [DP](06-dsa-interview/11_dp.ipynb) |
| Intervals, scheduling | Sort, then greedy | [Greedy](06-dsa-interview/12_greedy.ipynb) |
| Prefix search, autocomplete | Trie | [Tries](06-dsa-interview/13_tries.ipynb) |
| "Appears once", no extra space | XOR, bits | [Bits](06-dsa-interview/14_bits.ipynb) |

**The size of the input is a clue too.** Up to about 20 suggests exponential is fine. Up to about 5,000, O(n²). Up to about a million, O(n log n) or O(n)."""),
("md", """### Test yourself

Name the technique before you open each answer.

<details><summary><b>1. Find the longest stretch of a string with no repeated letter.</b></summary>

Sliding window, with a set or dictionary of what's in the window.
</details>

<details><summary><b>2. Given daily temperatures, how many days until a warmer one?</b></summary>

A monotonic stack ("next greater").
</details>

<details><summary><b>3. Can these courses be finished, given their prerequisites?</b></summary>

A graph: topological sort, or cycle detection.
</details>

<details><summary><b>4. What's the smallest eating speed that finishes all the bananas in h hours?</b></summary>

Binary search on the answer: "minimum that works".
</details>

<details><summary><b>5. How many ways can you make change for an amount?</b></summary>

Dynamic programming.
</details>

<details><summary><b>6. Keep the running median of a stream of numbers.</b></summary>

Two heaps.
</details>

<details><summary><b>7. SQL: the top 3 earners in each department.</b></summary>

A window function: DENSE_RANK or ROW_NUMBER with PARTITION BY, inside a CTE.
</details>

<details><summary><b>8. Your model is 99.9% accurate at finding fraud. Is it good?</b></summary>

Probably not. Fraud may be under 0.1%, so a model that always says "no" scores that too. Look at precision and recall, or PR-AUC.
</details>
"""),
("md", """## Behavioural questions: don't skip these

Many strong candidates fail here, and no code cell can practise it for you. Prepare **5 or 6 true stories** from your own experience: a hard technical problem, a conflict, a failure, a time you led something, and a time you changed your mind.

Tell each one with **STAR**:

| Letter | Meaning | Share of the story |
|---|---|---|
| **S**ituation | The context, in a sentence or two | small |
| **T**ask | What you had to do | small |
| **A**ction | What *you* did and why. Say "I", not "we" | **most of it** |
| **R**esult | What changed, with numbers if you can, and what you learned | small |

## In the last week

- [ ] Redo your mistakes list, from blank cells.
- [ ] Do at least 2 mock interviews with a real person, out loud.
- [ ] Prepare your "tell me about yourself", in under 2 minutes.
- [ ] Be ready to discuss every line of your resume and your projects.
- [ ] Prepare 3 real questions to ask them.
- [ ] Test your audio, video and editor, and sleep well the night before.

**Now open your first notebook from the [full list](README.md).** Good luck. You've got this, one question at a time."""),
]
