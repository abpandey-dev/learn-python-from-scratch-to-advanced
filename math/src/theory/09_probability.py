from lib import *

THEORY("Axioms and basic rules", """
<p>A probability P assigns a number to every event with: (1) P(A) ≥ 0, (2) P(sample space) = 1, (3) for mutually exclusive events P(A ∪ B) = P(A) + P(B). Everything else follows:</p>
<ul>
<li>P(∅) = 0, P(Aᶜ) = 1 − P(A), 0 ≤ P(A) ≤ 1.</li>
<li>Inclusion–exclusion: P(A ∪ B) = P(A) + P(B) − P(A ∩ B).</li>
<li>Interpretations: <b>classical</b> (equally likely outcomes), <b>frequentist</b> (long-run frequency), <b>Bayesian</b> (degree of belief).</li>
</ul>
""")

THEORY("Counting", """
<table>
<tr><th></th><th>Order matters</th><th>Order doesn't matter</th></tr>
<tr><td>Without repetition</td><td>P(n, k) = n!/(n − k)!</td><td>C(n, k) = n!/(k!(n − k)!)</td></tr>
<tr><td>With repetition</td><td>nᵏ</td><td>C(n + k − 1, k)</td></tr>
</table>
<p>Multinomial: arrangements of n items with groups of sizes k₁, k₂, … = n!/(k₁!k₂!…). Pascal's rule C(n, k) = C(n − 1, k − 1) + C(n − 1, k).</p>
""")

THEORY("Conditional probability, independence and Bayes", """
<ul>
<li>P(A | B) = P(A ∩ B)/P(B), for P(B) &gt; 0.</li>
<li>Chain rule: P(A ∩ B ∩ C) = P(A)·P(B | A)·P(C | A ∩ B).</li>
<li>Independence: P(A ∩ B) = P(A)P(B) ⇔ P(A | B) = P(A). Independent ≠ mutually exclusive (exclusive events with positive probability are dependent).</li>
<li>Law of total probability: P(B) = Σᵢ P(B | Aᵢ)P(Aᵢ) for a partition A₁, A₂, ….</li>
<li><b>Bayes</b>: P(A | B) = P(B | A)P(A)/P(B). Vocabulary: P(A) prior, P(B | A) likelihood, P(A | B) posterior, P(B) evidence.</li>
<li>Base-rate fallacy: ignoring a small prior makes a positive test seem far more conclusive than it is.</li>
</ul>
""")

THEORY("Random variables", """
<table>
<tr><th></th><th>Discrete</th><th>Continuous</th></tr>
<tr><td>Described by</td><td>PMF p(x) = P(X = x)</td><td>PDF f(x); P(a ≤ X ≤ b) = ∫ₐᵇ f</td></tr>
<tr><td>CDF</td><td colspan="2">F(x) = P(X ≤ x), rises from 0 to 1</td></tr>
<tr><td>E[X]</td><td>Σ x p(x)</td><td>∫ x f(x) dx</td></tr>
</table>
<ul>
<li>Linearity: E[aX + bY] = aE[X] + bE[Y] (always, even if dependent).</li>
<li>Var(aX + b) = a²Var(X); for independent X, Y: Var(X + Y) = Var X + Var Y.</li>
<li>Covariance Cov(X, Y) = E[XY] − E[X]E[Y]; independence ⇒ Cov = 0 (not the reverse).</li>
</ul>
""")

FAQ("What is the difference between independent and mutually exclusive?", "<p>Mutually exclusive events cannot both happen (rolling a 1 and a 6 on one die). Independent events don't affect each other's chances (two separate dice). If two events with positive probability are exclusive, they are dependent: knowing one happened tells you the other didn't.</p>")
FAQ("Explain Bayes' theorem simply.", "<p>It updates a prior belief with new evidence: posterior ∝ likelihood × prior. How likely the evidence is if the hypothesis were true, weighted by how plausible the hypothesis was before.</p>")
FAQ("Why is Naive Bayes called naive?", "<p>It assumes every feature (word) is independent of the others given the class, which is rarely true, yet it works well for text classification.</p>")
FAQ("Permutation vs combination?", "<p>Permutations count ordered arrangements (race podiums); combinations count unordered selections (lottery tickets). C(n, k) = P(n, k)/k!.</p>")
FAQ("What is expected value?", "<p>The probability-weighted average of all possible values — what you'd get on average if you repeated the experiment many times.</p>")
FAQ("Why do ML models output probabilities?", "<p>They let you choose a decision threshold, rank cases, combine with costs, and measure calibration — far more useful than a bare yes/no.</p>")
