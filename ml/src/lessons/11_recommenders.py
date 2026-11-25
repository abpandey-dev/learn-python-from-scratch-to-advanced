from lib import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

R = np.array([[5, 3, 0, 1, 4],
              [4, 0, 0, 1, 5],
              [1, 1, 0, 5, 0],
              [0, 1, 5, 4, 0],
              [5, 4, 1, 0, 4]], dtype=float)

LESSON("Basics", "What a recommender does", """
<p>Netflix rows, Amazon's "customers also bought", Spotify's weekly mix: a <b>recommender</b> ranks items a user hasn't seen by how likely they are to want them. The data is a <b>user × item matrix</b> that is almost entirely empty — a typical user has touched far less than 1% of the catalogue.</p>
<ul>
<li><b>Explicit feedback</b>: star ratings. Clear but rare.</li>
<li><b>Implicit feedback</b>: clicks, plays, purchases, watch time. Plentiful but noisy — a missing click doesn't mean dislike.</li>
</ul>
<p>Always start with the <b>popularity baseline</b> (most-interacted items the user hasn't seen). It's surprisingly strong, and every smarter method has to beat it.</p>
""", practice=["Most Popular Unseen Items", "Cold Start Fallback"])


@LD
def matrix_picture():
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.imshow(R, cmap="Greens", vmin=0, vmax=5)
    for (i, j), v in np.ndenumerate(R):
        ax.text(j, i, "?" if v == 0 else int(v), ha="center", va="center")
    ax.set_xlabel("items")
    ax.set_ylabel("users")
    ax.set_title("Ratings: ? = unknown, to predict")


LESSON("Core", "Similarity: who is like whom", """
<p>Collaborative filtering rests on one idea: <b>people who agreed before will agree again</b>. To use it we need a similarity score.</p>
<table>
<tr><th>Measure</th><th>Formula</th><th>Use for</th></tr>
<tr><td>Cosine</td><td>a·b / (‖a‖ ‖b‖)</td><td>rating or count vectors</td></tr>
<tr><td>Pearson (mean-centred)</td><td>cosine after subtracting each user's mean</td><td>harsh vs generous raters</td></tr>
<tr><td>Jaccard</td><td>|A ∩ B| / |A ∪ B|</td><td>yes/no interactions</td></tr>
</table>
<p>Centring matters: a user who rates everything 4–5 and one who rates everything 1–2 may love the same films. After subtracting their means, their <i>preferences</i> line up even though their numbers don't.</p>
""", practice=["Cosine Similarity of Two Users", "Mean-Centred (Pearson) Similarity", "Jaccard Similarity for Clicks", "Most Similar Item", "k Nearest Items"])


@LD
def item_similarity():
    S = cosine_similarity(R.T)
    fig, ax = plt.subplots(figsize=(3.6, 3))
    ax.imshow(S, cmap="Blues", vmin=0, vmax=1)
    for (i, j), v in np.ndenumerate(S):
        ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=7)
    ax.set_title("item × item cosine similarity")


LESSON("Core", "User-based and item-based collaborative filtering", """
<p><b>User-based</b>: find the k users most similar to you who rated the item, and take their similarity-weighted average rating. <b>Item-based</b>: for each item you haven't seen, look at the items you <i>have</i> rated and weight your ratings by how similar those items are.</p>
<pre><code class="py">S = cosine_similarity(R.T)                      # item × item
scores = (S[:, rated] @ R[user, rated]) / S[:, rated].sum(axis=1)</code></pre>
<p>Item-based CF is usually preferred in production (Amazon popularised it): there are fewer items than users, item similarities change slowly so they can be computed overnight, and the result is easy to explain — "because you bought X".</p>
""", practice=["User-Based Rating Prediction", "Item-Based Recommendations", "Baseline Predictor With Biases"])

LESSON("Core", "Content-based and hybrid recommenders", """
<p><b>Content-based</b> methods recommend items whose <i>features</i> resemble what the user liked: genre, price, brand, or the words in a description (TF-IDF), or an embedding from a language model. They work for brand-new items with no ratings, but they can't surprise you — they only find more of the same.</p>
<p>The <b>cold-start problem</b>: a new user has no history, a new item has no ratings. Fixes: popularity for new users, content features for new items, asking a few onboarding questions. Real systems are <b>hybrids</b> that combine collaborative and content signals.</p>
""", practice=["Content-Based: Similar Descriptions", "Cold Start Fallback"])

LESSON("Advanced", "Matrix factorisation and modern systems", """
<p><b>Matrix factorisation</b> learns a short vector for each user and each item (say 50 numbers) so that their dot product ≈ the rating. The numbers become <b>latent factors</b> such as "how much action" or "how highbrow". The Netflix Prize was won largely with this. SVD gives the best low-rank approximation of a full matrix; for sparse ratings, methods like ALS or SGD fit only the known entries, with regularisation.</p>
<p>Large modern systems work in two stages: <b>candidate generation</b> (pull a few hundred items fast, often by nearest-neighbour search over embeddings — the same vector search used in RAG) and <b>ranking</b> (a gradient-boosted or neural model scores those candidates using many features), followed by business rules such as diversity and removing already-bought items.</p>
<p><b>Market-basket analysis</b> finds items bought together: support (how common), confidence P(B | A), and <b>lift</b> = confidence / P(B). Lift above 1 means A really raises the chance of B.</p>
""", practice=["Rank-1 Matrix Factorisation", "Frequently Bought Together", "Association Rule Metrics"])

LESSON("Advanced", "Evaluating recommenders", """
<p>Split by <b>time</b>: hold out each user's latest interactions and see if you'd have recommended them. Then measure:</p>
<ul>
<li><b>Rating accuracy</b>: RMSE — only for explicit ratings, and rarely what the business cares about.</li>
<li><b>Ranking quality</b>: precision@k, recall@k, hit rate, MRR (how high the first hit is), <b>NDCG</b> (graded relevance with a discount for lower positions).</li>
<li><b>Beyond accuracy</b>: coverage (how much of the catalogue gets recommended), diversity, novelty — a system that recommends only bestsellers can score well and still be useless.</li>
</ul>
<p>Offline metrics are only a filter; the final judge is an <b>online A/B test</b> on clicks, purchases or watch time.</p>
""", practice=["Precision@k and Recall@k", "NDCG@k", "Hit Rate and Mean Reciprocal Rank", "Leave-Last-Out Split", "Catalogue Coverage", "RMSE of Rating Predictions"])
