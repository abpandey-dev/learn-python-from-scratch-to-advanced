from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


LESSON("Basics", "Why not just use dense layers on images?", """
<p>A 224 × 224 colour image has 224 × 224 × 3 = 150,528 input values. A dense layer of only 64 neurons needs (150,528 + 1) × 64 = <b>9,633,856</b> parameters. A convolutional layer with 64 filters of size 3 × 3 needs (3 × 3 × 3 + 1) × 64 = <b>1,792</b>.</p>
<p>Two good assumptions about images make this possible:</p>
<ul><li><b>Locality:</b> nearby pixels matter most. An edge is found from a small patch.</li>
<li><b>Weight sharing:</b> an edge detector useful in one corner is useful everywhere, so one filter slides over the whole image.</li></ul>
<p>A result is <b>translation equivariance</b>: move the cat, and the filter's response moves with it.</p>
""", practice=["Dense vs Conv Parameters", "Parameters in a Conv Layer", "Operations in a Conv Layer"])


LESSON("Basics", "1-D convolution by hand", """
<p>x = 1, 2, 3, 4, 5 and kernel k = 1, 0, −1. Slide the kernel along, multiply and add:</p>
<table><tr><th>Position</th><th>Window</th><th>Calculation</th><th>Output</th></tr>
<tr><td>0</td><td>1, 2, 3</td><td>1·1 + 2·0 + 3·(−1)</td><td>−2</td></tr>
<tr><td>1</td><td>2, 3, 4</td><td>2·1 + 3·0 + 4·(−1)</td><td>−2</td></tr>
<tr><td>2</td><td>3, 4, 5</td><td>3·1 + 4·0 + 5·(−1)</td><td>−2</td></tr></table>
<p>This filter measures the change across its window. The input rises steadily, so the output is constant. Kernel (0.5, 0.5) would instead be a moving average.</p>
<p>In a CNN, <b>the kernel's numbers are learned</b>; nobody hand-designs them.</p>
<p><b>Terminology:</b> strictly speaking this is <i>cross-correlation</i>. True maths convolution flips the kernel first. Deep learning calls this "convolution" anyway, and since the filter is learned, the flip doesn't matter.</p>
""", practice=["1-D Convolution", "1-D Convolution With Padding"])


@LD
def conv_1d_steps():
    x = np.array([1, 2, 3, 4, 5, 4, 3, 2, 1, 1])
    change = np.correlate(x, [1, 0, -1], "valid")
    smooth = np.correlate(x, [0.5, 0.5], "valid")
    fig, ax = plt.subplots(figsize=(4.8, 2.8))
    ax.plot(x, "o-", label="input")
    ax.plot(change, "s-", label="kernel 1, 0, −1")
    ax.plot(smooth, "^-", label="kernel 0.5, 0.5")
    ax.axhline(0, color="black", linewidth=0.5)
    ax.legend(fontsize=7)


LESSON("Core", "2-D convolution and finding edges", """
<p>Here's an image with a vertical edge, and the Sobel filter:</p>
<pre><code class="py">image = [[0, 0, 9, 9],      filter = [[-1, 0, 1],
         [0, 0, 9, 9],                [-2, 0, 2],
         [0, 0, 9, 9]]                [-1, 0, 1]]</code></pre>
<p>On the top-left 3 × 3 patch, the filter gives (−0 + 9) + (−0 + 18) + (−0 + 9) = <b>36</b>. The next patch also gives 36. On a flat region, the left and right columns cancel to 0, so the filter "lights up" only at edges.</p>
<p>The chart applies filters to a simple picture. A CNN learns many such filters by itself. Early layers end up detecting edges and colours, and later layers respond to textures, parts and objects.</p>
""", practice=["2-D Convolution", "Detect a Vertical Edge", "Convolution With Stride"])


@LD
def filter_picture():
    from numpy.lib.stride_tricks import sliding_window_view
    x, y = np.meshgrid(np.linspace(-1, 1, 80), np.linspace(-1, 1, 80))
    image = ((np.abs(x) < 0.5) & (np.abs(y) < 0.5)).astype(float)
    vertical = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    fig, axes = plt.subplots(1, 3, figsize=(7.5, 2.5))
    results = [image, (sliding_window_view(image, (3, 3)) * vertical).sum(axis=(2, 3)), (sliding_window_view(image, (3, 3)) * vertical.T).sum(axis=(2, 3))]
    for ax, picture, name in zip(axes, results, ["input", "vertical edges", "horizontal edges"]):
        ax.imshow(picture, cmap="gray")
        ax.set_title(name, fontsize=9)
        ax.axis("off")
    fig.tight_layout()


LESSON("Core", "Stride, padding and output size", """
<p style="text-align:center"><b>output = ⌊(n + 2p − k) / s⌋ + 1</b></p>
<table><tr><th>n</th><th>Kernel k</th><th>Stride s</th><th>Padding p</th><th>Calculation</th><th>Output</th></tr>
<tr><td>32</td><td>3</td><td>1</td><td>1</td><td>(32 + 2 − 3)/1 + 1</td><td>32 (same size)</td></tr>
<tr><td>32</td><td>2</td><td>2</td><td>0</td><td>(32 − 2)/2 + 1</td><td>16 (halved)</td></tr>
<tr><td>224</td><td>7</td><td>2</td><td>3</td><td>⌊223/2⌋ + 1</td><td>112</td></tr></table>
<h4>Tracking a whole network</h4>
<p>32 → conv(3, 1, 1) → 32 → pool(2, 2) → 16 → conv(3, 1, 1) → 16 → pool(2, 2) → <b>8</b>. With 32 channels at the end, the classifier's input is 32 × 8 × 8 = <b>2,048</b>. Working this out wrongly is the most common CNN error, and it's why you should print shapes.</p>
<p><b>Multiple channels:</b> an RGB filter has 3 × k × k weights and gives one output map. 64 filters give 64 maps.</p>
""", practice=["Output Size", "Shape Through a Network", "Flatten Size for the Classifier", "Convolution Across Channels", "Normalise Image Channels"])


