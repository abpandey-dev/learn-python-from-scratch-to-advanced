from lib import *

THEORY("The formula, piece by piece", """
<table><tr><th>Piece</th><th>Shape (one sequence)</th><th>Purpose</th></tr>
<tr><td>Q·Kᵀ</td><td>(T_q, T_k)</td><td>similarity of every pair</td></tr>
<tr><td>÷ √d</td><td>same</td><td>keeps the spread near 1</td></tr>
<tr><td>mask → −∞</td><td>same</td><td>hides positions</td></tr>
<tr><td>softmax over keys</td><td>same</td><td>each row sums to 1</td></tr>
<tr><td>× V</td><td>(T_q, d)</td><td>weighted average of values</td></tr></table>
""")

THEORY("Attention variants", """
<table><tr><th>Type</th><th>Q from</th><th>K, V from</th><th>Used for</th></tr>
<tr><td>Self-attention</td><td>sequence</td><td>same sequence</td><td>encoders, classifiers</td></tr>
<tr><td>Masked self-attention</td><td>sequence</td><td>same, past only</td><td>LLMs, generation</td></tr>
<tr><td>Cross-attention</td><td>decoder</td><td>encoder</td><td>translation, image-to-text</td></tr></table>
""")

THEORY("Design choices in a block", """
<ul><li><b>Pre-norm</b> (norm before each sublayer) is common in recent models, and tends to train more stably.</li>
<li><b>Feed-forward width</b> is about 4d in the classic design.</li>
<li><b>Activation:</b> ReLU originally; GELU and variants are now common.</li>
<li><b>Positions:</b> sinusoidal, learned or rotary, depending on the model.</li>
<li><b>Weight tying</b> shares the token table with the output layer, saving memory.</li></ul>
""")

FAQ("Why is the score divided by √d?", "<p>Dot products of random vectors spread out in proportion to √d. Without the division, large scores push softmax to nearly all-or-nothing, which gives tiny gradients.</p>")
FAQ("What's the difference between self- and cross-attention?", "<p>In self-attention, queries, keys and values come from one sequence. In cross-attention, queries come from one and keys and values from another.</p>")
FAQ("Why multiple heads?", "<p>Several smaller attentions can each learn a different way of relating tokens, at about the same total cost as one large attention.</p>")
FAQ("Why does a transformer need positional information?", "<p>Attention itself ignores order: shuffle the tokens and each token's output is the same, only shuffled. Positions must be added explicitly.</p>")
FAQ("What is a causal mask for?", "<p>It stops a position seeing later tokens. Without it, a next-token model simply reads the answer during training, and then fails when generating.</p>")
