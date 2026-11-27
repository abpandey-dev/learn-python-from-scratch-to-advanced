from lib import *
import argparse
import datetime as dt
import fnmatch
import posixpath
import re
import shlex
from collections import Counter, defaultdict

TOPIC(
    id="cli-linux", title="The Command Line & Linux", glyph="$",
    blurb="The shell skills every engineer needs, rebuilt in Python: permissions and chmod, globs, paths, argparse CLIs, exit codes and &&/||, wc, sort | uniq -c, grep, head and tail, cut, cron schedules, du, find, log parsing, variable expansion, process trees, signals, disk alerts and shell quoting.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">ls -la; cd -; pwd; mkdir -p a/b; cp -r src dst; mv a b; rm -rf build/
grep -rn "TODO" src/ ; find . -name "*.py" -mtime -1 ; du -sh * ; df -h
cut -d, -f2 data.csv | sort | uniq -c | sort -rn | head
tail -f app.log ; less app.log ; ps aux | grep python ; kill -TERM 4242
chmod 750 deploy.sh ; chmod u+x run.sh ; echo $? ; export APP_ENV=prod
crontab -e    # */15 9-17 * * 1-5  python /opt/report.py</code></pre>
""")


Q(None, "Read ls -l Permissions", "Easy", "rwx to octal",
  "Convert permission strings like <code>-rwxr-xr--</code> (type character, then owner, group, others) into <code>(type, octal)</code>: type is <code>'file'</code>, <code>'dir'</code> or <code>'link'</code>; each rwx triple is r=4 + w=2 + x=1.",
  [((["-rwxr-xr--", "drwxr-x---", "-rw-r--r--", "lrwxrwxrwx", "-rw-------"],), [('file', '754'), ('dir', '750'), ('file', '644'), ('link', '777'), ('file', '600')])],
  ("Add up each triple with if-statements.", "O(n)", "O(n)"),
  ("Map each character to a bit and use int(..., 2).", "O(n)", "O(n)"),
  viz=((["-rwx------"],)))


@B
def perms(entries):
    out = []
    for e in entries:
        kind = {"-": "file", "d": "dir", "l": "link"}[e[0]]
        digits = ""
        for i in range(1, 10, 3):
            v = 0
            if e[i] == "r":
                v += 4
            if e[i + 1] == "w":
                v += 2
            if e[i + 2] == "x":
                v += 1
            digits += str(v)
        out.append((kind, digits))
    return out


@O
def perms(entries):
    return [({"-": "file", "d": "dir", "l": "link"}[e[0]], format(int("".join("0" if c == "-" else "1" for c in e[1:]), 2), "03o")) for e in entries]


Q(None, "Apply chmod Changes", "Medium", "u+x, go-w, a=r",
  "Start from an octal mode (string like <code>'644'</code>) and apply symbolic changes in order: who (<code>u</code>, <code>g</code>, <code>o</code>, <code>a</code>, combinable), an operator (<code>+</code> add, <code>-</code> remove, <code>=</code> set exactly) and permissions (<code>r</code>, <code>w</code>, <code>x</code>). Return the mode after each change.",
  [(("644", ["u+x", "go-r", "a+x", "g=rw", "o=", "a-w"]), ['744', '700', '711', '761', '760', '540'])],
  ("Keep three digits and update each with if-statements.", "O(c)", "O(1)"),
  ("Work on a 9-bit integer with masks.", "O(c)", "O(1)"),
  viz=(("600", ["g+r"])))


@B
def chmod(mode, changes):
    digits = [int(c) for c in mode]
    out = []
    for ch in changes:
        m = re.fullmatch(r"([ugoa]+)([+=-])([rwx]*)", ch)
        who, op, what = m.groups()
        if "a" in who:
            who = "ugo"
        bits = 0
        for p in what:
            bits += {"r": 4, "w": 2, "x": 1}[p]
        for w in who:
            i = "ugo".index(w)
            if op == "+":
                digits[i] = digits[i] | bits
            elif op == "-":
                digits[i] = digits[i] & ~bits
            else:
                digits[i] = bits
        out.append("".join(str(d) for d in digits))
    return out


@O
def chmod(mode, changes):
    m, out = int(mode, 8), []
    for ch in changes:
        who, op, what = re.fullmatch(r"([ugoa]+)([+=-])([rwx]*)", ch).groups()
        bits = sum({"r": 4, "w": 2, "x": 1}[p] for p in what)
        shifts = [6, 3, 0] if "a" in who else [{"u": 6, "g": 3, "o": 0}[w] for w in who]
        for s in shifts:
            m = m | bits << s if op == "+" else m & ~(bits << s) if op == "-" else (m & ~(7 << s)) | bits << s
        out.append(format(m, "03o"))
    return out


Q(None, "Match Shell Globs", "Easy", "*, ? and [abc]",
  "For each pattern, return the paths it matches. As in the shell, <code>*</code> and <code>?</code> never match a <code>/</code>, so match segment by segment (same number of segments).",
  [((["*.py", "src/*.py", "data/202?-*.csv", "tests/test_[ab]*.py", "*/*/*.json"], ["setup.py", "src/app.py", "src/util/io.py", "data/2024-01.csv", "data/2025-06.csv", "data/archive/2023-01.csv", "tests/test_api.py", "tests/test_cli.py", "tests/test_b2.py", "conf/dev/settings.json"]), {'*.py': ['setup.py'], 'src/*.py': ['src/app.py'], 'data/202?-*.csv': ['data/2024-01.csv', 'data/2025-06.csv'], 'tests/test_[ab]*.py': ['tests/test_api.py', 'tests/test_b2.py'], '*/*/*.json': ['conf/dev/settings.json']})],
  ("Split into segments and fnmatch each.", "O(p · n · L)", "O(L)"),
  ("Translate each pattern to one regex where * is [^/]*.", "O(p · n · L)", "O(L)"),
  viz=((["*.txt"], ["a.txt", "d/b.txt"])))


@B
def globs(patterns, paths):
    out = {}
    for pat in patterns:
        pp = pat.split("/")
        hits = []
        for path in paths:
            parts = path.split("/")
            if len(parts) == len(pp) and all(fnmatch.fnmatchcase(a, b) for a, b in zip(parts, pp)):
                hits.append(path)
        out[pat] = hits
    return out


@O
def globs(patterns, paths):
    def rx(pat):
        r = ""
        for ch in re.split(r"(\*|\?|\[[^\]]*\])", pat):
            r += "[^/]*" if ch == "*" else "[^/]" if ch == "?" else ch if ch.startswith("[") else re.escape(ch)
        return re.compile(r)
    return {p: [x for x in paths if rx(p).fullmatch(x)] for p in patterns}


Q(None, "Resolve Paths", "Medium", "cd, ., .. and ~",
  "Turn each path into an absolute, normalised path, as the shell would from the current directory <code>cwd</code> with home <code>home</code>: <code>~</code> at the start means home, relative paths start from cwd, <code>.</code> and empty parts are dropped, <code>..</code> goes up (never above <code>/</code>).",
  [(("/home/asha/proj", "/home/asha", ["src/../tests", "./data//raw/", "~/notes.txt", "/var/log/../../etc", "../../../../..", "~"]), ['/home/asha/proj/tests', '/home/asha/proj/data/raw', '/home/asha/notes.txt', '/etc', '/', '/home/asha'])],
  ("A stack of parts.", "O(n · L)", "O(L)"),
  ("<code>posixpath.join</code> and <code>normpath</code>, then fix the root case.", "O(n · L)", "O(L)"),
  viz=(("/a", "/h", ["b/../c"])))


@B
def resolve_paths(cwd, home, paths):
    out = []
    for p in paths:
        if p == "~" or p.startswith("~/"):
            p = home + p[1:]
        if not p.startswith("/"):
            p = cwd + "/" + p
        stack = []
        for part in p.split("/"):
            if part in ("", "."):
                continue
            if part == "..":
                if stack:
                    stack.pop()
            else:
                stack.append(part)
        out.append("/" + "/".join(stack))
    return out


@O
def resolve_paths(cwd, home, paths):
    out = []
    for p in paths:
        p = posixpath.join(cwd, home + p[1:] if p == "~" or p.startswith("~/") else p)
        n = posixpath.normpath(p)
        out.append("/" + n.lstrip("/"))
    return out


def report_parser():
    p = argparse.ArgumentParser(prog="report")
    p.add_argument("inputs", nargs="+")
    p.add_argument("--since")
    p.add_argument("--format", choices=["csv", "json"], default="csv")
    p.add_argument("-v", "--verbose", action="count", default=0)
    p.add_argument("--dry-run", action="store_true")
    return p


Q(None, "Build a CLI With argparse", "Medium", "Options, flags and arguments",
  "The tool <code>report</code> takes one or more input files, an optional <code>--since DATE</code>, <code>--format</code> (<code>csv</code> or <code>json</code>, default csv), a repeatable <code>-v</code>/<code>--verbose</code> counter and a <code>--dry-run</code> flag. Return the parsed settings for each argument list as a dict. The brute force parses by hand; the optimal uses <code>argparse</code> (<code>report_parser()</code>).",
  [(([["sales.csv"], ["a.csv", "b.csv", "--format", "json", "-v", "-v"], ["--since", "2026-01-01", "--dry-run", "x.csv", "--verbose"], ["-vv", "jan.csv", "--format=json"]],), [{'inputs': ['sales.csv'], 'since': None, 'format': 'csv', 'verbose': 0, 'dry_run': False}, {'inputs': ['a.csv', 'b.csv'], 'since': None, 'format': 'json', 'verbose': 2, 'dry_run': False}, {'inputs': ['x.csv'], 'since': '2026-01-01', 'format': 'csv', 'verbose': 1, 'dry_run': True}, {'inputs': ['jan.csv'], 'since': None, 'format': 'json', 'verbose': 2, 'dry_run': False}])],
  ("Walk the arguments with a while loop.", "O(n)", "O(n)"),
  ("<code>argparse.ArgumentParser.parse_args</code>.", "O(n)", "O(n)"),
  viz=(([["a.csv", "-v"]],)))


@B
def parse_cli(argvs):
    out = []
    for argv in argvs:
        r = {"inputs": [], "since": None, "format": "csv", "verbose": 0, "dry_run": False}
        i = 0
        while i < len(argv):
            a = argv[i]
            if a.startswith("--") and "=" in a:
                key, val = a[2:].split("=", 1)
                r[key.replace("-", "_")] = val
            elif a in ("--since", "--format"):
                r[a[2:]] = argv[i + 1]
                i += 1
            elif a == "--dry-run":
                r["dry_run"] = True
            elif a == "--verbose":
                r["verbose"] += 1
            elif a.startswith("-v") and set(a[1:]) == {"v"}:
                r["verbose"] += len(a) - 1
            else:
                r["inputs"].append(a)
            i += 1
        out.append(r)
    return out


@O
def parse_cli(argvs):
    parser = report_parser()
    return [vars(parser.parse_args(a)) for a in argvs]


Q(None, "Exit Codes, && and ||", "Medium", "How the shell chains commands",
  "Each command has an exit code (0 = success). In <code>a && b</code>, b runs only if the last status is 0; in <code>a || b</code>, b runs only if it is non-zero; operators apply left to right. Given a chain like <code>['test', '&&', 'build', '||', 'notify']</code> and the exit code of each command, return <code>(commands that ran, final exit status)</code>.",
  [((["lint", "&&", "test", "&&", "deploy"], {"lint": 0, "test": 1, "deploy": 0}), (['lint', 'test'], 1)), ((["build", "||", "notify", "&&", "cleanup"], {"build": 2, "notify": 0, "cleanup": 0}), (['build', 'notify', 'cleanup'], 0)), ((["make", "||", "echo"], {"make": 0, "echo": 0}), (['make'], 0))],
  ("Walk the list with an index.", "O(n)", "O(n)"),
  ("Iterate over (operator, command) pairs.", "O(n)", "O(n)"),
  viz=((["a", "&&", "b"], {"a": 1, "b": 0})))


@B
def chain(tokens, codes):
    ran = [tokens[0]]
    status = codes[tokens[0]]
    i = 1
    while i < len(tokens):
        op, cmd = tokens[i], tokens[i + 1]
        if (op == "&&" and status == 0) or (op == "||" and status != 0):
            ran.append(cmd)
            status = codes[cmd]
        i += 2
    return (ran, status)


@O
def chain(tokens, codes):
    ran, status = [tokens[0]], codes[tokens[0]]
    for op, cmd in zip(tokens[1::2], tokens[2::2]):
        if (status == 0) == (op == "&&"):
            ran.append(cmd)
            status = codes[cmd]
    return (ran, status)


Q(None, "wc: Lines, Words, Characters", "Easy", "Counting text",
  "Return <code>(lines, words, characters)</code> like <code>wc</code>: lines counts newline characters, words are runs of non-whitespace, characters counts every character.",
  [(("ERROR db timeout\nINFO  started\n\nWARN  slow query 812ms\n",), (4, 9, 55)), (("no newline at end",), (0, 4, 17))],
  ("One pass with a state flag.", "O(n)", "O(1)"),
  ("<code>count</code>, <code>split</code> and <code>len</code>.", "O(n)", "O(n)"),
  viz=(("a b\nc\n",)))


@B
def wc(text):
    lines = words = 0
    in_word = False
    for ch in text:
        if ch == "\n":
            lines += 1
        if ch.isspace():
            in_word = False
        elif not in_word:
            words += 1
            in_word = True
    return (lines, words, len(text))


@O
def wc(text):
    return (text.count("\n"), len(text.split()), len(text))


Q(None, "sort | uniq -c | sort -rn | head", "Easy", "The classic count pipeline",
  "Count each line in a log (e.g. client IPs), and return the top <code>k</code> as <code>(count, line)</code>, highest count first (ties: line sorted ascending) — exactly what <code>sort | uniq -c | sort -rn | head -n k</code> shows.",
  [((["10.0.0.5", "10.0.0.9", "10.0.0.5", "192.168.1.20", "10.0.0.9", "10.0.0.5", "172.16.0.2", "192.168.1.20", "10.0.0.9"], 3), [(3, '10.0.0.5'), (3, '10.0.0.9'), (2, '192.168.1.20')])],
  ("Sort, group adjacent equal lines, then sort counts.", "O(n log n)", "O(n)"),
  ("<code>Counter</code> and a sort key.", "O(n + u log u)", "O(u)"),
  viz=((["a", "b", "a"], 1)))


@B
def top_lines(lines, k):
    s = sorted(lines)
    groups = []
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        groups.append((j - i, s[i]))
        i = j
    groups.sort(key=lambda g: (-g[0], g[1]))
    return groups[:k]


@O
def top_lines(lines, k):
    return sorted(((n, l) for l, n in Counter(lines).items()), key=lambda g: (-g[0], g[1]))[:k]


Q(None, "grep With Flags", "Easy", "-i, -v, -n, -c",
  "Implement <code>grep</code>: return matching lines for a regex <code>pattern</code>, honouring flags in <code>flags</code>: <code>i</code> (ignore case), <code>v</code> (invert), <code>n</code> (prefix <code>'line:'</code> with the 1-based line number), <code>c</code> (return only the count).",
  [(("error|warn", "i", ["INFO boot ok", "WARN disk 91%", "ERROR db timeout", "info error budget ok"]), ['WARN disk 91%', 'ERROR db timeout', 'info error budget ok']),
   (("^INFO", "vn", ["INFO boot ok", "WARN disk 91%", "ERROR db timeout"]), ['2:WARN disk 91%', '3:ERROR db timeout']),
   (("timeout", "c", ["ERROR db timeout", "ERROR api timeout", "INFO ok"]), 2)],
  ("Loop with if-statements per flag.", "O(n · L)", "O(n)"),
  ("Compile once; comprehension with an XOR for -v.", "O(n · L)", "O(n)"),
  viz=(("a", "", ["a", "b"])))


@B
def grep(pattern, flags, lines):
    out = []
    for i, line in enumerate(lines, 1):
        if "i" in flags:
            hit = re.search(pattern, line, re.IGNORECASE) is not None
        else:
            hit = re.search(pattern, line) is not None
        if "v" in flags:
            hit = not hit
        if hit:
            out.append(f"{i}:{line}" if "n" in flags else line)
    return len(out) if "c" in flags else out


@O
def grep(pattern, flags, lines):
    rx = re.compile(pattern, re.I if "i" in flags else 0)
    out = [f"{i}:{l}" if "n" in flags else l for i, l in enumerate(lines, 1) if bool(rx.search(l)) != ("v" in flags)]
    return len(out) if "c" in flags else out


Q(None, "head and tail", "Easy", "Slices of a file",
  "Run a small pipeline of <code>head -n N</code> and <code>tail -n N</code> steps (and <code>tail -n +N</code>, meaning 'from line N on') over the lines, in order. Return the result.",
  [((list(range(1, 21)), ["head -n 15", "tail -n 4"]), [12, 13, 14, 15]), ((list(range(1, 21)), ["tail -n +18"]), [18, 19, 20]), ((list(range(1, 6)), ["tail -n 10", "head -n 2"]), [1, 2])],
  ("Rebuild lists with loops.", "O(s · n)", "O(n)"),
  ("Slicing.", "O(s · n)", "O(n)"),
  viz=(([1, 2, 3], ["tail -n 2"])))


@B
def head_tail(lines, steps):
    cur = list(lines)
    for s in steps:
        cmd, _, n = s.split()
        if cmd == "head":
            new = []
            for i in range(min(int(n), len(cur))):
                new.append(cur[i])
            cur = new
        elif n.startswith("+"):
            cur = [cur[i] for i in range(int(n) - 1, len(cur))]
        else:
            start = max(0, len(cur) - int(n))
            cur = [cur[i] for i in range(start, len(cur))]
    return cur


@O
def head_tail(lines, steps):
    cur = list(lines)
    for s in steps:
        cmd, _, n = s.split()
        cur = cur[:int(n)] if cmd == "head" else cur[int(n) - 1:] if n[0] == "+" else cur[-int(n):] if int(n) else []
    return cur


Q(None, "cut Columns", "Easy", "cut -d, -f2,4",
  "Return the selected 1-based fields (a field list like <code>'2,4'</code> or a range like <code>'2-4'</code>, or a mix such as <code>'1,3-4'</code>) from each line split on the delimiter, joined back with the delimiter. Missing fields are left out.",
  [((["id,name,city,plan", "1,Asha,Pune,pro", "2,Ravi,Delhi", "3,Meera,Goa,basic"], ",", "1,3-4"), ['id,city,plan', '1,Pune,pro', '2,Delhi', '3,Goa,basic'])],
  ("Expand the field list with loops.", "O(n · f)", "O(f)"),
  ("A set of field numbers and a comprehension.", "O(n · f)", "O(f)"),
  viz=((["a:b:c"], ":", "2")))


@B
def cut(lines, delim, fields):
    wanted = []
    for part in fields.split(","):
        if "-" in part:
            a, b = part.split("-")
            for f in range(int(a), int(b) + 1):
                wanted.append(f)
        else:
            wanted.append(int(part))
    out = []
    for line in lines:
        cols = line.split(delim)
        picked = []
        for i in range(len(cols)):
            if i + 1 in wanted:
                picked.append(cols[i])
        out.append(delim.join(picked))
    return out


@O
def cut(lines, delim, fields):
    want = set()
    for part in fields.split(","):
        a, _, b = part.partition("-")
        want |= set(range(int(a), int(b or a) + 1))
    return [delim.join(c for i, c in enumerate(l.split(delim), 1) if i in want) for l in lines]


def cron_field(expr, lo, hi):
    out = set()
    for part in expr.split(","):
        rng, _, step = part.partition("/")
        if rng == "*":
            a, b = lo, hi
        elif "-" in rng:
            a, b = map(int, rng.split("-"))
        else:
            a = b = int(rng)
        out |= set(range(a, b + 1, int(step or 1)))
    return out


Q(None, "When Does the Cron Job Run?", "Medium", "minute hour day month weekday",
  "Given a cron expression (fields: minute 0–59, hour 0–23, day of month 1–31, month 1–12, weekday 0–6 with 0 = Sunday; supporting <code>*</code>, lists, ranges and <code>/step</code>) and a start time <code>'YYYY-MM-DD HH:MM'</code>, return the next <code>n</code> run times strictly after the start. (For simplicity, a run needs both the day-of-month and weekday fields to match.)",
  [(("*/15 9-17 * * 1-5", "2026-11-27 17:40", 4), ['2026-11-27 17:45', '2026-11-30 09:00', '2026-11-30 09:15', '2026-11-30 09:30']), (("0 2 1 * *", "2026-11-27 10:00", 2), ['2026-12-01 02:00', '2027-01-01 02:00'])],
  ("Step forward one minute at a time.", "O(minutes searched)", "O(1)"),
  ("Skip whole days and hours that can't match.", "O(days + matches)", "O(1)"),
  viz=(("0 * * * *", "2026-01-01 10:30", 2)))


@B
def cron_next(expr, start, n):
    mins, hours, doms, months, dows = (cron_field(f, lo, hi) for f, (lo, hi) in zip(expr.split(), [(0, 59), (0, 23), (1, 31), (1, 12), (0, 6)]))
    t = dt.datetime.strptime(start, "%Y-%m-%d %H:%M")
    out = []
    while len(out) < n:
        t += dt.timedelta(minutes=1)
        if t.minute in mins and t.hour in hours and t.day in doms and t.month in months and (t.weekday() + 1) % 7 in dows:
            out.append(t.strftime("%Y-%m-%d %H:%M"))
    return out


@O
def cron_next(expr, start, n):
    mins, hours, doms, months, dows = (sorted(cron_field(f, lo, hi)) for f, (lo, hi) in zip(expr.split(), [(0, 59), (0, 23), (1, 31), (1, 12), (0, 6)]))
    t0 = dt.datetime.strptime(start, "%Y-%m-%d %H:%M")
    day, out = t0.date(), []
    while len(out) < n:
        if day.day in doms and day.month in months and (day.weekday() + 1) % 7 in dows:
            for h in hours:
                for m in mins:
                    t = dt.datetime(day.year, day.month, day.day, h, m)
                    if t > t0 and len(out) < n:
                        out.append(t.strftime("%Y-%m-%d %H:%M"))
        day += dt.timedelta(days=1)
    return out


def human(size):
    for unit in ["B", "K", "M", "G", "T"]:
        if size < 1024 or unit == "T":
            return f"{size:.0f}{unit}" if unit == "B" else f"{size:.1f}{unit}"
        size /= 1024


Q(None, "du -sh: What's Using the Disk?", "Easy", "Sizes by folder",
  "Given file sizes in bytes (path → size), total them by top-level folder (files at the top level count under their own name) and return <code>(name, human size)</code> largest first, using <code>human</code> (1024-based units).",
  [(({"data/raw/events.parquet": 3_221_225_472, "data/raw/users.csv": 52_428_800, "logs/app.log": 734_003_200, "logs/app.log.1": 1_073_741_824, "src/main.py": 4_096, "README.md": 2_048, ".venv/lib/torch.so": 2_147_483_648},), [('data', '3.0G'), ('.venv', '2.0G'), ('logs', '1.7G'), ('src', '4.0K'), ('README.md', '2.0K')])],
  ("Sum into a dict, then sort.", "O(f log f)", "O(d)"),
  ("<code>defaultdict(int)</code> and sorted items.", "O(f log f)", "O(d)"),
  viz=(({"a/x": 2048, "b": 10},)))


@B
def du(files):
    totals = {}
    for path, size in files.items():
        top = path.split("/")[0]
        totals[top] = totals.get(top, 0) + size
    rows = sorted(totals.items(), key=lambda r: -r[1])
    return [(name, human(size)) for name, size in rows]


@O
def du(files):
    t = defaultdict(int)
    for path, size in files.items():
        t[path.partition("/")[0]] += size
    return [(n, human(s)) for n, s in sorted(t.items(), key=lambda r: -r[1])]


Q(None, "find Files by Name, Size and Age", "Easy", "find . -name -size -mtime",
  "Files are <code>(path, size_kb, age_days)</code>. Return the paths whose file name matches <code>name</code> (a glob), whose size is over <code>min_kb</code> and whose age is over <code>min_days</code> — e.g. old big logs to clean up.",
  [(([("logs/app-2026-10-01.log", 52_000, 57), ("logs/app-2026-11-26.log", 48_000, 1), ("logs/tiny.log", 3, 90), ("data/export.csv", 900_000, 120), ("logs/archive/app-2026-08-01.log", 61_000, 118)], "*.log", 1024, 30), ['logs/app-2026-10-01.log', 'logs/archive/app-2026-08-01.log'])],
  ("A loop with three conditions.", "O(n)", "O(n)"),
  ("A comprehension.", "O(n)", "O(n)"),
  viz=(([("a.log", 2000, 40)], "*.log", 1000, 30)))


@B
def find_files(files, name, min_kb, min_days):
    out = []
    for path, kb, age in files:
        base = path.split("/")[-1]
        if fnmatch.fnmatch(base, name) and kb > min_kb and age > min_days:
            out.append(path)
    return out


@O
def find_files(files, name, min_kb, min_days):
    return [p for p, kb, age in files if fnmatch.fnmatch(posixpath.basename(p), name) and kb > min_kb and age > min_days]


LOG = re.compile(r'^(\S+) \S+ \S+ \[[^\]]+\] "(\S+) (\S+) [^"]*" (\d{3}) (\d+)')


Q(None, "Parse an Access Log", "Medium", "Regex on real log lines",
  "Parse nginx access-log lines with the regex <code>LOG</code> and return <code>{'by_class': counts of 2xx/3xx/4xx/5xx, 'top_path': most requested path (ties alphabetical), 'bytes': total bytes sent, 'bad_lines': lines that didn't parse}</code>.",
  [(([
      '10.0.0.5 - - [27/Nov/2026:10:00:01 +0530] "GET /api/orders HTTP/1.1" 200 512 "-" "curl/8.4"',
      '10.0.0.9 - - [27/Nov/2026:10:00:02 +0530] "POST /api/login HTTP/1.1" 401 98 "-" "Mozilla/5.0"',
      '10.0.0.5 - - [27/Nov/2026:10:00:03 +0530] "GET /api/orders HTTP/1.1" 200 530 "-" "curl/8.4"',
      'garbage line',
      '10.0.0.7 - - [27/Nov/2026:10:00:04 +0530] "GET /health HTTP/1.1" 200 2 "-" "kube-probe"',
      '10.0.0.9 - - [27/Nov/2026:10:00:05 +0530] "GET /api/orders HTTP/1.1" 502 157 "-" "Mozilla/5.0"',
      '10.0.0.8 - - [27/Nov/2026:10:00:06 +0530] "GET /old HTTP/1.1" 301 0 "-" "Mozilla/5.0"'],), {'by_class': {'2xx': 3, '3xx': 1, '4xx': 1, '5xx': 1}, 'top_path': '/api/orders', 'bytes': 1299, 'bad_lines': 1})],
  ("Dicts and if-statements per line.", "O(n)", "O(n)"),
  ("Counters over the parsed tuples.", "O(n)", "O(n)"),
  viz=((['1.1.1.1 - - [x] "GET / HTTP/1.1" 200 5 "-" "-"'],)))


@B
def access_log(lines):
    by_class, paths, total, bad = {}, {}, 0, 0
    for line in lines:
        m = LOG.match(line)
        if not m:
            bad += 1
            continue
        _, _, path, status, size = m.groups()
        cls = status[0] + "xx"
        by_class[cls] = by_class.get(cls, 0) + 1
        paths[path] = paths.get(path, 0) + 1
        total += int(size)
    top = sorted(paths, key=lambda p: (-paths[p], p))[0]
    return {"by_class": dict(sorted(by_class.items())), "top_path": top, "bytes": total, "bad_lines": bad}


@O
def access_log(lines):
    parsed = [m.groups() for m in map(LOG.match, lines) if m]
    paths = Counter(p for _, _, p, _, _ in parsed)
    return {"by_class": dict(sorted(Counter(s[0] + "xx" for *_, s, _ in parsed).items())),
            "top_path": min(paths, key=lambda p: (-paths[p], p)), "bytes": sum(int(b) for *_, b in parsed),
            "bad_lines": len(lines) - len(parsed)}


Q(None, "Expand Shell Variables", "Medium", "$VAR, ${VAR} and ${VAR:-default}",
  "Expand <code>$NAME</code>, <code>${NAME}</code> and <code>${NAME:-default}</code> (default used when the variable is unset or empty) in each string using <code>env</code>; unknown variables become empty. Text in single quotes is not expanded (keep it, without the quotes).",
  [((["$HOME/projects/${APP}_logs", "${PORT:-8080}", "db=${DB_HOST:-localhost}:${DB_PORT:-5432}", "'$HOME stays literal' but $USER does not", "${EMPTY:-fallback}${MISSING}end"], {"HOME": "/home/asha", "APP": "billing", "DB_HOST": "db.internal", "USER": "asha", "EMPTY": ""}), ['/home/asha/projects/billing_logs', '8080', 'db=db.internal:5432', '$HOME stays literal but asha does not', 'fallbackend'])],
  ("A character-by-character scanner.", "O(n · L)", "O(L)"),
  ("Split on single-quoted parts; re.sub elsewhere.", "O(n · L)", "O(L)"),
  viz=((["$A-${B:-x}"], {"A": "1"})))


@B
def expand(strings, env):
    out = []
    for s in strings:
        r, i = "", 0
        while i < len(s):
            c = s[i]
            if c == "'":
                j = s.index("'", i + 1)
                r += s[i + 1:j]
                i = j + 1
            elif c == "$" and i + 1 < len(s) and s[i + 1] == "{":
                j = s.index("}", i)
                inner = s[i + 2:j]
                name, _, default = inner.partition(":-")
                r += env.get(name) or (default if ":-" in inner else "")
                i = j + 1
            elif c == "$":
                j = i + 1
                while j < len(s) and (s[j].isalnum() or s[j] == "_"):
                    j += 1
                r += env.get(s[i + 1:j], "")
                i = j
            else:
                r += c
                i += 1
        out.append(r)
    return out


@O
def expand(strings, env):
    rx = re.compile(r"\$\{(\w+)(:-([^}]*))?\}|\$(\w+)")
    def sub(m):
        if m.group(4):
            return env.get(m.group(4), "")
        return env.get(m.group(1)) or (m.group(3) if m.group(2) else "")
    return ["".join(p[1:-1] if p.startswith("'") else rx.sub(sub, p) for p in re.split(r"('[^']*')", s)) for s in strings]


Q(None, "Kill a Process Tree", "Medium", "Children first",
  "Processes are <code>(pid, ppid, command)</code>. To stop <code>root</code> cleanly, signal its descendants before it: return the pids in post-order (each child's subtree in ascending pid order, then the parent).",
  [(([(1, 0, "systemd"), (100, 1, "gunicorn master"), (101, 100, "gunicorn worker"), (102, 100, "gunicorn worker"), (150, 101, "python child"), (200, 1, "nginx"), (201, 200, "nginx worker")], 100), [150, 101, 102, 100])],
  ("Recursively scan the whole table for children.", "O(n²)", "O(n)"),
  ("Build a children map once.", "O(n log n)", "O(n)"),
  viz=(([(1, 0, "a"), (2, 1, "b")], 1)))


@B
def kill_order(procs, root):
    out = []
    def visit(pid):
        kids = sorted(p for p, pp, _ in procs if pp == pid)
        for k in kids:
            visit(k)
        out.append(pid)
    visit(root)
    return out


@O
def kill_order(procs, root):
    kids = defaultdict(list)
    for p, pp, _ in procs:
        kids[pp].append(p)
    def visit(pid):
        for k in sorted(kids[pid]):
            yield from visit(k)
        yield pid
    return list(visit(root))


Q(None, "SIGTERM, Then SIGKILL", "Easy", "Graceful shutdown",
  "On shutdown, each process gets SIGTERM and has <code>grace</code> seconds to finish (Docker and Kubernetes default to 10 and 30). A process needing longer is killed with SIGKILL and loses its in-flight work. Given shutdown times, return <code>(exited cleanly, killed)</code> as sorted name lists.",
  [(({"web": 2.5, "worker": 45.0, "scheduler": 0.4, "exporter": 10.0, "consumer": 12.0}, 10), (['exporter', 'scheduler', 'web'], ['consumer', 'worker']))],
  ("A loop.", "O(n log n)", "O(n)"),
  ("Two comprehensions.", "O(n log n)", "O(n)"),
  viz=(({"a": 1.0, "b": 20.0}, 10)))


@B
def shutdown(times, grace):
    clean, killed = [], []
    for name, t in times.items():
        if t <= grace:
            clean.append(name)
        else:
            killed.append(name)
    return (sorted(clean), sorted(killed))


@O
def shutdown(times, grace):
    return (sorted(n for n, t in times.items() if t <= grace), sorted(n for n, t in times.items() if t > grace))


Q(None, "Disk Space Alerts", "Easy", "df -h",
  "Rows are <code>(filesystem, mount, size_gb, used_gb)</code>. Return <code>(mount, use%)</code> rounded to whole percent for filesystems at or above <code>warn</code>%, highest first, marking each <code>'CRIT'</code> if at or above <code>crit</code>% else <code>'WARN'</code>.",
  [(([("/dev/nvme0n1p2", "/", 100, 61), ("/dev/nvme1n1", "/data", 2000, 1910), ("tmpfs", "/run", 8, 0.1), ("/dev/sdb1", "/var/log", 50, 42.5), ("/dev/sdc1", "/backup", 4000, 3200)], 80, 90), [('/data', 96, 'CRIT'), ('/var/log', 85, 'WARN'), ('/backup', 80, 'WARN')])],
  ("Compute and filter in a loop, then sort.", "O(n log n)", "O(n)"),
  ("A sorted comprehension.", "O(n log n)", "O(n)"),
  viz=(([("d", "/", 10, 9)], 80, 90)))


@B
def disk_alerts(rows, warn, crit):
    out = []
    for _, mount, size, used in rows:
        pct = round(used / size * 100)
        if pct >= warn:
            out.append((mount, pct, "CRIT" if pct >= crit else "WARN"))
    out.sort(key=lambda r: -r[1])
    return out


@O
def disk_alerts(rows, warn, crit):
    pcts = [(m, round(100 * u / s)) for _, m, s, u in rows]
    return sorted(((m, p, "CRIT" if p >= crit else "WARN") for m, p in pcts if p >= warn), key=lambda r: -r[1])


Q(None, "Split a Command Line Like the Shell", "Medium", "Quotes and escapes",
  "Split each command into arguments the way a POSIX shell does: spaces separate arguments, single quotes keep everything literal, double quotes keep spaces but allow <code>\\\\\"</code>, and a backslash outside quotes escapes the next character. The optimal answer is <code>shlex.split</code>.",
  [((["git commit -m 'fix: handle empty cart'", "grep -r \"TODO: later\" src/", "echo it\\'s fine", "python -c \"print(\\\"hi\\\")\"", "cp my\\ file.txt  'backup dir/'"],), [['git', 'commit', '-m', 'fix: handle empty cart'], ['grep', '-r', 'TODO: later', 'src/'], ['echo', "it's", 'fine'], ['python', '-c', 'print("hi")'], ['cp', 'my file.txt', 'backup dir/']])],
  ("A small state machine.", "O(n · L)", "O(L)"),
  ("<code>shlex.split</code>.", "O(n · L)", "O(L)"),
  viz=((["a 'b c'"],)))


@B
def split_command(lines):
    out = []
    for s in lines:
        args, cur, i, quote, started = [], "", 0, None, False
        while i < len(s):
            c = s[i]
            if quote == "'":
                if c == "'":
                    quote = None
                else:
                    cur += c
            elif quote == '"':
                if c == "\\" and i + 1 < len(s) and s[i + 1] in '"\\$`':
                    cur += s[i + 1]
                    i += 1
                elif c == '"':
                    quote = None
                else:
                    cur += c
            elif c == "\\" and i + 1 < len(s):
                cur += s[i + 1]
                started = True
                i += 1
            elif c in "'\"":
                quote, started = c, True
            elif c.isspace():
                if started:
                    args.append(cur)
                cur, started = "", False
            else:
                cur += c
                started = True
            i += 1
        if started:
            args.append(cur)
        out.append(args)
    return out


@O
def split_command(lines):
    return [shlex.split(s) for s in lines]
