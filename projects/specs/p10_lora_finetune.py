import numpy as np
import pandas as pd

CLASSES = ["billing", "delivery", "account", "technical"]
OLD = {"billing": ["price", "charged", "expensive", "payment", "refund", "invoice", "discount"],
       "delivery": ["shipping", "arrived", "late", "package", "courier", "box", "delayed"],
       "account": ["login", "password", "profile", "email", "signup", "username", "verify"],
       "technical": ["broken", "crash", "battery", "screen", "error", "update", "slow"]}
NEW = {"billing": ["paisa", "deducted", "upi", "emi", "cashback", "debited", "wallet"],
       "delivery": ["parcel", "rider", "pincode", "dispatch", "tracking", "pickup", "eta"],
       "account": ["otp", "kyc", "aadhaar", "blocked", "pin", "mobile", "relogin"],
       "technical": ["hang", "glitch", "lag", "bug", "freeze", "apk", "loading"]}
GENERIC = ["please", "help", "my", "the", "is", "not", "today", "again", "still", "very", "issue", "order"]


CONFLICT = {"billing": ["verify"], "delivery": ["update", "box"], "technical": ["screen"]}   # words whose meaning shifts in chats


def sentence(rng, cls, domain, mix=0.0):
    words = []
    for _ in range(int(rng.integers(3, 6))):
        pool = OLD if (domain == "old" or rng.random() < mix) else NEW
        words.append(rng.choice(pool[cls]))
    if domain == "new" and cls in CONFLICT and rng.random() < 0.6:
        words.append(rng.choice(CONFLICT[cls]))
    if rng.random() < 0.35:                                   # a distractor word from another intent
        other = rng.choice([c for c in CLASSES if c != cls])
        words.append(rng.choice((OLD if domain == "old" else NEW)[other]))
    words += list(rng.choice(GENERIC, int(rng.integers(1, 4))))
    rng.shuffle(words)
    return " ".join(words)


def frame(rng, n, domain, mix=0.0, noise=0.0):
    labels = rng.choice(len(CLASSES), n)
    texts = [sentence(rng, CLASSES[c], domain, mix) for c in labels]
    flip = rng.random(n) < noise                              # a few mislabelled examples, as in real data
    labels = np.where(flip, rng.choice(len(CLASSES), n), labels)
    return pd.DataFrame({"text": texts, "label": [CLASSES[c] for c in labels]})


def make_data(rng):
    vocab = sorted({w for d in (OLD, NEW) for ws in d.values() for w in ws} | set(GENERIC))
    old_train, old_test = frame(rng, 800, "old", noise=0.03), frame(rng, 200, "old", noise=0.03)
    new_train, new_test = frame(rng, 160, "new", mix=0.1, noise=0.08), frame(rng, 200, "new", mix=0.1, noise=0.08)
    extras = pd.concat([new_train.sample(12, random_state=1), new_test.sample(8, random_state=2),
                        pd.DataFrame({"text": ["", "  ", ""], "label": ["billing", "account", "delivery"]})])
    new_train = pd.concat([new_train, extras]).sample(frac=1, random_state=3).reset_index(drop=True)
    # "pre-train" the base model on the old domain: word embeddings (E) → average → classification head (H, b)
    idx = {w: i for i, w in enumerate(vocab)}
    X = np.zeros((len(old_train), len(vocab)))
    for r, t in enumerate(old_train.text):
        for w in t.split():
            X[r, idx[w]] += 1
    X /= X.sum(1, keepdims=True)
    Y = np.eye(4)[[CLASSES.index(l) for l in old_train.label]]
    g = np.random.default_rng(0)
    E, H, bias = g.normal(0, 0.1, (len(vocab), 32)), g.normal(0, 0.1, (32, 4)), np.zeros(4)
    for _ in range(800):
        h = X @ E
        z = h @ H + bias
        P = np.exp(z - z.max(1, keepdims=True))
        P /= P.sum(1, keepdims=True)
        G = (P - Y) / len(X)
        gH, gE = h.T @ G, X.T @ (G @ H.T)
        H, E, bias = H - gH, E - gE, bias - G.sum(0)
    embed = pd.DataFrame(np.round(E, 6), columns=[f"e{i}" for i in range(32)])
    embed.insert(0, "word", vocab)
    head = pd.DataFrame(np.round(np.vstack([H, bias]), 6), columns=CLASSES)
    head.insert(0, "row", [f"h{i}" for i in range(32)] + ["bias"])
    return {"ft_old_train.csv": old_train, "ft_old_test.csv": old_test, "ft_new_train.csv": new_train,
            "ft_new_test.csv": new_test,
            "ft_base_embed.csv": embed, "ft_base_head.csv": head}


