"""Build behavioural/README.md and behavioural/index.html from content.py.

    python3 behavioural/build_guide.py
"""
import html
import json
import re
from pathlib import Path

from content import LEAD, QUESTIONS, ROLE_QUESTIONS, SECTIONS, TITLE

HERE = Path(__file__).resolve().parent
SITE = "https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced"


# ---------- a small Markdown → HTML converter for the subset content.py uses ----------

def inline(text):
    t = html.escape(text, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*([^*]+)\*(?![\w*])", r"<i>\1</i>", t)
    return t


def md_to_html(md):
    out, lines, i = [], md.strip().split("\n"), 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
        elif line.startswith("### "):
            out.append(f"<h3>{inline(line[4:])}</h3>")
            i += 1
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip("|").split("|")])
                i += 1
            head, body = rows[0], [r for r in rows[2:]]
            out.append('<div class="table"><table><thead><tr>' + "".join(f"<th>{inline(c)}</th>" for c in head)
                       + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
                       + "</tbody></table></div>")
        elif line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(lines[i][2:])
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
        elif re.match(r"\d+\. ", line):
            items = []
            while i < len(lines) and re.match(r"\d+\. ", lines[i]):
                items.append(re.sub(r"^\d+\. ", "", lines[i]))
                i += 1
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>")
        elif line.startswith("> "):
            quote = []
            while i < len(lines) and lines[i].startswith("> "):
                quote.append(lines[i][2:])
                i += 1
            out.append(f"<blockquote>{inline(' '.join(quote))}</blockquote>")
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not re.match(r"(### |\||- |\d+\. |> )", lines[i]):
                para.append(lines[i])
                i += 1
            out.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(out)


# ---------- README.md ----------

def build_readme():
    n = sum(len(v) for v in QUESTIONS.values()) + sum(len(v) for v in ROLE_QUESTIONS.values())
    md = [f"# {TITLE}", "", LEAD, "",
          f"**Web page with a timed practice drill:** {SITE}/behavioural/", "",
          "## Contents", ""]
    md += [f"- [{title}](#{re.sub(r'[^a-z0-9 -]', '', title.lower()).replace(' ', '-')})" for _, title, _ in SECTIONS]
    md += ["- [Question bank](#question-bank)", ""]
    for _, title, body in SECTIONS:
        md += [f"## {title}", "", body.strip(), ""]
    md += ["## Question bank", "", f"{n} questions, grouped by what they test. For each: what the interviewer is really asking, and what a strong answer includes.", ""]
    for theme, qs in QUESTIONS.items():
        md += [f"### {theme}", "", "| Question | They're really asking | A strong answer includes |", "|---|---|---|"]
        md += [f"| {q} | {a} | {s} |" for q, a, s in qs]
        md.append("")
    md += ["### By role", ""]
    for role, qs in ROLE_QUESTIONS.items():
        md += [f"**{role}**", ""] + [f"- {q}" for q in qs] + [""]
    md += ["---", "", "Edit `content.py` and run `python3 behavioural/build_guide.py` to rebuild this page and the website."]
    (HERE / "README.md").write_text("\n".join(md) + "\n")
    return n


