from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np



LESSON("Basics", "The framework: how to answer any design question", """
<p>"Design a recommendation system" feels impossible because it's open-ended. There's no single right answer. The interviewer is judging how you structure the problem and weigh trade-offs. Use the same seven steps every time, and say them aloud.</p>
<table><tr><th>Step</th><th>Questions to ask</th></tr>
<tr><td>1. Clarify</td><td>Who's it for? What scale? How fast? What's out of scope?</td></tr>
<tr><td>2. Frame</td><td>What's the business metric? What's the ML task? Is ML even needed?</td></tr>
<tr><td>3. Data</td><td>What's the label? What features? Is anything leaking from the future?</td></tr>
<tr><td>4. Model</td><td>What's the baseline? When is a more complex one worth it?</td></tr>
<tr><td>5. Evaluate</td><td>Which offline metrics? Which online experiment?</td></tr>
<tr><td>6. Serve</td><td>Batch or real time? Latency and cost? What if the model fails?</td></tr>
<tr><td>7. Monitor</td><td>Drift, quality, retraining, feedback loops?</td></tr></table>
<p><b>Spend your time roughly like this</b> in 45 minutes: 5 clarifying, 5 framing, 10 on data, 10 on the model, 5 on evaluation, 5 on serving, and 5 on monitoring.</p>
<p><b>Common mistakes:</b></p>
<ul><li>Jumping straight to "I'd use a transformer".</li>
<li>Skipping labels, even though the hardest part of a real system is often the data.</li>
<li>Reporting only offline metrics, with no plan for an A/B test.</li>
<li>Never mentioning a simple baseline, or what happens when the model is down.</li>
<li>Going silent. Say what you're thinking, including trade-offs you rejected.</li></ul>
""", practice=["Spot Feature Leakage", "Split by Time"])


LESSON("Core", "Back-of-the-envelope sizing", """
<p>Rough numbers guide design, so practice doing them quickly. Round freely, and <b>state your assumptions</b>.</p>
<p><b>Traffic.</b> 10 million daily users × 20 requests = 200 million per day. A day has about 86,400 seconds, so about <b>2,300 QPS</b> on average. At a peak of 3×, about 6,900 QPS.</p>
<p><b>Servers.</b> If one handles 100 QPS and you run at 70% utilisation, then 3,000 peak QPS needs 3000 / 70 ≈ 43, plus 2 spare = <b>45</b>.</p>
<p><b>Memory for embeddings.</b> 100 million items × 768 dimensions × 4 bytes × 2 replicas = <b>614 GB</b>. That's a real constraint, and it points toward approximate indexes, compression or sharding.</p>
<p><b>Latency budget.</b> For a 100 ms limit:</p>
<table><tr><th>Step</th><th>ms</th></tr>
<tr><td>Network and request handling</td><td>5</td></tr>
<tr><td>Fetch features, in parallel (10, 30, 20): the slowest counts</td><td>30</td></tr>
<tr><td>Model inference</td><td>40</td></tr>
<tr><td>Response</td><td>5</td></tr>
<tr><td><b>Total</b></td><td><b>80 ✓</b></td></tr></table>
<p><b>A cache reduces load:</b> 1,000 QPS with an 80% hit rate means the model sees only 200 QPS.</p>
<p><b>Useful numbers:</b> a day is about 10⁵ seconds. A memory read takes nanoseconds, a network hop within a data centre takes about a millisecond or less, and a cross-continent trip takes about 100 ms.</p>
""", practice=["Requests per Second", "How Many Servers?", "Embedding Storage", "Latency Budget", "Cache Effect on Traffic"])


