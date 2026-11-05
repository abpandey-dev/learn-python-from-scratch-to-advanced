from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


LESSON("Basics", "Why sequences need memory", """
<p>A dense network takes a fixed-size input and treats each position separately. Language doesn't work like that. Compare:</p>
<ul><li>"The dog bit the man."</li><li>"The man bit the dog."</li></ul>
<p>Same words, opposite meaning. Average the word vectors and these two sentences become identical, because an average forgets order. Sequences also vary in length: 3 words here, 3,000 there.</p>
<p>A <b>recurrent neural network</b> solves both problems with one idea: read one item at a time and keep a running summary, the <b>hidden state</b> h.</p>
<p style="text-align:center"><b>hₜ = tanh(W_h·hₜ₋₁ + W_x·xₜ + b)</b></p>
<p>The same weights are used at every step, just as a CNN reuses one filter across an image. So the number of parameters doesn't depend on sequence length.</p>
<p><b>A single step by hand:</b> h = 0.5, x = 1, w_h = 0.8, w_x = 0.5, b = 0.1.</p>
<ul><li>Inside: 0.8·0.5 + 0.5·1 + 0.1 = 0.4 + 0.5 + 0.1 = 1.0.</li><li>tanh(1.0) = <b>0.7616</b>. That's the new memory.</li></ul>
<p>Why tanh? It keeps the state between −1 and 1, so it can't blow up however long the sequence is, and it lets values be positive or negative.</p>
""", practice=["One RNN Step", "A Vector RNN Step"])


LESSON("Basics", "Unrolling: one sequence, step by step", """
<p>Read 1, 0, −1 with w_h = 0.5, w_x = 1 and b = 0, starting from h = 0:</p>
<table><tr><th>t</th><th>x</th><th>Inside tanh</th><th>h</th></tr>
<tr><td>1</td><td>1</td><td>0.5·0 + 1 = 1</td><td><b>0.7616</b></td></tr>
<tr><td>2</td><td>0</td><td>0.5·0.7616 + 0 = 0.3808</td><td><b>0.3634</b></td></tr>
<tr><td>3</td><td>−1</td><td>0.5·0.3634 − 1 = −0.8183</td><td><b>−0.6741</b></td></tr></table>
<p>Look at step 2. The input is 0, yet h isn't 0: the network remembers the earlier 1. That's the whole point of a hidden state.</p>
<p><b>Unrolling</b> means drawing one copy of the cell per time step. It's still one set of weights, but seeing it as a long chain shows two things: why you can't run the steps in parallel (each needs the previous one), and how gradients have to flow back through every copy.</p>
<p><b>Size of the cell:</b> for input size d and hidden size h, an RNN has d·h + h·h + h parameters. With d = 64, h = 128: 8,192 + 16,384 + 128 = <b>24,704</b>, whether the sequence has 5 or 5,000 steps.</p>
""", practice=["Run an RNN Over a Sequence", "Parameters: RNN, GRU, LSTM"])


LESSON("Core", "Training over time, by hand", """
<p>Training an RNN uses ordinary backpropagation on the unrolled chain, called <b>backpropagation through time</b> (BPTT).</p>
<p>Take a simplified RNN with no tanh: hₜ = w·hₜ₋₁ + xₜ. With w = 0.5 and xs = 1, 2, 3, the loss is the final state.</p>
<ul><li>h₁ = 1</li><li>h₂ = 0.5·1 + 2 = 2.5</li><li>h₃ = 0.5·2.5 + 3 = <b>4.25</b></li></ul>
<p>Written out, h₃ = w²·1 + w·2 + 3. Its derivative is 2w·1 + 2 = 2·0.5 + 2 = <b>3</b>.</p>
<p>You can get this without the algebra, by tracking d = dh/dw alongside h. The update comes from the product rule: <b>d ← hₜ₋₁ + w·d</b>.</p>
<table><tr><th>t</th><th>d</th><th>h</th></tr>
<tr><td>1</td><td>0 + 0.5·0 = 0</td><td>1</td></tr>
<tr><td>2</td><td>1 + 0.5·0 = 1</td><td>2.5</td></tr>
<tr><td>3</td><td>2.5 + 0.5·1 = <b>3</b></td><td>4.25</td></tr></table>
<p>The chart uses this exact gradient. Data comes from a hidden w = 0.8. We start at w = 0.1, and gradient descent finds it.</p>
<p><b>Long sequences:</b> BPTT must store every step, and that's expensive. <b>Truncated BPTT</b> cuts a long sequence into chunks and backpropagates only within each one, keeping the hidden state between chunks. It's cheaper, but can't directly learn links longer than a chunk.</p>
""", practice=["Backprop Through Time", "Truncated BPTT Chunks"])


