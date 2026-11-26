from lib import *
import base64
import math
import numpy as np
from functools import lru_cache


TOPIC(
    id="multimodal", title="Multimodal AI: Images, Documents & Speech", glyph="◐",
    blurb="Build with images, PDFs and audio: how images become tokens and what they cost, resizing and patches, sending images to an API, document AI (reading order, tables, field validation, page routing), speech (framing, chunking, WER, subtitles), CLIP-style zero-shot labels, voice-agent latency and video frames.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">tokens ≈ width × height / 750                 # Claude's documented estimate for an image
patches = ⌈H / p⌉ × ⌈W / p⌉                     # a vision transformer splits the image into p×p patches
{"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": b64}}
frames = 1 + (n_samples − win) // hop          # audio: 25 ms windows every 10 ms
WER = (substitutions + deletions + insertions) / words in reference</code></pre>
""")


Q(None, "What Does an Image Cost?", "Easy", "Image tokens",
  "Using the estimate tokens ≈ width × height / 750 (rounded up), return tokens and dollars for each image size at <code>price</code> per million input tokens (dollars rounded to 4).",
  [(([(1092, 1092), (800, 600), (200, 200)], 3.0), [(1590, 0.0048), (640, 0.0019), (54, 0.0002)])],
  ("A loop.", "O(n)", "O(n)"),
  ("A comprehension with <code>math.ceil</code>.", "O(n)", "O(n)"),
  viz=(([(1092, 1092), (800, 600)], 3.0)))


@B
def image_cost(sizes, price):
    out = []
    for w, h in sizes:
        t = w * h // 750
        if w * h % 750:
            t += 1
        out.append((t, round(t * price / 1e6, 4)))
    return out


@O
def image_cost(sizes, price):
    return [(t, round(t * price / 1e6, 4)) for t in (math.ceil(w * h / 750) for w, h in sizes)]


Q(None, "Resize Before Sending", "Easy", "Keep the aspect ratio",
  "Large images get downscaled by the API anyway (and cost more to upload). Shrink so the long edge is at most <code>max_edge</code>, keeping the aspect ratio (round down); smaller images stay as they are.",
  [(((4032, 3024), 1568), (1568, 1176)), (((1000, 3000), 1568), (522, 1568)), (((640, 480), 1568), (640, 480))],
  ("Compute the scale with an if.", "O(1)", "O(1)"),
  ("Integer arithmetic <code>v * max_edge // long_edge</code> avoids floating-point rounding surprises.", "O(1)", "O(1)"),
  viz=(((4032, 3024), 1568)))


@B
def resize(size, max_edge):
    w, h = size
    long_edge = w if w > h else h
    if long_edge <= max_edge:
        return (w, h)
    return (w * max_edge // long_edge, h * max_edge // long_edge)


@O
def resize(size, max_edge):
    long_edge = max(size)
    return size if long_edge <= max_edge else tuple(v * max_edge // long_edge for v in size)


Q(None, "How Many Patches?", "Easy", "Vision transformers",
  "A vision transformer splits an image into p×p patches (padding the edges). Return <code>(patches, patches after resizing to <code>target</code>×<code>target</code>)</code>.",
  [(((224, 224), 16, 224), (196, 196)), (((1000, 750), 14, 336), (3888, 576))],
  ("Ceiling division by hand.", "O(1)", "O(1)"),
  ("<code>math.ceil</code>.", "O(1)", "O(1)"),
  viz=(((1000, 750), 14, 336)))


@B
def patches(size, p, target):
    w, h = size
    cols = w // p + (1 if w % p else 0)
    rows = h // p + (1 if h % p else 0)
    t = target // p + (1 if target % p else 0)
    return (cols * rows, t * t)


@O
def patches(size, p, target):
    return (math.ceil(size[0] / p) * math.ceil(size[1] / p), math.ceil(target / p) ** 2)


IMG = np.arange(36).reshape(6, 6).tolist()


Q(None, "Cut an Image Into Patch Vectors", "Medium", "From pixels to tokens",
  "Split an H×W grey image (H, W divisible by p) into p×p patches, row by row, and flatten each into a vector. Return <code>(number of patches, the first two patch vectors)</code>.",
  [((IMG, 3), (4, [[0, 1, 2, 6, 7, 8, 12, 13, 14], [3, 4, 5, 9, 10, 11, 15, 16, 17]])), ((IMG, 2), (9, [[0, 1, 6, 7], [2, 3, 8, 9]]))],
  ("Nested loops over patch positions and pixels.", "O(H·W)", "O(H·W)"),
  ("NumPy reshape + transpose: (H/p, p, W/p, p) → (H/p, W/p, p, p).", "O(H·W)", "O(H·W)"),
  viz=((IMG, 3)))


@B
def to_patches(img, p):
    out = []
    for r in range(0, len(img), p):
        for c in range(0, len(img[0]), p):
            vec = []
            for i in range(p):
                for j in range(p):
                    vec.append(img[r + i][c + j])
            out.append(vec)
    return (len(out), out[:2])


@O
def to_patches(img, p):
    a = np.array(img)
    H, W = a.shape
    v = a.reshape(H // p, p, W // p, p).transpose(0, 2, 1, 3).reshape(-1, p * p)
    return (len(v), v[:2].tolist())


Q(None, "Normalise Pixels", "Easy", "Model input preprocessing",
  "Scale RGB pixels from 0–255 to 0–1, then normalise each channel with the given mean and std. Return the normalised pixels rounded to 3.",
  [(([[255, 128, 0], [10, 200, 90]], [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]), [[2.249, 0.205, -1.804], [-1.947, 1.466, -0.236]])],
  ("Loops over pixels and channels.", "O(n)", "O(n)"),
  ("NumPy broadcasting.", "O(n)", "O(n)"),
  viz=(([[255, 128, 0]], [0.485, 0.456, 0.406], [0.229, 0.224, 0.225])))


@B
def normalise(pixels, mean, std):
    out = []
    for px in pixels:
        out.append([round((px[c] / 255 - mean[c]) / std[c], 3) for c in range(3)])
    return out


@O
def normalise(pixels, mean, std):
    return np.round((np.array(pixels) / 255 - np.array(mean)) / np.array(std), 3).tolist()


Q(None, "Build an Image Content Block", "Easy", "Sending images to the API",
  "Return the Claude API image content block for a file: base64-encode the bytes, and set <code>media_type</code> from the extension (.png, .jpg/.jpeg, .gif, .webp). Unsupported types return None.",
  [(("chart.png", b"\x89PNG..."), {'type': 'image', 'source': {'type': 'base64', 'media_type': 'image/png', 'data': 'iVBORy4uLg=='}}), (("photo.JPG", b"\xff\xd8\xff"), {'type': 'image', 'source': {'type': 'base64', 'media_type': 'image/jpeg', 'data': '/9j/'}}), (("scan.tiff", b"II*"), None)],
  ("An if-chain on the lower-cased extension.", "O(n)", "O(n)"),
  ("A dict lookup.", "O(n)", "O(n)"),
  viz=(("chart.png", b"\x89PNG...")))


@B
def image_block(name, data):
    ext = name.lower().rsplit(".", 1)[-1]
    if ext == "png":
        mt = "image/png"
    elif ext in ("jpg", "jpeg"):
        mt = "image/jpeg"
    elif ext == "gif":
        mt = "image/gif"
    elif ext == "webp":
        mt = "image/webp"
    else:
        return None
    return {"type": "image", "source": {"type": "base64", "media_type": mt, "data": base64.b64encode(data).decode()}}


@O
def image_block(name, data):
    types = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "gif": "image/gif", "webp": "image/webp"}
    mt = types.get(name.lower().rsplit(".", 1)[-1])
    return {"type": "image", "source": {"type": "base64", "media_type": mt, "data": base64.b64encode(data).decode()}} if mt else None


Q(None, "Slice Audio Into Frames", "Easy", "Speech features",
  "Audio at <code>sr</code> samples per second is analysed in windows of <code>win_ms</code> milliseconds every <code>hop_ms</code>. Return <code>(samples, duration in seconds rounded to 2, number of full frames)</code> for <code>n_samples</code>.",
  [((16000, 48000, 25, 10), (48000, 3.0, 298)), ((16000, 300, 25, 10), (300, 0.02, 0))],
  ("Convert ms to samples, then count frames with a loop.", "O(frames)", "O(1)"),
  ("Closed form 1 + (n − win) // hop.", "O(1)", "O(1)"),
  viz=((16000, 48000, 25, 10)))


@B
def frames(sr, n_samples, win_ms, hop_ms):
    win, hop = sr * win_ms // 1000, sr * hop_ms // 1000
    count, start = 0, 0
    while start + win <= n_samples:
        count += 1
        start += hop
    return (n_samples, round(n_samples / sr, 2), count)


@O
def frames(sr, n_samples, win_ms, hop_ms):
    win, hop = sr * win_ms // 1000, sr * hop_ms // 1000
    return (n_samples, round(n_samples / sr, 2), max(0, 1 + (n_samples - win) // hop))


Q(None, "Chunk Long Audio for Transcription", "Medium", "Overlapping windows",
  "Speech models accept limited lengths. Split <code>duration</code> seconds into chunks of <code>chunk</code> seconds that overlap by <code>overlap</code> seconds (so words at the edges aren't cut). Return <code>(start, end)</code> pairs; the last chunk ends at the duration.",
  [((70, 30, 5), [(0, 30), (25, 55), (50, 70)]), ((25, 30, 5), [(0, 25)])],
  ("A while loop stepping by chunk − overlap.", "O(c)", "O(c)"),
  ("<code>range</code> with the step, clipped at the end.", "O(c)", "O(c)"),
  viz=((70, 30, 5)))


@B
def audio_chunks(duration, chunk, overlap):
    out, start = [], 0
    while True:
        end = start + chunk
        if end >= duration:
            out.append((start, duration))
            break
        out.append((start, end))
        start = end - overlap
    return out


@O
def audio_chunks(duration, chunk, overlap):
    out = []
    for start in range(0, duration, chunk - overlap):
        out.append((start, min(start + chunk, duration)))
        if start + chunk >= duration:
            break
    return out


Q(None, "Word Error Rate", "Medium", "Scoring transcripts",
  "WER = (substitutions + deletions + insertions) ÷ words in the reference, from the minimum edit distance between word lists. Round to 3.",
  [(("refund my order today please", "refund my order to day please"), 0.4), (("cancel order", "cancel the order"), 0.5), (("hello", "hello"), 0.0)],
  ("Recursive edit distance with memoisation.", "O(n·m)", "O(n·m)"),
  ("A bottom-up dynamic-programming table, one row at a time.", "O(n·m)", "O(m)"),
  viz=(("cancel order", "cancel the order")))


@B
def wer(ref, hyp):
    r, h = ref.split(), hyp.split()

    @lru_cache(maxsize=None)
    def d(i, j):
        if i == 0:
            return j
        if j == 0:
            return i
        if r[i - 1] == h[j - 1]:
            return d(i - 1, j - 1)
        return 1 + min(d(i - 1, j), d(i, j - 1), d(i - 1, j - 1))
    return round(d(len(r), len(h)) / len(r), 3)


@O
def wer(ref, hyp):
    r, h = ref.split(), hyp.split()
    prev = list(range(len(h) + 1))
    for i, rw in enumerate(r, 1):
        cur = [i]
        for j, hw in enumerate(h, 1):
            cur.append(prev[j - 1] if rw == hw else 1 + min(prev[j], cur[j - 1], prev[j - 1]))
        prev = cur
    return round(prev[-1] / len(r), 3)


Q(None, "Write Subtitles", "Easy", "Timestamps",
  "Turn transcript segments <code>(start_s, end_s, text)</code> into SRT blocks: index, then <code>HH:MM:SS,mmm --&gt; HH:MM:SS,mmm</code>, then the text, separated by blank lines.",
  [(([(0.0, 2.5, "Hello and welcome."), (2.5, 65.25, "Today: multimodal AI.")],), '1\n00:00:00,000 --> 00:00:02,500\nHello and welcome.\n\n2\n00:00:02,500 --> 00:01:05,250\nToday: multimodal AI.')],
  ("Format each time with divmod by hand.", "O(n)", "O(n)"),
  ("A helper with f-string zero-padding.", "O(n)", "O(n)"),
  viz=([(0.0, 2.5, "Hello and welcome.")],))


@B
def srt(segments):
    def ts(sec):
        ms = int(round(sec * 1000))
        h = ms // 3600000
        ms -= h * 3600000
        m = ms // 60000
        ms -= m * 60000
        s = ms // 1000
        ms -= s * 1000
        return str(h).zfill(2) + ":" + str(m).zfill(2) + ":" + str(s).zfill(2) + "," + str(ms).zfill(3)
    blocks = []
    for i, (a, b, text) in enumerate(segments, 1):
        blocks.append(str(i) + "\n" + ts(a) + " --> " + ts(b) + "\n" + text)
    return "\n\n".join(blocks)


@O
def srt(segments):
    def ts(sec):
        ms = round(sec * 1000)
        h, ms = divmod(ms, 3_600_000)
        m, ms = divmod(ms, 60_000)
        s, ms = divmod(ms, 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"
    return "\n\n".join(f"{i}\n{ts(a)} --> {ts(b)}\n{t}" for i, (a, b, t) in enumerate(segments, 1))


BOXES = [("Total:", 400, 700), ("INVOICE", 250, 40), ("Qty", 300, 200), ("Date:", 50, 95), ("2026-11-02", 140, 98),
         ("Item", 50, 200), ("Pen", 50, 240), ("10", 300, 242), ("Rs 50", 480, 702)]


Q(None, "Put OCR Words in Reading Order", "Medium", "Document layout",
  "OCR returns words with top-left positions <code>(text, x, y)</code> in no particular order. Group words into lines when their y values are within <code>tol</code> of the line's first word, order lines top to bottom and words left to right, and return the lines as strings.",
  [((BOXES, 10), ['INVOICE', 'Date: 2026-11-02', 'Item Qty', 'Pen 10', 'Total: Rs 50'])],
  ("Sort by y, then build lines in a loop.", "O(n log n)", "O(n)"),
  ("Same grouping, then sort each line by x.", "O(n log n)", "O(n)"),
  viz=(([("Total:", 400, 700), ("INVOICE", 250, 40), ("Rs 50", 480, 702)], 10)))


@B
def reading_order(boxes, tol):
    rows = []
    for word in sorted(boxes, key=lambda b: b[2]):
        if rows and abs(word[2] - rows[-1][0][2]) <= tol:
            rows[-1].append(word)
        else:
            rows.append([word])
    lines = []
    for row in rows:
        row.sort(key=lambda b: b[1])
        lines.append(" ".join(b[0] for b in row))
    return lines


@O
def reading_order(boxes, tol):
    rows = []
    for w in sorted(boxes, key=lambda b: b[2]):
        if rows and w[2] - rows[-1][0][2] <= tol:
            rows[-1].append(w)
        else:
            rows.append([w])
    return [" ".join(t for t, _, _ in sorted(r, key=lambda b: b[1])) for r in rows]


Q(None, "Table Rows to Markdown", "Easy", "Giving tables to an LLM",
  "Models read tables best as Markdown. Convert rows (the first is the header) into a Markdown table string, with cells separated by ' | ' and a '---' separator row.",
  [(([["Item", "Qty", "Price"], ["Pen", "10", "5"], ["Book", "2", "120"]],), '| Item | Qty | Price |\n| --- | --- | --- |\n| Pen | 10 | 5 |\n| Book | 2 | 120 |')],
  ("String building in loops.", "O(cells)", "O(cells)"),
  ("Joins.", "O(cells)", "O(cells)"),
  viz=(([["Item", "Qty"], ["Pen", "10"]],)))


@B
def to_markdown(rows):
    lines = []
    for i, row in enumerate(rows):
        lines.append("| " + " | ".join(row) + " |")
        if i == 0:
            seps = []
            for _ in row:
                seps.append("---")
            lines.append("| " + " | ".join(seps) + " |")
    return "\n".join(lines)


@O
def to_markdown(rows):
    line = lambda cells: "| " + " | ".join(cells) + " |"
    return "\n".join([line(rows[0]), line(["---"] * len(rows[0]))] + [line(r) for r in rows[1:]])


Q(None, "Validate Extracted Invoice Fields", "Medium", "Don't trust extraction blindly",
  "A vision model extracted an invoice as JSON. Return a sorted list of problems: 'missing: f' for required fields (<code>invoice_no</code>, <code>date</code>, <code>items</code>, <code>total</code>); 'bad date' if the date isn't valid YYYY-MM-DD; 'total mismatch' if Σ qty × price differs from total by more than 0.01.",
  [(({"invoice_no": "A-17", "date": "2026-11-02", "items": [{"qty": 10, "price": 5}, {"qty": 2, "price": 120}], "total": 290},), []),
   (({"invoice_no": "A-18", "date": "2026-13-40", "items": [{"qty": 1, "price": 99.5}], "total": 99.5},), ['bad date']),
   (({"date": "2026-11-02", "items": [], "total": 10},), ['missing: invoice_no', 'total mismatch'])],
  ("Checks one by one.", "O(i)", "O(1)"),
  ("<code>date.fromisoformat</code> for the date and a generator <code>sum</code> for the total.", "O(i)", "O(1)"),
  viz=(({"invoice_no": "A-17", "date": "2026-11-02", "items": [{"qty": 10, "price": 5}], "total": 60},)))


@B
def check_invoice(inv):
    problems = []
    for f in ["invoice_no", "date", "items", "total"]:
        if f not in inv:
            problems.append("missing: " + f)
    if "date" in inv:
        parts = inv["date"].split("-")
        ok = len(parts) == 3 and all(p.isdigit() for p in parts)
        if ok:
            y, m, d = map(int, parts)
            days = [31, 29 if y % 4 == 0 and (y % 100 or y % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            ok = 1 <= m <= 12 and 1 <= d <= days[m - 1]
        if not ok:
            problems.append("bad date")
    if "items" in inv and "total" in inv:
        s = 0
        for it in inv["items"]:
            s += it["qty"] * it["price"]
        if abs(s - inv["total"]) > 0.01:
            problems.append("total mismatch")
    return sorted(problems)


@O
def check_invoice(inv):
    from datetime import date
    problems = [f"missing: {f}" for f in ("invoice_no", "date", "items", "total") if f not in inv]
    if "date" in inv:
        try:
            date.fromisoformat(inv["date"])
        except ValueError:
            problems.append("bad date")
    if "items" in inv and "total" in inv and abs(sum(i["qty"] * i["price"] for i in inv["items"]) - inv["total"]) > 0.01:
        problems.append("total mismatch")
    return sorted(problems)


Q(None, "Text or Image for Each Page?", "Easy", "Multimodal RAG routing",
  "<code>pages</code> are (extracted characters, figures). For PDF pages, plain extracted text is cheap, but pages that are mostly charts, scans or diagrams need the page image. Send the image if the page has fewer than <code>min_chars</code> extracted characters or more than <code>max_figures</code> figures. Return 'text' or 'image' per page.",
  [(([(2400, 0), (120, 1), (1800, 3), (60, 0)], 300, 2), ['text', 'image', 'image', 'image'])],
  ("A loop with an if.", "O(p)", "O(p)"),
  ("A comprehension.", "O(p)", "O(p)"),
  viz=([(2400, 0), (120, 1)], 300, 2))


@B
def page_mode(pages, min_chars, max_figures):
    out = []
    for chars, figs in pages:
        if chars < min_chars or figs > max_figures:
            out.append("image")
        else:
            out.append("text")
    return out


@O
def page_mode(pages, min_chars, max_figures):
    return ["image" if c < min_chars or f > max_figures else "text" for c, f in pages]


EMB = {"cat_photo": [0.9, 0.1, 0.0], "dog_photo": [0.7, 0.6, 0.1], "invoice_scan": [0.0, 0.2, 0.95], "chart": [0.1, 0.1, 0.8]}


Q(None, "Find Similar Images", "Easy", "Image embeddings",
  "Images are embedded as vectors; similar images point the same way. Return the ids of the <code>k</code> images most similar (cosine) to <code>query</code>, excluding itself.",
  [(("cat_photo", 2), ['dog_photo', 'chart']), (("invoice_scan", 1), ['chart'])],
  ("Cosine by hand in a loop, then sort.", "O(n·d)", "O(n)"),
  ("Normalise once with NumPy and use a matrix–vector product.", "O(n·d)", "O(n·d)"),
  viz=(("cat_photo", 2)))


@B
def similar_images(query, k):
    q = EMB[query]
    scores = []
    for name, v in EMB.items():
        if name == query:
            continue
        dot = sum(a * b for a, b in zip(q, v))
        cos = dot / (math.sqrt(sum(a * a for a in q)) * math.sqrt(sum(b * b for b in v)))
        scores.append((cos, name))
    scores.sort(reverse=True)
    return [n for _, n in scores[:k]]


@O
def similar_images(query, k):
    names = [n for n in EMB if n != query]
    M = np.array([EMB[n] for n in names])
    q = np.array(EMB[query])
    sims = (M / np.linalg.norm(M, axis=1, keepdims=True)) @ (q / np.linalg.norm(q))
    return [names[i] for i in np.argsort(-sims)[:k]]


Q(None, "Zero-Shot Labels, CLIP Style", "Medium", "Images meet text",
  "A CLIP-style model embeds images and text into one space. Score the image against each label's text embedding (cosine), divide by <code>temp</code>, and softmax. Return <code>(best label, probabilities rounded to 3)</code>.",
  [(([0.8, 0.5, 0.1], {"a photo of a cat": [0.9, 0.3, 0.0], "a photo of a dog": [0.6, 0.7, 0.1], "a scanned document": [0.0, 0.1, 1.0]}, 0.1), ('a photo of a cat', {'a photo of a cat': 0.53, 'a photo of a dog': 0.47, 'a scanned document': 0.0}))],
  ("Cosines and softmax in loops.", "O(l·d)", "O(l)"),
  ("NumPy, subtracting the max before <code>exp</code> for stability.", "O(l·d)", "O(l)"),
  viz=(([0.8, 0.5, 0.1], {"a photo of a cat": [0.9, 0.3, 0.0], "a scanned document": [0.0, 0.1, 1.0]}, 0.1)))


@B
def zero_shot(img, labels, temp):
    def cos(a, b):
        return sum(x * y for x, y in zip(a, b)) / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))
    logits = {name: cos(img, v) / temp for name, v in labels.items()}
    m = max(logits.values())
    exps = {k: math.exp(v - m) for k, v in logits.items()}
    z = sum(exps.values())
    probs = {k: round(v / z, 3) for k, v in exps.items()}
    return (max(probs, key=probs.get), probs)


@O
def zero_shot(img, labels, temp):
    names = list(labels)
    T = np.array([labels[n] for n in names])
    v = np.array(img)
    logits = (T / np.linalg.norm(T, axis=1, keepdims=True)) @ (v / np.linalg.norm(v)) / temp
    p = np.exp(logits - logits.max())
    p /= p.sum()
    return (names[int(p.argmax())], {n: round(float(x), 3) for n, x in zip(names, p)})


Q(None, "A Voice Agent's Latency Budget", "Medium", "Speech in, speech out",
  "Time to the first audio the user hears = end-of-speech detection + speech-to-text + LLM time to first token + text-to-speech time to first audio (all ms). For each configuration return the total, and the fastest configuration's name — conversation feels natural under about 800 ms.",
  [(({"cascade-big": (300, 250, 700, 200), "cascade-small": (300, 150, 250, 150), "speech-to-speech": (200, 0, 350, 0)},), ({'cascade-big': 1450, 'cascade-small': 850, 'speech-to-speech': 550}, 'speech-to-speech'))],
  ("Sum in a loop and track the minimum.", "O(c)", "O(c)"),
  ("A dict comprehension and <code>min</code>.", "O(c)", "O(c)"),
  viz=(({"cascade-big": (300, 250, 700, 200), "cascade-small": (300, 150, 250, 150)},)))


@B
def voice_latency(configs):
    totals = {}
    best = None
    for name, parts in configs.items():
        t = 0
        for p in parts:
            t += p
        totals[name] = t
        if best is None or t < totals[best]:
            best = name
    return (totals, best)


@O
def voice_latency(configs):
    totals = {n: sum(p) for n, p in configs.items()}
    return (totals, min(totals, key=totals.get))


Q(None, "How Many Video Frames to Send?", "Medium", "Video as images",
  "Models see video as sampled frames. Sample at <code>fps</code> frames per second, but send at most what fits <code>budget</code> tokens when each frame costs <code>per_frame</code> tokens; if over budget, sample evenly with fewer frames. Return <code>(frames sent, seconds between frames rounded to 2)</code>.",
  [((120, 1, 400, 20000), (50, 2.4)), ((30, 1, 400, 20000), (30, 1.0))],
  ("Compute wanted and affordable frames step by step.", "O(1)", "O(1)"),
  ("<code>min</code> of the two.", "O(1)", "O(1)"),
  viz=((120, 1, 400, 20000)))


@B
def video_frames(seconds, fps, per_frame, budget):
    wanted = seconds * fps
    affordable = budget // per_frame
    n = wanted if wanted <= affordable else affordable
    return (n, round(seconds / n, 2))


@O
def video_frames(seconds, fps, per_frame, budget):
    n = min(seconds * fps, budget // per_frame)
    return (n, round(seconds / n, 2))


PAGES = ["Invoice terms. Payment is due in 30 days. Late fees apply after 45 days.",
         "Returns policy. Items can be returned within 10 days. Refunds take 5 to 7 business days to reach cards.",
         ""]


Q(None, "Chunk a PDF and Keep Page Numbers", "Easy", "Citable document chunks",
  "Split each page's text into chunks of at most <code>max_words</code> words, skipping empty pages, and keep the page number (from 1) with each chunk so answers can cite 'p. 2'. Return <code>[(page, chunk text)]</code>.",
  [((PAGES, 8), [(1, 'Invoice terms. Payment is due in 30 days.'), (1, 'Late fees apply after 45 days.'), (2, 'Returns policy. Items can be returned within 10'), (2, 'days. Refunds take 5 to 7 business days'), (2, 'to reach cards.')])],
  ("Nested loops over pages and word windows.", "O(words)", "O(words)"),
  ("A comprehension over <code>enumerate(pages, 1)</code> and <code>range</code> steps.", "O(words)", "O(words)"),
  viz=((PAGES[:1], 8)))


@B
def pdf_chunks(pages, max_words):
    out = []
    for i, text in enumerate(pages):
        words = text.split()
        start = 0
        while start < len(words):
            out.append((i + 1, " ".join(words[start:start + max_words])))
            start += max_words
    return out


@O
def pdf_chunks(pages, max_words):
    return [(n, " ".join(w[i:i + max_words])) for n, text in enumerate(pages, 1)
            for w in [text.split()] for i in range(0, len(w), max_words)]


Q(None, "Detect the End of the User's Turn", "Medium", "Voice activity",
  "A voice agent must know when the user has stopped speaking. Given audio energy per 20 ms frame, the turn ends at the first frame that starts a run of at least <code>min_silent</code> consecutive frames below <code>threshold</code> — but only after some speech (a frame at or above threshold) has happened. Return that frame index and the time in ms, or None.",
  [(([0.01, 0.02, 0.4, 0.6, 0.5, 0.05, 0.3, 0.02, 0.01, 0.03, 0.01, 0.02], 0.1, 4), (7, 140)), (([0.01, 0.02, 0.01], 0.1, 2), None)],
  ("Scan with counters for speech seen and current silence run.", "O(n)", "O(1)"),
  ("Same scan, remembering where the current silent run began.", "O(n)", "O(1)"),
  viz=([0.01, 0.4, 0.6, 0.05, 0.02, 0.01, 0.03], 0.1, 3))


@B
def end_of_turn(energy, threshold, min_silent):
    spoke = False
    run = 0
    for i, e in enumerate(energy):
        if e >= threshold:
            spoke = True
            run = 0
        elif spoke:
            run += 1
            if run == min_silent:
                start = i - min_silent + 1
                return (start, start * 20)
    return None


@O
def end_of_turn(energy, threshold, min_silent):
    spoke, start = False, None
    for i, e in enumerate(energy):
        if e >= threshold:
            spoke, start = True, None
        elif spoke:
            start = i if start is None else start
            if i - start + 1 >= min_silent:
                return (start, start * 20)
    return None
