from lib import *
import math
import numpy as np


TOPIC(
    id="serving", title="Serving LLMs: Inference Optimisation", glyph="⚡",
    blurb="What it takes to run models yourself: memory for weights and the KV cache, batching (static vs continuous), prefill vs decode, speculative decoding, quantisation, paged KV memory and prefix sharing, scheduling, rate limits, fallbacks and the self-host vs API cost decision.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">weights_GB = params × bytes_per_param / 1e9          # bf16 = 2 bytes, int8 = 1, int4 = 0.5
kv_bytes   = 2 × layers × kv_heads × head_dim × bytes × tokens × batch   # K and V for every layer
tokens per target step (speculative) = (1 − a^(k+1)) / (1 − a)       # a = acceptance rate, k = draft length
cost_per_M_tokens = gpu_$per_hour / (tokens_per_sec × 3600) × 1e6

vllm serve meta-llama/Llama-3.1-8B-Instruct --max-model-len 8192   # OpenAI-compatible server with continuous batching</code></pre>
""")

BYTES = {"fp32": 4, "bf16": 2, "fp8": 1, "int8": 1, "int4": 0.5}


Q(None, "Memory for the Weights", "Easy", "Will it fit on the GPU?",
  "Return the GB needed to hold <code>params</code> parameters (in billions) at each dtype in <code>dtypes</code>, rounded to 1 (1 GB = 10⁹ bytes).",
  [((8, ["fp32", "bf16", "int8", "int4"]), {'fp32': 32, 'bf16': 16, 'int8': 8, 'int4': 4.0}), ((70, ["bf16", "int4"]), {'bf16': 140, 'int4': 35.0})],
  ("A loop with a bytes table.", "O(d)", "O(d)"),
  ("A dict comprehension.", "O(d)", "O(d)"),
  viz=((8, ["fp32", "bf16", "int4"])))


@B
def weight_gb(params, dtypes):
    out = {}
    for d in dtypes:
        out[d] = round(params * 1e9 * BYTES[d] / 1e9, 1)
    return out


@O
def weight_gb(params, dtypes):
    return {d: round(params * BYTES[d], 1) for d in dtypes}


Q(None, "How Big Is the KV Cache?", "Medium", "Memory grows with tokens",
  "The KV cache stores a key and a value vector per layer, per KV head, per token. Return GB (rounded to 2) for <code>batch</code> sequences of <code>tokens</code> tokens.",
  [((32, 8, 128, 2, 8192, 1), 1.07), ((32, 8, 128, 2, 8192, 16), 17.18), ((32, 32, 128, 2, 8192, 1), 4.29)],
  ("Multiply step by step: per token per layer, then up.", "O(1)", "O(1)"),
  ("One product.", "O(1)", "O(1)"),
  viz=((32, 8, 128, 2, 8192, 1)))


@B
def kv_gb(layers, kv_heads, head_dim, dtype_bytes, tokens, batch):
    per_token_layer = 2 * kv_heads * head_dim * dtype_bytes
    per_token = per_token_layer * layers
    return round(per_token * tokens * batch / 1e9, 2)


@O
def kv_gb(layers, kv_heads, head_dim, dtype_bytes, tokens, batch):
    return round(2 * layers * kv_heads * head_dim * dtype_bytes * tokens * batch / 1e9, 2)


Q(None, "How Many Users at Once?", "Medium", "Concurrency on one GPU",
  "A GPU has <code>gpu_gb</code> memory; weights take <code>weights_gb</code> and the runtime reserves 10% of the GPU. Each sequence needs <code>kv_mb_per_token</code> MB per token, for <code>tokens</code> tokens. Return how many sequences fit (rounded down).",
  [((80, 16, 0.125, 8192), 54), ((80, 16, 0.125, 2048), 218), ((24, 16, 0.125, 8192), 5)],
  ("Subtract and divide step by step.", "O(1)", "O(1)"),
  ("Floor division in one expression, clamped at 0.", "O(1)", "O(1)"),
  viz=((80, 16, 0.125, 8192)))


@B
def max_sequences(gpu_gb, weights_gb, kv_mb_per_token, tokens):
    free_gb = gpu_gb * 0.9 - weights_gb
    per_seq_gb = kv_mb_per_token * tokens / 1000
    n = int(free_gb // per_seq_gb)
    if n < 0:
        n = 0
    return n


@O
def max_sequences(gpu_gb, weights_gb, kv_mb_per_token, tokens):
    return max(0, int((gpu_gb * 0.9 - weights_gb) // (kv_mb_per_token * tokens / 1000)))


Q(None, "Static vs Continuous Batching", "Hard", "Why vLLM is fast",
  "Requests need <code>lengths[i]</code> decode steps; the GPU runs <code>slots</code> sequences per step. <b>Static</b>: take requests in groups of <code>slots</code>; a group takes as long as its longest request. <b>Continuous</b>: whenever a sequence finishes, the next waiting request takes its slot. Return <code>(static steps, continuous steps)</code>.",
  [(([10, 200, 15, 30, 190, 20, 25, 12], 2), (445, 257)), (([10, 200, 15, 30, 190, 20, 25, 12], 4), (390, 200))],
  ("Static: sum of each group's max. Continuous: simulate slots freeing up.", "O(n · slots)", "O(slots)"),
  ("Continuous is a min-heap of slot finish times (like a worker pool).", "O(n log slots)", "O(slots)"),
  viz=([10, 200, 15, 30], 2))


@B
def batching_steps(lengths, slots):
    static = 0
    for i in range(0, len(lengths), slots):
        static += max(lengths[i:i + slots])
    finish = [0] * slots
    for L in lengths:
        j = finish.index(min(finish))
        finish[j] += L
    return (static, max(finish))


@O
def batching_steps(lengths, slots):
    import heapq
    static = sum(max(lengths[i:i + slots]) for i in range(0, len(lengths), slots))
    heap = [0] * slots
    for L in lengths:
        heapq.heappush(heap, heapq.heappop(heap) + L)
    return (static, max(heap))


Q(None, "Prefill vs Decode", "Easy", "Where the time goes",
  "Prefill processes the whole prompt in parallel at <code>prefill_tps</code> tokens/s; decode makes one token at a time at <code>decode_tps</code> tokens/s. Return <code>(time to first token, total time)</code> in seconds, rounded to 2.",
  [((4000, 300, 8000, 60), (0.5, 5.5)), ((200, 1500, 8000, 60), (0.03, 25.02))],
  ("Two divisions.", "O(1)", "O(1)"),
  ("The same, as one tuple expression.", "O(1)", "O(1)"),
  viz=((4000, 300, 8000, 60)))


@B
def prefill_decode(prompt, output, prefill_tps, decode_tps):
    ttft = prompt / prefill_tps
    total = ttft + output / decode_tps
    return (round(ttft, 2), round(total, 2))


@O
def prefill_decode(prompt, output, prefill_tps, decode_tps):
    ttft = prompt / prefill_tps
    return (round(ttft, 2), round(ttft + output / decode_tps, 2))


Q(None, "Speculative Decoding: Expected Speed-Up", "Medium", "Draft and verify",
  "A small draft model proposes <code>k</code> tokens; the big model checks them in one step. Each is accepted with probability <code>a</code> until the first rejection, and the big model always adds one token of its own. Expected tokens per big-model step = (1 − a^(k+1)) / (1 − a). Return it for each k in <code>ks</code>, rounded to 2.",
  [((0.8, [1, 2, 4, 8]), [1.8, 2.44, 3.36, 4.33]), ((0.5, [1, 4, 8]), [1.5, 1.94, 2.0])],
  ("Sum the probabilities that the first j tokens are all accepted, j = 0..k.", "O(k)", "O(1)"),
  ("The geometric-series closed form.", "O(1)", "O(1)"),
  viz=((0.8, [1, 2, 4])))


@B
def spec_tokens(a, ks):
    out = []
    for k in ks:
        total = 0
        for j in range(k + 1):
            total += a ** j
        out.append(round(total, 2))
    return out


@O
def spec_tokens(a, ks):
    return [round((1 - a ** (k + 1)) / (1 - a), 2) for k in ks]


Q(None, "Verify a Draft", "Medium", "Accepting the matching prefix",
  "Greedy speculative decoding: keep the draft's tokens while they match what the big model would produce, then take the big model's token at the first mismatch (or one extra token if all match). Return <code>(accepted draft tokens, tokens emitted this step)</code>.",
  [((["The", "cat", "sat", "on"], ["The", "cat", "is", "on", "the"]), (2, ['The', 'cat', 'is'])), ((["a", "b"], ["a", "b", "c"]), (2, ['a', 'b', 'c'])), ((["x"], ["y", "z"]), (0, ['y']))],
  ("Walk both lists with an index.", "O(k)", "O(k)"),
  ("<code>itertools.takewhile</code> over the zipped pair.", "O(k)", "O(k)"),
  viz=((["The", "cat", "sat", "on"], ["The", "cat", "is", "on", "the"])))


@B
def verify_draft(draft, target):
    n = 0
    while n < len(draft) and draft[n] == target[n]:
        n += 1
    return (n, target[:n + 1])


@O
def verify_draft(draft, target):
    from itertools import takewhile
    n = sum(1 for _ in takewhile(lambda p: p[0] == p[1], zip(draft, target)))
    return (n, target[:n + 1])


W = [0.42, -1.27, 0.03, 0.88, -0.51, 2.31, -0.07, 0.66]


Q(None, "Quantise to int8", "Medium", "Smaller and faster",
  "Symmetric int8 quantisation: scale = max |w| / 127, q = round(w / scale), restored = q × scale. Return <code>(q values, largest absolute error rounded to 4)</code>.",
  [((W,), ([23, -70, 2, 48, -28, 127, -4, 36], 0.0069))],
  ("Loop over weights.", "O(n)", "O(n)"),
  ("NumPy: <code>np.round</code>, <code>np.abs</code>.", "O(n)", "O(n)"),
  viz=((W,)))


@B
def int8(weights):
    scale = max(abs(w) for w in weights) / 127
    q, err = [], 0
    for w in weights:
        v = round(w / scale)
        q.append(v)
        err = max(err, abs(w - v * scale))
    return (q, round(err, 4))


@O
def int8(weights):
    w = np.array(weights)
    scale = np.abs(w).max() / 127
    q = np.round(w / scale)
    return (q.astype(int).tolist(), round(float(np.abs(w - q * scale).max()), 4))


Q(None, "Why Group-Wise Scales Help", "Medium", "Outliers in quantisation",
  "Quantise to int4 (levels −7…7, scale = max|w|/7) either with <b>one</b> scale for all weights or a separate scale per <code>group</code> consecutive weights. Return <code>(mean absolute error per-tensor, per-group)</code>, rounded to 4. One big weight ruins a shared scale.",
  [((W, 4), (0.0625, 0.0418)), ((W, 2), (0.0625, 0.0327))],
  ("A helper that quantises a list, used once and per group.", "O(n)", "O(n)"),
  ("NumPy reshape into groups and a per-row max.", "O(n)", "O(n)"),
  viz=((W, 4)))


@B
def group_quant(weights, group):
    def err(ws):
        scale = max(abs(w) for w in ws) / 7
        return [abs(w - round(w / scale) * scale) for w in ws]
    whole = err(weights)
    grouped = []
    for i in range(0, len(weights), group):
        grouped += err(weights[i:i + group])
    return (round(sum(whole) / len(whole), 4), round(sum(grouped) / len(grouped), 4))


@O
def group_quant(weights, group):
    w = np.array(weights)

    def mae(m):
        scale = np.abs(m).max(axis=-1, keepdims=True) / 7
        return np.abs(m - np.round(m / scale) * scale).mean()
    return (round(float(mae(w[None, :])), 4), round(float(mae(w.reshape(-1, group))), 4))


Q(None, "Paged KV Memory", "Medium", "PagedAttention",
  "Old servers reserved <code>max_len</code> tokens of KV memory per sequence up front. Paged allocation uses blocks of <code>block</code> tokens, only as needed. Return <code>(tokens reserved up front, tokens reserved with paging, % wasted up front)</code> for sequences of the given lengths.",
  [(([300, 1200, 50, 4096, 700], 4096, 16), (20480, 6368, 69.0))],
  ("Ceiling division per sequence in a loop.", "O(n)", "O(1)"),
  ("Sums with <code>-(-L // block) * block</code>.", "O(n)", "O(1)"),
  viz=([300, 1200, 50], 4096, 16))


@B
def paged(lengths, max_len, block):
    upfront = max_len * len(lengths)
    paged_total = 0
    for L in lengths:
        blocks = L // block
        if L % block:
            blocks += 1
        paged_total += blocks * block
    used = sum(lengths)
    return (upfront, paged_total, round((upfront - used) / upfront * 100, 1))


@O
def paged(lengths, max_len, block):
    upfront = max_len * len(lengths)
    return (upfront, sum(-(-L // block) * block for L in lengths), round((upfront - sum(lengths)) / upfront * 100, 1))


Q(None, "Share the System Prompt's Cache", "Easy", "Prefix caching",
  "Every request starts with the same <code>prefix</code>-token system prompt. With prefix sharing its KV blocks are stored once. Return <code>(blocks without sharing, blocks with sharing)</code> for requests whose own extra tokens are <code>extras</code> (blocks of <code>block</code> tokens; the prefix fills whole blocks).",
  [((2048, [100, 400, 30, 900], 16), (603, 219))],
  ("Count blocks per request.", "O(n)", "O(1)"),
  ("Sums with ceiling division.", "O(n)", "O(1)"),
  viz=((2048, [100, 400], 16)))


@B
def shared_prefix(prefix, extras, block):
    p_blocks = prefix // block
    without = 0
    with_sharing = p_blocks
    for e in extras:
        e_blocks = e // block + (1 if e % block else 0)
        without += p_blocks + e_blocks
        with_sharing += e_blocks
    return (without, with_sharing)


@O
def shared_prefix(prefix, extras, block):
    p = prefix // block
    own = sum(-(-e // block) for e in extras)
    return (p * len(extras) + own, p + own)


Q(None, "How Many GPUs for the Traffic?", "Medium", "Little's law",
  "Requests arrive at <code>rps</code> per second and each takes <code>secs</code> seconds on a server that handles <code>per_gpu</code> requests at once. Keep utilisation at most <code>util</code>. Return the number of GPUs (round up).",
  [((20, 6, 32, 0.7), 6), ((5, 2, 64, 0.7), 1)],
  ("In-flight = rps × secs, then divide by usable capacity per GPU.", "O(1)", "O(1)"),
  ("<code>math.ceil</code> of one expression.", "O(1)", "O(1)"),
  viz=((20, 6, 32, 0.7)))


@B
def gpus_needed(rps, secs, per_gpu, util):
    in_flight = rps * secs
    usable = per_gpu * util
    n = 1
    while n * usable < in_flight:
        n += 1
    return n


@O
def gpus_needed(rps, secs, per_gpu, util):
    return max(1, math.ceil(round(rps * secs / (per_gpu * util), 9)))


BATCH_TABLE = [(1, 95, 95), (8, 80, 640), (32, 52, 1664), (64, 31, 1984), (128, 17, 2176)]


Q(None, "Throughput vs Per-User Speed", "Easy", "Picking a batch size",
  "<code>BATCH_TABLE</code> rows are <code>(batch size, tokens/s per user, total tokens/s)</code>. Pick the batch size with the highest total throughput while each user still gets at least <code>min_user_tps</code>.",
  [((40,), 32), ((10,), 128), ((100,), None)],
  ("Loop and keep the best valid row.", "O(r)", "O(1)"),
  ("<code>max</code> over a filtered generator, with a default.", "O(r)", "O(1)"),
  viz=((40,)))


@B
def pick_batch(min_user_tps):
    best = None
    for b, user, total in BATCH_TABLE:
        if user >= min_user_tps and (best is None or total > best[2]):
            best = (b, user, total)
    return best[0] if best else None


@O
def pick_batch(min_user_tps):
    ok = [r for r in BATCH_TABLE if r[1] >= min_user_tps]
    return max(ok, key=lambda r: r[2])[0] if ok else None


Q(None, "Cost per Million Tokens, Self-Hosted", "Easy", "Unit economics",
  "A GPU costs <code>usd_per_hour</code> and produces <code>tps</code> output tokens per second at <code>util</code> average utilisation. Return dollars per million output tokens, rounded to 3.",
  [((2.5, 2000, 0.6), 0.579), ((2.5, 2000, 0.1), 3.472)],
  ("Tokens per hour, then divide.", "O(1)", "O(1)"),
  ("One expression.", "O(1)", "O(1)"),
  viz=((2.5, 2000, 0.6)))


@B
def self_host_cost(usd_per_hour, tps, util):
    tokens_per_hour = tps * 3600 * util
    return round(usd_per_hour / tokens_per_hour * 1_000_000, 3)


@O
def self_host_cost(usd_per_hour, tps, util):
    return round(usd_per_hour * 1e6 / (tps * 3600 * util), 3)


Q(None, "Self-Host or Use an API?", "Medium", "Break-even volume",
  "Self-hosting costs a fixed <code>fixed_month</code> per month (GPUs, engineers) and the API costs <code>api_per_m</code> dollars per million tokens. Return the monthly volume (millions of tokens, rounded up) above which self-hosting is cheaper, and the cheaper option at <code>volume</code> million tokens.",
  [((12000, 6.0, 500), (2000, 'api')), ((12000, 6.0, 5000), (2000, 'self-host'))],
  ("Divide, then compare costs.", "O(1)", "O(1)"),
  ("One expression each.", "O(1)", "O(1)"),
  viz=((12000, 6.0, 500)))


@B
def break_even(fixed_month, api_per_m, volume):
    even = fixed_month / api_per_m
    if even != int(even):
        even = int(even) + 1
    choice = "self-host" if volume * api_per_m > fixed_month else "api"
    return (int(even), choice)


@O
def break_even(fixed_month, api_per_m, volume):
    return (math.ceil(fixed_month / api_per_m), "self-host" if volume * api_per_m > fixed_month else "api")


Q(None, "Shortest Job First", "Medium", "Scheduling",
  "All requests arrive together and run one at a time; <code>lengths</code> are their run times. Return the average waiting time (rounded to 2) for first-come-first-served and for shortest-job-first.",
  [(([40, 2, 15, 3, 8],), (39.8, 9.6))],
  ("Accumulate start times in a loop for each order.", "O(n log n)", "O(n)"),
  ("<code>itertools.accumulate</code> gives each job's start time.", "O(n log n)", "O(n)"),
  viz=([40, 2, 15],))


@B
def avg_wait(lengths):
    def wait(order):
        t, total = 0, 0
        for L in order:
            total += t
            t += L
        return total / len(order)
    return (round(wait(lengths), 2), round(wait(sorted(lengths)), 2))


@O
def avg_wait(lengths):
    from itertools import accumulate
    wait = lambda order: sum(accumulate([0] + order[:-1])) / len(order)
    return (round(wait(lengths), 2), round(wait(sorted(lengths)), 2))


Q(None, "A Token Bucket Rate Limiter", "Medium", "Tokens per minute",
  "Allow at most <code>capacity</code> tokens in the bucket, refilled at <code>rate</code> tokens per second (starting full). Each request <code>(time, tokens)</code> is accepted if the bucket holds enough, and then those tokens are removed. Return accept/reject booleans.",
  [(([(0, 600), (1, 600), (2, 300), (10, 800), (10.5, 300)], 1000, 50), [True, False, True, False, True])],
  ("Track the level and the last time.", "O(n)", "O(1)"),
  ("Same, with <code>min</code> for the refill.", "O(n)", "O(1)"),
  viz=([(0, 600), (1, 600), (2, 300)], 1000, 50))


@B
def token_bucket(requests, capacity, rate):
    level, last, out = capacity, 0, []
    for t, need in requests:
        level = level + (t - last) * rate
        if level > capacity:
            level = capacity
        last = t
        if need <= level:
            level -= need
            out.append(True)
        else:
            out.append(False)
    return out


@O
def token_bucket(requests, capacity, rate):
    level, last, out = capacity, 0, []
    for t, need in requests:
        level, last = min(capacity, level + (t - last) * rate), t
        ok = need <= level
        level -= need if ok else 0
        out.append(ok)
    return out


Q(None, "Fall Back When a Model Fails", "Easy", "Resilience",
  "Try models in order; <code>status[model]</code> says whether it succeeds and <code>latency[model]</code> how long the attempt takes (a failure still costs its latency). Return <code>(model that answered or None, total seconds)</code>.",
  [((["primary", "secondary", "small"], {"primary": False, "secondary": True, "small": True}, {"primary": 4.0, "secondary": 2.5, "small": 1.0}), ('secondary', 6.5)),
   ((["a", "b"], {"a": False, "b": False}, {"a": 1.0, "b": 1.5}), (None, 2.5))],
  ("A loop that adds latency and stops on success.", "O(m)", "O(1)"),
  ("Same loop with <code>for … else</code>.", "O(m)", "O(1)"),
  viz=((["primary", "secondary", "small"], {"primary": False, "secondary": True, "small": True}, {"primary": 4.0, "secondary": 2.5, "small": 1.0})))


@B
def fallback(models, status, latency):
    total = 0.0
    for m in models:
        total += latency[m]
        if status[m]:
            return (m, total)
    return (None, total)


@O
def fallback(models, status, latency):
    total = 0.0
    for m in models:
        total += latency[m]
        if status[m]:
            break
    else:
        m = None
    return (m, total)


Q(None, "Many Fine-Tunes on One GPU", "Easy", "Serving LoRA adapters",
  "Serving <code>n</code> customers' fine-tuned models: full copies cost <code>base_gb</code> each, while LoRA serving keeps one base model plus an adapter of <code>adapter_mb</code> MB per customer. Return <code>(GB for full copies, GB with adapters)</code>, rounded to 2.",
  [((50, 16, 40), (800, 18.0))],
  ("Two products.", "O(1)", "O(1)"),
  ("One tuple expression.", "O(1)", "O(1)"),
  viz=((50, 16, 40)))


@B
def adapters(n, base_gb, adapter_mb):
    full = n * base_gb
    lora = base_gb + n * adapter_mb / 1000
    return (round(full, 2), round(lora, 2))


@O
def adapters(n, base_gb, adapter_mb):
    return (round(n * base_gb, 2), round(base_gb + n * adapter_mb / 1000, 2))


Q(None, "Longest Context That Fits", "Medium", "Memory budgeting",
  "With <code>free_gb</code> GB left after weights, and KV cost <code>kv_kb_per_token</code> KB per token, return the longest context (tokens, rounded down to a multiple of 1,024) each of <code>batch</code> sequences can have.",
  [((40, 128, 8), 38912), ((40, 128, 1), 312320)],
  ("Compute tokens per sequence, then round down.", "O(1)", "O(1)"),
  ("Floor division twice.", "O(1)", "O(1)"),
  viz=((40, 128, 8)))


@B
def max_context(free_gb, kv_kb_per_token, batch):
    tokens = free_gb * 1e6 / kv_kb_per_token / batch
    tokens = int(tokens)
    return tokens - tokens % 1024


@O
def max_context(free_gb, kv_kb_per_token, batch):
    return int(free_gb * 1e6 // (kv_kb_per_token * batch)) // 1024 * 1024
