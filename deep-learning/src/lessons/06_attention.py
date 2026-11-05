from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


LESSON("Basics", "Attention is a soft dictionary lookup", """
<p>A Python dictionary finds an exact key and returns its value. <b>Attention</b> is a fuzzy version: compare your query with <i>every</i> key, then return a blend of all values, weighted by how well they matched.</p>
<p><b>By hand.</b> Keys 1, 2, 3, values 10, 20, 30, query 2.1. Use similarity = −(query − key)²:</p>
<table><tr><th>Key</th><th>Value</th><th>Similarity</th><th>Weight (softmax)</th></tr>
<tr><td>1</td><td>10</td><td>−1.21</td><td>0.172</td></tr>
<tr><td>2</td><td>20</td><td>−0.01</td><td>0.571</td></tr>
<tr><td>3</td><td>30</td><td>−0.81</td><td>0.257</td></tr></table>
<p>Answer: 0.172·10 + 0.571·20 + 0.257·30 = <b>20.85</b>. It's mostly the value of the closest key, nudged towards 30 because the query sits a little on that side. With query 2.0 exactly, the weights are symmetric (0.212, 0.576, 0.212), giving exactly <b>20</b>. With query 1 and keys 1, 5, the far key gets a weight near zero, so the answer is about 10: nearly an exact lookup.</p>
<p>Why does it matter that it's soft? A weighted average is <b>differentiable</b>, so gradients can flow through the choice of what to look at, and the network learns what to pay attention to.</p>
<p>In language: for each word, the model asks "which other words help me understand this one?" In "The animal didn't cross the street because <i>it</i> was tired", "it" should attend to "animal".</p>
""", practice=["Soft Dictionary Lookup"])


LESSON("Core", "Scaled dot-product attention, by hand", """
<p style="text-align:center"><b>Attention(Q, K, V) = softmax(Q·Kᵀ / √d) · V</b></p>
<p>Take three tokens with 2-dimensional vectors, using X for Q, K and V alike: (1, 0), (0, 1), (1, 1). Here d = 2, so √d = 1.414.</p>
<p><b>Step 1: scores.</b> Dot every query with every key, and divide by 1.414:</p>
<table><tr><th></th><th>k₁</th><th>k₂</th><th>k₃</th></tr><tr><th>q₁</th><td>0.707</td><td>0</td><td>0.707</td></tr><tr><th>q₂</th><td>0</td><td>0.707</td><td>0.707</td></tr><tr><th>q₃</th><td>0.707</td><td>0.707</td><td>1.414</td></tr></table>
<p><b>Step 2: softmax each row.</b> Each row now sums to 1, a budget of attention for that token:</p>
<table><tr><th></th><th>k₁</th><th>k₂</th><th>k₃</th></tr><tr><th>q₁</th><td>0.401</td><td>0.198</td><td>0.401</td></tr><tr><th>q₂</th><td>0.198</td><td>0.401</td><td>0.401</td></tr><tr><th>q₃</th><td>0.248</td><td>0.248</td><td>0.503</td></tr></table>
<p><b>Step 3: blend the values.</b> For token 1: 0.401·(1, 0) + 0.198·(0, 1) + 0.401·(1, 1) = <b>(0.802, 0.599)</b>.</p>
<p>The result has the same shape as the input, but each token now contains information from others it found relevant. The token count is unchanged, and any length works with the same weights.</p>
<p><b>Why divide by √d?</b> For random vectors with variance 1, a dot product's variance grows in proportion to d. So at large d, scores get large, and softmax turns almost all-or-nothing. Compare softmax of (1, 2, 3) = (0.09, 0.245, 0.665) with softmax of (10, 20, 30), which is about (0, 0, 1). Almost-all-or-nothing means tiny gradients. Dividing by √d brings the spread back to about 1, and the chart shows this.</p>
""", practice=["Attention Scores", "Attention Weights", "Scaled Dot-Product Attention", "Which Token Was Attended?"])


@LD
def why_scale():
    rng = np.random.default_rng(0)
    dims = [4, 16, 64, 256, 1024]
    raw, scaled = [], []
    for d in dims:
        q, k = rng.normal(size=(5000, d)), rng.normal(size=(5000, d))
        dots = (q * k).sum(axis=1)
        raw.append(dots.std())
        scaled.append((dots / np.sqrt(d)).std())
    print("std of scores, raw:", np.round(raw, 2))
    print("std of scores, scaled:", np.round(scaled, 2))
    fig, ax = plt.subplots(figsize=(4.6, 2.7))
    ax.semilogx(dims, raw, "o-", label="raw dot product")
    ax.semilogx(dims, scaled, "s-", label="divided by √d")
    ax.set_xlabel("vector size d")
    ax.set_ylabel("spread of scores (std)")
    ax.legend(fontsize=7)


