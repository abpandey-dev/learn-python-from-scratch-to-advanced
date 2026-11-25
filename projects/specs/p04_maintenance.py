import numpy as np
import pandas as pd


def make_data(rng):
    rows = []
    for m in range(1, 41):
        base_v, base_t, base_p = rng.normal(1.0, 0.08), rng.normal(62, 2), rng.normal(30, 1)
        next_fail = int(rng.integers(30, 110))
        for day in range(1, 241):
            to_fail = next_fail - day
            v = base_v + rng.normal(0, 0.07)
            t = base_t + rng.normal(0, 1.2)
            if 0 <= to_fail < 12:
                v += 0.05 * (12 - to_fail) + rng.normal(0, 0.05)
                t += 0.35 * (12 - to_fail)
            if rng.random() < 0.01:
                v += rng.uniform(0.3, 0.6)
            failure = int(to_fail == 0)
            rows.append((f"M{m:02d}", day, round(t, 2), round(v, 3), round(base_p + rng.normal(0, 1.5), 2), failure))
            if failure:
                next_fail = day + int(rng.integers(45, 110))
    return {"machine_sensors.csv": pd.DataFrame(rows, columns=["machine_id", "day", "temperature", "vibration", "pressure", "failure"])}


PROJECT = dict(
    slug="predictive-maintenance",
    title="Predictive Maintenance from Sensor Data",
    role="ML Engineer",
    level="Intermediate–Advanced",
    hours="8–10",
    summary="A factory wants a warning before machines break. Build the label carefully, engineer time-series features, validate on the future, and design an alert policy the maintenance crew can act on.",
    skills=["time-series features", "label engineering", "leakage", "time-based validation", "random forests", "precision–recall", "alert policies", "business case"],
    brief="""
**The situation.** A packaging plant runs 40 machines. When one breaks unexpectedly the line stops for a day, costing about **₹2,00,000**. An inspection costs **₹20,000** and fixes the problem if done in time. Each machine reports daily temperature, vibration and pressure.

The plant manager asks: *"Can you warn us a few days before a machine fails, without sending the crew on so many false alarms that they stop listening?"*

Time-series problems hide traps: labels that peek into the future, features that leak, and validation that accidentally trains on tomorrow. This project walks you past each one.
""",
    deliverable="a labelled, feature-engineered dataset, a model validated on later days, an alert policy (how many machines to inspect per day), and a business case in rupees.",
    data_notes="""
**machine_sensors.csv** — one row per machine per day, 40 machines × 240 days:

| Column | Meaning |
|---|---|
| machine_id | M01 … M40 |
| day | 1 … 240 |
| temperature, vibration, pressure | daily sensor averages |
| failure | 1 on the day the machine broke down |

Machines are repaired the same day and keep running.
""",
    setup="""
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score
sensors = load("machine_sensors.csv").sort_values(["machine_id", "day"]).reset_index(drop=True)
FEATURES = ["temperature", "vibration", "pressure", "vib_mean7", "temp_mean7", "vib_trend"]
print(sensors.shape, "failures:", sensors.failure.sum())


# Used by the checks: your functions chained together.
def prepared():
    return add_features(make_label(sensors))


def test_scores():
    train, test = time_split(prepared())
    model = train_model(train)
    return test.assign(prob=model.predict_proba(test[FEATURES])[:, 1])
""",
    explore=[("Look at one machine before modelling. What happens to vibration and temperature before a failure (red lines)?", """
m = sensors[sensors.machine_id == "M01"]
fig, ax = plt.subplots(2, 1, figsize=(10, 4), sharex=True)
ax[0].plot(m.day, m.vibration); ax[0].set_ylabel("vibration")
ax[1].plot(m.day, m.temperature, color="#b45309"); ax[1].set_ylabel("temperature")
for d in m.day[m.failure == 1]:
    for a in ax: a.axvline(d, color="red", alpha=0.5)
plt.show()
""")],
    milestones=[
        dict(title="Build the label: fails in the next 7 days?",
             task="""
We want to predict, at the end of each day, whether the machine will fail **in the next 7 days** (days d+1 … d+7, not today).

Write `make_label(df, horizon=7)` returning a copy of `df` with a `label` column (0/1). Work **within each machine** — one machine's failure must not label another machine's rows.
""",
             hint="For k in 1..horizon, `df.groupby('machine_id')['failure'].shift(-k)` looks k days ahead on the same machine. A row is positive if any of them is 1 (treat missing as 0).",
             starter="""
def make_label(df, horizon=7):
    raise NotImplementedError
""",
             solution="""
def make_label(df, horizon=7):
    out = df.copy()
    ahead = sum(out.groupby("machine_id")["failure"].shift(-k).fillna(0) for k in range(1, horizon + 1))
    out["label"] = (ahead > 0).astype(int)
    return out
""",
             call="[int(make_label(sensors)['label'].sum()), round(make_label(sensors)['label'].mean(), 4)]", tol=1e-9),
        dict(title="Features from the recent past",
             task="""
Write `add_features(df)` adding, per machine:
- `vib_mean7`, `temp_mean7`: mean of the **last 7 days including today** (`min_periods=1`),
- `vib_trend`: vibration today minus vibration 7 days ago (0 when there's no value 7 days ago).

Only use today and earlier — never future rows. The check reads machine M05's features on day 60.
""",
             hint="`df.groupby('machine_id')['vibration'].transform(lambda s: s.rolling(7, min_periods=1).mean())`.",
             starter="""
def add_features(df):
    raise NotImplementedError
""",
             solution="""
def add_features(df):
    out = df.copy()
    g = out.groupby("machine_id")
    out["vib_mean7"] = g["vibration"].transform(lambda s: s.rolling(7, min_periods=1).mean())
    out["temp_mean7"] = g["temperature"].transform(lambda s: s.rolling(7, min_periods=1).mean())
    out["vib_trend"] = (out["vibration"] - g["vibration"].shift(7)).fillna(0)
    return out
""",
             call="add_features(sensors).query('machine_id == \"M05\" and day == 60')[['vib_mean7', 'temp_mean7', 'vib_trend']].round(3).iloc[0].tolist()", tol=1e-6),
        dict(title="Validate on the future",
             task="""
A random split would let the model learn from day 200 to predict day 150. Instead split by time: **train = days 1–160, test = days 161–240**.

Write `time_split(df)` returning `(train, test)`. The check looks at their sizes and positive rates.
""",
             starter="""
def time_split(df):
    raise NotImplementedError
""",
             solution="""
def time_split(df):
    return df[df["day"] <= 160].copy(), df[df["day"] > 160].copy()
""",
             call="[len(time_split(prepared())[0]), len(time_split(prepared())[1]), round(time_split(prepared())[0]['label'].mean(), 4), round(time_split(prepared())[1]['label'].mean(), 4)]", tol=1e-9),
        dict(title="Train and measure the model",
             task="""
Write `train_model(train)` returning a fitted `RandomForestClassifier(n_estimators=200, max_depth=6, class_weight="balanced", random_state=0)` trained on `FEATURES` → `label`.

The check reports **average precision** (area under the precision–recall curve) on the test days. With rare positives (~8%) it's far more informative than accuracy: always predicting "no failure" is 92% accurate and useless.
""",
             starter="""
def train_model(train):
    raise NotImplementedError
""",
             solution="""
def train_model(train):
    model = RandomForestClassifier(n_estimators=200, max_depth=6, class_weight="balanced", random_state=0)
    return model.fit(train[FEATURES], train["label"])
""",
             call="round(average_precision_score(test_scores()['label'], test_scores()['prob']), 3)", tol=0.04,
             after="Compare with the base rate: a random ranking would score about the share of positives (≈0.08). How much better is yours?"),
        dict(title="An alert policy the crew can follow",
             task="""
The crew can inspect **3 machines per day**. Each test day, alert the 3 machines with the highest probability.

Write `alerts(scored, k=3)` returning `(number of alerts, precision)` where precision = share of alerts whose `label` is 1, rounded to 3.
""",
             hint="`scored.sort_values('prob', ascending=False).groupby('day').head(k)`",
             starter="""
def alerts(scored, k=3):
    raise NotImplementedError
""",
             solution="""
def alerts(scored, k=3):
    chosen = scored.sort_values(["day", "prob"], ascending=[True, False]).groupby("day").head(k)
    return len(chosen), round(chosen["label"].mean(), 3)
""",
             call="alerts(test_scores())", tol=0.06),
        dict(title="The business case",
             task="""
A failure is **caught** if its machine got at least one alert in the 7 days before it (days d−7 … d−1). Each caught failure saves ₹2,00,000; each alert costs ₹20,000 for the inspection.

Write `business_case(scored, k=3)` returning `(failures in test, caught, net saving in ₹)`.

Then try k = 1, 2, 3, 5. Which k gives the best net saving?
""",
             hint="Build the alert set as `{(machine_id, day)}`; for each failure row in the test period, check whether any `(machine, day - j)` for j in 1..7 is in the set.",
             starter="""
def business_case(scored, k=3):
    raise NotImplementedError
""",
             solution="""
def business_case(scored, k=3):
    chosen = scored.sort_values(["day", "prob"], ascending=[True, False]).groupby("day").head(k)
    alerted = set(zip(chosen["machine_id"], chosen["day"]))
    fails = scored[scored["failure"] == 1]
    caught = sum(any((m, d - j) in alerted for j in range(1, 8)) for m, d in zip(fails["machine_id"], fails["day"]))
    return len(fails), int(caught), int(caught * 200000 - len(chosen) * 20000)
""",
             call="business_case(test_scores())", tol=0.15,
             after="The policy is a trade-off you can now show in rupees: more inspections catch more failures but cost more. That chart — net saving vs k — is what convinces a plant manager."),
    ],
    present="""
Prepare a one-page note for the plant manager:

1. **Problem**: cost of a breakdown vs an inspection.
2. **What the model sees**: the warning signs (rising vibration and temperature) — include the machine chart.
3. **How we tested it**: trained on days 1–160, tested on 161–240, never on the future.
4. **Policy**: inspect the top k machines per day; failures caught, alerts raised, precision.
5. **Money**: net saving per 80 days, and per year.
6. **Next steps**: more sensors, per-machine baselines, a pilot on one line.
""",
    resume=[
        "Built a predictive-maintenance model on 9,600 machine-days of sensor data with leakage-safe labels and rolling features",
        "Validated on held-out future days (average precision **0.XX** vs a 0.08 base rate)",
        "Designed a top-k daily inspection policy catching **X of Y** failures, worth an estimated **₹Z** net saving per quarter",
    ],
    interview=[
        "How did you create the label, and what mistake would make it leak the future?",
        "Why not a random train/test split here?",
        "Why average precision and not accuracy or ROC AUC?",
        "How did you choose how many machines to inspect per day?",
        "One random vibration spike causes a false alarm. How would you make the model more robust?",
        "How would you deploy this so alerts arrive every morning?",
    ],
    extensions=[
        "Add features: rolling standard deviation, days since last failure, per-machine z-scores.",
        "Try gradient boosting and compare average precision on the same time split.",
        "Plot net saving against k (1–8) and mark the best value.",
        "Schedule the daily scoring with Airflow (see the Data Engineering course) and send alerts by email.",
    ],
)
