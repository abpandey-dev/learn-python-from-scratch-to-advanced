"""Build the industry projects: data files, notebooks with checked milestones, and the index.

    python3 projects/build_projects.py            # build everything
    python3 projects/build_projects.py verify     # also execute every notebook, with and without the solutions

Each project lives in projects/specs/pNN_*.py and defines:
    make_data(rng) -> {"file.csv": DataFrame, ...}
    PROJECT = dict(slug, title, role, level, hours, skills, brief, deliverable, data_notes,
                   setup, milestones=[dict(title, task, starter, solution, call, tol, hint)], extra_cells,
                   present, resume, interview, extensions)
The expected answer for each milestone is computed here by running the solutions in order,
so the numbers in the notebook always match the data that ships with it.
"""
import importlib.util
import json
import math
import os
import re
import sys
import textwrap
from pathlib import Path

import nbformat as nbf
import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
REPO = "abpandey-dev/learn-python-from-scratch-to-advanced"
RAW = f"https://raw.githubusercontent.com/{REPO}/main/projects/data/"
SITE = f"https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced"


def colab(name):
    return f"https://colab.research.google.com/github/{REPO}/blob/main/projects/{name}"


HELPERS = r'''
import math, os, warnings
from pathlib import Path
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
RAW = "__RAW__"


def load(name):
    """Read a project data file: from the local data/ folder if it is there, otherwise from GitHub."""
    local = Path("data") / name
    return pd.read_csv(local if local.exists() else RAW + name)


def _plain(x):
    if isinstance(x, pd.DataFrame):
        return {str(c): _plain(x[c].tolist()) for c in x.columns}
    if isinstance(x, pd.Series):
        return {_plain(k): _plain(v) for k, v in x.items()}
    if isinstance(x, np.ndarray):
        return _plain(x.tolist())
    if isinstance(x, np.generic):
        return _plain(x.item())
    if isinstance(x, (list, tuple)):
        return [_plain(v) for v in x]
    if isinstance(x, dict):
        return {_plain(k): _plain(v) for k, v in x.items()}
    return x


def _same(a, b, tol):
    if isinstance(b, bool) or isinstance(a, bool):
        return a == b
    if isinstance(b, (int, float)) and isinstance(a, (int, float)):
        return math.isclose(a, b, rel_tol=tol, abs_tol=tol if tol > 1e-3 else 1e-6)
    if isinstance(b, list) and isinstance(a, list):
        return len(a) == len(b) and all(_same(x, y, tol) for x, y in zip(a, b))
    if isinstance(b, dict) and isinstance(a, dict):
        return set(map(str, a)) == set(map(str, b)) and all(_same(a[k], b[k], tol) for k in a if k in b)
    return a == b


def _why(a, b):
    if a is None:
        return "your function returned None — finish the code and return the result."
    if type(a) != type(b) and not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        return f"expected a {type(b).__name__}, got a {type(a).__name__}."
    if isinstance(b, (list, dict)) and len(a) != len(b):
        return f"expected {len(b)} items, got {len(a)}."
    if isinstance(b, dict) and set(map(str, a)) != set(map(str, b)):
        return f"the keys should be {sorted(map(str, b))[:8]}."
    return "the values are not right yet. Re-read the task and the hints."


def check(name, fn, want, tol=1e-3):
    """Run your code for one milestone and compare it with the expected answer."""
    try:
        got = _plain(fn())
    except NotImplementedError:
        print(f"⬜ {name}: not started yet.")
        return
    except Exception as e:
        print(f"❌ {name}: your code raised {type(e).__name__}: {e}")
        return
    if _same(got, want, tol):
        print(f"✅ {name}: correct!")
        return
    print(f"❌ {name}: not yet — {_why(got, want)}")
'''


