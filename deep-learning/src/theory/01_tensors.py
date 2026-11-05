from lib import *

THEORY("Core vocabulary", """
<table><tr><th>Term</th><th>Meaning</th></tr>
<tr><td>Tensor</td><td>n-dimensional array</td></tr>
<tr><td>Dense / linear / fully connected layer</td><td>z = Wx + b</td></tr>
<tr><td>Activation</td><td>non-linearity applied after a layer</td></tr>
<tr><td>Logits</td><td>raw scores before softmax</td></tr>
<tr><td>Loss</td><td>a number measuring how wrong the model is</td></tr>
<tr><td>Forward pass</td><td>inputs → predictions</td></tr>
<tr><td>Backward pass</td><td>loss → gradient of every weight</td></tr>
<tr><td>Parameters</td><td>the weights and biases learned</td></tr>
<tr><td>Hyper-parameters</td><td>settings you choose: learning rate, depth, width</td></tr></table>
""")

THEORY("Numerical stability", """
<ul><li>Sum logs instead of multiplying probabilities.</li>
<li>Use the log-sum-exp trick: log Σ eᶻ = max(z) + log Σ e^(z − max z).</li>
<li>Prefer losses that take logits (<code>BCEWithLogitsLoss</code>, <code>CrossEntropyLoss</code>).</li>
<li>Float16 and mixed precision speed up training but need loss scaling to avoid underflow.</li></ul>
""")

THEORY("Common shape bugs", """
<table><tr><th>Bug</th><th>Symptom</th><th>Fix</th></tr>
<tr><td>(n,) minus (n, 1)</td><td>silent n × n table; loss won't fall</td><td>squeeze one, or match shapes</td></tr>
<tr><td>Wrong flatten size</td><td>"mat1 and mat2 shapes" error</td><td>print the shape before the dense layer</td></tr>
<tr><td>Channels last vs first</td><td>wrong number of channels error</td><td>PyTorch wants (N, C, H, W)</td></tr>
<tr><td>Forgetting the batch dimension</td><td>errors on a single example</td><td>add one: <code>x.unsqueeze(0)</code></td></tr></table>
""")

FAQ("Why do we use batches?", "<p>A batch gradient is a cheap, reasonably accurate estimate of the full gradient. GPUs also process many examples in parallel. Noise from small batches is often harmless or even helpful.</p>")
FAQ("What are logits?", "<p>The raw, unnormalised outputs of the last layer. Softmax or sigmoid turns them into probabilities.</p>")
FAQ("Why can't all weights start at zero?", "<p>Neurons in a layer would stay identical, because they'd compute the same output and get the same gradient. Random starts break this symmetry.</p>")
FAQ("Glorot vs He initialisation?", "<p>Both keep signal variance steady across layers. Glorot suits tanh and sigmoid; He doubles the variance for ReLU, which silences about half its inputs.</p>")
FAQ("What does loss.backward() do?", "<p>It walks the recorded computation backwards with the chain rule, storing each parameter's gradient in its .grad field.</p>")