LESSON("Core", "Data: where systems actually go wrong", """
<p><b>Labels.</b> Ask how you know the right answer. Clicks are plentiful but noisy, and purchases are rarer but stronger. Fraud labels may arrive 60 days later, as chargebacks, so very recent data looks falsely clean.</p>
<p><b>Leakage</b> means using information that won't exist at prediction time. A warning sign is a model that's suspiciously excellent:</p>
<ul><li><code>refund_issued</code> predicting fraud: it happens because of the fraud, after the fact.</li>
<li>Random splits for time-based data: tomorrow's rows train the model that "predicts" yesterday's.</li>
<li>Target encoding computed on all rows, including the current label.</li></ul>
<p>The defence is <b>split by time</b>, and to compute each feature <b>as of</b> the prediction moment. For categories a, a, b, a with labels 1, 0, 1, 1 and prior 0.5, safe target encoding gives 0.5, 1.0, 0.5, 0.5. Each row sees only earlier rows.</p>
<p><b>Training-serving skew.</b> A feature computed one way in a nightly batch job and differently in the live service. It's silent, since nothing crashes, and accuracy just falls. Compare the same rows from both paths. A <b>feature store</b> helps by defining each feature once.</p>
<p><b>Imbalance.</b> With 0.1% fraud, you might keep all positives and just 10% of negatives. Training becomes faster, but probabilities are now inflated, so correct them: p / (p + (1 − p)/w). A prediction of 0.5 with w = 0.1 is really <b>0.091</b>. Without this, any downstream decision based on the probability will be wrong.</p>
<p><b>High-cardinality categories,</b> such as millions of user IDs: use embeddings, or feature hashing into a fixed number of buckets. Collisions will happen: "ab", "ba" and "c" all land in one bucket with our simple hash. Fixed memory is what you get in exchange.</p>
""", practice=["Training vs Serving Skew", "Target Encoding Without Leakage", "Correct for Negative Downsampling", "Feature Hashing"])


LESSON("Core", "From model score to business decision", """
<p>A score isn't a decision. Connect it to money.</p>
<p><b>Choose a threshold by cost.</b> If a false positive costs 1 (annoying a customer) and a false negative costs 10 (missed fraud), a threshold of 0.5 isn't special. Scores 0.9, 0.7, 0.4, 0.2 with labels 1, 0, 1, 0:</p>
<table><tr><th>Threshold</th><th>False positives</th><th>False negatives</th><th>Cost</th></tr>
<tr><td>0.3</td><td>1</td><td>0</td><td><b>1</b></td></tr>
<tr><td>0.5</td><td>1</td><td>1</td><td>11</td></tr>
<tr><td>0.8</td><td>0</td><td>1</td><td>10</td></tr></table>
<p>The chart shows this on a larger simulated data set.</p>
<p><b>Calibration:</b> when the model says 90%, is it right 90% of the time? A model predicting 0.9 for all rows when only 25% are positive has a calibration error of <b>0.65</b>, however well it ranks. Calibration matters when the probability itself is used, as in pricing or expected value. It doesn't matter if you only sort.</p>
<p><b>Limited capacity.</b> If reviewers can check only 100 cases a day, precision in the top 100 is what counts. <b>Lift</b> compares that with random: top-2 precision of 1.0 on a base rate of 0.4 gives lift 2.5.</p>
<table><tr><th>Offline metric</th><th>Good for</th></tr>
<tr><td>PR-AUC</td><td>rare positives</td></tr><tr><td>ROC-AUC</td><td>balanced ranking quality</td></tr>
<tr><td>Log-loss, calibration</td><td>when probabilities matter</td></tr><tr><td>nDCG, recall@k</td><td>ranking and retrieval</td></tr></table>
<p>Offline metrics only suggest a model is better. Business value is decided online, by an experiment.</p>
""", practice=["Pick a Threshold by Cost", "Expected Calibration Error", "Lift at the Top"])


