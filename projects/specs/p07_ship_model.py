from p03_churn import churn_frame


def make_data(rng):
    live = churn_frame(rng, 2000, shift=True)
    live.insert(0, "customer_id", [f"N{i:05d}" for i in range(len(live))])
    return {"churn_new_month.csv": live}


API_CODE = '''
# app.py — run locally with:  pip install fastapi uvicorn joblib scikit-learn pandas
#                              uvicorn app:app --reload   then open http://127.0.0.1:8000/docs
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal

model = joblib.load("churn_model.joblib")
app = FastAPI(title="Churn scoring API", version="1.0.0")


class Customer(BaseModel):
    tenure_months: int = Field(ge=0, le=600)
    plan: Literal["basic", "standard", "premium"]
    contract: Literal["monthly", "annual"]
    region: Literal["North", "South", "East", "West"]
    monthly_charge: float = Field(gt=0)
    usage_hours: float = Field(ge=0)
    support_tickets: int = Field(ge=0)
    payment_failures: int = Field(ge=0)
    last_login_days: int = Field(ge=0)


@app.get("/health")
def health():
    return {"status": "ok", "model_version": "1.0.0"}


@app.post("/predict")
def predict(c: Customer):
    p = float(model.predict_proba(pd.DataFrame([c.model_dump()]))[0, 1])
    return {"churn_probability": round(p, 3), "risk": "high" if p >= 0.5 else "medium" if p >= 0.2 else "low"}
'''

DOCKERFILE = '''
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py churn_model.joblib ./
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
'''

