from lib import *

THEORY("Eigenvalues and eigenvectors", """
<p>For a square matrix A, a non-zero vector v with <b>Av = λv</b> is an eigenvector and λ its eigenvalue. The eigenvalues are the roots of the characteristic polynomial <b>det(A − λI) = 0</b> (degree n, so n eigenvalues counting repeats, possibly complex).</p>
<ul>
<li>Σλᵢ = trace(A), Πλᵢ = det(A). A is invertible ⇔ 0 is not an eigenvalue.</li>
<li>Triangular matrices: eigenvalues are the diagonal entries.</li>
<li>Aᵏ has eigenvalues λᵏ with the same eigenvectors; A⁻¹ has 1/λ.</li>
<li><b>Spectral theorem</b>: a real symmetric matrix has real eigenvalues and an orthonormal set of eigenvectors: A = QΛQᵀ.</li>
<li>If A has n independent eigenvectors it is <b>diagonalisable</b>: A = PDP⁻¹.</li>
</ul>
""")

THEORY("Computing them", """
<table>
<tr><th>Method</th><th>Idea</th></tr>
<tr><td>Characteristic polynomial</td><td>exact for 2 × 2 / 3 × 3 by hand; unstable for large n</td></tr>
<tr><td>Power iteration</td><td>vₖ₊₁ = Avₖ / ‖Avₖ‖ → dominant eigenvector; converges at rate |λ₂/λ₁|</td></tr>
<tr><td>QR algorithm</td><td>what <code>np.linalg.eig</code> uses (LAPACK)</td></tr>
<tr><td><code>eigh</code></td><td>faster and more accurate for symmetric matrices; returns ascending order</td></tr>
</table>
""")

THEORY("PCA step by step", """
<ol>
<li>Standardise features if they have different units (otherwise large-scale features dominate).</li>
<li>Centre: Xc = X − mean.</li>
<li>Covariance C = XcᵀXc/(n − 1) (d × d, symmetric, positive semi-definite).</li>
<li>Eigen-decompose C; sort eigenvalues λ₁ ≥ λ₂ ≥ …; eigenvectors are the principal components (loadings).</li>
<li>Scores Z = Xc·W_k (n × k). Reconstruction X̂ = Z·W_kᵀ + mean.</li>
<li>Explained variance ratio λᵢ/Σλ; choose k to keep e.g. 95% (look at a scree plot).</li>
</ol>
<p>Equivalently via SVD: Xc = UΣVᵀ, the components are the rows of Vᵀ and λᵢ = σᵢ²/(n − 1). PCA is linear and unsupervised; it maximises variance, which is not always what helps prediction.</p>
""")

THEORY("Singular Value Decomposition", """
<p>Every m × n matrix factors as <b>A = UΣVᵀ</b>: U (m × m) and V (n × n) orthogonal, Σ diagonal with σ₁ ≥ … ≥ 0. σᵢ = √(eigenvalues of AᵀA). rank(A) = number of non-zero σ. ‖A‖₂ = σ₁; ‖A‖_F = √Σσᵢ². Truncating to k terms gives the best rank-k approximation with error √(σ²ₖ₊₁ + …) in Frobenius norm. Condition number κ = σ₁/σₙ.</p>
""")

THEORY("Where this appears in ML", """
<ul>
<li>PCA for dimensionality reduction and visualisation; whitening.</li>
<li>Recommenders (matrix factorisation ≈ truncated SVD); latent semantic analysis for text.</li>
<li>Spectral clustering (eigenvectors of a graph Laplacian), PageRank, Markov chains.</li>
<li>Stability of training: the Hessian's eigenvalues describe the curvature of the loss (next topics).</li>
<li>Positive-definite matrices (all λ &gt; 0) — covariance matrices, convex quadratic losses.</li>
</ul>
""")

FAQ("What is an eigenvector in plain words?", "<p>A direction that a matrix does not turn, only stretches. The eigenvalue is the stretch factor (negative means it flips).</p>")
FAQ("Why does PCA use the covariance matrix's eigenvectors?", "<p>The variance of the data projected onto a unit vector w is wᵀCw, which is maximised by the eigenvector with the largest eigenvalue; the next best direction perpendicular to it is the second eigenvector, and so on.</p>")
FAQ("Should you scale data before PCA?", "<p>Yes, when features have different units or ranges. Otherwise the feature with the biggest numbers dominates the first component.</p>")
FAQ("PCA vs SVD?", "<p>PCA is a goal (find directions of maximum variance); SVD of the centred data matrix is the standard way to compute it, avoiding forming XᵀX.</p>")
FAQ("What does a large condition number mean?", "<p>The matrix is close to singular: tiny changes in the input cause large changes in the solution — a warning sign of collinear features in regression.</p>")
