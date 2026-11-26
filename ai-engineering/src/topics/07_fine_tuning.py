from lib import *
import math
import numpy as np


TOPIC(
    id="fine-tuning", title="Fine-Tuning in Practice: LoRA, QLoRA & DPO", glyph="∂W",
    blurb="Adapt open models yourself: when to fine-tune, LoRA maths and merging, memory for full vs LoRA vs QLoRA, chat templates and loss masking, packing, cleaning and de-duplicating data, schedules and batch sizes, preference data and the DPO loss, early stopping and checking for forgetting.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">h = x @ W + (alpha / r) * (x @ A) @ B            # LoRA: W frozen; A (d×r) and B (r×k) trained; B starts at 0
trainable = r × (d + k)   vs   d × k               # per adapted matrix
DPO loss = −log σ(β [(log π(y_w) − log π_ref(y_w)) − (log π(y_l) − log π_ref(y_l))])

from peft import LoraConfig, get_peft_model
model = get_peft_model(model, LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"]))
# TRL: SFTTrainer for supervised fine-tuning, DPOTrainer for preference tuning</code></pre>
""")


Q(None, "How Small Is a LoRA Adapter?", "Easy", "Parameter counts",
  "LoRA replaces training a d×k matrix with two small matrices A (d×r) and B (r×k). Return <code>(full params, LoRA params, LoRA as % of full rounded to 3)</code>.",
  [((4096, 4096, 16), (16777216, 131072, 0.781)), ((4096, 14336, 8), (58720256, 147456, 0.251))],
  ("Multiply step by step.", "O(1)", "O(1)"),
  ("One tuple expression.", "O(1)", "O(1)"),
  viz=((4096, 4096, 16)))


@B
def lora_params(d, k, r):
    full = d * k
    lora = d * r + r * k
    return (full, lora, round(lora / full * 100, 3))


@O
def lora_params(d, k, r):
    return (d * k, r * (d + k), round(r * (d + k) / (d * k) * 100, 3))


Q(None, "Trainable Share of a Whole Model", "Medium", "Choosing target modules",
  "A model has <code>layers</code> layers; in each, LoRA adapts the matrices in <code>shapes</code> (name → (d, k)). Return <code>(trainable LoRA params, % of the model's <code>total_b</code> billion params, rounded to 3)</code>.",
  [((32, {"q_proj": (4096, 4096), "k_proj": (4096, 1024), "v_proj": (4096, 1024), "o_proj": (4096, 4096)}, 16, 8.0), (13631488, 0.17)),
   ((32, {"q_proj": (4096, 4096), "v_proj": (4096, 1024)}, 8, 8.0), (3407872, 0.043))],
  ("Nested loop over layers and matrices.", "O(L · m)", "O(1)"),
  ("Per-layer sum times the number of layers.", "O(m)", "O(1)"),
  viz=((32, {"q_proj": (4096, 4096), "v_proj": (4096, 1024)}, 8, 8.0)))


@B
def model_lora(layers, shapes, r, total_b):
    n = 0
    for _ in range(layers):
        for d, k in shapes.values():
            n += r * (d + k)
    return (n, round(n / (total_b * 1e9) * 100, 3))


@O
def model_lora(layers, shapes, r, total_b):
    n = layers * sum(r * (d + k) for d, k in shapes.values())
    return (n, round(n / (total_b * 1e9) * 100, 3))


rng = np.random.default_rng(0)
X = np.round(rng.normal(size=(2, 4)), 2).tolist()
W0 = np.round(rng.normal(size=(4, 3)), 2).tolist()
A0 = np.round(rng.normal(size=(4, 2)) * 0.1, 3).tolist()
B0 = np.round(rng.normal(size=(2, 3)) * 0.1, 3).tolist()


Q(None, "The LoRA Forward Pass", "Medium", "x W + (α/r) x A B",
  "Compute the LoRA layer output h = x·W + (alpha / r)·(x·A)·B, rounded to 4. r is the number of columns of A.",
  [((X, W0, A0, B0, 16), [[-0.9509, -0.2796, -0.3356], [-1.5245, -0.6897, 0.4585]])],
  ("Matrix multiplication with nested loops.", "O(n·d·k)", "O(n·k)"),
  ("NumPy <code>@</code>. Note it never forms the full d×k update.", "O(n·d·(k + r))", "O(n·k)"),
  viz=((X, W0, A0, B0, 16)))


@B
def lora_forward(x, W, A, B, alpha):
    def matmul(P, Q):
        return [[sum(P[i][t] * Q[t][j] for t in range(len(Q))) for j in range(len(Q[0]))] for i in range(len(P))]
    r = len(A[0])
    base = matmul(x, W)
    delta = matmul(matmul(x, A), B)
    return [[round(base[i][j] + alpha / r * delta[i][j], 4) for j in range(len(base[0]))] for i in range(len(base))]


@O
def lora_forward(x, W, A, B, alpha):
    x, W, A, B = map(np.array, (x, W, A, B))
    return np.round(x @ W + alpha / A.shape[1] * (x @ A) @ B, 4).tolist()


Q(None, "Merge the Adapter for Serving", "Medium", "W' = W + (α/r)·A·B",
  "After training, LoRA can be folded into the weights so serving has no extra cost. Return <code>(merged W rounded to 4, max |difference| between x·W' and the LoRA forward, rounded to 8)</code>.",
  [((X, W0, A0, B0, 16), ([[-0.7182, -1.2898, -0.5503], [0.0588, -2.3463, -0.1507], [-1.2846, -0.7153, -0.6088], [-0.2773, 0.4088, 1.06]], 0.0))],
  ("Nested loops to build W', then compare outputs.", "O(d·k·r)", "O(d·k)"),
  ("NumPy outer product of A and B.", "O(d·k·r)", "O(d·k)"),
  viz=((X, W0, A0, B0, 16)))


@B
def merge(x, W, A, B, alpha):
    r = len(A[0])
    merged = [[W[i][j] + alpha / r * sum(A[i][t] * B[t][j] for t in range(r)) for j in range(len(W[0]))] for i in range(len(W))]
    out_merged = [[sum(x[n][i] * merged[i][j] for i in range(len(W))) for j in range(len(W[0]))] for n in range(len(x))]
    out_lora = np.array(x) @ np.array(W) + alpha / r * (np.array(x) @ np.array(A)) @ np.array(B)
    diff = max(abs(out_merged[n][j] - out_lora[n][j]) for n in range(len(x)) for j in range(len(W[0])))
    return ([[round(v, 4) for v in row] for row in merged], round(float(diff), 8))


@O
def merge(x, W, A, B, alpha):
    x, W, A, B = map(np.array, (x, W, A, B))
    merged = W + alpha / A.shape[1] * A @ B
    diff = np.abs(x @ merged - (x @ W + alpha / A.shape[1] * (x @ A) @ B)).max()
    return (np.round(merged, 4).tolist(), round(float(diff), 8))


Q(None, "Why B Starts at Zero", "Easy", "Safe initialisation",
  "LoRA initialises A randomly and B to zeros, so at step 0 the adapted model behaves exactly like the original. Return <code>(max |LoRA output − base output| with B = 0, the same with B random)</code>, rounded to 6.",
  [((X, W0, A0, B0, 16), (0.0, 0.0831))],
  ("Compute both outputs with loops.", "O(n·d·k)", "O(n·k)"),
  ("NumPy, with <code>np.zeros_like(B)</code>.", "O(n·d·k)", "O(n·k)"),
  viz=((X, W0, A0, B0, 16)))


@B
def zero_init(x, W, A, B, alpha):
    x, W, A, B = map(np.array, (x, W, A, B))
    r = A.shape[1]
    base = x @ W
    zero_B = [[0.0] * B.shape[1] for _ in range(B.shape[0])]
    with_zero = base + alpha / r * (x @ A) @ np.array(zero_B)
    with_rand = base + alpha / r * (x @ A) @ B
    return (round(float(abs(with_zero - base).max()), 6), round(float(abs(with_rand - base).max()), 6))


@O
def zero_init(x, W, A, B, alpha):
    x, W, A, B = map(np.array, (x, W, A, B))
    r = A.shape[1]
    out = lambda Bm: x @ W + alpha / r * (x @ A) @ Bm
    return (round(float(np.abs(out(np.zeros_like(B)) - x @ W).max()), 6), round(float(np.abs(out(B) - x @ W).max()), 6))


Q(None, "Will Training Fit on the GPU?", "Medium", "Full vs LoRA vs QLoRA memory",
  "Rough training memory in GB for a <code>params_b</code>-billion model (activations ignored): <b>full</b> = weights bf16 (2 bytes) + gradients bf16 (2) + Adam states fp32 (8) + fp32 master weights (4) per param; <b>LoRA</b> = frozen bf16 weights (2/param) + 16 bytes per trainable LoRA param; <b>QLoRA</b> = 4-bit frozen weights (0.5/param) + 16 bytes per LoRA param. Return the three, rounded to 1.",
  [((8, 40_000_000), (128, 16.6, 4.6)), ((70, 200_000_000), (1120, 143.2, 38.2))],
  ("Add the parts step by step.", "O(1)", "O(1)"),
  ("Three expressions.", "O(1)", "O(1)"),
  viz=((8, 40_000_000)))


@B
def train_memory(params_b, lora_params_n):
    p = params_b * 1e9
    full = (p * 2 + p * 2 + p * 8 + p * 4) / 1e9
    lora = (p * 2 + lora_params_n * 16) / 1e9
    qlora = (p * 0.5 + lora_params_n * 16) / 1e9
    return (round(full, 1), round(lora, 1), round(qlora, 1))


@O
def train_memory(params_b, lora_params_n):
    extra = lora_params_n * 16 / 1e9
    return (round(params_b * 16, 1), round(params_b * 2 + extra, 1), round(params_b * 0.5 + extra, 1))


Q(None, "Apply a Chat Template", "Easy", "Formatting training data",
  "Fine-tuning data must use the model's own chat format. Render messages as <code>&lt;|role|&gt;\\ncontent&lt;|end|&gt;\\n</code> for each, and end with <code>&lt;|assistant|&gt;\\n</code> if <code>add_generation_prompt</code>. (Real models each have their own template; <code>tokenizer.apply_chat_template</code> applies it.)",
  [(([{"role": "system", "content": "Be brief."}, {"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello!"}], False), '<|system|>\nBe brief.<|end|>\n<|user|>\nHi<|end|>\n<|assistant|>\nHello!<|end|>\n'),
   (([{"role": "user", "content": "2+2?"}], True), '<|user|>\n2+2?<|end|>\n<|assistant|>\n')],
  ("String concatenation in a loop.", "O(n)", "O(n)"),
  ("<code>''.join</code> over f-strings.", "O(n)", "O(n)"),
  viz=(([{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello!"}], False)))


@B
def chat_template(messages, add_generation_prompt):
    text = ""
    for m in messages:
        text += "<|" + m["role"] + "|>\n" + m["content"] + "<|end|>\n"
    if add_generation_prompt:
        text += "<|assistant|>\n"
    return text


@O
def chat_template(messages, add_generation_prompt):
    return "".join(f"<|{m['role']}|>\n{m['content']}<|end|>\n" for m in messages) + ("<|assistant|>\n" if add_generation_prompt else "")


Q(None, "Only Learn From the Assistant's Words", "Medium", "Loss masking",
  "In supervised fine-tuning, the loss is usually computed only on assistant tokens — the model shouldn't learn to imitate the user. Given per-token losses and each token's role, return <code>(mean loss over all tokens, mean over assistant tokens)</code>, rounded to 4.",
  [(([2.1, 1.9, 2.4, 0.6, 0.4, 0.5, 3.0, 0.7], ["user", "user", "user", "assistant", "assistant", "assistant", "user", "assistant"]), (1.45, 0.55))],
  ("Loop with a mask.", "O(n)", "O(1)"),
  ("NumPy boolean mask.", "O(n)", "O(n)"),
  viz=(([2.1, 1.9, 0.6, 0.4], ["user", "user", "assistant", "assistant"])))


@B
def masked_loss(losses, roles):
    total = n = 0
    for l, r in zip(losses, roles):
        if r == "assistant":
            total += l
            n += 1
    return (round(sum(losses) / len(losses), 4), round(total / n, 4))


@O
def masked_loss(losses, roles):
    l, mask = np.array(losses), np.array(roles) == "assistant"
    return (round(float(l.mean()), 4), round(float(l[mask].mean()), 4))


Q(None, "Pack Short Examples Together", "Medium", "Packing",
  "Training runs on fixed-length sequences of <code>max_len</code> tokens. Pack examples (in order) into sequences first-fit: each goes into the first sequence with room, else a new one. Return <code>(sequences used, % of tokens that are padding rounded to 1)</code>.",
  [(([900, 300, 1500, 200, 700, 1800, 100, 400], 2048), (4, 28.0))],
  ("A list of remaining space per sequence, scanned for each example.", "O(n · s)", "O(s)"),
  ("Same first-fit with <code>next</code> over enumerated free space.", "O(n · s)", "O(s)"),
  viz=([900, 300, 1500, 200], 2048))


@B
def pack(lengths, max_len):
    free = []
    for L in lengths:
        placed = False
        for i in range(len(free)):
            if free[i] >= L:
                free[i] -= L
                placed = True
                break
        if not placed:
            free.append(max_len - L)
    return (len(free), round(sum(free) / (len(free) * max_len) * 100, 1))


@O
def pack(lengths, max_len):
    free = []
    for L in lengths:
        i = next((i for i, f in enumerate(free) if f >= L), None)
        if i is None:
            free.append(max_len - L)
        else:
            free[i] -= L
    return (len(free), round(sum(free) / (len(free) * max_len) * 100, 1))


Q(None, "Clean the Training Set", "Medium", "Data quality",
  "Drop examples that are (in this order of checks) missing a response ('empty'), have a prompt plus response longer than <code>max_chars</code> ('too long'), are exact duplicates of an earlier example ('duplicate'), or whose prompt appears in the eval set ('eval leak'). Return <code>(kept count, {reason: count})</code>.",
  [(([("hi", "hello"), ("2+2", ""), ("hi", "hello"), ("long " * 50, "x"), ("capital of France", "Paris"), ("refund?", "10 days")], ["capital of France"], 100), (2, {'empty': 1, 'duplicate': 1, 'too long': 1, 'eval leak': 1}))],
  ("An if-chain with a seen set.", "O(n)", "O(n)"),
  ("A rule list of (reason, test) checked in order.", "O(n · r)", "O(n)"),
  viz=(([("hi", "hello"), ("2+2", ""), ("hi", "hello")], [], 100)))


@B
def clean_data(examples, eval_prompts, max_chars):
    seen, kept, reasons = set(), 0, {}
    for p, r in examples:
        reason = None
        if not r.strip():
            reason = "empty"
        elif len(p) + len(r) > max_chars:
            reason = "too long"
        elif (p, r) in seen:
            reason = "duplicate"
        elif p in eval_prompts:
            reason = "eval leak"
        seen.add((p, r))
        if reason:
            reasons[reason] = reasons.get(reason, 0) + 1
        else:
            kept += 1
    return (kept, reasons)


@O
def clean_data(examples, eval_prompts, max_chars):
    from collections import Counter
    seen, kept, reasons, evals = set(), 0, Counter(), set(eval_prompts)
    for p, r in examples:
        rules = [("empty", not r.strip()), ("too long", len(p) + len(r) > max_chars),
                 ("duplicate", (p, r) in seen), ("eval leak", p in evals)]
        reason = next((name for name, hit in rules if hit), None)
        seen.add((p, r))
        if reason:
            reasons[reason] += 1
        else:
            kept += 1
    return (kept, dict(reasons))


Q(None, "Warm-Up Then Cosine", "Easy", "Learning-rate schedule",
  "The learning rate rises linearly from 0 to <code>peak</code> over <code>warmup</code> steps, then follows a cosine down to 0 at <code>total</code> steps. Return the rate at each step in <code>steps</code> in <b>millionths</b> (rate × 10⁶), rounded to 2.",
  [((2e-4, 100, 1000, [0, 50, 100, 550, 1000]), [0.0, 100.0, 200.0, 100.0, 0.0])],
  ("An if/else per step.", "O(s)", "O(s)"),
  ("A helper function and a comprehension.", "O(s)", "O(s)"),
  viz=((2e-4, 100, 1000, [0, 50, 100, 550, 1000])))


@B
def lr_schedule(peak, warmup, total, steps):
    out = []
    for s in steps:
        if s < warmup:
            lr = peak * s / warmup
        else:
            progress = (s - warmup) / (total - warmup)
            lr = peak * 0.5 * (1 + math.cos(math.pi * progress))
        out.append(round(lr * 1e6, 2))
    return out


@O
def lr_schedule(peak, warmup, total, steps):
    lr = lambda s: peak * s / warmup if s < warmup else peak * 0.5 * (1 + math.cos(math.pi * (s - warmup) / (total - warmup)))
    return [round(lr(s) * 1e6, 2) for s in steps]


Q(None, "Batch Size and Steps", "Easy", "Gradient accumulation",
  "Effective batch = per-device batch × accumulation steps × GPUs. Return <code>(effective batch, optimizer steps per epoch rounded up, total steps for <code>epochs</code>)</code> for <code>n</code> examples.",
  [((4, 8, 2, 10000, 3), (64, 157, 471)), ((1, 16, 1, 1200, 2), (16, 75, 150))],
  ("Multiply, then ceiling divide.", "O(1)", "O(1)"),
  ("<code>math.ceil</code>.", "O(1)", "O(1)"),
  viz=((4, 8, 2, 10000, 3)))


@B
def batch_steps(per_device, accum, gpus, n, epochs):
    eff = per_device * accum * gpus
    per_epoch = n // eff
    if n % eff:
        per_epoch += 1
    return (eff, per_epoch, per_epoch * epochs)


@O
def batch_steps(per_device, accum, gpus, n, epochs):
    eff = per_device * accum * gpus
    return (eff, math.ceil(n / eff), math.ceil(n / eff) * epochs)


Q(None, "The DPO Loss for One Pair", "Medium", "Preference tuning",
  "Direct Preference Optimisation pushes the model to prefer the chosen answer over the rejected one <i>relative to a frozen reference model</i>. Given log-probabilities, return <code>(loss, implicit reward margin)</code> rounded to 4, where margin = β·[(lp_chosen − ref_chosen) − (lp_rejected − ref_rejected)] and loss = −log σ(margin).",
  [((-12.0, -15.0, -13.0, -14.0, 0.1), (0.5981, 0.2)), ((-14.0, -12.0, -13.0, -13.0, 0.1), (0.7981, -0.2))],
  ("Compute the margin, then the sigmoid by hand.", "O(1)", "O(1)"),
  ("Use the stable form −log σ(m) = log(1 + e^(−m)) via <code>np.logaddexp(0, −m)</code>.", "O(1)", "O(1)"),
  viz=((-12.0, -15.0, -13.0, -14.0, 0.1)))


@B
def dpo_loss(lp_chosen, lp_rejected, ref_chosen, ref_rejected, beta):
    margin = beta * ((lp_chosen - ref_chosen) - (lp_rejected - ref_rejected))
    sigmoid = 1 / (1 + math.exp(-margin))
    return (round(-math.log(sigmoid), 4), round(margin, 4))


@O
def dpo_loss(lp_chosen, lp_rejected, ref_chosen, ref_rejected, beta):
    m = beta * ((lp_chosen - ref_chosen) - (lp_rejected - ref_rejected))
    return (round(float(np.logaddexp(0, -m)), 4), round(m, 4))


Q(None, "A Batch of Preference Pairs", "Medium", "DPO metrics",
  "For a batch of pairs <code>(lp_chosen, lp_rejected, ref_chosen, ref_rejected)</code> return <code>(mean DPO loss, reward accuracy)</code> rounded to 4, where reward accuracy is the share of pairs with a positive margin — the main number to watch during DPO training.",
  [(([(-12, -15, -13, -14), (-14, -12, -13, -13), (-10, -20, -11, -18), (-9, -9, -10, -10)], 0.1), (0.6609, 0.5))],
  ("Loop over pairs.", "O(n)", "O(1)"),
  ("NumPy arrays for the whole batch.", "O(n)", "O(n)"),
  viz=(([(-12, -15, -13, -14), (-14, -12, -13, -13)], 0.1)))


@B
def dpo_batch(pairs, beta):
    total, correct = 0.0, 0
    for c, r, rc, rr in pairs:
        m = beta * ((c - rc) - (r - rr))
        total += math.log(1 + math.exp(-m))
        if m > 0:
            correct += 1
    return (round(total / len(pairs), 4), round(correct / len(pairs), 4))


@O
def dpo_batch(pairs, beta):
    c, r, rc, rr = np.array(pairs, dtype=float).T
    m = beta * ((c - rc) - (r - rr))
    return (round(float(np.logaddexp(0, -m).mean()), 4), round(float((m > 0).mean()), 4))


Q(None, "Build Preference Pairs From Ratings", "Medium", "Preference data",
  "Each prompt has several rated responses. Make one pair per prompt — the best-rated as 'chosen', the worst as 'rejected' — but only if the rating gap is at least <code>min_gap</code> (small gaps are noise). Return <code>[(prompt, chosen, rejected)]</code>.",
  [(({"p1": [("a", 4.5), ("b", 2.0), ("c", 3.9)], "p2": [("d", 3.0), ("e", 3.2)], "p3": [("f", 5.0), ("g", 1.0)]}, 1.0), [('p1', 'a', 'b'), ('p3', 'f', 'g')])],
  ("Find max and min by looping.", "O(n)", "O(p)"),
  ("<code>max</code> and <code>min</code> with a key.", "O(n)", "O(p)"),
  viz=(({"p1": [("a", 4.5), ("b", 2.0)], "p2": [("d", 3.0), ("e", 3.2)]}, 1.0)))


@B
def make_pairs(ratings, min_gap):
    out = []
    for prompt, responses in ratings.items():
        best = worst = responses[0]
        for resp in responses:
            if resp[1] > best[1]:
                best = resp
            if resp[1] < worst[1]:
                worst = resp
        if best[1] - worst[1] >= min_gap:
            out.append((prompt, best[0], worst[0]))
    return out


@O
def make_pairs(ratings, min_gap):
    out = []
    for prompt, rs in ratings.items():
        best, worst = max(rs, key=lambda r: r[1]), min(rs, key=lambda r: r[1])
        if best[1] - worst[1] >= min_gap:
            out.append((prompt, best[0], worst[0]))
    return out


Q(None, "Stop Before It Overfits", "Easy", "Early stopping",
  "Validation loss per epoch is given. Stop once it hasn't improved for <code>patience</code> epochs. Return <code>(best epoch, its loss, epoch at which training stops)</code> (epochs counted from 1).",
  [(([1.9, 1.5, 1.32, 1.28, 1.30, 1.35, 1.41, 1.5], 2), (4, 1.28, 6)), (([2.0, 1.8, 1.6], 2), (3, 1.6, 3))],
  ("A loop tracking best and a counter.", "O(e)", "O(1)"),
  ("Same loop with <code>enumerate(…, 1)</code>.", "O(e)", "O(1)"),
  viz=([1.9, 1.5, 1.32, 1.28, 1.30, 1.35], 2))


@B
def early_stop(val_losses, patience):
    best, best_epoch, waited = float("inf"), 0, 0
    stop = len(val_losses)
    for i in range(len(val_losses)):
        if val_losses[i] < best:
            best, best_epoch, waited = val_losses[i], i + 1, 0
        else:
            waited += 1
            if waited >= patience:
                stop = i + 1
                break
    return (best_epoch, best, stop)


@O
def early_stop(val_losses, patience):
    best, best_epoch = float("inf"), 0
    for epoch, loss in enumerate(val_losses, 1):
        if loss < best:
            best, best_epoch = loss, epoch
        elif epoch - best_epoch >= patience:
            return (best_epoch, best, epoch)
    return (best_epoch, best, len(val_losses))


Q(None, "Did It Forget Everything Else?", "Easy", "Catastrophic forgetting",
  "Compare benchmark scores before and after fine-tuning. Return <code>(target task gain rounded to 1, general benchmarks that dropped by more than <code>tol</code> points)</code>.",
  [(({"target": 61.0, "reasoning": 72.0, "coding": 55.0, "safety": 93.0}, {"target": 84.5, "reasoning": 70.5, "coding": 47.0, "safety": 86.0}, 2.0), (23.5, ['coding', 'safety']))],
  ("Loop over benchmarks.", "O(b)", "O(b)"),
  ("A comprehension.", "O(b)", "O(b)"),
  viz=(({"target": 61.0, "coding": 55.0}, {"target": 84.5, "coding": 47.0}, 2.0)))


@B
def forgetting(before, after, tol):
    dropped = []
    for b in before:
        if b != "target" and before[b] - after[b] > tol:
            dropped.append(b)
    return (round(after["target"] - before["target"], 1), dropped)


@O
def forgetting(before, after, tol):
    return (round(after["target"] - before["target"], 1), [b for b in before if b != "target" and before[b] - after[b] > tol])


Q(None, "Prompt, RAG or Fine-Tune?", "Medium", "Choosing the technique",
  "Recommend an approach from a problem's traits, in this order: needs fresh or private facts → 'RAG'; needs a new skill, format or style learned from many examples and you have ≥ 500 examples → 'fine-tune'; needs lower cost/latency at high volume and you have ≥ 500 examples → 'fine-tune a smaller model (distil)'; otherwise 'prompt engineering'.",
  [(({"fresh_facts": True, "examples": 5000},), 'RAG'), (({"new_format": True, "examples": 2000},), 'fine-tune'), (({"new_format": True, "examples": 50},), 'prompt engineering'),
   (({"cost_pressure": True, "examples": 20000},), 'fine-tune a smaller model (distil)')],
  ("An if-chain.", "O(1)", "O(1)"),
  ("An ordered rule list.", "O(r)", "O(r)"),
  viz=(({"new_format": True, "examples": 2000},)))


@B
def choose_technique(t):
    many = t.get("examples", 0) >= 500
    if t.get("fresh_facts"):
        return "RAG"
    if t.get("new_format") and many:
        return "fine-tune"
    if t.get("cost_pressure") and many:
        return "fine-tune a smaller model (distil)"
    return "prompt engineering"


@O
def choose_technique(t):
    many = t.get("examples", 0) >= 500
    rules = [(t.get("fresh_facts"), "RAG"), (t.get("new_format") and many, "fine-tune"),
             (t.get("cost_pressure") and many, "fine-tune a smaller model (distil)")]
    return next((name for ok, name in rules if ok), "prompt engineering")


Q(None, "What Does a Distillation Dataset Cost?", "Easy", "Synthetic data",
  "Generate <code>n</code> training examples with a large teacher model: each call reads <code>inp</code> tokens and writes <code>out</code> tokens, at prices per million tokens. A batch API halves the price. Return <code>(cost, cost with batch discount)</code> in dollars rounded to 2.",
  [((20000, 600, 400, 3.0, 15.0), (156.0, 78.0))],
  ("Multiply step by step.", "O(1)", "O(1)"),
  ("One expression.", "O(1)", "O(1)"),
  viz=((20000, 600, 400, 3.0, 15.0)))


@B
def distil_cost(n, inp, out, pin, pout):
    per = inp * pin / 1e6 + out * pout / 1e6
    total = per * n
    return (round(total, 2), round(total / 2, 2))


@O
def distil_cost(n, inp, out, pin, pout):
    total = n * (inp * pin + out * pout) / 1e6
    return (round(total, 2), round(total * 0.5, 2))


RANK_EVAL = {4: (71.2, 4.2), 8: (74.8, 8.4), 16: (76.1, 16.8), 32: (76.4, 33.6), 64: (76.5, 67.1)}


Q(None, "Choose the LoRA Rank", "Easy", "Good enough, smallest",
  "<code>RANK_EVAL[r] = (eval score, adapter size in MB)</code>. Return the smallest rank whose score is within <code>tol</code> points of the best score.",
  [((1.0,), 16), ((0.2,), 32), ((5.0,), 8)],
  ("Find the best, then loop over ranks in order.", "O(r)", "O(1)"),
  ("<code>min</code> over a filtered generator.", "O(r)", "O(1)"),
  viz=((1.0,)))


@B
def pick_rank(tol):
    best = max(score for score, _ in RANK_EVAL.values())
    for r in sorted(RANK_EVAL):
        if best - RANK_EVAL[r][0] <= tol:
            return r


@O
def pick_rank(tol):
    best = max(s for s, _ in RANK_EVAL.values())
    return min(r for r, (s, _) in RANK_EVAL.items() if best - s <= tol + 1e-9)
