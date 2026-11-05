from lib import *

THEORY("k-nearest neighbours", """
<ul>
<li><b>Lazy / instance-based</b>: stores the data; prediction cost O(n·d) per query (KD-trees / ball trees / approximate nearest neighbour indexes speed this up).</li>
<li>Hyper-parameters: k, distance metric (Euclidean, Manhattan, Minkowski p, cosine), uniform vs distance weights.</li>
<li>k = 1: zero training error, high variance. Large k: high bias. As n → ∞, 1-NN error ≤ 2 × Bayes error.</li>
<li><b>Curse of dimensionality</b>: in high dimensions all points become nearly equidistant; reduce dimensions or select features.</li>
<li>Requires scaled features; handles multiclass naturally; non-parametric (boundary can be any shape).</li>
</ul>
""")

THEORY("Naive Bayes", """
<p>ŷ = argmax_c P(c) Πⱼ P(xⱼ | c), assuming conditional independence of features given the class. Computed as log P(c) + Σ log P(xⱼ | c).</p>
<table>
<tr><th>Variant</th><th>P(xⱼ | c)</th></tr>
<tr><td>Gaussian</td><td>N(xⱼ; μⱼc, σ²ⱼc)</td></tr>
<tr><td>Multinomial</td><td>θⱼc = (Nⱼc + α)/(N_c + αV)</td></tr>
<tr><td>Bernoulli</td><td>θⱼc^xⱼ (1 − θⱼc)^(1−xⱼ)</td></tr>
<tr><td>Categorical</td><td>smoothed category frequencies</td></tr>
</table>
<p>A generative model: it models how each class generates features. Fast, works with tiny data and many features; independence is usually false, so probabilities are poorly calibrated even when the ranking is good.</p>
""")

THEORY("Support vector machines", """
<p><b>Hard margin</b>: minimise ½‖w‖² subject to yᵢ(w·xᵢ + b) ≥ 1. <b>Soft margin</b>: minimise ½‖w‖² + C Σ ξᵢ with yᵢ(w·xᵢ + b) ≥ 1 − ξᵢ, equivalently ½‖w‖² + C Σ max(0, 1 − yᵢ(w·xᵢ + b)) (hinge loss).</p>
<ul>
<li>The <b>dual</b> problem depends on data only through dot products xᵢ·xⱼ → replace with a kernel K(xᵢ, xⱼ). The solution w = Σ αᵢyᵢxᵢ is non-zero only for support vectors.</li>
<li>A kernel is valid if its Gram matrix is positive semi-definite (Mercer).</li>
<li>Training cost grows between O(n²) and O(n³) — use LinearSVC / SGDClassifier for large data.</li>
<li>Outputs are scores, not probabilities (<code>probability=True</code> adds Platt scaling via CV).</li>
<li>Multiclass via one-vs-one (SVC) or one-vs-rest (LinearSVC). SVR does regression with an ε-insensitive tube.</li>
</ul>
""")

FAQ("Why must features be scaled for k-NN and SVM?", "<p>Both rely on distances or dot products; a feature with a large range dominates them, so the model effectively ignores the others.</p>")
FAQ("How do you choose k in k-NN?", "<p>By cross-validation over a range of k. Odd k avoids ties in binary problems; rule-of-thumb starts near √n.</p>")
FAQ("Why is Naive Bayes 'naive', and why does it still work?", "<p>It assumes features are independent given the class. Even when that's false, classification only needs the correct class to have the highest score, which often survives the approximation.</p>")
FAQ("What is Laplace smoothing?", "<p>Adding α (usually 1) to every count so a word never seen with a class doesn't get probability 0, which would wipe out the whole product.</p>")
FAQ("What are support vectors?", "<p>The training points on or inside the margin. They alone determine the SVM's boundary; removing other points doesn't change it.</p>")
FAQ("What do C and gamma control in an RBF SVM?", "<p>C sets how much margin violations are penalised (high C: fit training data tightly). γ sets how far each point's influence reaches (high γ: very local, wiggly boundary). Both high → overfitting.</p>")
FAQ("What is the kernel trick?", "<p>Computing dot products in a high-dimensional feature space directly from the original inputs, so the SVM can learn non-linear boundaries without ever building those features.</p>")

THEORY("Choosing between them", """
<table>
<tr><th></th><th>k-NN</th><th>Naive Bayes</th><th>SVM</th></tr>
<tr><td>Training</td><td>none</td><td>very fast</td><td>slow on large data (kernels)</td></tr>
<tr><td>Prediction</td><td>slow on large data</td><td>very fast</td><td>fast if few support vectors</td></tr>
<tr><td>Needs scaling</td><td>yes</td><td>no</td><td>yes</td></tr>
<tr><td>Many features</td><td>poor</td><td>good (text)</td><td>good</td></tr>
<tr><td>Probabilities</td><td>rough</td><td>overconfident</td><td>extra step</td></tr>
<tr><td>Best for</td><td>small, low-dimensional data; similarity search</td><td>text baselines, tiny data</td><td>medium data with clear margins</td></tr>
</table>
""")
