# DSA Interview Handbook

14 topics · theory with 93 theory questions · 90 lessons from basics to advanced · 280 most-asked interview questions · Python · brute force and optimal solution for each, with a step-by-step animation of the optimal one.

**Live site:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/

Every solution is run against its test cases by `build.py` before the site is generated, and each animation is recorded from a real run of the code you see.

## Topics

- [Arrays & Hashing](#arrays-hashing) — Indexing, prefix sums, hash maps and in-place tricks — the base of every other topic.
- [Two Pointers](#two-pointers) — Two indices walking toward each other or in the same direction to replace a nested loop.
- [Sliding Window](#sliding-window) — Grow a window on the right, shrink it on the left, and never re-scan what's inside.
- [Stack & Queue](#stack-queue) — Last-in-first-out for matching and 'next greater' questions; first-in-first-out for order.
- [Binary Search](#binary-search) — Halve the search space every step — on sorted arrays and on the answer itself.
- [Linked List](#linked-list) — Nodes joined by pointers — master dummy heads, fast/slow pointers and in-place reversal.
- [Trees & BST](#trees-bst) — Recursion on left and right subtrees, BFS by level, and the ordering rule of binary search trees.
- [Heap / Priority Queue](#heap-priority-queue) — Always know the smallest (or largest) item in O(1) and update it in O(log n) — top-k, merging, scheduling.
- [Recursion & Backtracking](#recursion-backtracking) — Build answers one choice at a time, undo the choice, try the next — with pruning to skip dead branches.
- [Graphs](#graphs) — BFS, DFS, topological sort, union-find and shortest paths — on grids and on adjacency lists.
- [Dynamic Programming](#dynamic-programming) — Recursion that remembers: define a state, write the recurrence, fill a table in the right order.
- [Greedy & Intervals](#greedy-intervals) — Make the locally best choice and prove it never hurts — usually after sorting, often on intervals.
- [Tries](#tries) — Prefix trees: share common prefixes so insert, search and 'starts with' cost O(length of the word).
- [Bit Manipulation](#bit-manipulation) — Work on the binary digits directly: XOR cancelling, n & (n − 1), masks and per-bit counting.

## Arrays & Hashing

| # | Question | LeetCode | Level | Pattern |
|---|---|---|---|---|
| 1 | [Two Sum](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/arrays/two-sum) | [1](https://leetcode.com/problems/two-sum/) | Easy | Hash map |
| 2 | [Contains Duplicate](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/arrays/contains-duplicate) | [217](https://leetcode.com/problems/contains-duplicate/) | Easy | Hash set |
| 3 | [Valid Anagram](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/arrays/valid-anagram) | [242](https://leetcode.com/problems/valid-anagram/) | Easy | Counting |
| 4 | [Group Anagrams](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/arrays/group-anagrams) | [49](https://leetcode.com/problems/group-anagrams/) | Medium | Hash map · key design |
| 5 | [Top K Frequent Elements](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/arrays/top-k-frequent-elements) | [347](https://leetcode.com/problems/top-k-frequent-elements/) | Medium | Bucket sort |
| 6 | [Product of Array Except Self](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/arrays/product-of-array-except-self) | [238](https://leetcode.com/problems/product-of-array-except-self/) | Medium | Prefix / suffix |
| 7 | [Longest Consecutive Sequence](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/arrays/longest-consecutive-sequence) | [128](https://leetcode.com/problems/longest-consecutive-sequence/) | Medium | Hash set |
| 8 | [Maximum Subarray](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/arrays/maximum-subarray) | [53](https://leetcode.com/problems/maximum-subarray/) | Medium | Kadane |
| 9 | [Best Time to Buy and Sell Stock](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/arrays/best-time-to-buy-and-sell-stock) | [121](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | Easy | Running minimum |
| 10 | [Majority Element](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/arrays/majority-element) | [169](https://leetcode.com/problems/majority-element/) | Easy | Boyer–Moore voting |
| 11 | [Move Zeroes](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/arrays/move-zeroes) | [283](https://leetcode.com/problems/move-zeroes/) | Easy | Write pointer |
| 12 | [Rotate Array](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/arrays/rotate-array) | [189](https://leetcode.com/problems/rotate-array/) | Medium | Reverse trick |
| 13 | [Subarray Sum Equals K](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/arrays/subarray-sum-equals-k) | [560](https://leetcode.com/problems/subarray-sum-equals-k/) | Medium | Prefix sum + hash map |
| 14 | [Sort Colors](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/arrays/sort-colors) | [75](https://leetcode.com/problems/sort-colors/) | Medium | Dutch national flag |
| 15 | [Next Permutation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/arrays/next-permutation) | [31](https://leetcode.com/problems/next-permutation/) | Medium | Pivot + reverse |
| 16 | [Find the Duplicate Number](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/arrays/find-the-duplicate-number) | [287](https://leetcode.com/problems/find-the-duplicate-number/) | Medium | Floyd cycle |
| 17 | [Missing Number](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/arrays/missing-number) | [268](https://leetcode.com/problems/missing-number/) | Easy | Math / XOR |
| 18 | [Set Matrix Zeroes](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/arrays/set-matrix-zeroes) | [73](https://leetcode.com/problems/set-matrix-zeroes/) | Medium | In-place markers |
| 19 | [Spiral Matrix](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/arrays/spiral-matrix) | [54](https://leetcode.com/problems/spiral-matrix/) | Medium | Boundary shrink |
| 20 | [Rotate Image](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/arrays/rotate-image) | [48](https://leetcode.com/problems/rotate-image/) | Medium | Transpose + reverse |

## Two Pointers

| # | Question | LeetCode | Level | Pattern |
|---|---|---|---|---|
| 1 | [Valid Palindrome](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/two-pointers/valid-palindrome) | [125](https://leetcode.com/problems/valid-palindrome/) | Easy | Opposite ends |
| 2 | [Two Sum II - Input Array Is Sorted](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/two-pointers/two-sum-ii-input-array-is-sorted) | [167](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | Medium | Opposite ends |
| 3 | [3Sum](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/two-pointers/3sum) | [15](https://leetcode.com/problems/3sum/) | Medium | Sort + two pointers |
| 4 | [Container With Most Water](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/two-pointers/container-with-most-water) | [11](https://leetcode.com/problems/container-with-most-water/) | Medium | Opposite ends · greedy |
| 5 | [Trapping Rain Water](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/two-pointers/trapping-rain-water) | [42](https://leetcode.com/problems/trapping-rain-water/) | Hard | Opposite ends · running max |
| 6 | [Remove Duplicates from Sorted Array](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/two-pointers/remove-duplicates-from-sorted-array) | [26](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) | Easy | Read / write |
| 7 | [Merge Sorted Array](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/two-pointers/merge-sorted-array) | [88](https://leetcode.com/problems/merge-sorted-array/) | Easy | Fill from the back |
| 8 | [Squares of a Sorted Array](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/two-pointers/squares-of-a-sorted-array) | [977](https://leetcode.com/problems/squares-of-a-sorted-array/) | Easy | Opposite ends |
| 9 | [Reverse String](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/two-pointers/reverse-string) | [344](https://leetcode.com/problems/reverse-string/) | Easy | Opposite ends · swap |
| 10 | [4Sum](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/two-pointers/4sum) | [18](https://leetcode.com/problems/4sum/) | Medium | Sort + two loops + two pointers |
| 11 | [3Sum Closest](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/two-pointers/3sum-closest) | [16](https://leetcode.com/problems/3sum-closest/) | Medium | Sort + two pointers |
| 12 | [Valid Palindrome II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/two-pointers/valid-palindrome-ii) | [680](https://leetcode.com/problems/valid-palindrome-ii/) | Easy | Opposite ends · one skip |
| 13 | [Is Subsequence](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/two-pointers/is-subsequence) | [392](https://leetcode.com/problems/is-subsequence/) | Easy | Two sequences |
| 14 | [Remove Element](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/two-pointers/remove-element) | [27](https://leetcode.com/problems/remove-element/) | Easy | Read / write |
| 15 | [Boats to Save People](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/two-pointers/boats-to-save-people) | [881](https://leetcode.com/problems/boats-to-save-people/) | Medium | Sort + greedy pairing |
| 16 | [Backspace String Compare](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/two-pointers/backspace-string-compare) | [844](https://leetcode.com/problems/backspace-string-compare/) | Easy | Two pointers from the back |
| 17 | [Sort Array By Parity](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/two-pointers/sort-array-by-parity) | [905](https://leetcode.com/problems/sort-array-by-parity/) | Easy | Partition |
| 18 | [Intersection of Two Arrays II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/two-pointers/intersection-of-two-arrays-ii) | [350](https://leetcode.com/problems/intersection-of-two-arrays-ii/) | Easy | Sort + two sequences |
| 19 | [Reverse Words in a String](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/two-pointers/reverse-words-in-a-string) | [151](https://leetcode.com/problems/reverse-words-in-a-string/) | Medium | Reverse twice |
| 20 | [Reverse Vowels of a String](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/two-pointers/reverse-vowels-of-a-string) | [345](https://leetcode.com/problems/reverse-vowels-of-a-string/) | Easy | Opposite ends · swap |

## Sliding Window

| # | Question | LeetCode | Level | Pattern |
|---|---|---|---|---|
| 1 | [Longest Substring Without Repeating Characters](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/sliding-window/longest-substring-without-repeating-characters) | [3](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Medium | Variable window · last index |
| 2 | [Longest Repeating Character Replacement](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/sliding-window/longest-repeating-character-replacement) | [424](https://leetcode.com/problems/longest-repeating-character-replacement/) | Medium | Variable window · max count |
| 3 | [Permutation in String](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/sliding-window/permutation-in-string) | [567](https://leetcode.com/problems/permutation-in-string/) | Medium | Fixed window · counts |
| 4 | [Minimum Window Substring](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/sliding-window/minimum-window-substring) | [76](https://leetcode.com/problems/minimum-window-substring/) | Hard | Variable window · need / have |
| 5 | [Sliding Window Maximum](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/sliding-window/sliding-window-maximum) | [239](https://leetcode.com/problems/sliding-window-maximum/) | Hard | Monotonic deque |
| 6 | [Minimum Size Subarray Sum](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/sliding-window/minimum-size-subarray-sum) | [209](https://leetcode.com/problems/minimum-size-subarray-sum/) | Medium | Variable window · sum |
| 7 | [Max Consecutive Ones III](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/sliding-window/max-consecutive-ones-iii) | [1004](https://leetcode.com/problems/max-consecutive-ones-iii/) | Medium | Variable window · budget |
| 8 | [Fruit Into Baskets](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/sliding-window/fruit-into-baskets) | [904](https://leetcode.com/problems/fruit-into-baskets/) | Medium | At most 2 distinct |
| 9 | [Maximum Average Subarray I](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/sliding-window/maximum-average-subarray-i) | [643](https://leetcode.com/problems/maximum-average-subarray-i/) | Easy | Fixed window · sum |
| 10 | [Find All Anagrams in a String](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/sliding-window/find-all-anagrams-in-a-string) | [438](https://leetcode.com/problems/find-all-anagrams-in-a-string/) | Medium | Fixed window · counts |
| 11 | [Subarrays with K Different Integers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/sliding-window/subarrays-with-k-different-integers) | [992](https://leetcode.com/problems/subarrays-with-k-different-integers/) | Hard | exactly = atMost(k) − atMost(k−1) |
| 12 | [Number of Substrings Containing All Three Characters](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/sliding-window/number-of-substrings-containing-all-three-characters) | [1358](https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/) | Medium | Variable window · count starts |
| 13 | [Maximum Points You Can Obtain from Cards](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/sliding-window/maximum-points-you-can-obtain-from-cards) | [1423](https://leetcode.com/problems/maximum-points-you-can-obtain-from-cards/) | Medium | Window on the complement |
| 14 | [Contains Duplicate II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/sliding-window/contains-duplicate-ii) | [219](https://leetcode.com/problems/contains-duplicate-ii/) | Easy | Window as a set |
| 15 | [Binary Subarrays With Sum](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/sliding-window/binary-subarrays-with-sum) | [930](https://leetcode.com/problems/binary-subarrays-with-sum/) | Medium | atMost trick on 0/1 |
| 16 | [Count Number of Nice Subarrays](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/sliding-window/count-number-of-nice-subarrays) | [1248](https://leetcode.com/problems/count-number-of-nice-subarrays/) | Medium | atMost trick |
| 17 | [Maximum Number of Vowels in a Substring of Given Length](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/sliding-window/maximum-number-of-vowels-in-a-substring-of-given-length) | [1456](https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/) | Medium | Fixed window · count |
| 18 | [Grumpy Bookstore Owner](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/sliding-window/grumpy-bookstore-owner) | [1052](https://leetcode.com/problems/grumpy-bookstore-owner/) | Medium | Fixed window · extra gain |
| 19 | [Longest Subarray of 1's After Deleting One Element](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/sliding-window/longest-subarray-of-1s-after-deleting-one-element) | [1493](https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/) | Medium | At most one zero |
| 20 | [Frequency of the Most Frequent Element](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/sliding-window/frequency-of-the-most-frequent-element) | [1838](https://leetcode.com/problems/frequency-of-the-most-frequent-element/) | Medium | Sort + window cost |

## Stack & Queue

| # | Question | LeetCode | Level | Pattern |
|---|---|---|---|---|
| 1 | [Valid Parentheses](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/stack-queue/valid-parentheses) | [20](https://leetcode.com/problems/valid-parentheses/) | Easy | Matching stack |
| 2 | [Min Stack](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/stack-queue/min-stack) | [155](https://leetcode.com/problems/min-stack/) | Medium | Stack of (value, min) |
| 3 | [Evaluate Reverse Polish Notation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/stack-queue/evaluate-reverse-polish-notation) | [150](https://leetcode.com/problems/evaluate-reverse-polish-notation/) | Medium | Operand stack |
| 4 | [Daily Temperatures](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/stack-queue/daily-temperatures) | [739](https://leetcode.com/problems/daily-temperatures/) | Medium | Monotonic stack |
| 5 | [Next Greater Element I](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/stack-queue/next-greater-element-i) | [496](https://leetcode.com/problems/next-greater-element-i/) | Easy | Monotonic stack + map |
| 6 | [Next Greater Element II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/stack-queue/next-greater-element-ii) | [503](https://leetcode.com/problems/next-greater-element-ii/) | Medium | Monotonic stack · circular |
| 7 | [Largest Rectangle in Histogram](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/stack-queue/largest-rectangle-in-histogram) | [84](https://leetcode.com/problems/largest-rectangle-in-histogram/) | Hard | Monotonic stack · widths |
| 8 | [Car Fleet](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/stack-queue/car-fleet) | [853](https://leetcode.com/problems/car-fleet/) | Medium | Sort + stack of arrival times |
| 9 | [Asteroid Collision](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/stack-queue/asteroid-collision) | [735](https://leetcode.com/problems/asteroid-collision/) | Medium | Stack simulation |
| 10 | [Decode String](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/stack-queue/decode-string) | [394](https://leetcode.com/problems/decode-string/) | Medium | Stack of (string, count) |
| 11 | [Simplify Path](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/stack-queue/simplify-path) | [71](https://leetcode.com/problems/simplify-path/) | Medium | Stack of directories |
| 12 | [Remove K Digits](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/stack-queue/remove-k-digits) | [402](https://leetcode.com/problems/remove-k-digits/) | Medium | Monotonic stack · greedy |
| 13 | [Online Stock Span](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/stack-queue/online-stock-span) | [901](https://leetcode.com/problems/online-stock-span/) | Medium | Monotonic stack · design |
| 14 | [Sum of Subarray Minimums](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/stack-queue/sum-of-subarray-minimums) | [907](https://leetcode.com/problems/sum-of-subarray-minimums/) | Medium | Monotonic stack · contribution |
| 15 | [Implement Queue using Stacks](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/stack-queue/implement-queue-using-stacks) | [232](https://leetcode.com/problems/implement-queue-using-stacks/) | Easy | Two stacks · amortised |
| 16 | [Implement Stack using Queues](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/stack-queue/implement-stack-using-queues) | [225](https://leetcode.com/problems/implement-stack-using-queues/) | Easy | One queue · rotate |
| 17 | [Basic Calculator II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/stack-queue/basic-calculator-ii) | [227](https://leetcode.com/problems/basic-calculator-ii/) | Medium | Stack with deferred + and − |
| 18 | [Remove All Adjacent Duplicates In String](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/stack-queue/remove-all-adjacent-duplicates-in-string) | [1047](https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string/) | Easy | Stack as the result |
| 19 | [Maximal Rectangle](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/stack-queue/maximal-rectangle) | [85](https://leetcode.com/problems/maximal-rectangle/) | Hard | Histogram per row |
| 20 | [Longest Valid Parentheses](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/stack-queue/longest-valid-parentheses) | [32](https://leetcode.com/problems/longest-valid-parentheses/) | Hard | Stack of indices |

## Binary Search

| # | Question | LeetCode | Level | Pattern |
|---|---|---|---|---|
| 1 | [Binary Search](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/binary-search/binary-search) | [704](https://leetcode.com/problems/binary-search/) | Easy | Closed range |
| 2 | [Search Insert Position](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/binary-search/search-insert-position) | [35](https://leetcode.com/problems/search-insert-position/) | Easy | Lower bound |
| 3 | [Find First and Last Position of Element in Sorted Array](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/binary-search/find-first-and-last-position-of-element-in-sorted-array) | [34](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) | Medium | Lower + upper bound |
| 4 | [Search in Rotated Sorted Array](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/binary-search/search-in-rotated-sorted-array) | [33](https://leetcode.com/problems/search-in-rotated-sorted-array/) | Medium | Find the sorted half |
| 5 | [Find Minimum in Rotated Sorted Array](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/binary-search/find-minimum-in-rotated-sorted-array) | [153](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) | Medium | Compare with right end |
| 6 | [Search a 2D Matrix](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/binary-search/search-a-2d-matrix) | [74](https://leetcode.com/problems/search-a-2d-matrix/) | Medium | Flatten the index |
| 7 | [Koko Eating Bananas](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/binary-search/koko-eating-bananas) | [875](https://leetcode.com/problems/koko-eating-bananas/) | Medium | Search on the answer |
| 8 | [Capacity To Ship Packages Within D Days](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/binary-search/capacity-to-ship-packages-within-d-days) | [1011](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | Medium | Search on the answer |
| 9 | [Median of Two Sorted Arrays](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/binary-search/median-of-two-sorted-arrays) | [4](https://leetcode.com/problems/median-of-two-sorted-arrays/) | Hard | Binary search the partition |
| 10 | [Find Peak Element](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/binary-search/find-peak-element) | [162](https://leetcode.com/problems/find-peak-element/) | Medium | Follow the slope |
| 11 | [Sqrt(x)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/binary-search/sqrt-x) | [69](https://leetcode.com/problems/sqrt-x/) | Easy | Search on the answer |
| 12 | [Split Array Largest Sum](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/binary-search/split-array-largest-sum) | [410](https://leetcode.com/problems/split-array-largest-sum/) | Hard | Minimise the max |
| 13 | [Single Element in a Sorted Array](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/binary-search/single-element-in-a-sorted-array) | [540](https://leetcode.com/problems/single-element-in-a-sorted-array/) | Medium | Pair parity |
| 14 | [Search in Rotated Sorted Array II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/binary-search/search-in-rotated-sorted-array-ii) | [81](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/) | Medium | Rotated with duplicates |
| 15 | [Minimum Number of Days to Make m Bouquets](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/binary-search/minimum-number-of-days-to-make-m-bouquets) | [1482](https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets/) | Medium | Search on the answer |
| 16 | [Find the Smallest Divisor Given a Threshold](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/binary-search/find-the-smallest-divisor-given-a-threshold) | [1283](https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/) | Medium | Search on the answer |
| 17 | [Kth Missing Positive Number](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/binary-search/kth-missing-positive-number) | [1539](https://leetcode.com/problems/kth-missing-positive-number/) | Easy | Missing count at index |
| 18 | [Magnetic Force Between Two Balls](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/binary-search/magnetic-force-between-two-balls) | [1552](https://leetcode.com/problems/magnetic-force-between-two-balls/) | Medium | Maximise the min (aggressive cows) |
| 19 | [Find K Closest Elements](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/binary-search/find-k-closest-elements) | [658](https://leetcode.com/problems/find-k-closest-elements/) | Medium | Binary search the window start |
| 20 | [Search a 2D Matrix II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/binary-search/search-a-2d-matrix-ii) | [240](https://leetcode.com/problems/search-a-2d-matrix-ii/) | Medium | Staircase from a corner |

## Linked List

| # | Question | LeetCode | Level | Pattern |
|---|---|---|---|---|
| 1 | [Reverse Linked List](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/linked-list/reverse-linked-list) | [206](https://leetcode.com/problems/reverse-linked-list/) | Easy | In-place reversal |
| 2 | [Merge Two Sorted Lists](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/linked-list/merge-two-sorted-lists) | [21](https://leetcode.com/problems/merge-two-sorted-lists/) | Easy | Dummy head · splice |
| 3 | [Linked List Cycle](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/linked-list/linked-list-cycle) | [141](https://leetcode.com/problems/linked-list-cycle/) | Easy | Fast & slow |
| 4 | [Linked List Cycle II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/linked-list/linked-list-cycle-ii) | [142](https://leetcode.com/problems/linked-list-cycle-ii/) | Medium | Floyd · find the entrance |
| 5 | [Middle of the Linked List](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/linked-list/middle-of-the-linked-list) | [876](https://leetcode.com/problems/middle-of-the-linked-list/) | Easy | Fast & slow |
| 6 | [Remove Nth Node From End of List](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/linked-list/remove-nth-node-from-end-of-list) | [19](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | Medium | Gap pointers |
| 7 | [Reorder List](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/linked-list/reorder-list) | [143](https://leetcode.com/problems/reorder-list/) | Medium | Middle + reverse + weave |
| 8 | [Palindrome Linked List](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/linked-list/palindrome-linked-list) | [234](https://leetcode.com/problems/palindrome-linked-list/) | Easy | Reverse the second half |
| 9 | [Intersection of Two Linked Lists](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/linked-list/intersection-of-two-linked-lists) | [160](https://leetcode.com/problems/intersection-of-two-linked-lists/) | Easy | Switch heads |
| 10 | [Add Two Numbers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/linked-list/add-two-numbers) | [2](https://leetcode.com/problems/add-two-numbers/) | Medium | Digit-by-digit with carry |
| 11 | [LRU Cache](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/linked-list/lru-cache) | [146](https://leetcode.com/problems/lru-cache/) | Medium | Hash map + doubly linked list |
| 12 | [Merge k Sorted Lists](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/linked-list/merge-k-sorted-lists) | [23](https://leetcode.com/problems/merge-k-sorted-lists/) | Hard | Min-heap of heads |
| 13 | [Reverse Nodes in k-Group](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/linked-list/reverse-nodes-in-k-group) | [25](https://leetcode.com/problems/reverse-nodes-in-k-group/) | Hard | Reverse in chunks |
| 14 | [Rotate List](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/linked-list/rotate-list) | [61](https://leetcode.com/problems/rotate-list/) | Medium | Close the ring, cut |
| 15 | [Remove Duplicates from Sorted List](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/linked-list/remove-duplicates-from-sorted-list) | [83](https://leetcode.com/problems/remove-duplicates-from-sorted-list/) | Easy | Skip equal neighbours |
| 16 | [Odd Even Linked List](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/linked-list/odd-even-linked-list) | [328](https://leetcode.com/problems/odd-even-linked-list/) | Medium | Two chains |
| 17 | [Sort List](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/linked-list/sort-list) | [148](https://leetcode.com/problems/sort-list/) | Medium | Merge sort on a list |
| 18 | [Swap Nodes in Pairs](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/linked-list/swap-nodes-in-pairs) | [24](https://leetcode.com/problems/swap-nodes-in-pairs/) | Medium | Pointer rewiring |
| 19 | [Reverse Linked List II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/linked-list/reverse-linked-list-ii) | [92](https://leetcode.com/problems/reverse-linked-list-ii/) | Medium | Reverse a sub-range |
| 20 | [Partition List](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/linked-list/partition-list) | [86](https://leetcode.com/problems/partition-list/) | Medium | Two dummy lists |

## Trees & BST

| # | Question | LeetCode | Level | Pattern |
|---|---|---|---|---|
| 1 | [Binary Tree Inorder Traversal](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/trees/binary-tree-inorder-traversal) | [94](https://leetcode.com/problems/binary-tree-inorder-traversal/) | Easy | Iterative stack |
| 2 | [Maximum Depth of Binary Tree](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/trees/maximum-depth-of-binary-tree) | [104](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | Easy | Postorder height |
| 3 | [Invert Binary Tree](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/trees/invert-binary-tree) | [226](https://leetcode.com/problems/invert-binary-tree/) | Easy | Swap children recursively |
| 4 | [Same Tree](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/trees/same-tree) | [100](https://leetcode.com/problems/same-tree/) | Easy | Parallel recursion |
| 5 | [Symmetric Tree](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/trees/symmetric-tree) | [101](https://leetcode.com/problems/symmetric-tree/) | Easy | Mirror recursion |
| 6 | [Binary Tree Level Order Traversal](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/trees/binary-tree-level-order-traversal) | [102](https://leetcode.com/problems/binary-tree-level-order-traversal/) | Medium | BFS by level |
| 7 | [Diameter of Binary Tree](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/trees/diameter-of-binary-tree) | [543](https://leetcode.com/problems/diameter-of-binary-tree/) | Easy | Height + global best |
| 8 | [Balanced Binary Tree](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/trees/balanced-binary-tree) | [110](https://leetcode.com/problems/balanced-binary-tree/) | Easy | Height or −1 |
| 9 | [Subtree of Another Tree](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/trees/subtree-of-another-tree) | [572](https://leetcode.com/problems/subtree-of-another-tree/) | Easy | Serialise + substring |
| 10 | [Lowest Common Ancestor of a Binary Search Tree](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/trees/lowest-common-ancestor-of-a-binary-search-tree) | [235](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | Medium | BST split point |
| 11 | [Lowest Common Ancestor of a Binary Tree](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/trees/lowest-common-ancestor-of-a-binary-tree) | [236](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | Medium | Postorder report-up |
| 12 | [Validate Binary Search Tree](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/trees/validate-binary-search-tree) | [98](https://leetcode.com/problems/validate-binary-search-tree/) | Medium | Bounds passed down |
| 13 | [Kth Smallest Element in a BST](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/trees/kth-smallest-element-in-a-bst) | [230](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | Medium | Inorder with early stop |
| 14 | [Binary Tree Right Side View](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/trees/binary-tree-right-side-view) | [199](https://leetcode.com/problems/binary-tree-right-side-view/) | Medium | DFS right-first by depth |
| 15 | [Construct Binary Tree from Preorder and Inorder Traversal](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/trees/construct-binary-tree-from-preorder-and-inorder-traversal) | [105](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | Medium | Split by root index |
| 16 | [Binary Tree Maximum Path Sum](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/trees/binary-tree-maximum-path-sum) | [124](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | Hard | Gain returned up, best through node |
| 17 | [Serialize and Deserialize Binary Tree](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/trees/serialize-and-deserialize-binary-tree) | [297](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | Hard | Preorder with null markers |
| 18 | [Binary Tree Zigzag Level Order Traversal](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/trees/binary-tree-zigzag-level-order-traversal) | [103](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/) | Medium | BFS + direction flag |
| 19 | [Count Good Nodes in Binary Tree](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/trees/count-good-nodes-in-binary-tree) | [1448](https://leetcode.com/problems/count-good-nodes-in-binary-tree/) | Medium | Carry the max downward |
| 20 | [Flatten Binary Tree to Linked List](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/trees/flatten-binary-tree-to-linked-list) | [114](https://leetcode.com/problems/flatten-binary-tree-to-linked-list/) | Medium | Rewire in place (Morris style) |

## Heap / Priority Queue

| # | Question | LeetCode | Level | Pattern |
|---|---|---|---|---|
| 1 | [Kth Largest Element in an Array](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/heap/kth-largest-element-in-an-array) | [215](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Medium | Min-heap of size k |
| 2 | [Kth Largest Element in a Stream](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/heap/kth-largest-element-in-a-stream) | [703](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | Easy | Min-heap of size k · design |
| 3 | [Last Stone Weight](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/heap/last-stone-weight) | [1046](https://leetcode.com/problems/last-stone-weight/) | Easy | Max-heap |
| 4 | [K Closest Points to Origin](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/heap/k-closest-points-to-origin) | [973](https://leetcode.com/problems/k-closest-points-to-origin/) | Medium | Max-heap of size k |
| 5 | [Top K Frequent Words](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/heap/top-k-frequent-words) | [692](https://leetcode.com/problems/top-k-frequent-words/) | Medium | Heap with (−count, word) |
| 6 | [Task Scheduler](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/heap/task-scheduler) | [621](https://leetcode.com/problems/task-scheduler/) | Medium | Max-heap + cooldown queue |
| 7 | [Find Median from Data Stream](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/heap/find-median-from-data-stream) | [295](https://leetcode.com/problems/find-median-from-data-stream/) | Hard | Two heaps |
| 8 | [Reorganize String](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/heap/reorganize-string) | [767](https://leetcode.com/problems/reorganize-string/) | Medium | Max-heap, alternate the top two |
| 9 | [Sort Characters By Frequency](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/heap/sort-characters-by-frequency) | [451](https://leetcode.com/problems/sort-characters-by-frequency/) | Medium | Max-heap of counts |
| 10 | [Find K Pairs with Smallest Sums](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/heap/find-k-pairs-with-smallest-sums) | [373](https://leetcode.com/problems/find-k-pairs-with-smallest-sums/) | Medium | Heap frontier on a sorted grid |
| 11 | [Kth Smallest Element in a Sorted Matrix](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/heap/kth-smallest-element-in-a-sorted-matrix) | [378](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/) | Medium | Heap of row heads |
| 12 | [IPO](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/heap/ipo) | [502](https://leetcode.com/problems/ipo/) | Hard | Sort by capital + max-heap of profit |
| 13 | [Smallest Range Covering Elements from K Lists](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/heap/smallest-range-covering-elements-from-k-lists) | [632](https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/) | Hard | Heap of one per list + running max |
| 14 | [Ugly Number II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/heap/ugly-number-ii) | [264](https://leetcode.com/problems/ugly-number-ii/) | Medium | Heap of multiples |
| 15 | [Single-Threaded CPU](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/heap/single-threaded-cpu) | [1834](https://leetcode.com/problems/single-threaded-cpu/) | Medium | Sort by time + heap by (duration, index) |
| 16 | [Furthest Building You Can Reach](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/heap/furthest-building-you-can-reach) | [1642](https://leetcode.com/problems/furthest-building-you-can-reach/) | Medium | Min-heap of ladder climbs |
| 17 | [Hand of Straights](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/heap/hand-of-straights) | [846](https://leetcode.com/problems/hand-of-straights/) | Medium | Count + min-heap of starts |
| 18 | [Meeting Rooms II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/heap/meeting-rooms-ii) | [253](https://leetcode.com/problems/meeting-rooms-ii/) | Medium | Min-heap of end times |
| 19 | [Maximum Subsequence Score](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/heap/maximum-subsequence-score) | [2542](https://leetcode.com/problems/maximum-subsequence-score/) | Medium | Sort by multiplier + min-heap of sums |
| 20 | [Remove Stones to Minimize the Total](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/heap/remove-stones-to-minimize-the-total) | [1962](https://leetcode.com/problems/remove-stones-to-minimize-the-total/) | Medium | Max-heap |

## Recursion & Backtracking

| # | Question | LeetCode | Level | Pattern |
|---|---|---|---|---|
| 1 | [Subsets](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/backtracking/subsets) | [78](https://leetcode.com/problems/subsets/) | Medium | Include / skip |
| 2 | [Subsets II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/backtracking/subsets-ii) | [90](https://leetcode.com/problems/subsets-ii/) | Medium | Sort + skip duplicates |
| 3 | [Permutations](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/backtracking/permutations) | [46](https://leetcode.com/problems/permutations/) | Medium | used[] array |
| 4 | [Permutations II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/backtracking/permutations-ii) | [47](https://leetcode.com/problems/permutations-ii/) | Medium | Sort + skip used duplicates |
| 5 | [Combination Sum](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/backtracking/combination-sum) | [39](https://leetcode.com/problems/combination-sum/) | Medium | Reuse allowed · prune by sum |
| 6 | [Combination Sum II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/backtracking/combination-sum-ii) | [40](https://leetcode.com/problems/combination-sum-ii/) | Medium | Each once · skip duplicates |
| 7 | [Combinations](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/backtracking/combinations) | [77](https://leetcode.com/problems/combinations/) | Medium | Choose k · prune by count |
| 8 | [Letter Combinations of a Phone Number](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/backtracking/letter-combinations-of-a-phone-number) | [17](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) | Medium | One level per digit |
| 9 | [Generate Parentheses](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/backtracking/generate-parentheses) | [22](https://leetcode.com/problems/generate-parentheses/) | Medium | Open / close counts |
| 10 | [Palindrome Partitioning](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/backtracking/palindrome-partitioning) | [131](https://leetcode.com/problems/palindrome-partitioning/) | Medium | Cut where the prefix is a palindrome |
| 11 | [Word Search](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/backtracking/word-search) | [79](https://leetcode.com/problems/word-search/) | Medium | Grid DFS · mark and unmark |
| 12 | [N-Queens](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/backtracking/n-queens) | [51](https://leetcode.com/problems/n-queens/) | Hard | Row by row with column / diagonal sets |
| 13 | [Sudoku Solver](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/backtracking/sudoku-solver) | [37](https://leetcode.com/problems/sudoku-solver/) | Hard | Constraint sets + most-constrained cell |
| 14 | [Combination Sum III](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/backtracking/combination-sum-iii) | [216](https://leetcode.com/problems/combination-sum-iii/) | Medium | Choose k from 1..9 |
| 15 | [Restore IP Addresses](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/backtracking/restore-ip-addresses) | [93](https://leetcode.com/problems/restore-ip-addresses/) | Medium | Four parts with validity pruning |
| 16 | [Pow(x, n)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/backtracking/pow-x-n) | [50](https://leetcode.com/problems/pow-x-n/) | Medium | Fast exponentiation |
| 17 | [Letter Case Permutation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/backtracking/letter-case-permutation) | [784](https://leetcode.com/problems/letter-case-permutation/) | Medium | Branch on letters only |
| 18 | [Partition to K Equal Sum Subsets](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/backtracking/partition-to-k-equal-sum-subsets) | [698](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/) | Medium | Fill buckets · prune |
| 19 | [Word Break II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/backtracking/word-break-ii) | [140](https://leetcode.com/problems/word-break-ii/) | Hard | Memoised DFS on start index |
| 20 | [Matchsticks to Square](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/backtracking/matchsticks-to-square) | [473](https://leetcode.com/problems/matchsticks-to-square/) | Medium | Four sides · sort + prune |

## Graphs

| # | Question | LeetCode | Level | Pattern |
|---|---|---|---|---|
| 1 | [Number of Islands](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/graphs/number-of-islands) | [200](https://leetcode.com/problems/number-of-islands/) | Medium | DFS flood fill |
| 2 | [Flood Fill](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/graphs/flood-fill) | [733](https://leetcode.com/problems/flood-fill/) | Easy | DFS from the start pixel |
| 3 | [Max Area of Island](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/graphs/max-area-of-island) | [695](https://leetcode.com/problems/max-area-of-island/) | Medium | DFS returning area |
| 4 | [Rotting Oranges](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/graphs/rotting-oranges) | [994](https://leetcode.com/problems/rotting-oranges/) | Medium | Multi-source BFS |
| 5 | [01 Matrix](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/graphs/01-matrix) | [542](https://leetcode.com/problems/01-matrix/) | Medium | Multi-source BFS from zeros |
| 6 | [Surrounded Regions](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/graphs/surrounded-regions) | [130](https://leetcode.com/problems/surrounded-regions/) | Medium | Search from the border |
| 7 | [Pacific Atlantic Water Flow](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/graphs/pacific-atlantic-water-flow) | [417](https://leetcode.com/problems/pacific-atlantic-water-flow/) | Medium | Reverse DFS from both oceans |
| 8 | [Number of Provinces](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/graphs/number-of-provinces) | [547](https://leetcode.com/problems/number-of-provinces/) | Medium | Union–Find |
| 9 | [Is Graph Bipartite?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/graphs/is-graph-bipartite) | [785](https://leetcode.com/problems/is-graph-bipartite/) | Medium | BFS 2-colouring |
| 10 | [Course Schedule](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/graphs/course-schedule) | [207](https://leetcode.com/problems/course-schedule/) | Medium | Kahn's topological sort |
| 11 | [Course Schedule II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/graphs/course-schedule-ii) | [210](https://leetcode.com/problems/course-schedule-ii/) | Medium | Topological order |
| 12 | [Find Eventual Safe States](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/graphs/find-eventual-safe-states) | [802](https://leetcode.com/problems/find-eventual-safe-states/) | Medium | 3-colour DFS |
| 13 | [Redundant Connection](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/graphs/redundant-connection) | [684](https://leetcode.com/problems/redundant-connection/) | Medium | Union–Find detects the cycle edge |
| 14 | [Accounts Merge](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/graphs/accounts-merge) | [721](https://leetcode.com/problems/accounts-merge/) | Medium | Union–Find over emails |
| 15 | [Word Ladder](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/graphs/word-ladder) | [127](https://leetcode.com/problems/word-ladder/) | Hard | BFS with wildcard buckets |
| 16 | [Shortest Path in Binary Matrix](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/graphs/shortest-path-in-binary-matrix) | [1091](https://leetcode.com/problems/shortest-path-in-binary-matrix/) | Medium | BFS, 8 directions |
| 17 | [Network Delay Time](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/graphs/network-delay-time) | [743](https://leetcode.com/problems/network-delay-time/) | Medium | Dijkstra |
| 18 | [Cheapest Flights Within K Stops](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/graphs/cheapest-flights-within-k-stops) | [787](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | Medium | Bellman–Ford, k + 1 rounds |
| 19 | [Path With Minimum Effort](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/graphs/path-with-minimum-effort) | [1631](https://leetcode.com/problems/path-with-minimum-effort/) | Medium | Dijkstra on max edge |
| 20 | [Min Cost to Connect All Points](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/graphs/min-cost-to-connect-all-points) | [1584](https://leetcode.com/problems/min-cost-to-connect-all-points/) | Medium | Prim's MST (dense) |

## Dynamic Programming

| # | Question | LeetCode | Level | Pattern |
|---|---|---|---|---|
| 1 | [Climbing Stairs](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/dp/climbing-stairs) | [70](https://leetcode.com/problems/climbing-stairs/) | Easy | 1-D · Fibonacci |
| 2 | [Min Cost Climbing Stairs](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/dp/min-cost-climbing-stairs) | [746](https://leetcode.com/problems/min-cost-climbing-stairs/) | Easy | 1-D · min of two |
| 3 | [House Robber](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/dp/house-robber) | [198](https://leetcode.com/problems/house-robber/) | Medium | 1-D · take or skip |
| 4 | [House Robber II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/dp/house-robber-ii) | [213](https://leetcode.com/problems/house-robber-ii/) | Medium | Circle → two linear runs |
| 5 | [Coin Change](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/dp/coin-change) | [322](https://leetcode.com/problems/coin-change/) | Medium | Unbounded knapsack · min |
| 6 | [Coin Change II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/dp/coin-change-ii) | [518](https://leetcode.com/problems/coin-change-ii/) | Medium | Count combinations |
| 7 | [Longest Increasing Subsequence](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/dp/longest-increasing-subsequence) | [300](https://leetcode.com/problems/longest-increasing-subsequence/) | Medium | Patience sorting · binary search |
| 8 | [Longest Common Subsequence](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/dp/longest-common-subsequence) | [1143](https://leetcode.com/problems/longest-common-subsequence/) | Medium | Two strings · 2-D table |
| 9 | [Edit Distance](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/dp/edit-distance) | [72](https://leetcode.com/problems/edit-distance/) | Medium | Two strings · insert / delete / replace |
| 10 | [Partition Equal Subset Sum](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/dp/partition-equal-subset-sum) | [416](https://leetcode.com/problems/partition-equal-subset-sum/) | Medium | 0/1 knapsack · reachable sums |
| 11 | [Word Break](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/dp/word-break) | [139](https://leetcode.com/problems/word-break/) | Medium | 1-D over prefixes |
| 12 | [Unique Paths](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/dp/unique-paths) | [62](https://leetcode.com/problems/unique-paths/) | Medium | Grid · from top and left |
| 13 | [Minimum Path Sum](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/dp/minimum-path-sum) | [64](https://leetcode.com/problems/minimum-path-sum/) | Medium | Grid · min of top and left |
| 14 | [Decode Ways](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/dp/decode-ways) | [91](https://leetcode.com/problems/decode-ways/) | Medium | 1-D · one or two digits |
| 15 | [Longest Palindromic Substring](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/dp/longest-palindromic-substring) | [5](https://leetcode.com/problems/longest-palindromic-substring/) | Medium | Expand around centres |
| 16 | [Maximum Product Subarray](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/dp/maximum-product-subarray) | [152](https://leetcode.com/problems/maximum-product-subarray/) | Medium | Track max and min |
| 17 | [Target Sum](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/dp/target-sum) | [494](https://leetcode.com/problems/target-sum/) | Medium | Subset-sum count |
| 18 | [Best Time to Buy and Sell Stock with Cooldown](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/dp/best-time-to-buy-and-sell-stock-with-cooldown) | [309](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) | Medium | State machine DP |
| 19 | [Burst Balloons](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/dp/burst-balloons) | [312](https://leetcode.com/problems/burst-balloons/) | Hard | Interval DP · last balloon |
| 20 | [Maximal Square](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/dp/maximal-square) | [221](https://leetcode.com/problems/maximal-square/) | Medium | Grid · min of three neighbours |

## Greedy & Intervals

| # | Question | LeetCode | Level | Pattern |
|---|---|---|---|---|
| 1 | [Jump Game](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/greedy/jump-game) | [55](https://leetcode.com/problems/jump-game/) | Medium | Furthest reach |
| 2 | [Jump Game II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/greedy/jump-game-ii) | [45](https://leetcode.com/problems/jump-game-ii/) | Medium | BFS by reach windows |
| 3 | [Gas Station](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/greedy/gas-station) | [134](https://leetcode.com/problems/gas-station/) | Medium | Running tank, restart on deficit |
| 4 | [Merge Intervals](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/greedy/merge-intervals) | [56](https://leetcode.com/problems/merge-intervals/) | Medium | Sort by start |
| 5 | [Insert Interval](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/greedy/insert-interval) | [57](https://leetcode.com/problems/insert-interval/) | Medium | Three phases: before, overlap, after |
| 6 | [Non-overlapping Intervals](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/greedy/non-overlapping-intervals) | [435](https://leetcode.com/problems/non-overlapping-intervals/) | Medium | Sort by end, keep earliest finish |
| 7 | [Minimum Number of Arrows to Burst Balloons](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/greedy/minimum-number-of-arrows-to-burst-balloons) | [452](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/) | Medium | Sort by end, shoot at the end |
| 8 | [Partition Labels](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/greedy/partition-labels) | [763](https://leetcode.com/problems/partition-labels/) | Medium | Last occurrence |
| 9 | [Assign Cookies](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/greedy/assign-cookies) | [455](https://leetcode.com/problems/assign-cookies/) | Easy | Sort both, smallest that fits |
| 10 | [Lemonade Change](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/greedy/lemonade-change) | [860](https://leetcode.com/problems/lemonade-change/) | Easy | Give the biggest change first |
| 11 | [Candy](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/greedy/candy) | [135](https://leetcode.com/problems/candy/) | Hard | Two passes |
| 12 | [Valid Parenthesis String](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/greedy/valid-parenthesis-string) | [678](https://leetcode.com/problems/valid-parenthesis-string/) | Medium | Range of open counts |
| 13 | [Best Time to Buy and Sell Stock II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/greedy/best-time-to-buy-and-sell-stock-ii) | [122](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) | Medium | Take every rise |
| 14 | [Largest Number](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/greedy/largest-number) | [179](https://leetcode.com/problems/largest-number/) | Medium | Custom comparator a+b vs b+a |
| 15 | [Queue Reconstruction by Height](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/greedy/queue-reconstruction-by-height) | [406](https://leetcode.com/problems/queue-reconstruction-by-height/) | Medium | Tallest first, insert at k |
| 16 | [Interval List Intersections](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/greedy/interval-list-intersections) | [986](https://leetcode.com/problems/interval-list-intersections/) | Medium | Two pointers on intervals |
| 17 | [Two City Scheduling](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/greedy/two-city-scheduling) | [1029](https://leetcode.com/problems/two-city-scheduling/) | Medium | Sort by cost difference |
| 18 | [Maximum Units on a Truck](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/greedy/maximum-units-on-a-truck) | [1710](https://leetcode.com/problems/maximum-units-on-a-truck/) | Easy | Best units per box first |
| 19 | [Remove Covered Intervals](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/greedy/remove-covered-intervals) | [1288](https://leetcode.com/problems/remove-covered-intervals/) | Medium | Sort by start asc, end desc |
| 20 | [Car Pooling](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/greedy/car-pooling) | [1094](https://leetcode.com/problems/car-pooling/) | Medium | Sweep line over stops |

## Tries

| # | Question | LeetCode | Level | Pattern |
|---|---|---|---|---|
| 1 | [Implement Trie (Prefix Tree)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/tries/implement-trie-prefix-tree) | [208](https://leetcode.com/problems/implement-trie-prefix-tree/) | Medium | Trie node class |
| 2 | [Design Add and Search Words Data Structure](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/tries/design-add-and-search-words-data-structure) | [211](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | Medium | Trie + DFS on '.' |
| 3 | [Word Search II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/tries/word-search-ii) | [212](https://leetcode.com/problems/word-search-ii/) | Hard | Trie-guided grid DFS |
| 4 | [Longest Common Prefix](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/tries/longest-common-prefix) | [14](https://leetcode.com/problems/longest-common-prefix/) | Easy | Walk the single-child chain |
| 5 | [Replace Words](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/tries/replace-words) | [648](https://leetcode.com/problems/replace-words/) | Medium | Shortest root in a trie |
| 6 | [Longest Word in Dictionary](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/tries/longest-word-in-dictionary) | [720](https://leetcode.com/problems/longest-word-in-dictionary/) | Medium | DFS through end nodes only |
| 7 | [Search Suggestions System](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/tries/search-suggestions-system) | [1268](https://leetcode.com/problems/search-suggestions-system/) | Medium | Trie nodes keep top 3 |
| 8 | [Maximum XOR of Two Numbers in an Array](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/tries/maximum-xor-of-two-numbers-in-an-array) | [421](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/) | Medium | Binary trie, greedy opposite bit |
| 9 | [Map Sum Pairs](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/tries/map-sum-pairs) | [677](https://leetcode.com/problems/map-sum-pairs/) | Medium | Trie with prefix totals |
| 10 | [Prefix and Suffix Search](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/tries/prefix-and-suffix-search) | [745](https://leetcode.com/problems/prefix-and-suffix-search/) | Hard | Trie of 'suffix#word' |
| 11 | [Stream of Characters](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/tries/stream-of-characters) | [1032](https://leetcode.com/problems/stream-of-characters/) | Hard | Trie of reversed words |
| 12 | [Concatenated Words](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/tries/concatenated-words) | [472](https://leetcode.com/problems/concatenated-words/) | Hard | Trie + word-break DFS |
| 13 | [Palindrome Pairs](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/tries/palindrome-pairs) | [336](https://leetcode.com/problems/palindrome-pairs/) | Hard | Split each word, look up the reverse |
| 14 | [Maximum XOR With an Element From Array](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/tries/maximum-xor-with-an-element-from-array) | [1707](https://leetcode.com/problems/maximum-xor-with-an-element-from-array/) | Hard | Offline queries + binary trie |
| 15 | [Sum of Prefix Scores of Strings](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/tries/sum-of-prefix-scores-of-strings) | [2416](https://leetcode.com/problems/sum-of-prefix-scores-of-strings/) | Hard | Trie with pass counts |
| 16 | [Short Encoding of Words](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/tries/short-encoding-of-words) | [820](https://leetcode.com/problems/short-encoding-of-words/) | Medium | Trie of reversed words, count leaves |
| 17 | [Lexicographical Numbers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/tries/lexicographical-numbers) | [386](https://leetcode.com/problems/lexicographical-numbers/) | Medium | Preorder walk of the digit trie |
| 18 | [K-th Smallest in Lexicographical Order](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/tries/k-th-smallest-in-lexicographical-order) | [440](https://leetcode.com/problems/k-th-smallest-in-lexicographical-order/) | Hard | Count subtree sizes, skip |
| 19 | [Remove Sub-Folders from the Filesystem](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/tries/remove-sub-folders-from-the-filesystem) | [1233](https://leetcode.com/problems/remove-sub-folders-from-the-filesystem/) | Medium | Trie of path parts |
| 20 | [Counting Words With a Given Prefix](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/tries/counting-words-with-a-given-prefix) | [2185](https://leetcode.com/problems/counting-words-with-a-given-prefix/) | Easy | Trie with counts |

## Bit Manipulation

| # | Question | LeetCode | Level | Pattern |
|---|---|---|---|---|
| 1 | [Single Number](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/bits/single-number) | [136](https://leetcode.com/problems/single-number/) | Easy | XOR cancels pairs |
| 2 | [Single Number II](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/bits/single-number-ii) | [137](https://leetcode.com/problems/single-number-ii/) | Medium | Count bits mod 3 (ones / twos) |
| 3 | [Single Number III](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/bits/single-number-iii) | [260](https://leetcode.com/problems/single-number-iii/) | Medium | XOR, then split by a differing bit |
| 4 | [Number of 1 Bits](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/bits/number-of-1-bits) | [191](https://leetcode.com/problems/number-of-1-bits/) | Easy | n & (n − 1) |
| 5 | [Counting Bits](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/bits/counting-bits) | [338](https://leetcode.com/problems/counting-bits/) | Easy | DP on i >> 1 |
| 6 | [Reverse Bits](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/bits/reverse-bits) | [190](https://leetcode.com/problems/reverse-bits/) | Easy | Swap halves with masks |
| 7 | [Power of Two](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/bits/power-of-two) | [231](https://leetcode.com/problems/power-of-two/) | Easy | Exactly one set bit |
| 8 | [Power of Four](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/bits/power-of-four) | [342](https://leetcode.com/problems/power-of-four/) | Easy | One bit, on an even position |
| 9 | [Sum of Two Integers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/bits/sum-of-two-integers) | [371](https://leetcode.com/problems/sum-of-two-integers/) | Medium | XOR = sum without carry, AND = carry |
| 10 | [Bitwise AND of Numbers Range](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/bits/bitwise-and-of-numbers-range) | [201](https://leetcode.com/problems/bitwise-and-of-numbers-range/) | Medium | Common binary prefix |
| 11 | [Hamming Distance](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/bits/hamming-distance) | [461](https://leetcode.com/problems/hamming-distance/) | Easy | Popcount of XOR |
| 12 | [Total Hamming Distance](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/bits/total-hamming-distance) | [477](https://leetcode.com/problems/total-hamming-distance/) | Medium | Count each bit: ones × zeros |
| 13 | [Sum of All Subset XOR Totals](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/bits/sum-of-all-subset-xor-totals) | [1863](https://leetcode.com/problems/sum-of-all-subset-xor-totals/) | Easy | Each bit is in half the subsets |
| 14 | [Find the Difference](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/bits/find-the-difference) | [389](https://leetcode.com/problems/find-the-difference/) | Easy | XOR all characters |
| 15 | [Divide Two Integers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/bits/divide-two-integers) | [29](https://leetcode.com/problems/divide-two-integers/) | Medium | Subtract shifted divisors |
| 16 | [Minimum Flips to Make a OR b Equal to c](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/bits/minimum-flips-to-make-a-or-b-equal-to-c) | [1318](https://leetcode.com/problems/minimum-flips-to-make-a-or-b-equal-to-c/) | Medium | Per-bit cases |
| 17 | [Minimum Bit Flips to Convert Number](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/bits/minimum-bit-flips-to-convert-number) | [2220](https://leetcode.com/problems/minimum-bit-flips-to-convert-number/) | Easy | Popcount of XOR |
| 18 | [Count Triplets That Can Form Two Arrays of Equal XOR](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/bits/count-triplets-that-can-form-two-arrays-of-equal-xor) | [1442](https://leetcode.com/problems/count-triplets-that-can-form-two-arrays-of-equal-xor/) | Medium | Prefix XOR + index sums |
| 19 | [XOR Queries of a Subarray](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/bits/xor-queries-of-a-subarray) | [1310](https://leetcode.com/problems/xor-queries-of-a-subarray/) | Medium | Prefix XOR |
| 20 | [Gray Code](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/handbook/#/q/bits/gray-code) | [89](https://leetcode.com/problems/gray-code/) | Medium | i ^ (i >> 1) |

## Build

```bash
python3 handbook/build.py
```

Sources live in `handbook/src/`: `topics/` (questions and solutions), `lessons/` and `theory/`.
