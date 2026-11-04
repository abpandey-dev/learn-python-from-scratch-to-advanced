from lib import *

THEORY("Definitions", """
<p>A <b>vector</b> in ℝⁿ is an ordered n-tuple v = (v₁, …, vₙ). A <b>scalar</b> is a single number. Vectors are usually written as columns. The <b>zero vector</b> has all components 0; <b>standard basis vectors</b> e₁ = (1, 0, …), e₂ = (0, 1, …) point along the axes, and every vector is a linear combination of them: v = v₁e₁ + … + vₙeₙ.</p>
""")

THEORY("Operations", """
<table>
<tr><th>Operation</th><th>Formula</th><th>Result</th></tr>
<tr><td>Addition</td><td>(u + v)ᵢ = uᵢ + vᵢ</td><td>vector</td></tr>
<tr><td>Scalar multiple</td><td>(cv)ᵢ = c·vᵢ</td><td>vector</td></tr>
<tr><td>Dot product</td><td>u·v = Σ uᵢvᵢ = ‖u‖‖v‖cos θ</td><td>scalar</td></tr>
<tr><td>Norm (L2)</td><td>‖v‖ = √(v·v)</td><td>scalar ≥ 0</td></tr>
<tr><td>L1 norm</td><td>‖v‖₁ = Σ|vᵢ|</td><td>scalar</td></tr>
<tr><td>Projection</td><td>proj_v u = (u·v / v·v) v</td><td>vector</td></tr>
<tr><td>Cross product (ℝ³)</td><td>u × v ⟂ u and v, ‖u × v‖ = ‖u‖‖v‖ sin θ</td><td>vector</td></tr>
<tr><td>Hadamard</td><td>(u ⊙ v)ᵢ = uᵢvᵢ</td><td>vector</td></tr>
</table>
""")

THEORY("Key properties", """
<ul>
<li>Dot product is commutative and distributive: u·(v + w) = u·v + u·w.</li>
<li><b>Cauchy–Schwarz</b>: |u·v| ≤ ‖u‖‖v‖ — so cosine similarity is always in [−1, 1].</li>
<li><b>Triangle inequality</b>: ‖u + v‖ ≤ ‖u‖ + ‖v‖.</li>
<li>u ⟂ v ⇔ u·v = 0. A set of mutually perpendicular unit vectors is <b>orthonormal</b>.</li>
<li>Vectors are <b>linearly independent</b> if none is a combination of the others; n independent vectors in ℝⁿ form a <b>basis</b>. The set of all their combinations is their <b>span</b>.</li>
</ul>
""")

THEORY("Distances used in ML", """
<table>
<tr><th>Distance</th><th>Formula</th><th>Used in</th></tr>
<tr><td>Euclidean (L2)</td><td>√Σ(pᵢ − qᵢ)²</td><td>k-NN, k-means</td></tr>
<tr><td>Manhattan (L1)</td><td>Σ|pᵢ − qᵢ|</td><td>robust distance, grids, Lasso penalty</td></tr>
<tr><td>Cosine distance</td><td>1 − cos θ</td><td>text, embeddings, recommendation</td></tr>
<tr><td>Hamming</td><td>number of positions that differ</td><td>binary / categorical codes</td></tr>
</table>
<p>Distances are sensitive to scale: a feature measured in thousands dominates one measured in units, so scale features first.</p>
""")

FAQ("Vector vs scalar?", "<p>A scalar is one number (temperature). A vector is a list of numbers with an order (wind = speed in x, speed in y), with direction and magnitude.</p>")
FAQ("What does the dot product tell you?", "<p>How much two vectors point the same way, scaled by their lengths. Zero means perpendicular. In ML it is a weighted sum: weights · features.</p>")
FAQ("Why is cosine similarity used for text?", "<p>Document vectors of different lengths (long vs short articles) can still be about the same thing. Cosine compares direction only, ignoring length.</p>")
FAQ("L1 vs L2 norm?", "<p>L2 is straight-line length (√Σx²); L1 is the sum of absolute values. L1 penalties (Lasso) push weights to exactly zero; L2 penalties (Ridge) shrink them smoothly.</p>")
FAQ("What is an embedding?", "<p>A learned vector representing an item (word, user, image) so that similar items have nearby vectors — compared with cosine similarity or dot products.</p>")