LESSON("Core", "Pooling and the receptive field", """
<h4>Pooling</h4>
<p><b>Max pooling</b> with size 2 turns each 2 × 2 block into its largest value. It halves the size and adds a little tolerance to small shifts. <b>Global average pooling</b> turns each whole map into one number, which removes the need for huge dense layers at the end.</p>
<h4>Receptive field: how much does one output see?</h4>
<p>For each layer: r ← r + (k − 1) × jump, then jump ← jump × s. Start with r = 1, jump = 1.</p>
<table><tr><th>Layer (k, s)</th><th>r</th><th>jump</th></tr>
<tr><td>conv (3, 1)</td><td>3</td><td>1</td></tr><tr><td>pool (2, 2)</td><td>4</td><td>2</td></tr>
<tr><td>conv (3, 1)</td><td>8</td><td>2</td></tr><tr><td>pool (2, 2)</td><td>10</td><td>4</td></tr>
<tr><td>conv (3, 1)</td><td>18</td><td>4</td></tr></table>
<p>So three plain 3 × 3 layers see just 7 pixels, but with pooling, the same three see 18. To recognise an object, the receptive field must be about as big as the object.</p>
""", practice=["Max Pooling", "Average Pooling", "Global Average Pooling", "Receptive Field"])


@LD
def receptive_growth():
    layers = [(3, 1), (2, 2), (3, 1), (2, 2), (3, 1), (2, 2), (3, 1)]
    pooled, plain = [], []
    r, jump = 1, 1
    for k, s in layers:
        r += (k - 1) * jump
        jump *= s
        pooled.append(r)
    r = 1
    for k, s in layers:
        r += k - 1
        plain.append(r)
    fig, ax = plt.subplots(figsize=(4.6, 2.8))
    ax.plot(range(1, 8), pooled, "o-", label="with pooling")
    ax.plot(range(1, 8), plain, "o-", label="without")
    ax.set_xlabel("layer")
    ax.set_ylabel("receptive field (pixels)")
    ax.legend(fontsize=8)


LESSON("Advanced", "1×1 convolutions and residual connections", """
<h4>1 × 1 convolutions</h4>
<p>A 1 × 1 filter looks at one position across all channels, so it <b>mixes channels without changing height and width</b>. Going from 256 to 64 channels makes later layers far cheaper.</p>
<h4>Residual connections: output = x + F(x)</h4>
<p>Around 2015, researchers found that much deeper plain networks did <i>worse</i>, even on training data. ResNet's fix was to learn just the <b>change</b> F(x).</p>
<ul><li><b>Doing nothing is easy:</b> with F's weights at zero, output = x. A new layer can't easily hurt.</li>
<li><b>Gradients flow:</b> the derivative of x + F(x) is 1 + F′(x), so the "1" gives gradients a direct route back. Without it they multiply and shrink.</li></ul>
<p>This same idea appears in every transformer block.</p>
<table><tr><th>Architecture</th><th>Idea</th></tr>
<tr><td>VGG</td><td>stacks of 3 × 3 convolutions</td></tr>
<tr><td>ResNet</td><td>residual connections</td></tr>
<tr><td>MobileNet</td><td>cheap depthwise-separable convolutions</td></tr>
<tr><td>Vision Transformer</td><td>attention over image patches</td></tr></table>
""", practice=["1×1 Convolution", "A Residual Block"])


@LD
def residual_gradients():
    depths = np.arange(1, 51)
    plain = 0.7 ** depths
    residual = 1.0 + 0 * depths
    fig, ax = plt.subplots(figsize=(4.6, 2.8))
    ax.semilogy(depths, plain, label="plain: each layer multiplies by 0.7")
    ax.semilogy(depths, residual, label="residual: a direct path keeps 1")
    ax.set_xlabel("layers from the output")
    ax.set_ylabel("gradient size (illustration)")
    ax.legend(fontsize=7)


LESSON("Advanced", "Transfer learning and a CNN in PyTorch", """
<p>You rarely train an image model from zero. <b>Transfer learning</b> reuses a network trained on millions of images:</p>
<ol><li>Load a pre-trained model.</li><li>Replace the final layer with one for your classes.</li><li>Train only that layer first.</li><li>Optionally unfreeze more layers, with a small learning rate.</li></ol>
<p>With a few hundred images per class, this often beats anything you could train from scratch. <b>Augmentation</b> helps too: random flips, crops and colour changes create new views. Check they make sense: rotating a "6" upside down makes a "9", so that label would be wrong.</p>
<pre><code class="py">class SmallCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.classifier = nn.Linear(32 * 8 * 8, 10)

    def forward(self, x):                  # x: (N, 3, 32, 32)
        x = self.features(x)               # (N, 32, 8, 8)
        return self.classifier(x.flatten(1))   # (N, 10)</code></pre>
""", practice=["Flip Augmentation"])
