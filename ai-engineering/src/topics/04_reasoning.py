from lib import *
import math
import re
import statistics
from collections import Counter
from itertools import product


TOPIC(
    id="reasoning", title="Reasoning Models & Test-Time Compute", glyph="∴",
    blurb="Models that think before answering: what thinking tokens cost, effort levels, when reasoning helps, self-consistency voting, best-of-N with verifiers, pass@k, process vs outcome checks, routing easy and hard questions, and checking a model's working.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">cost = input × in_price + (thinking + answer) × out_price      # thinking is billed as output
P(majority of n correct) = Σ_{k&gt;n/2} C(n,k) p^k (1−p)^(n−k)      # self-consistency
P(best-of-n has a correct one) = 1 − (1 − p)^n                   # needs a good verifier to pick it
pass@k = 1 − C(n−c, k) / C(n, k)                                  # unbiased, from n samples with c correct</code></pre>
<p>More thinking helps multi-step problems (maths, code, planning) and wastes money on simple lookups. Measure, then choose the effort level per task.</p>
""")


Q(None, "What Does Thinking Cost?", "Easy", "Thinking is billed as output",
  "A call reads <code>inp</code> input tokens and writes <code>think</code> thinking tokens plus <code>out</code> answer tokens. Prices are per million tokens. Return <code>(cost without thinking, cost with thinking)</code> in dollars, rounded to 5.",
  [((3000, 8000, 400, 3.0, 15.0), (0.015, 0.135)), ((3000, 0, 400, 3.0, 15.0), (0.015, 0.015))],
  ("Compute each part step by step.", "O(1)", "O(1)"),
  ("Two expressions.", "O(1)", "O(1)"),
  viz=((3000, 8000, 400, 3.0, 15.0)))


@B
def thinking_cost(inp, think, out, in_price, out_price):
    input_cost = inp * in_price / 1_000_000
    answer_cost = out * out_price / 1_000_000
    thinking = think * out_price / 1_000_000
    return (round(input_cost + answer_cost, 5), round(input_cost + answer_cost + thinking, 5))


@O
def thinking_cost(inp, think, out, in_price, out_price):
    base = (inp * in_price + out * out_price) / 1e6
    return (round(base, 5), round(base + think * out_price / 1e6, 5))


Q(None, "How Long Will the User Wait?", "Easy", "Latency",
  "Time = time to first token <code>ttft</code> + (thinking + answer tokens) ÷ <code>speed</code> tokens per second. Return seconds (rounded to 1) for each thinking amount in <code>thinks</code>.",
  [((0.6, 80, 300, [0, 2000, 16000]), [4.3, 29.4, 204.3])],
  ("A loop.", "O(n)", "O(n)"),
  ("A comprehension.", "O(n)", "O(n)"),
  viz=((0.6, 80, 300, [0, 2000, 16000])))


@B
def wait_time(ttft, speed, answer, thinks):
    out = []
    for t in thinks:
        out.append(round(ttft + (t + answer) / speed, 1))
    return out


@O
def wait_time(ttft, speed, answer, thinks):
    return [round(ttft + (t + answer) / speed, 1) for t in thinks]


Q(None, "Majority Voting Helps — How Much?", "Medium", "Self-consistency",
  "If each sample is right with probability <code>p</code> independently, what is the chance that a strict majority of <code>n</code> samples (n odd) is right? Round to 4.",
  [((0.7, 1), 0.7), ((0.7, 5), 0.8369), ((0.7, 15), 0.95), ((0.4, 15), 0.2131)],
  ("Enumerate every right/wrong pattern of n samples.", "O(2ⁿ · n)", "O(n)"),
  ("Add binomial probabilities with <code>math.comb</code>.", "O(n)", "O(1)"),
  viz=((0.7, 5)))


@B
def majority_right(p, n):
    total = 0.0
    for pattern in product([0, 1], repeat=n):
        k = sum(pattern)
        if k > n / 2:
            total += p ** k * (1 - p) ** (n - k)
    return round(total, 4)


@O
def majority_right(p, n):
    return round(sum(math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n // 2 + 1, n + 1)), 4)


Q(None, "How Many Samples for Best-of-N?", "Easy", "Verifiers",
  "With a perfect verifier you only need one correct sample. If each is right with probability <code>p</code>, return the smallest n with P(at least one right) ≥ <code>target</code>.",
  [((0.3, 0.9), 7), ((0.05, 0.95), 59), ((0.9, 0.9), 1)],
  ("Increase n until 1 − (1 − p)ⁿ reaches the target.", "O(n)", "O(1)"),
  ("Solve with logarithms: n = ⌈log(1 − target) / log(1 − p)⌉.", "O(1)", "O(1)"),
  viz=((0.3, 0.9)))


@B
def samples_needed(p, target):
    n = 1
    while 1 - (1 - p) ** n < target - 1e-12:
        n += 1
    return n


@O
def samples_needed(p, target):
    return max(1, math.ceil(math.log(1 - target) / math.log(1 - p) - 1e-9))


Q(None, "Unbiased pass@k", "Medium", "Evaluating code models",
  "From <code>n</code> samples of which <code>c</code> passed the tests, estimate pass@k = the chance at least one of k random samples passes: 1 − C(n−c, k) / C(n, k). Round to 4.",
  [((20, 3, 1), 0.15), ((20, 3, 5), 0.6009), ((10, 0, 3), 0.0), ((10, 9, 3), 1.0)],
  ("A running product: Π (1 − k / i) for i from n−c+1 to n.", "O(c)", "O(1)"),
  ("<code>math.comb</code> directly.", "O(k)", "O(1)"),
  viz=((20, 3, 5)))


@B
def pass_at_k(n, c, k):
    if n - c < k:
        return 1.0
    prod = 1.0
    for i in range(n - c + 1, n + 1):
        prod *= 1 - k / i
    return round(1 - prod, 4)


@O
def pass_at_k(n, c, k):
    return round(1 - math.comb(n - c, k) / math.comb(n, k), 4) if n - c >= k else 1.0


Q(None, "Find the Final Answer", "Easy", "Parsing reasoning",
  "Return the value after the <b>last</b> 'Answer:' (case-insensitive) in the text, stripped, or None.",
  [(("Let's think. 12*3=36, minus 4... Answer: 30? No wait.\nAnswer: 32",), '32'), (("I'm not sure.",), None)],
  ("Scan lines from the end.", "O(n)", "O(1)"),
  ("<code>re.findall</code> and take the last match.", "O(n)", "O(m)"),
  viz=(("Let's think. 12*3=36... Answer: 30? No wait.\nAnswer: 32",)))


@B
def final_answer(text):
    lower = text.lower()
    i = lower.rfind("answer:")
    if i == -1:
        return None
    return text[i + len("answer:"):].split("\n")[0].strip()


@O
def final_answer(text):
    found = re.findall(r"answer:\s*(.*)", text, re.I)
    return found[-1].strip() if found else None


Q(None, "Separate Thinking From the Answer", "Easy", "Response blocks",
  "A response's content is a list of blocks: <code>{'type': 'thinking', ...}</code>, <code>{'type': 'text', 'text': ...}</code> or <code>{'type': 'tool_use', ...}</code>. Return <code>(the joined text of all text blocks, number of thinking blocks)</code>. Show users the text, keep thinking for debugging.",
  [(([{"type": "thinking", "thinking": "..."}, {"type": "text", "text": "The answer"}, {"type": "text", "text": " is 42."}],), ('The answer is 42.', 1))],
  ("A loop with if-statements.", "O(b)", "O(b)"),
  ("A join over a filtered generator and a <code>sum</code>.", "O(b)", "O(b)"),
  viz=([{"type": "thinking", "thinking": "..."}, {"type": "text", "text": "The answer"}],))


@B
def split_blocks(blocks):
    text, thinking = "", 0
    for b in blocks:
        if b["type"] == "text":
            text += b["text"]
        elif b["type"] == "thinking":
            thinking += 1
    return (text, thinking)


@O
def split_blocks(blocks):
    return ("".join(b["text"] for b in blocks if b["type"] == "text"), sum(b["type"] == "thinking" for b in blocks))


EFFORT = {"low": (0.71, 0.004), "medium": (0.83, 0.011), "high": (0.88, 0.032), "max": (0.89, 0.09)}


Q(None, "Choose the Effort Level", "Easy", "Cheapest level that's good enough",
  "<code>EFFORT[level] = (accuracy, cost per task)</code> from your own evaluation. Return the cheapest level whose accuracy reaches <code>target</code>, or 'none'.",
  [((0.8,), 'medium'), ((0.88,), 'high'), ((0.95,), 'none')],
  ("Loop and keep the cheapest passing level.", "O(l)", "O(1)"),
  ("<code>min</code> over a filtered generator with a default.", "O(l)", "O(1)"),
  viz=((0.8,)))


@B
def choose_effort(target):
    best = None
    for level, (acc, cost) in EFFORT.items():
        if acc >= target and (best is None or cost < EFFORT[best][1]):
            best = level
    return best if best else "none"


@O
def choose_effort(target):
    return min((l for l, (a, _) in EFFORT.items() if a >= target), key=lambda l: EFFORT[l][1], default="none")


Q(None, "Route Easy and Hard Questions", "Medium", "Reasoning only where it pays",
  "Send a question to the reasoning model if its difficulty score ≥ <code>cutoff</code>, else to the fast model. Accuracy and cost per question: fast (0.95 easy, 0.40 hard, $0.002), reasoning (0.97 easy, 0.85 hard, $0.03). Difficulty ≥ 0.5 means the question is really hard. Return <code>(expected accuracy, total cost)</code> rounded to 3 and 4.",
  [(([0.1, 0.2, 0.9, 0.3, 0.7, 0.1, 0.8, 0.2], 0.5), (0.912, 0.1)), (([0.1, 0.2, 0.9, 0.3, 0.7, 0.1, 0.8, 0.2], 0.0), (0.925, 0.24)), (([0.1, 0.2, 0.9, 0.3, 0.7, 0.1, 0.8, 0.2], 1.1), (0.744, 0.016))],
  ("Loop and add up.", "O(n)", "O(1)"),
  ("A table of (model, hard?) → accuracy and two sums.", "O(n)", "O(1)"),
  viz=([0.1, 0.9, 0.3, 0.7], 0.5))


@B
def route_cost(difficulty, cutoff):
    acc, cost = 0.0, 0.0
    for d in difficulty:
        hard = d >= 0.5
        if d >= cutoff:
            acc += 0.85 if hard else 0.97
            cost += 0.03
        else:
            acc += 0.40 if hard else 0.95
            cost += 0.002
    return (round(acc / len(difficulty), 3), round(cost, 4))


@O
def route_cost(difficulty, cutoff):
    table = {("reason", True): (0.85, 0.03), ("reason", False): (0.97, 0.03),
             ("fast", True): (0.40, 0.002), ("fast", False): (0.95, 0.002)}
    picks = [table[("reason" if d >= cutoff else "fast", d >= 0.5)] for d in difficulty]
    return (round(sum(a for a, _ in picks) / len(picks), 3), round(sum(c for _, c in picks), 4))


Q(None, "Judge the Steps, Not Just the Answer", "Medium", "Process vs outcome scoring",
  "Each candidate solution has per-step verifier scores and a final-answer score. Outcome scoring picks the best final score; process scoring picks the best <b>weakest step</b> (a chain is only as strong as its worst step). Return <code>(outcome pick, process pick)</code> — indexes, ties to the earlier.",
  [(([([0.9, 0.2, 0.95], 0.97), ([0.8, 0.85, 0.8], 0.9), ([0.99, 0.99, 0.5], 0.92)],), (0, 1))],
  ("Two loops tracking the best.", "O(c · s)", "O(1)"),
  ("<code>max</code> with keys over the indexes.", "O(c · s)", "O(1)"),
  viz=([([0.9, 0.2, 0.95], 0.97), ([0.8, 0.85, 0.8], 0.9)],))


@B
def pick_solutions(cands):
    best_o, best_p = 0, 0
    for i, (steps, final) in enumerate(cands):
        if final > cands[best_o][1]:
            best_o = i
        if min(steps) > min(cands[best_p][0]):
            best_p = i
    return (best_o, best_p)


@O
def pick_solutions(cands):
    idx = range(len(cands))
    return (max(idx, key=lambda i: cands[i][1]), max(idx, key=lambda i: min(cands[i][0])))


Q(None, "Check the Arithmetic in the Working", "Medium", "Verifying reasoning",
  "Find lines of the form <code>a op b = c</code> (integers, op in + − × * /) and return the 1-based line numbers whose result is wrong. '×' means multiply. Division must be exact.",
  [(("We have 12 boxes.\n12 * 8 = 96\n96 + 15 = 101\n101 - 7 = 94\n94 / 2 = 47\n3 × 4 = 13",), [3, 6])],
  ("Split each line by hand and compute.", "O(n)", "O(1)"),
  ("One regex with groups and an operator table.", "O(n)", "O(1)"),
  viz=(("12 * 8 = 96\n96 + 15 = 101\n3 × 4 = 13",)))


@B
def wrong_lines(text):
    bad = []
    for i, line in enumerate(text.split("\n"), 1):
        parts = line.replace("×", "*").split()
        if len(parts) == 5 and parts[3] == "=" and parts[1] in "+-*/" and all(p.lstrip("-").isdigit() for p in (parts[0], parts[2], parts[4])):
            a, op, b, c = int(parts[0]), parts[1], int(parts[2]), int(parts[4])
            if op == "+":
                v = a + b
            elif op == "-":
                v = a - b
            elif op == "*":
                v = a * b
            else:
                v = a / b
            if v != c:
                bad.append(i)
    return bad


@O
def wrong_lines(text):
    ops = {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b, "×": lambda a, b: a * b,
           "/": lambda a, b: a / b}
    bad = []
    for i, line in enumerate(text.splitlines(), 1):
        m = re.fullmatch(r"\s*(-?\d+)\s*([-+*/×])\s*(-?\d+)\s*=\s*(-?\d+)\s*", line)
        if m and ops[m[2]](int(m[1]), int(m[3])) != int(m[4]):
            bad.append(i)
    return bad


Q(None, "Combine Numeric Estimates", "Easy", "Median beats mean",
  "Several samples estimated a number; one went wild. Return <code>(mean, median)</code> rounded to 2 — the median ignores the outlier.",
  [(([42, 40, 44, 41, 4100],), (853.4, 42)), (([10, 12],), (11, 11.0))],
  ("Sort and pick the middle by hand.", "O(n log n)", "O(n)"),
  ("<code>statistics.mean</code> and <code>statistics.median</code>.", "O(n log n)", "O(n)"),
  viz=([42, 40, 44, 41, 4100],))


@B
def combine(estimates):
    s = sorted(estimates)
    n = len(s)
    median = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
    return (round(sum(s) / n, 2), round(median, 2))


@O
def combine(estimates):
    return (round(statistics.mean(estimates), 2), round(statistics.median(estimates), 2))


Q(None, "Know When to Abstain", "Medium", "Agreement as confidence",
  "Sample answers several times. If the most common answer has at least <code>threshold</code> of the votes, return it; otherwise return 'not sure — escalate'. In high-stakes settings, saying 'I don't know' beats a confident guess.",
  [((["B", "B", "B", "A", "B"], 0.6), 'B'), ((["A", "B", "C", "A", "B"], 0.6), 'not sure — escalate')],
  ("Count with a dict.", "O(n)", "O(n)"),
  ("<code>Counter.most_common(1)</code>.", "O(n)", "O(n)"),
  viz=(["B", "B", "B", "A", "B"], 0.6))


@B
def answer_or_abstain(samples, threshold):
    counts = {}
    for s in samples:
        counts[s] = counts.get(s, 0) + 1
    best = max(counts, key=counts.get)
    if counts[best] / len(samples) >= threshold:
        return best
    return "not sure — escalate"


@O
def answer_or_abstain(samples, threshold):
    best, n = Counter(samples).most_common(1)[0]
    return best if n / len(samples) >= threshold else "not sure — escalate"


Q(None, "Accuracy Per Dollar", "Easy", "Is reasoning worth it here?",
  "For each option <code>(name, accuracy, cost per task)</code>, compute correct answers per dollar and return the names sorted from best to worst value.",
  [(([("fast", 0.78, 0.002), ("fast+vote5", 0.86, 0.01), ("reasoning", 0.92, 0.03)],), ['fast', 'fast+vote5', 'reasoning'])],
  ("Compute ratios in a loop, then sort.", "O(n log n)", "O(n)"),
  ("<code>sorted</code> with a key.", "O(n log n)", "O(n)"),
  viz=([("fast", 0.78, 0.002), ("reasoning", 0.92, 0.03)],))


@B
def value_rank(options):
    scored = []
    for name, acc, cost in options:
        scored.append((acc / cost, name))
    scored.sort(reverse=True)
    return [n for _, n in scored]


@O
def value_rank(options):
    return [n for n, a, c in sorted(options, key=lambda o: o[1] / o[2], reverse=True)]


Q(None, "Sampling Many Times, Cheaply", "Medium", "Caching the shared prompt",
  "Run <code>n</code> samples of the same prompt (<code>inp</code> tokens), each writing <code>out</code> tokens. With caching, the first sample writes the prompt to the cache (1.25×) and the rest read it (0.1×). Prices per million: input <code>pin</code>, output <code>pout</code>. Return <code>(cost without caching, with caching)</code> rounded to 4.",
  [((5, 20000, 800, 3.0, 15.0), (0.36, 0.159))],
  ("Add sample by sample.", "O(n)", "O(1)"),
  ("A closed form.", "O(1)", "O(1)"),
  viz=((5, 20000, 800, 3.0, 15.0)))


@B
def sampling_cost(n, inp, out, pin, pout):
    plain = cached = 0.0
    for i in range(n):
        plain += (inp * pin + out * pout) / 1e6
        factor = 1.25 if i == 0 else 0.1
        cached += (inp * pin * factor + out * pout) / 1e6
    return (round(plain, 4), round(cached, 4))


@O
def sampling_cost(n, inp, out, pin, pout):
    outputs = n * out * pout / 1e6
    return (round(n * inp * pin / 1e6 + outputs, 4), round((1.25 + 0.1 * (n - 1)) * inp * pin / 1e6 + outputs, 4))


Q(None, "Beam Search Over Reasoning Steps", "Hard", "Search with a verifier",
  "At each step there are candidate next steps with verifier scores. Keep the best <code>beam</code> partial solutions (scored by the sum of step scores) and extend each with every candidate. <code>steps[i]</code> is the list of (label, score) options at step i, the same for every path. Return the best full path (labels) and its score rounded to 2.",
  [(([[("a", 0.9), ("b", 0.6)], [("c", 0.2), ("d", 0.8)], [("e", 0.5), ("f", 0.95)]], 2), (['a', 'd', 'f'], 2.65))],
  ("Enumerate every path (for this small case) and take the best.", "O(kˢ)", "O(kˢ)"),
  ("Keep only the top-b partial paths with <code>heapq.nlargest</code> at each step.", "O(s · b · k log b)", "O(b)"),
  viz=([[("a", 0.9), ("b", 0.6)], [("c", 0.2), ("d", 0.8)]], 2))


@B
def beam_path(steps, beam):
    best = None
    for path in product(*steps):
        score = sum(s for _, s in path)
        if best is None or score > best[1]:
            best = ([l for l, _ in path], score)
    return (best[0], round(best[1], 2))


@O
def beam_path(steps, beam):
    import heapq
    beams = [([], 0.0)]
    for options in steps:
        grown = [(path + [l], score + s) for path, score in beams for l, s in options]
        beams = heapq.nlargest(beam, grown, key=lambda b: b[1])
    path, score = beams[0]
    return (path, round(score, 2))


Q(None, "Stop Thinking at the Budget", "Easy", "Budget control",
  "A model thinks in chunks of tokens. Stop adding chunks once the next one would exceed <code>budget</code>. Return <code>(chunks used, tokens used, chunks cut)</code>.",
  [(([1200, 3000, 800, 4000, 500], 5000), (3, 5000, 2))],
  ("A running total that breaks at the limit.", "O(n)", "O(1)"),
  ("<code>itertools.accumulate</code> to find where the total crosses the budget.", "O(n)", "O(n)"),
  viz=([1200, 3000, 800, 4000, 500], 5000))


@B
def think_budget(chunks, budget):
    used, n = 0, 0
    for c in chunks:
        if used + c > budget:
            break
        used += c
        n += 1
    return (n, used, len(chunks) - n)


@O
def think_budget(chunks, budget):
    from itertools import accumulate, takewhile
    totals = list(takewhile(lambda t: t <= budget, accumulate(chunks)))
    return (len(totals), totals[-1] if totals else 0, len(chunks) - len(totals))


Q(None, "Prompt for Reasoning Without a Reasoning Model", "Easy", "Chain-of-thought prompts",
  "Build a prompt that asks a standard model to reason first: the question, then 'Think step by step inside &lt;thinking&gt; tags, then give only the final answer inside &lt;answer&gt; tags.' Then parse a reply: return the text inside the last &lt;answer&gt;…&lt;/answer&gt;, stripped. Return <code>(prompt, parsed answer)</code>.",
  [(("What is 17 × 6?", "<thinking>17×6 = 102</thinking><answer> 102 </answer>"), ('What is 17 × 6?\n\nThink step by step inside <thinking> tags, then give only the final answer inside <answer> tags.', '102'))],
  ("String concatenation and <code>find</code>.", "O(n)", "O(n)"),
  ("An f-string and a regex.", "O(n)", "O(n)"),
  viz=(("What is 17 × 6?", "<thinking>17×6 = 102</thinking><answer> 102 </answer>")))


@B
def cot(question, reply):
    prompt = question + "\n\nThink step by step inside <thinking> tags, then give only the final answer inside <answer> tags."
    start = reply.rfind("<answer>")
    end = reply.rfind("</answer>")
    answer = reply[start + len("<answer>"):end].strip() if start != -1 and end > start else None
    return (prompt, answer)


@O
def cot(question, reply):
    prompt = f"{question}\n\nThink step by step inside <thinking> tags, then give only the final answer inside <answer> tags."
    found = re.findall(r"<answer>(.*?)</answer>", reply, re.S)
    return (prompt, found[-1].strip() if found else None)


Q(None, "Does More Thinking Pay Off?", "Medium", "Diminishing returns",
  "Given evaluation results <code>(thinking budget, accuracy)</code> sorted by budget, return the largest budget where the accuracy gained per extra 1,000 tokens (vs the previous budget) is still at least <code>min_gain</code> percentage points.",
  [(([(0, 61.0), (1000, 70.0), (4000, 78.0), (16000, 81.0), (32000, 81.5)], 0.5), 4000), (([(0, 61.0), (1000, 61.2)], 0.5), 0)],
  ("Walk pairs of neighbours.", "O(n)", "O(1)"),
  ("<code>zip(results, results[1:])</code> and keep the last that passes.", "O(n)", "O(1)"),
  viz=([(0, 61.0), (1000, 70.0), (4000, 78.0), (16000, 81.0)], 0.5))


@B
def worth_it(results, min_gain):
    best = results[0][0]
    for i in range(1, len(results)):
        b0, a0 = results[i - 1]
        b1, a1 = results[i]
        if (a1 - a0) / ((b1 - b0) / 1000) >= min_gain:
            best = b1
        else:
            break
    return best


@O
def worth_it(results, min_gain):
    best = results[0][0]
    for (b0, a0), (b1, a1) in zip(results, results[1:]):
        if (a1 - a0) * 1000 / (b1 - b0) < min_gain:
            break
        best = b1
    return best


WORDS = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
         "ten": 10, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50}


Q(None, "Normalise Before You Vote", "Medium", "Free-form answers",
  "'$32', '32 dollars', '32.0' and 'thirty-two' are the same answer. Normalise each answer to a number (strip symbols and words, parse number words up to 'fifty-nine' written with a hyphen), then return the majority value as an int and its vote count. Unparseable answers are ignored.",
  [((["$32", "32 dollars", "thirty-two", "32.0", "31", "no idea"],), (32, 4))],
  ("Character-by-character cleaning and a word table.", "O(n · l)", "O(n)"),
  ("A regex for the first number, the word table for the rest, then <code>Counter</code>.", "O(n · l)", "O(n)"),
  viz=(["$32", "32 dollars", "thirty-two", "31"],))


@B
def normalised_vote(answers):
    counts = {}
    for a in answers:
        a = a.lower().strip()
        digits = ""
        for ch in a:
            if ch.isdigit() or (ch == "." and digits):
                digits += ch
            elif digits:
                break
        value = None
        if digits:
            value = int(float(digits))
        else:
            parts = a.split("-")
            if all(p in WORDS for p in parts):
                value = sum(WORDS[p] for p in parts)
        if value is not None:
            counts[value] = counts.get(value, 0) + 1
    best = max(counts, key=counts.get)
    return (best, counts[best])


@O
def normalised_vote(answers):
    def parse(a):
        a = a.lower().strip()
        m = re.search(r"\d+(?:\.\d+)?", a)
        if m:
            return int(float(m.group()))
        parts = a.split("-")
        return sum(WORDS[p] for p in parts) if all(p in WORDS for p in parts) else None
    values = [v for v in map(parse, answers) if v is not None]
    return Counter(values).most_common(1)[0]
