from lib import *

THEORY("Formulas", """
<table><tr><th>Quantity</th><th>Formula</th></tr>
<tr><td>Output size</td><td>⌊(n + 2p − k)/s⌋ + 1</td></tr>
<tr><td>Parameters</td><td>(k_h·k_w·c_in + 1)·c_out</td></tr>
<tr><td>Multiplications</td><td>k_h·k_w·c_in·c_out·H·W</td></tr>
<tr><td>Receptive field</td><td>r ← r + (k − 1)·j; j ← j·s</td></tr></table>
<p>Parameters don't depend on image size, while operations do. A cheap-to-store model can still be slow.</p>
""")

THEORY("Beyond plain convolution", """
<table><tr><th>Variant</th><th>Idea</th></tr>
<tr><td>Dilated</td><td>gaps in the kernel: larger view, same cost</td></tr>
<tr><td>Depthwise separable</td><td>per-channel filter + 1×1 mix; much cheaper</td></tr>
<tr><td>Transposed</td><td>upsamples, used in segmentation and generation</td></tr>
<tr><td>Vision transformer</td><td>attention over image patches; needs more data or pre-training</td></tr></table>
""")

THEORY("Common computer-vision tasks", """
<table><tr><th>Task</th><th>Output</th></tr>
<tr><td>Classification</td><td>one label per image</td></tr>
<tr><td>Detection</td><td>boxes and labels</td></tr>
<tr><td>Segmentation</td><td>one label per pixel</td></tr>
<tr><td>Embedding</td><td>a vector for similarity search</td></tr></table>
""")

FAQ("Why do CNNs need fewer parameters than dense networks?", "<p>Each filter only looks at a small patch (locality), and the same filter is reused across the image (weight sharing).</p>")
FAQ("What does pooling do?", "<p>It shrinks the map, widens the receptive field and adds small shift tolerance, with no parameters to learn.</p>")
FAQ("What is a receptive field?", "<p>The input region that can influence one output. It grows with depth and much faster with stride or pooling.</p>")
FAQ("Why do residual connections help?", "<p>They make the identity easy to learn and give gradients a direct path back, so very deep networks can train.</p>")
FAQ("What is transfer learning?", "<p>Reusing a model trained on a large dataset as the starting point for a new task, usually replacing the final layer.</p>")
