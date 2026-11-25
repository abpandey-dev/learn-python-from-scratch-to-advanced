from lib import *

THEORY("The ML lifecycle", """
<table>
<tr><th>Stage</th><th>Key question</th><th>Typical tools</th></tr>
<tr><td>Data</td><td>is it complete, valid, versioned?</td><td>SQL, DVC, Great Expectations</td></tr>
<tr><td>Features</td><td>same logic offline and online? point-in-time correct?</td><td>feature stores (Feast)</td></tr>
<tr><td>Training</td><td>reproducible and tracked?</td><td>MLflow, W&amp;B</td></tr>
<tr><td>Evaluation</td><td>better than production, on every key segment?</td><td>test sets, CI checks</td></tr>
<tr><td>Packaging</td><td>runs the same everywhere?</td><td>joblib, Docker</td></tr>
<tr><td>Serving</td><td>batch or real-time? fast enough?</td><td>FastAPI, KServe, SageMaker, Vertex AI</td></tr>
<tr><td>Release</td><td>safe rollout and rollback?</td><td>shadow, canary, blue/green</td></tr>
<tr><td>Monitoring</td><td>drifting? decaying? healthy?</td><td>Evidently, Prometheus + Grafana</td></tr>
</table>
""")

THEORY("Kinds of drift", """
<ul>
<li><b>Data (covariate) drift</b>: P(X) changes — new customer mix, a new app version sending different values.</li>
<li><b>Label (prior) drift</b>: P(y) changes — fraud rate doubles during a festival sale.</li>
<li><b>Concept drift</b>: P(y | X) changes — the same behaviour now means something different.</li>
<li><b>Upstream breakage</b>: a column renamed, units changed (rupees → paise), a join started dropping rows. Not "drift" but the most common cause of alerts.</li>
</ul>
""")

THEORY("Drift statistics", """
<table>
<tr><th>Statistic</th><th>For</th><th>Rule of thumb</th></tr>
<tr><td>PSI = Σ (a − e) ln(a / e)</td><td>binned numeric or categorical</td><td>&lt; 0.1 stable · 0.1–0.25 moderate · &gt; 0.25 major</td></tr>
<tr><td>KS statistic</td><td>numeric</td><td>max ECDF gap; p-value from <code>ks_2samp</code></td></tr>
<tr><td>χ² test</td><td>categorical</td><td>counts vs training shares</td></tr>
<tr><td>Jensen–Shannon distance</td><td>any distribution</td><td>bounded 0–1, symmetric</td></tr>
</table>
<p>With very large samples, tests flag tiny harmless shifts; judge by effect size (PSI) and by impact on model quality.</p>
""")

FAQ("Batch or real-time serving?", "<p>Batch when predictions can be computed ahead of time (daily churn scores, recommendations refreshed nightly): simpler and cheaper. Real-time when the answer depends on fresh input at request time (fraud checks, search ranking).</p>")
FAQ("What is training–serving skew and how do you prevent it?", "<p>A difference between features or preprocessing at training time and at serving time. Prevent it by packaging preprocessing inside the model pipeline, sharing feature code or a feature store, and comparing logged online features with offline recomputation.</p>")
FAQ("How do you know a deployed model is getting worse?", "<p>Monitor input and prediction drift continuously, and model quality once labels arrive, on rolling windows and per segment, with alerts on thresholds.</p>")
FAQ("What does a model registry give you?", "<p>Versioned models with metadata (metrics, data and code versions), stage transitions with an audit trail, and one-step rollback to a previous version.</p>")
FAQ("Shadow vs canary deployment?", "<p>Shadow runs the new model on live traffic without using its answers — zero user risk. Canary actually serves a small share of users with the new model, so it tests real-world effects but carries limited risk.</p>")
FAQ("Why use Docker for ML?", "<p>It packages the code, exact library versions, system dependencies and model into one image, so it behaves identically on a laptop, in CI and in production, and scales easily on Kubernetes.</p>")
FAQ("What is a point-in-time join?", "<p>Joining each training label only with feature values that existed at the label's timestamp, so the model never trains on information from the future.</p>")
