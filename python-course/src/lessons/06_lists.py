from lib import *

LESSON("Basics", "Creating a list and reading items", """
<p>A <b>list</b> stores many values in one variable, in order:</p>
<pre><code class="py">marks = [72, 85, 90]
mixed = ["Ana", 21, True, 3.5]    # items can be any type
empty = []</code></pre>
<p>Items are numbered from 0, just like string characters: <code>marks[0]</code> is 72, <code>marks[-1]</code> is the last item. <code>len(marks)</code> is the number of items and <code>85 in marks</code> checks membership.</p>
<p>Slicing works too: <code>marks[0:2]</code> → <code>[72, 85]</code>. A slice is a <b>new</b> list.</p>
""", practice=["Sum of a List", "Average of a List"])


@LD
def list_basics_demo():
    marks = [72, 85, 90]
    first = marks[0]
    last = marks[-1]
    size = len(marks)
    top_two = marks[1:]
    has_85 = 85 in marks
    print(first, last, size, top_two, has_85)


LESSON("Basics", "Changing a list", """
<p>Unlike strings, lists are <b>mutable</b> — you can change them in place:</p>
<table>
<tr><th>Code</th><th>Effect</th></tr>
<tr><td><code>a[1] = 50</code></td><td>replace item 1</td></tr>
<tr><td><code>a.append(x)</code></td><td>add x at the end</td></tr>
<tr><td><code>a.insert(i, x)</code></td><td>insert x before position i</td></tr>
<tr><td><code>a.extend([x, y])</code></td><td>add several items</td></tr>
<tr><td><code>a.remove(x)</code></td><td>delete the first x (ValueError if missing)</td></tr>
<tr><td><code>a.pop()</code> / <code>a.pop(i)</code></td><td>delete and <b>return</b> the last / i-th item</td></tr>
<tr><td><code>del a[i]</code></td><td>delete item i</td></tr>
<tr><td><code>a.clear()</code></td><td>remove everything</td></tr>
</table>
""", practice=["Remove Every Copy of a Value", "Move Zeros to the End"])


@LD
def modify_demo():
    cart = ["milk", "eggs"]
    cart.append("bread")
    cart.insert(0, "tea")
    cart[2] = "butter"
    removed = cart.pop()
    cart.remove("tea")
    cart.extend(["rice", "salt"])
    print(cart, "removed:", removed)


LESSON("Core", "Two names, one list (aliasing)", """
<p>This surprises every beginner. Assignment does <b>not</b> copy a list — it adds another name for the same list:</p>
<pre><code class="py">a = [1, 2, 3]
b = a          # b and a are the SAME list
b.append(4)
print(a)       # [1, 2, 3, 4]  ← a changed too!</code></pre>
<p>To get an independent copy use <code>a[:]</code>, <code>a.copy()</code> or <code>list(a)</code>. For lists that contain other lists, those make a <b>shallow</b> copy (the inner lists are still shared) — use <code>copy.deepcopy(a)</code> for a full copy.</p>
<p>The same thing happens when you pass a list to a function: the function can change the caller's list.</p>
""", practice=["Reverse a List in Place"])


@LD
def aliasing_demo():
    a = [1, 2, 3]
    b = a
    b.append(4)
    c = a[:]
    c.append(99)
    print("a =", a, "| b =", b, "| c =", c)
    print("a is b:", a is b, "| a is c:", a is c)


LESSON("Core", "Looping over lists and building new ones", """
<p>Loop directly over the items, or use <code>enumerate</code> when you also need the position:</p>
<pre><code class="py">for price in prices:
    ...
for i, price in enumerate(prices):
    ...</code></pre>
<p>A very common task is building a new list from an old one. The long way uses a loop and <code>append</code>; the short way is a <b>list comprehension</b>:</p>
<pre><code class="py">doubled = []
for x in nums:
    doubled.append(x * 2)

doubled = [x * 2 for x in nums]              # same result
evens = [x for x in nums if x % 2 == 0]     # with a filter</code></pre>
""", practice=["Separate Evens and Odds", "Running Total", "Remove Duplicates, Keep Order", "Common Elements"])


