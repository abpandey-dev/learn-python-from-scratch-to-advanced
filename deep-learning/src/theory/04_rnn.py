from lib import *

THEORY("The three cells", """
<table><tr><th>Cell</th><th>Update</th><th>Weight sets</th></tr>
<tr><td>RNN</td><td>h = tanh(W_h·h + W_x·x + b)</td><td>1</td></tr>
<tr><td>GRU</td><td>h = (1 − u)·h + u·tanh(z)</td><td>3</td></tr>
<tr><td>LSTM</td><td>c = f·c + i·tanh(z); h = o·tanh(c)</td><td>4</td></tr></table>
<p>Parameters per set: d·h + h·h + h. Frameworks can differ slightly in how they count biases.</p>
""")

THEORY("Shapes to remember (batch first)", """
<table><tr><th>Thing</th><th>Shape</th></tr>
<tr><td>Token ids</td><td>(N, T)</td></tr>
<tr><td>Embedded</td><td>(N, T, d)</td></tr>
<tr><td>All outputs</td><td>(N, T, h); (N, T, 2h) if bidirectional</td></tr>
<tr><td>Final state</td><td>(layers × directions, N, h)</td></tr>
<tr><td>Next-token scores</td><td>(N, T, vocab)</td></tr></table>
""")

THEORY("Common bugs", """
<ul><li>Averaging the loss over padding positions.</li>
<li>Taking the last column instead of the last <i>real</i> output.</li>
<li>Forgetting <code>batch_first=True</code>.</li>
<li>Shuffling a time series across the train/test boundary.</li>
<li>Using a bidirectional model for next-token prediction, which lets it see the answer.</li>
<li>Not clipping gradients. RNNs are especially prone to exploding.</li></ul>
""")

FAQ("Why do RNNs have vanishing gradients?", "<p>The gradient is multiplied by roughly the same factor once per step. Factors below 1 shrink it exponentially over long sequences.</p>")
FAQ("How does an LSTM help?", "<p>Its cell state is updated mostly by addition, controlled by gates. With the forget gate near 1, the signal and its gradient pass along largely intact.</p>")
FAQ("LSTM or GRU?", "<p>They perform similarly on most tasks. A GRU is smaller and faster; an LSTM has more separate control. Test both if it matters.</p>")
FAQ("What is teacher forcing?", "<p>Feeding the true previous token during training, instead of the model's own prediction. It speeds up training but can leave the model weak at recovering from its own errors.</p>")
FAQ("Why mask padding?", "<p>Padding only exists to make tensors rectangular. If it reaches the loss, pooling or attention, the model's results depend on meaningless values.</p>")