@LD
def learn_recurrent_weight():
    rng = np.random.default_rng(0)
    data = rng.normal(size=(64, 12))
    true_w, w, lr = 0.8, 0.1, 0.02

    def final_state(weight, xs):
        h = 0.0
        for x in xs:
            h = weight * h + x
        return h

    targets = [final_state(true_w, xs) for xs in data]
    history = [w]
    for _ in range(40):
        grad = 0.0
        for xs, y in zip(data, targets):
            h, d = 0.0, 0.0
            for x in xs:
                d = h + w * d
                h = w * h + x
            grad += 2 * (h - y) * d
        w -= lr * grad / len(data)
        history.append(w)
    print("final w:", round(w, 4))
    fig, ax = plt.subplots(figsize=(4.6, 2.7))
    ax.plot(history, label="learned w")
    ax.axhline(true_w, color="black", linestyle="--", label="true w = 0.8")
    ax.set_xlabel("training step")
    ax.set_ylabel("w")
    ax.legend(fontsize=7)


LESSON("Core", "Vanishing and exploding gradients", """
<p>In the derivative above, an old input is multiplied by w once per step it has travelled. In general, the influence of something t steps ago scales roughly like wᵗ:</p>
<table><tr><th>w</th><th>t = 1</th><th>t = 10</th><th>t = 50</th><th>Problem</th></tr>
<tr><td>0.9</td><td>0.9</td><td>0.349</td><td><b>0.005</b></td><td>vanishes</td></tr>
<tr><td>1.0</td><td>1</td><td>1</td><td>1</td><td>stable, but a knife edge</td></tr>
<tr><td>1.1</td><td>1.1</td><td>2.594</td><td><b>117.4</b></td><td>explodes</td></tr></table>
<p>So a small change in w turns "forgets everything" into "numbers blow up". Tanh makes vanishing more likely still, since its slope is at most 1.</p>
<p>What this means in practice: in "<i>The keys</i> to the old wooden cabinet in the hall <i>are</i> missing", the verb depends on a word far back. By the time the gradient arrives, it's nearly zero, so the network struggles to learn that link.</p>
<ul><li><b>Exploding</b> gradients have a simple fix: clip them (the training topic covers this).</li><li><b>Vanishing</b> gradients need a better architecture. That's why LSTMs exist.</li></ul>
""", practice=["How Gradients Fade Through Time"])


@LD
def fading_signal():
    t = np.arange(1, 51)
    fig, ax = plt.subplots(figsize=(4.6, 2.7))
    for w in [0.5, 0.9, 1.0, 1.1]:
        ax.semilogy(t, float(w) ** t, label=f"w = {w}")
    ax.set_xlabel("steps back in time")
    ax.set_ylabel("remaining signal (log)")
    ax.legend(fontsize=7)


LESSON("Core", "The LSTM cell, by hand", """
<p>An LSTM adds a second memory, the <b>cell state</b> c, and three learned <b>gates</b>. A gate is a sigmoid between 0 (closed) and 1 (open).</p>
<table><tr><th>Gate</th><th>Question it answers</th><th>Equation</th></tr>
<tr><td>Forget f</td><td>How much old memory to keep?</td><td>c ← <b>f</b>·c + …</td></tr>
<tr><td>Input i</td><td>How much new information to add?</td><td>… + <b>i</b>·tanh(z)</td></tr>
<tr><td>Output o</td><td>How much to reveal now?</td><td>h = <b>o</b>·tanh(c)</td></tr></table>
<p>Each gate has the same form: σ(w_h·h + w_x·x + b). With h = 0.5, x = 1, w_h = w_x = 1, b = 0, the inside is 1.5, so the gate is σ(1.5) = <b>0.8176</b>. Applied to c = 2, it keeps 1.6351.</p>
<p><b>A full step:</b> f = 0.9, i = 0.2, o = 0.5, z = 1, c = 2.</p>
<ol><li>Keep: 0.9·2 = 1.8.</li><li>Add: 0.2·tanh(1) = 0.2·0.7616 = 0.1523.</li><li>New c = 1.8 + 0.1523 = <b>1.9523</b>.</li><li>Output: h = 0.5·tanh(1.9523) = <b>0.4802</b>.</li></ol>
<p><b>Why it survives:</b> the cell state update is mostly <i>addition</i>. Instead of being forced through a multiply-and-squash at every step, c passes along almost unchanged when f ≈ 1. Compare 20 steps: an RNN with w = 0.5 keeps 0.5²⁰ ≈ 0.000001; a cell with f = 0.99 keeps 0.99²⁰ ≈ <b>0.818</b>.</p>
<p>That's the same idea as a residual connection, arriving almost two decades earlier: a direct path for the signal. Networks often initialise the forget gate's bias to a positive value so it starts open.</p>
<p><b>Cost:</b> 4 sets of weights (three gates and the candidate), so 4 times the RNN's parameters: 4 × 24,704 = 98,816 for d = 64, h = 128. PyTorch's <code>nn.LSTM</code> reports slightly more, 99,328, because it keeps two bias vectors per set.</p>
""", practice=["An LSTM Gate", "One LSTM Step", "Memory Across Many Steps"])


