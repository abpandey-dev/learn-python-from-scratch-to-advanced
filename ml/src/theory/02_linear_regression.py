from lib import *

THEORY("Model and estimation", """
<p>ŷ = Xw (with a column of 1s for the intercept). Ordinary least squares minimises ‖y − Xw‖², giving the <b>normal equations</b> XᵀXw = Xᵀy and w = (XᵀX)⁻¹Xᵀy when XᵀX is invertible. Geometrically, ŷ is the projection of y onto the column space of X. Computed in practice by QR/SVD (<code>lstsq</code>) or by gradient descent for very large data.</p>
<p>Maximum-likelihood view: if y = Xw + ε with ε ~ N(0, σ²), least squares is the MLE.</p>
""")

THEORY("Assumptions (for valid inference)", """
<ol>
<li><b>Linearity</b>: E[y | x] is linear in the parameters (features may be transformed).</li>
<li><b>Independence</b> of errors.</li>
<li><b>Homoscedasticity</b>: constant error variance (no funnel shape in residuals).</li>
<li><b>Normality</b> of errors (matters for confidence intervals, not for prediction).</li>
<li>No perfect <b>multicollinearity</b> among features (check correlations / VIF).</li>
</ol>
<p>Diagnose with residual plots; fix with transformations, interaction or polynomial terms, robust or regularised regression.</p>
""")

THEORY("Metrics", """
<table>
<tr><th>Metric</th><th>Formula</th><th>Notes</th></tr>
<tr><td>MSE</td><td>(1/n)Σ(y − ŷ)²</td><td>differentiable, outlier-sensitive</td></tr>
<tr><td>RMSE</td><td>√MSE</td><td>same units as y</td></tr>
<tr><td>MAE</td><td>(1/n)Σ|y − ŷ|</td><td>robust; median-optimal</td></tr>
<tr><td>MAPE</td><td>(1/n)Σ|y − ŷ|/|y|</td><td>undefined at y = 0, asymmetric</td></tr>
<tr><td>R²</td><td>1 − SS_res/SS_tot</td><td>can be negative on test data</td></tr>
<tr><td>Adjusted R²</td><td>1 − (1 − R²)(n − 1)/(n − p − 1)</td><td>penalises extra features</td></tr>
</table>
""")

THEORY("Regularisation", """
<table>
<tr><th></th><th>Ridge</th><th>Lasso</th><th>Elastic Net</th></tr>
<tr><td>Penalty</td><td>α‖w‖₂²</td><td>α‖w‖₁</td><td>α(ρ‖w‖₁ + (1 − ρ)‖w‖₂²/2)</td></tr>
<tr><td>Solution</td><td>closed form (XᵀX + αI)⁻¹Xᵀy</td><td>coordinate descent with soft-thresholding</td><td>coordinate descent</td></tr>
<tr><td>Sparsity</td><td>no</td><td>yes</td><td>yes</td></tr>
<tr><td>Correlated features</td><td>shares weight among them</td><td>picks one arbitrarily</td><td>groups them</td></tr>
</table>
<p>Bayesian view: Ridge = Gaussian prior on weights, Lasso = Laplace prior. The intercept is not penalised; features must be scaled.</p>
""")

THEORY("Bias–variance decomposition", """
<p>Expected test error = <b>bias²</b> + <b>variance</b> + irreducible noise. Simple models: high bias, low variance. Flexible models: low bias, high variance. Regularisation, more data, fewer features and ensembling reduce variance; richer features or models reduce bias.</p>
""")

FAQ("Why squared error rather than absolute error?", "<p>It is smooth and differentiable, has a closed-form solution, corresponds to Gaussian noise (maximum likelihood), and penalises large errors more. Absolute error is more robust to outliers but has no closed form.</p>")
FAQ("What does a coefficient mean?", "<p>The expected change in the prediction for a one-unit increase in that feature, holding all other features constant.</p>")
FAQ("What is multicollinearity and why is it a problem?", "<p>Features that are strongly correlated make XᵀX nearly singular, so coefficients become unstable and hard to interpret (predictions may still be fine). Ridge regression or removing redundant features helps.</p>")
FAQ("Ridge vs Lasso?", "<p>Ridge (L2) shrinks all weights toward zero but keeps them; Lasso (L1) can set weights exactly to zero, performing feature selection. Elastic Net mixes both.</p>")
FAQ("How do you detect overfitting?", "<p>Training error much lower than validation/test error. Learning curves and validation curves make it visible.</p>")
FAQ("Can R² be negative?", "<p>Yes, on test data: a model worse than always predicting the mean gives R² &lt; 0.</p>")
