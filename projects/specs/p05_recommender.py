import numpy as np
import pandas as pd

WORDS = {
    "Electronics": ["wireless", "earbuds", "charger", "smart", "speaker", "cable", "power", "bank", "watch", "keyboard"],
    "Kitchen": ["steel", "pan", "nonstick", "bottle", "mixer", "knife", "set", "tiffin", "kettle", "jar"],
    "Books": ["python", "novel", "thriller", "history", "guide", "data", "poems", "cookbook", "kids", "science"],
    "Fitness": ["yoga", "mat", "dumbbell", "resistance", "band", "shaker", "protein", "running", "shoes", "rope"],
    "Beauty": ["herbal", "face", "wash", "serum", "sunscreen", "lip", "balm", "hair", "oil", "kajal"],
}


def make_data(rng):
    cats = list(WORDS)
    n_items, n_users, dim = 150, 400, 5
    item_cat = rng.choice(len(cats), n_items)
    item_vec = rng.normal(0, 0.4, (n_items, dim))
    item_vec[np.arange(n_items), item_cat] += 1.5
    pop = rng.gamma(1.2, 1.0, n_items)
    items = pd.DataFrame({
        "item_id": [f"I{i:03d}" for i in range(n_items)],
        "category": [cats[c] for c in item_cat],
        "title": [" ".join(rng.choice(WORDS[cats[c]], 3, replace=False)) for c in item_cat],
        "price": np.round(rng.uniform(99, 2999, n_items), 0),
    })
    rows = []
    for u in range(n_users):
        taste = rng.normal(0, 0.3, dim)
        taste[rng.choice(dim, 2, replace=False)] += rng.uniform(0.8, 1.6, 2)
        score = item_vec @ taste + 0.35 * np.log(pop)
        p = np.exp(score * 2.2)
        p /= p.sum()
        n = int(rng.integers(4, 40))
        chosen = rng.choice(n_items, n, replace=False, p=p)
        ts = np.sort(rng.integers(1, 365, n))
        for it, t in zip(chosen, ts):
            rows.append((f"U{u:03d}", f"I{it:03d}", int(t)))
    return {"rec_interactions.csv": pd.DataFrame(rows, columns=["user_id", "item_id", "day"]),
            "rec_items.csv": items}