@LD
def rnn_vs_lstm_memory():
    steps = np.arange(0, 101)
    fig, ax = plt.subplots(figsize=(4.6, 2.7))
    ax.plot(steps, 0.9 ** steps, label="RNN-style: multiply by w = 0.9")
    ax.plot(steps, 0.99 ** steps, label="LSTM-style: forget gate f = 0.99")
    ax.set_xlabel("steps")
    ax.set_ylabel("signal kept")
    ax.legend(fontsize=7)


LESSON("Core", "The GRU: fewer gates", """
<p>A GRU merges the cell state and hidden state, and uses a single <b>update gate</b> u to blend old with new:</p>
<p style="text-align:center"><b>hₜ = (1 − u)·hₜ₋₁ + u·tanh(z)</b></p>
<p>(The full GRU also has a reset gate, which shapes the candidate z. So 3 sets of weights in all.)</p>
<p>With h = 0.2 and z = 1, so tanh(z) = 0.7616:</p>
<table><tr><th>u</th><th>Calculation</th><th>New h</th><th>Meaning</th></tr>
<tr><td>0</td><td>1·0.2 + 0·0.7616</td><td>0.2</td><td>keep the old memory unchanged</td></tr>
<tr><td>0.5</td><td>0.5·0.2 + 0.5·0.7616</td><td><b>0.4808</b></td><td>half and half</td></tr>
<tr><td>1</td><td>0·0.2 + 1·0.7616</td><td>0.7616</td><td>replace it entirely</td></tr></table>
<table><tr><th></th><th>RNN</th><th>GRU</th><th>LSTM</th></tr>
<tr><td>Sets of weights</td><td>1</td><td>3</td><td>4</td></tr>
<tr><td>Parameters (d = 10, h = 20)</td><td>620</td><td>1,860</td><td>2,480</td></tr>
<tr><td>Long memory</td><td>poor</td><td>good</td><td>good</td></tr></table>
<p>GRU and LSTM usually perform about the same. If the choice matters for your task, test both on your data.</p>
""", practice=["One GRU Step"])


LESSON("Core", "Batches: padding, masks and masked loss", """
<p>Tensors must be rectangular, but sentences aren't. So you <b>pad</b> short ones with a special token, and keep a <b>mask</b> saying which positions are real:</p>
<pre><code class="py">[[5, 2, 9],        mask  [[1, 1, 1],
 [7, 0, 0],               [1, 0, 0],
 [3, 3, 0]]               [1, 1, 0]]</code></pre>
<p>Padding is a tensor-shape requirement and carries no meaning, so it must not affect anything. Three places commonly go wrong:</p>
<p><b>1. The loss.</b> Per-position losses are [1, 2, <s>9</s>] and [3, <s>9</s>, <s>9</s>]. Crossed-out values are padding.</p>
<ul><li>Wrong (all values): 33 / 6 = <b>5.5</b>.</li><li>Right (masked): (1 + 2 + 3) / 3 = <b>2</b>.</li></ul>
<p>Note the division is by the number of <i>real</i> positions, not the table size. Otherwise short sequences shrink the loss for no good reason.</p>
<p><b>2. The final state.</b> The usual summary of a sequence is its output at the last real step. With outputs [1,2,3], [4,5,6], [7,8,9] and lengths 3, 1, 2, that's 3, 4 and 8. Taking the last column instead would give 3, 6, 9: two of those came from padding.</p>
<p><b>3. Averaging.</b> Mean pooling over [1,2], [3,4] and a padding row [100,100] must give [2, 3], and not include the 100s.</p>
<p><b>Efficiency tip:</b> sort or bucket by length so similar lengths share a batch; there's less wasted padding.</p>
""", practice=["Pad a Batch of Sequences", "Mask From Lengths", "Masked Average Loss", "Last Real Output of Each Sequence", "Average of the Real States"])


