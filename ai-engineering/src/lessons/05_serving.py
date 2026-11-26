from lib import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LESSON("Basics", "API or your own GPUs?", """
<p>Most teams start with a hosted API: no infrastructure, the best models, pay per token. Teams <b>self-host open-weight models</b> (Llama, Qwen, Mistral, Gemma and others) when they need data to stay inside their network, very high volume at low cost per token, a fine-tuned small model, or offline use. Self-hosting means you now own memory, batching, latency and uptime — the subject of this topic.</p>
<table>
<tr><th>Tool</th><th>Used for</th></tr>
<tr><td><b>vLLM</b>, <b>SGLang</b>, TensorRT-LLM</td><td>high-throughput GPU servers with continuous batching</td></tr>
<tr><td><b>llama.cpp</b>, <b>Ollama</b></td><td>laptops and CPUs, quantised models</td></tr>
<tr><td>Hugging Face TGI / Inference Endpoints, cloud model gardens</td><td>managed hosting of open models</td></tr>
</table>
<pre><code class="bash">pip install vllm
vllm serve Qwen/Qwen2.5-7B-Instruct --max-model-len 8192
curl localhost:8000/v1/chat/completions -H "Content-Type: application/json" \\
  -d '{"model": "Qwen/Qwen2.5-7B-Instruct", "messages": [{"role": "user", "content": "Hi"}]}'</code></pre>
""", practice=["Self-Host or Use an API?", "Cost per Million Tokens, Self-Hosted"])

LESSON("Core", "Memory: weights and the KV cache", """
<p>GPU memory holds two big things:</p>
<ul>
<li><b>Weights</b>: parameters × bytes each. An 8B model is 16 GB in bf16, 8 GB in int8, 4 GB in int4.</li>
<li><b>KV cache</b>: while generating, each layer keeps the key and value vectors of every previous token so it doesn't recompute them. Size = 2 × layers × KV heads × head size × bytes × tokens × sequences. It grows with context length <i>and</i> with the number of users, and is usually what limits how many requests a GPU can serve at once.</li>
</ul>
<p>Grouped-query attention (fewer KV heads than query heads) shrinks the KV cache a lot — compare 8 KV heads with 32 in the questions.</p>
""", practice=["Memory for the Weights", "How Big Is the KV Cache?", "How Many Users at Once?", "Longest Context That Fits"])

LESSON("Core", "Batching, prefill and decode", """
<p>Generation has two phases. <b>Prefill</b> reads the whole prompt in parallel — fast per token, and it sets the time to first token. <b>Decode</b> produces one token at a time; each step reads all the weights from memory, so a single sequence leaves the GPU mostly idle.</p>
<p>The fix is <b>batching</b>: decode many sequences per step. <b>Static batching</b> waits for the slowest sequence in a batch before starting the next. <b>Continuous batching</b> (vLLM, SGLang) slots a new request in the moment any sequence finishes, keeping the GPU busy — often several times more throughput.</p>
<p>Bigger batches raise total tokens per second but lower each user's speed; pick the batch size that meets your per-user latency target. Scheduling also matters: short jobs first lowers average waiting time.</p>
""", practice=["Static vs Continuous Batching", "Prefill vs Decode", "Throughput vs Per-User Speed", "Shortest Job First"])


@LD
def batching_chart():
    lengths = [10, 200, 15, 30, 190, 20, 25, 12]
    import heapq
    static, cont = [], []
    for slots in (1, 2, 4, 8):
        static.append(sum(max(lengths[i:i + slots]) for i in range(0, len(lengths), slots)))
        heap = [0] * slots
        for L in lengths:
            heapq.heappush(heap, heapq.heappop(heap) + L)
        cont.append(max(heap))
    fig, ax = plt.subplots(figsize=(5, 2.6))
    ax.plot([1, 2, 4, 8], static, marker="o", label="static batching")
    ax.plot([1, 2, 4, 8], cont, marker="o", label="continuous batching")
    ax.set_xlabel("slots per step"); ax.set_ylabel("steps to finish all"); ax.legend()


LESSON("Core", "Making each token cheaper", """
<ul>
<li><b>Quantisation</b>: store weights in 8 or 4 bits instead of 16. Less memory and faster decode (it's memory-bound), with a small quality loss. Per-group scales handle outlier weights much better than one scale for the whole tensor (methods like GPTQ, AWQ). KV caches can be quantised too.</li>
<li><b>Speculative decoding</b>: a small draft model guesses several tokens; the big model checks them all in one step and keeps the matching prefix. Same output, often 2–3× faster when the draft is usually right.</li>
<li><b>Paged KV memory</b> (PagedAttention): allocate the KV cache in small blocks as sequences grow instead of reserving the maximum length, so far more sequences fit.</li>
<li><b>Prefix caching</b>: share the KV blocks of a common system prompt across requests.</li>
</ul>
""", practice=["Quantise to int8", "Why Group-Wise Scales Help", "Speculative Decoding: Expected Speed-Up", "Verify a Draft", "Paged KV Memory", "Share the System Prompt's Cache"])

LESSON("Advanced", "Running it in production", """
<ul>
<li><b>Capacity</b>: by Little's law, requests in flight = arrival rate × time per request; size the fleet with headroom.</li>
<li><b>Rate limits</b>: a token bucket per customer stops one user starving the rest.</li>
<li><b>Fallbacks</b>: if the main model errors or times out, retry on a secondary model or provider.</li>
<li><b>Multi-tenant fine-tunes</b>: serve one base model with many small LoRA adapters instead of one full copy per customer.</li>
<li><b>Measure</b>: time to first token, tokens per second per user, total throughput, GPU utilisation and cost per million tokens.</li>
</ul>
""", practice=["How Many GPUs for the Traffic?", "A Token Bucket Rate Limiter", "Fall Back When a Model Fails", "Many Fine-Tunes on One GPU"])
