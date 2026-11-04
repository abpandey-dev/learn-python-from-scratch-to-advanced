from lib import *

THEORY("The model", """
<p>P(y = 1 | x) = σ(wᵀx + b), with σ(z) = 1/(1 + e⁻ᶻ). Equivalently the <b>log-odds</b> are linear: ln(p/(1 − p)) = wᵀx + b. It is a <b>generalised linear model</b> with a Bernoulli outcome and logit link. Despite the name, it is a classification model.</p>
""")

THEORY("Training", """
<ul>
<li>Maximum likelihood ⇔ minimise log-loss L = −(1/n)Σ[y ln p + (1 − y) ln(1 − p)].</li>
<li>Gradient: ∇L = Xᵀ(p − y)/n. Hessian: XᵀSX/n with S = diag(p(1 − p)) — positive semi-definite, so L is convex.</li>
<li>Solvers: gradient descent/SGD, Newton's method (IRLS), L-BFGS (sklearn's default <code>lbfgs</code>), <code>liblinear</code>, <code>saga</code> (L1, large data).</li>
<li>If classes are perfectly separable, unregularised weights grow without bound — regularisation keeps them finite.</li>
<li>sklearn objective: ½‖w‖² + C·Σ log-loss (L2). Smaller C ⇒ stronger regularisation.</li>
</ul>
""")

THEORY("Multiclass", """
<table>
<tr><th>Strategy</th><th>How</th></tr>
<tr><td>Multinomial (softmax)</td><td>K weight vectors; pₖ = e^{zₖ}/Σe^{zⱼ}; loss = categorical cross-entropy</td></tr>
<tr><td>One-vs-rest (OvR)</td><td>K binary classifiers, pick the highest score</td></tr>
<tr><td>One-vs-one (OvO)</td><td>K(K − 1)/2 pairwise classifiers, majority vote (used by SVC)</td></tr>
</table>
""")

THEORY("Linear classifiers compared", """
<table>
<tr><th>Model</th><th>Loss</th><th>Output</th></tr>
<tr><td>Logistic regression</td><td>log-loss</td><td>calibrated-ish probabilities</td></tr>
<tr><td>Perceptron</td><td>max(0, −y·z)</td><td>class only; converges only if separable</td></tr>
<tr><td>Linear SVM</td><td>hinge max(0, 1 − y·z) + ‖w‖²</td><td>class + margin</td></tr>
<tr><td>Linear discriminant analysis</td><td>generative Gaussian model</td><td>probabilities</td></tr>
</table>
""")

FAQ("Why is it called regression if it classifies?", "<p>It regresses the log-odds of the class on the features (a linear model for the log-odds); the classification comes from thresholding the resulting probability.</p>")
FAQ("Why not use linear regression for classification?", "<p>Its outputs aren't bounded to [0, 1], squared error is a poor loss for 0/1 targets, and outliers shift the boundary badly. The sigmoid plus log-loss fixes all three.</p>")
FAQ("How do you interpret a logistic regression coefficient?", "<p>A one-unit increase in the feature adds w to the log-odds, i.e. multiplies the odds by e^w, holding other features fixed.</p>")
FAQ("What does C do in sklearn's LogisticRegression?", "<p>C is the inverse regularisation strength. Small C = strong penalty, smaller weights, simpler model; large C = weak penalty, risk of overfitting.</p>")
FAQ("How do you handle class imbalance in logistic regression?", "<p>class_weight='balanced' (or custom weights), resampling, choosing a threshold other than 0.5, and evaluating with precision/recall or PR-AUC instead of accuracy.</p>")
FAQ("What is the decision boundary of logistic regression?", "<p>The set where wᵀx + b = 0 (p = 0.5): a hyperplane, so the model is a linear classifier unless you add non-linear features.</p>")
