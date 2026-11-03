# Python from Scratch

12 topics · theory with 89 theory questions · 75 lessons from basics to advanced · 240 practice questions with answers · for complete beginners · every question has a brute-force and an optimal solution, and both are shown running line by line like Python Tutor.

**Live site:** https://abpandey-dev.github.io/python-dsa-visualizer/python-course/

Every solution is run against its test cases by `build.py` before the site is generated, and each animation is recorded from a real run of the code you see.

## Topics

- [Python Basics](#python-basics) — Your first programs: print, variables, data types, type conversion and input.
- [Operators & Expressions](#operators-expressions) — Arithmetic, comparison, logical, assignment, identity, membership and bitwise operators — and the order Python applies them.
- [Conditions (if / elif / else)](#conditions-if-elif-else) — Make decisions: if, elif, else, nested conditions, the one-line conditional and match-case.
- [Loops (for / while)](#loops-for-while) — Repeat work with for and while, control loops with break and continue, and nest loops for patterns.
- [Strings](#strings) — Text in Python: indexing, slicing, string methods, formatting and why strings can't be changed in place.
- [Lists](#lists) — Ordered, changeable collections: indexing, methods, slicing, copying, sorting and lists of lists.
- [Tuples & Sets](#tuples-sets) — Tuples: fixed records and unpacking. Sets: unique items, fast membership and set algebra.
- [Dictionaries](#dictionaries) — Key → value maps: lookups, updates, counting, grouping, nesting and dict comprehensions.
- [Functions & Recursion](#functions-recursion) — Package code into reusable functions: parameters, return values, scope, lambdas, closures and recursion.
- [Comprehensions, Iterators & Generators](#comprehensions-iterators-generators) — Build collections in one line, use the iteration built-ins, and produce values lazily with generators.
- [Object-Oriented Programming](#object-oriented-programming) — Model things as objects: classes, attributes, methods, encapsulation, inheritance, polymorphism and special methods.
- [Errors, Exceptions & Files](#errors-exceptions-files) — Handle things that go wrong with try / except / else / finally, raise your own errors, and read and write files safely.

## Python Basics

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Swap Two Variables](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/basics/swap-two-variables) | Easy | Variables · tuple assignment |
| 2 | [Celsius to Fahrenheit](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/basics/celsius-to-fahrenheit) | Easy | Arithmetic · float |
| 3 | [Rectangle Area and Perimeter](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/basics/rectangle-area-and-perimeter) | Easy | Variables · returning two values |
| 4 | [Add Two Numbers Given as Text](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/basics/add-two-numbers-given-as-text) | Easy | Type conversion |
| 5 | [Name of a Value's Type](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/basics/name-of-a-values-type) | Easy | Data types · type() |
| 6 | [Minutes to Hours and Minutes](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/basics/minutes-to-hours-and-minutes) | Easy | // and % |
| 7 | [Sum of Digits](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/basics/sum-of-digits) | Easy | // and % · str |
| 8 | [Last Digit](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/basics/last-digit) | Easy | % operator |
| 9 | [Average of Three Numbers](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/basics/average-of-three-numbers) | Easy | Arithmetic |
| 10 | [Is It Truthy?](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/basics/is-it-truthy) | Easy | bool · truthiness |
| 11 | [Full Name](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/basics/full-name) | Easy | String joining · f-strings |
| 12 | [Seconds to Clock Time](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/basics/seconds-to-clock-time) | Medium | divmod · formatting |
| 13 | [Format Money](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/basics/format-money) | Easy | Format specifiers |
| 14 | [Count the True Values](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/basics/count-the-true-values) | Easy | bool is a kind of int |
| 15 | [Distance Between Two Points](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/basics/distance-between-two-points) | Easy | math module |
| 16 | [Quotient and Remainder](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/basics/quotient-and-remainder) | Easy | divmod |
| 17 | [Kilometres to Miles](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/basics/kilometres-to-miles) | Easy | Constants · rounding |
| 18 | [Is It a Whole Number String?](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/basics/is-it-a-whole-number-string) | Easy | str methods · conversion |
| 19 | [Greeting From Input](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/basics/greeting-from-input) | Easy | input() · f-strings |
| 20 | [Bill Split With Tip](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/basics/bill-split-with-tip) | Medium | Expressions · rounding |

## Operators & Expressions

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Even or Odd](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/operators/even-or-odd) | Easy | % operator |
| 2 | [Leap Year](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/operators/leap-year) | Easy | and / or |
| 3 | [Power Without **](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/operators/power-without) | Easy | ** · loops |
| 4 | [Absolute Value](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/operators/absolute-value) | Easy | Unary minus · abs() |
| 5 | [Largest of Three](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/operators/largest-of-three) | Easy | Comparison operators |
| 6 | [FizzBuzz Word](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/operators/fizzbuzz-word) | Easy | % · and |
| 7 | [Compound Interest](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/operators/compound-interest) | Easy | ** operator |
| 8 | [Perfect Square](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/operators/perfect-square) | Easy | ** · math.isqrt |
| 9 | [Reverse a Number](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/operators/reverse-a-number) | Medium | // and % |
| 10 | [Floats Almost Equal](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/operators/floats-almost-equal) | Easy | Float comparison |
| 11 | [Ceiling Division](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/operators/ceiling-division) | Easy | // trick |
| 12 | [Power of Two](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/operators/power-of-two) | Medium | Bitwise & |
| 13 | [Count Digits](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/operators/count-digits) | Easy | // · len(str()) |
| 14 | [Round to Nearest Multiple](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/operators/round-to-nearest-multiple) | Medium | // and arithmetic |
| 15 | [Exactly One Is True](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/operators/exactly-one-is-true) | Easy | Logical operators |
| 16 | [Within a Range](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/operators/within-a-range) | Easy | Chained comparison |
| 17 | [Sum From 1 to n](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/operators/sum-from-1-to-n) | Easy | Formula vs loop |
| 18 | [Weekly Pay With Overtime](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/operators/weekly-pay-with-overtime) | Medium | min / max arithmetic |
| 19 | [Number of Handshakes](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/operators/number-of-handshakes) | Easy | Formula vs nested loop |
| 20 | [Clamp a Value](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/operators/clamp-a-value) | Easy | min and max |

## Conditions (if / elif / else)

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Positive, Negative or Zero](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/conditions/positive-negative-or-zero) | Easy | if / elif / else |
| 2 | [Grade From Marks](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/conditions/grade-from-marks) | Easy | elif chain |
| 3 | [Ticket Price by Age](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/conditions/ticket-price-by-age) | Easy | Ranges |
| 4 | [Larger of Two](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/conditions/larger-of-two) | Easy | Conditional expression |
| 5 | [Triangle Type](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/conditions/triangle-type) | Medium | Combined conditions |
| 6 | [Vowel or Consonant](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/conditions/vowel-or-consonant) | Easy | in operator |
| 7 | [Day Name](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/conditions/day-name) | Easy | elif chain vs lookup |
| 8 | [BMI Category](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/conditions/bmi-category) | Easy | Float conditions |
| 9 | [Simple Calculator](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/conditions/simple-calculator) | Medium | match-case |
| 10 | [Quadrant of a Point](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/conditions/quadrant-of-a-point) | Easy | Nested conditions |
| 11 | [Shopping Discount](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/conditions/shopping-discount) | Easy | Tiers |
| 12 | [Can It Be a Triangle?](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/conditions/can-it-be-a-triangle) | Easy | and |
| 13 | [Electricity Bill](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/conditions/electricity-bill) | Medium | Slabs |
| 14 | [Rock Paper Scissors](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/conditions/rock-paper-scissors) | Medium | Conditions vs lookup |
| 15 | [Greeting by Hour](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/conditions/greeting-by-hour) | Easy | Chained comparisons |
| 16 | [Sort Three Numbers](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/conditions/sort-three-numbers) | Medium | Swaps with if |
| 17 | [Strong Password](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/conditions/strong-password) | Medium | Conditions with any() |
| 18 | [Character Type](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/conditions/character-type) | Easy | str methods in conditions |
| 19 | [Days in a Month](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/conditions/days-in-a-month) | Medium | Conditions + lookup |
| 20 | [Next Traffic Light](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/conditions/next-traffic-light) | Easy | Lookup instead of if |

## Loops (for / while)

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Multiplication Table](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/loops/multiplication-table) | Easy | for · range |
| 2 | [Factorial](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/loops/factorial) | Easy | Accumulator |
| 3 | [Count Vowels](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/loops/count-vowels) | Easy | Loop over a string |
| 4 | [Sum of Even Numbers](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/loops/sum-of-even-numbers) | Easy | range with step |
| 5 | [Fibonacci Sequence](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/loops/fibonacci-sequence) | Easy | Two running variables |
| 6 | [Is It Prime?](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/loops/is-it-prime) | Medium | Loop with early exit |
| 7 | [Greatest Common Divisor](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/loops/greatest-common-divisor) | Medium | while loop · Euclid |
| 8 | [Countdown](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/loops/countdown) | Easy | range backwards |
| 9 | [First Position of a Value](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/loops/first-position-of-a-value) | Easy | break · enumerate |
| 10 | [Star Triangle](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/loops/star-triangle) | Easy | Nested loops · patterns |
| 11 | [Collatz Steps](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/loops/collatz-steps) | Medium | while with a changing condition |
| 12 | [Digital Root](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/loops/digital-root) | Medium | Nested while loops |
| 13 | [Armstrong Number](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/loops/armstrong-number) | Medium | Loop over digits |
| 14 | [Count Multiples in a Range](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/loops/count-multiples-in-a-range) | Easy | Loop vs formula |
| 15 | [Primes Up To n](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/loops/primes-up-to-n) | Hard | Sieve of Eratosthenes |
| 16 | [Largest in a List](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/loops/largest-in-a-list) | Easy | Running maximum |
| 17 | [Perfect Number](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/loops/perfect-number) | Medium | Divisor pairs |
| 18 | [Sum Skipping Negatives](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/loops/sum-skipping-negatives) | Easy | continue |
| 19 | [Pairs With a Given Sum](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/loops/pairs-with-a-given-sum) | Medium | Nested loops vs set |
| 20 | [Smallest Divisor](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/loops/smallest-divisor) | Easy | for … else |

## Strings

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Reverse a String](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/strings/reverse-a-string) | Easy | Slicing |
| 2 | [Palindrome Word](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/strings/palindrome-word) | Easy | Comparison · lower() |
| 3 | [Count a Character](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/strings/count-a-character) | Easy | count() |
| 4 | [Capitalise Each Word](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/strings/capitalise-each-word) | Easy | split · join · capitalize |
| 5 | [Count Words](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/strings/count-words) | Easy | split() |
| 6 | [Remove Vowels](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/strings/remove-vowels) | Easy | Building strings |
| 7 | [Anagram Check](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/strings/anagram-check) | Medium | sorted · Counter |
| 8 | [Title Initials](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/strings/title-initials) | Easy | split · indexing |
| 9 | [Replace Spaces](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/strings/replace-spaces) | Easy | replace() |
| 10 | [Most Frequent Character](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/strings/most-frequent-character) | Medium | Counting |
| 11 | [Compress Repeated Letters](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/strings/compress-repeated-letters) | Medium | Run-length encoding |
| 12 | [Is It a Pangram?](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/strings/is-it-a-pangram) | Medium | Sets of characters |
| 13 | [Swap Case](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/strings/swap-case) | Easy | Character methods |
| 14 | [Longest Word](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/strings/longest-word) | Easy | max with key |
| 15 | [Mask a Card Number](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/strings/mask-a-card-number) | Easy | Slicing · repetition |
| 16 | [Caesar Cipher](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/strings/caesar-cipher) | Medium | ord · chr · % |
| 17 | [Only Digits](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/strings/only-digits) | Easy | Filtering characters |
| 18 | [First Non-Repeating Character](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/strings/first-non-repeating-character) | Medium | Counting · order |
| 19 | [Centre a Title](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/strings/centre-a-title) | Easy | Format specifiers |
| 20 | [Valid Username](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/strings/valid-username) | Medium | Several checks |

## Lists

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Sum of a List](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/lists/sum-of-a-list) | Easy | Accumulator vs sum() |
| 2 | [Average of a List](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/lists/average-of-a-list) | Easy | sum / len |
| 3 | [Remove Duplicates, Keep Order](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/lists/remove-duplicates-keep-order) | Easy | in vs dict |
| 4 | [Second Largest](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/lists/second-largest) | Medium | One pass |
| 5 | [Reverse a List in Place](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/lists/reverse-a-list-in-place) | Easy | Swapping |
| 6 | [Rotate Right by k](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/lists/rotate-right-by-k) | Medium | Slicing |
| 7 | [Merge Two Sorted Lists](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/lists/merge-two-sorted-lists) | Medium | Two indices |
| 8 | [Flatten a List of Lists](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/lists/flatten-a-list-of-lists) | Easy | Nested loops vs comprehension |
| 9 | [Count Occurrences](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/lists/count-occurrences) | Easy | count() |
| 10 | [Common Elements](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/lists/common-elements) | Medium | Nested loop vs set |
| 11 | [Move Zeros to the End](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/lists/move-zeros-to-the-end) | Medium | In-place write index |
| 12 | [Split Into Chunks](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/lists/split-into-chunks) | Easy | Slicing with a step |
| 13 | [Running Total](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/lists/running-total) | Easy | Prefix sums |
| 14 | [Transpose a Matrix](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/lists/transpose-a-matrix) | Medium | Lists of lists · zip |
| 15 | [Product of a List](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/lists/product-of-a-list) | Easy | math.prod |
| 16 | [Remove Every Copy of a Value](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/lists/remove-every-copy-of-a-value) | Easy | remove() vs comprehension |
| 17 | [Index of the Maximum](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/lists/index-of-the-maximum) | Easy | max with key |
| 18 | [Is the List Sorted?](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/lists/is-the-list-sorted) | Easy | Neighbour pairs |
| 19 | [Separate Evens and Odds](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/lists/separate-evens-and-odds) | Easy | Building two lists |
| 20 | [Shopping Cart Total](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/lists/shopping-cart-total) | Easy | List of pairs |

## Tuples & Sets

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Swap a Pair](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/tuples-sets/swap-a-pair) | Easy | Tuple unpacking |
| 2 | [Min and Max Together](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/tuples-sets/min-and-max-together) | Easy | Returning a tuple |
| 3 | [Describe a Record](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/tuples-sets/describe-a-record) | Easy | Unpacking |
| 4 | [Sort Pairs by Second Item](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/tuples-sets/sort-pairs-by-second-item) | Medium | sorted with key |
| 5 | [Distance From Origin](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/tuples-sets/distance-from-origin) | Easy | Tuple unpacking · math |
| 6 | [Count in a Tuple](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/tuples-sets/count-in-a-tuple) | Easy | tuple.count |
| 7 | [Pair Up Two Lists](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/tuples-sets/pair-up-two-lists) | Easy | zip |
| 8 | [Unzip Pairs](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/tuples-sets/unzip-pairs) | Medium | zip(*pairs) |
| 9 | [Distinct Cells Visited](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/tuples-sets/distinct-cells-visited) | Medium | Tuples in a set |
| 10 | [Sum, Mean and Max](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/tuples-sets/sum-mean-and-max) | Easy | Returning several values |
| 11 | [Count Unique Values](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/tuples-sets/count-unique-values) | Easy | set() |
| 12 | [Common Letters](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/tuples-sets/common-letters) | Easy | Intersection |
| 13 | [Union of Two Lists](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/tuples-sets/union-of-two-lists) | Easy | Union |
| 14 | [In First List Only](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/tuples-sets/in-first-list-only) | Easy | Difference |
| 15 | [In Exactly One List](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/tuples-sets/in-exactly-one-list) | Medium | Symmetric difference |
| 16 | [Has Duplicates?](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/tuples-sets/has-duplicates) | Easy | set size |
| 17 | [Is It a Subset?](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/tuples-sets/is-it-a-subset) | Easy | Subset test |
| 18 | [Missing Numbers](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/tuples-sets/missing-numbers) | Medium | Difference with a range |
| 19 | [Unique Words, Ignoring Case](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/tuples-sets/unique-words-ignoring-case) | Easy | Set comprehension |
| 20 | [Two Numbers Add Up](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/tuples-sets/two-numbers-add-up) | Medium | Set of seen values |

## Dictionaries

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Word Frequency](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/dictionaries/word-frequency) | Easy | Counting with a dict |
| 2 | [Character Frequency](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/dictionaries/character-frequency) | Easy | Counter |
| 3 | [Invert a Dictionary](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/dictionaries/invert-a-dictionary) | Easy | Dict comprehension |
| 4 | [Merge Dicts, Adding Values](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/dictionaries/merge-dicts-adding-values) | Medium | Merging |
| 5 | [Safe Lookup](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/dictionaries/safe-lookup) | Easy | get() with a default |
| 6 | [Group Words by First Letter](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/dictionaries/group-words-by-first-letter) | Medium | setdefault / defaultdict |
| 7 | [Group Anagrams](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/dictionaries/group-anagrams) | Medium | Tuple / sorted keys |
| 8 | [Most Common Word](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/dictionaries/most-common-word) | Easy | max with key |
| 9 | [Pass or Fail Report](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/dictionaries/pass-or-fail-report) | Easy | Dict comprehension |
| 10 | [Sort by Value](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/dictionaries/sort-by-value) | Medium | sorted on items() |
| 11 | [Election Winner](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/dictionaries/election-winner) | Easy | Counting votes |
| 12 | [Read a Nested Setting](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/dictionaries/read-a-nested-setting) | Medium | Nested dicts |
| 13 | [Two Lists to a Dict](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/dictionaries/two-lists-to-a-dict) | Easy | dict(zip()) |
| 14 | [Filter by Value](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/dictionaries/filter-by-value) | Easy | Comprehension with a condition |
| 15 | [Key With the Largest Value](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/dictionaries/key-with-the-largest-value) | Easy | max(d, key=d.get) |
| 16 | [Total of All Values](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/dictionaries/total-of-all-values) | Easy | values() |
| 17 | [Roman to Integer](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/dictionaries/roman-to-integer) | Medium | Lookup table |
| 18 | [First Repeated Word](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/dictionaries/first-repeated-word) | Easy | Seen set / dict |
| 19 | [Total per Category](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/dictionaries/total-per-category) | Easy | Summing into a dict |
| 20 | [Word Pattern](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/dictionaries/word-pattern) | Medium | Two-way mapping |

## Functions & Recursion

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Greeting With a Default](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/functions/greeting-with-a-default) | Easy | Default parameters |
| 2 | [Circle Area (return, don't print)](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/functions/circle-area-return-dont-print) | Easy | return values |
| 3 | [Sum Any Number of Values](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/functions/sum-any-number-of-values) | Easy | *args |
| 4 | [Keyword Arguments to Text](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/functions/keyword-arguments-to-text) | Medium | **kwargs |
| 5 | [Factorial with Recursion](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/functions/factorial-with-recursion) | Easy | Recursion · base case |
| 6 | [n-th Fibonacci Number](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/functions/n-th-fibonacci-number) | Medium | Memoisation |
| 7 | [Fast Power](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/functions/fast-power) | Medium | Divide and conquer |
| 8 | [Sum of Digits, Recursively](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/functions/sum-of-digits-recursively) | Easy | Recursion on numbers |
| 9 | [Reverse a String, Recursively](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/functions/reverse-a-string-recursively) | Easy | Recursion on strings |
| 10 | [Palindrome, Recursively](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/functions/palindrome-recursively) | Easy | Two base cases |
| 11 | [Countdown List, Recursively](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/functions/countdown-list-recursively) | Easy | Building a list recursively |
| 12 | [Apply an Operation by Name](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/functions/apply-an-operation-by-name) | Medium | Functions as values |
| 13 | [Scale With a Closure](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/functions/scale-with-a-closure) | Medium | Closures |
| 14 | [Validate an Order](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/functions/validate-an-order) | Medium | Guard clauses |
| 15 | [Sort by Last Letter](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/functions/sort-by-last-letter) | Easy | lambda as a key |
| 16 | [GCD, Recursively](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/functions/gcd-recursively) | Easy | Euclid's algorithm |
| 17 | [Binary String, Recursively](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/functions/binary-string-recursively) | Medium | Recursion on n // 2 |
| 18 | [Flatten Any Depth](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/functions/flatten-any-depth) | Hard | Recursion on nested lists |
| 19 | [Tower of Hanoi Moves](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/functions/tower-of-hanoi-moves) | Medium | Recursion vs formula |
| 20 | [Climbing Stairs](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/functions/climbing-stairs) | Medium | Recursion + memo |

## Comprehensions, Iterators & Generators

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Squares](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/comprehensions/squares) | Easy | List comprehension |
| 2 | [Keep the Even Numbers](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/comprehensions/keep-the-even-numbers) | Easy | Filtering |
| 3 | [Word Lengths](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/comprehensions/word-lengths) | Easy | Dict comprehension |
| 4 | [Distinct Word Lengths](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/comprehensions/distinct-word-lengths) | Easy | Set comprehension |
| 5 | [Multiplication Grid](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/comprehensions/multiplication-grid) | Medium | Nested comprehension |
| 6 | [Label Even and Odd](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/comprehensions/label-even-and-odd) | Easy | if/else inside a comprehension |
| 7 | [Parse and Keep Positives](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/comprehensions/parse-and-keep-positives) | Medium | map and filter |
| 8 | [Pairwise Sums](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/comprehensions/pairwise-sums) | Easy | zip |
| 9 | [All Positions of a Value](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/comprehensions/all-positions-of-a-value) | Easy | enumerate |
| 10 | [All Positive?](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/comprehensions/all-positive) | Easy | all() and any() |
| 11 | [Sort People by Age, Then Name](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/comprehensions/sort-people-by-age-then-name) | Medium | Tuple keys |
| 12 | [First n Squares (Generator)](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/comprehensions/first-n-squares-generator) | Easy | yield |
| 13 | [Take From an Endless Stream](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/comprehensions/take-from-an-endless-stream) | Medium | Infinite generator · islice |
| 14 | [Running Average](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/comprehensions/running-average) | Medium | Generator with state |
| 15 | [Batches (Generator)](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/comprehensions/batches-generator) | Medium | yield slices |
| 16 | [Fibonacci Up To a Limit](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/comprehensions/fibonacci-up-to-a-limit) | Medium | Generator |
| 17 | [Sum of Squares Without a List](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/comprehensions/sum-of-squares-without-a-list) | Easy | Generator expression |
| 18 | [Countdown Iterator](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/comprehensions/countdown-iterator) | Medium | Iterator protocol vs generator |
| 19 | [Chain Several Lists](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/comprehensions/chain-several-lists) | Easy | itertools.chain |
| 20 | [Adjacent Differences](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/comprehensions/adjacent-differences) | Easy | zip with a shifted copy |

## Object-Oriented Programming

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Rectangle Class](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/oop/rectangle-class) | Easy | Attributes and methods |
| 2 | [Bank Account](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/oop/bank-account) | Easy | Methods that change state |
| 3 | [Click Counter](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/oop/click-counter) | Easy | Instance state |
| 4 | [Student Average](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/oop/student-average) | Easy | Lists inside objects |
| 5 | [Temperature With a Property](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/oop/temperature-with-a-property) | Medium | @property |
| 6 | [Simple Stack Class](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/oop/simple-stack-class) | Easy | Wrapping a list |
| 7 | [Simple Queue Class](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/oop/simple-queue-class) | Medium | deque inside a class |
| 8 | [Shopping Cart](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/oop/shopping-cart) | Medium | Objects holding dicts |
| 9 | [Library Loans](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/oop/library-loans) | Medium | Sets inside objects |
| 10 | [Protected Age](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/oop/protected-age) | Medium | Encapsulation and validation |
| 11 | [Playlist With len and in](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/oop/playlist-with-len-and-in) | Medium | Special methods |
| 12 | [Add Two Points](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/oop/add-two-points) | Medium | Operator overloading |
| 13 | [Readable Object Text](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/oop/readable-object-text) | Easy | __str__ / __repr__ |
| 14 | [Total Area of Shapes](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/oop/total-area-of-shapes) | Medium | Inheritance and polymorphism |
| 15 | [Animal Sounds](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/oop/animal-sounds) | Easy | Method overriding |
| 16 | [Count Instances](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/oop/count-instances) | Medium | Class attributes |
| 17 | [Sort Employees by Salary](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/oop/sort-employees-by-salary) | Medium | __lt__ for sorting |
| 18 | [Date From Text](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/oop/date-from-text) | Medium | @classmethod constructors |
| 19 | [Car With an Engine](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/oop/car-with-an-engine) | Medium | Composition |
| 20 | [Equal Records](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/oop/equal-records) | Easy | @dataclass equality |

## Errors, Exceptions & Files

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Safe Division](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/exceptions/safe-division) | Easy | ZeroDivisionError |
| 2 | [Parse a Number or Use a Default](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/exceptions/parse-a-number-or-use-a-default) | Easy | ValueError |
| 3 | [Safe List Access](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/exceptions/safe-list-access) | Easy | IndexError |
| 4 | [Safe Dictionary Lookup](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/exceptions/safe-dictionary-lookup) | Easy | KeyError |
| 5 | [Sum the Valid Numbers](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/exceptions/sum-the-valid-numbers) | Medium | Skipping bad input |
| 6 | [Validate an Age](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/exceptions/validate-an-age) | Medium | raise and except |
| 7 | [Custom Exception: Insufficient Funds](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/exceptions/custom-exception-insufficient-funds) | Medium | Defining exceptions |
| 8 | [Clean-up With finally](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/exceptions/clean-up-with-finally) | Medium | finally |
| 9 | [Success Message With else](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/exceptions/success-message-with-else) | Easy | try / except / else |
| 10 | [First Valid Attempt](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/exceptions/first-valid-attempt) | Medium | Retry loop |
| 11 | [Several Kinds of Error](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/exceptions/several-kinds-of-error) | Medium | Multiple except blocks |
| 12 | [Square Root of a Negative](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/exceptions/square-root-of-a-negative) | Easy | Raising errors |
| 13 | [Count Lines in a File](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/exceptions/count-lines-in-a-file) | Easy | Iterating a file |
| 14 | [Words in a File](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/exceptions/words-in-a-file) | Easy | Reading text |
| 15 | [Totals From CSV](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/exceptions/totals-from-csv) | Medium | csv module |
| 16 | [Write Lines, Read Them Back](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/exceptions/write-lines-read-them-back) | Easy | Writing files |
| 17 | [Longest Line](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/exceptions/longest-line) | Easy | max over a file |
| 18 | [Make Your Own Context Manager](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/exceptions/make-your-own-context-manager) | Hard | __enter__ / __exit__ |
| 19 | [Read key=value Settings](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/exceptions/read-key-value-settings) | Medium | Unpacking errors |
| 20 | [Parse JSON Safely](https://abpandey-dev.github.io/python-dsa-visualizer/python-course/#/q/exceptions/parse-json-safely) | Medium | json + JSONDecodeError |

## Build

```bash
python3 handbook/build.py --book python-course
```

Sources live in `python-course/src/`: `topics/` (questions and solutions), `lessons/` and `theory/`.
