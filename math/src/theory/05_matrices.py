from lib import *

THEORY("Definitions and special matrices", """
<table>
<tr><th>Matrix</th><th>Property</th></tr>
<tr><td>Square</td><td>n × n</td></tr>
<tr><td>Identity I</td><td>1 on the diagonal, 0 elsewhere; AI = IA = A</td></tr>
<tr><td>Diagonal</td><td>non-zero only on the diagonal; scales each axis</td></tr>
<tr><td>Symmetric</td><td>A = Aᵀ (covariance matrices)</td></tr>
<tr><td>Triangular</td><td>zeros below (upper) or above (lower) the diagonal</td></tr>
<tr><td>Orthogonal</td><td>QᵀQ = I; rotations and reflections, preserve lengths</td></tr>
<tr><td>Singular</td><td>det = 0, no inverse</td></tr>
</table>
""")

THEORY("Operations and rules", """
<ul>
<li>(AB)ᵢⱼ = Σₖ AᵢₖBₖⱼ; defined when columns of A = rows of B.</li>
<li>Associative (AB)C = A(BC), distributive A(B + C) = AB + AC, <b>not commutative</b>.</li>
<li>(AB)ᵀ = BᵀAᵀ; (AB)⁻¹ = B⁻¹A⁻¹.</li>
<li>Trace: tr(A) = Σ Aᵢᵢ; tr(AB) = tr(BA).</li>
<li>Cost of multiplying n × n matrices naively: n³ multiplications.</li>
</ul>
""")

THEORY("Determinant", """
<p>2 × 2: ad − bc. 3 × 3: cofactor expansion along a row. Properties: det(AB) = det A · det B; det Aᵀ = det A; swapping two rows flips the sign; a row of zeros or two equal rows gives 0; det(A⁻¹) = 1/det A. |det A| is the factor by which A scales area (volume); the sign tells whether orientation flips.</p>
""")

THEORY("Systems, inverse and rank", """
<p>A·x = b has a unique solution ⇔ A is square with det A ≠ 0 ⇔ rank A = n ⇔ A is invertible ⇔ the columns are linearly independent (the <b>invertible matrix theorem</b>).</p>
<ul>
<li><b>Gaussian elimination</b> reduces A to triangular form with row operations, then back-substitutes: O(n³).</li>
<li><b>Rank</b> = number of pivots = dimension of the column space. rank + nullity = number of columns.</li>
<li>Over-determined systems (more equations than unknowns, as in regression) are solved by <b>least squares</b>: minimise ‖Xw − y‖², giving XᵀXw = Xᵀy.</li>
</ul>
""")

THEORY("Matrices in machine learning", """
<table>
<tr><th>Where</th><th>Matrix</th></tr>
<tr><td>Dataset</td><td>X: n examples × d features</td></tr>
<tr><td>Linear / logistic regression</td><td>predictions Xw</td></tr>
<tr><td>Neural-network layer</td><td>activation(Wx + b); a batch: activation(XWᵀ + b)</td></tr>
<tr><td>Images</td><td>height × width (× colour channels)</td></tr>
<tr><td>Covariance / correlation</td><td>XᵀX/(n − 1) on centred data</td></tr>
<tr><td>Recommenders</td><td>user × item ratings, factorised into two thin matrices</td></tr>
<tr><td>Graphs</td><td>adjacency matrix; Markov transition matrix</td></tr>
</table>
""")

FAQ("Why is matrix multiplication not commutative?", "<p>AB means 'apply B, then A'. Rotating then stretching generally differs from stretching then rotating; and AB may exist while BA doesn't (shapes).</p>")
FAQ("What does a determinant of zero mean?", "<p>The matrix squashes space into a lower dimension (a plane onto a line), so different inputs give the same output and it cannot be undone — no inverse, and A·x = b has no or infinitely many solutions.</p>")
FAQ("Why use np.linalg.solve instead of inv(A) @ b?", "<p>Solving directly with elimination is about twice as fast and more numerically accurate than forming the inverse first.</p>")
FAQ("What is the difference between A * B and A @ B in NumPy?", "<p>A * B multiplies matching entries (shapes must match or broadcast). A @ B is the matrix product (rows times columns).</p>")
FAQ("Why do GPUs matter for deep learning?", "<p>Training is dominated by huge matrix multiplications, which GPUs perform in parallel thousands of times faster than a loop on a CPU.</p>")
