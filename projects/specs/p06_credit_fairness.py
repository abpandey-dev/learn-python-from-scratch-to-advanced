import numpy as np
import pandas as pd


def make_data(rng):
    n = 6000
    gender = rng.choice(["F", "M"], n, p=[0.42, 0.58])
    region = rng.choice(["urban", "rural"], n, p=[0.65, 0.35])
    age = rng.integers(21, 61, n)
    income = np.round(rng.lognormal(np.log(45) + 0.25 * (region == "urban") + 0.08 * (gender == "M"), 0.45), 1)
    employment = np.clip(np.round(rng.gamma(2, 2.5, n) * (age - 18) / 25, 1), 0, 40)
    dti = np.round(np.clip(rng.beta(2, 5, n) * 0.9, 0.02, 0.85), 3)
    prior = rng.poisson(0.25, n)
    loan = np.round(income * rng.uniform(2, 12, n), 0)
    history = np.clip(np.round(rng.normal((age - 21) * 0.6, 2), 1), 0, None)
    logit = (-2.0 - 0.025 * (income - 45) + 4.2 * (dti - 0.25) + 0.9 * prior - 0.06 * employment
             + 0.004 * (loan / income - 7) * 10 - 0.03 * history + 0.2 * (region == "rural"))
    default = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    df = pd.DataFrame({"applicant_id": [f"A{i:05d}" for i in range(n)], "age": age, "gender": gender, "region": region,
                       "income_k": income, "employment_years": employment, "debt_to_income": dti,
                       "prior_defaults": prior, "loan_amount_k": loan, "credit_history_years": history, "default": default})
    return {"credit_applicants.csv": df}