def load_spec(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def plain(x):
    """The same conversion the notebook's checker uses, applied here to the reference answers."""
    import pandas as pd
    if isinstance(x, pd.DataFrame):
        return {str(c): plain(x[c].tolist()) for c in x.columns}
    if isinstance(x, pd.Series):
        return {plain(k): plain(v) for k, v in x.items()}
    if isinstance(x, np.ndarray):
        return plain(x.tolist())
    if isinstance(x, np.generic):
        return plain(x.item())
    if isinstance(x, (list, tuple)):
        return [plain(v) for v in x]
    if isinstance(x, dict):
        return {plain(k): plain(v) for k, v in x.items()}
    if isinstance(x, float):
        return round(x, 6)
    return x


def md(text):
    return nbf.v4.new_markdown_cell(textwrap.dedent(text).strip())


def code(text):
    return nbf.v4.new_code_cell(textwrap.dedent(text).strip())


def details(summary, body):
    return f"<details>\n<summary><b>{summary}</b></summary>\n\n{body}\n\n</details>"


def fence(src):
    return f"```python\n{textwrap.dedent(src).strip()}\n```"


def expected_answers(spec):
    """Run the setup and every solution in one namespace; evaluate each milestone's call."""
    ns = {"__name__": "__main__"}
    cwd = os.getcwd()
    os.chdir(HERE)
    try:
        exec(HELPERS.replace("__RAW__", RAW), ns)
        exec(textwrap.dedent(spec.PROJECT["setup"]), ns)
        wants = []
        for m in spec.PROJECT["milestones"]:
            exec(textwrap.dedent(m["solution"]), ns)
            wants.append(plain(eval(m["call"], ns)))
        for c in spec.PROJECT.get("extra_code", []):
            exec(textwrap.dedent(c), ns)
        import matplotlib.pyplot as plt
        plt.close("all")
    finally:
        os.chdir(cwd)
    return wants


def notebook(spec, number, wants, solved=False):
    P = spec.PROJECT
    name = f"{number:02d}_{P['slug']}.ipynb"
    header = "\n\n".join([
        f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab(name)})",
        f"*Industry Project {number} of {TOTAL} · {P['role']} · {P['level']} · about {P['hours']} hours*",
        f"# {P['title']}",
        textwrap.dedent(P["brief"]).strip(),
        f"**What you'll hand in:** {' '.join(P['deliverable'].split())}",
        f"**Skills:** {', '.join(P['skills'])}",
        "**How this works:** each milestone has a task, a code cell for you to finish, and a ✅ check. Hints and a "
        "reference solution are hidden until you open them. Try for at least 20 minutes before opening the solution "
        "— the struggle is where the learning happens.",
    ])
    cells = [nbf.v4.new_markdown_cell(header)]
    cells.append(md("## The data\n\n" + textwrap.dedent(P["data_notes"]).strip()))
    cells.append(code("# ▶ Run this cell first: it loads the libraries, the data and the checker.\n"
                      + HELPERS.replace("__RAW__", RAW).strip() + "\n\n" + textwrap.dedent(P["setup"]).strip()
                      + '\nprint("Ready! Data loaded.")'))
    for c in P.get("explore", []):
        cells.append(md(c[0]) if c[1] is None else md(c[0]))
        if c[1]:
            cells.append(code(c[1]))
    for i, (m, want) in enumerate(zip(P["milestones"], wants), 1):
        cells.append(md(f"## Milestone {i}: {m['title']}\n\n" + textwrap.dedent(m["task"]).strip()
                        + ("\n\n" + details("💡 Hint", textwrap.dedent(m["hint"]).strip()) if m.get("hint") else "")))
        cells.append(code(m["solution"] if solved else m["starter"]))
        tol = m.get("tol", 1e-3)
        cells.append(code(f"check({json.dumps(m['title'])}, lambda: {m['call']}, {want!r}, tol={tol})"))
        cells.append(md(details("🔑 Reference solution (open after you've tried)", fence(m["solution"]))
                        + ("\n\n" + m["after"].strip() if m.get("after") else "")))
    for c in P.get("extra", []):
        cells.append(md(c[0]))
        if c[1]:
            cells.append(code(c[1]))
    cells.append(md("## Present your work\n\n" + textwrap.dedent(P["present"]).strip()))
    cells.append(md("## Put it on your resume\n\nWrite bullets with **your own numbers** from the milestones above. A template:\n\n"
                    + "\n".join(f"- {b}" for b in P["resume"])
                    + "\n\nOnly claim what you built and measured. Put the notebook on your GitHub with a short README: problem, data, approach, results, what you'd do next."))
    cells.append(md("## Interview questions about this project\n\nPractise answering these out loud in 1–2 minutes each:\n\n"
                    + "\n".join(f"{k}. {q}" for k, q in enumerate(P["interview"], 1))))
    cells.append(md("## Take it further\n\n" + "\n".join(f"- {e}" for e in P["extensions"])))
    nb = nbf.v4.new_notebook(cells=cells)
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nb.metadata["colab"] = {"provenance": []}
    return name, nb


