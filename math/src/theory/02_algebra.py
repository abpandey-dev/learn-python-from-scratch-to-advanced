from lib import *

THEORY("Vocabulary", """
<table>
<tr><th>Word</th><th>Meaning</th><th>Example</th></tr>
<tr><td>Variable</td><td>a letter standing for an unknown or changing number</td><td>x, y, w</td></tr>
<tr><td>Coefficient</td><td>the number multiplying a variable</td><td>3 in 3x</td></tr>
<tr><td>Constant</td><td>a number on its own</td><td>5</td></tr>
<tr><td>Term</td><td>a constant, a variable, or their product</td><td>4x²</td></tr>
<tr><td>Expression</td><td>terms joined by + or −, no "="</td><td>4x² − 3x + 5</td></tr>
<tr><td>Equation</td><td>two expressions set equal</td><td>2x + 3 = 11</td></tr>
<tr><td>Polynomial</td><td>sum of terms with whole-number powers; degree = highest power</td><td>x³ − 2x + 1 (degree 3)</td></tr>
</table>
""")

THEORY("Solving equations", """
<ul>
<li><b>Linear</b> (degree 1): isolate x with inverse operations. ax + b = c ⇒ x = (c − b)/a.</li>
<li><b>Quadratic</b> (degree 2): factorise, complete the square, or use x = (−b ± √(b² − 4ac)) / 2a. Discriminant D = b² − 4ac.</li>
<li>Sum of roots = −b/a, product = c/a (Vieta's formulas).</li>
<li>Higher degree: no simple general formula for degree ≥ 5 — use numerical methods (bisection, Newton) or <code>np.roots</code>.</li>
<li><b>Inequalities</b> are solved like equations, except multiplying or dividing by a negative <b>flips</b> the sign.</li>
<li><b>Absolute value</b>: |x − a| = b splits into x − a = b or x − a = −b.</li>
</ul>
""")

THEORY("Identities worth memorising", """
<table>
<tr><td>(a + b)² = a² + 2ab + b²</td></tr>
<tr><td>(a − b)² = a² − 2ab + b²</td></tr>
<tr><td>(a + b)(a − b) = a² − b²</td></tr>
<tr><td>(x + a)(x + b) = x² + (a + b)x + ab</td></tr>
</table>
<p>(a − b)² appears constantly in ML: the squared error between a prediction and a target.</p>
""")

THEORY("Systems of linear equations", """
<p>A system can have <b>one</b> solution (lines cross), <b>none</b> (parallel lines) or <b>infinitely many</b> (same line). Methods: substitution, elimination, and matrices (A·x = b ⇒ x = A⁻¹b when A is invertible). Linear regression is a giant system with more equations than unknowns, solved in the "least squares" sense.</p>
""")

THEORY("Sequences and series", """
<table>
<tr><th></th><th>Arithmetic</th><th>Geometric</th></tr>
<tr><td>Rule</td><td>add d</td><td>multiply by r</td></tr>
<tr><td>n-th term</td><td>a + (n − 1)d</td><td>a·rⁿ⁻¹</td></tr>
<tr><td>Sum of n terms</td><td>n(2a + (n − 1)d)/2</td><td>a(1 − rⁿ)/(1 − r)</td></tr>
<tr><td>Infinite sum</td><td>diverges (d ≠ 0)</td><td>a/(1 − r) if |r| &lt; 1</td></tr>
</table>
""")

FAQ("What is the difference between an expression and an equation?", "<p>An expression is a value to compute (3x + 2). An equation states that two expressions are equal (3x + 2 = 11) and can be solved for x.</p>")
FAQ("Why must you do the same thing to both sides?", "<p>An equation is a balance. Changing only one side breaks the equality, so the x you find would no longer satisfy the original equation.</p>")
FAQ("When does a quadratic have no real solution?", "<p>When the discriminant b² − 4ac is negative: the parabola never reaches the x-axis. (It has two complex solutions.)</p>")
FAQ("Why does the inequality sign flip when dividing by a negative?", "<p>2 &lt; 3, but −2 &gt; −3: multiplying by −1 mirrors numbers around zero and reverses their order.</p>")
FAQ("Where is algebra used in machine learning?", "<p>Everywhere: the model equation (y = wx + b), rearranging the loss, solving for optimal weights (normal equation), and simplifying gradients.</p>")
