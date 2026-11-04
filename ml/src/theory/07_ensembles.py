from lib import *

THEORY("Ensemble families", """
<table>
<tr><th>Method</th><th>Idea</th><th>sklearn</th></tr>
<tr><td>Voting</td><td>combine different models by majority or averaged probabilities</td><td>VotingClassifier / VotingRegressor</td></tr>
<tr><td>Bagging</td><td>same model on bootstrap samples, averaged</td><td>BaggingClassifier / Regressor</td></tr>
<tr><td>Random forest</td><td>bagged trees + random feature subsets per split</td><td>RandomForestClassifier / Regressor</td></tr>
<tr><td>Extra trees</td><td>random thresholds too — even less correlated</td><td>ExtraTreesClassifier</td></tr>
<tr><td>AdaBoost</td><td>reweight misclassified samples sequentially</td><td>AdaBoostClassifier</td></tr>
<tr><td>Gradient boosting</td><td>fit each new tree to the negative gradient of the loss</td><td>GradientBoosting*, HistGradientBoosting*</td></tr>
<tr><td>Stacking</td><td>meta-model on out-of-fold base predictions</td><td>StackingClassifier / Regressor</td></tr>
</table>
""")

THEORY("Random forests", """
<ul>
<li>Each tree: bootstrap sample of size n; at each split, consider max_features random features ('sqrt' default for classification, 1.0 for regression in recent sklearn).</li>
<li>P(a row is out of bag) = (1 − 1/n)ⁿ → e⁻¹ ≈ 0.368. OOB predictions give a validation estimate without a separate split (<code>oob_score=True</code>).</li>
<li>Variance of the average: ρσ² + (1 − ρ)σ²/B. More trees never overfit (only plateau); feature subsampling lowers ρ.</li>
<li>Classifier prediction = average of tree probabilities (not a hard vote).</li>
<li>Key hyper-parameters: n_estimators, max_features, max_depth / min_samples_leaf, class_weight.</li>
</ul>
""")

THEORY("Gradient boosting", """
<p>F₀(x) = argmin_c Σ L(yᵢ, c) (the mean for squared error). For m = 1 … M: pseudo-residuals rᵢ = −∂L/∂F(xᵢ); fit a regression tree hₘ to r; set leaf values by a line search (Newton step for log-loss); Fₘ = Fₘ₋₁ + η·hₘ.</p>
<table>
<tr><th>Loss</th><th>Pseudo-residual</th></tr>
<tr><td>Squared error</td><td>y − F</td></tr>
<tr><td>Absolute error</td><td>sign(y − F)</td></tr>
<tr><td>Log-loss</td><td>y − σ(F)</td></tr>
</table>
<p>Regularisation: learning rate η, n_estimators with early stopping, max_depth / max_leaf_nodes, subsample &lt; 1 (stochastic boosting), min_samples_leaf, L2 on leaf values (XGBoost). Modern libraries bin features into histograms for speed and handle missing values and categories natively.</p>
""")

THEORY("AdaBoost (SAMME)", """
<ol>
<li>Initialise weights wᵢ = 1/n.</li>
<li>Fit a weak learner with weights; err = Σ wᵢ[yᵢ ≠ ŷᵢ] / Σ wᵢ.</li>
<li>α = ln((1 − err)/err) + ln(K − 1).</li>
<li>wᵢ ← wᵢ·e^α for misclassified rows; normalise.</li>
<li>Predict by the α-weighted vote. Binary AdaBoost minimises the exponential loss e^(−y·F(x)).</li>
</ol>
""")

FAQ("Bagging vs boosting?", "<p>Bagging trains models independently on bootstrap samples and averages them, mainly reducing variance. Boosting trains models sequentially, each correcting the previous ones' errors, mainly reducing bias.</p>")
FAQ("Why does a random forest use random feature subsets?", "<p>Without them, every tree would split on the same strong features and the trees would be highly correlated, so averaging would remove little variance. Random subsets decorrelate the trees.</p>")
FAQ("Can adding more trees to a random forest overfit?", "<p>No — performance plateaus as trees are added. Boosting, by contrast, can overfit with too many rounds unless the learning rate is small and early stopping is used.</p>")
FAQ("What is the out-of-bag score?", "<p>Each row is predicted only by the trees that did not see it in their bootstrap sample; the accuracy of those predictions estimates generalisation without a separate validation set.</p>")
FAQ("What does the learning rate do in gradient boosting?", "<p>It scales each new tree's contribution. Smaller rates need more trees but generalise better; it trades training time for accuracy.</p>")
FAQ("Why are gradient-boosted trees so popular for tabular data?", "<p>They capture non-linearities and interactions automatically, handle mixed feature types and missing values, need little preprocessing, and with tuning usually give the best accuracy on structured data.</p>")
