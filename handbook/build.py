"""Run every solution against its tests, record the animations, and write a
site's data (data/*.js) and README.md. A site ("book") is a folder with
book.json, index.html and src/{topics,lessons,theory}/.

    python3 handbook/build.py                          # the DSA handbook
    python3 handbook/build.py --book python-course     # the Python course
    python3 handbook/build.py arrays                   # only topics whose file name contains "arrays"
"""
import copy
import hashlib
import importlib.util
import inspect
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
import lib  # noqa: E402

BOOK = ROOT          # set by main() from --book
CONF = {}
DATA = ROOT / "data"


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower().replace("'", "")).strip("-")


def run(q, fn, args):
    if "runner" in q:
        return q["runner"](fn, copy.deepcopy(args))
    if q.get("design"):
        ctor, ops = copy.deepcopy(args)
        obj = fn(*ctor)
        return [getattr(obj, m)(*a) for m, a in ops]
    if hasattr(fn, "__globals__"):
        fn.__globals__[fn.__name__] = fn  # recursive calls by name hit this version
    a = copy.deepcopy(args)
    if "prep" in q:
        a = q["prep"](a)
    res = fn(*a)
    if "inplace" in q:
        res = a[q["inplace"]]
    if "post" in q:
        res = q["post"](res)
    return res


def _result_text(q, args, kind="opt"):
    try:
        out = repr(run(q, q[kind], args))
    except Exception:  # noqa: BLE001
        return "(see above)"
    return out if len(out) <= 160 else out[:157] + "..."


def passes(q, args, want, got):
    if "check" in q:
        return q["check"](copy.deepcopy(args), got)
    norm = q.get("norm", lambda x: x)
    return norm(copy.deepcopy(got)) == norm(copy.deepcopy(want))


def fmt_args(q, args):
    if q.get("design"):
        ctor, ops = args
        calls = [f"{type_name(q)}({', '.join(map(repr, ctor))})"]
        calls += [f"{m}({', '.join(map(repr, a))})" for m, a in ops]
        return " → ".join(calls)
    names = q.get("names") or list(inspect.signature(q["opt"]).parameters)
    return ", ".join(f"{n} = {v!r}" for n, v in zip(names, args))


def type_name(q):
    return q["opt"].__name__


def load(path):
    lib.REG.update(topic=None, questions=[], demo=None, lessons=[], theory=[], faq=[])
    for kind, file in (("topic", path), ("lessons", BOOK / "src" / "lessons" / path.name), ("theory", BOOK / "src" / "theory" / path.name)):
        if not file.exists():
            continue
        spec = importlib.util.spec_from_file_location(f"{kind}_{path.stem}", file)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod  # inspect needs this to find class sources
        spec.loader.exec_module(mod)
    return dict(lib.REG)


def trace(fn, call):
    """Frames from T() calls if the code has them, otherwise an automatic line-by-line trace."""
    if lib.uses_T(fn):
        code = lib.start_trace(fn)
        try:
            call()
        finally:
            frames = lib.stop_trace()
        return code, frames
    code, frames, _ = lib.auto_trace(fn, call)
    return code, frames


def build_topic(path, failures):
    reg = load(path)
    meta = reg["topic"]
    out = {"id": meta["id"], "theory": meta["theory"], "qs": {}}
    if reg["demo"]:
        code, frames = trace(reg["demo"], reg["demo"])
        out["demo"] = {"code": code, "frames": frames, "title": meta.get("demo_title", "")}
    out["sections"], out["faq"] = reg["theory"], reg["faq"]
    by_lc = {q["lc"]: slug(q["title"]) for q in reg["questions"]}
    out["lessons"] = []
    for k, les in enumerate(reg["lessons"], 1):
        item = {"level": les["level"], "title": les["title"], "body": les["body"], "practice": []}
        qids = {slug(q["title"]) for q in reg["questions"]}
        for ref in les["practice"]:
            qid = slug(ref) if isinstance(ref, str) else by_lc.get(ref)
            if qid in qids:
                item["practice"].append(qid)
            else:
                failures.append(f"{meta['id']} lesson {k}: practice {ref!r} is not a question in this topic")
        if les["demo"]:
            code, frames = lib._code(les["demo"])[0], []
            try:
                code, frames = trace(les["demo"], les["demo"])
            except Exception as e:  # noqa: BLE001
                failures.append(f"{meta['id']} lesson {k} demo: {type(e).__name__}: {e}")
            item["demo"] = {"code": code, "frames": frames}
            if not item["demo"]["frames"]:
                failures.append(f"{meta['id']} lesson {k} demo recorded no frames")
        out["lessons"].append(item)
    index = []
    seen = set()
    for n, q in enumerate(reg["questions"], 1):
        qid = slug(q["title"])
        assert qid not in seen, qid
        seen.add(qid)
        where = f"{meta['id']}/{qid}"
        if "brute" not in q or "opt" not in q:
            failures.append(f"{where}: missing @B or @O")
            continue
        times = {}
        for kind in ("brute", "opt"):
            t0 = time.perf_counter()
            for args, want in q["tests"]:
                try:
                    got = run(q, q[kind], args)
                    ok = passes(q, args, want, got)
                except Exception as e:  # noqa: BLE001
                    got, ok = f"{type(e).__name__}: {e}", False
                if not ok:
                    failures.append(f"{where} [{kind}] args={args!r} want={want!r} got={got!r}")
            times[kind] = time.perf_counter() - t0
        viz_args = q.get("viz", q["tests"][0][0])
        traced = {}
        for kind in ("opt", "brute") if CONF.get("trace_brute") else ("opt",):
            code, frames = lib._code(q[kind])[0], []
            try:
                code, frames = trace(q[kind], lambda: run(q, q[kind], viz_args))
            except Exception as e:  # noqa: BLE001
                failures.append(f"{where} [{kind} trace] {type(e).__name__}: {e}")
            if frames:
                frames.append({"m": f"Result: {_result_text(q, viz_args, kind)}", "l": -1, "v": frames[-1]["v"]})
            else:
                failures.append(f"{where}: {kind} solution recorded no frames")
            traced[kind] = (code, frames)
        opt_code, frames = traced["opt"]
        (bi, bt, bs), (oi, ot, os_) = q["brute_meta"], q["opt_meta"]
        out["qs"][qid] = {
            "statement": q["statement"],
            "examples": [[fmt_args(q, a), repr(w)] for a, w in q["tests"][:3]],
            "vizIn": fmt_args(q, viz_args),
            "brute": {"idea": bi, "tc": bt, "sc": bs, "code": traced["brute"][0] if "brute" in traced else lib._code(q["brute"])[0],
                      **({"frames": traced["brute"][1]} if "brute" in traced else {})},
            "opt": {"idea": oi, "tc": ot, "sc": os_, "code": opt_code, "frames": frames},
            "tests": len(q["tests"]),
        }
        index.append({"id": qid, "n": n, "lc": q["lc"], "title": q["title"], "diff": q["diff"], "tags": q["tags"]})
    topic_index = {k: meta[k] for k in ("id", "title", "blurb", "glyph")}
    topic_index["lessons"] = len(out["lessons"])
    topic_index["faq"] = len(out["faq"])
    topic_index["qs"] = index
    return out, topic_index