@LD
def cost_curve():
    rng = np.random.default_rng(0)
    y = rng.binomial(1, 0.1, 5000)
    score = np.clip(rng.normal(0.25 + 0.4 * y, 0.15), 0, 1)
    thresholds = np.linspace(0.05, 0.95, 37)
    cost = [1 * ((score >= t) & (y == 0)).sum() + 10 * ((score < t) & (y == 1)).sum() for t in thresholds]
    best = thresholds[int(np.argmin(cost))]
    print("cheapest threshold:", round(float(best), 3))
    fig, ax = plt.subplots(figsize=(4.6, 2.7))
    ax.plot(thresholds, cost)
    ax.axvline(best, color="black", linestyle="--", label="cheapest")
    ax.axvline(0.5, color="gray", linestyle=":", label="the default 0.5")
    ax.set_xlabel("threshold")
    ax.set_ylabel("total cost")
    ax.legend(fontsize=7)


LESSON("Core", "Walkthrough: design a recommender", """
<p><b>Clarify.</b> A video app, 10 million daily users, 10 million videos, a page within 100 ms. The goal is long-term watch time, not just clicks, since clicks reward clickbait.</p>
<p><b>The key idea is a two-stage funnel,</b> because scoring 10 million items per request with a heavy model isn't possible.</p>
<table><tr><th>Stage</th><th>Items</th><th>Model</th><th>Goal</th></tr>
<tr><td>Candidate generation</td><td>10M → 500</td><td>two-tower embeddings + ANN search, plus popular and recent</td><td>high recall, fast</td></tr>
<tr><td>Ranking</td><td>500 → 50</td><td>gradient boosting or deep network, with rich features</td><td>accurate ordering</td></tr>
<tr><td>Re-ranking</td><td>50 → 10</td><td>rules</td><td>diversity, freshness, policy</td></tr></table>
<p><b>Data.</b> Labels from watch time, likes and skips. Features: user history, video info, and context such as device and time. Split by time.</p>
<p><b>Traps to raise:</b></p>
<ul><li><b>Cold start:</b> new users get popular and regional items. New videos use content embeddings and limited exploration.</li>
<li><b>Position bias:</b> top items get clicked because they're on top. An item with 2% CTR at a position seen 25% of the time really has an 8% rate, higher than a 5% item at the top.</li>
<li><b>Feedback loop:</b> you train only on what you showed. Reserve some traffic for exploration.</li></ul>
<p><b>Evaluate.</b> Offline: recall@k for retrieval, and nDCG for ranking. Online: an A/B test on watch time and retention, with guardrails such as latency and complaints.</p>
<p><b>Serve.</b> Pre-compute item embeddings in batches; compute the user embedding live. If a model fails, fall back to a popular list.</p>
""", practice=["Recommendation: Two-Stage Funnel", "Position Bias Correction"])


LESSON("Core", "Walkthrough: design fraud detection", """
<p><b>Clarify.</b> Card payments: decide within 100 ms, with fraud at about 0.1%, and blocking a good customer is costly.</p>
<p><b>Frame.</b> Binary classification, with three outcomes rather than two: allow, block, or send for manual review. Thresholds come from costs and from reviewer capacity.</p>
<p><b>Data.</b></p>
<ul><li><b>Labels are delayed:</b> chargebacks can take 60 days, so the newest data isn't reliable yet.</li>
<li><b>Features:</b> velocity (cards used in the last hour), distance from the usual location, merchant history, and device signals. These must be computed as of the transaction time, typically by a streaming system.</li>
<li><b>Imbalance:</b> accuracy is useless, since always saying "not fraud" gets 99.9%. Use PR-AUC and precision at a fixed review capacity.</li></ul>
<p><b>Model.</b> Start with rules plus logistic regression as a baseline. Gradient boosting usually does well on tabular features. Keep rules for immediate response to a new attack.</p>
<p><b>The special challenge is adversaries.</b> Fraudsters adapt, so performance decays. Monitor drift, retrain often, and analyse what's new. You also get no label on transactions you blocked, so let a small random sample through under controlled limits to keep an unbiased view.</p>
<p><b>Serve.</b> Real time, with strict latency. If the model times out, fall back to rules. Log the features as they were seen, to prevent training-serving skew. Keep explanations available for reviewers and regulators.</p>
""", practice=["Batch or Real Time?"])


