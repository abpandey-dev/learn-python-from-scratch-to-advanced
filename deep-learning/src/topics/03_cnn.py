from lib import *
import math
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


TOPIC(
    id="cnn", title="Convolutional Networks", glyph="▦",
    blurb="How networks see: convolution by hand, stride and padding, output sizes, parameter counts, pooling, receptive fields, channels, 1×1 convolutions and residual connections.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">output = floor((n + 2p − k) / s) + 1
params = (k·k·in_channels + 1)·out_channels
receptive field: r ← r + (k − 1)·jump;  jump ← jump·s
sliding_window_view(img, (k, k))         # all k × k patches
(windows * kernel).sum(axis=(2, 3))      # 2-D convolution</code></pre>
<p>PyTorch: <code>nn.Conv2d(in, out, kernel_size, stride, padding)</code>; images are (batch, channels, height, width).</p>
""")

IMG = [[1, 2, 3, 0], [4, 5, 6, 1], [7, 8, 9, 2], [1, 0, 1, 3]]
K2 = [[1, 0], [0, -1]]
EDGE = [[0, 0, 9, 9], [0, 0, 9, 9], [0, 0, 9, 9]]
SOBEL = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]


def conv2d_loops(img, kernel, stride=1):
    h, w = len(img), len(img[0])
    kh, kw = len(kernel), len(kernel[0])
    out = []
    for i in range(0, h - kh + 1, stride):
        row = []
        for j in range(0, w - kw + 1, stride):
            row.append(sum(img[i + a][j + b] * kernel[a][b] for a in range(kh) for b in range(kw)))
        out.append(row)
    return out



Q(None, "1-D Convolution", "Easy", "Slide and multiply",
  "Slide kernel k along x with no padding (no flipping, as deep learning does) and return the dot product at each position.",
  [(([1, 2, 3, 4, 5], [1, 0, -1]), [-2, -2, -2]), (([2, 4, 6], [0.5, 0.5]), [3.0, 5.0])],
  ("Two nested loops.", "O(n·k)", "O(n)"),
  ("<code>np.correlate(x, k, 'valid')</code>.", "O(n·k)", "O(n)"),
  names=["x", "k"])


@B
def conv1d(x, k):
    out = []
    for i in range(len(x) - len(k) + 1):
        out.append(sum(x[i + j] * k[j] for j in range(len(k))))
    return out


@O
def conv1d(x, k):
    return np.correlate(x, k, "valid")


Q(None, "1-D Convolution With Padding", "Easy", "Keep the edges",
  "Add p zeros to each end of x, then convolve.",
  [(([1, 2, 3], [1, 1, 1], 1), [3, 6, 5])],
  ("Build the padded list, then two loops.", "O(n·k)", "O(n)"),
  ("<code>np.pad</code> and <code>np.correlate</code>.", "O(n·k)", "O(n)"),
  names=["x", "k", "p"])


@B
def conv1d_pad(x, k, p):
    x = [0] * p + list(x) + [0] * p
    return [sum(x[i + j] * k[j] for j in range(len(k))) for i in range(len(x) - len(k) + 1)]


@O
def conv1d_pad(x, k, p):
    return np.correlate(np.pad(x, p), k, "valid")


Q(None, "Output Size", "Easy", "⌊(n + 2p − k)/s⌋ + 1",
  "Return how many positions a kernel of size k fits along n, with padding p and stride s.",
  [((224, 7, 2, 3), 112), ((32, 3, 1, 1), 32), ((5, 2, 2, 0), 2)],
  ("Walk the kernel along, counting positions.", "O(n / s)", "O(1)"),
  ("The formula.", "O(1)", "O(1)"),
  names=["n", "k", "s", "p"])


@B
def output_size(n, k, s, p):
    total, start, count = n + 2 * p, 0, 0
    while start + k <= total:
        count += 1
        start += s
    return count


@O
def output_size(n, k, s, p):
    return (n + 2 * p - k) // s + 1


Q(None, "2-D Convolution", "Medium", "A filter over an image",
  "Return the convolution of img with the kernel (no padding, stride 1).",
  [((IMG, K2), [[-4, -4, 2], [-4, -4, 4], [7, 7, 6]])],
  ("Four nested loops.", "O(h·w·k²)", "O(h·w)"),
  ("<code>sliding_window_view</code> gives all patches at once; multiply and sum.", "O(h·w·k²)", "O(h·w)"),
  names=["img", "kernel"])


@B
def conv2d(img, kernel):
    return conv2d_loops(img, kernel)


@O
def conv2d(img, kernel):
    kernel = np.array(kernel)
    windows = sliding_window_view(np.array(img), kernel.shape)
    return (windows * kernel).sum(axis=(2, 3))


Q(None, "Detect a Vertical Edge", "Easy", "The Sobel filter",
  "Apply the Sobel filter [[−1, 0, 1], [−2, 0, 2], [−1, 0, 1]] to the image.",
  [((EDGE,), [[36, 36]])],
  ("Four nested loops.", "O(h·w)", "O(h·w)"),
  ("Patch windows and a sum.", "O(h·w)", "O(h·w)"))


@B
def sobel(img):
    return conv2d_loops(img, SOBEL)


@O
def sobel(img):
    k = np.array(SOBEL)
    return (sliding_window_view(np.array(img), k.shape) * k).sum(axis=(2, 3))


Q(None, "Convolution With Stride", "Medium", "Skip positions",
  "Convolve with stride s in both directions.",
  [((IMG, K2, 2), [[-4, 2], [7, 6]])],
  ("Step the loops by s.", "O(h·w·k²/s²)", "O(h·w/s²)"),
  ("Patch windows, then slice <code>[::s, ::s]</code>.", "O(h·w)", "O(h·w)"),
  names=["img", "kernel", "s"])


@B
def conv2d_stride(img, kernel, s):
    return conv2d_loops(img, kernel, s)


@O
def conv2d_stride(img, kernel, s):
    kernel = np.array(kernel)
    windows = sliding_window_view(np.array(img), kernel.shape)[::s, ::s]
    return (windows * kernel).sum(axis=(2, 3))


Q(None, "Max Pooling", "Easy", "Keep the strongest",
  "Apply k × k max pooling with stride k.",
  [((IMG, 2), [[5, 6], [8, 9]])],
  ("Loops over blocks.", "O(h·w)", "O(h·w/k²)"),
  ("Windows, then <code>.max(axis=(2, 3))</code>.", "O(h·w)", "O(h·w)"),
  names=["img", "k"])


@B
def max_pool(img, k):
    out = []
    for i in range(0, len(img) - k + 1, k):
        row = []
        for j in range(0, len(img[0]) - k + 1, k):
            row.append(max(img[i + a][j + b] for a in range(k) for b in range(k)))
        out.append(row)
    return out


@O
def max_pool(img, k):
    return sliding_window_view(np.array(img), (k, k))[::k, ::k].max(axis=(2, 3))


Q(None, "Average Pooling", "Easy", "Smooth and shrink",
  "Apply k × k average pooling with stride k, rounded to 4 decimals.",
  [((IMG, 2), [[3.0, 2.5], [4.0, 3.75]])],
  ("Loops over blocks.", "O(h·w)", "O(h·w/k²)"),
  ("Windows, then <code>.mean(axis=(2, 3))</code>.", "O(h·w)", "O(h·w)"),
  names=["img", "k"])


@B
def avg_pool(img, k):
    out = []
    for i in range(0, len(img) - k + 1, k):
        row = []
        for j in range(0, len(img[0]) - k + 1, k):
            row.append(round(sum(img[i + a][j + b] for a in range(k) for b in range(k)) / (k * k), 4))
        out.append(row)
    return out


@O
def avg_pool(img, k):
    return sliding_window_view(np.array(img, dtype=float), (k, k))[::k, ::k].mean(axis=(2, 3)).round(4)


Q(None, "Global Average Pooling", "Easy", "One number per channel",
  "Input is (channels, height, width). Return the average of each channel, rounded to 4 decimals.",
  [(([[[1, 2], [3, 4]], [[0, 0], [0, 8]]],), [2.5, 2.0])],
  ("Add everything in loops per channel.", "O(c·h·w)", "O(c)"),
  ("<code>x.mean(axis=(1, 2))</code>.", "O(c·h·w)", "O(c)"))


@B
def global_avg(x):
    out = []
    for channel in x:
        values = [v for row in channel for v in row]
        out.append(round(sum(values) / len(values), 4))
    return out


@O
def global_avg(x):
    return np.array(x, dtype=float).mean(axis=(1, 2)).round(4)


Q(None, "Parameters in a Conv Layer", "Easy", "(k·k·in + 1)·out",
  "Return the number of learnable parameters, including one bias per filter.",
  [((3, 3, 64), 1792), ((5, 64, 128), 204928)],
  ("Add up each filter's weights and bias in a loop.", "O(out)", "O(1)"),
  ("The formula.", "O(1)", "O(1)"),
  names=["k", "in_channels", "out_channels"])


@B
def conv_params(k, in_channels, out_channels):
    total = 0
    for _ in range(out_channels):
        total += k * k * in_channels + 1
    return total


@O
def conv_params(k, in_channels, out_channels):
    return (k * k * in_channels + 1) * out_channels


Q(None, "Dense vs Conv Parameters", "Easy", "Why CNNs exist",
  "For an h × w × c image, compare a dense layer with `units` outputs against a 3 × 3 conv layer with the same number of filters. Return (dense params, conv params).",
  [((224, 224, 3, 64), (9633856, 1792)), ((32, 32, 3, 16), (49168, 448))],
  ("Multiply the sizes step by step.", "O(1)", "O(1)"),
  ("One formula each.", "O(1)", "O(1)"),
  names=["h", "w", "c", "units"])


@B
def dense_vs_conv(h, w, c, units):
    inputs = h * w * c
    dense_weights = inputs * units
    dense_total = dense_weights + units
    filter_weights = 3 * 3 * c
    conv_total = (filter_weights + 1) * units
    return (dense_total, conv_total)


@O
def dense_vs_conv(h, w, c, units):
    return ((h * w * c + 1) * units, (9 * c + 1) * units)


Q(None, "Operations in a Conv Layer", "Medium", "Parameters aren't cost",
  "Return the multiplications for one image: k·k·in·out·H·W, where H × W is the output size (no bias).",
  [((3, 3, 64, 222, 222), 85162752), ((3, 64, 128, 110, 110), 892108800)],
  ("Count one output position's work, then multiply up.", "O(1)", "O(1)"),
  ("<code>np.prod</code> of all the factors.", "O(1)", "O(1)"),
  names=["k", "c_in", "c_out", "H", "W"])


@B
def conv_ops(k, c_in, c_out, H, W):
    per_filter_position = k * k * c_in
    per_position = per_filter_position * c_out
    return per_position * H * W


@O
def conv_ops(k, c_in, c_out, H, W):
    return int(np.prod([k, k, c_in, c_out, H, W], dtype=np.int64))


Q(None, "Receptive Field", "Medium", "How much each output sees",
  "Layers are (kernel, stride) pairs. Return the size of the input region seen by one output of the last layer.",
  [(([(3, 1), (3, 1), (3, 1)],), 7), (([(3, 1), (2, 2), (3, 1), (2, 2), (3, 1)],), 18)],
  ("r ← r + (k − 1)·jump, then jump ← jump·s, in a loop.", "O(L)", "O(1)"),
  ("Vectorised: <code>1 + Σ (k−1)·Π(previous strides)</code> with <code>np.cumprod</code>.", "O(L)", "O(L)"))


@B
def receptive_field(layers):
    r, jump = 1, 1
    for k, s in layers:
        r += (k - 1) * jump
        jump *= s
    return r


@O
def receptive_field(layers):
    a = np.array(layers)
    jumps = np.r_[1, np.cumprod(a[:, 1])[:-1]]
    return int(1 + ((a[:, 0] - 1) * jumps).sum())


Q(None, "Shape Through a Network", "Medium", "Track sizes before coding",
  "Start at size n. Each layer is (k, s, p). Return the size after each layer.",
  [((32, [(3, 1, 1), (2, 2, 0), (3, 1, 1), (2, 2, 0)]), [32, 16, 16, 8]), ((224, [(7, 2, 3), (3, 2, 1)]), [112, 56])],
  ("Count the positions layer by layer.", "O(L·n)", "O(L)"),
  ("The formula in a loop.", "O(L)", "O(L)"),
  names=["n", "layers"])


@B
def sizes_through(n, layers):
    out = []
    for k, s, p in layers:
        total, start, count = n + 2 * p, 0, 0
        while start + k <= total:
            count += 1
            start += s
        n = count
        out.append(n)
    return out


@O
def sizes_through(n, layers):
    out = []
    for k, s, p in layers:
        n = (n + 2 * p - k) // s + 1
        out.append(n)
    return out


Q(None, "Flatten Size for the Classifier", "Easy", "The number everyone gets wrong",
  "After convolutions the tensor has (channels, h, w). Return the input size for the first dense layer.",
  [((64, 8, 8), 4096), ((512, 7, 7), 25088)],
  ("Multiply the three sizes.", "O(1)", "O(1)"),
  ("<code>np.prod</code>.", "O(1)", "O(1)"),
  names=["channels", "h", "w"])


@B
def flatten_size(channels, h, w):
    return channels * h * w


@O
def flatten_size(channels, h, w):
    return int(np.prod([channels, h, w]))


Q(None, "Convolution Across Channels", "Hard", "One filter sees all colours",
  "Input is (channels, h, w) and the filter is (channels, k, k). Return the single output map: the sum across channels of each channel's convolution.",
  [(([[[1, 2], [3, 4]], [[0, 1], [1, 0]]], [[[1]], [[10]]]), [[1, 12], [13, 4]]), (([[[1, 2, 0], [3, 4, 1]], [[0, 1, 1], [1, 0, 2]]], [[[1, -1]], [[2, 0]]]), [[-1, 4], [1, 3]])],
  ("Convolve each channel separately and add the maps.", "O(c·h·w·k²)", "O(h·w)"),
  ("Windows over the height and width axes, then a sum over channels and kernel axes.", "O(c·h·w·k²)", "O(c·h·w)"),
  names=["x", "kernel"])


@B
def conv_channels(x, kernel):
    total = None
    for channel, k in zip(x, kernel):
        part = conv2d_loops(channel, k)
        if total is None:
            total = part
        else:
            total = [[a + b for a, b in zip(r1, r2)] for r1, r2 in zip(total, part)]
    return total


@O
def conv_channels(x, kernel):
    x, kernel = np.array(x), np.array(kernel)
    windows = sliding_window_view(x, kernel.shape[1:], axis=(1, 2))
    return (windows * kernel[:, None, None]).sum(axis=(0, 3, 4))


Q(None, "1×1 Convolution", "Medium", "Mix channels, keep the size",
  "x is (channels, h, w). W has one row per output channel and one column per input channel. Return the mixed result.",
  [(([[[1, 2]], [[3, 4]]], [[1, 1], [1, -1]]), [[[4, 6]], [[-2, -2]]])],
  ("Loop over each pixel position, mixing channel values.", "O(h·w·c²)", "O(h·w·c)"),
  ("<code>np.tensordot(W, x, axes=1)</code>.", "O(h·w·c²)", "O(h·w·c)"),
  names=["x", "W"])


@B
def conv_1x1(x, W):
    c_in, h, w = len(x), len(x[0]), len(x[0][0])
    out = []
    for row in W:
        channel = []
        for i in range(h):
            channel.append([sum(row[c] * x[c][i][j] for c in range(c_in)) for j in range(w)])
        out.append(channel)
    return out


@O
def conv_1x1(x, W):
    return np.tensordot(np.array(W), np.array(x), axes=1)


Q(None, "Normalise Image Channels", "Easy", "Mean and std per colour",
  "x is (channels, h, w). Subtract each channel's given mean and divide by its std. Round to 4 decimals.",
  [(([[[0.5, 1.0]], [[0.0, 0.5]]], [0.5, 0.25], [0.5, 0.25]), [[[0.0, 1.0]], [[-1.0, 1.0]]])],
  ("Three loops.", "O(c·h·w)", "O(c·h·w)"),
  ("Broadcast with <code>mean[:, None, None]</code>.", "O(c·h·w)", "O(c·h·w)"),
  names=["x", "mean", "std"])


@B
def normalise_channels(x, mean, std):
    return [[[round((v - m) / s, 4) + 0.0 for v in row] for row in channel] for channel, m, s in zip(x, mean, std)]


@O
def normalise_channels(x, mean, std):
    x, mean, std = np.array(x), np.array(mean), np.array(std)
    return ((x - mean[:, None, None]) / std[:, None, None]).round(4) + 0.0


Q(None, "Flip Augmentation", "Easy", "More data for free",
  "Flip each row of the image left to right.",
  [(([[1, 2, 3], [4, 5, 6]],), [[3, 2, 1], [6, 5, 4]])],
  ("Reverse each row.", "O(h·w)", "O(h·w)"),
  ("<code>np.fliplr</code>.", "O(h·w)", "O(1) view"))


@B
def flip(img):
    return [row[::-1] for row in img]


@O
def flip(img):
    return np.fliplr(np.array(img))


Q(None, "A Residual Block", "Medium", "Output = x + F(x)",
  "Given x and matrices W1, W2, return x + ReLU(x·W1)·W2, rounded to 4 decimals.",
  [(([[1.0, 2.0]], [[1.0, 0.0], [0.0, 1.0]], [[0.5, 0.0], [0.0, 0.5]]), [[1.5, 3.0]]), (([[1.0, 2.0]], [[0.0, 0.0], [0.0, 0.0]], [[1.0, 1.0], [1.0, 1.0]]), [[1.0, 2.0]])],
  ("Loops for each matrix product.", "O(d²)", "O(d)"),
  ("<code>x + np.maximum(0, x @ W1) @ W2</code>.", "O(d²)", "O(d)"),
  names=["x", "W1", "W2"])


@B
def residual(x, W1, W2):
    out = []
    for row in x:
        h = [max(0.0, sum(row[i] * W1[i][j] for i in range(len(row)))) for j in range(len(W1[0]))]
        f = [sum(h[i] * W2[i][j] for i in range(len(h))) for j in range(len(W2[0]))]
        out.append([round(a + b, 4) for a, b in zip(row, f)])
    return out


@O
def residual(x, W1, W2):
    x = np.array(x)
    return (x + np.maximum(0, x @ np.array(W1)) @ np.array(W2)).round(4)
