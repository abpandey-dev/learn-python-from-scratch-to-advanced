from lib import *

THEORY("Kinds of fine-tuning", """
<table>
<tr><th>Method</th><th>Data</th><th>Teaches</th></tr>
<tr><td>Continued pre-training</td><td>raw domain text</td><td>domain language (expensive)</td></tr>
<tr><td>SFT (instruction tuning)</td><td>prompt → ideal response</td><td>format, style, task skill</td></tr>
<tr><td>Preference tuning (DPO, RLHF)</td><td>prompt + chosen + rejected</td><td>which answers people prefer</td></tr>
<tr><td>RL with verifiable rewards</td><td>problems with checkable answers</td><td>reasoning on maths / code</td></tr>
<tr><td>Distillation</td><td>teacher model outputs</td><td>a small model imitating a big one</td></tr>
</table>
""")

THEORY("Parameter-efficient methods", """
<ul>
<li><b>LoRA</b>: low-rank update A·B per chosen matrix; rank r and scale α are the key knobs.</li>
<li><b>QLoRA</b>: LoRA on a 4-bit quantised frozen base (NF4), with bf16 compute.</li>
<li>Variants (DoRA, LoRA+, rank-stabilised scaling) tweak the same idea.</li>
<li>Adapters can be merged into W for serving, or hot-swapped per tenant.</li>
</ul>
""")

FAQ("Why does LoRA work with so few parameters?", "<p>The weight changes needed to adapt a pre-trained model to a task have low intrinsic rank, so a product of two thin matrices captures most of the useful update.</p>")
FAQ("Fine-tuning or RAG for company knowledge?", "<p>RAG. Knowledge changes and must be cited and kept current; fine-tuning bakes in behaviour, not reliable, updatable facts. Fine-tune for format, style or skills — sometimes on top of RAG.</p>")
FAQ("What is QLoRA?", "<p>Training LoRA adapters on top of a base model stored in 4-bit precision, cutting memory roughly fourfold so large models can be tuned on one GPU.</p>")
FAQ("Why mask the loss on user tokens?", "<p>So the model learns to produce assistant responses, not to predict or imitate user messages, and so gradients focus on the behaviour you want.</p>")
FAQ("How does DPO differ from RLHF?", "<p>RLHF trains a reward model and optimises the policy with reinforcement learning (e.g. PPO). DPO optimises the policy directly on preference pairs with a closed-form loss relative to a reference model — simpler and more stable.</p>")
FAQ("How do you know a fine-tune helped?", "<p>Compare against a well-prompted baseline on a held-out eval set for the target task, and re-check general and safety benchmarks for regressions.</p>")
