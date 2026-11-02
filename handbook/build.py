"""Run every solution against its tests, record the optimal solution's trace,
and write the site data (data/*.js) plus handbook/README.md.

    python3 handbook/build.py            # all topics
    python3 handbook/build.py arrays     # only topics whose id contains "arrays"
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


def _result_text(q, args):
    try:
        out = repr(run(q, q["opt"], args))
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
    for kind, file in (("topic", path), ("lessons", ROOT / "src" / "lessons" / path.name), ("theory", ROOT / "src" / "theory" / path.name)):
        if not file.exists():
            continue
        spec = importlib.util.spec_from_file_location(f"{kind}_{path.stem}", file)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod  # inspect needs this to find class sources
        spec.loader.exec_module(mod)
    return dict(lib.REG)


def build_topic(path, failures):
    reg = load(path)
    meta = reg["topic"]
    out = {"id": meta["id"], "theory": meta["theory"], "qs": {}}
    if reg["demo"]:
        code = lib.start_trace(reg["demo"])
        reg["demo"]()
        out["demo"] = {"code": code, "frames": lib.stop_trace(), "title": meta.get("demo_title", "")}
    out["sections"], out["faq"] = reg["theory"], reg["faq"]
    by_lc = {q["lc"]: slug(q["title"]) for q in reg["questions"]}
    out["lessons"] = []
    for k, les in enumerate(reg["lessons"], 1):
        item = {"level": les["level"], "title": les["title"], "body": les["body"], "practice": []}
        for lc in les["practice"]:
            if lc in by_lc:
                item["practice"].append(by_lc[lc])
            else:
                failures.append(f"{meta['id']} lesson {k}: practice LC {lc} is not a question in this topic")
        if les["demo"]:
            code = lib.start_trace(les["demo"])
            try:
                les["demo"]()
            except Exception as e:  # noqa: BLE001
                failures.append(f"{meta['id']} lesson {k} demo: {type(e).__name__}: {e}")
            item["demo"] = {"code": code, "frames": lib.stop_trace()}
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
        opt_code = lib.start_trace(q["opt"])
        try:
            run(q, q["opt"], viz_args)
        except Exception as e:  # noqa: BLE001
            failures.append(f"{where} [trace] {type(e).__name__}: {e}")
        frames = lib.stop_trace()
        if frames:
            frames.append({"m": f"Result: {_result_text(q, viz_args)}", "l": -1, "v": frames[-1]["v"]})
        if not frames:
            failures.append(f"{where}: optimal solution recorded no frames")
        (bi, bt, bs), (oi, ot, os_) = q["brute_meta"], q["opt_meta"]
        out["qs"][qid] = {
            "statement": q["statement"],
            "examples": [[fmt_args(q, a), repr(w)] for a, w in q["tests"][:3]],
            "vizIn": fmt_args(q, viz_args),
            "brute": {"idea": bi, "tc": bt, "sc": bs, "code": lib._code(q["brute"])[0]},
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
    lines = [
        "# DSA Interview Handbook",
        "",
        f"{len(topics)} topics · theory with {sum(t['faq'] for t in topics)} theory questions · {sum(t['lessons'] for t in topics)} lessons from basics to advanced · {total} most-asked interview questions · Python · brute force and optimal solution for each, with a step-by-step animation of the optimal one.",
        "",
        "**Live site:** https://abpandey-dev.github.io/python-dsa-visualizer/handbook/",
        "",
        "Every solution is run against its test cases by `build.py` before the site is generated, and each animation is recorded from a real run of the code you see.",
        "",
        "## Topics",
        "",
    ]
    for t in topics:
        lines.append(f"- [{t['title']}](#{slug(t['title'])}) — {t['blurb']}")
    for t in topics:
        lines += ["", f"## {t['title']}", "", "| # | Question | LeetCode | Level | Pattern |", "|---|---|---|---|---|"]
        for q in t["qs"]:
            link = f"https://abpandey-dev.github.io/python-dsa-visualizer/handbook/#/q/{t['id']}/{q['id']}"
            lc = f"[{q['lc']}](https://leetcode.com/problems/{slug(q['title'])}/)" if isinstance(q["lc"], int) else str(q["lc"])
            lines.append(f"| {q['n']} | [{q['title']}]({link}) | {lc} | {q['diff']} | {q['tags']} |")
    lines += [
        "",
        "## Build",
        "",
        "```bash",
        "python3 handbook/build.py",
        "```",
        "",
        "Solutions live in `handbook/src/topics/`. Lines starting with `T(` record a frame of the animation and are hidden from the code shown on the site.",
        "",
    ]
    return "\n".join(lines)


def stamp_assets():
    """Add ?v=<content hash> to the page's asset links so browsers never serve stale files."""
    page = ROOT / "index.html"
    html = page.read_text()
    for name in ("style.css", "app.js", "data/index.js"):
        v = hashlib.sha1((ROOT / name).read_bytes()).hexdigest()[:10]
        html = re.sub(re.escape(name) + r'(\?v=\w+)?"', f'{name}?v={v}"', html)
    page.write_text(html)


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    DATA.mkdir(exist_ok=True)
    failures, topics = [], []
    for path in sorted((ROOT / "src" / "topics").glob("*.py")):
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
        (ROOT / "README.md").write_text(readme(topics))
        stamp_assets()
    if failures:
        print(f"\n{len(failures)} FAILURES")
        for f in failures:
            print("  " + f[:400])
        sys.exit(1)
    print("\nAll tests passed.")


if __name__ == "__main__":
    main()
