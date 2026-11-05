from lib import *

THEORY("Decoding methods", """
<table><tr><th>Method</th><th>Rule</th><th>Best for</th></tr>
<tr><td>Greedy</td><td>top token</td><td>deterministic, short outputs</td></tr>
<tr><td>Beam search</td><td>keep the best few paths</td><td>translation, speech</td></tr>
<tr><td>Temperature</td><td>softmax(logits / T)</td><td>controlling variety</td></tr>
<tr><td>Top-k</td><td>keep k tokens</td><td>removing the tail</td></tr>
<tr><td>Top-p</td><td>keep up to total probability p</td><td>adapting to certainty</td></tr></table>
""")

THEORY("Numbers worth remembering", """
<table><tr><th>Quantity</th><th>Value</th></tr>
<tr><td>Initial loss</td><td>ln V</td></tr>
<tr><td>Perplexity of a uniform guess</td><td>V</td></tr>
<tr><td>Cost without KV cache</td><td>N·P + N(N−1)/2</td></tr>
<tr><td>Cost with KV cache</td><td>P + N − 1</td></tr>
<tr><td>Entropy of a uniform guess</td><td>ln V</td></tr></table>
""")

THEORY("Common bugs", """
<ul><li>Forgetting to shift targets: the model learns to copy its input and reports a nearly-zero loss.</li>
<li>Missing the causal mask, with the same symptom.</li>
<li>A loss far from ln V at the start, usually a sign of a data or label bug.</li>
<li>Comparing perplexity across different tokenisers.</li>
<li>Padding counted in the loss.</li></ul>
""")

FAQ("What does temperature do?", "<p>It divides the logits before softmax. Below 1 sharpens the distribution, above 1 flattens it. It doesn't change the order of tokens.</p>")
FAQ("Top-k or top-p?", "<p>Top-p adapts: it keeps few tokens when the model is sure, more when unsure. Top-k keeps the same number regardless.</p>")
FAQ("What is perplexity?", "<p>The exponential of the average negative log probability. It reads as the effective number of equally likely choices the model is torn between.</p>")
FAQ("Why does an LLM need a KV cache?", "<p>Previous tokens' keys and values don't change, so storing them avoids recomputing the whole sequence for every new token.</p>")
FAQ("Why do LLMs make things up?", "<p>They're trained to produce likely text. Likely and true often coincide, but not always, and the model has no built-in guarantee of truth.</p>")
