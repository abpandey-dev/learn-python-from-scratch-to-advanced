import numpy as np
import pandas as pd


def churn_frame(rng, n, shift=False):
    plan = rng.choice(["basic", "standard", "premium"], n, p=[0.45, 0.35, 0.2])
    contract = rng.choice(["monthly", "annual"], n, p=[0.62, 0.38])
    region = rng.choice(["North", "South", "East", "West"], n)
    tenure = rng.integers(1, 61, n)
    base = np.select([plan == "basic", plan == "standard"], [299, 499], 799)
    charge = np.round(base * rng.uniform(0.9, 1.25 if shift else 1.15, n), 0)
    usage = np.round(rng.gamma(4, 6 if not shift else 4.5, n), 1)
    tickets = rng.poisson(1.2, n)
    failures = rng.poisson(0.3, n)
    last_login = rng.integers(0, 45, n)
    logit = (-1.9 + 1.4 * (contract == "monthly") - 0.035 * tenure + 0.55 * failures + 0.28 * tickets
             + 0.04 * last_login - 0.035 * usage + 0.35 * (plan == "basic") + 0.002 * (charge - base))
    churned = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    return pd.DataFrame({"tenure_months": tenure, "plan": plan, "contract": contract, "region": region,
                         "monthly_charge": charge, "usage_hours": usage, "support_tickets": tickets,
                         "payment_failures": failures, "last_login_days": last_login, "churned": churned})


def make_data(rng):
    df = churn_frame(rng, 5000)
    df.insert(0, "customer_id", [f"S{i:05d}" for i in range(len(df))])
    return {"churn_customers.csv": df}