PROJECT = dict(
    slug="fair-credit-scoring",
    title="Fair Credit-Risk Scoring",
    role="Data Scientist",
    level="Advanced",
    hours="8–10",
    summary="A digital lender wants an automated loan decision. Build a calibrated default-risk model, audit it for fairness between groups, and give every rejected applicant reasons and a path to approval.",
    skills=["logistic regression", "calibration", "Brier score", "approval policy", "fairness metrics", "disparate impact", "reason codes", "counterfactuals"],
    brief="""
**The situation.** *QuickCredit*, a digital lender, approves personal loans in minutes. Regulators and the company's own ethics board require that the automated decision is **accurate, well-calibrated, fair across groups, and explainable** to every applicant who is turned down.

The model must not use gender. But removing a column doesn't guarantee fairness: other features can carry the same information. You'll build the model, set the approval policy, then audit it like a model-risk reviewer would.
""",
    deliverable="a default-risk model with calibration evidence, an approval policy, a fairness audit (selection rates, disparate impact, equal opportunity), reason codes for rejections, and a counterfactual for one applicant.",
    data_notes="""
**credit_applicants.csv** — 6,000 past applicants with known outcomes:

| Column | Meaning |
|---|---|
| applicant_id | ID |
| age, gender, region | demographics (`gender` must **not** be a model input; it's kept only for the audit) |
| income_k | monthly income, ₹ thousand |
| employment_years | years in current employment |
| debt_to_income | existing debt payments ÷ income |
| prior_defaults | number of past defaults |
| loan_amount_k | requested amount, ₹ thousand |
| credit_history_years | length of credit history |
| default | **target**: 1 if the loan defaulted |
""",
    setup="""
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, brier_score_loss
apps = load("credit_applicants.csv")
NUM = ["age", "income_k", "employment_years", "debt_to_income", "prior_defaults", "loan_amount_k", "credit_history_years"]
CAT = ["region"]
FEATURES = NUM + CAT
CUTOFF = 0.15        # approve when predicted default probability is below this
train, test = train_test_split(apps, test_size=0.3, stratify=apps["default"], random_state=7)


# Used by the checks: your model's test-set probabilities.
def test_pd():
    model = fit_model(train)
    return model, model.predict_proba(test[FEATURES])[:, 1]
""",
    milestones=[
        dict(title="Know the base rates",
             task="""
Write `default_rates(apps)` returning `{"overall": %, "F": %, "M": %, "urban": %, "rural": %}` — default rates rounded to 2.

Differences in base rates between groups are a fact about the data; how the model treats people *given* their risk is what the fairness audit will check.
""",
             starter="""
def default_rates(apps):
    raise NotImplementedError
""",
             solution="""
def default_rates(apps):
    out = {"overall": round(apps["default"].mean() * 100, 2)}
    for col in ["gender", "region"]:
        out.update((apps.groupby(col)["default"].mean() * 100).round(2).to_dict())
    return out
""",
             call="default_rates(apps)"),
        dict(title="An explainable risk model",
             task="""
Write `fit_model(train)` returning a fitted `Pipeline`: one-hot `CAT`, standard-scale `NUM`, then `LogisticRegression(max_iter=1000)`, trained on `FEATURES` (no gender!) → `default`.

The check reports test ROC AUC. Lenders often prefer logistic regression: every coefficient can be explained and audited.
""",
             starter="""
def fit_model(train):
    raise NotImplementedError
""",
             solution="""
def fit_model(train):
    prep = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), CAT), ("num", StandardScaler(), NUM)])
    model = Pipeline([("prep", prep), ("lr", LogisticRegression(max_iter=1000))])
    return model.fit(train[FEATURES], train["default"])
""",
             call="round(roc_auc_score(test['default'], test_pd()[1]), 3)", tol=0.01),
        dict(title="Can we trust the probabilities?",
             task="""
Pricing and the cut-off use the probability itself, so it must be **calibrated**: among applicants scored 10%, about 10% should default.

Write `calibration(y, p, bins=10)` returning `[Brier score, ECE]` rounded to 4. ECE = Σ over non-empty equal-width bins of (bin share of rows) × |mean predicted − observed default rate|.
""",
             hint="Bin index = `np.minimum((p * bins).astype(int), bins - 1)`; then group by it.",
             starter="""
def calibration(y, p, bins=10):
    raise NotImplementedError
""",
             solution="""
def calibration(y, p, bins=10):
    y, p = np.asarray(y), np.asarray(p)
    b = np.minimum((p * bins).astype(int), bins - 1)
    ece = sum((b == k).mean() * abs(p[b == k].mean() - y[b == k].mean()) for k in np.unique(b))
    return [round(float(brier_score_loss(y, p)), 4), round(float(ece), 4)]
""",
             call="calibration(test['default'], test_pd()[1])", tol=0.05),
        dict(title="The approval policy and its impact on groups",
             task="""
Approve when predicted default probability < `CUTOFF` (0.15). Write `approval_audit(test, p)` returning:
`{"approval_rate": %, "F": %, "M": %, "disparate_impact": lower group rate ÷ higher group rate}` — rates rounded to 1, the ratio to 3.

The **four-fifths rule** flags a ratio below 0.8 for review.
""",
             starter="""
def approval_audit(test, p):
    raise NotImplementedError
""",
             solution="""
def approval_audit(test, p):
    approved = pd.Series(p < CUTOFF, index=test.index)
    by = approved.groupby(test["gender"]).mean() * 100
    return {"approval_rate": round(approved.mean() * 100, 1), "F": round(by["F"], 1), "M": round(by["M"], 1),
            "disparate_impact": round(by.min() / by.max(), 3)}
""",
             call="approval_audit(test, test_pd()[1])", tol=0.03),
        dict(title="Equal opportunity for good borrowers",
             task="""
Different approval rates can come from different risk levels. A sharper question: **among applicants who would have repaid** (`default == 0`), are both genders approved at the same rate?

Write `equal_opportunity(test, p)` returning `{"F": %, "M": %, "gap_pp": M − F}`, rounded to 1.
""",
             starter="""
def equal_opportunity(test, p):
    raise NotImplementedError
""",
             solution="""
def equal_opportunity(test, p):
    good = test["default"] == 0
    approved = pd.Series(p < CUTOFF, index=test.index)
    rate = approved[good].groupby(test.loc[good, "gender"]).mean() * 100
    return {"F": round(rate["F"], 1), "M": round(rate["M"], 1), "gap_pp": round(rate["M"] - rate["F"], 1)}
""",
             call="equal_opportunity(test, test_pd()[1])", tol=0.04,
             after="The model never saw gender, yet good borrowers of the two groups are approved at slightly different rates (a gap of a few points), because **income** — a model input — differs between groups in this data. That's the proxy problem, here in a mild form. A ratio of 0.97 passes the four-fifths rule, but an auditor will still ask you to explain the gap. Options: accept it if income is a legitimate, necessary risk factor; adjust the policy; or collect better features. Write down which you'd recommend and why — that judgement is the point of the audit."),
        dict(title="Reason codes for rejected applicants",
             task="""
Lenders must tell rejected applicants **why**. For a logistic model, each scaled numeric feature contributes `coefficient × scaled value` to the risk score.

Write `reasons(model, row, n=2)` returning the names of the n numeric features (from `NUM`) pushing this applicant's risk **up** the most, biggest first. The check runs it on the first three rejected test applicants.
""",
             hint="`prep = model.named_steps['prep']`; `x = prep.transform(row[FEATURES])[0]`; names from `prep.get_feature_names_out()` look like `num__income_k`.",
             starter="""
def reasons(model, row, n=2):
    raise NotImplementedError
""",
             solution="""
def reasons(model, row, n=2):
    prep, lr = model.named_steps["prep"], model.named_steps["lr"]
    x = prep.transform(row[FEATURES])[0]
    names = prep.get_feature_names_out()
    contrib = {name.split("__")[1]: c * v for name, c, v in zip(names, lr.coef_[0], x) if name.startswith("num__")}
    return sorted(contrib, key=contrib.get, reverse=True)[:n]
""",
             call="[reasons(test_pd()[0], test.iloc[[i]]) for i in np.flatnonzero(test_pd()[1] >= CUTOFF)[:3]]", tol=1e-9),
        dict(title="What would get them approved?",
             task="""
Write `income_needed(model, row)` returning the smallest monthly income (₹ thousand, a whole number) at which this applicant's predicted default probability drops below `CUTOFF`, keeping everything else the same — or `None` if no income up to 1,000 works. The check uses the first rejected test applicant.
""",
             hint="Copy the row, try income = current, current + 1, … and predict each time. (A smarter way: solve the logistic equation directly — try it after.)",
             starter="""
def income_needed(model, row):
    raise NotImplementedError
""",
             solution="""
def income_needed(model, row):
    trial = row[FEATURES].copy()
    for income in range(int(math.ceil(row["income_k"].iloc[0])), 1001):
        trial["income_k"] = float(income)
        if model.predict_proba(trial)[0, 1] < CUTOFF:
            return income
    return None
""",
             call="income_needed(test_pd()[0], test.iloc[[int(np.flatnonzero(test_pd()[1] >= CUTOFF)[0])]])", tol=0.05,
             after="Good counterfactuals use features a person can change (income, debt). Never suggest changing age or gender, and check the suggestion is realistic."),
    ],
    present="""
Write a model-risk memo (one page):

1. **Purpose and data**: what the model decides, the base default rate.
2. **Performance**: AUC and calibration (Brier, ECE) — is the probability trustworthy?
3. **Policy**: the cut-off, approval rate, expected default rate among approved applicants.
4. **Fairness audit**: approval rates by gender, disparate impact, equal opportunity gap, and the proxy explanation.
5. **Explainability**: example reason codes and a counterfactual.
6. **Recommendation and monitoring**: what you'd change before launch, and which fairness and calibration metrics to track monthly.
""",
    resume=[
        "Built an explainable default-risk model (logistic regression, test AUC **0.XX**, ECE **0.0X**) for 6,000 loan applicants",
        "Audited the approval policy for fairness (disparate impact **0.XX**, equal-opportunity gap **X pp**) and traced the gap to an income proxy",
        "Generated reason codes and income counterfactuals for rejected applicants to meet explainability requirements",
    ],
    interview=[
        "You removed gender from the features. Why is the model still not necessarily fair?",
        "What's the difference between demographic parity and equal opportunity? Which would you use for lending?",
        "Why does calibration matter for a credit model?",
        "How did you generate reason codes, and when would that method be misleading?",
        "The business wants a higher approval rate. What do you change, and what are the risks?",
        "What would you monitor after launch?",
    ],
    extensions=[
        "Try a gradient-boosting model, then explain it with SHAP. Is the accuracy gain worth the explainability cost?",
        "Find a cut-off per group that equalises the equal-opportunity gap, and discuss whether that's allowed.",
        "Recalibrate with `CalibratedClassifierCV` and compare ECE.",
        "Write a model card for this model.",
    ],
)