@LD
def attention_heatmap():
    tokens = ["the", "cat", "sat", "on", "mat"]
    X = np.array([[0.1, 0.1, 0.9], [1.0, 0.1, 0.1], [0.1, 1.0, 0.1], [0.1, 0.1, 1.0], [0.9, 0.2, 0.1]])
    S = X @ X.T / np.sqrt(3) * 4
    A = np.exp(S) / np.exp(S).sum(axis=1, keepdims=True)
    fig, ax = plt.subplots(figsize=(3.4, 3))
    ax.imshow(A, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(5), tokens, fontsize=8)
    ax.set_yticks(range(5), tokens, fontsize=8)
    ax.set_title("Hand-made vectors: who attends to whom", fontsize=8)


LESSON("Core", "Queries, keys and values are learned", """
<p>So far Q, K and V were all X itself. A real layer first passes X through three learned matrices:</p>
<p style="text-align:center"><b>Q = X·W_q,  K = X·W_k,  V = X·W_v</b></p>
<table><tr><th>Part</th><th>Plain meaning</th></tr>
<tr><td>Query</td><td>what this token is looking for</td></tr>
<tr><td>Key</td><td>what this token offers to be found by</td></tr>
<tr><td>Value</td><td>what this token passes on if chosen</td></tr></table>
<p>A verb could look for its subject while offering itself to be found by something else entirely. Separate matrices allow that. Without them, a token's query and key are the same vector, so it tends to match itself strongly.</p>
<p><b>A small example.</b> X = (1, 0), (0, 1); W_q is the identity; W_k swaps the two axes; W_v = (2), (3), so V = 2, 3.</p>
<ul><li>Q = (1, 0), (0, 1). K = (0, 1), (1, 0). So token 1 now matches token <i>2's</i> key best.</li>
<li>Scores for token 1: (0, 0.707). Softmax: 0.3302, 0.6698.</li>
<li>Output: 0.3302·2 + 0.6698·3 = <b>2.6698</b>.</li></ul>
<p>Token 1 now reads mostly from token 2, purely because of learned weights.</p>
<p><b>Terminology:</b> in <b>self-attention</b>, Q, K and V all come from one sequence. In <b>cross-attention</b>, queries come from one (decoder), keys and values from another (encoder). That's how a translator looks at the source sentence: query (1, 0) against encoder states (1, 0), (0, 1), (1, 1) returns (0.802, 0.599).</p>
""", practice=["Self-Attention With Learned Projections", "Cross-Attention"])


LESSON("Core", "Masks: what attention mustn't see", """
<p>Masks hide positions by setting their scores to −∞ before softmax, since e^(−∞) = 0. Remaining weights still sum to 1.</p>
<p><b>By hand:</b> scores 1, 2, 3 with only the first two allowed: e¹ = 2.718, e² = 7.389, so the weights are 2.718/10.107 = <b>0.269</b>, 7.389/10.107 = <b>0.731</b> and exactly 0.</p>
<p>Why −∞, instead of multiplying by 0 after softmax? The weights wouldn't sum to 1 any more. And setting scores to 0 before softmax wouldn't work either, because e⁰ = 1 still takes a share.</p>
<p><b>Padding mask:</b> don't attend to padding. <b>Causal mask:</b> when predicting token t, don't look at later tokens, because that would be cheating:</p>
<pre><code class="py">[[1, 0, 0],      # token 0 sees itself
 [1, 1, 0],      # token 1 sees tokens 0 and 1
 [1, 1, 1]]      # token 2 sees everything before it</code></pre>
<p>Combine them by multiplying. For padding mask (1, 1, 0), the last column goes to zero: [[1,0,0], [1,1,0], [1,1,0]].</p>
<p><b>By hand with the earlier vectors:</b> token 1 = (0, 1) can only see tokens 0 and 1. Scores: 0 and 0.707. Weights: 0.330, 0.670. Output: <b>(0.330, 0.670)</b>. Without the mask it got (0.599, 0.802), but that included information from the future.</p>
<p>A language model without a causal mask would score brilliantly in training (the answer is in its input) and fail completely when generating. If your training loss looks too good, this is a good thing to check.</p>
""", practice=["Causal Mask", "Masked Softmax", "Padding Plus Causal Mask", "Masked Self-Attention"])