LESSON("Advanced", "Sequence tasks and how to prepare data", """
<p><b>Predicting the next item</b> is the single most important setup in this course. Every language model trains this way. For tokens [5, 8, 2, 9]:</p>
<table><tr><th>Input</th><td>5</td><td>8</td><td>2</td></tr><tr><th>Target</th><td>8</td><td>2</td><td>9</td></tr></table>
<p>Shift by one, and each position becomes a training example. During training, the input at each step is the <i>true</i> previous token, even if the model got the last one wrong. That's <b>teacher forcing</b>. It trains faster, but at prediction time the model only has its own outputs to go on, so errors can snowball.</p>
<p><b>Forecasting</b> a number series uses a sliding window. With 1, 2, 3, 4, 5 and window 2: X = [1,2], [2,3], [3,4] and y = 3, 4, 5. For a time series, split by time and never shuffle across the split.</p>
<p><b>Text to numbers:</b> "hello" has characters e, h, l, o, numbered 0, 1, 2, 3, so it encodes to [1, 0, 2, 2, 3]. Real tokenisers are the next topic.</p>
<p><b>Bidirectional RNNs</b> read both ways and join the two states. This helps tagging ("Apple" as a company depends on later words), but can't work when predicting the next token: the future isn't available. For 1, 0, −1 the first position gets forward state 0.7616 and backward state 0.6741. The second number was computed from the whole sequence read in reverse, so it carries information about what comes later.</p>
<table><tr><th>Task</th><th>Shape</th><th>Uses</th></tr>
<tr><td>Many-to-one</td><td>sequence → label</td><td>last state or mean pooling</td></tr>
<tr><td>Many-to-many</td><td>sequence → one output per step</td><td>all states</td></tr>
<tr><td>Seq-to-seq</td><td>sequence → different sequence</td><td>encoder + decoder (the problem attention was invented for)</td></tr></table>
""", practice=["Teacher Forcing Targets", "Sliding Windows for Forecasting", "Encode, Decode With a Vocabulary", "Bidirectional States"])


LESSON("Advanced", "RNNs in PyTorch, and why transformers replaced them", """
<pre><code class="py">import torch, torch.nn as nn

emb = nn.Embedding(1000, 64)
lstm = nn.LSTM(64, 128, batch_first=True)
head = nn.Linear(128, 1000)

tokens = torch.randint(0, 1000, (8, 20))    # (batch, time)
output, (h, c) = lstm(emb(tokens))
print(output.shape)   # (8, 20, 128): one state per step
print(h.shape)        # (1, 8, 128): (layers, batch, hidden)
logits = head(output) # (8, 20, 1000): next-token scores</code></pre>
<p>Shape mistake to watch for: without <code>batch_first=True</code>, PyTorch expects (time, batch, features). It won't raise an error if your numbers happen to fit, and it will silently read the data the wrong way round.</p>
<p><b>Why did transformers take over language?</b></p>
<table><tr><th></th><th>RNN</th><th>Transformer</th></tr>
<tr><td>Processing</td><td>one step at a time</td><td>all positions in parallel</td></tr>
<tr><td>A word 1,000 steps back</td><td>must pass through 1,000 updates</td><td>one direct attention link</td></tr>
<tr><td>Summary of input</td><td>squeezed into a fixed-size state</td><td>can look back at everything</td></tr>
<tr><td>Cost per token</td><td>constant memory</td><td>grows with context length</td></tr></table>
<p>RNNs are still a reasonable choice for small on-device models and streaming signals, where constant memory matters.</p>
<p>The PyTorch code here is shown as text. PyTorch doesn't run in this site's browser IDE, so the practice questions use NumPy and plain Python.</p>
""", practice=[])
