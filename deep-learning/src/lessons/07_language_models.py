from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


LESSON("Basics", "A language model predicts the next token", """
<p>Every language model, from a tiny one to the largest, does one thing: <b>given the tokens so far, return a probability for each possible next token</b>. Long answers come from doing this repeatedly.</p>
<p><b>The smallest possible model</b> looks only at the previous word. Corpus: the cat sat the cat ran the dog ran.</p>
<table><tr><th>Previous</th><th>Next: count</th><th>Probabilities</th></tr>
<tr><td>the</td><td>cat: 2, dog: 1</td><td>cat 2/3 = 0.667, dog 1/3 = 0.333</td></tr>
<tr><td>cat</td><td>sat: 1, ran: 1</td><td>0.5 each</td></tr>
<tr><td>sat</td><td>the: 1</td><td>the 1.0</td></tr>
<tr><td>ran</td><td>the: 1</td><td>the 1.0</td></tr>
<tr><td>dog</td><td>ran: 1</td><td>ran 1.0</td></tr></table>
<p>That table <i>is</i> the model: it was "trained" by counting. To generate:</p>
<ol><li>Look at the last token.</li><li>Choose the next one using its row of probabilities.</li><li>Add it and repeat.</li></ol>
<p>The demo trains this on a slightly longer text and generates from it. The output has the right local word pairs, yet makes little overall sense, because a single word of context can't carry meaning across a sentence. Everything else in this course, from embeddings to attention, exists to use more context better.</p>
""", practice=["Bigram Counts"])


@LD
def bigram_generates():
    text = "the cat sat on the mat the dog sat on the log the cat ran to the dog the dog ran to the mat".split()
    table = {}
    for a, b in zip(text, text[1:]):
        table.setdefault(a, []).append(b)
    rng = np.random.default_rng(1)
    word, out = "the", ["the"]
    for _ in range(14):
        word = str(rng.choice(table[word]))
        out.append(word)
    print(" ".join(out))


LESSON("Basics", "Smoothing, log probabilities and perplexity", """
<p><b>Problem 1: zero counts.</b> "the ran" never appeared, so its probability is 0, and any sentence containing it scores 0. With <b>add-k smoothing</b> you pretend everything happened k extra times:</p>
<p style="text-align:center"><b>P(next | prev) = (count + k) / (count of prev + k·V)</b></p>
<p>With V = 5 distinct words and k = 1: P(ran | the) = (0 + 1) / (3 + 5) = <b>0.125</b>, up from 0.</p>
<p>Another option is <b>backoff</b>: when a pair is unseen, use a discounted single-word estimate. "dog cat" is unseen, and "cat" is 2 of 9 tokens, so the score is 0.4 × 2/9 = <b>0.0889</b>.</p>
<p><b>Problem 2: tiny numbers.</b> Multiply 0.1 by itself 4 times and you get 0.0001. After a few hundred tokens, a computer rounds the product to exactly 0. So add logs instead: 4 × ln 0.1 = <b>−9.2103</b>.</p>
<p><b>How good is a model?</b> <b>Perplexity</b> = exp(average negative log probability of the true tokens). It reads as "the model is as unsure as if choosing between this many equally likely options":</p>
<table><tr><th>Probabilities given to the true tokens</th><th>Calculation</th><th>Perplexity</th></tr>
<tr><td>1, 1</td><td>exp(0)</td><td>1: always certain and right</td></tr>
<tr><td>0.25, 0.25, 0.25</td><td>exp(1.3863)</td><td>4: like choosing among 4</td></tr>
<tr><td>0.5, 0.125</td><td>exp((0.693 + 2.079) / 2)</td><td>4: same average uncertainty</td></tr></table>
<p>A uniform guess over a vocabulary of size V gives a perplexity of exactly V. That's a useful sanity check for an untrained model. It's only comparable between models using the same tokeniser and test text.</p>
""", practice=["Bigram Probability With Smoothing", "Backoff When a Pair Is Unseen", "Log-Probability of a Sentence", "Perplexity"])


