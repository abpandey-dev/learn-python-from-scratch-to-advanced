"""Shared helpers for handbook topic files.

A topic file calls Q(...) once per question, then decorates a brute-force
function with @B and an optimal one with @O. Lines that start with `T(` are
trace calls: build.py runs the optimal solution once with tracing on, records a
frame per T() call, and strips those lines from the code shown on the site.
"""
import inspect
import math
import sys
import textwrap

REG = {"topic": None, "questions": [], "demo": None}
MAX_FRAMES = 90


# ---------- data structures used by list / tree problems ----------

class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def mk_list(vals, pos=-1):
    """Build a linked list; pos >= 0 links the tail back to that index (a cycle)."""
    dummy = cur = ListNode()
    nodes = []
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
        nodes.append(cur)
    if pos >= 0 and nodes:
        nodes[-1].next = nodes[pos]
    return dummy.next


def list_arr(head):
    out, seen = [], set()
    while head and id(head) not in seen:
        seen.add(id(head))
        out.append(head.val)
        head = head.next
    return out


def mk_tree(vals):
    """Level-order list with None for gaps, LeetCode style."""
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue, i = [root], 1
    while queue and i < len(vals):
        node = queue.pop(0)
        for side in ("left", "right"):
            if i < len(vals) and vals[i] is not None:
                child = TreeNode(vals[i])
                setattr(node, side, child)
                queue.append(child)
            i += 1
    return root


def tree_arr(root):
    out, queue = [], [root]
    while queue:
        node = queue.pop(0)
        if node:
            out.append(node.val)
            queue += [node.left, node.right]
        else:
            out.append(None)
    while out and out[-1] is None:
        out.pop()
    return out


def find(root, val):
    if not root or root.val == val:
        return root
    return find(root.left, val) or find(root.right, val)


# ---------- registration ----------

def TOPIC(**kw):
    REG["topic"] = kw


def Q(lc, title, diff, tags, statement, tests, brute, opt, **kw):
    """brute/opt are (idea, time, space). Optional kw: prep, post, norm, check,
    viz (args for the visual run), design (tests are (ctor_args, [(method, args)]))."""
    q = dict(lc=lc, title=title, diff=diff, tags=tags, statement=statement,
             tests=tests, brute_meta=brute, opt_meta=opt, **kw)
    REG["questions"].append(q)
    return q


def _code(fn):
    src = textwrap.dedent(inspect.getsource(fn)).rstrip("\n").split("\n")
    kept, raw_to_kept = [], {}
    for i, line in enumerate(src):
        s = line.strip()
        if s.startswith("T(") or s in ("@B", "@O", "@D"):
            continue
        raw_to_kept[i] = len(kept)
        kept.append(line)
    first = fn.__code__.co_firstlineno if hasattr(fn, "__code__") else inspect.getsourcelines(fn)[1]
    return "\n".join(kept), raw_to_kept, first, len(src)


def B(fn):
    REG["questions"][-1]["brute"] = fn
    return fn


def O(fn):
    REG["questions"][-1]["opt"] = fn
    return fn


def D(fn):
    """Topic concept demo: a small traced function shown with the theory."""
    REG["demo"] = fn
    return fn


# ---------- tracing ----------

class _Trace:
    on = False
    frames = []
    first = 0
    raw_to_kept = {}
    nraw = 0
    file = None


def start_trace(fn):
    code, raw_to_kept, first, nraw = _code(fn)
    _Trace.on, _Trace.frames = True, []
    _Trace.first, _Trace.raw_to_kept, _Trace.nraw = first, raw_to_kept, nraw
    _Trace.file = inspect.getsourcefile(fn)
    return code


def stop_trace():
    _Trace.on = False
    return _Trace.frames


def T(msg, *views, at="next"):
    if not _Trace.on or len(_Trace.frames) >= MAX_FRAMES:
        return
    f = sys._getframe(1)
    line = -1
    if f.f_code.co_filename == _Trace.file:
        raw = f.f_lineno - _Trace.first
        if 0 <= raw < _Trace.nraw:
            for step in ((1, -1) if at == "next" else (-1, 1)):
                r = raw
                while 0 <= r < _Trace.nraw and r not in _Trace.raw_to_kept:
                    r += step
                line = _Trace.raw_to_kept.get(r, -1)
                if line > 0:
                    break
    _Trace.frames.append({"m": msg, "l": line, "v": [v for v in views if v]})


# ---------- view builders (each returns a JSON-ready dict) ----------

def s(x):
    """Short display string for a cell value."""
    if x is None:
        return "None"
    if isinstance(x, bool):
        return "T" if x else "F"
    if isinstance(x, float):
        if math.isinf(x):
            return "∞" if x > 0 else "-∞"
        return f"{x:.4g}"
    if isinstance(x, str):
        return x
    if isinstance(x, (list, tuple)):
        return "[" + ",".join(s(y) for y in x) + "]"
    if isinstance(x, ListNode):
        return f"node({x.val})"
    if isinstance(x, TreeNode):
        return f"node({x.val})"
    return str(x)


