from lib import *

THEORY("Families of recommenders", """
<table>
<tr><th>Approach</th><th>Uses</th><th>Strength</th><th>Weakness</th></tr>
<tr><td>Popularity</td><td>counts</td><td>simple, strong baseline</td><td>not personal</td></tr>
<tr><td>User-based CF</td><td>similar users</td><td>intuitive</td><td>many users, sparse overlap</td></tr>
<tr><td>Item-based CF</td><td>similar items</td><td>stable, explainable</td><td>new items</td></tr>
<tr><td>Content-based</td><td>item features</td><td>handles new items</td><td>over-specialises</td></tr>
<tr><td>Matrix factorisation</td><td>latent factors</td><td>accurate, compact</td><td>cold start, less explainable</td></tr>
<tr><td>Two-stage neural</td><td>embeddings + ranker</td><td>scales to billions</td><td>complex</td></tr>
</table>
""")

THEORY("Ranking metrics", """
<table>
<tr><th>Metric</th><th>Formula</th></tr>
<tr><td>Precision@k</td><td>relevant in top k ÷ k</td></tr>
<tr><td>Recall@k</td><td>relevant in top k ÷ all relevant</td></tr>
<tr><td>Hit rate@k</td><td>share of users with ≥ 1 relevant in top k</td></tr>
<tr><td>MRR</td><td>mean of 1 / rank of the first relevant item</td></tr>
<tr><td>DCG@k</td><td>Σ relᵢ / log₂(i + 1), i = 1..k</td></tr>
<tr><td>NDCG@k</td><td>DCG@k ÷ DCG@k of the ideal order</td></tr>
</table>
""")

THEORY("Association rules", """
<ul>
<li><b>Support</b>(A→B) = P(A ∧ B)</li>
<li><b>Confidence</b>(A→B) = P(B | A) = support(A ∧ B) / support(A)</li>
<li><b>Lift</b>(A→B) = confidence / P(B); 1 = independent, &gt; 1 = A raises the chance of B</li>
</ul>
<p>The Apriori algorithm only grows itemsets whose subsets are already frequent, because support can only shrink as sets grow.</p>
""")

FAQ("User-based or item-based CF?", "<p>Item-based is usually more practical: item–item similarities are fewer, more stable and can be precomputed, and recommendations are easy to explain.</p>")
FAQ("How do you handle cold start?", "<p>Popular or trending items and short onboarding questions for new users; content features or embeddings for new items; and exploration (showing new items to some users) to collect data.</p>")
FAQ("Why not just optimise RMSE?", "<p>Users see a ranked list, not predicted stars. Ranking metrics (NDCG, recall@k) and online business metrics matter more; a model can have lower RMSE and still rank worse.</p>")
FAQ("What is implicit feedback and why is it tricky?", "<p>Behaviour such as clicks and plays. It's abundant, but you only observe positives — an unclicked item might be disliked or simply unseen — so missing values can't be treated as negatives without care.</p>")
FAQ("How do large platforms serve recommendations quickly?", "<p>Two stages: fast candidate generation using approximate nearest-neighbour search over embeddings, then a heavier ranking model on a few hundred candidates, with caching of precomputed results.</p>")
FAQ("What is popularity bias?", "<p>Popular items get recommended more, so they get more interactions, so they get recommended even more. It hurts diversity and new items; counter it with re-ranking for diversity and exploration.</p>")