LESSON("Core", "Walkthrough: design an LLM support assistant", """
<p><b>Clarify.</b> It answers customer questions from 50,000 help articles, and hands off to a person when unsure. Goals: resolve more tickets without wrong answers.</p>
<p><b>Architecture:</b></p>
<table><tr><th>Stage</th><th>Choice</th><th>Why</th></tr>
<tr><td>Ingest</td><td>chunk by section, with titles</td><td>keep chunks self-contained</td></tr>
<tr><td>Retrieve</td><td>hybrid BM25 + vectors, filtered by product and permissions</td><td>catches both error codes and paraphrases</td></tr>
<tr><td>Re-rank</td><td>keep the top 5</td><td>accuracy, and fewer tokens</td></tr>
<tr><td>Generate</td><td>answer only from sources, with citations</td><td>reduces invented answers, and lets you check</td></tr>
<tr><td>Act</td><td>tools such as order lookup, with checks in code</td><td>live data; risky actions need approval</td></tr>
<tr><td>Escalate</td><td>low retrieval score or user request → a person</td><td>the safe failure</td></tr></table>
<p><b>Budget.</b> With an 8,000-token window, 500 for the system prompt, 100 for the question and 1,000 for the answer, there's room for (8000 − 1600) / 400 = <b>16</b> chunks of 400 tokens. In practice use fewer, as it's cheaper and often no worse.</p>
<p><b>Evaluate, in layers.</b> Retrieval recall on questions with known articles. Answer faithfulness to sources, judged by people or an LLM rubric. Then in production, resolution rate, escalations and customer satisfaction.</p>
<p><b>Risks to raise:</b> prompt injection through retrieved text or user messages; leaking data between customers, so filter at retrieval; stale documents; cost and latency, which caching helps; and model upgrades, which need your eval suite to pass first.</p>
<p><b>Common follow-up: fine-tune or RAG?</b> Facts change, so use RAG. Fine-tuning suits style or format, and it's rarely the first step.</p>
""", practice=["RAG Assistant Budget"])


LESSON("Advanced", "Launching and keeping it healthy", """
<p><b>Roll out in stages:</b></p>
<table><tr><th>Stage</th><th>What happens</th><th>Risk</th></tr>
<tr><td>Shadow</td><td>new model runs and logs, but users see the old one</td><td>none for users</td></tr>
<tr><td>Canary</td><td>a small share of traffic</td><td>small</td></tr>
<tr><td>A/B test</td><td>a controlled comparison</td><td>measured</td></tr>
<tr><td>Full rollout</td><td>everyone, keeping an easy rollback</td><td>reversible</td></tr></table>
<p><b>Automate the canary decision.</b> CTR rose 4%, which is good. But p95 latency went from 100 to 130 ms, 30% worse against a 10% limit. So <b>roll back</b>, however good the model looks.</p>
<p><b>Batch or real time?</b></p>
<table><tr><th></th><th>Batch</th><th>Real time</th></tr>
<tr><td>Freshness</td><td>hours old</td><td>immediate</td></tr>
<tr><td>Cost</td><td>often lower at high volume</td><td>pay per request; needs spare capacity</td></tr>
<tr><td>Failure</td><td>serve yesterday's results</td><td>needs a fallback</td></tr>
<tr><td>Fits</td><td>daily recommendations, churn lists</td><td>fraud, search, chat</td></tr></table>
<p>Example: 4 runs at 50 costs 200 a day; a million calls at 0.001 costs 1,000. Batch wins, unless the use case needs fresh results.</p>
<p><b>Monitor at three levels:</b> system (latency, errors), data (missing values, drift), and model (quality, often delayed by slow labels).</p>
<p><b>Retrain on evidence,</b> not out of habit: a drift score above a limit, quality falling more than 5% below baseline, or a model older than your limit. Then validate the new model against the old one before promoting it.</p>
""", practice=["Canary Decision", "When to Retrain"])
