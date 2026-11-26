from lib import *
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LESSON("Basics", "How a model sees an image", """
<p>A vision-language model cuts an image into small square <b>patches</b> (e.g. 14×14 pixels), turns each patch into a vector, and feeds those vectors to the transformer alongside text tokens. So an image <b>costs tokens</b> — roughly in proportion to its pixel area (Claude's documented estimate: width × height ÷ 750), and very large images are downscaled first.</p>
<p>Practical rules: resize before sending (saves upload time and tokens), crop to what matters, put images <b>before</b> the question about them, and label several images ("Image 1:", "Image 2:").</p>
<pre><code class="py">import base64
data = base64.b64encode(open("chart.png", "rb").read()).decode()
client.messages.create(model="claude-opus-5-5", max_tokens=500, messages=[{"role": "user", "content": [
    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": data}},
    {"type": "text", "text": "What trend does this chart show?"}]}])</code></pre>
""", practice=["What Does an Image Cost?", "Resize Before Sending", "How Many Patches?", "Build an Image Content Block"])


@LD
def patch_grid():
    img = np.add.outer(np.arange(48), np.arange(48)) % 17
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.imshow(img, cmap="viridis")
    for k in range(0, 49, 12):
        ax.axhline(k - 0.5, color="white"); ax.axvline(k - 0.5, color="white")
    ax.set_title("16 patches of 12×12 pixels → 16 tokens")
    ax.set_xticks([]); ax.set_yticks([])


LESSON("Core", "Inside the pipeline: patches, normalisation, embeddings", """
<p>Before a vision model sees pixels, they're scaled to 0–1 and normalised per channel with the mean and standard deviation the model was trained with. Patches are flattened into vectors and projected to embeddings — the same "everything is a sequence of vectors" idea as text.</p>
<p><b>Image embeddings</b> (CLIP-style models) put images and text into one vector space, so you can search images with text, find similar images, or classify with <b>zero-shot labels</b> ("a photo of a cat" vs "a scanned document") — no training needed.</p>
""", practice=["Cut an Image Into Patch Vectors", "Normalise Pixels", "Find Similar Images", "Zero-Shot Labels, CLIP Style"])

LESSON("Core", "Document AI: PDFs, scans, tables and forms", """
<p>Real business data is PDFs, scans, invoices and slide decks. Two routes, often combined:</p>
<ul>
<li><b>Text route</b>: extract text (PDF text layer or OCR), restore reading order (OCR returns words with positions, not sentences), turn tables into Markdown, chunk with page numbers for citations.</li>
<li><b>Vision route</b>: send the page image (or the whole PDF — Claude accepts PDFs as document blocks) when layout, charts or handwriting matter.</li>
</ul>
<p>Route per page: text for dense prose, images for charts and scans. When a model extracts fields (invoice number, totals), <b>validate them in code</b> — required fields, valid dates, line items that add up — and send failures for review instead of trusting them.</p>
""", practice=["Put OCR Words in Reading Order", "Table Rows to Markdown", "Validate Extracted Invoice Fields", "Text or Image for Each Page?", "Chunk a PDF and Keep Page Numbers"])

LESSON("Core", "Speech: from audio to text and back", """
<p>Audio is a long list of samples (16,000 per second is common for speech). Models analyse it in short overlapping <b>frames</b> (25 ms every 10 ms) turned into spectrogram features. Speech-to-text models (such as the open-source Whisper family, or hosted transcription APIs) accept limited lengths, so long recordings are split into <b>overlapping chunks</b> and stitched back together.</p>
<p>Measure transcription quality with <b>word error rate</b> (the edit distance between word lists divided by the reference length), and produce subtitles with timestamps (SRT/VTT).</p>
""", practice=["Slice Audio Into Frames", "Chunk Long Audio for Transcription", "Word Error Rate", "Write Subtitles"])

LESSON("Advanced", "Voice agents and video", """
<p>A <b>voice agent</b> listens, thinks and speaks. The classic <b>cascade</b> is: voice activity detection (has the user finished?) → speech-to-text → LLM → text-to-speech. <b>Speech-to-speech</b> models do it in one model, with lower latency and more natural prosody. Either way, latency is everything: aim for the first audio within about 800 ms by streaming every stage, using a fast model, and starting text-to-speech on the first sentence. Good turn detection — not cutting people off, not waiting too long — matters as much as model quality.</p>
<p><b>Video</b> is usually handled as sampled frames (images) plus the audio transcript. Sample sparsely to fit the token budget; sample densely only around moments that matter.</p>
""", practice=["A Voice Agent's Latency Budget", "Detect the End of the User's Turn", "How Many Video Frames to Send?"])
