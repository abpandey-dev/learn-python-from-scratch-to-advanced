from lib import *

THEORY("Common distributions", """
<table>
<tr><th>Distribution</th><th>Support</th><th>PMF / PDF</th><th>Mean</th><th>Variance</th></tr>
<tr><td>Bernoulli(p)</td><td>{0, 1}</td><td>pᵏ(1 − p)¹⁻ᵏ</td><td>p</td><td>p(1 − p)</td></tr>
<tr><td>Binomial(n, p)</td><td>0 … n</td><td>C(n, k)pᵏ(1 − p)ⁿ⁻ᵏ</td><td>np</td><td>np(1 − p)</td></tr>
<tr><td>Geometric(p)</td><td>1, 2, …</td><td>(1 − p)ᵏ⁻¹p</td><td>1/p</td><td>(1 − p)/p²</td></tr>
<tr><td>Poisson(λ)</td><td>0, 1, …</td><td>λᵏe^(−λ)/k!</td><td>λ</td><td>λ</td></tr>
<tr><td>Uniform(a, b)</td><td>[a, b]</td><td>1/(b − a)</td><td>(a + b)/2</td><td>(b − a)²/12</td></tr>
<tr><td>Exponential(λ)</td><td>[0, ∞)</td><td>λe^(−λx)</td><td>1/λ</td><td>1/λ²</td></tr>
<tr><td>Normal(μ, σ²)</td><td>ℝ</td><td>e^(−(x−μ)²/2σ²)/(σ√2π)</td><td>μ</td><td>σ²</td></tr>
</table>
<p>The exponential distribution is <b>memoryless</b>: having waited 5 minutes doesn't change the distribution of the remaining wait. Poisson counts and exponential gaps describe the same random process.</p>
""")

THEORY("The normal distribution and limit theorems", """
<ul>
<li>Standard normal Z ~ N(0, 1); any X ~ N(μ, σ²) standardises as Z = (X − μ)/σ. Φ(z) = ½(1 + erf(z/√2)).</li>
<li>Key values: Φ(1) ≈ 0.8413, Φ(1.645) ≈ 0.95, Φ(1.96) ≈ 0.975, Φ(2.576) ≈ 0.995.</li>
<li>Sums of independent normals are normal: means add, variances add.</li>
<li><b>Law of large numbers</b>: the sample mean converges to the true mean as n grows.</li>
<li><b>Central limit theorem</b>: the mean of n independent samples with mean μ and variance σ² is approximately N(μ, σ²/n) for large n, whatever the original distribution.</li>
</ul>
""")

THEORY("Information theory", """
<table>
<tr><th>Quantity</th><th>Formula</th><th>Meaning</th></tr>
<tr><td>Self-information</td><td>−log p(x)</td><td>surprise of one outcome</td></tr>
<tr><td>Entropy</td><td>H(p) = −Σ p log p</td><td>average surprise; max for uniform (log n)</td></tr>
<tr><td>Cross-entropy</td><td>H(p, q) = −Σ p log q</td><td>average surprise when you believe q but reality is p</td></tr>
<tr><td>KL divergence</td><td>D(p‖q) = Σ p log(p/q) = H(p, q) − H(p)</td><td>≥ 0; = 0 iff p = q; not symmetric</td></tr>
<tr><td>Mutual information</td><td>I(X; Y) = H(X) − H(X | Y)</td><td>information Y gives about X (information gain)</td></tr>
</table>
<p>log₂ gives bits, ln gives nats. Minimising cross-entropy with respect to q is the same as minimising KL, because H(p) doesn't depend on q.</p>
""")

THEORY("Maximum likelihood and ML losses", """
<p>The <b>likelihood</b> L(θ) = Π f(xᵢ; θ) is how probable the data is under parameters θ; maximum-likelihood estimation picks the θ that maximises it (in practice, the log-likelihood, a sum). Results: Bernoulli p̂ = sample mean; normal μ̂ = sample mean, σ̂ = population std (divide by n).</p>
<table>
<tr><th>Assume the target is…</th><th>Negative log-likelihood becomes…</th><th>Used by</th></tr>
<tr><td>Normal around the prediction</td><td>mean squared error</td><td>linear regression</td></tr>
<tr><td>Bernoulli with probability σ(z)</td><td>binary cross-entropy (log-loss)</td><td>logistic regression</td></tr>
<tr><td>Categorical with probabilities softmax(z)</td><td>categorical cross-entropy</td><td>neural-network classifiers, LLMs</td></tr>
</table>
""")

FAQ("Why is the normal distribution so common?", "<p>Because of the central limit theorem: anything formed by adding many small independent effects (errors, heights, averages) is approximately normal.</p>")
FAQ("PDF vs probability?", "<p>For continuous variables the PDF is a density, not a probability — it can exceed 1. Probabilities are areas under it: P(a ≤ X ≤ b) = ∫ₐᵇ f.</p>")
FAQ("What is entropy in simple words?", "<p>How unpredictable something is, measured as the average number of yes/no questions needed to identify the outcome.</p>")
FAQ("Why is cross-entropy used as the classification loss?", "<p>It is the negative log-likelihood of the true labels under the model's predicted probabilities, it heavily punishes confident mistakes, and with softmax/sigmoid it gives simple, well-behaved gradients (p − y).</p>")
FAQ("Why subtract the maximum in softmax?", "<p>softmax(z) = softmax(z − c) for any constant c, and subtracting the max keeps every exponent ≤ 0, so e^z never overflows to infinity.</p>")
FAQ("Gini vs entropy in decision trees?", "<p>Both measure how mixed a node is and usually choose similar splits. Gini is slightly faster (no logarithm); entropy relates directly to information gain.</p>")
