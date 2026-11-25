import numpy as np
import pandas as pd


def make_data(rng):
    n = 12000
    variant = rng.choice(["control", "new_checkout"], n)
    device = rng.choice(["mobile", "desktop"], n, p=[0.65, 0.35])
    country = rng.choice(["IN", "AE", "SG", "UK"], n, p=[0.7, 0.12, 0.1, 0.08])
    users = pd.DataFrame({"user_id": [f"U{i:05d}" for i in range(n)], "variant": variant, "device": device, "country": country})
    events, orders = [], []
    for u, v, d in zip(users.user_id, variant, device):
        p_cart = 0.42 if d == "desktop" else 0.36
        p_check = 0.55
        if v == "new_checkout":
            p_buy = 0.60 if d == "mobile" else 0.60
        else:
            p_buy = 0.47 if d == "mobile" else 0.62
        events.append((u, "visit"))
        if rng.random() < p_cart:
            events.append((u, "cart"))
            if rng.random() < p_check:
                events.append((u, "checkout"))
                if rng.random() < p_buy:
                    events.append((u, "purchase"))
                    value = round(float(rng.lognormal(7.2, 0.5)), 2)
                    refund = rng.random() < (0.055 if v == "new_checkout" else 0.045)
                    orders.append((u, value, int(refund)))
    return {"ab_users.csv": users, "ab_events.csv": pd.DataFrame(events, columns=["user_id", "step"]),
            "ab_orders.csv": pd.DataFrame(orders, columns=["user_id", "order_value", "refunded"])}