LESSON("Core", "From counting to a neural network", """
<p>The same bigram model can be learned rather than counted. Give each previous word a row of <b>logits</b>, one per possible next word. Softmax turns these into probabilities, and gradient descent adjusts them.</p>
<p>The gradient of cross-entropy has a neat form. For one example:</p>
<p style="text-align:center"><b>new logits = logits + lr · (one_hot(target) − probs)</b></p>
<p>Two next words, logits 0 and 0, true target 0, lr = 1. Then probs = (0.5, 0.5), so:</p>
<ul><li>Update for target: 1 − 0.5 = +0.5</li><li>Update for other: 0 − 0.5 = −0.5</li><li>New logits: <b>(0.5, −0.5)</b></li></ul>
<p>Read that as "more of the right answer, less of whatever you were wrongly predicting". A confident correct prediction barely changes anything, and a confident wrong one changes a lot.</p>
<p>The chart trains on the demo's text. The loss starts at ln 9 = 2.197, since there are 9 words and all begin equally likely. It falls towards 0.640, the loss of the exact counting table, reaching 0.648 after 300 steps. So training has rediscovered what counting gave directly.</p>
<p><b>So why bother with a network?</b> A table can't scale. With 50,000 tokens and a context of just 5, there would be 50,000⁵ rows. A neural network shares its weights, so it can generalise to contexts it has never seen. That's the actual leap from n-grams to LLMs.</p>
""", practice=["One Learning Step on Logits"])


@LD
def neural_bigram_training():
    text = ("the cat sat on the mat the dog sat on the log the cat ran to the dog the dog ran to the mat " * 6).split()
    vocab = sorted(set(text))
    ids = np.array([vocab.index(w) for w in text])
    x, y = ids[:-1], ids[1:]
    V = len(vocab)
    counts = np.zeros((V, V))
    np.add.at(counts, (x, y), 1)
    exact = -np.log((counts / counts.sum(axis=1, keepdims=True))[x, y]).mean()
    logits, curve = np.zeros((V, V)), []
    for _ in range(301):
        e = np.exp(logits - logits.max(axis=1, keepdims=True))
        p = e / e.sum(axis=1, keepdims=True)
        curve.append(-np.log(p[x, y]).mean())
        grad = np.zeros_like(logits)
        np.add.at(grad, (x, y), 1)
        np.add.at(grad, x, -p[x])
        logits += 5 * grad / len(x)
    print("start:", round(curve[0], 3), "end:", round(curve[-1], 3), "counting:", round(exact, 3))
    fig, ax = plt.subplots(figsize=(4.6, 2.7))
    ax.plot(curve, label="neural bigram")
    ax.axhline(exact, color="black", linestyle="--", label="counting table")
    ax.set_xlabel("training step")
    ax.set_ylabel("cross-entropy")
    ax.legend(fontsize=7)


LESSON("Core", "How an LLM is trained", """
<p>The training recipe for a large model is surprisingly close to this. First, cut windows from a huge text:</p>
<pre><code class="py">data = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19], block = 3, offsets = [0, 5]
x = [[10, 11, 12], [15, 16, 17]]
y = [[11, 12, 13], [16, 17, 18]]</code></pre>
<p>The model outputs a row of logits per position, and the loss is the average cross-entropy against y. Every position is a prediction: seeing 10, predict 11; seeing 10, 11, predict 12; and so on. The causal mask from the last topic is what makes this fair.</p>
<p><b>The loss by hand.</b> Logits [2, 0, 0], target 0: e² / (e² + 1 + 1) = 7.389 / 9.389 = 0.787, and −ln 0.787 = 0.2395. Logits [0, 1, 0], target 1: e / (e + 2) = 0.576, and −ln 0.576 = 0.5514. Mean: <b>0.3955</b>.</p>
<p><b>Sanity check:</b> an untrained model should start near ln V. With 4 tokens and equal logits: ln 4 = <b>1.3863</b>. If your loss starts far from this, look for a bug before training.</p>
<p><b>Padding:</b> by convention, a target of −100 means "ignore". For logits [2, 0], [0, 3], [9, 0] and targets 0, 1, −100, only the first two count: (0.1269 + 0.0486) / 2 = <b>0.0878</b>.</p>
<pre><code class="py">logits = model(x)                                    # (N, T, vocab)
loss = F.cross_entropy(logits.reshape(-1, vocab), y.reshape(-1), ignore_index=-100)</code></pre>
<p>The largest models apply this to enormous amounts of text with thousands of GPUs. That's a real engineering challenge, but the objective is this same line.</p>
""", practice=["Make a Training Batch", "Next-Token Cross-Entropy", "Ignore Padding in the Loss"])


