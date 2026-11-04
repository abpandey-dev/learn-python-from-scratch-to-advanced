from lib import *

THEORY("Definition", """
<p>A <b>function</b> f from a set X (the <b>domain</b>) to a set Y assigns to every x in X exactly one f(x) in Y. The set of outputs actually produced is the <b>range</b>. Graphically: any vertical line meets the graph at most once (the vertical line test).</p>
<ul>
<li><b>One-to-one</b> (injective): different inputs give different outputs — only these have an inverse.</li>
<li><b>Inverse</b> f⁻¹ undoes f: f⁻¹(f(x)) = x. Its graph is f's mirrored in the line y = x.</li>
<li><b>Composition</b> (f ∘ g)(x) = f(g(x)) — apply g first.</li>
</ul>
""")

THEORY("Families of functions", """
<table>
<tr><th>Family</th><th>Formula</th><th>Shape</th><th>Seen in ML as</th></tr>
<tr><td>Linear</td><td>mx + c</td><td>straight line</td><td>linear regression, a neuron before activation</td></tr>
<tr><td>Quadratic</td><td>ax² + bx + c</td><td>parabola</td><td>squared-error loss</td></tr>
<tr><td>Polynomial</td><td>aₙxⁿ + … + a₀</td><td>wiggles (≤ n − 1 turns)</td><td>polynomial features</td></tr>
<tr><td>Exponential</td><td>a·bˣ, eˣ</td><td>explodes or decays</td><td>softmax, growth models</td></tr>
<tr><td>Logarithmic</td><td>log_b x</td><td>slow growth</td><td>log-loss, log transforms</td></tr>
<tr><td>Sigmoid / tanh</td><td>1/(1+e⁻ˣ)</td><td>S-curve</td><td>logistic regression, gates</td></tr>
<tr><td>Piecewise</td><td>different rule per interval</td><td>corners</td><td>ReLU, decision trees</td></tr>
</table>
""")

THEORY("Lines", """
<ul>
<li>Slope m = Δy/Δx = (y₂ − y₁)/(x₂ − x₁); slope-intercept form y = mx + c; point-slope form y − y₁ = m(x − x₁).</li>
<li>Parallel lines have equal slopes; perpendicular lines have m₁·m₂ = −1.</li>
<li>The <b>average rate of change</b> of any f on [a, b] is the slope of the line through (a, f(a)) and (b, f(b)) — the doorway to derivatives.</li>
</ul>
""")

THEORY("Exponentials and logarithms", """
<p>y = bˣ ⇔ x = log_b y. Natural log ln = log_e, where e = lim (1 + 1/n)ⁿ ≈ 2.71828.</p>
<table>
<tr><td>log_b(xy) = log_b x + log_b y</td><td>log_b(x/y) = log_b x − log_b y</td></tr>
<tr><td>log_b(xⁿ) = n log_b x</td><td>log_b x = ln x / ln b (change of base)</td></tr>
<tr><td>log_b 1 = 0, log_b b = 1</td><td>log is only defined for x &gt; 0</td></tr>
</table>
""")

THEORY("Transformations and symmetry", """
<p>g(x) = a·f(b(x − h)) + k: shift right h, up k, stretch vertically by a (reflect if a &lt; 0), compress horizontally by b. <b>Even</b> functions satisfy f(−x) = f(x) (mirror in the y-axis, e.g. x², cos x); <b>odd</b> functions satisfy f(−x) = −f(x) (rotational symmetry, e.g. x³, sin x, tanh x).</p>
""")

FAQ("Is every equation a function?", "<p>No. x² + y² = 1 (a circle) gives two y values for most x, so y is not a function of x.</p>")
FAQ("Why is a machine-learning model called a function?", "<p>It maps each input (features) to one output (prediction). Training searches over a family of functions (e.g. all lines y = mx + c) for the one with the smallest error.</p>")
FAQ("Why use logarithms on data?", "<p>They compress large ranges, turn multiplicative effects into additive ones, and make right-skewed data (incomes, prices) more symmetric, which many models prefer.</p>")
FAQ("Why do neural networks need non-linear activations?", "<p>A composition of linear functions is still linear, so without activations a deep network could only draw straight lines. Non-linearities like ReLU let it model curves.</p>")
FAQ("What does slope mean in real life?", "<p>A rate: price per square metre, km per hour, extra marks per hour studied. It is how much the output changes per unit of input.</p>")