PROJECT = dict(
    slug="ship-the-churn-model",
    title="Ship It: Serve and Monitor the Churn Model",
    role="MLOps / ML Engineer",
    level="Advanced",
    hours="8–10",
    summary="Take the churn model from project 3 to production: package the pipeline, validate requests, serve predictions, score a monthly batch, detect drift in new data, and decide when to retrain.",
    skills=["joblib", "request validation", "FastAPI", "Docker", "batch scoring", "PSI drift", "monitoring", "retraining policy"],
    brief="""
**The situation.** The retention team loved your churn model (project 3 — do that one first). Now engineering wants it **in production**: the app should get a churn score for a customer in real time, the marketing system needs scores for every customer each month, and the team must know when the model goes stale.

A month after launch, a new batch of customers arrives. Pricing changed and people are watching less. Is the model still trustworthy?
""",
    deliverable="a saved model pipeline, a validated prediction function, an API (FastAPI) and Dockerfile, a monthly batch score file, a drift report with PSI per feature, and a retrain decision backed by numbers.",
    data_notes="""
**churn_customers.csv** — the 5,000 customers the model is trained on (same file as project 3).

**churn_new_month.csv** — 2,000 customers from the month after launch, same columns. Their `churned` outcomes arrive at the end of the month, so use them only for the final monitoring milestone.
""",
    setup="""
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
train_df = load("churn_customers.csv")
live_df = load("churn_new_month.csv")
CAT = ["plan", "contract", "region"]
NUM = ["tenure_months", "monthly_charge", "usage_hours", "support_tickets", "payment_failures", "last_login_days"]
FEATURES = NUM + CAT
SCHEMA = {"tenure_months": (int, 0, 600), "monthly_charge": (float, 1, 100000), "usage_hours": (float, 0, 1000),
          "support_tickets": (int, 0, 100), "payment_failures": (int, 0, 100), "last_login_days": (int, 0, 3650),
          "plan": (["basic", "standard", "premium"],), "contract": (["monthly", "annual"],),
          "region": (["North", "South", "East", "West"],)}
GOOD = {"tenure_months": 3, "monthly_charge": 299.0, "usage_hours": 2.5, "support_tickets": 4, "payment_failures": 2,
        "last_login_days": 30, "plan": "basic", "contract": "monthly", "region": "East"}


# Used by the checks.
def loaded_model():
    return joblib.load(train_and_save(train_df))
""",
    milestones=[
        dict(title="Package the whole pipeline",
             task="""
In production you ship **one object** that does preprocessing *and* prediction, so the app can't prepare features differently from training (training–serving skew).

Write `train_and_save(df, path="churn_model.joblib")`: fit a `Pipeline` (one-hot `CAT`, scale `NUM`, `LogisticRegression(max_iter=1000)`) on **all** rows of `df`, save it with `joblib.dump`, and return the path.

The check loads it back and scores the first 200 new customers.
""",
             starter="""
def train_and_save(df, path="churn_model.joblib"):
    raise NotImplementedError
""",
             solution="""
def train_and_save(df, path="churn_model.joblib"):
    prep = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), CAT), ("num", StandardScaler(), NUM)])
    model = Pipeline([("prep", prep), ("lr", LogisticRegression(max_iter=1000))]).fit(df[FEATURES], df["churned"])
    joblib.dump(model, path)
    return path
""",
             call="round(float(loaded_model().predict_proba(live_df[FEATURES].head(200))[:, 1].mean()), 3)", tol=0.01),
        dict(title="Never trust the input",
             task="""
An API receives whatever clients send. Write `validate(request)` returning `(ok, errors)`, where `errors` is a sorted list of messages:
- `"<field>: missing"` for each field of `SCHEMA` not present,
- `"<field>: wrong type"` if a number field isn't a number (ints are fine for float fields; booleans are never numbers), or a category isn't a string,
- `"<field>: out of range"` if a number is outside (min, max) or a category isn't one of the allowed values.

`SCHEMA[field]` is `(type, min, max)` for numbers or `([allowed values],)` for categories.
""",
             hint="For numbers: `isinstance(v, (int, float)) and not isinstance(v, bool)`; ints are required where the type is `int`.",
             starter="""
def validate(request):
    raise NotImplementedError
""",
             solution="""
def validate(request):
    errors = []
    for field, rule in SCHEMA.items():
        if field not in request:
            errors.append(f"{field}: missing")
            continue
        v = request[field]
        if len(rule) == 1:
            if not isinstance(v, str):
                errors.append(f"{field}: wrong type")
            elif v not in rule[0]:
                errors.append(f"{field}: out of range")
            continue
        kind, lo, hi = rule
        number = isinstance(v, (int, float)) and not isinstance(v, bool)
        if not number or (kind is int and not isinstance(v, int)):
            errors.append(f"{field}: wrong type")
        elif not lo <= v <= hi:
            errors.append(f"{field}: out of range")
    return not errors, sorted(errors)
""",
             call="[validate(GOOD), validate({**GOOD, 'plan': 'gold', 'tenure_months': 2.5}), validate({k: v for k, v in GOOD.items() if k != 'region'}), validate({**GOOD, 'usage_hours': True, 'monthly_charge': -5})]", tol=1e-9),
        dict(title="Predict one customer",
             task="""
Write `predict_one(model, request)`. If the request is invalid return `{"errors": [...]}`. Otherwise return `{"churn_probability": p rounded to 3, "risk": "high" if p ≥ 0.5, "medium" if p ≥ 0.2, else "low"}`.

This is exactly what the `/predict` endpoint of the API below will call.
""",
             starter="""
def predict_one(model, request):
    raise NotImplementedError
""",
             solution="""
def predict_one(model, request):
    ok, errors = validate(request)
    if not ok:
        return {"errors": errors}
    p = float(model.predict_proba(pd.DataFrame([request])[FEATURES])[0, 1])
    risk = "high" if p >= 0.5 else "medium" if p >= 0.2 else "low"
    return {"churn_probability": round(p, 3), "risk": risk}
""",
             call="[predict_one(loaded_model(), GOOD), predict_one(loaded_model(), {**GOOD, 'contract': 'annual', 'tenure_months': 48, 'payment_failures': 0, 'support_tickets': 0, 'last_login_days': 1, 'usage_hours': 40.0}), predict_one(loaded_model(), {**GOOD, 'plan': 'gold'})]", tol=0.02),
        dict(title="Score the monthly batch",
             task="""
Marketing needs a score for every customer each month. Write `score_batch(model, frame, chunk=500)` that scores `frame` **in chunks** of `chunk` rows (big tables don't fit in memory at once) and returns a DataFrame with `customer_id`, `churn_probability` and `risk`.

The check counts customers per risk level for the new month.
""",
             starter="""
def score_batch(model, frame, chunk=500):
    raise NotImplementedError
""",
             solution="""
def score_batch(model, frame, chunk=500):
    parts = []
    for start in range(0, len(frame), chunk):
        part = frame.iloc[start:start + chunk]
        p = model.predict_proba(part[FEATURES])[:, 1]
        parts.append(pd.DataFrame({"customer_id": part["customer_id"].to_numpy(), "churn_probability": p.round(3)}))
    out = pd.concat(parts, ignore_index=True)
    out["risk"] = np.select([out.churn_probability >= 0.5, out.churn_probability >= 0.2], ["high", "medium"], "low")
    return out
""",
             call="score_batch(loaded_model(), live_df)['risk'].value_counts().sort_index().to_dict()", tol=0.05),
        dict(title="Has the data drifted?",
             task="""
Write `psi(expected, actual, bins=10)`, the **Population Stability Index** of a numeric feature: cut both samples using the **deciles of the training data** as bin edges (extend the outer edges to −∞ and +∞), take each bin's share (use 0.0001 for empty bins), and return Σ (actual − expected) × ln(actual / expected), rounded to 3.

The check runs it for every numeric feature, training vs new month. Rule of thumb: < 0.1 stable, 0.1–0.25 watch, > 0.25 act.
""",
             hint="`edges = np.quantile(expected, np.linspace(0, 1, bins + 1))`, then `edges[0], edges[-1] = -np.inf, np.inf` and `np.unique(edges)` (repeated values can merge bins). `np.histogram(x, edges)[0] / len(x)`.",
             starter="""
def psi(expected, actual, bins=10):
    raise NotImplementedError
""",
             solution="""
def psi(expected, actual, bins=10):
    edges = np.quantile(expected, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    edges = np.unique(edges)
    e = np.maximum(np.histogram(expected, edges)[0] / len(expected), 0.0001)
    a = np.maximum(np.histogram(actual, edges)[0] / len(actual), 0.0001)
    return round(float(((a - e) * np.log(a / e)).sum()), 3)
""",
             call="{c: psi(train_df[c], live_df[c]) for c in NUM}", tol=0.1,
             after="Two features moved: prices went up (`monthly_charge`) and people watch less (`usage_hours`). Also compare the average predicted churn probability on training vs new data — **prediction drift** often shows up before labels arrive."),
        dict(title="Monitor and decide",
             task="""
The month is over and the `churned` labels for the new customers have arrived. Write `monitoring_report(model)` returning a dict:
- `train_auc`, `live_auc`: ROC AUC on training data and on the new month (rounded to 3),
- `drifted`: sorted list of numeric features with PSI > 0.2,
- `decision`: `"retrain"` if any feature drifted **or** live AUC is more than 0.05 below training AUC, else `"keep"`.
""",
             starter="""
def monitoring_report(model):
    raise NotImplementedError
""",
             solution="""
def monitoring_report(model):
    auc = lambda d: round(roc_auc_score(d["churned"], model.predict_proba(d[FEATURES])[:, 1]), 3)
    train_auc, live_auc = auc(train_df), auc(live_df)
    drifted = sorted(c for c in NUM if psi(train_df[c], live_df[c]) > 0.2)
    decision = "retrain" if drifted or live_auc < train_auc - 0.05 else "keep"
    return {"train_auc": train_auc, "live_auc": live_auc, "drifted": drifted, "decision": decision}
""",
             call="monitoring_report(loaded_model())", tol=0.03,
             after="Notice the model's AUC barely moved even though inputs drifted. Drift is a *warning*, not proof the model is broken. A good policy retrains on a schedule, investigates drift alerts, and only ships the retrained model if it beats the current one on recent data."),
    ],
    extra=[
        ("## Serve it as an API\n\nSave this as `app.py` next to `churn_model.joblib` and run it on your computer. FastAPI validates requests with the `Customer` model (the same rules you wrote by hand) and gives you interactive docs at `/docs`.\n\n```python\n" + API_CODE.strip() + "\n```", None),
        ("## Package it with Docker\n\nA `Dockerfile` puts the code, the exact library versions and the model into one image that runs the same on your laptop and in the cloud. Create `requirements.txt` with pinned versions (`pip freeze`), then:\n\n```dockerfile\n" + DOCKERFILE.strip() + "\n```\n\n```bash\ndocker build -t churn-api:1.0.0 .\ndocker run -p 8000:8000 churn-api:1.0.0\ncurl -X POST localhost:8000/predict -H 'Content-Type: application/json' -d '{\"tenure_months\": 3, \"plan\": \"basic\", \"contract\": \"monthly\", \"region\": \"East\", \"monthly_charge\": 299, \"usage_hours\": 2.5, \"support_tickets\": 4, \"payment_failures\": 2, \"last_login_days\": 30}'\n```", None),
    ],
    present="""
Write a short launch document (a README for the service):

1. **What it does**: inputs, outputs, risk bands.
2. **How to run it**: API, Docker, batch job.
3. **Validation rules** for requests.
4. **Monitoring**: which metrics (PSI per feature, prediction drift, live AUC when labels arrive), thresholds and the retrain rule.
5. **First month's report**: your drift table and decision.
6. **Rollback plan**: keep the previous model file and version; how to switch back.
""",
    resume=[
        "Productionised a churn model as a versioned scikit-learn pipeline behind a FastAPI endpoint with request validation, containerised with Docker",
        "Built chunked batch scoring for monthly runs and a drift monitor (PSI per feature, live AUC) with an automatic retrain rule",
        "Detected pricing and usage drift one month after launch (PSI **X**) and documented the retrain decision",
    ],
    interview=[
        "What is training–serving skew and how did packaging the pipeline prevent it?",
        "Why validate requests if the model would just raise an error anyway?",
        "Batch vs real-time scoring — when would you use each here?",
        "Your PSI flagged drift but AUC is fine. Retrain or not? Why?",
        "How would you roll out a retrained model safely?",
        "What would you log for every prediction?",
    ],
    extensions=[
        "Track runs and the model version with MLflow, and register the model.",
        "Add a GitHub Actions workflow that runs tests on `predict_one` and `validate` on every push.",
        "Log every prediction to a SQLite table and compute daily prediction drift from it.",
        "Shadow-test a retrained model on the new month before switching.",
    ],
)