LESSON("Core", "Temperature: how bold to be", """
<p>Once the model gives logits, you decide how to choose. <b>Temperature</b> divides the logits before softmax:</p>
<p style="text-align:center"><b>probs = softmax(logits / T)</b></p>
<p>With logits 2, 1, 0:</p>
<table><tr><th>T</th><th>Logits ÷ T</th><th>Probabilities</th><th>Behaviour</th></tr>
<tr><td>0.5</td><td>4, 2, 0</td><td>0.867, 0.117, 0.016</td><td>focused, predictable</td></tr>
<tr><td>1</td><td>2, 1, 0</td><td>0.665, 0.245, 0.090</td><td>as the model learned</td></tr>
<tr><td>2</td><td>1, 0.5, 0</td><td>0.506, 0.307, 0.186</td><td>varied, riskier</td></tr></table>
<p>As T approaches 0, it becomes "always take the top token". As T grows, it approaches a uniform random choice. Dividing doesn't reorder tokens; it only changes how sharply the probabilities separate.</p>
<p><b>Entropy</b> measures the spread: −Σ p·ln p. It's 0 for (1, 0, 0), 0.693 for (0.5, 0.5), and 1.386 for four equal options.</p>
<p><b>Sampling itself is simple.</b> Draw a random u in [0, 1), and walk along the running total. For probabilities 0.5, 0.3, 0.2 the running total is 0.5, 0.8, 1.0, so u = 0.1 picks token 0, u = 0.6 picks token 1 and u = 0.95 picks token 2.</p>
<p><b>In real APIs:</b> not every model offers these controls. Recent Claude models reject non-default <code>temperature</code>, <code>top_p</code> and <code>top_k</code> values, so check the docs for the model you're using. It's still essential to understand them, for running your own models and reading research.</p>
""", practice=["Temperature", "How Unsure Is the Model?", "Sampling With a Random Number"])


@LD
def temperature_chart():
    logits = np.array([3.0, 2.0, 1.5, 0.5, 0.0])
    fig, axes = plt.subplots(1, 3, figsize=(7, 2.3), sharey=True)
    for ax, T in zip(axes, [0.3, 1.0, 3.0]):
        e = np.exp(logits / T)
        ax.bar(range(5), e / e.sum())
        ax.set_title(f"T = {T}", fontsize=9)
    axes[0].set_ylabel("probability")
    fig.tight_layout()


LESSON("Core", "Top-k and top-p", """
<p>Temperature keeps every token possible, so sometimes an absurd one gets chosen. Filtering removes the unlikely tail before sampling.</p>
<p><b>Top-k</b> keeps a fixed number. With probabilities 0.4, 0.3, 0.2, 0.1 and k = 2: keep 0.4 and 0.3, total 0.7. Rescale: 0.4/0.7 = <b>0.5714</b> and 0.3/0.7 = <b>0.4286</b>.</p>
<p><b>Top-p</b>, or nucleus sampling, keeps however many are needed to reach a total probability p, which adapts to the model's certainty:</p>
<table><tr><th>Probabilities</th><th>p</th><th>Added up</th><th>Kept</th><th>After rescaling</th></tr>
<tr><td>0.5, 0.3, 0.15, 0.05</td><td>0.75</td><td>0.5, then 0.8 ≥ 0.75</td><td>2 tokens</td><td>0.625, 0.375</td></tr>
<tr><td>0.9, 0.05, 0.05</td><td>0.5</td><td>0.9 ≥ 0.5</td><td>1 token</td><td>1.0</td></tr></table>
<p>The same p keeps one token when the model is sure, and more when it's unsure. A fixed k can't do that, which is why top-p is often preferred.</p>
<p>The usual order is: repetition penalty, then temperature, then top-k or top-p, then sample.</p>
<p><b>Repetition penalty:</b> without it, models can loop. For tokens already used, divide a positive logit by the penalty, and multiply a negative one by it. Either way the token gets less likely. With penalty 1.5: logit 2 → 1.3333 and logit −1 → −1.5. Use it gently, as some repetition is correct: names and "the" need repeating.</p>
""", practice=["Top-k Filtering", "Top-p (Nucleus) Filtering", "Repetition Penalty"])


