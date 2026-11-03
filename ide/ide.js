/* Python IDE: CodeMirror editor + Pyodide worker. Opened with #p=<base64 JSON>
   ({title, code, back, check: {name, tests, listify, design}}) from the course and handbook pages. */
(function () {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } },
  };

  const EXAMPLES = {
    "Hello and input": `name = input("What's your name? ")\nage = int(input("How old are you? "))\nprint(f"Hi {name}! Next year you'll be {age + 1}.")\n`,
    "Loop and list": `marks = [72, 45, 90, 38]\ntotal = 0\nfor m in marks:\n    total += m\n    if m >= 40:\n        print(m, "pass")\n    else:\n        print(m, "fail")\nprint("average:", total / len(marks))\n`,
    "Dictionary counting": `text = "to be or not to be"\ncounts = {}\nfor word in text.split():\n    counts[word] = counts.get(word, 0) + 1\nprint(counts)\n`,
    "Recursion": `def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n\nprint(factorial(5))\n`,
    "Class and objects": `class BankAccount:\n    def __init__(self, owner, balance=0):\n        self.owner = owner\n        self.balance = balance\n\n    def deposit(self, amount):\n        self.balance += amount\n\nacc = BankAccount("Ana", 100)\nacc.deposit(50)\nprint(acc.owner, acc.balance)\n`,
    "Handling errors": `values = ["10", "abc", "7"]\nfor v in values:\n    try:\n        print(int(v) * 2)\n    except ValueError:\n        print(v, "is not a number")\n`,
  };
  const WELCOME = `# Welcome! Write Python here and press ▶ Run (Ctrl/⌘ + Enter).\n# Press ⏯ Visualize to watch it run one line at a time.\n\n${EXAMPLES["Loop and list"]}`;

  /* ---------- payload from the URL ---------- */
  function decode(s) {
    try {
      const b64 = s.replace(/-/g, "+").replace(/_/g, "/");
      return JSON.parse(decodeURIComponent(escape(atob(b64))));
    } catch (e) { return null; }
  }
  function encode(obj) {
    return btoa(unescape(encodeURIComponent(JSON.stringify(obj)))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  }
  const m = location.hash.match(/p=([^&]+)/);
  const payload = (m && decode(m[1])) || { title: "", code: null };
  const saveKey = "ide-code:" + (payload.title || "scratch");
  const startCode = payload.code || WELCOME;

  if (payload.title) { $("title").textContent = payload.title; document.title = payload.title + " · Python IDE"; }
  if (payload.back) { $("back").href = payload.back; $("back").hidden = false; }
  if (payload.check && payload.check.tests && payload.check.tests.length) {
    $("check").hidden = false;
    document.querySelector('[data-tab="tests"]').hidden = false;
  }

  /* ---------- editor ---------- */
  const editor = CodeMirror.fromTextArea($("code"), {
    mode: "python", lineNumbers: true, indentUnit: 4, tabSize: 4, indentWithTabs: false,
    matchBrackets: true, autoCloseBrackets: true, autofocus: true, lineWrapping: false,
    extraKeys: {
      Tab: (cm) => (cm.somethingSelected() ? cm.indentSelection("add") : cm.replaceSelection("    ", "end")),
      "Shift-Tab": (cm) => cm.indentSelection("subtract"),
      "Cmd-/": "toggleComment", "Ctrl-/": "toggleComment",
      "Ctrl-Enter": () => go("run"), "Cmd-Enter": () => go("run"),
      "Shift-Ctrl-Enter": () => go("trace"), "Shift-Cmd-Enter": () => go("trace"),
    },
  });
  editor.setValue(store.get(saveKey) || startCode);
  editor.on("change", () => { store.set(saveKey, editor.getValue()); clearMarks(); });
  let marked = [];
  function clearMarks() { marked.forEach((l) => editor.removeLineClass(l, "background", "error-line")); marked = []; }
  function markLine(n) { if (n == null) return; const l = editor.addLineClass(n - 1, "background", "error-line"); marked.push(l); editor.scrollIntoView({ line: n - 1, ch: 0 }, 80); }

  const sel = $("examples");
  Object.keys(EXAMPLES).forEach((k) => sel.insertAdjacentHTML("beforeend", `<option>${esc(k)}</option>`));
  sel.addEventListener("change", () => { if (sel.value) { editor.setValue(EXAMPLES[sel.value]); sel.value = ""; editor.focus(); } });
  $("reset").addEventListener("click", () => { editor.setValue(startCode); editor.focus(); });
  $("share").addEventListener("click", async () => {
    const url = location.href.split("#")[0] + "#p=" + encode({ ...payload, code: editor.getValue() });
    try { await navigator.clipboard.writeText(url); setStatus("Link copied to the clipboard"); }
    catch (e) { prompt("Copy this link:", url); }
  });

  /* ---------- tabs ---------- */
  function showTab(k) {
    document.querySelectorAll(".ide-tabs [data-tab]").forEach((b) => b.setAttribute("aria-selected", b.dataset.tab === k));
    document.querySelectorAll(".panel").forEach((p) => { p.hidden = p.dataset.panel !== k; });
  }
  document.querySelector(".ide-tabs").addEventListener("click", (e) => { const b = e.target.closest("[data-tab]"); if (b) showTab(b.dataset.tab); });

  /* ---------- worker ---------- */
  let worker, ready = false, busy = false, seq = 0;
  const status = $("status");
  function setStatus(text, spinning) { status.textContent = text; status.classList.toggle("busy", !!spinning); }
  function setBusy(on) {
    busy = on;
    ["run", "viz", "check"].forEach((id) => { $(id).disabled = on || !ready; });
    $("stop").hidden = !on;
  }
  function startWorker() {
    ready = false;
    setBusy(false);
    setStatus("Loading Python… (first visit downloads about 10 MB)", true);
    worker = new Worker("worker.js");
    worker.onmessage = (e) => {
      const d = e.data;
      if (d.type === "ready") { ready = true; setBusy(false); setStatus(`Python ${d.version} ready`); }
      else if (d.type === "fatal") setStatus("Couldn't load Python: " + d.error);
      else if (d.type === "result" && d.id === seq) { setBusy(false); show(d.cmd, d.result); }
    };
  }
  startWorker();
  $("stop").addEventListener("click", () => {
    worker.terminate();
    setBusy(false);
    $("out").innerHTML = `<span class="err">Stopped.</span> <span class="meta">(Python restarts — an infinite loop? Check that your loop condition eventually becomes False.)</span>`;
    showTab("out");
    startWorker();
  });

  function go(cmd) {
    if (!ready || busy) return;
    clearMarks();
    seq += 1;
    setBusy(true);
    setStatus(cmd === "trace" ? "Recording every step…" : cmd === "check" ? "Running the tests…" : "Running…", true);
    worker.postMessage({ id: seq, cmd, code: editor.getValue(), stdin: $("stdin").value, payload: payload.check });
  }
  $("run").addEventListener("click", () => go("run"));
  $("viz").addEventListener("click", () => go("trace"));
  $("check").addEventListener("click", () => go("check"));

  /* ---------- results ---------- */
  function errorHtml(r) {
    if (!r.error) return "";
    return `\n<span class="err">${esc(r.error)}${r.line ? ` (line ${r.line})` : ""}</span>` + (r.hint ? `\n<span class="hint">Hint: ${esc(r.hint)}</span>` : "");
  }
  function show(cmd, r) {
    setStatus(r.error ? "Finished with an error" : "Done");
    const out = $("out");
    out.innerHTML = (r.out ? esc(r.out) : r.error ? "" : '<span class="meta">(the program printed nothing)</span>') + errorHtml(r);
    if (r.line) markLine(r.line);
    if (cmd === "trace") {
      const panel = document.querySelector('[data-panel="viz"]');
      panel.replaceChildren();
      if (!r.frames || !r.frames.length) {
        panel.innerHTML = `<p class="empty-v">Nothing to show${r.error ? " — fix the error first (see Output)" : ""}.</p>`;
      } else {
        if (r.truncated) panel.insertAdjacentHTML("beforeend", `<p class="empty-v">Showing the first ${r.frames.length} steps.</p>`);
        let cur = null;
        const p = DSA_PLAYER.player({
          code: null, frames: r.frames,
          onStep: (f) => {
            if (cur != null) editor.removeLineClass(cur, "background", "CodeMirror-activeline-background");
            if (f.l >= 0) { cur = f.l; editor.addLineClass(cur, "background", "CodeMirror-activeline-background"); editor.scrollIntoView({ line: cur, ch: 0 }, 80); }
          },
        });
        panel.appendChild(p);
      }
      showTab("viz");
      return;
    }
    if (cmd === "check") {
      const panel = document.querySelector('[data-panel="tests"]');
      const tests = r.tests || [];
      const passed = tests.filter((t) => t.ok).length;
      panel.innerHTML = r.error && !tests.length
        ? `<p class="test-sum fail">Couldn't run the tests</p><pre class="console">${esc(r.error)}${r.line ? ` (line ${r.line})` : ""}${r.hint ? "\n" + esc(r.hint) : ""}</pre>`
        : `<p class="test-sum ${passed === tests.length ? "pass" : "fail"}">${passed === tests.length ? "🎉 All tests passed" : `${passed} of ${tests.length} tests passed`}</p>` +
          tests.map((t) => `<div class="test ${t.ok ? "ok" : "no"}"><b>${t.ok ? "✓" : "✗"}</b> ${esc(t.call)}<br>expected ${esc(t.want)}<br>got&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${esc(t.got)}</div>`).join("");
      showTab("tests");
      return;
    }
    showTab("out");
  }
  const style = document.createElement("style");
  style.textContent = ".CodeMirror-activeline-background{background:var(--code-line)!important;box-shadow:inset 3px 0 0 var(--hot)}";
  document.head.appendChild(style);
})();
