from lib import *

THEORY("Modalities at a glance", """
<table>
<tr><th>Input</th><th>Becomes</th><th>Watch out for</th></tr>
<tr><td>Image</td><td>patch embeddings (tokens ∝ pixels)</td><td>cost of big images; tiny text in screenshots</td></tr>
<tr><td>PDF / scan</td><td>text layer, OCR, or page images</td><td>reading order, tables, handwriting</td></tr>
<tr><td>Audio</td><td>frames → spectrogram → tokens or text</td><td>chunk boundaries, accents, noise, latency</td></tr>
<tr><td>Video</td><td>sampled frames + transcript</td><td>token budget, missing fast events</td></tr>
</table>
""")

THEORY("Architectures", """
<ul>
<li><b>Vision encoder + LLM</b>: a ViT turns images into embeddings that are projected into the LLM's token space.</li>
<li><b>Contrastive (CLIP-style)</b>: separate image and text encoders trained so matching pairs have similar embeddings — great for search and zero-shot labels.</li>
<li><b>Speech</b>: encoder–decoder transcription models; speech-to-speech models handle audio end to end.</li>
</ul>
""")

FAQ("How are images turned into tokens?", "<p>The image is resized and split into fixed-size patches; each patch is flattened and projected to an embedding, and those embeddings join the text tokens in the transformer. More pixels means more patches and more tokens.</p>")
FAQ("How would you build a system that answers questions over scanned invoices?", "<p>Classify pages, extract with OCR plus layout or send page images to a vision model, extract fields into a schema, validate them in code (totals, dates, required fields), route failures to humans, and index text chunks with page numbers for retrieval and citations.</p>")
FAQ("What is word error rate?", "<p>The minimum number of word substitutions, deletions and insertions to turn the transcript into the reference, divided by the number of reference words.</p>")
FAQ("Cascade vs speech-to-speech voice agents?", "<p>Cascades (STT → LLM → TTS) are modular, debuggable and can use any LLM; speech-to-speech models have lower latency and more natural speech but are less controllable. Many products use cascades with aggressive streaming.</p>")
FAQ("What is zero-shot image classification?", "<p>Embedding the image and a text description of each label in a shared space and choosing the label whose text is most similar — no labelled training images needed.</p>")
FAQ("Why validate what a vision model extracted?", "<p>Extraction can misread digits or invent fields. Cheap code checks (sums, formats, required fields) catch many errors before they reach accounting systems.</p>")
