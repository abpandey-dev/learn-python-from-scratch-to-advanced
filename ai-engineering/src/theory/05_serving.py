from lib import *

THEORY("Key serving metrics", """
<table>
<tr><th>Metric</th><th>Meaning</th><th>Driven by</th></tr>
<tr><td>TTFT</td><td>time to first token</td><td>queueing + prefill (prompt length)</td></tr>
<tr><td>TPOT / ITL</td><td>time per output token</td><td>decode speed, batch size</td></tr>
<tr><td>Throughput</td><td>total tokens/s across users</td><td>batching, GPU memory, quantisation</td></tr>
<tr><td>Goodput</td><td>requests/s that meet the latency target</td><td>everything above</td></tr>
<tr><td>Cost per 1M tokens</td><td>GPU cost ÷ tokens produced</td><td>throughput and utilisation</td></tr>
</table>
""")

THEORY("Why decode is memory-bound", """
<p>Generating one token for one sequence needs every weight read from GPU memory once, but does relatively little arithmetic with it. Memory bandwidth, not compute, is the limit. Batching reuses each weight read for many sequences, which is why it raises throughput so much, and why smaller (quantised) weights speed decode up.</p>
""")

FAQ("What is the KV cache?", "<p>Stored key and value vectors for all previous tokens in every layer, so each new token only computes its own. It trades memory for speed and grows with context length and batch size.</p>")
FAQ("Continuous vs static batching?", "<p>Static batching runs a fixed group until its longest sequence finishes. Continuous batching adds new requests as soon as any sequence finishes, keeping the GPU full and raising throughput.</p>")
FAQ("How does speculative decoding keep the same output?", "<p>The big model verifies the draft's tokens and only accepts those it would have produced itself (or, with sampling, accepts them with a probability that preserves its distribution), so quality is unchanged while several tokens can be emitted per big-model step.</p>")
FAQ("What does quantisation cost you?", "<p>Some accuracy, especially at 4 bits or below and on reasoning-heavy tasks. Measure on your own evaluation set; per-group methods like GPTQ and AWQ keep the loss small.</p>")
FAQ("When does self-hosting beat an API?", "<p>At high, steady volume where fixed GPU and engineering costs spread over many tokens, or when data residency, latency control, offline use or a custom fine-tuned model require it.</p>")
FAQ("What is PagedAttention?", "<p>Managing the KV cache in fixed-size blocks allocated on demand (like virtual memory pages), avoiding the waste of reserving maximum length per sequence and enabling prefix sharing.</p>")
