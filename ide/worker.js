/* Runs Python (Pyodide) off the main thread so a stuck program can be stopped by terminating the worker. */
importScripts("https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js");

const ready = (async () => {
  const py = await loadPyodide();
  const src = await (await fetch("runner.py")).text();
  py.runPython(src);
  postMessage({ type: "ready", version: py.runPython("import sys; sys.version.split()[0]") });
  return py;
})().catch((err) => postMessage({ type: "fatal", error: String(err) }));

onmessage = async (e) => {
  const py = await ready;
  if (!py) return;
  const { id, cmd, code, stdin, payload } = e.data;
  try {
    const text = cmd === "check"
      ? py.globals.get("check_code")(code, stdin || "", JSON.stringify(payload))
      : py.globals.get("execute")(code, stdin || "", cmd === "trace");
    postMessage({ type: "result", id, cmd, result: JSON.parse(text) });
  } catch (err) {
    postMessage({ type: "result", id, cmd, result: { out: "", error: String(err), frames: [] } });
  }
};
