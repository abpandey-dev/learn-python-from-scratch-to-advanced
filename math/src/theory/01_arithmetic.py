from lib import *

THEORY("Which math does data science and machine learning need?", """
<p>You do <b>not</b> need a math degree. You need five areas, and this course teaches them in this order because each one is built from the ones before it:</p>
<table>
<tr><th>#</th><th>Area</th><th>What it gives you in ML</th><th>Topics here</th></tr>
<tr><td>1</td><td><b>Foundations</b>: arithmetic, algebra, functions</td><td>reading and rearranging every formula; understanding a model as a function from inputs to outputs</td><td>1 – 3</td></tr>
<tr><td>2</td><td><b>Linear algebra</b>: vectors, matrices, eigenvectors</td><td>data is stored as vectors and matrices; a neural network layer is a matrix multiply; PCA and embeddings come from eigenvectors</td><td>4 – 6</td></tr>
<tr><td>3</td><td><b>Calculus</b>: derivatives, integrals, gradients</td><td>training = adjusting weights to make the error smaller, using derivatives (gradient descent, backpropagation)</td><td>7 – 8</td></tr>
<tr><td>4</td><td><b>Probability</b></td><td>reasoning under uncertainty; Naive Bayes; predictions as probabilities</td><td>9</td></tr>
<tr><td>5</td><td><b>Distributions &amp; information</b></td><td>the normal curve, likelihood, and the loss functions (cross-entropy, log-loss) models minimise</td><td>10</td></tr>
</table>
<p>Descriptive statistics (mean, median, standard deviation, correlation, regression) is in the <a href="../data-science/#/t/statistics">Statistics topic of the Data Science course</a>.</p>
<p><b>How to study:</b> one lesson a day is enough. Read the plain-words explanation, look at the picture, then work one practice question with pen and paper <i>before</i> opening the answer.</p>
""")

THEORY("Number systems", """
<table>
<tr><th>Set</th><th>Symbol</th><th>Contains</th></tr>
<tr><td>Natural numbers</td><td>ℕ</td><td>1, 2, 3, … (sometimes 0)</td></tr>
<tr><td>Integers</td><td>ℤ</td><td>whole numbers and their negatives</td></tr>
<tr><td>Rational numbers</td><td>ℚ</td><td>p/q with p, q integers, q ≠ 0; decimals that end or repeat</td></tr>
<tr><td>Irrational numbers</td><td>—</td><td>decimals that never end or repeat: √2, π, e</td></tr>
<tr><td>Real numbers</td><td>ℝ</td><td>rational + irrational: the whole number line</td></tr>
</table>
<p>ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ. A <b>prime</b> is a natural number greater than 1 whose only divisors are 1 and itself; every natural number above 1 is a unique product of primes (the Fundamental Theorem of Arithmetic).</p>
""")

THEORY("Operations, properties and order", """
<ul>
<li><b>Commutative</b>: a + b = b + a, a·b = b·a (not for − or ÷).</li>
<li><b>Associative</b>: (a + b) + c = a + (b + c); same for ×.</li>
<li><b>Distributive</b>: a(b + c) = ab + ac — the rule behind "expanding brackets".</li>
<li><b>Identity</b>: a + 0 = a, a·1 = a. <b>Inverse</b>: a + (−a) = 0, a·(1/a) = 1.</li>
<li>Division by zero is undefined.</li>
<li>Order of operations: brackets, powers/roots, × ÷ left to right, + − left to right.</li>
</ul>
""")

THEORY("Fractions, ratios and percentages", """
<ul>
<li>a/b = (a·k)/(b·k) for any k ≠ 0 — so you can simplify by the GCD or scale to a common denominator (the LCM of the bottoms).</li>
<li>a/b + c/d = (ad + cb)/bd; a/b × c/d = ac/bd; a/b ÷ c/d = a/b × d/c.</li>
<li>Percent = part / whole × 100. Percent change = (new − old) / old × 100. A 50% rise followed by a 50% fall is a 25% loss overall.</li>
<li>A ratio a : b splits a quantity into a + b equal parts.</li>
</ul>
""")

THEORY("Exponents, roots, logs preview and notation", """
<table>
<tr><th>Rule</th><th>Formula</th></tr>
<tr><td>Product</td><td>xᵃ·xᵇ = xᵃ⁺ᵇ</td></tr>
<tr><td>Quotient</td><td>xᵃ / xᵇ = xᵃ⁻ᵇ</td></tr>
<tr><td>Power</td><td>(xᵃ)ᵇ = xᵃᵇ</td></tr>
<tr><td>Zero / negative</td><td>x⁰ = 1, x⁻ⁿ = 1/xⁿ</td></tr>
<tr><td>Fractional</td><td>x^(p/q) = (q√x)ᵖ</td></tr>
</table>
<p><b>Scientific notation</b> writes x = a × 10ⁿ with 1 ≤ a &lt; 10; n = ⌊log₁₀ x⌋. <b>Significant figures</b> count digits from the first non-zero digit.</p>
<p><b>Σ</b> means sum, <b>Π</b> means product, n! = 1·2·…·n. Useful closed forms: Σk = n(n+1)/2, Σk² = n(n+1)(2n+1)/6.</p>
""")

FAQ("Why does ML need math at all if libraries do it for me?", "<p>Libraries do the computing, but you choose the model, the loss and the learning rate, and you debug it when training fails. That needs you to read the formulas and know what the numbers mean — e.g. why a loss became NaN or why features must be scaled.</p>")
FAQ("What is the difference between rational and irrational numbers?", "<p>Rational numbers can be written as a fraction of two integers; their decimals end or repeat. Irrational numbers (√2, π, e) cannot; their decimals go on forever without repeating.</p>")
FAQ("Why is any number to the power 0 equal to 1?", "<p>From the quotient rule: xⁿ / xⁿ = xⁿ⁻ⁿ = x⁰, and anything divided by itself is 1.</p>")
FAQ("What does Σ mean?", "<p>Add up. Σ from k = 1 to n of f(k) means f(1) + f(2) + … + f(n) — a for-loop that adds.</p>")
FAQ("How do you find the GCD quickly?", "<p>Euclid's algorithm: gcd(a, b) = gcd(b, a mod b), repeat until the second number is 0. It is one of the oldest algorithms still in use.</p>")
FAQ("Why do computers sometimes say 0.1 + 0.2 = 0.30000000000000004?", "<p>Floats are stored in binary, and 0.1 has no exact binary form (like 1/3 in decimal). Tiny rounding errors appear; compare floats with a tolerance (math.isclose) instead of ==.</p>")