def specs():
    files = sorted((HERE / "specs").glob("p[0-9][0-9]_*.py"))
    return [load_spec(f) for f in files]


def main():
    global TOTAL
    sys.path.insert(0, str(HERE / "specs"))
    DATA.mkdir(exist_ok=True)
    all_specs = specs()
    TOTAL = len(all_specs)
    built = []
    for number, spec in enumerate(all_specs, 1):
        rng = np.random.default_rng(1000 + number)
        for fname, frame in spec.make_data(rng).items():
            frame.to_csv(DATA / fname, index=False)
        wants = expected_answers(spec)
        name, nb = notebook(spec, number, wants)
        nbf.write(nb, HERE / name)
        built.append((number, name, spec.PROJECT, wants))
        print(f"{name}: {len(wants)} milestones")
    write_readme(built)
    write_page(built)
    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        verify(all_specs, built)


def write_readme(built):
    lines = ["# Industry Projects", "",
             "Eight end-to-end projects that turn the courses into portfolio work, each modelled on a real job task. "
             "Every project has a business brief, realistic data, 6–8 milestones whose answers are **checked automatically**, "
             "hints, a hidden reference solution, how to present it, resume bullets and the interview questions you'll be asked about it.", "",
             f"**Web page:** {SITE}/projects/", "",
             "| # | Project | Role | Level | Hours | Skills | Open |", "|---|---|---|---|---|---|---|"]
    for number, name, P, wants in built:
        lines.append(f"| {number} | [{P['title']}]({name}) | {P['role']} | {P['level']} | {P['hours']} | {', '.join(P['skills'][:5])} | "
                     f"[Colab]({colab(name)}) |")
    lines += ["", "## How to do a project", "",
              "1. Open it in Colab (nothing to install) or run it locally with Jupyter.",
              "2. Run the first cell, read the brief, then work milestone by milestone. Each ✅ check tells you when you're right.",
              "3. Write the short report at the end in your own words, and publish the notebook on your GitHub.", "",
              "Suggested order: projects 1–2 after **Python for Data Science**, 3–6 after **Machine Learning**, 7 after the **MLOps** topic and 8 after **Deep Learning & LLMs**.", "",
              "## Rebuild", "", "```bash", "python3 projects/build_projects.py verify", "```", "",
              "The data is synthetic but realistic, generated with fixed seeds and saved in [data/](data/), so every learner gets the same numbers."]
    (HERE / "README.md").write_text("\n".join(lines) + "\n")


def write_page(built):
    import html
    cards = []
    for number, name, P, wants in built:
        cards.append(f'''    <article class="card">
      <p class="meta">Project {number} · {html.escape(P['role'])} · {P['level']} · ~{P['hours']} h</p>
      <h2>{html.escape(P['title'])}</h2>
      <p>{html.escape(P['summary'])}</p>
      <p class="skills">{" ".join(f"<span>{html.escape(s)}</span>" for s in P['skills'])}</p>
      <p class="links"><a href="{colab(name)}">Open in Colab →</a> <a href="https://github.com/{REPO}/blob/main/projects/{name}">View on GitHub</a></p>
    </article>''')
    page = (HERE / "page_template.html").read_text().replace("<!--CARDS-->", "\n".join(cards))
    (HERE / "index.html").write_text(page)


def verify(all_specs, built):
    from nbclient import NotebookClient
    import copy
    bad = 0
    for spec, (number, name, P, wants) in zip(all_specs, built):
        for solved in (False, True):
            _, nb = notebook(spec, number, wants, solved=solved)
            NotebookClient(nb, timeout=600, kernel_name="python3", allow_errors=False,
                           resources={"metadata": {"path": str(HERE)}}).execute()
            text = "\n".join(o.get("text", "") for c in nb.cells if c.cell_type == "code" for o in c.get("outputs", []))
            ok, no = text.count("✅"), text.count("❌")
            todo = text.count("⬜")
            expect_ok = len(wants) if solved else 0
            status = "OK" if (ok == expect_ok and no == 0 and (solved or todo == len(wants))) else "PROBLEM"
            bad += status != "OK"
            print(f"{name} [{'solved' if solved else 'learner'}]: ✅ {ok}  ❌ {no}  ⬜ {todo}  -> {status}")
            if solved:
                nbf.write(nb, HERE / name.replace(".ipynb", ".solved-check.ipynb")) if status != "OK" else None
    print("verify:", "all good" if not bad else f"{bad} problems")


TOTAL = 0

if __name__ == "__main__":
    main()
