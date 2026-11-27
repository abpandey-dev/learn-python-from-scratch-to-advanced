from lib import *
import fnmatch
import hashlib
import re
from collections import Counter, defaultdict, deque

TOPIC(
    id="git", title="Git: From Commits to Pull Requests", glyph="⎇",
    blurb="What Git really stores and how it decides things: content hashes, the commit graph, merge bases, fast-forwards, ahead/behind, diffs, three-way merges, .gitignore rules, conventional commits and version bumps, bisect, rebase and cherry-pick, stash, blame, branch protection, secret scanning and shortlog.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">git switch -c feature/login        # new branch
git add -p                         # stage chosen hunks
git commit -m "feat(auth): add login rate limit"
git fetch &amp;&amp; git rebase origin/main  # replay your commits on the latest main
git push -u origin feature/login   # then open a pull request
git log --oneline --graph --all    # see the commit graph
git bisect start; git bisect bad; git bisect good v1.2   # binary-search a regression</code></pre>
<p>A commit is a snapshot plus pointers to its parents. A branch is just a movable name for a commit.</p>
""")


Q(None, "Hash a File the Way Git Does", "Easy", "Content addressing",
  "Git names every file version by the SHA-1 of <code>b'blob ' + size + b'\\0' + content</code>. Return the first 12 hex characters for each text (UTF-8). Same content → same id, wherever it lives.",
  [((["hello\n", "", "print('hi')\n", "hello\n"],), ['ce013625030b', 'e69de29bb2d1', '9f1b437537a2', 'ce013625030b'])],
  ("Build the header as a string, then hash.", "O(total size)", "O(size)"),
  ("Hash bytes directly with an f-string header.", "O(total size)", "O(size)"),
  viz=((["hello\n"],)))


@B
def blob_ids(texts):
    out = []
    for t in texts:
        data = t.encode("utf-8")
        header = "blob " + str(len(data)) + "\0"
        out.append(hashlib.sha1(header.encode() + data).hexdigest()[:12])
    return out


@O
def blob_ids(texts):
    return [hashlib.sha1(b"blob %d\0" % len(d) + d).hexdigest()[:12] for d in (t.encode() for t in texts)]


Q(None, "Walk the First-Parent History", "Easy", "git log --first-parent",
  "<code>parents</code> maps each commit to its parent list (merge commits have two). Starting at <code>head</code>, follow the <b>first</b> parent until the root and return the commits in that order.",
  [(({"m3": ["m2", "f2"], "m2": ["m1"], "f2": ["f1"], "f1": ["m1"], "m1": ["root"], "root": []}, "m3"), ['m3', 'm2', 'm1', 'root'])],
  ("A while loop with a list.", "O(h)", "O(h)"),
  ("Same loop, using <code>dict.get</code>.", "O(h)", "O(h)"),
  viz=(({"b": ["a"], "a": []}, "b")))


@B
def first_parent_log(parents, head):
    out, c = [], head
    while True:
        out.append(c)
        if len(parents[c]) == 0:
            return out
        c = parents[c][0]


@O
def first_parent_log(parents, head):
    out = [head]
    while parents.get(out[-1]):
        out.append(parents[out[-1]][0])
    return out


def ancestors(parents, c):
    seen, stack = set(), [c]
    while stack:
        x = stack.pop()
        if x not in seen:
            seen.add(x)
            stack.extend(parents[x])
    return seen


Q(None, "Find the Merge Base", "Medium", "Where two branches split",
  "Return the best common ancestors of commits <code>a</code> and <code>b</code> (sorted): common ancestors that are not themselves ancestors of another common ancestor. This is the base a three-way merge compares against.",
  [(({"m3": ["m2"], "m2": ["m1"], "f2": ["f1"], "f1": ["m1"], "m1": ["root"], "root": []}, "m3", "f2"), ['m1']),
   (({"x": ["p", "q"], "y": ["q", "p"], "p": ["r"], "q": ["r"], "r": []}, "x", "y"), ['p', 'q'])],
  ("Ancestor sets by DFS; check every pair of common ancestors.", "O(n²)", "O(n)"),
  ("Remove the strict ancestors of every common ancestor in one sweep.", "O(n · k)", "O(n)"),
  viz=(({"b": ["a"], "c": ["a"], "a": []}, "b", "c")))


@B
def merge_base(parents, a, b):
    common = ancestors(parents, a) & ancestors(parents, b)
    best = []
    for c in common:
        dominated = False
        for d in common:
            if d != c and c in ancestors(parents, d):
                dominated = True
        if not dominated:
            best.append(c)
    return sorted(best)


@O
def merge_base(parents, a, b):
    common = ancestors(parents, a) & ancestors(parents, b)
    below = set()
    for c in common:
        below |= ancestors(parents, c) - {c}
    return sorted(common - below)


Q(None, "Can It Fast-Forward?", "Easy", "Moving a branch pointer",
  "Merging <code>src</code> into <code>dst</code> can fast-forward (just move the pointer, no merge commit) exactly when <code>dst</code> is an ancestor of <code>src</code>. Return a bool for each <code>(dst, src)</code> pair.",
  [(({"c4": ["c3"], "c3": ["c2"], "c2": ["c1"], "f1": ["c2"], "c1": []}, [("c2", "c4"), ("c4", "c2"), ("c3", "f1"), ("c1", "f1"), ("c4", "c4")]), [True, False, False, True, True])],
  ("Compute the ancestor set each time.", "O(p · n)", "O(n)"),
  ("Same, reusing the helper.", "O(p · n)", "O(n)"),
  viz=(({"b": ["a"], "a": []}, [("a", "b")])))


@B
def can_fast_forward(parents, pairs):
    out = []
    for dst, src in pairs:
        seen, stack = set(), [src]
        while stack:
            x = stack.pop()
            if x not in seen:
                seen.add(x)
                stack += parents[x]
        out.append(dst in seen)
    return out


@O
def can_fast_forward(parents, pairs):
    return [dst in ancestors(parents, src) for dst, src in pairs]


Q(None, "Ahead and Behind", "Easy", "What git status tells you",
  "Return <code>(ahead, behind)</code>: commits reachable from <code>local</code> but not <code>remote</code>, and the reverse.",
  [(({"l2": ["l1"], "l1": ["b"], "r3": ["r2"], "r2": ["r1"], "r1": ["b"], "b": ["a"], "a": []}, "l2", "r3"), (2, 3))],
  ("Two ancestor walks, then loops.", "O(n)", "O(n)"),
  ("Set differences.", "O(n)", "O(n)"),
  viz=(({"x": ["a"], "a": []}, "x", "a")))


@B
def ahead_behind(parents, local, remote):
    mine, theirs = ancestors(parents, local), ancestors(parents, remote)
    ahead = 0
    for c in mine:
        if c not in theirs:
            ahead += 1
    behind = 0
    for c in theirs:
        if c not in mine:
            behind += 1
    return (ahead, behind)


@O
def ahead_behind(parents, local, remote):
    mine, theirs = ancestors(parents, local), ancestors(parents, remote)
    return (len(mine - theirs), len(theirs - mine))


Q(None, "Count Added and Removed Lines", "Medium", "git diff --stat",
  "Diffs are built on the longest common subsequence (LCS) of lines. Return <code>(added, removed)</code>: lines of <code>new</code> not in the LCS, and lines of <code>old</code> not in it.",
  [((["import os", "def main():", "    print('hi')", "    return 0", "main()"], ["import os", "import sys", "def main():", "    print('hello')", "    return 0", "if __name__ == '__main__':", "    main()"]), (4, 2))],
  ("A full (n+1)×(m+1) LCS table.", "O(n · m)", "O(n · m)"),
  ("The same DP keeping only two rows.", "O(n · m)", "O(m)"),
  viz=((["a", "b"], ["a", "c"])))


@B
def diff_stat(old, new):
    n, m = len(old), len(new)
    t = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            t[i + 1][j + 1] = t[i][j] + 1 if old[i] == new[j] else max(t[i][j + 1], t[i + 1][j])
    lcs = t[n][m]
    return (m - lcs, n - lcs)


@O
def diff_stat(old, new):
    prev = [0] * (len(new) + 1)
    for a in old:
        cur = [0]
        for j, b in enumerate(new):
            cur.append(prev[j] + 1 if a == b else max(prev[j + 1], cur[j]))
        prev = cur
    return (len(new) - prev[-1], len(old) - prev[-1])


Q(None, "A Three-Way Merge", "Medium", "Base, ours, theirs",
  "Merge line by line (the three versions have the same number of lines here): if only one side changed a line from <code>base</code>, take that side; if both made the same change, take it; if both changed it differently, emit conflict markers <code>'<<<<<<< ours'</code>, our line, <code>'======='</code>, their line, <code>'>>>>>>> theirs'</code>. Return <code>(merged lines, conflicts)</code>.",
  [((["a = 1", "b = 2", "c = 3", "d = 4"], ["a = 1", "b = 20", "c = 3", "d = 40"], ["a = 10", "b = 2", "c = 3", "d = 400"]), (['a = 10', 'b = 20', 'c = 3', '<<<<<<< ours', 'd = 40', '=======', 'd = 400', '>>>>>>> theirs'], 1))],
  ("If/elif per line.", "O(n)", "O(n)"),
  ("Same rules in fewer branches.", "O(n)", "O(n)"),
  viz=((["x"], ["y"], ["x"])))


@B
def three_way(base, ours, theirs):
    out, conflicts = [], 0
    for b, o, t in zip(base, ours, theirs):
        if o == t:
            out.append(o)
        elif o == b:
            out.append(t)
        elif t == b:
            out.append(o)
        else:
            out += ["<<<<<<< ours", o, "=======", t, ">>>>>>> theirs"]
            conflicts += 1
    return (out, conflicts)


@O
def three_way(base, ours, theirs):
    out, conflicts = [], 0
    for b, o, t in zip(base, ours, theirs):
        if o == t or t == b:
            out.append(o)
        elif o == b:
            out.append(t)
        else:
            out += ["<<<<<<< ours", o, "=======", t, ">>>>>>> theirs"]
            conflicts += 1
    return (out, conflicts)


def ignore_match(pattern, path):
    if pattern.endswith("/"):
        return pattern[:-1] in path.split("/")[:-1]
    if "/" in pattern.strip("/"):
        pp, parts = pattern.lstrip("/").split("/"), path.split("/")
        return len(pp) == len(parts) and all(fnmatch.fnmatch(a, b) for a, b in zip(parts, pp))
    return any(fnmatch.fnmatch(part, pattern) for part in path.split("/"))


Q(None, "Apply .gitignore Rules", "Medium", "The last matching rule wins",
  "For each path, the last pattern that matches decides: a plain pattern ignores, a <code>!</code> pattern un-ignores. Patterns ending in <code>/</code> match directories; patterns containing <code>/</code> match the full path segment by segment (so <code>*</code> never crosses a <code>/</code>); others match any path part (use <code>ignore_match</code>). Return the ignored paths.",
  [((["*.pyc", "build/", ".env", "!.env.example", "*.env*", "!config/.env.example", "docs/*.html"], ["app/main.py", "app/__pycache__/main.cpython-312.pyc", "build/lib/app.py", ".env", ".env.example", "config/.env.example", "docs/index.html", "docs/api/index.html", "README.md"]), ['app/__pycache__/main.cpython-312.pyc', 'build/lib/app.py', '.env', '.env.example', 'docs/index.html'])],
  ("Check every pattern and remember the last match.", "O(p · n)", "O(n)"),
  ("Scan patterns backwards and stop at the first match.", "O(p · n)", "O(n)"),
  viz=((["*.log", "!keep.log"], ["a.log", "keep.log"])))


@B
def ignored(patterns, paths):
    out = []
    for path in paths:
        state = False
        for p in patterns:
            neg = p.startswith("!")
            if ignore_match(p[1:] if neg else p, path):
                state = not neg
        if state:
            out.append(path)
    return out


@O
def ignored(patterns, paths):
    def decide(path):
        for p in reversed(patterns):
            neg = p.startswith("!")
            if ignore_match(p.lstrip("!"), path):
                return not neg
        return False
    return [p for p in paths if decide(p)]


CC = re.compile(r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z0-9-]+\))?(!)?: \S.*$")


Q(None, "Validate Conventional Commits", "Easy", "Machine-readable messages",
  "A conventional commit subject looks like <code>type(scope)!: description</code> — type from a fixed list, optional lower-case scope, optional <code>!</code> for breaking, then <code>': '</code> and a description. Return a bool per message (use the regex <code>CC</code>).",
  [((["feat(auth): add login rate limit", "fix: handle empty cart", "Fixed stuff", "feat!: drop Python 3.9", "docs(README): typo", "chore(deps):bump numpy", "refactor(api-client)!: rename methods"],), [True, True, False, True, False, False, True])],
  ("Split by hand and check each part.", "O(n · L)", "O(1)"),
  ("One regular expression.", "O(n · L)", "O(1)"),
  viz=((["fix: x", "oops"],)))


@B
def valid_commits(messages):
    types = ["feat", "fix", "docs", "style", "refactor", "perf", "test", "build", "ci", "chore", "revert"]
    out = []
    for m in messages:
        head, sep, desc = m.partition(": ")
        ok = sep == ": " and len(desc) > 0 and not desc[0].isspace()
        if head.endswith("!"):
            head = head[:-1]
        if "(" in head:
            t, _, scope = head.partition("(")
            ok = ok and scope.endswith(")") and len(scope) > 1 and all(ch.islower() or ch.isdigit() or ch == "-" for ch in scope[:-1])
        else:
            t = head
        out.append(ok and t in types)
    return out


@O
def valid_commits(messages):
    return [bool(CC.match(m)) for m in messages]


Q(None, "Bump the Version From Commits", "Medium", "Semantic versioning",
  "Given the current version <code>'MAJOR.MINOR.PATCH'</code> and the commit subjects since the last release: any breaking change (<code>!</code> before the colon, or <code>BREAKING CHANGE</code> in the text) bumps major; else any <code>feat</code> bumps minor; else any <code>fix</code> or <code>perf</code> bumps patch; else no release (return the same version). Lower parts reset to 0.",
  [(("1.4.2", ["fix: null check", "feat(ui): dark mode", "chore: tidy"]), '1.5.0'), (("1.4.2", ["fix: typo", "perf: faster parse"]), '1.4.3'), (("1.4.2", ["refactor!: new config format", "feat: x"]), '2.0.0'), (("0.9.0", ["docs: readme"]), '0.9.0')],
  ("Flags for each level, then if/elif.", "O(c)", "O(1)"),
  ("Compute the highest level with max.", "O(c)", "O(1)"),
  viz=(("1.0.0", ["feat: x"])))


@B
def next_version(version, commits):
    major, minor, patch = [int(x) for x in version.split(".")]
    breaking = feat = fix = False
    for c in commits:
        head = c.split(":")[0]
        if head.endswith("!") or "BREAKING CHANGE" in c:
            breaking = True
        elif head.split("(")[0] == "feat":
            feat = True
        elif head.split("(")[0] in ("fix", "perf"):
            fix = True
    if breaking:
        return f"{major + 1}.0.0"
    if feat:
        return f"{major}.{minor + 1}.0"
    if fix:
        return f"{major}.{minor}.{patch + 1}"
    return version


@O
def next_version(version, commits):
    def level(c):
        head = c.split(":")[0]
        if head.endswith("!") or "BREAKING CHANGE" in c:
            return 3
        return {"feat": 2, "fix": 1, "perf": 1}.get(head.split("(")[0], 0)
    lvl = max(map(level, commits), default=0)
    v = [int(x) for x in version.split(".")]
    if lvl == 0:
        return version
    i = 3 - lvl
    v[i] += 1
    v[i + 1:] = [0] * (2 - i)
    return ".".join(map(str, v))


Q(None, "Bisect: Find the First Bad Commit", "Medium", "Binary search through history",
  "Commits are in order from old to new; <code>bad[i]</code> says whether the test fails at commit i (once broken, it stays broken). Return the index of the first bad commit and how many commits <code>git bisect</code> would test (binary search between the known good first and known bad last commit).",
  [(([False] * 37 + [True] * 27,), (37, 6)), (([False, True],), (1, 0)), (([False] * 999 + [True],), (999, 10))],
  ("Test commits one by one from the start.", "O(n)", "O(1)"),
  ("Binary search, counting tests.", "O(log n)", "O(1)"),
  viz=(([False, False, True, True],)))


@B
def bisect_first_bad(bad):
    first = next(i for i, b in enumerate(bad) if b)
    good, worst, tests = 0, len(bad) - 1, 0
    while worst - good > 1:
        mid = (good + worst) // 2
        tests += 1
        if mid >= first:
            worst = mid
        else:
            good = mid
    return (first, tests)


@O
def bisect_first_bad(bad):
    lo, hi, tests = 0, len(bad) - 1, 0
    while hi - lo > 1:
        mid = (lo + hi) // 2
        tests += 1
        lo, hi = (lo, mid) if bad[mid] else (mid, hi)
    return (hi, tests)


Q(None, "Rebase Replays Your Commits", "Medium", "New commits, same changes",
  "Your branch has commits <code>(id, {file: new content})</code> made on an old base. Rebasing replays each change, in order, on top of <code>new_base</code> (a dict of files), producing new commit ids <code>id + \"'\"</code>. Return the final files (sorted items) and the new ids.",
  [(({"app.py": "v1", "README.md": "hello", "setup.cfg": "x"}, [("a1", {"app.py": "v2"}), ("a2", {"tests.py": "t1", "app.py": "v3"})]), ([('README.md', 'hello'), ('app.py', 'v3'), ('setup.cfg', 'x'), ('tests.py', 't1')], ["a1'", "a2'"]))],
  ("Copy the dict and update in a loop.", "O(c · f)", "O(f)"),
  ("<code>dict.update</code> per commit.", "O(c · f)", "O(f)"),
  viz=(({"a": "1"}, [("c1", {"a": "2"})])))


@B
def rebase(new_base, commits):
    files = {}
    for k in new_base:
        files[k] = new_base[k]
    ids = []
    for cid, change in commits:
        for f, content in change.items():
            files[f] = content
        ids.append(cid + "'")
    return (sorted(files.items()), ids)


@O
def rebase(new_base, commits):
    files = dict(new_base)
    for _, change in commits:
        files.update(change)
    return (sorted(files.items()), [cid + "'" for cid, _ in commits])


Q(None, "Cherry-Pick One Commit", "Medium", "Apply a change elsewhere",
  "A commit changed files from <code>before</code> to <code>after</code> (dicts). Cherry-picking it onto <code>target</code> applies each changed file — but if the target's version of a changed file differs from <code>before</code>, that file conflicts. Return <code>(resulting files sorted, conflicting files sorted)</code>; conflicting files keep the target's version.",
  [(({"api.py": "v1", "db.py": "d1"}, {"api.py": "v2", "db.py": "d1", "new.py": "n1"}, {"api.py": "v1", "db.py": "d9", "ui.py": "u1"}), ([('api.py', 'v2'), ('db.py', 'd9'), ('new.py', 'n1'), ('ui.py', 'u1')], [])),
   (({"api.py": "v1"}, {"api.py": "v2"}, {"api.py": "v7"}), ([('api.py', 'v7')], ['api.py']))],
  ("Loop over the union of files.", "O(f)", "O(f)"),
  ("Compute changed files first, then apply.", "O(f)", "O(f)"),
  viz=(({"a": "1"}, {"a": "2"}, {"a": "1"})))


@B
def cherry_pick(before, after, target):
    result, conflicts = dict(target), []
    for f in set(before) | set(after):
        if before.get(f) == after.get(f):
            continue
        if target.get(f) != before.get(f):
            conflicts.append(f)
        elif f in after:
            result[f] = after[f]
        else:
            result.pop(f, None)
    return (sorted(result.items()), sorted(conflicts))


@O
def cherry_pick(before, after, target):
    changed = {f for f in before.keys() | after.keys() if before.get(f) != after.get(f)}
    conflicts = sorted(f for f in changed if target.get(f) != before.get(f))
    result = dict(target)
    for f in changed - set(conflicts):
        if f in after:
            result[f] = after[f]
        else:
            result.pop(f, None)
    return (sorted(result.items()), conflicts)


Q(None, "The Stash Stack", "Easy", "Put work aside",
  "Process commands: <code>('save', message)</code> pushes; <code>('pop',)</code> removes and returns the newest; <code>('apply', i)</code> returns entry i (0 = newest) without removing; <code>('list',)</code> returns the messages newest first. Return the outputs of pop, apply and list (an empty pop returns <code>'No stash entries found.'</code>).",
  [(([("save", "wip: login form"), ("save", "try new parser"), ("list",), ("apply", 1), ("pop",), ("pop",), ("pop",), ("list",)],), [['try new parser', 'wip: login form'], 'wip: login form', 'try new parser', 'wip: login form', 'No stash entries found.', []])],
  ("A list used as a stack, newest at the end.", "O(c · s)", "O(s)"),
  ("A deque with the newest on the left.", "O(c · s)", "O(s)"),
  viz=(([("save", "a"), ("pop",)],)))


@B
def stash(commands):
    stack, out = [], []
    for c in commands:
        if c[0] == "save":
            stack.append(c[1])
        elif c[0] == "pop":
            out.append(stack.pop() if stack else "No stash entries found.")
        elif c[0] == "apply":
            out.append(stack[len(stack) - 1 - c[1]])
        else:
            out.append(list(reversed(stack)))
    return out


@O
def stash(commands):
    stack, out = deque(), []
    for c in commands:
        if c[0] == "save":
            stack.appendleft(c[1])
        elif c[0] == "pop":
            out.append(stack.popleft() if stack else "No stash entries found.")
        else:
            out.append(stack[c[1]] if c[0] == "apply" else list(stack))
    return out


Q(None, "Who Wrote This Line? (blame)", "Medium", "Trace each line to its origin",
  "<code>versions</code> is the file's history: <code>(author, lines)</code> from oldest to newest. For each line of the newest version, return the author of the <b>earliest</b> version from which that exact line text was present in every later version.",
  [(([("asha", ["import os", "x = 1", "print(x)"]), ("ravi", ["import os", "import sys", "x = 1", "print(x)"]), ("meera", ["import os", "import sys", "x = 2", "print(x)"])],), [('asha', 'import os'), ('ravi', 'import sys'), ('meera', 'x = 2'), ('asha', 'print(x)')])],
  ("For each line, walk back while the previous version contains it.", "O(l · v · n)", "O(1)"),
  ("Same walk with sets of lines per version.", "O(v · n + l · v)", "O(v · n)"),
  viz=(([("a", ["x"]), ("b", ["x", "y"])],)))


@B
def blame(versions):
    final = versions[-1][1]
    out = []
    for line in final:
        i = len(versions) - 1
        while i > 0 and line in versions[i - 1][1]:
            i -= 1
        out.append((versions[i][0], line))
    return out


@O
def blame(versions):
    sets = [set(lines) for _, lines in versions]
    out = []
    for line in versions[-1][1]:
        i = len(versions) - 1
        while i and line in sets[i - 1]:
            i -= 1
        out.append((versions[i][0], line))
    return out


Q(None, "Branch Protection Rules", "Medium", "Can this PR be merged?",
  "A pull request can merge into a protected branch only if it has at least <code>rules['approvals']</code> approvals, every check in <code>rules['required_checks']</code> passed, it is not behind the base when <code>rules['up_to_date']</code> is True, and it has no unresolved conversations. Return <code>(mergeable, reasons sorted)</code> for each PR.",
  [(({"approvals": 2, "required_checks": ["lint", "tests", "build"], "up_to_date": True},
     [{"approvals": 2, "passed": ["lint", "tests", "build", "docs"], "behind": 0, "unresolved": 0},
      {"approvals": 1, "passed": ["lint", "tests"], "behind": 3, "unresolved": 1},
      {"approvals": 3, "passed": ["lint", "tests", "build"], "behind": 1, "unresolved": 0}]), [(True, []), (False, ['branch is behind', 'check failed: build', 'needs approvals', 'unresolved conversations']), (False, ['branch is behind'])])],
  ("If-statements collecting reasons.", "O(p · c)", "O(c)"),
  ("A list of (reason, failed?) checks.", "O(p · c)", "O(c)"),
  viz=(({"approvals": 1, "required_checks": ["t"], "up_to_date": False}, [{"approvals": 0, "passed": [], "behind": 0, "unresolved": 0}])))


@B
def can_merge(rules, prs):
    out = []
    for pr in prs:
        reasons = []
        if pr["approvals"] < rules["approvals"]:
            reasons.append("needs approvals")
        for c in rules["required_checks"]:
            if c not in pr["passed"]:
                reasons.append("check failed: " + c)
        if rules["up_to_date"] and pr["behind"] > 0:
            reasons.append("branch is behind")
        if pr["unresolved"] > 0:
            reasons.append("unresolved conversations")
        out.append((len(reasons) == 0, sorted(reasons)))
    return out


@O
def can_merge(rules, prs):
    def why(pr):
        tests = [("needs approvals", pr["approvals"] < rules["approvals"]),
                 ("branch is behind", rules["up_to_date"] and pr["behind"] > 0),
                 ("unresolved conversations", pr["unresolved"] > 0)]
        tests += [(f"check failed: {c}", c not in pr["passed"]) for c in rules["required_checks"]]
        return sorted(r for r, bad in tests if bad)
    return [(not r, r) for r in map(why, prs)]


Q(None, "Merge, Squash or Rebase?", "Easy", "What lands on main",
  "A branch has <code>n</code> commits and main has moved on (so no fast-forward). Return how many new commits each strategy adds to main: a merge commit (the branch commits plus one merge commit), squash-and-merge (one commit), rebase-and-merge (the branch commits, rewritten) — for each n.",
  [(([1, 4, 12],), [{'merge': 2, 'squash': 1, 'rebase': 1}, {'merge': 5, 'squash': 1, 'rebase': 4}, {'merge': 13, 'squash': 1, 'rebase': 12}])],
  ("A loop.", "O(k)", "O(k)"),
  ("A comprehension.", "O(k)", "O(k)"),
  viz=(([3],)))


@B
def strategies(ns):
    out = []
    for n in ns:
        out.append({"merge": n + 1, "squash": 1, "rebase": n})
    return out


@O
def strategies(ns):
    return [{"merge": n + 1, "squash": 1, "rebase": n} for n in ns]


SECRET_PATTERNS = [("aws_access_key", r"AKIA[0-9A-Z]{16}"), ("private_key", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
                   ("password", r"(?i)(password|passwd|pwd)\s*=\s*['\"][^'\"]{4,}['\"]"), ("github_token", r"gh[pousr]_[A-Za-z0-9]{36}")]


Q(None, "Catch Secrets Before You Commit", "Medium", "A pre-commit hook",
  "Scan a diff: only <b>added</b> lines (starting with <code>+</code>, but not the <code>+++</code> file header) count. Return <code>(line number in the diff, kind)</code> for every match of <code>SECRET_PATTERNS</code>, in order. Secrets in Git history are effectively public — catching them before commit is far cheaper than rotating them after.",
  [(([ "+++ b/settings.py", "+DEBUG = True", "+password = 'hunter2!'", "-password = os.environ['PW']", "+AWS_KEY = 'AKIAIOSFODNN7EXAMPLE'", " unchanged = 1", "+key = '-----BEGIN RSA PRIVATE KEY-----'", "+token = 'ghp_abcdefghijklmnopqrstuvwxyz0123456789'"],), [(3, 'password'), (5, 'aws_access_key'), (7, 'private_key'), (8, 'github_token')])],
  ("Loop over lines and patterns with re.search.", "O(l · p)", "O(1)"),
  ("Precompile the patterns once.", "O(l · p)", "O(p)"),
  viz=((["+pwd = 'secret1'"],)))


@B
def find_secrets(diff):
    out = []
    for i, line in enumerate(diff, 1):
        if not line.startswith("+") or line.startswith("+++"):
            continue
        for kind, pat in SECRET_PATTERNS:
            if re.search(pat, line):
                out.append((i, kind))
    return out


@O
def find_secrets(diff):
    compiled = [(k, re.compile(p)) for k, p in SECRET_PATTERNS]
    return [(i, k) for i, line in enumerate(diff, 1) if line[:1] == "+" and line[:3] != "+++"
            for k, rx in compiled if rx.search(line)]


Q(None, "What Changed Between Two Commits?", "Medium", "git diff --name-status",
  "Each snapshot maps path → content hash. Return sorted <code>(status, path)</code> entries: <code>A</code> added, <code>D</code> deleted, <code>M</code> modified, and <code>R</code> for a rename — a deleted path whose exact hash appears at a single added path (report it as <code>'old -> new'</code>, not as A + D).",
  [(({"src/app.py": "h1", "src/util.py": "h2", "docs/old.md": "h3", "setup.py": "h4"}, {"src/app.py": "h1b", "src/utils/helpers.py": "h2", "docs/guide.md": "h9", "setup.py": "h4", "tests/test_app.py": "h5"}), [('A', 'docs/guide.md'), ('A', 'tests/test_app.py'), ('D', 'docs/old.md'), ('M', 'src/app.py'), ('R', 'src/util.py -> src/utils/helpers.py')])],
  ("Compare dicts with loops, then pair renames.", "O(n²)", "O(n)"),
  ("Index added files by hash for rename matching.", "O(n)", "O(n)"),
  viz=(({"a": "1"}, {"b": "1"})))


@B
def name_status(old, new):
    added = [p for p in new if p not in old]
    deleted = [p for p in old if p not in new]
    out = [("M", p) for p in old if p in new and old[p] != new[p]]
    for d in deleted:
        same = [a for a in added if new[a] == old[d]]
        if len(same) == 1:
            out.append(("R", d + " -> " + same[0]))
            added.remove(same[0])
        else:
            out.append(("D", d))
    out += [("A", a) for a in added]
    return sorted(out)


@O
def name_status(old, new):
    added = new.keys() - old.keys()
    by_hash = defaultdict(list)
    for a in added:
        by_hash[new[a]].append(a)
    out, renamed = [("M", p) for p in old.keys() & new.keys() if old[p] != new[p]], set()
    for d in old.keys() - new.keys():
        match = by_hash.get(old[d], [])
        if len(match) == 1:
            out.append(("R", f"{d} -> {match[0]}"))
            renamed.add(match[0])
        else:
            out.append(("D", d))
    out += [("A", a) for a in added - renamed]
    return sorted(out)


Q(None, "Contribution Summary (shortlog)", "Easy", "Who did what",
  "Commits are <code>(author, insertions, deletions)</code>. Return <code>(author, commits, insertions, deletions)</code> per author, most commits first (ties by name).",
  [(([("asha", 120, 30), ("ravi", 15, 2), ("asha", 40, 40), ("meera", 300, 10), ("ravi", 8, 1), ("ravi", 60, 5)],), [('ravi', 3, 83, 8), ('asha', 2, 160, 70), ('meera', 1, 300, 10)])],
  ("Dicts of running totals.", "O(c + a log a)", "O(a)"),
  ("<code>defaultdict</code> of lists.", "O(c + a log a)", "O(a)"),
  viz=(([("a", 1, 0)],)))


@B
def shortlog(commits):
    stats = {}
    for a, ins, dels in commits:
        if a not in stats:
            stats[a] = [0, 0, 0]
        stats[a][0] += 1
        stats[a][1] += ins
        stats[a][2] += dels
    rows = [(a, s[0], s[1], s[2]) for a, s in stats.items()]
    rows.sort(key=lambda r: (-r[1], r[0]))
    return rows


@O
def shortlog(commits):
    s = defaultdict(lambda: [0, 0, 0])
    for a, ins, dels in commits:
        s[a][0] += 1
        s[a][1] += ins
        s[a][2] += dels
    return sorted(((a, *v) for a, v in s.items()), key=lambda r: (-r[1], r[0]))