def readme(topics):
    total = sum(len(t["qs"]) for t in topics)
    url = CONF["url"]
    has_lc = any(isinstance(q["lc"], int) for t in topics for q in t["qs"])
    counts = (f"{len(topics)} topics · theory with {sum(t['faq'] for t in topics)} theory questions · "
              f"{sum(t['lessons'] for t in topics)} lessons from basics to advanced · {total} {CONF['unit']}")
    lines = [f"# {CONF['title']}", "", counts + " · " + CONF["summary"], "", f"**Live site:** {url}", "",
             "Every solution is run against its test cases by `build.py` before the site is generated, and each animation is recorded from a real run of the code you see.",
             "", "## Topics", ""]
    for t in topics:
        lines.append(f"- [{t['title']}](#{slug(t['title'])}) — {t['blurb']}")
    for t in topics:
        head = "| # | Question | LeetCode | Level | Pattern |" if has_lc else "| # | Question | Level | Concept |"
        lines += ["", f"## {t['title']}", "", head, "|---|---|---|---|---|" if has_lc else "|---|---|---|---|"]
        for q in t["qs"]:
            link = f"{url}#/q/{t['id']}/{q['id']}"
            if has_lc:
                lc = f"[{q['lc']}](https://leetcode.com/problems/{slug(q['title'])}/)" if isinstance(q["lc"], int) else str(q["lc"])
                lines.append(f"| {q['n']} | [{q['title']}]({link}) | {lc} | {q['diff']} | {q['tags']} |")
            else:
                lines.append(f"| {q['n']} | [{q['title']}]({link}) | {q['diff']} | {q['tags']} |")
    rel = BOOK.relative_to(ROOT.parent)
    lines += ["", "## Build", "", "```bash", f"python3 handbook/build.py{'' if BOOK == ROOT else ' --book ' + str(rel)}", "```", "",
              f"Sources live in `{rel}/src/`: `topics/` (questions and solutions), `lessons/` and `theory/`.", ""]
    return "\n".join(lines)


def stamp_assets():
    """Add ?v=<content hash> to the page's local script and style links so browsers never serve stale files."""
    page = BOOK / "index.html"
    html = page.read_text()

    def stamp(m):
        name = m.group(2)
        v = hashlib.sha1((BOOK / name).read_bytes()).hexdigest()[:10]
        return f'{m.group(1)}="{name}?v={v}"'
    html = re.sub(r'(src|href)="((?!https?:)[^"?#]+\.(?:js|css))(?:\?v=\w+)?"', stamp, html)
    page.write_text(html)


def main():
    global BOOK, DATA, CONF
    args = sys.argv[1:]
    if "--book" in args:
        i = args.index("--book")
        BOOK = (ROOT.parent / args[i + 1]).resolve()
        del args[i:i + 2]
    DATA = BOOK / "data"
    CONF = json.loads((BOOK / "book.json").read_text())
    only = args[0] if args else None
    DATA.mkdir(exist_ok=True)
    failures, topics = [], []
    for path in sorted((BOOK / "src" / "topics").glob("*.py")):
        if only and only not in path.stem:
            continue
        data, idx = build_topic(path, failures)
        topics.append(idx)
        js = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        (DATA / f"{data['id']}.js").write_text(f"(window.DSA_TOPIC=window.DSA_TOPIC||{{}})[{json.dumps(data['id'])}]={js};\n")
        frames = sum(len(q["opt"]["frames"]) for q in data["qs"].values())
        print(f"{idx['title']:<28} {len(idx['qs']):>3} questions  {frames:>5} frames")
    if not only:
        version = hashlib.sha1(b"".join(f.read_bytes() for f in sorted(DATA.glob("*.js")) if f.name != "index.js")).hexdigest()[:10]
        (DATA / "index.js").write_text(f"window.DSA_VERSION={json.dumps(version)};window.DSA_INDEX=" + json.dumps(topics, ensure_ascii=False, separators=(",", ":")) + ";\n")
        (BOOK / "README.md").write_text(readme(topics))
        stamp_assets()
    if failures:
        print(f"\n{len(failures)} FAILURES")
        for f in failures:
            print("  " + f[:400])
        sys.exit(1)
    print("\nAll tests passed.")


if __name__ == "__main__":
    main()