PROJECT = dict(
    slug="store-recommender",
    title="\"You Might Also Like\": A Store Recommender",
    role="ML Engineer",
    level="Intermediate",
    hours="7–9",
    summary="Build the recommendations widget for an online store: a popularity baseline, item-based collaborative filtering, content-based similar items for new products, a hybrid, and an honest offline evaluation.",
    skills=["implicit feedback", "leave-last-out evaluation", "hit rate", "item-item collaborative filtering", "cosine similarity", "TF-IDF", "cold start", "coverage"],
    brief="""
**The situation.** *ShopKart* wants a "You might also like" row on every customer's home page. You have a year of purchase history: 400 customers, 150 products. The product manager asks:

1. Can we beat simply showing the bestsellers?
2. What do we show a brand-new product that nobody has bought yet?
3. What do we show a customer who has bought almost nothing?
4. Why was a product recommended (so we can show "Because you bought …")?

You'll build each piece and measure it the way recommendation teams do: hide each customer's latest purchase and check whether your top 10 would have found it.
""",
    deliverable="a popularity baseline, an item-based collaborative-filtering recommender, content-based similar items, a hybrid with a cold-start rule, hit-rate and coverage results for each, and an explanation feature.",
    data_notes="""
**rec_interactions.csv** — one row per purchase: user_id, item_id, day (1–365). Implicit feedback: a purchase means interest; no purchase doesn't mean dislike.

**rec_items.csv** — item_id, category, title (a few words), price (₹)
""",
    setup="""
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
inter = load("rec_interactions.csv")
items = load("rec_items.csv")
K = 10


# Used by the checks: hit rate@K of a recommender over the held-out purchases.
def hit_rate(make_recommender):
    train, test = leave_last_out(inter)
    recommend = make_recommender(train)
    hits = [row.item_id in recommend(row.user_id, K) for row in test.itertuples()]
    return round(float(np.mean(hits)), 3)


def coverage(make_recommender):
    # % of the catalogue that appears in at least one test user's top K
    train, test = leave_last_out(inter)
    rec = make_recommender(train)
    shown = {i for u in test["user_id"] for i in rec(u, K)}
    return round(len(shown) / inter["item_id"].nunique() * 100, 1)
""",
    milestones=[
        dict(title="How sparse is the data?",
             task="""
Write `data_stats(inter)` returning `[sparsity %, median purchases per user, share of purchases going to the top 10% of items (%)]`, each rounded to 1. Sparsity = % of the user × item grid with **no** purchase.
""",
             starter="""
def data_stats(inter):
    raise NotImplementedError
""",
             solution="""
def data_stats(inter):
    users, products = inter["user_id"].nunique(), inter["item_id"].nunique()
    sparsity = (1 - len(inter) / (users * products)) * 100
    per_user = inter.groupby("user_id").size().median()
    counts = inter["item_id"].value_counts()
    top = counts.head(math.ceil(len(counts) * 0.1)).sum() / counts.sum() * 100
    return [round(sparsity, 1), round(float(per_user), 1), round(top, 1)]
""",
             call="data_stats(inter)"),
        dict(title="Hold out each customer's latest purchase",
             task="""
Write `leave_last_out(inter)` returning `(train, test)`: for every user with **at least 5** purchases, their latest purchase (highest `day`; on ties, the last row) goes to `test`; everything else is `train`.
""",
             hint="Sort by `['user_id', 'day']`, take `groupby('user_id').tail(1)` for users whose count ≥ 5, and drop those rows' index from the data.",
             starter="""
def leave_last_out(inter):
    raise NotImplementedError
""",
             solution="""
def leave_last_out(inter):
    df = inter.sort_values(["user_id", "day"], kind="stable")
    counts = df.groupby("user_id")["item_id"].transform("size")
    test = df[counts >= 5].groupby("user_id").tail(1)
    return df.drop(index=test.index), test
""",
             call="[len(leave_last_out(inter)[0]), len(leave_last_out(inter)[1])]", tol=1e-9),
        dict(title="Baseline: bestsellers",
             task="""
Write `popular_recommender(train)` that **returns a function** `recommend(user_id, k)`. It recommends the k most-bought items in `train` that this user hasn't bought (ties: smaller item_id first).

The check reports hit rate@10: the share of held-out purchases that appear in the user's top 10.
""",
             hint="Count once outside the inner function: `order = train.item_id.value_counts()` then sort by (−count, item_id). Inside, skip items in the user's set.",
             starter="""
def popular_recommender(train):
    def recommend(user_id, k):
        raise NotImplementedError
    return recommend
""",
             solution="""
def popular_recommender(train):
    counts = train["item_id"].value_counts()
    order = sorted(counts.index, key=lambda i: (-counts[i], i))
    seen = train.groupby("user_id")["item_id"].apply(set).to_dict()

    def recommend(user_id, k):
        mine = seen.get(user_id, set())
        return [i for i in order if i not in mine][:k]
    return recommend
""",
             call="hit_rate(popular_recommender)"),
        dict(title="Item-based collaborative filtering",
             task="""
Write `item_cf_recommender(train)` returning `recommend(user_id, k)`:
1. Build a user × item 0/1 matrix from `train` (`pd.crosstab(...).clip(upper=1)`).
2. Item–item similarity = cosine similarity of the item columns.
3. A user's score for item j = Σ similarity(j, i) over items i they bought.
4. Recommend the top k unbought items by score (ties: smaller item_id first).

Does it beat the bestsellers?
""",
             hint="`S = cosine_similarity(M.T.values)`; scores for a user = `S[:, bought_idx].sum(axis=1)`. Use `np.lexsort((item_ids, -scores))` for a stable tie-break.",
             starter="""
def item_cf_recommender(train):
    def recommend(user_id, k):
        raise NotImplementedError
    return recommend
""",
             solution="""
def item_cf_recommender(train):
    M = pd.crosstab(train["user_id"], train["item_id"]).clip(upper=1)
    ids = M.columns.to_numpy()
    S = cosine_similarity(M.T.values)
    np.fill_diagonal(S, 0)

    def recommend(user_id, k):
        if user_id not in M.index:
            return []
        bought = M.loc[user_id].to_numpy() > 0
        scores = S[:, bought].sum(axis=1)
        order = np.lexsort((ids, -scores))
        return [ids[j] for j in order if not bought[j]][:k]
    return recommend
""",
             call="hit_rate(item_cf_recommender)", tol=0.02),
        dict(title="New products: content-based similar items",
             task="""
A new product has no purchases, so collaborative filtering can't recommend it. Use its text instead. Write `similar_items(items, item_id, n=3)` returning the ids of the n most similar items by cosine similarity of **TF-IDF** vectors of `category + " " + title` (excluding the item itself; ties: smaller id first).
""",
             starter="""
def similar_items(items, item_id, n=3):
    raise NotImplementedError
""",
             solution="""
def similar_items(items, item_id, n=3):
    text = items["category"] + " " + items["title"]
    X = TfidfVectorizer().fit_transform(text)
    i = items.index[items["item_id"] == item_id][0]
    sims = cosine_similarity(X[i], X).ravel()
    sims[i] = -1
    order = np.lexsort((items["item_id"].to_numpy(), -np.round(sims, 12)))
    return items["item_id"].to_numpy()[order][:n].tolist()
""",
             call="[similar_items(items, 'I007'), similar_items(items, 'I042')]", tol=1e-9),
        dict(title="A hybrid with a cold-start rule",
             task="""
Customers with few purchases give CF little to work with. Write `hybrid_recommender(train, min_items=6)`: use item-CF for users with at least `min_items` purchases in `train`, and bestsellers otherwise.

The check reports `[hit rate, catalogue coverage %]` where coverage = % of all items that appear in at least one test user's top 10.
""",
             starter="""
def hybrid_recommender(train, min_items=6):
    def recommend(user_id, k):
        raise NotImplementedError
    return recommend
""",
             solution="""
def hybrid_recommender(train, min_items=6):
    cf, pop = item_cf_recommender(train), popular_recommender(train)
    sizes = train.groupby("user_id").size()

    def recommend(user_id, k):
        return cf(user_id, k) if sizes.get(user_id, 0) >= min_items else pop(user_id, k)
    return recommend

""",
             call="[hit_rate(hybrid_recommender), coverage(hybrid_recommender)]", tol=0.03,
             after="Here the hybrid's hit rate is a little *below* pure item-CF: every test user already has at least 4 purchases, so CF has something to work with. The rule earns its place with truly new customers, who have no history at all. Compare coverage with `coverage(popular_recommender)`: bestsellers show the same few items to everyone. Report trade-offs like this honestly — it's what senior reviewers look for."),
        dict(title="\"Because you bought …\"",
             task="""
Explanations build trust. Write `because_you_bought(train, user_id, item_id)` returning the item **this user bought** that is most similar (item-CF cosine) to the recommended `item_id` — that's the item to show in "Because you bought X".
""",
             starter="""
def because_you_bought(train, user_id, item_id):
    raise NotImplementedError
""",
             solution="""
def because_you_bought(train, user_id, item_id):
    M = pd.crosstab(train["user_id"], train["item_id"]).clip(upper=1)
    S = pd.DataFrame(cosine_similarity(M.T.values), index=M.columns, columns=M.columns)
    bought = sorted(M.columns[M.loc[user_id] > 0])
    return max(bought, key=lambda i: (round(S.loc[item_id, i], 12), -int(i[1:])))
""",
             call="[because_you_bought(leave_last_out(inter)[0], u, item_cf_recommender(leave_last_out(inter)[0])(u, 1)[0]) for u in ['U001', 'U010', 'U100']]", tol=1e-9),
    ],
    present="""
Write a short design note for the product manager:

1. **Results table**: hit rate@10 and coverage for bestsellers, item-CF and hybrid.
2. **What ships**: the hybrid, and the rule for new customers.
3. **New products**: content-based similar items until they collect purchases.
4. **Explanations**: example "Because you bought" lines for 3 customers.
5. **How to confirm online**: an A/B test on clicks and purchases from the widget.
""",
    resume=[
        "Built an item-based collaborative-filtering recommender for 400 users × 150 products from implicit purchase data",
        "Improved hit rate@10 from **X%** (bestsellers) to **Y%** with leave-last-out evaluation, and raised catalogue coverage to **Z%**",
        "Added TF-IDF similar-item recommendations for cold-start products and \"Because you bought\" explanations",
    ],
    interview=[
        "Why evaluate by hiding the latest purchase rather than a random one?",
        "What is implicit feedback, and why can't you treat unbought items as dislikes?",
        "Item-based vs user-based collaborative filtering — why did you choose item-based?",
        "How do you handle a new user? A new product?",
        "Hit rate went up. Why might the A/B test still disappoint?",
        "How would this scale to 10 million users and 1 million products?",
    ],
    extensions=[
        "Add matrix factorisation (implicit ALS or truncated SVD) and compare hit rate.",
        "Re-rank for diversity: at most 4 items per category in the top 10.",
        "Weight recent purchases more than old ones.",
        "Serve recommendations from an API and cache them per user (see project 7).",
    ],
)
