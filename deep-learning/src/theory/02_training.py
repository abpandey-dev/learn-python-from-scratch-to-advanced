from lib import *

THEORY("Optimisers", """
<table><tr><th>Name</th><th>Update</th><th>Notes</th></tr>
<tr><td>SGD</td><td>w −= ηg</td><td>simple; good final quality when tuned</td></tr>
<tr><td>Momentum</td><td>v = μv − ηg; w += v</td><td>faster through ravines</td></tr>
<tr><td>RMSProp</td><td>divide by √(EMA of g²)</td><td>per-weight step sizes</td></tr>
<tr><td>Adam</td><td>momentum + RMSProp + bias correction</td><td>good default</td></tr>
<tr><td>AdamW</td><td>Adam + decoupled decay</td><td>default for transformers</td></tr></table>
""")

THEORY("A practical recipe", """
<ol><li>Overfit a tiny batch to prove the code works.</li>
<li>Start with AdamW, lr 1e-3 (or 1e-4 to 3e-5 when fine-tuning a transformer).</li>
<li>Use warm-up and cosine decay, with gradient clipping at 1.0.</li>
<li>Add regularisation only after you see overfitting.</li>
<li>Change one thing at a time; log experiments with their settings.</li></ol>
""")

THEORY("Normalisation layers", """
<table><tr><th>Layer</th><th>Normalises across</th><th>Used in</th></tr>
<tr><td>BatchNorm</td><td>the batch, per feature</td><td>CNNs</td></tr>
<tr><td>LayerNorm</td><td>the features of each example</td><td>transformers</td></tr>
<tr><td>GroupNorm</td><td>groups of channels</td><td>small-batch vision</td></tr>
<tr><td>RMSNorm</td><td>LayerNorm without centring</td><td>many modern LLMs</td></tr></table>
""")

FAQ("Adam vs SGD?", "<p>Adam converges fast with little tuning. SGD with momentum and a good schedule can generalise slightly better in some vision tasks. Start with Adam or AdamW.</p>")
FAQ("Why warm up the learning rate?", "<p>Early gradients are large and unreliable, and Adam's averages haven't settled, so a small starting rate prevents the training from blowing up.</p>")
FAQ("Batch norm vs layer norm?", "<p>Batch norm normalises each feature across the batch and depends on batch size. Layer norm normalises each example across features, works at batch size 1, and is the norm for sequence models.</p>")
FAQ("Why is gradient clipping used?", "<p>A rare extreme gradient can destroy the weights in one step. Clipping limits the update size while keeping the direction, which is especially useful for RNNs and transformers.</p>")
FAQ("What is gradient accumulation?", "<p>Summing gradients over several small batches before an update, to simulate a larger batch than fits in memory.</p>")
FAQ("What is label smoothing?", "<p>Replacing hard 0/1 targets with slightly softened ones. It reduces overconfidence and can improve generalisation.</p>")
