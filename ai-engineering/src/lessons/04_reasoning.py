from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LESSON("Basics", "What a reasoning model does differently", """
<p>A <b>reasoning</b> (or "thinking") model writes out a chain of working before its final answer — trying approaches, checking steps, backtracking. Spending more computation at answer time (<b>test-time compute</b>) makes it much better at maths, code, planning and tricky multi-step questions.</p>
<p>The trade-offs:</p>
<ul>
<li><b>Cost</b>: thinking tokens are billed as output tokens, often many thousands per answer.</li>
<li><b>Latency</b>: the user waits while it thinks — stream the response, or use thinking only where it helps.</li>
<li><b>No gain on easy tasks</b>: lookups, classification and simple rewrites don't need it.</li>
</ul>
<pre><code class="py">reply = client.messages.create(
    model="claude-opus-5-5", max_tokens=16000,
    thinking={"type": "adaptive"},              # the model decides how much to think
    messages=[{"role": "user", "content": problem}])
answer = "".join(b.text for b in reply.content if b.type == "text")</code></pre>
<p>APIs differ in the controls they offer (adaptive thinking, effort levels, explicit budgets on older models) — check your model's docs. The thinking comes back as separate blocks you can log for debugging.</p>
""", practice=["What Does Thinking Cost?", "How Long Will the User Wait?", "Separate Thinking From the Answer"])

LESSON("Core", "Choosing how much to think", """
<p>Treat thinking effort like any other hyper-parameter: <b>measure accuracy and cost on your own evaluation set</b> at each level and pick the cheapest that meets the bar. Returns diminish: going from no thinking to a little often helps a lot; going from a lot to the maximum rarely does.</p>
<p>Even better, <b>route</b>: send easy questions to a fast model and hard ones to a reasoning model. A small classifier (or the fast model itself) can estimate difficulty. Compare options by <b>correct answers per dollar</b>, not accuracy alone.</p>
""", practice=["Choose the Effort Level", "Route Easy and Hard Questions", "Accuracy Per Dollar", "Does More Thinking Pay Off?", "Stop Thinking at the Budget"])

LESSON("Core", "Sampling more: self-consistency and best-of-N", """
<p>You can also spend test-time compute by <b>asking several times</b>:</p>
<ul>
<li><b>Self-consistency</b>: sample n answers and take the majority. If each is right with probability p &gt; 0.5, the majority is right more often than any single answer — and it improves with n. If p &lt; 0.5, voting makes things <i>worse</i>.</li>
<li><b>Best-of-N</b>: sample n and let a <b>verifier</b> pick (unit tests for code, a calculator for maths, a reward model). With a perfect verifier you only need one correct sample.</li>
</ul>
<p>Normalise free-form answers before voting, and use agreement as a confidence signal: if samples disagree, abstain or escalate. Cache the shared prompt so n samples don't cost n times the input.</p>
""", practice=["Majority Voting Helps — How Much?", "How Many Samples for Best-of-N?", "Normalise Before You Vote", "Know When to Abstain", "Combine Numeric Estimates", "Sampling Many Times, Cheaply"])


@LD
def voting_curve():
    ns = list(range(1, 26, 2))
    fig, ax = plt.subplots(figsize=(5, 2.6))
    for p in (0.4, 0.6, 0.75):
        acc = [sum(math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n // 2 + 1, n + 1)) for n in ns]
        ax.plot(ns, acc, marker="o", label=f"single-sample accuracy {p}")
    ax.set_xlabel("samples voted"); ax.set_ylabel("majority accuracy"); ax.legend(fontsize=7)


LESSON("Core", "Evaluating reasoning: pass@k and checking the working", """
<p>For code, run the tests: <b>pass@k</b> is the probability that at least one of k samples passes. Estimate it from n ≥ k samples with the unbiased formula 1 − C(n−c, k)/C(n, k), rather than literally taking k samples.</p>
<p>Don't trust the final answer alone. <b>Process</b> checks score each step (a chain is only as strong as its weakest step); <b>outcome</b> checks score only the final answer. Simple tools catch a lot: recompute every arithmetic line, run the code, check units. Ask for answers in a fixed format (<code>Answer: …</code> or <code>&lt;answer&gt;</code> tags) so you can parse them reliably.</p>
""", practice=["Unbiased pass@k", "Find the Final Answer", "Check the Arithmetic in the Working", "Judge the Steps, Not Just the Answer", "Prompt for Reasoning Without a Reasoning Model"])

LESSON("Advanced", "Search over reasoning", """
<p>Beyond voting, systems can <b>search</b>: generate several candidate next steps, score them with a verifier, keep the best few (beam search), and continue — or explore a tree of thoughts. This trades a lot more compute for accuracy on hard problems with a reliable verifier, such as maths proofs or code with tests.</p>
<p>Reasoning models are trained with <b>reinforcement learning on verifiable rewards</b>: problems whose answers can be checked automatically (maths, code), rewarding correct final answers so the model learns useful thinking habits.</p>
""", practice=["Beam Search Over Reasoning Steps"])