PROJECT = dict(
    slug="checkout-ab-test",
    title="Checkout Redesign: A/B Test Readout",
    role="Product / Data Analyst",
    level="Intermediate",
    hours="5–7",
    summary="A product team tested a new one-page checkout on 12,000 users. Decide whether to ship it — with a funnel, significance test, confidence interval, segment and guardrail checks, and a power calculation.",
    skills=["A/B testing", "funnels", "sample ratio mismatch", "two-proportion z-test", "confidence intervals", "segments", "guardrail metrics", "power analysis"],
    brief="""
**The situation.** *ShopKart*'s product team redesigned checkout into a single page and ran an experiment: each visitor was randomly assigned to `control` (old checkout) or `new_checkout`. The experiment is over and the product manager asks: **"Should we ship it?"**

A good readout doesn't stop at "p < 0.05". You'll check the experiment was run properly, find where in the funnel the change acted, test significance, size the effect with a confidence interval, check it holds across devices, make sure it didn't harm a guardrail metric (refunds), and turn it into a clear recommendation.
""",
    deliverable="an experiment readout: validity check, funnel by variant, effect size with a 95% CI and p-value, device breakdown, guardrail check, a ship / don't-ship decision with reasons, and the sample size you'd need for a follow-up test.",
    data_notes="""
**ab_users.csv** — one row per user in the experiment: user_id, variant (`control` / `new_checkout`), device (`mobile` / `desktop`), country

**ab_events.csv** — funnel steps each user reached: user_id, step (`visit` → `cart` → `checkout` → `purchase`)

**ab_orders.csv** — one row per purchase: user_id, order_value (₹), refunded (1 = refunded)
""",
    setup="""
from scipy import stats
users = load("ab_users.csv")
events = load("ab_events.csv")
ab_orders = load("ab_orders.csv")
STEPS = ["visit", "cart", "checkout", "purchase"]
print(users.variant.value_counts().to_dict())
""",
    milestones=[
        dict(title="Was the split fair? (sample ratio mismatch)",
             task="""
Before reading any result, check the randomisation worked. With a 50/50 split, the two group sizes should differ only by chance. Write `srm(users)` returning a dict with each variant's user count and `p_value` from a chi-square goodness-of-fit test against an equal split (rounded to 4).

A tiny p-value (say < 0.001) means the split is broken and the results can't be trusted.
""",
             hint="`stats.chisquare(counts)` tests against equal expected counts by default.",
             starter="""
def srm(users):
    raise NotImplementedError
""",
             solution="""
def srm(users):
    counts = users["variant"].value_counts().sort_index()
    p = stats.chisquare(counts.values).pvalue
    return {**counts.to_dict(), "p_value": round(float(p), 4)}
""",
             call="srm(users)"),
        dict(title="Funnel by variant",
             task="""
Write `funnel(events, users)` returning `{variant: [users at visit, cart, checkout, purchase]}`. Count **distinct users** at each step.

Look at the numbers: at which step does the new checkout differ?
""",
             hint="Merge events with users to get the variant, then `groupby(['variant', 'step'])['user_id'].nunique()`.",
             starter="""
def funnel(events, users):
    raise NotImplementedError
""",
             solution="""
def funnel(events, users):
    e = events.merge(users[["user_id", "variant"]], on="user_id")
    counts = e.groupby(["variant", "step"])["user_id"].nunique().unstack()[STEPS]
    return {v: [int(x) for x in row] for v, row in counts.iterrows()}
""",
             call="funnel(events, users)", tol=1e-9),
        dict(title="Conversion and lift",
             task="""
The primary metric is **purchase conversion** = users who purchased ÷ users in the variant. Write `conversion(events, users)` returning a dict:
`{"control": rate %, "new_checkout": rate %, "lift_pp": difference in percentage points, "lift_rel_pct": relative lift %}`, all rounded to 2.
""",
             hint="Users who purchased: `set(events[events.step == 'purchase'].user_id)`; flag them in `users` and take the mean per variant.",
             starter="""
def conversion(events, users):
    raise NotImplementedError
""",
             solution="""
def conversion(events, users):
    buyers = set(events.loc[events["step"] == "purchase", "user_id"])
    rate = users.assign(bought=users["user_id"].isin(buyers)).groupby("variant")["bought"].mean() * 100
    c, t = rate["control"], rate["new_checkout"]
    return {"control": round(c, 2), "new_checkout": round(t, 2), "lift_pp": round(t - c, 2), "lift_rel_pct": round((t - c) / c * 100, 2)}
""",
             call="conversion(events, users)"),
        dict(title="Is it significant? z-test and confidence interval",
             task="""
Write `z_and_ci(events, users)` returning `(z, p_value, ci_low, ci_high)`:
- `z`, `p_value`: two-sided **two-proportion z-test** using the pooled rate (rounded to 4),
- `ci_low`, `ci_high`: 95% confidence interval for (new − control) in **percentage points**, using the unpooled standard error (rounded to 2).
""",
             hint="Pooled p̂ = all buyers ÷ all users; SE = √(p̂(1−p̂)(1/n₁+1/n₂)). For the CI, SE = √(p₁(1−p₁)/n₁ + p₂(1−p₂)/n₂) and multiply by `stats.norm.ppf(0.975)`.",
             starter="""
def z_and_ci(events, users):
    raise NotImplementedError
""",
             solution="""
def z_and_ci(events, users):
    buyers = set(events.loc[events["step"] == "purchase", "user_id"])
    g = users.assign(b=users["user_id"].isin(buyers)).groupby("variant")["b"].agg(["sum", "count"])
    x1, n1 = g.loc["control"]
    x2, n2 = g.loc["new_checkout"]
    p1, p2 = x1 / n1, x2 / n2
    p = (x1 + x2) / (n1 + n2)
    z = (p2 - p1) / math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    pval = 2 * stats.norm.sf(abs(z))
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    zc = stats.norm.ppf(0.975)
    d = (p2 - p1) * 100
    return (round(z, 4), round(float(pval), 4), round(d - zc * se * 100, 2), round(d + zc * se * 100, 2))
""",
             call="z_and_ci(events, users)", tol=2e-3),
        dict(title="Does it hold on every device?",
             task="""
An average can hide opposite effects. Write `lift_by_device(events, users)` returning `{device: lift in percentage points}` (new − control conversion, rounded to 2).

What do you see? What would you tell the team?
""",
             starter="""
def lift_by_device(events, users):
    raise NotImplementedError
""",
             solution="""
def lift_by_device(events, users):
    buyers = set(events.loc[events["step"] == "purchase", "user_id"])
    rate = users.assign(b=users["user_id"].isin(buyers)).groupby(["device", "variant"])["b"].mean() * 100
    return {d: round(rate[d]["new_checkout"] - rate[d]["control"], 2) for d in sorted(users["device"].unique())}
""",
             call="lift_by_device(events, users)",
             after="The new page helps mobile a lot and does nothing (or slightly harms) desktop. That's a finding worth more than the overall p-value: you might ship to mobile first and investigate desktop."),
        dict(title="Guardrail: did refunds go up?",
             task="""
A change that sells more but causes more refunds may not be a win. Write `refund_guardrail(ab_orders, users)` returning `{"control": refund rate %, "new_checkout": refund rate %, "p_value": two-proportion z-test p}` — rates rounded to 2, p to 4. Refund rate = refunded orders ÷ orders.
""",
             starter="""
def refund_guardrail(ab_orders, users):
    raise NotImplementedError
""",
             solution="""
def refund_guardrail(ab_orders, users):
    o = ab_orders.merge(users[["user_id", "variant"]], on="user_id")
    g = o.groupby("variant")["refunded"].agg(["sum", "count"])
    x1, n1 = g.loc["control"]
    x2, n2 = g.loc["new_checkout"]
    p = (x1 + x2) / (n1 + n2)
    z = (x2 / n2 - x1 / n1) / math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    return {"control": round(x1 / n1 * 100, 2), "new_checkout": round(x2 / n2 * 100, 2),
            "p_value": round(float(2 * stats.norm.sf(abs(z))), 4)}
""",
             call="refund_guardrail(ab_orders, users)", tol=2e-3),
        dict(title="Make the call",
             task="""
Write `decide(srm_p, p_value, ci_low, refund_p, refund_up)` that returns one of:
- `"invalid test"` if the split is broken (`srm_p < 0.001`),
- `"don't ship"` if refunds rose significantly (`refund_up` and `refund_p < 0.05`),
- `"ship"` if the result is significant (`p_value < 0.05`) **and** the whole CI is above zero (`ci_low > 0`),
- otherwise `"keep testing"`.

The check runs it on your real numbers and on a few made-up cases.
""",
             starter="""
def decide(srm_p, p_value, ci_low, refund_p, refund_up):
    raise NotImplementedError
""",
             solution="""
def decide(srm_p, p_value, ci_low, refund_p, refund_up):
    if srm_p < 0.001:
        return "invalid test"
    if refund_up and refund_p < 0.05:
        return "don't ship"
    if p_value < 0.05 and ci_low > 0:
        return "ship"
    return "keep testing"
""",
             call="[decide(srm(users)['p_value'], z_and_ci(events, users)[1], z_and_ci(events, users)[2], refund_guardrail(ab_orders, users)['p_value'], refund_guardrail(ab_orders, users)['new_checkout'] > refund_guardrail(ab_orders, users)['control']), decide(0.0001, 0.01, 1, 0.5, False), decide(0.4, 0.01, 0.5, 0.02, True), decide(0.4, 0.2, -0.3, 0.6, False)]",
             tol=1e-9),
        dict(title="Plan the follow-up test",
             task="""
The team wants a desktop-only follow-up. Write `users_needed(base_rate, lift_pp, alpha=0.05, power=0.8)` returning the users needed **per group** to detect an absolute lift of `lift_pp` percentage points from `base_rate` (a fraction), rounded up:

n = (z₁₋α/₂ + z_power)² × (p₁(1−p₁) + p₂(1−p₂)) / (p₂ − p₁)²
""",
             starter="""
def users_needed(base_rate, lift_pp, alpha=0.05, power=0.8):
    raise NotImplementedError
""",
             solution="""
def users_needed(base_rate, lift_pp, alpha=0.05, power=0.8):
    p1, p2 = base_rate, base_rate + lift_pp / 100
    z = stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(power)
    return math.ceil(z ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / (p2 - p1) ** 2)
""",
             call="[users_needed(0.13, 1), users_needed(0.13, 2), users_needed(0.13, 1, power=0.9)]", tol=1e-9,
             after="Halving the effect you want to detect roughly **quadruples** the users you need. That's why teams agree the minimum effect worth detecting *before* the test."),
    ],
    extra=[("## A chart for the readout", """
import matplotlib.pyplot as plt
e = events.merge(users[["user_id", "variant"]], on="user_id")
f = e.groupby(["step", "variant"])["user_id"].nunique().unstack().loc[STEPS]
(f / f.loc["visit"] * 100).plot(kind="bar", figsize=(7, 3), color=["#94a3b8", "#0f766e"])
plt.ylabel("% of visitors"); plt.title("The new checkout wins at the last step"); plt.xticks(rotation=0); plt.show()
""")],
    present="""
Write the readout as you'd post it to the product team (half a page):

1. **Decision** first: ship / don't ship / keep testing, in one line.
2. **Validity**: the split was fair (SRM p-value).
3. **Result**: conversion control vs new, lift in pp and %, 95% CI, p-value.
4. **Where it acted**: the funnel step, and the device breakdown.
5. **Guardrail**: refunds.
6. **Next steps**: e.g. ship to mobile, follow-up desktop test with N users per group.
""",
    resume=[
        "Analysed a 12,000-user checkout A/B test end to end: randomisation check, funnel, z-test and 95% CI",
        "Found a **+X pp** conversion lift driven entirely by mobile, recommending a mobile-first rollout",
        "Sized a follow-up experiment (**N** users per group for 80% power) and defined a refund guardrail",
    ],
    interview=[
        "What is a sample ratio mismatch and why check it first?",
        "Explain your p-value and confidence interval to a product manager without jargon.",
        "The overall lift is positive but desktop is flat. What would you do?",
        "Why shouldn't you check the p-value every day and stop when it's significant?",
        "How did you decide the experiment needed N users? What happens if you want to detect half the effect?",
        "What guardrail metrics would you add for a checkout change?",
    ],
    extensions=[
        "Compare average order value between variants with a t-test or bootstrap (it's skewed — which is better?).",
        "Do a Bayesian analysis: the probability that the new checkout is better, using Beta posteriors.",
        "Check for a novelty effect: does the lift shrink if you split users by when they arrived?",
        "Build a reusable `ab_readout()` function that prints the whole report for any experiment.",
    ],
)