def _idx(xs):
    if xs is None:
        return []
    if isinstance(xs, (int,)):
        return [xs]
    return [i for i in xs if i is not None]


def A(name, arr, /, hl=(), ok=(), bad=(), **ptrs):
    """Array / string row. ptrs: label=index (None hides the pointer)."""
    return {"k": "arr", "n": name, "v": [s(x) for x in arr],
            "p": {k: v for k, v in ptrs.items() if isinstance(v, int) and not isinstance(v, bool)},
            "hl": _idx(hl), "ok": _idx(ok), "bad": _idx(bad)}


def V(**kw):
    return {"k": "vars", "v": [[k, s(v)] for k, v in kw.items()]}


def M(name, d, hl=None):
    if isinstance(d, dict):
        items = [[s(k), s(v)] for k, v in d.items()]
    else:
        items = [[s(k), None] for k in d]
    return {"k": "map", "n": name, "v": items, "hl": None if hl is None else s(hl)}


def S(name, st, hl=()):
    return {"k": "stack", "n": name, "v": [s(x) for x in st], "hl": _idx(hl)}


def G(name, grid, hl=(), ok=(), bad=(), rl=None, cl=None):
    cells = lambda xs: [[r, c] for r, c in (xs or [])]
    return {"k": "grid", "n": name, "v": [[s(x) for x in row] for row in grid],
            "hl": cells(hl), "ok": cells(ok), "bad": cells(bad),
            "rl": None if rl is None else [s(x) for x in rl],
            "cl": None if cl is None else [s(x) for x in cl]}


def L(name, head, /, hl=(), **ptrs):
    nodes, index, cur = [], {}, head
    while cur and id(cur) not in index and len(nodes) < 30:
        index[id(cur)] = len(nodes)
        nodes.append(cur)
        cur = cur.next
    cyc = index.get(id(cur), -1) if cur else -1
    p = {}
    for k, node in ptrs.items():
        if node is not None and id(node) in index:
            p[k] = index[id(node)]
    hl_ids = [index[id(n)] for n in (hl or []) if n is not None and id(n) in index]
    return {"k": "list", "n": name, "v": [s(n.val) for n in nodes], "p": p, "cyc": cyc, "hl": hl_ids}


def TR(name, root, /, hl=(), ok=(), **ptrs):
    nodes, index = [], {}

    def walk(n):
        if not n or id(n) in index:
            return
        index[id(n)] = len(nodes)
        nodes.append(n)
        walk(n.left)
        walk(n.right)

    walk(root)

    def ids(xs):
        out = []
        for x in xs or []:
            if isinstance(x, TreeNode):
                if id(x) in index:
                    out.append(index[id(x)])
            else:
                out += [i for i, n in enumerate(nodes) if n.val == x]
        return out

    return {"k": "tree", "n": name,
            "v": [[s(n.val), index.get(id(n.left), -1) if n.left else -1,
                   index.get(id(n.right), -1) if n.right else -1] for n in nodes],
            "hl": ids(hl), "ok": ids(ok),
            "p": {k: index[id(n)] for k, n in ptrs.items() if n is not None and id(n) in index}}


def GR(name, nodes, edges, hl=(), ok=(), he=(), directed=False):
    """Graph. nodes: count or list of labels; edges: (u, v) or (u, v, w)."""
    labels = list(range(nodes)) if isinstance(nodes, int) else list(nodes)
    pos = {lab: i for i, lab in enumerate(labels)}
    es = []
    for e in edges:
        es.append([pos[e[0]], pos[e[1]], s(e[2]) if len(e) > 2 else None])
    hes = {(pos[a], pos[b]) for a, b, *_ in (he or [])}
    return {"k": "graph", "n": name, "v": [s(x) for x in labels], "e": es, "d": directed,
            "hl": [pos[x] for x in hl or [] if x in pos], "ok": [pos[x] for x in ok or [] if x in pos],
            "he": [list(x) for x in hes]}


def H(name, heap, hl=()):
    """A binary heap (list) drawn as the complete tree it represents. hl: heap indices."""
    nodes = [TreeNode(s(v)) for v in heap]
    for i, n in enumerate(nodes):
        if 2 * i + 1 < len(nodes):
            n.left = nodes[2 * i + 1]
        if 2 * i + 2 < len(nodes):
            n.right = nodes[2 * i + 2]
    view = TR(name, nodes[0] if nodes else None, hl=[nodes[i] for i in _idx(hl) if 0 <= i < len(nodes)])
    return view


__all__ = ["ListNode", "TreeNode", "mk_list", "list_arr", "mk_tree", "tree_arr", "find",
           "TOPIC", "Q", "B", "O", "D", "T", "A", "V", "M", "S", "G", "L", "TR", "GR", "H", "math"]
