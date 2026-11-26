from lib import *
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LESSON("Basics", "When fine-tuning is the right tool", """
<p>Fine-tuning changes a model's weights with your examples. Try cheaper options first:</p>
<table>
<tr><th>Problem</th><th>Best first tool</th></tr>
<tr><td>Model doesn't know your facts / documents</td><td><b>RAG</b> — facts change; weights shouldn't</td></tr>
<tr><td>Output format or tone is off</td><td><b>Prompting</b> with examples, then fine-tune if you have hundreds+ of examples</td></tr>
<tr><td>A narrow task done millions of times</td><td><b>Fine-tune a small model</b> (often by distilling a big one) for cost and latency</td></tr>
<tr><td>Model should prefer some answers over others</td><td><b>Preference tuning</b> (DPO)</td></tr>
</table>
<p>Fine-tuning teaches <b>behaviour</b> (format, style, a skill), not reliable new <b>knowledge</b>. And always compare against a well-prompted baseline on your eval set.</p>
""", practice=["Prompt, RAG or Fine-Tune?", "What Does a Distillation Dataset Cost?"])

LESSON("Core", "LoRA: train a tiny update instead of the whole model", """
<p>Full fine-tuning updates every weight — billions of numbers, with gradients and optimizer state for each. <b>LoRA</b> (Low-Rank Adaptation) freezes the original weight W and learns a small update as the product of two thin matrices:</p>
<pre><code class="py">h = x @ W + (alpha / r) * (x @ A) @ B      # W: d×k frozen;  A: d×r,  B: r×k trained;  r ≪ d, k</code></pre>
<p>With r = 16 on a 4096×4096 matrix that's 0.8% of the parameters. B starts at zero, so training begins exactly at the original model. After training you can <b>merge</b> A·B into W (no extra serving cost), or keep adapters separate and swap them per customer.</p>
<pre><code class="py">from peft import LoraConfig, get_peft_model
config = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05,
                    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])
model = get_peft_model(base_model, config)
model.print_trainable_parameters()</code></pre>
""", practice=["How Small Is a LoRA Adapter?", "Trainable Share of a Whole Model", "The LoRA Forward Pass", "Merge the Adapter for Serving", "Why B Starts at Zero", "Choose the LoRA Rank"])

LESSON("Core", "Memory: full vs LoRA vs QLoRA", """
<p>Training memory per parameter, roughly: full fine-tuning with Adam needs ~16 bytes (weights, gradients, two optimizer moments, master copy) — about 128 GB for an 8B model before activations. LoRA keeps the frozen weights in bf16 (2 bytes) and pays the 16 bytes only for the small adapter. <b>QLoRA</b> stores the frozen weights in 4 bits (0.5 bytes), which puts 7–8B models on a single consumer GPU or a free Colab GPU.</p>
<pre><code class="py">from transformers import AutoModelForCausalLM, BitsAndBytesConfig
bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype="bfloat16")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-7B-Instruct", quantization_config=bnb)</code></pre>
""", practice=["Will Training Fit on the GPU?"])

LESSON("Core", "Data and training: where results are won", """
<ul>
<li><b>Format</b> every example with the model's own chat template, and compute the loss only on the assistant's tokens.</li>
<li><b>Quality over quantity</b>: a few thousand clean, diverse, correct examples beat a hundred thousand noisy ones. Remove empties, over-long items and duplicates, and make sure no eval prompts leak into training.</li>
<li><b>Packing</b> short examples into full sequences wastes less compute on padding.</li>
<li><b>Hyper-parameters</b>: LoRA learning rates around 1e-4 to 2e-4 with warm-up and cosine decay; a few epochs; watch validation loss and stop early when it rises.</li>
</ul>
<pre><code class="py">from trl import SFTTrainer, SFTConfig
trainer = SFTTrainer(model=model, train_dataset=train, eval_dataset=val, peft_config=config,
                     args=SFTConfig(learning_rate=2e-4, num_train_epochs=2, per_device_train_batch_size=4,
                                    gradient_accumulation_steps=8, lr_scheduler_type="cosine", warmup_ratio=0.05))
trainer.train()</code></pre>
<p>Library arguments change between versions — check the docs for the versions you install.</p>
""", practice=["Apply a Chat Template", "Only Learn From the Assistant's Words", "Pack Short Examples Together", "Clean the Training Set", "Warm-Up Then Cosine", "Batch Size and Steps", "Stop Before It Overfits"])


@LD
def schedule_plot():
    steps = np.arange(0, 1001)
    lr = np.where(steps < 100, 2e-4 * steps / 100, 2e-4 * 0.5 * (1 + np.cos(np.pi * (steps - 100) / 900)))
    fig, ax = plt.subplots(figsize=(5, 2.4))
    ax.plot(steps, lr * 1e6)
    ax.set_xlabel("step"); ax.set_ylabel("learning rate (×1e-6)"); ax.set_title("Warm-up, then cosine decay")


LESSON("Advanced", "Preference tuning with DPO", """
<p>Supervised fine-tuning shows the model good answers. <b>Preference tuning</b> shows pairs — a chosen and a rejected answer to the same prompt — and teaches it to prefer the chosen kind. <b>DPO</b> (Direct Preference Optimisation) does this with a simple classification-style loss, no separate reward model or RL loop:</p>
<pre><code class="py">margin = beta * ((logp_chosen - ref_chosen) - (logp_rejected - ref_rejected))
loss = -log(sigmoid(margin))          # push the margin up, relative to a frozen reference copy</code></pre>
<p>β controls how far the model may drift from the reference. Watch <b>reward accuracy</b> (share of pairs with a positive margin) during training. Build pairs from ratings or A/B judgements, keeping only clear gaps.</p>
<p>After any fine-tune, re-run general benchmarks: narrow training can erode other skills (<b>catastrophic forgetting</b>) and safety behaviour.</p>
""", practice=["The DPO Loss for One Pair", "A Batch of Preference Pairs", "Build Preference Pairs From Ratings", "Did It Forget Everything Else?"])
