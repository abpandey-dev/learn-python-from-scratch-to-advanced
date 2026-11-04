from lib import *

THEORY("Limits and continuity", """
<p>lim_{x→a} f(x) = L means f(x) gets arbitrarily close to L as x gets close to a (from both sides). f is <b>continuous</b> at a if lim_{x→a} f(x) = f(a) — no jumps or holes. Famous limits: lim (sin x)/x = 1 as x → 0; lim (1 + 1/n)ⁿ = e as n → ∞.</p>
""")

THEORY("The derivative", """
<p><b>f′(a) = lim_{h→0} (f(a + h) − f(a)) / h</b> — the slope of the tangent line, the instantaneous rate of change. Notation: f′(x), dy/dx, df/dx. A function with a corner (|x| at 0, ReLU at 0) is continuous but not differentiable there.</p>
<table>
<tr><th>Rule</th><th>Formula</th></tr>
<tr><td>Power</td><td>d/dx xⁿ = nxⁿ⁻¹</td></tr>
<tr><td>Exponential</td><td>d/dx eˣ = eˣ, d/dx aˣ = aˣ ln a</td></tr>
<tr><td>Logarithm</td><td>d/dx ln x = 1/x</td></tr>
<tr><td>Trig</td><td>sin′ = cos, cos′ = −sin</td></tr>
<tr><td>Linearity</td><td>(af + bg)′ = af′ + bg′</td></tr>
<tr><td>Product</td><td>(fg)′ = f′g + fg′</td></tr>
<tr><td>Quotient</td><td>(f/g)′ = (f′g − fg′)/g²</td></tr>
<tr><td>Chain</td><td>(f∘g)′(x) = f′(g(x))·g′(x)</td></tr>
</table>
""")

THEORY("Using derivatives", """
<ul>
<li><b>Tangent line</b> at a: y = f(a) + f′(a)(x − a) — the best straight-line approximation near a (linearisation).</li>
<li><b>Monotonicity</b>: f′ &gt; 0 increasing, f′ &lt; 0 decreasing.</li>
<li><b>Critical points</b>: f′ = 0 (or undefined). Second-derivative test: f″ &gt; 0 local min, f″ &lt; 0 local max, f″ = 0 inconclusive.</li>
<li><b>Convex</b> functions (f″ ≥ 0 everywhere) have no false valleys: any local minimum is global — why convex losses (MSE for linear regression, log-loss for logistic regression) are easy to train.</li>
<li><b>Taylor series</b>: f(x) ≈ f(a) + f′(a)(x − a) + f″(a)(x − a)²/2 + … — the basis of Newton's method.</li>
<li><b>Newton's method</b> for roots: xₙ₊₁ = xₙ − f(xₙ)/f′(xₙ); for minimums: xₙ₊₁ = xₙ − f′(xₙ)/f″(xₙ).</li>
</ul>
""")

THEORY("Integrals", """
<p>∫ₐᵇ f(x) dx = lim Σ f(xᵢ)Δx (Riemann sum) — signed area under the curve. The indefinite integral ∫ f dx = F(x) + C where F′ = f.</p>
<p><b>Fundamental Theorem of Calculus</b>: d/dx ∫ₐˣ f(t) dt = f(x) and ∫ₐᵇ f dx = F(b) − F(a).</p>
<table>
<tr><td>∫ xⁿ dx = xⁿ⁺¹/(n + 1) + C (n ≠ −1)</td><td>∫ 1/x dx = ln|x| + C</td></tr>
<tr><td>∫ eˣ dx = eˣ + C</td><td>average value = (1/(b − a)) ∫ₐᵇ f dx</td></tr>
</table>
<p>Numerical integration: left/right/midpoint rectangles (error ∝ Δx or Δx²), trapezoid (∝ Δx²), Simpson's rule (∝ Δx⁴).</p>
""")

FAQ("What is a derivative in one sentence?", "<p>The rate at which a function's output changes as its input changes, at a single point — the slope of the curve there.</p>")
FAQ("Why does machine learning need derivatives?", "<p>Training minimises a loss. The derivative (gradient) of the loss with respect to each weight says which way to nudge that weight to reduce the loss.</p>")
FAQ("What is the chain rule and why is it central to deep learning?", "<p>The derivative of a composition is the product of the derivatives of each stage. A network is a long composition, so backpropagation multiplies local derivatives from the output back to every weight.</p>")
FAQ("What is the relationship between derivatives and integrals?", "<p>They are inverse operations (Fundamental Theorem of Calculus): integrating a rate gives the total change; differentiating a running total gives the rate.</p>")
FAQ("Is ReLU differentiable?", "<p>Everywhere except at 0, where it has a corner. Frameworks simply use 0 (or 1) as the derivative there; it doesn't matter in practice.</p>")
FAQ("Forward vs central difference?", "<p>Forward (f(x + h) − f(x))/h has error proportional to h; central (f(x + h) − f(x − h))/2h has error proportional to h², so it is much more accurate for the same h.</p>")