QLORA = '''
# Real QLoRA fine-tuning of a small open LLM — run on a GPU (e.g. Colab T4/A100).
# pip install -U transformers peft trl bitsandbytes datasets accelerate
import torch
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig

model_id = "Qwen/Qwen2.5-0.5B-Instruct"                       # small enough for a free GPU
tok = AutoTokenizer.from_pretrained(model_id)
bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16)
model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb, device_map="auto")

rows = [{"messages": [{"role": "user", "content": f"Classify this support message: {t}"},
                      {"role": "assistant", "content": l}]} for t, l in zip(new_train.text, new_train.label)]
lora = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, target_modules="all-linear", task_type="CAUSAL_LM")
trainer = SFTTrainer(model=model, train_dataset=Dataset.from_list(rows), peft_config=lora, processing_class=tok,
                     args=SFTConfig(output_dir="out", num_train_epochs=3, learning_rate=2e-4,
                                    per_device_train_batch_size=8, logging_steps=10))
trainer.train()
trainer.save_model("intent-lora")        # saves only the small adapter
# Argument names change between library versions — check the TRL / PEFT docs for yours.
'''

PROJECT = dict(
    slug="lora-fine-tuning",
    title="Fine-Tune With LoRA: Adapt a Model to a New Domain",
    role="AI / ML Engineer",
    level="Advanced",
    hours="8–10",
    summary="A support-intent model trained on product reviews fails on Indian support chats. Clean the new data, implement LoRA training yourself, compare it with full fine-tuning, check forgetting, merge the adapter, pick the rank — then run the same recipe with QLoRA on a real LLM.",
    skills=["LoRA", "full vs parameter-efficient fine-tuning", "gradient descent", "data cleaning and leakage", "catastrophic forgetting", "adapter merging", "rank selection", "QLoRA with PEFT/TRL"],
    brief="""
**The situation.** *ShopKart*'s ticket router sends each message to the billing, delivery, account or technical team. It was trained on English product reviews ("charged twice, refund please") and works well there. But customers now write in support chat like *"paisa debited upi still"* or *"otp nahi aaya, kyc blocked"*, and the router gets many of them wrong.

You have only ~160 labelled chat messages. Retraining from scratch isn't an option, so you'll **fine-tune** the existing model — and compare two ways:

- **Full fine-tuning**: update every weight.
- **LoRA**: freeze the weights and learn a small low-rank update, the technique used to adapt large language models cheaply.

The model here is small enough to train on a laptop in seconds, so you can implement LoRA's maths yourself and see exactly what libraries like PEFT do. The last section runs the same recipe on a real LLM with QLoRA.
""",
    deliverable="a cleaned training set, a from-scratch LoRA trainer, a comparison table (accuracy on the new and old domains, trainable parameters) for the base model, LoRA and full fine-tuning, a merged adapter, a chosen rank, and a QLoRA script for a real LLM.",
    data_notes="""
| File | Rows | What |
|---|---|---|
| `ft_base_embed.csv` | one per word | the pre-trained **embedding matrix** E: a 32-number vector per word |
| `ft_base_head.csv` | 33 | the pre-trained **classification head** H (32 × 4) and, in the last row, the bias |
| `ft_old_train.csv` / `ft_old_test.csv` | 800 / 200 | the old domain (reviews) — used only to measure forgetting |
| `ft_new_train.csv` | ~180 | new-domain chat messages to fine-tune on (**messy**: blanks, duplicates, and some leaked test messages) |
| `ft_new_test.csv` | 200 | new-domain messages to evaluate on |

The model averages the embeddings of a message's words and feeds that through the head: logits = (x·E)·H + b, where x holds each word's share of the message. A large language model is the same idea with many more layers. LoRA adapts big matrices like E — exactly what you'll implement here.
""",
    setup="""
import matplotlib.pyplot as plt
embed, head = load("ft_base_embed.csv"), load("ft_base_head.csv")
old_train, old_test = load("ft_old_train.csv"), load("ft_old_test.csv")
new_train_raw, new_test = load("ft_new_train.csv").fillna(""), load("ft_new_test.csv")
CLASSES = ["billing", "delivery", "account", "technical"]
VOCAB = embed.word.tolist()
E0 = embed.drop(columns="word").to_numpy()           # (vocabulary, 32) pre-trained embeddings
H0 = head[CLASSES].to_numpy()[:-1]                   # (32, 4) classification head
B0 = head[CLASSES].to_numpy()[-1]                    # (4,) bias
STEPS, LR, SCALE = 300, 1.0, 2.0                     # SCALE = alpha / r with alpha = 2r


def softmax(z):
    e = np.exp(z - z.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)


def labels_of(df):
    return np.array([CLASSES.index(l) for l in df.label])


# Used by the checks: your functions chained together.
def data():
    tr = clean(new_train_raw, new_test)[0]
    return vectorise(tr.text), labels_of(tr), vectorise(new_test.text), labels_of(new_test), vectorise(old_test.text), labels_of(old_test)


def lora_result(r):
    X, y, Xt, yt, Xo, yo = data()
    A, B = train_lora(X, y, r)
    return [accuracy(E0 + SCALE * A @ B, H0, B0, Xt, yt), A.size + B.size]



def full_result():
    X, y, Xt, yt, Xo, yo = data()
    E, H, b = train_full(X, y)
    return [accuracy(E, H, b, Xt, yt), E.size + H.size + b.size]
""",
    milestones=[
        dict(title="Clean the fine-tuning data",
             task="""
Write `clean(train, test)` returning `(clean_train, {reason: count})`. Drop, checking in this order:
- `"empty"`: text that is blank after stripping,
- `"duplicate"`: an exact (text, label) repeat of an earlier row,
- `"leak"`: text that also appears in the **test** set — training on test messages would make your results look better than they are.

With only ~160 examples, every bad row matters.
""",
             starter="""
def clean(train, test):
    raise NotImplementedError
""",
             solution="""
def clean(train, test):
    test_texts = set(test.text)
    keep, reasons, seen = [], {}, set()
    for i, (text, label) in enumerate(zip(train.text, train.label)):
        if not str(text).strip():
            reason = "empty"
        elif (text, label) in seen:
            reason = "duplicate"
        elif text in test_texts:
            reason = "leak"
        else:
            reason = None
        seen.add((text, label))
        if reason:
            reasons[reason] = reasons.get(reason, 0) + 1
        else:
            keep.append(i)
    return train.iloc[keep].reset_index(drop=True), reasons
""",
             call="[len(clean(new_train_raw, new_test)[0]), clean(new_train_raw, new_test)[1]]", tol=1e-9),
        dict(title="Turn text into features",
             task="""
Write `vectorise(texts)` returning a NumPy array of shape (number of texts, len(VOCAB)) where entry [i, j] is the **share** of text i's known words that are `VOCAB[j]` (count ÷ number of known words; split on spaces, ignore unknown words, leave all-zero rows as zeros). Multiplying this by E averages the word embeddings.
""",
             starter="""
def vectorise(texts):
    raise NotImplementedError
""",
             solution="""
def vectorise(texts):
    index = {w: j for j, w in enumerate(VOCAB)}
    X = np.zeros((len(texts), len(VOCAB)))
    for i, t in enumerate(texts):
        for w in str(t).split():
            if w in index:
                X[i, index[w]] += 1
    totals = X.sum(axis=1, keepdims=True)
    return np.divide(X, totals, out=np.zeros_like(X), where=totals > 0)
""",
             call="[list(vectorise(['upi debited debited', 'hello world']).shape), [round(v, 4) for v in sorted(set(vectorise(['upi debited debited']).ravel().tolist()))], vectorise(['hello world']).sum()]", tol=1e-9),
        dict(title="How good is the base model?",
             task="""
Write `accuracy(E, H, b, X, y)` — the share of rows where `argmax((X @ E) @ H + b)` equals the label — rounded to 4.

The check measures the pre-trained model on the **old** test set and the **new** one. That gap is why you're fine-tuning.
""",
             starter="""
def accuracy(E, H, b, X, y):
    raise NotImplementedError
""",
             solution="""
def accuracy(E, H, b, X, y):
    return round(float(((X @ E @ H + b).argmax(axis=1) == y).mean()), 4)
""",
             call="(lambda X, y, Xt, yt, Xo, yo: [accuracy(E0, H0, B0, Xo, yo), accuracy(E0, H0, B0, Xt, yt)])(*data())", tol=1e-9),
        dict(title="Train a LoRA adapter yourself",
             task="""
Freeze `E0`, `H0` and `B0`. Learn A (vocabulary × r) and B (r × 32) so the embeddings become E0 + SCALE·A·B, and logits = X·(E0 + SCALE·A·B)·H0 + B0.

Write `train_lora(X, y, r, steps=STEPS, lr=LR)` returning `(A, B)`:
- initialise `A = np.random.default_rng(0).normal(0, 0.01, (len(VOCAB), r))` and `B = np.zeros((r, 32))`,
- each step: P = softmax(logits), G = (P − one_hot(y)) / n, U = G·H0ᵀ (the gradient reaching the embeddings), then
  `grad_B = SCALE · (X·A)ᵀ·U` and `grad_A = SCALE · Xᵀ·(U·Bᵀ)`, and subtract `lr ×` each (both from the old A and B).

The check trains with r = 4 and reports `[new-domain accuracy, trainable parameters]`.
""",
             hint="One-hot labels: `np.eye(4)[y]`. Compute `G` and `U` once per step and use them for both gradients.",
             starter="""
def train_lora(X, y, r, steps=STEPS, lr=LR):
    raise NotImplementedError
""",
             solution="""
def train_lora(X, y, r, steps=STEPS, lr=LR):
    A = np.random.default_rng(0).normal(0, 0.01, (len(VOCAB), r))
    B = np.zeros((r, 32))
    Y = np.eye(4)[y]
    for _ in range(steps):
        P = softmax(X @ (E0 + SCALE * A @ B) @ H0 + B0)
        U = (P - Y) / len(X) @ H0.T
        grad_B = SCALE * (X @ A).T @ U
        grad_A = SCALE * X.T @ (U @ B.T)
        A, B = A - lr * grad_A, B - lr * grad_B
    return A, B
""",
             call="lora_result(4)", tol=0.02,
             after="On the very first step A gets no gradient (B is zero), but B does — then A starts moving too. That's why LoRA can start at exactly the original model without being stuck."),
        dict(title="Compare with full fine-tuning",
             task="""
Write `train_full(X, y, steps=STEPS, lr=LR)` that starts from copies of `E0`, `H0` and `B0` and updates **all** of them with gradient descent on the same loss: with h = X·E and G as before, `grad_H = hᵀ·G`, `grad_E = Xᵀ·(G·Hᵀ)`, `grad_b = Σ G over rows`. Return `(E, H, b)`.

The check returns `[new accuracy, trainable parameters]`. Compare with LoRA.
""",
             starter="""
def train_full(X, y, steps=STEPS, lr=LR):
    raise NotImplementedError
""",
             solution="""
def train_full(X, y, steps=STEPS, lr=LR):
    E, H, b, Y = E0.copy(), H0.copy(), B0.copy(), np.eye(4)[y]
    for _ in range(steps):
        h = X @ E
        G = (softmax(h @ H + b) - Y) / len(X)
        grad_H, grad_E = h.T @ G, X.T @ (G @ H.T)
        E, H, b = E - lr * grad_E, H - lr * grad_H, b - lr * G.sum(axis=0)
    return E, H, b
""",
             call="full_result()", tol=0.02),
        dict(title="Did it forget the old domain? And merge the adapter",
             task="""
Write `forgetting_and_merge(r=4)` returning a dict:
- `old_base`, `old_lora`, `old_full`: accuracy on the **old** test set for the base model, the LoRA model and the fully fine-tuned model,
- `merge_identical`: whether predictions with the merged embeddings `E0 + SCALE·A·B` equal computing base and adapter separately (`X·E0 + SCALE·(X·A)·B`) on the new test set — the reason a merged LoRA costs nothing extra to serve.
""",
             starter="""
def forgetting_and_merge(r=4):
    raise NotImplementedError
""",
             solution="""
def forgetting_and_merge(r=4):
    X, y, Xt, yt, Xo, yo = data()
    A, B = train_lora(X, y, r)
    Ef, Hf, bf = train_full(X, y)
    merged = E0 + SCALE * A @ B
    separate = ((Xt @ E0 + SCALE * (Xt @ A) @ B) @ H0 + B0).argmax(axis=1)
    return {"old_base": accuracy(E0, H0, B0, Xo, yo), "old_lora": accuracy(merged, H0, B0, Xo, yo),
            "old_full": accuracy(Ef, Hf, bf, Xo, yo),
            "merge_identical": bool((separate == (Xt @ merged @ H0 + B0).argmax(axis=1)).all())}
""",
             call="forgetting_and_merge()", tol=0.02,
             after="Look closely: here LoRA forgot **more** of the old domain than full fine-tuning. The adapter could only change the word embeddings, and some words (\"update\", \"box\", \"screen\", \"verify\") mean different intents in the two domains — so it rewrote words the old domain relies on, while full fine-tuning could also adjust the head. \"LoRA forgets less\" is a tendency, not a law: always measure the old task after fine-tuning."),
        dict(title="Choose the rank",
             task="""
Write `rank_sweep(ranks=(1, 2, 4, 8, 16), tol=0.01)` that trains LoRA at each rank and returns `(chosen rank, {rank: new-domain accuracy})` — the chosen rank is the **smallest** whose accuracy is within `tol` of the best. Smaller adapters are cheaper to store, load and serve.
""",
             starter="""
def rank_sweep(ranks=(1, 2, 4, 8, 16), tol=0.01):
    raise NotImplementedError
""",
             solution="""
def rank_sweep(ranks=(1, 2, 4, 8, 16), tol=0.01):
    X, y, Xt, yt, Xo, yo = data()
    scores = {}
    for r in ranks:
        A, B = train_lora(X, y, r)
        scores[r] = accuracy(E0 + SCALE * A @ B, H0, B0, Xt, yt)
    best = max(scores.values())
    return [min(r for r in ranks if scores[r] >= best - tol - 1e-9), scores]
""",
             call="rank_sweep()", tol=0.02),
    ],
    extra=[("## A chart for your report", """
try:
    X, y, Xt, yt, Xo, yo = data()
    A, B = train_lora(X, y, 4)
    Ef, Hf, bf = train_full(X, y)
    rows = {"base": (E0, H0, B0), "LoRA r=4": (E0 + SCALE * A @ B, H0, B0), "full fine-tune": (Ef, Hf, bf)}
    new = [accuracy(*m, Xt, yt) for m in rows.values()]
    old = [accuracy(*m, Xo, yo) for m in rows.values()]
    x = np.arange(3)
    plt.figure(figsize=(7, 3))
    plt.bar(x - 0.2, new, 0.4, label="new domain (chats)", color="#0f766e")
    plt.bar(x + 0.2, old, 0.4, label="old domain (reviews)", color="#94a3b8")
    plt.xticks(x, rows.keys()); plt.ylim(0, 1); plt.ylabel("accuracy"); plt.legend(); plt.title("Fine-tuning: gain on new data, cost on old")
    plt.show()
except NotImplementedError:
    print("Finish the milestones above first — this chart uses your functions.")
"""),
           ("## Now do it on a real LLM with QLoRA\n\nThe same recipe — freeze the base, train low-rank adapters, evaluate on held-out data and the old task — applied to a 0.5B-parameter chat model, stored in 4 bits. Run this on a GPU runtime (in Colab: Runtime → Change runtime type → T4 GPU). It isn't run automatically here.\n\n```python\n" + QLORA.strip() + "\n```\n\nThen evaluate the tuned model on `new_test` by generating a label for each message and computing accuracy — and compare against simply prompting the base model with a few examples. If prompting gets close, you may not need fine-tuning at all.", None)],
    present="""
Write a short fine-tuning report:

1. **Problem**: the domain shift, with the base model's old vs new accuracy.
2. **Data**: what you removed and why (especially the leaked test rows).
3. **Results table**: base, LoRA (chosen rank) and full fine-tuning — new-domain accuracy, old-domain accuracy, trainable parameters.
4. **Recommendation**: which you'd ship and why (accuracy, forgetting, storage, serving several customers' adapters on one base).
5. **Next steps**: more labelled chats, the QLoRA run on a real LLM, and a prompting baseline.
""",
    resume=[
        "Implemented LoRA from scratch (forward pass, gradients, merging) and adapted a pre-trained intent classifier to a new domain, lifting accuracy from **X%** to **Y%** with **Z** trainable parameters",
        "Compared LoRA with full fine-tuning on accuracy, forgetting and parameter count, and chose the adapter rank with a sweep",
        "Prepared a fine-tuning dataset with leakage and duplicate checks, and wrote a QLoRA (PEFT + TRL) script for a 0.5B chat model",
    ],
    interview=[
        "Explain LoRA. Why does a low-rank update work, and why is B initialised to zero?",
        "LoRA vs full fine-tuning: what did you see on accuracy, forgetting and parameter count?",
        "What happens if test examples leak into the training data?",
        "How do you choose the rank and the scaling factor alpha?",
        "Why can a merged LoRA model be served at no extra cost? When would you keep adapters separate?",
        "When would you choose prompting or RAG instead of fine-tuning?",
    ],
    extensions=[
        "Add a DPO-style step: build preference pairs between correct and confusable labels and optimise the DPO loss.",
        "Try different learning rates and steps for LoRA vs full fine-tuning — which is more sensitive?",
        "Run the QLoRA script on a GPU and compare with a few-shot prompt of the base LLM.",
        "Serve two adapters (two 'customers') on one base model and switch between them per request.",
    ],
)