@LD
def building_demo():
    nums = [3, 8, 5, 12]
    doubled = []
    for x in nums:
        doubled.append(x * 2)
    evens = [x for x in nums if x % 2 == 0]
    for i, x in enumerate(nums):
        if x > 6:
            print("index", i, "has", x)
    print(doubled, evens)


LESSON("Core", "Sorting", """
<table>
<tr><th></th><th><code>list.sort()</code></th><th><code>sorted(iterable)</code></th></tr>
<tr><td>Changes the original?</td><td>yes, in place</td><td>no, returns a new list</td></tr>
<tr><td>Returns</td><td><code>None</code></td><td>the sorted list</td></tr>
<tr><td>Works on</td><td>lists only</td><td>any iterable (strings, tuples, dicts…)</td></tr>
</table>
<p>Both accept <code>reverse=True</code> and a <code>key</code> function that says what to sort by:</p>
<pre><code class="py">words.sort(key=len)                          # by length
people.sort(key=lambda p: p[1])              # by the second field
sorted(names, key=str.lower)                 # case-insensitive</code></pre>
<div class="warn"><code>nums = nums.sort()</code> sets nums to None. Use either <code>nums.sort()</code> or <code>nums = sorted(nums)</code>.</div>
""", practice=["Second Largest", "Is the List Sorted?", "Merge Two Sorted Lists"])


@LD
def sorting_demo():
    nums = [5, 2, 9, 1]
    new = sorted(nums)
    nums.sort(reverse=True)
    words = ["kiwi", "fig", "banana"]
    by_len = sorted(words, key=len)
    result = nums.sort()
    print(new, nums, by_len, result)


LESSON("Advanced", "Lists of lists (2-D lists)", """
<p>A list can hold other lists — a simple way to represent a table or grid. <code>grid[r][c]</code> is row r, column c.</p>
<pre><code class="py">grid = [[1, 2, 3],
        [4, 5, 6]]
grid[1][2]          # 6
for row in grid:
    for x in row:
        ...</code></pre>
<div class="warn">Create grids with a comprehension: <code>[[0] * cols for _ in range(rows)]</code>. Writing <code>[[0] * cols] * rows</code> repeats the <b>same</b> row object, so changing one row changes all of them.</div>
""", practice=["Flatten a List of Lists", "Transpose a Matrix", "Split Into Chunks"])


@LD
def grid_demo():
    wrong = [[0] * 3] * 2
    wrong[0][0] = 9
    right = [[0] * 3 for _ in range(2)]
    right[0][0] = 9
    print("wrong:", wrong)
    print("right:", right)


LESSON("Advanced", "Performance of list operations", """
<p>A Python list is a <b>dynamic array</b>: items sit side by side in memory with some spare room at the end.</p>
<table>
<tr><th>Operation</th><th>Cost</th></tr>
<tr><td><code>a[i]</code>, <code>a[i] = x</code>, <code>len(a)</code></td><td>O(1)</td></tr>
<tr><td><code>append</code>, <code>pop()</code></td><td>O(1) (amortised)</td></tr>
<tr><td><code>insert(0, x)</code>, <code>pop(0)</code>, <code>remove(x)</code></td><td>O(n) — items shift</td></tr>
<tr><td><code>x in a</code>, <code>a.index(x)</code>, <code>a.count(x)</code></td><td>O(n) — scans</td></tr>
<tr><td><code>a[i:j]</code>, <code>a + b</code>, <code>a.copy()</code></td><td>O(length of result)</td></tr>
<tr><td><code>sort</code>, <code>sorted</code></td><td>O(n log n)</td></tr>
</table>
<p>That's why the "brute force" answers that call <code>in</code>, <code>remove</code> or <code>insert(0, …)</code> inside a loop are O(n²), while the optimal ones use a set, a dict or a single pass.</p>
""", practice=["Rotate Right by k", "Index of the Maximum"])


@LD
def stack_demo():
    stack = []
    for page in ["home", "search", "result"]:
        stack.append(page)
    back = stack.pop()
    print("went back from", back, "to", stack[-1])