LESSON("Core", "Multi-head attention", """
<p>One attention has one way of relating tokens. A word may need several at once: its grammar, what it refers to, nearby words. <b>Multi-head attention</b> runs several smaller attentions side by side.</p>
<p>With d = 4 and 2 heads, each token's vector is split in half:</p>
<pre><code class="py">X = [[1, 2, 3, 4],        head 0: [[1, 2],     head 1: [[3, 4],
     [5, 6, 7, 8]]                 [5, 6]]              [7, 8]]</code></pre>
<p>Each head computes attention on its own. Then the pieces are joined back to the original shape, and a final linear layer mixes them.</p>
<table><tr><th>Stage</th><th>Shape (d = 512, 8 heads, T = 100)</th></tr>
<tr><td>Input</td><td>(100, 512)</td></tr>
<tr><td>Split</td><td>(8, 100, 64)</td></tr>
<tr><td>Attention per head</td><td>(8, 100, 64)</td></tr>
<tr><td>Concatenate + mix</td><td>(100, 512)</td></tr></table>
<p>Each head has d/h = 512/8 = <b>64</b> dimensions, so 8 heads cost about the same as one large one. Parameters: 4 maps of d × d (Q, K, V, output) = 4 · 512² = <b>1,048,576</b>, and this doesn't depend on the number of heads.</p>
<p><b>A common mistake:</b> d must divide evenly by h. Also, don't over-interpret a chart of attention weights: heads rarely map onto neat ideas like "the grammar head", and high attention doesn't necessarily explain a decision.</p>
""", practice=["Split Into Heads", "Merge Heads", "Multi-Head Parameters"])


LESSON("Core", "The transformer block", """
<p>Stack these four parts, and you've built what's inside an LLM:</p>
<pre><code class="py">x = x + attention(norm(x))      # tokens communicate
x = x + feed_forward(norm(x))   # each token thinks on its own</code></pre>
<p><b>Feed-forward.</b> The same small network is applied to each position separately. Attention mixes information <i>between</i> tokens; this transforms it <i>within</i> one.</p>
<p>For x = (1, 2) with W₁ = identity and b₁ = (0, −1): hidden = ReLU(1, 1) = (1, 1). With W₂ = [[1, 1], [1, −1]] and b₂ = (0.5, 0.5): output = (1 + 1 + 0.5, 1 − 1 + 0.5) = <b>(2.5, 0.5)</b>.</p>
<p><b>Add and norm.</b> A residual path (as in ResNet) keeps gradients flowing. Layer norm keeps values stable, with no dependence on batch. x = (1, 2) plus sublayer (1, 0) gives (2, 2): every value is the same, so normalised they're all 0. For (1, 2, 3) with sublayer 0: mean 2, std 0.8165, giving (−1.2247, 0, 1.2247).</p>
<p><b>Size of one block</b> (d = 768):</p>
<table><tr><th>Part</th><th>Formula</th><th>Parameters</th></tr>
<tr><td>Attention</td><td>4d²</td><td>2,359,296</td></tr>
<tr><td>Feed-forward 1</td><td>4d² + 4d</td><td>2,362,368</td></tr>
<tr><td>Feed-forward 2</td><td>4d² + d</td><td>2,360,064</td></tr>
<tr><td>Two layer norms</td><td>4d</td><td>3,072</td></tr>
<tr><td colspan="2"><b>Total</b></td><td><b>7,084,800</b></td></tr></table>
<p>A 12-block model holds 85 million. Add a 50,000 × 768 token table and 1,000 × 768 positions, and you have about <b>124 million</b>. If the output layer shares the token table (<b>weight tying</b>), it avoids another 38.4 million parameters, or 153.6 MB.</p>
""", practice=["Position-Wise Feed-Forward", "Add and Norm", "Transformer Block Parameters", "Add Positions to Embeddings", "Weight Tying Savings"])


LESSON("Advanced", "Costs, and a transformer in PyTorch", """
<p><b>Attention compares every token with every token</b>, so cost grows with the square of length:</p>
<table><tr><th>Tokens T</th><th>T²</th><th>Relative to 100 tokens</th></tr><tr><td>100</td><td>10,000</td><td>1×</td></tr><tr><td>1,000</td><td>1,000,000</td><td>100×</td></tr><tr><td>4,000</td><td>16,000,000</td><td>1,600×</td></tr></table>
<p>This matters for real applications, because longer prompts are slower and need more memory. Generation uses tricks to reduce the cost, such as caching earlier keys and values, which the next topic explains.</p>
<pre><code class="py">import torch, torch.nn as nn, torch.nn.functional as F

class Block(nn.Module):
    def __init__(self, d, heads):
        super().__init__()
        self.norm1, self.norm2 = nn.LayerNorm(d), nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, heads, batch_first=True)
        self.ff = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))

    def forward(self, x, mask):
        y = self.norm1(x)
        x = x + self.attn(y, y, y, attn_mask=mask, need_weights=False)[0]
        return x + self.ff(self.norm2(x))

T = 20
mask = nn.Transformer.generate_square_subsequent_mask(T)
out = Block(64, 4)(torch.randn(8, T, 64), mask)     # (8, 20, 64)</code></pre>
<p><b>Mask convention trap:</b> PyTorch's <code>attn_mask</code> uses True or −∞ to mean <i>blocked</i>, while <code>F.scaled_dot_product_attention</code> with a boolean mask uses True to mean <i>allowed</i>. Mixing them up gives no error, only a model that quietly trains wrongly.</p>
<p>PyTorch code here is shown as text and was tested separately; it doesn't run in the browser IDE.</p>
""", practice=["Attention Cost vs Length"])
