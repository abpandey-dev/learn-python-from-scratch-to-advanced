from lib import *

TOPIC(
    id="strings", title="Strings", glyph='"abc"',
    blurb="Text in Python: indexing, slicing, string methods, formatting and why strings can't be changed in place.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">s = "Python"
s[0], s[-1]          # 'P', 'n'
s[1:4], s[::-1]      # 'yth', 'nohtyP'
len(s)               # 6
s.lower(), s.upper(), s.title(), s.strip()
s.replace("P", "J"), s.find("th"), s.count("o")
s.split(","), ",".join(parts)
s.startswith("Py"), s.isdigit(), s.isalpha()
f"{name:&gt;10}"       # formatting</code></pre>
<ul>
<li>Strings are <b>immutable</b>: methods return a <b>new</b> string.</li>
<li>Slices never raise IndexError; indexing does.</li>
<li>Build long strings with a list and <code>"".join()</code>, not <code>+=</code> in a loop.</li>
</ul>
""")


Q(None, "Reverse a String", "Easy", "Slicing",
  "Return the string reversed.",
  [(("hello",), "olleh"), (("a",), "a"), (("",), "")],
  ("Build a new string by adding characters from the end to the start.", "O(n²) — each + copies", "O(n)"),
  ("Slice with step −1: <code>s[::-1]</code>.", "O(n)", "O(n)"),
  viz=("code",))


@B
def reverse_string(s):
    result = ""
    for i in range(len(s) - 1, -1, -1):
        result = result + s[i]
    return result


@O
def reverse_string(s):
    return s[::-1]


Q(None, "Palindrome Word", "Easy", "Comparison · lower()",
  "Return True if the word reads the same backwards (ignore letter case).",
  [(("Level",), True), (("hello",), False), (("A",), True)],
  ("Compare characters from both ends moving inward.", "O(n)", "O(1)"),
  ("Lower-case it and compare with its reverse.", "O(n)", "O(n)"),
  viz=("Racecar",))


@B
def is_palindrome(word):
    word = word.lower()
    i, j = 0, len(word) - 1
    while i < j:
        if word[i] != word[j]:
            return False
        i += 1
        j -= 1
    return True


@O
def is_palindrome(word):
    w = word.lower()
    return w == w[::-1]


Q(None, "Count a Character", "Easy", "count()",
  "Return how many times character <code>ch</code> appears in <code>s</code>.",
  [(("banana", "a"), 3), (("hello", "z"), 0), (("aaa", "a"), 3)],
  ("Loop and compare each character.", "O(n)", "O(1)"),
  ("<code>s.count(ch)</code>.", "O(n)", "O(1)"))


@B
def count_char(s, ch):
    count = 0
    for c in s:
        if c == ch:
            count += 1
    return count


@O
def count_char(s, ch):
    return s.count(ch)


Q(None, "Capitalise Each Word", "Easy", "split · join · capitalize",
  "Return the sentence with the first letter of every word in upper case and the rest lower case. Words are separated by single spaces.",
  [(("hello world",), "Hello World"), (("pYTHON is FUN",), "Python Is Fun")],
  ("Walk the characters, upper-casing the one after a space.", "O(n)", "O(n)"),
  ("Split into words, capitalise each, join with spaces.", "O(n)", "O(n)"),
  viz=("hi there",))


@B
def capitalise_words(sentence):
    result = ""
    new_word = True
    for ch in sentence:
        if ch == " ":
            result += ch
            new_word = True
        elif new_word:
            result += ch.upper()
            new_word = False
        else:
            result += ch.lower()
    return result


@O
def capitalise_words(sentence):
    return " ".join(word.capitalize() for word in sentence.split(" "))


Q(None, "Count Words", "Easy", "split()",
  "Return the number of words in the text (words are separated by any amount of whitespace).",
  [(("The quick  brown fox",), 4), (("   ",), 0), (("one",), 1)],
  ("Walk the characters and count every place where a word starts.", "O(n)", "O(1)"),
  ("<code>split()</code> with no argument splits on runs of whitespace and ignores the ends.", "O(n)", "O(n)"),
  viz=("hi  you all",))


@B
def count_words(text):
    count = 0
    in_word = False
    for ch in text:
        if ch.isspace():
            in_word = False
        elif not in_word:
            count += 1
            in_word = True
    return count


@O
def count_words(text):
    return len(text.split())


Q(None, "Remove Vowels", "Easy", "Building strings",
  "Return the text with all vowels (a, e, i, o, u in either case) removed.",
  [(("Hello World",), "Hll Wrld"), (("aeiou",), ""), (("xyz",), "xyz")],
  ("Add each non-vowel to a result string with +=.", "O(n²) worst", "O(n)"),
  ("Join the kept characters from a generator — one allocation.", "O(n)", "O(n)"),
  viz=("Education",))


@B
def remove_vowels(text):
    result = ""
    for ch in text:
        if ch.lower() not in "aeiou":
            result += ch
    return result


@O
def remove_vowels(text):
    return "".join(ch for ch in text if ch.lower() not in "aeiou")


Q(None, "Anagram Check", "Medium", "sorted · Counter",
  "Return True if two words use exactly the same letters (ignore case).",
  [(("Listen", "Silent"), True), (("abc", "abd"), False), (("aab", "abb"), False)],
  ("For each letter of the first word, find and remove it from a list of the second word's letters.", "O(n²)", "O(n)"),
  ("Compare the sorted letters (or <code>Counter</code>s).", "O(n log n)", "O(n)"),
  viz=("Note", "Tone"))


@B
def is_anagram(a, b):
    letters = list(b.lower())
    for ch in a.lower():
        if ch in letters:
            letters.remove(ch)
        else:
            return False
    return len(letters) == 0


@O
def is_anagram(a, b):
    return sorted(a.lower()) == sorted(b.lower())


Q(None, "Title Initials", "Easy", "split · indexing",
  "Return the initials of a full name in upper case, e.g. 'ada king lovelace' → 'AKL'.",
  [(("ada king lovelace",), "AKL"), (("Grace Hopper",), "GH")],
  ("Walk characters, taking the first one and every character after a space.", "O(n)", "O(k)"),
  ("Split into words and join their first letters.", "O(n)", "O(k)"))


@B
def initials(name):
    result = name[0].upper()
    for i in range(1, len(name)):
        if name[i - 1] == " ":
            result += name[i].upper()
    return result


@O
def initials(name):
    return "".join(word[0].upper() for word in name.split())


Q(None, "Replace Spaces", "Easy", "replace()",
  "Replace every space in <code>text</code> with <code>'_'</code>.",
  [(("snake case me",), "snake_case_me"), (("nospace",), "nospace")],
  ("Build a new string character by character.", "O(n)", "O(n)"),
  ("<code>text.replace(' ', '_')</code>.", "O(n)", "O(n)"))


@B
def underscores(text):
    out = []
    for ch in text:
        out.append("_" if ch == " " else ch)
    return "".join(out)


@O
def underscores(text):
    return text.replace(" ", "_")


Q(None, "Most Frequent Character", "Medium", "Counting",
  "Return the character that appears most often in <code>s</code> (ties → the one that appears first).",
  [(("banana",), "a"), (("abcab",), "a"), (("zzyy",), "z")],
  ("For each character, count it with a loop over the whole string.", "O(n²)", "O(1)"),
  ("Count once with a dict, then pick the max by count; dicts keep insertion order so ties favour the earliest.", "O(n)", "O(k)"),
  viz=("banana",))


@B
def most_frequent(s):
    best, best_count = "", 0
    for ch in s:
        c = 0
        for other in s:
            if other == ch:
                c += 1
        if c > best_count:
            best, best_count = ch, c
    return best


@O
def most_frequent(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    return max(counts, key=counts.get)


Q(None, "Compress Repeated Letters", "Medium", "Run-length encoding",
  "Compress runs of the same letter: 'aaabccdddd' → 'a3b1c2d4'.",
  [(("aaabccdddd",), "a3b1c2d4"), (("abc",), "a1b1c1"), (("",), "")],
  ("Walk with an index and an inner while loop that measures each run.", "O(n)", "O(n)"),
  ("<code>itertools.groupby</code> groups consecutive equal letters for you.", "O(n)", "O(n)"),
  viz=("aaabcc",))


@B
def compress(s):
    out = ""
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        out += s[i] + str(j - i)
        i = j
    return out


@O
def compress(s):
    from itertools import groupby
    return "".join(f"{ch}{len(list(run))}" for ch, run in groupby(s))


Q(None, "Is It a Pangram?", "Medium", "Sets of characters",
  "Return True if the sentence contains every letter a–z at least once.",
  [(("The quick brown fox jumps over the lazy dog",), True), (("Hello world",), False)],
  ("For each of the 26 letters, check whether it's in the sentence.", "O(26 · n)", "O(1)"),
  ("Turn the lower-cased sentence into a set and check the alphabet is a subset of it.", "O(n)", "O(1)"))


@B
def is_pangram(sentence):
    s = sentence.lower()
    for code in range(ord("a"), ord("z") + 1):
        if chr(code) not in s:
            return False
    return True


@O
def is_pangram(sentence):
    import string
    return set(string.ascii_lowercase) <= set(sentence.lower())


Q(None, "Swap Case", "Easy", "Character methods",
  "Return the text with upper-case letters made lower-case and vice versa.",
  [(("Hello World",), "hELLO wORLD"), (("123abc",), "123ABC")],
  ("Check each character and convert it.", "O(n)", "O(n)"),
  ("<code>str.swapcase()</code>.", "O(n)", "O(n)"),
  viz=("PyThOn",))


@B
def swap_case(text):
    out = ""
    for ch in text:
        if ch.isupper():
            out += ch.lower()
        elif ch.islower():
            out += ch.upper()
        else:
            out += ch
    return out


@O
def swap_case(text):
    return text.swapcase()


Q(None, "Longest Word", "Easy", "max with key",
  "Return the longest word in a sentence (the first one if there's a tie).",
  [(("I love programming in Python",), "programming"), (("a bb cc",), "bb")],
  ("Track the longest word while looping over the split words.", "O(n)", "O(n)"),
  ("<code>max(words, key=len)</code> returns the first longest.", "O(n)", "O(n)"))


@B
def longest_word(sentence):
    best = ""
    for word in sentence.split():
        if len(word) > len(best):
            best = word
    return best


@O
def longest_word(sentence):
    return max(sentence.split(), key=len)


Q(None, "Mask a Card Number", "Easy", "Slicing · repetition",
  "Replace every character except the last 4 with '#'.",
  [(("4556364607935616",), "############5616"), (("1234",), "1234"), (("12",), "12")],
  ("Loop with an index and decide character by character.", "O(n)", "O(n)"),
  ("Repeat '#' for the hidden length and add the last 4 with a slice.", "O(n)", "O(n)"))


@B
def mask(card):
    out = ""
    for i in range(len(card)):
        if i < len(card) - 4:
            out += "#"
        else:
            out += card[i]
    return out


@O
def mask(card):
    return "#" * max(len(card) - 4, 0) + card[-4:]


Q(None, "Caesar Cipher", "Medium", "ord · chr · %",
  "Shift every lowercase letter forward by <code>k</code> places in the alphabet (wrapping z → a). Leave other characters as they are.",
  [(("abc xyz", 3), "def abc"), (("hello", 13), "uryyb"), (("a-b", 1), "b-c")],
  ("Look up each letter's position in the alphabet string with <code>index</code>.", "O(26 · n)", "O(n)"),
  ("Use character codes: <code>chr((ord(c) − 97 + k) % 26 + 97)</code>.", "O(n)", "O(n)"),
  viz=("xyz", 3))


@B
def caesar(text, k):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    out = ""
    for ch in text:
        if ch in alphabet:
            pos = alphabet.index(ch)
            out += alphabet[(pos + k) % 26]
        else:
            out += ch
    return out


@O
def caesar(text, k):
    return "".join(chr((ord(c) - 97 + k) % 26 + 97) if "a" <= c <= "z" else c for c in text)


Q(None, "Only Digits", "Easy", "Filtering characters",
  "Return just the digits from a string, e.g. '+91 98-765' → '9198765'.",
  [(("+91 98-765",), "9198765"), (("abc",), ""), (("2024",), "2024")],
  ("Compare each character with '0'…'9'.", "O(n)", "O(n)"),
  ("Join the characters for which <code>isdigit()</code> is True.", "O(n)", "O(n)"))


@B
def only_digits(s):
    out = ""
    for ch in s:
        if ch >= "0" and ch <= "9":
            out += ch
    return out


@O
def only_digits(s):
    return "".join(ch for ch in s if ch.isdigit())


Q(None, "First Non-Repeating Character", "Medium", "Counting · order",
  "Return the first character that appears exactly once, or '' if none.",
  [(("swiss",), "w"), (("aabb",), ""), (("python",), "p")],
  ("For each character, count it by scanning the whole string.", "O(n²)", "O(1)"),
  ("Count all characters once with a dict, then scan again for the first count of 1.", "O(n)", "O(k)"),
  viz=("swiss",))


@B
def first_unique(s):
    for ch in s:
        if s.count(ch) == 1:
            return ch
    return ""


@O
def first_unique(s):
    from collections import Counter
    counts = Counter(s)
    return next((ch for ch in s if counts[ch] == 1), "")


Q(None, "Centre a Title", "Easy", "Format specifiers",
  "Return <code>title</code> centred in a field of <code>width</code> characters, padded with '*'. Extra padding goes on the right.",
  [(("Hi", 6), "**Hi**"), (("Py", 5), "*Py**"), (("Long", 2), "Long")],
  ("Work out left and right padding with arithmetic and build the string.", "O(width)", "O(width)"),
  ("<code>title.center(width, '*')</code> (or f-string <code>:*^{width}</code>).", "O(width)", "O(width)"))


@B
def centre(title, width):
    total = max(width - len(title), 0)
    left = total // 2
    right = total - left
    return "*" * left + title + "*" * right


@O
def centre(title, width):
    return f"{title:*^{width}}"


Q(None, "Valid Username", "Medium", "Several checks",
  "A valid username is 3–12 characters, starts with a letter, and contains only letters, digits or '_'. Return True or False.",
  [(("ada_99",), True), (("9lives",), False), (("ab",), False), (("hello world",), False)],
  ("Check length, then the first character, then loop over the rest with explicit comparisons.", "O(n)", "O(1)"),
  ("Combine <code>isalpha</code>, a length range check and <code>all()</code> over the characters.", "O(n)", "O(1)"))


@B
def valid_username(name):
    if len(name) < 3 or len(name) > 12:
        return False
    first = name[0]
    if not (("a" <= first <= "z") or ("A" <= first <= "Z")):
        return False
    for ch in name:
        ok = ("a" <= ch <= "z") or ("A" <= ch <= "Z") or ("0" <= ch <= "9") or ch == "_"
        if not ok:
            return False
    return True


@O
def valid_username(name):
    return 3 <= len(name) <= 12 and name[0].isalpha() and all(c.isalnum() or c == "_" for c in name)
