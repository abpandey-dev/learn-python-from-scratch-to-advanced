from lib import *

THEORY("Architecture", """
<p>A <b>multi-layer perceptron</b> (MLP) is a composition of layers: h⁽ˡ⁾ = g(W⁽ˡ⁾h⁽ˡ⁻¹⁾ + b⁽ˡ⁾), with h⁽⁰⁾ = x. A layer from a inputs to b outputs has a·b + b parameters. <b>Depth</b> is the number of layers, <b>width</b> the neurons per layer.</p>
<table>
<tr><th>Task</th><th>Output layer</th><th>Loss</th></tr>
<tr><td>Regression</td><td>linear</td><td>(half) mean squared error</td></tr>
<tr><td>Binary classification</td><td>1 sigmoid</td><td>binary cross-entropy</td></tr>
<tr><td>Multi-class</td><td>k softmax</td><td>categorical cross-entropy</td></tr>
<tr><td>Multi-label</td><td>k sigmoids</td><td>binary cross-entropy per label</td></tr>
</table>
""")

THEORY("Backpropagation", """
<p>For a network x → h → ŷ → L, the chain rule gives ∂L/∂W = (∂L/∂ŷ)(∂ŷ/∂h)(∂h/∂W). Backprop evaluates this from the output backwards, reusing intermediate results, so all gradients cost about one extra pass. It is <b>reverse-mode automatic differentiation</b>, which PyTorch and JAX perform for you.</p>
<ul>
<li><b>Vanishing gradients</b>: products of small slopes shrink towards 0 (sigmoid, tanh, very deep nets).</li>
<li><b>Exploding gradients</b>: products of large values grow; use gradient clipping.</li>
<li><b>Dead ReLUs</b>: neurons stuck at 0 output with zero gradient; try a lower learning rate or Leaky ReLU.</li>
</ul>
""")

THEORY("Optimisers", """
<table>
<tr><th>Optimiser</th><th>Update</th></tr>
<tr><td>SGD</td><td>w ← w − η·g</td></tr>
<tr><td>Momentum</td><td>v ← μv − η·g; w ← w + v</td></tr>
<tr><td>RMSProp</td><td>divide by a running average of g²</td></tr>
<tr><td>Adam</td><td>m ← β₁m + (1 − β₁)g; v ← β₂v + (1 − β₂)g²; w ← w − η·m̂/(√v̂ + ε), with bias correction</td></tr>
<tr><td>AdamW</td><td>Adam with weight decay kept separate from the gradient</td></tr>
</table>
<p>The learning rate is the most important setting. Schedules (step, cosine, warm-up) reduce it during training. An <b>epoch</b> is one pass through the data; a <b>batch</b> is the group used for one step.</p>
""")

THEORY("Initialisation and regularisation", """
<table>
<tr><th>Technique</th><th>What it does</th></tr>
<tr><td>Random initialisation</td><td>breaks symmetry; all-zero weights make every neuron identical</td></tr>
<tr><td>Glorot / Xavier</td><td>scales the range by fan-in + fan-out; suits tanh and sigmoid</td></tr>
<tr><td>He</td><td>scales by fan-in; suits ReLU</td></tr>
<tr><td>L2 / weight decay</td><td>penalises large weights</td></tr>
<tr><td>Dropout</td><td>randomly zeroes activations while training, scaled by 1/keep</td></tr>
<tr><td>Batch / layer normalisation</td><td>stabilises each layer's inputs</td></tr>
<tr><td>Early stopping</td><td>stops when validation loss stops improving</td></tr>
<tr><td>Data augmentation</td><td>more varied training examples</td></tr>
</table>
""")

THEORY("Beyond the MLP", """
<table>
<tr><th>Architecture</th><th>Key idea</th><th>Used for</th></tr>
<tr><td>CNN</td><td>small filters shared across an image</td><td>images, some audio</td></tr>
<tr><td>RNN / LSTM</td><td>state carried along a sequence</td><td>time series, older language models</td></tr>
<tr><td>Transformer</td><td>attention: every token weighs every other token</td><td>language, LLMs, much more</td></tr>
<tr><td>Autoencoder</td><td>compress, then reconstruct</td><td>representations, anomaly detection</td></tr>
</table>
<p>For tables, gradient-boosted trees usually beat MLPs with far less tuning.</p>
""")

FAQ("Why do neural networks need non-linear activations?", "<p>A composition of linear functions is still linear, so without them any depth of network could only model straight-line relationships.</p>")
FAQ("What is backpropagation?", "<p>An efficient use of the chain rule that computes the gradient of the loss with respect to every weight by passing the error backwards through the network. The optimiser then uses those gradients to update the weights.</p>")
FAQ("Why not initialise all weights to zero?", "<p>Neurons in a layer would compute the same output and receive the same gradient, so they'd stay identical forever. Random initialisation breaks that symmetry.</p>")
FAQ("Why is ReLU preferred to sigmoid in hidden layers?", "<p>Its slope is 1 for positive inputs, so gradients don't shrink through many layers, and it is cheap to compute. Sigmoid's slope is at most 0.25 and nearly 0 for large inputs.</p>")
FAQ("What does dropout do?", "<p>During training it randomly zeroes activations, which stops neurons relying on specific others and acts like averaging many smaller networks. It is switched off for prediction.</p>")
FAQ("SGD vs Adam?", "<p>Adam adapts a step size per weight and usually trains quickly with little tuning. Well-tuned SGD with momentum can generalise as well or better on some problems, especially in vision.</p>")
FAQ("How do you know a network is overfitting?", "<p>Training loss keeps falling while validation loss stops improving or rises. Add regularisation or data, shrink the network, or stop early.</p>")