LESSON("Core", "Greedy, beam search and stopping", """
<p><b>Greedy</b> always takes the top token. It's simple, but the locally best step can lead somewhere poor:</p>
<table><tr><th>From</th><th>Options</th></tr><tr><td>s</td><td>x: 0.6, y: 0.4</td></tr><tr><td>x</td><td>a: 0.5, b: 0.5</td></tr><tr><td>y</td><td>c: 0.9, d: 0.1</td></tr></table>
<ul><li>Greedy: s → x (0.6), x → a (0.5). Probability = <b>0.30</b>.</li><li>Best overall: s → y (0.4), y → c (0.9). Probability = <b>0.36</b>.</li></ul>
<p>Greedy rejected y at the first step because 0.4 &lt; 0.6, and never saw that y leads to a strong continuation.</p>
<p><b>Beam search</b> keeps the best few candidates at every step. With width 2, it extends both x and y:</p>
<table><tr><th>Candidates after step 2</th><th>Probability</th></tr><tr><td>s y c</td><td><b>0.36</b></td></tr><tr><td>s x a</td><td>0.30</td></tr><tr><td>s x b</td><td>0.30</td></tr><tr><td>s y d</td><td>0.04</td></tr></table>
<p>Trying every path takes Vˢᵗᵉᵖˢ work. With V = 50,000 and only 10 steps, that's unthinkable. A beam needs just width × V per step.</p>
<p>Beam search suits tasks with one right answer, such as translation or speech recognition. In open-ended writing, the highest-probability text tends to be bland and repetitive, so chat models usually sample instead.</p>
<p><b>Stopping</b> happens when one of these occurs: the model produces its end token, the token limit is reached, or the text matches a <b>stop sequence</b>. "Answer: 42\\nUser: next" with stop "User:" returns "Answer: 42\\n".</p>
""", practice=["Greedy Generation", "Beam Search", "Stop Sequences"])


LESSON("Advanced", "Generating quickly: the KV cache", """
<p>To generate a token, the model needs attention over all previous tokens. A naive loop re-runs everything each time:</p>
<table><tr><th>Step</th><th>Without a cache</th><th>With a cache</th></tr>
<tr><td>1</td><td>100</td><td>100</td></tr><tr><td>2</td><td>101</td><td>1</td></tr><tr><td>3</td><td>102</td><td>1</td></tr><tr><td>…</td><td>…</td><td>…</td></tr></table>
<p>For a 100-token prompt and 50 new tokens, without a cache that's 50·100 + (50·49)/2 = <b>6,225</b> positions. With a cache it's 100 + 49 = <b>149</b>, about 42 times fewer.</p>
<p><b>Why does this work?</b> Thanks to the causal mask, a token's output depends only on earlier tokens, so old keys and values never change. The model saves them per layer, and each new token computes only its own.</p>
<p>The price is memory, which grows with sequence length and has to be kept for each user. This is why long context costs money even when the model isn't generating much, and it's the mechanism behind <b>prompt caching</b> in the next topic: a provider reuses the work for a prefix it has already processed.</p>
<p><b>Context windows:</b> a model has a maximum length, and past it something must go. With window 3 and tokens 1, 2, 3, then 4, 5: it sees [2, 3, 4], then [3, 4, 5]. Note that this forgets the <i>oldest</i> tokens, including possibly your instructions, so applications manage this deliberately.</p>
""", practice=["What the KV Cache Saves", "Context Window"])


@LD
def kv_cache_chart():
    N = np.arange(1, 501)
    P = 200
    fig, ax = plt.subplots(figsize=(4.6, 2.7))
    ax.plot(N, N * P + N * (N - 1) / 2, label="no cache")
    ax.plot(N, P + N - 1, label="with KV cache")
    ax.set_yscale("log")
    ax.set_xlabel("tokens generated (prompt = 200)")
    ax.set_ylabel("positions processed")
    ax.legend(fontsize=7)


LESSON("Advanced", "From raw model to helpful assistant", """
<p>A model that only predicts the next token continues text; it doesn't answer. Ask a raw model "What is the capital of France?" and it may produce more quiz questions, since that's what often follows on the web. Getting to an assistant takes further stages:</p>
<table><tr><th>Stage</th><th>Data</th><th>What it adds</th></tr>
<tr><td>Pre-training</td><td>a very large body of text</td><td>language and knowledge</td></tr>
<tr><td>Supervised fine-tuning</td><td>example conversations</td><td>answering in the assistant format</td></tr>
<tr><td>Preference training</td><td>which of two responses is better</td><td>helpfulness and safer behaviour</td></tr></table>
<p><b>Limits that follow from how it works:</b></p>
<ul><li><b>Plausible isn't the same as true.</b> A model picks likely continuations, so it can state wrong things confidently. That's why you'd give it sources (RAG) and check output.</li>
<li><b>Knowledge has a date.</b> It only knows its training data, unless given tools.</li>
<li><b>Random output.</b> The same prompt can give different answers, which affects how you test.</li>
<li><b>Tokens, not letters.</b> Counting characters is harder than it looks.</li></ul>
<p>Knowing what's actually going on makes you a better LLM engineer: you stop expecting magic, and you'd design for these limits. That's the next three topics.</p>
""", practice=[])