PROJECT = dict(
    slug="subscription-churn",
    title="Predict Churn for a Subscription App",
    role="Data Scientist",
    level="Intermediate",
    hours="8–10",
    summary="A streaming app loses customers every month. Build a churn model, choose a decision threshold from the business cost, explain what drives churn, and hand the retention team a prioritised call list.",
    skills=["EDA", "train/test split", "scikit-learn pipelines", "logistic regression", "gradient boosting", "ROC AUC", "cost-based thresholds", "permutation importance"],
    brief="""
**The situation.** *StreamBox*, a subscription video app, loses about one in five customers each period. The retention team can call customers and offer a discount, but the offer costs money, so they can't call everyone. They ask you for:

1. Who is likely to churn, with a score for every customer.
2. How many customers to call: where to set the cut-off.
3. *Why* customers churn, in terms the business can act on.
4. A list of the customers to call first.
""",
    deliverable="a tested churn model (baseline and a stronger model), a threshold chosen from the business cost, the top churn drivers, and a prioritised retention list with its expected value.",
    data_notes="""
**churn_customers.csv** — one row per customer (5,000):

| Column | Meaning |
|---|---|
| customer_id | ID (not a feature!) |
| tenure_months | months as a customer |
| plan | basic / standard / premium |
| contract | monthly / annual |
| region | North / South / East / West |
| monthly_charge | ₹ per month |
| usage_hours | hours watched last month |
| support_tickets | tickets raised last quarter |
| payment_failures | failed payments last quarter |
| last_login_days | days since last login |
| churned | **target**: 1 if they left |
""",
    setup="""
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.inspection import permutation_importance
df = load("churn_customers.csv")
CAT = ["plan", "contract", "region"]
NUM = ["tenure_months", "monthly_charge", "usage_hours", "support_tickets", "payment_failures", "last_login_days"]


# Helpers used by the checks (they call the functions you write).
def fitted(make_model):
    X_train, X_test, y_train, y_test = split(df)
    return make_model(X_train, y_train), X_test, y_test


def auc_of(make_model):
    model, X_test, y_test = fitted(make_model)
    return round(roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]), 3)


def test_probs(make_model):
    model, X_test, y_test = fitted(make_model)
    return model.predict_proba(X_test)[:, 1], y_test.to_numpy()
""",
    milestones=[
        dict(title="Where is churn highest?",
             task="""
Write `churn_by(df, col)` returning `{category: churn rate %}` (rounded to 1) for a categorical column. The check runs it for `plan` and `contract`.

Then explore numeric columns yourself, e.g. `df.groupby('churned')[NUM].mean()`. Which ones look different for churners?
""",
             starter="""
def churn_by(df, col):
    raise NotImplementedError
""",
             solution="""
def churn_by(df, col):
    return (df.groupby(col)["churned"].mean() * 100).round(1).to_dict()
""",
             call="[churn_by(df, 'plan'), churn_by(df, 'contract')]"),
        dict(title="Split without leaking",
             task="""
Write `split(df)` returning `X_train, X_test, y_train, y_test`:
- features = every column except `customer_id` and `churned`,
- target = `churned`,
- 25% test, **stratified** on the target, `random_state=42`.

The check looks at the sizes and the churn rate in each part (stratifying keeps them equal).
""",
             hint="`train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)`.",
             starter="""
def split(df):
    raise NotImplementedError
""",
             solution="""
def split(df):
    X = df.drop(columns=["customer_id", "churned"])
    y = df["churned"]
    return train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
""",
             call="[len(split(df)[0]), len(split(df)[1]), round(split(df)[2].mean(), 4), round(split(df)[3].mean(), 4)]", tol=1e-9),
        dict(title="A baseline you can explain",
             task="""
Write `baseline_model(X_train, y_train)` returning a **fitted** `Pipeline`:
- a `ColumnTransformer` that one-hot encodes `CAT` and standard-scales `NUM`,
- then `LogisticRegression(max_iter=1000)`.

The check reports test ROC AUC. Putting preprocessing inside the pipeline means it is learned from training data only, and the same steps run when the model is used later.
""",
             hint="`ColumnTransformer([('cat', OneHotEncoder(handle_unknown='ignore'), CAT), ('num', StandardScaler(), NUM)])`",
             starter="""
def baseline_model(X_train, y_train):
    raise NotImplementedError
""",
             solution="""
def baseline_model(X_train, y_train):
    prep = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), CAT), ("num", StandardScaler(), NUM)])
    return Pipeline([("prep", prep), ("model", LogisticRegression(max_iter=1000))]).fit(X_train, y_train)
""",
             call="auc_of(baseline_model)", tol=0.01),
        dict(title="A stronger model",
             task="""
Write `boosted_model(X_train, y_train)`: same preprocessing idea, but `HistGradientBoostingClassifier(max_iter=200, learning_rate=0.05, random_state=0)` (scaling isn't needed for trees; one-hot with `sparse_output=False`).

Compare the AUC with your baseline. Is the extra complexity worth it here? (On this data the honest answer may surprise you.)
""",
             starter="""
def boosted_model(X_train, y_train):
    raise NotImplementedError
""",
             solution="""
def boosted_model(X_train, y_train):
    prep = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CAT)],
                             remainder="passthrough")
    model = HistGradientBoostingClassifier(max_iter=200, learning_rate=0.05, random_state=0)
    return Pipeline([("prep", prep), ("model", model)]).fit(X_train, y_train)
""",
             call="auc_of(boosted_model)", tol=0.015,
             after="When the true relationship is close to linear (as here), a well-prepared logistic regression is as good as boosting and far easier to explain. Always compare against a simple baseline before reaching for complexity."),
        dict(title="Choose the cut-off from the business cost",
             task="""
The retention team calls every customer whose churn probability is ≥ a threshold. Each call + discount costs **₹200**. A called customer who *would* have churned stays with probability **0.5**, and keeping a customer is worth **₹3,000**.

So for a threshold t, net value = Σ over called customers of (0.5 × 3000 × churned − 200).

Write `best_threshold(probs, y)` that tries t = 0.05, 0.10, …, 0.95 and returns `(best t, net value)`. The check uses the baseline model's test probabilities.
""",
             hint="For each t: `called = probs >= t`; value = `(0.5 * 3000 * y[called]).sum() - 200 * called.sum()`.",
             starter="""
def best_threshold(probs, y):
    raise NotImplementedError
""",
             solution="""
def best_threshold(probs, y):
    best = None
    for t in np.round(np.arange(0.05, 0.96, 0.05), 2):
        called = probs >= t
        value = (0.5 * 3000 * y[called]).sum() - 200 * called.sum()
        if best is None or value > best[1]:
            best = (float(t), float(value))
    return best
""",
             call="best_threshold(*test_probs(baseline_model))", tol=0.03,
             after="Notice the best threshold is far below 0.5: a missed churner costs much more than a wasted call. The *default* 0.5 cut-off is almost never the business-optimal one."),
        dict(title="What drives churn?",
             task="""
Write `top_drivers(model, X_test, y_test)` returning the names of the **3 most important** original columns by permutation importance (`scoring='roc_auc'`, `n_repeats=5`, `random_state=0`), most important first. The check uses the boosted model and compares **which** three features you found, not their order: features with nearly equal importance can swap places between library versions.
""",
             hint="`permutation_importance(model, X_test, y_test, scoring='roc_auc', n_repeats=5, random_state=0)` works on the whole pipeline, so it shuffles the original columns.",
             starter="""
def top_drivers(model, X_test, y_test):
    raise NotImplementedError
""",
             solution="""
def top_drivers(model, X_test, y_test):
    r = permutation_importance(model, X_test, y_test, scoring="roc_auc", n_repeats=5, random_state=0)
    order = np.argsort(-r.importances_mean)[:3]
    return [X_test.columns[i] for i in order]
""",
             call="sorted(top_drivers(*fitted(boosted_model)))", tol=1e-9,
             after="Turn drivers into actions: monthly contracts → offer an annual plan; payment failures → fix billing reminders; low usage / long since login → re-engagement emails."),
        dict(title="The call list",
             task="""
The team can call **100** customers this week. Rank test customers by **expected value at risk** = churn probability × monthly_charge × 12, and take the top 100.

Write `call_list(model, X_test, y_test, n=100)` returning `(how many of the n actually churned, total expected value at risk rounded to 0)`. The check uses the baseline model.
""",
             starter="""
def call_list(model, X_test, y_test, n=100):
    raise NotImplementedError
""",
             solution="""
def call_list(model, X_test, y_test, n=100):
    p = model.predict_proba(X_test)[:, 1]
    value = p * X_test["monthly_charge"].to_numpy() * 12
    top = np.argsort(-value)[:n]
    return int(y_test.to_numpy()[top].sum()), round(float(value[top].sum()))
""",
             call="call_list(*fitted(baseline_model))", tol=0.05),
    ],
    present="""
Write a short model report for the retention team and your manager:

1. **Problem and data**: what churn means here, the churn rate, the features.
2. **Models**: baseline vs boosted AUC, which you chose and why.
3. **Decision rule**: the threshold, how many customers it flags, and the expected net value vs calling no one or everyone.
4. **Drivers** and a recommended action for each.
5. **Call list**: the top 100, how many are expected to churn.
6. **Risks**: the model is correlational, it needs monitoring and retraining, and the offer's real effect should be measured with an A/B test.
""",
    resume=[
        "Built a churn model for 5,000 subscribers with scikit-learn pipelines (logistic regression and gradient boosting, test AUC **0.XX**)",
        "Chose the decision threshold from offer cost and customer value, raising expected retention value to **₹X** vs the default cut-off",
        "Identified the top churn drivers with permutation importance and turned them into retention actions",
    ],
    interview=[
        "Why did you stratify the split, and why exclude customer_id?",
        "Your boosted model wasn't much better than logistic regression. What does that tell you, and which would you deploy?",
        "Why isn't 0.5 the right threshold? Walk me through your cost calculation.",
        "Permutation importance says payment failures matter. Does that mean fixing payments will reduce churn?",
        "How would you check that the retention offer actually works?",
        "What would you monitor after deploying this model?",
    ],
    extensions=[
        "Calibrate the probabilities (`CalibratedClassifierCV`) and check with a reliability curve.",
        "Tune the boosted model with cross-validated search and see whether AUC moves.",
        "Explain single predictions with SHAP values for the top 5 customers on the call list.",
        "Project 7 takes this model to production — do it next.",
    ],
)
