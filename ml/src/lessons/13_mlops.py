from lib import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

LESSON("Basics", "Why most models never reach production", """
<p>A model in a notebook is a prototype. A model in production has to be <b>reproducible</b> (rebuild exactly the same one), <b>deployable</b> (answer requests in milliseconds or score millions of rows overnight), <b>monitored</b> (notice when it gets worse) and <b>maintainable</b> (retrain and roll back safely). <b>MLOps</b> is the set of practices that does this — DevOps plus data and models.</p>
<pre><code class="text">data → validate → features → train → evaluate → register → deploy → monitor
  ↑                                                                    │
  └──────────────── retrain when drift or decay is detected ───────────┘</code></pre>
<p>Tools you'll meet: <b>MLflow</b> or Weights &amp; Biases (tracking, registry), <b>DVC</b> (data versions), <b>Great Expectations</b> (data checks), <b>FastAPI</b> (serving), <b>Docker</b> and <b>Kubernetes</b> (packaging, scaling), <b>Airflow</b> (scheduling), <b>Evidently</b> and <b>Grafana</b> (monitoring), and managed platforms such as SageMaker and Vertex AI. They run on servers, so here every idea is practised in plain Python you can run in the browser.</p>
""", practice=["Pick the Best Run"])

LESSON("Core", "Reproducibility: tracking, registry, versions", """
<ul>
<li><b>Experiment tracking</b>: log every run's parameters, metrics, code version (git commit), data version and the model file. Then "which settings gave 0.903?" has an answer.
<pre><code class="py">with mlflow.start_run():
    mlflow.log_params({"depth": 3}); mlflow.log_metric("val_auc", 0.903)
    mlflow.sklearn.log_model(pipeline, "model")</code></pre></li>
<li><b>Data versioning</b>: store a fingerprint (hash) or a DVC version of the exact training data.</li>
<li><b>Model registry</b>: numbered versions with stages (Staging → Production → Archived). Promotion is a deliberate, recorded step, and rollback means pointing Production at the previous version.</li>
<li><b>Semantic versions</b> tell consumers what changed: a new input schema breaks callers (major), a retrain doesn't (minor).</li>
</ul>
""", practice=["Pick the Best Run", "Promote a Model Version", "Same Data, Different Order?", "Bump the Model Version"])

LESSON("Core", "Gates before training and before deploying", """
<p>Bad data silently makes bad models. Put a <b>data quality gate</b> before training: required columns present, null rates under limits, values in valid ranges, row counts plausible. If it fails, stop the pipeline and alert — don't train.</p>
<p>Before deploying, run <b>model CI</b> like software tests:</p>
<ul>
<li>Metric thresholds on a fixed test set (and per important segment).</li>
<li><b>Invariance tests</b>: changing something irrelevant (a name) must not change the prediction.</li>
<li><b>Directional tests</b>: raising income shouldn't lower a credit score.</li>
<li>Latency and memory budgets.</li>
</ul>
""", practice=["Data Quality Gate", "Pre-Deployment Checks"])

LESSON("Core", "Serving: batch, real-time, and the training–serving gap", """
<p><b>Batch</b> scoring runs on a schedule over many rows (nightly churn scores) — simple and cheap; process in chunks to fit in memory. <b>Real-time</b> serving answers one request at a time behind an API:</p>
<pre><code class="py">from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()
model = joblib.load("model.joblib")          # the whole pipeline: preprocessing + model

class Applicant(BaseModel):
    age: int
    income: float

@app.post("/predict")
def predict(a: Applicant):
    return {"score": float(model.predict_proba([[a.age, a.income]])[0, 1])}</code></pre>
<p>Pydantic validates every request (types, ranges) before it reaches the model. A <b>Dockerfile</b> installs pinned libraries and copies the code and model, so the same image runs on a laptop and in the cloud.</p>
<p>The classic production bug is <b>training–serving skew</b>: features computed one way in the training pipeline and another way in the serving code. Fixes: save preprocessing <i>inside</i> the model pipeline (a fitted scaler, never re-fitted on live data), share feature code, and build training sets with <b>point-in-time joins</b> so each label only sees feature values that existed at that moment.</p>
""", practice=["Save and Reload a Model", "Batch Scoring in Chunks", "Validate an Inference Request", "Training–Serving Skew", "Point-in-Time Feature Join", "Scale Serving Data With Training Statistics"])

LESSON("Core", "Releasing safely and sizing the service", """
<ul>
<li><b>Shadow mode</b>: the new model scores live traffic but its answers are only logged. Compare with the current model at zero risk.</li>
<li><b>Canary</b>: send a small, sticky share of users (hash of the user id) to the new model, watch metrics, then widen. <b>Blue/green</b> keeps the old version running for instant rollback.</li>
<li><b>A/B test</b> the business metric before a full launch.</li>
</ul>
<p>Size the service from the <b>tail</b>, not the average: p95 and p99 latency are what users feel. Little's law (requests in flight = arrival rate × time per request) gives the number of replicas, with headroom so they don't run at 100%.</p>
""", practice=["Shadow Mode Comparison", "Canary Routing by Hash", "Latency Percentiles", "How Many Replicas?"])

LESSON("Advanced", "Monitoring: drift, decay and retraining", """
<p>The world changes, so models decay. Watch three layers:</p>
<ol>
<li><b>Service health</b>: errors, latency, throughput.</li>
<li><b>Data drift</b>: are inputs still like the training data? <b>PSI</b> on binned features (&lt; 0.1 stable, 0.1–0.25 watch, &gt; 0.25 act) and the <b>KS test</b> for numeric columns; also the prediction distribution itself.</li>
<li><b>Model quality</b>: accuracy once true labels arrive — often days or weeks later — tracked on a rolling window.</li>
</ol>
<p><b>Concept drift</b> (the relationship between inputs and outcome changes, e.g. fraudsters adapt) can happen with no input drift at all, which is why labelled feedback matters. Retrain on a schedule, on alerts, or both — and every retrained model goes through the same gates and release steps as the first.</p>
""", practice=["Population Stability Index", "Kolmogorov–Smirnov Drift Statistic", "Rolling Accuracy Alerts", "Should We Retrain?"])


@LD
def drift_picture():
    train = [21, 25, 29, 33, 35, 38, 41, 44, 47, 52, 55, 58, 61, 30, 36, 42]
    live = [45, 49, 52, 55, 58, 60, 62, 65, 41, 50, 57, 63, 66, 70, 39, 48]
    fig, ax = plt.subplots(figsize=(5, 2.6))
    for data, label, color in [(train, "training", "#0f766e"), (live, "live", "#b45309")]:
        xs = np.sort(data)
        ax.step(xs, np.arange(1, len(xs) + 1) / len(xs), where="post", label=label, color=color)
    ax.legend()
    ax.set_title("KS statistic = biggest vertical gap between the curves")