# ---------- index.html ----------

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Behavioural Interviews · Learn Python</title>
<meta name="description" content="How behavioural interviews are scored, the STAR method, a story bank, a question bank and a timed practice drill.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,800&family=JetBrains+Mono:wght@600&display=swap">
<style>
:root {
  --paper: #EEF2F5; --grid: rgba(20, 60, 110, 0.06); --surface: #FFFFFF; --sunk: #F5F8FA;
  --ink: #14213A; --muted: #586980; --line: #D3DCE5; --accent: #0F766E; --chip: #E3F1EF; --warn: #B45309;
  color-scheme: light;
}
@media (prefers-color-scheme: dark) {
  :root { --paper: #0D141C; --grid: rgba(140, 180, 230, 0.05); --surface: #151F2B; --sunk: #111A24; --ink: #E4ECF4; --muted: #93A3B7; --line: #26354A; --accent: #3CC2B4; --chip: #1B2F33; --warn: #F0A85A; color-scheme: dark; }
}
* { box-sizing: border-box; }
body { margin: 0; color: var(--ink); font: 16px/1.65 "Atkinson Hyperlegible", "Segoe UI", system-ui, sans-serif;
  background-color: var(--paper);
  background-image: linear-gradient(var(--grid) 1px, transparent 1px), linear-gradient(90deg, var(--grid) 1px, transparent 1px);
  background-size: 24px 24px; }
main { max-width: 860px; margin: 0 auto; display: flex; flex-direction: column; gap: 22px; padding-block: 48px 80px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
a { color: var(--accent); }
.back { font: 600 13px "JetBrains Mono", ui-monospace, monospace; text-decoration: none; }
.eyebrow { font: 600 12px/1 "JetBrains Mono", ui-monospace, monospace; letter-spacing: 0.12em; text-transform: uppercase; color: var(--accent); margin: 0; }
h1 { font: 800 clamp(2.2rem, 6vw, 3.2rem)/1.05 "Bricolage Grotesque", system-ui, sans-serif; letter-spacing: -0.02em; margin: 0; text-wrap: balance; }
h2 { font: 800 1.6rem/1.2 "Bricolage Grotesque", system-ui, sans-serif; margin: 0 0 6px; }
h3 { font: 800 1.15rem/1.3 "Bricolage Grotesque", system-ui, sans-serif; margin: 18px 0 4px; }
p { margin: 8px 0; }
.lead { color: var(--muted); max-width: 66ch; margin: 0; }
.toc { display: flex; flex-wrap: wrap; gap: 8px; }
.toc a, .chip { font-size: 13.5px; padding: 4px 10px; border-radius: 999px; background: var(--chip); color: var(--ink); text-decoration: none; border: 1px solid transparent; cursor: pointer; font-family: inherit; }
.chip[aria-pressed="true"] { border-color: var(--accent); color: var(--accent); }
section { background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 20px 22px; scroll-margin-top: 16px; }
.table { overflow-x: auto; margin: 10px 0; }
table { border-collapse: collapse; width: 100%; font-size: 14.5px; }
th, td { text-align: left; vertical-align: top; padding: 7px 10px; border-bottom: 1px solid var(--line); }
th { font-weight: 700; background: var(--sunk); }
blockquote { margin: 12px 0; padding: 12px 16px; border-left: 3px solid var(--accent); background: var(--sunk); border-radius: 0 10px 10px 0; }
code { font: 600 0.9em "JetBrains Mono", ui-monospace, monospace; }
ul, ol { padding-left: 1.3em; margin: 8px 0; }
li { margin: 4px 0; }
details { border-bottom: 1px solid var(--line); padding: 8px 0; }
details:last-child { border-bottom: 0; }
summary { cursor: pointer; font-weight: 700; }
details dl { margin: 8px 0 4px; display: grid; grid-template-columns: max-content 1fr; gap: 4px 12px; font-size: 14.5px; }
dt { color: var(--muted); }
dd { margin: 0; }
.drill { border: 2px solid var(--accent); }
.qbox { font: 800 clamp(1.25rem, 3.5vw, 1.6rem)/1.3 "Bricolage Grotesque", system-ui, sans-serif; margin: 12px 0; min-height: 2.6em; }
.hint { color: var(--muted); font-size: 14.5px; }
.row { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
button.btn { font: 700 14.5px "Atkinson Hyperlegible", system-ui, sans-serif; padding: 8px 14px; border-radius: 10px; border: 1px solid var(--line); background: var(--sunk); color: var(--ink); cursor: pointer; }
button.btn.primary { background: var(--accent); border-color: var(--accent); color: var(--surface); }
.timer { font: 600 1.6rem "JetBrains Mono", ui-monospace, monospace; min-width: 4.5ch; }
.timer.over { color: var(--warn); }
.checks { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 6px 14px; margin: 12px 0; font-size: 14.5px; }
.checks label { display: flex; gap: 8px; align-items: flex-start; cursor: pointer; }
select, textarea { font: inherit; color: var(--ink); background: var(--sunk); border: 1px solid var(--line); border-radius: 10px; padding: 7px 10px; }
textarea { width: 100%; min-height: 110px; resize: vertical; }
.score { font-weight: 700; }
</style>
</head>
<body>
<main>
  <a class="back" href="../">← All courses</a>
  <p class="eyebrow">Interview prep · Behavioural</p>
  <h1>Behavioural Interviews</h1>
  <p class="lead">__LEAD__</p>
  <nav class="toc" aria-label="Contents">__TOC__<a href="#bank-q">Question bank</a><a href="#drill">Practice drill</a></nav>
__SECTIONS__
  <section id="bank-q">
    <h2>Question bank</h2>
    <p class="hint">__N__ questions grouped by what they test. Open one to see what the interviewer is really asking and what a strong answer includes.</p>
    <div class="row" id="filters" role="group" aria-label="Filter by theme"></div>
    <div id="qlist"></div>
    <h3>By role</h3>
    __ROLES__
  </section>
  <section id="drill" class="drill">
    <h2>Practice drill</h2>
    <p class="hint">Get a random question, start the 2-minute timer and answer <b>out loud</b> using one of your stories. Then tick what your answer had. Notes are saved in this browser only.</p>
    <div class="row">
      <label for="pool">Questions from</label>
      <select id="pool"></select>
      <button class="btn primary" id="next" type="button">New question</button>
    </div>
    <div class="qbox" id="q" aria-live="polite">Press “New question” to start.</div>
    <div class="row">
      <span class="timer" id="timer" role="timer" aria-live="off">2:00</span>
      <button class="btn" id="start" type="button">Start timer</button>
      <button class="btn" id="reset" type="button">Reset</button>
    </div>
    <div class="checks" id="checks"></div>
    <p class="score" id="score"></p>
    <label for="notes" class="hint">Your story for this question (title, numbers, what you'd improve)</label>
    <textarea id="notes" placeholder="e.g. Release automation — 1 day → 45 min, hotfixes 30% → 8%. Next time: say the trade-off earlier."></textarea>
  </section>
</main>
<script>
const QUESTIONS = __QUESTIONS__;
const ROLES = __ROLE_DATA__;
const CHECKS = ["Situation set in 1–2 sentences", "My task and why it mattered", "Actions in my own words (“I”, not “we”)",
  "A decision or trade-off explained", "A result with a number", "What I learned or would change", "Under about 2 minutes", "Ended cleanly and let them ask"];
const store = { get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
                set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };
const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

/* question bank with theme filters */
const filters = document.getElementById("filters"), qlist = document.getElementById("qlist");
let theme = "All";
function renderBank() {
  qlist.innerHTML = Object.entries(QUESTIONS).filter(([t]) => theme === "All" || t === theme).map(([t, qs]) =>
    `<h3>${esc(t)}</h3>` + qs.map(([q, a, s]) => `<details><summary>${esc(q)}</summary><dl><dt>They're asking</dt><dd>${esc(a)}</dd><dt>Strong answer</dt><dd>${esc(s)}</dd></dl></details>`).join("")).join("");
  filters.querySelectorAll(".chip").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.t === theme)));
}
["All", ...Object.keys(QUESTIONS)].forEach((t) => {
  const b = document.createElement("button");
  b.type = "button"; b.className = "chip"; b.dataset.t = t; b.textContent = t;
  b.addEventListener("click", () => { theme = t; renderBank(); });
  filters.appendChild(b);
});
renderBank();

/* practice drill */
const pool = document.getElementById("pool");
const pools = { "Any theme": Object.values(QUESTIONS).flat().map((x) => x[0]) };
Object.entries(QUESTIONS).forEach(([t, qs]) => { pools[t] = qs.map((x) => x[0]); });
Object.entries(ROLES).forEach(([r, qs]) => { pools["Role: " + r] = qs; });
Object.keys(pools).forEach((k) => { const o = document.createElement("option"); o.textContent = k; pool.appendChild(o); });
const saved = store.get("bq-pool"); if (saved && pools[saved]) pool.value = saved;
pool.addEventListener("change", () => store.set("bq-pool", pool.value));

const qEl = document.getElementById("q"), notes = document.getElementById("notes"), checks = document.getElementById("checks"), score = document.getElementById("score");
let current = null, last = null;
checks.innerHTML = CHECKS.map((c, i) => `<label><input type="checkbox" data-i="${i}"> <span>${esc(c)}</span></label>`).join("");
function updateScore() {
  const n = checks.querySelectorAll("input:checked").length;
  score.textContent = current ? `${n} / ${CHECKS.length}` + (n === CHECKS.length ? " — strong answer. Try it again tomorrow from memory." : n >= 5 ? " — good. Fix the unticked parts and say it again." : " — say it again, focusing on the unticked parts.") : "";
}
checks.addEventListener("change", updateScore);
function next() {
  const list = pools[pool.value];
  let q; do { q = list[Math.floor(Math.random() * list.length)]; } while (list.length > 1 && q === last);
  current = last = q; qEl.textContent = q;
  checks.querySelectorAll("input").forEach((x) => { x.checked = false; });
  notes.value = store.get("bq-note:" + q) || "";
  resetTimer(); updateScore();
}
document.getElementById("next").addEventListener("click", next);
notes.addEventListener("input", () => { if (current) store.set("bq-note:" + current, notes.value); });

const timerEl = document.getElementById("timer"), startBtn = document.getElementById("start");
let left = 120, tick = null;
function show() { const m = Math.floor(Math.abs(left) / 60), s = Math.abs(left) % 60; timerEl.textContent = (left < 0 ? "+" : "") + m + ":" + String(s).padStart(2, "0"); timerEl.classList.toggle("over", left < 0); }
function resetTimer() { clearInterval(tick); tick = null; left = 120; startBtn.textContent = "Start timer"; show(); }
startBtn.addEventListener("click", () => {
  if (tick) { clearInterval(tick); tick = null; startBtn.textContent = "Resume"; return; }
  startBtn.textContent = "Pause"; tick = setInterval(() => { left -= 1; show(); }, 1000);
});
document.getElementById("reset").addEventListener("click", resetTimer);
</script>
</body>
</html>
"""


def build_page(n):
    toc = "".join(f'<a href="#{sid}">{html.escape(title)}</a>' for sid, title, _ in SECTIONS)
    sections = "\n".join(f'  <section id="{sid}">\n    <h2>{html.escape(title)}</h2>\n{md_to_html(body)}\n  </section>' for sid, title, body in SECTIONS)
    roles = "".join(f"<p><b>{html.escape(r)}</b></p><ul>" + "".join(f"<li>{html.escape(q)}</li>" for q in qs) + "</ul>" for r, qs in ROLE_QUESTIONS.items())
    page = (PAGE.replace("__LEAD__", inline(LEAD)).replace("__TOC__", toc).replace("__SECTIONS__", sections)
            .replace("__N__", str(n)).replace("__ROLES__", roles)
            .replace("__QUESTIONS__", json.dumps(QUESTIONS, ensure_ascii=False))
            .replace("__ROLE_DATA__", json.dumps(ROLE_QUESTIONS, ensure_ascii=False)))
    (HERE / "index.html").write_text(page)


if __name__ == "__main__":
    total = build_readme()
    build_page(total)
    print(f"built README.md and index.html: {len(SECTIONS)} sections, {total} questions")
