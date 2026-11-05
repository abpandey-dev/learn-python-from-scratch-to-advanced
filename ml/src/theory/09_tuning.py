from lib import *

THEORY("Search strategies", """
<table>
<tr><th>Method</th><th>How</th><th>Use when</th></tr>
<tr><td>Grid search</td><td>every combination</td><td>few parameters, small grids</td></tr>
<tr><td>Randomised search</td><td>random samples from distributions</td><td>many parameters; only a few usually matter</td></tr>
<tr><td>Successive halving</td><td>many candidates on little data, keep the best, give them more</td><td>expensive models</td></tr>
<tr><td>Bayesian optimisation</td><td>a model of the score chooses the next try (Optuna)</td><td>each fit is costly</td></tr>
<tr><td>Built-in CV</td><td>RidgeCV, LassoCV, LogisticRegressionCV</td><td>fast paths for one parameter</td></tr>
</table>
""")

THEORY("Common hyper-parameters", """
<table>
<tr><th>Model</th><th>Tune first</th></tr>
<tr><td>Linear / logistic</td><td>α or C (log scale)</td></tr>
<tr><td>k-NN</td><td>k, weights, metric</td></tr>
<tr><td>SVM (RBF)</td><td>C and γ together (log scale)</td></tr>
<tr><td>Decision tree</td><td>max_depth, min_samples_leaf</td></tr>
<tr><td>Random forest</td><td>max_features, min_samples_leaf; n_estimators just needs to be large enough</td></tr>
<tr><td>Gradient boosting</td><td>learning_rate with early stopping, max_depth, subsample</td></tr>
<tr><td>Neural network</td><td>learning rate first, then size, regularisation, batch size</td></tr>
</table>
""")

THEORY("Keeping the estimate honest", """
<ul>
<li>Split off the test set first and use it once.</li>
<li>Put every fitted preprocessing step inside the pipeline, so each fold fits it on its training part only.</li>
<li>The best CV score is optimistically biased, because it is the maximum of many noisy scores. <b>Nested CV</b> (an inner loop tunes, an outer loop scores) gives an unbiased estimate.</li>
<li>Match the splitter to the data: stratified for classes, grouped for repeated subjects, time-based for time series.</li>
<li>Compare mean ± std across folds. A difference smaller than the spread may be noise.</li>
</ul>
""")

THEORY("sklearn's composition tools", """
<table>
<tr><th>Tool</th><th>Purpose</th></tr>
<tr><td>Pipeline / make_pipeline</td><td>steps in sequence</td></tr>
<tr><td>ColumnTransformer</td><td>different steps per column</td></tr>
<tr><td>FeatureUnion</td><td>several transformers side by side</td></tr>
<tr><td>TransformedTargetRegressor</td><td>fit on a transformed y, predict back on the original scale</td></tr>
<tr><td>FunctionTransformer</td><td>wrap any function as a step</td></tr>
<tr><td>make_scorer</td><td>turn a metric into a CV scorer (scores are always "higher is better", so errors become negative)</td></tr>
<tr><td>joblib.dump / load</td><td>save and reload a fitted pipeline</td></tr>
</table>
""")

FAQ("Grid search vs randomised search?", "<p>Grid search tries every combination, which grows exponentially with the number of parameters. Randomised search samples a fixed number of combinations and covers each parameter's range better for the same budget, so it is usually preferred for more than two or three parameters.</p>")
FAQ("Why are scikit-learn error scores negative?", "<p>Model selection tools always maximise the score. Errors are negated (neg_mean_squared_error) so that higher still means better.</p>")
FAQ("What does a learning curve tell you?", "<p>If training and validation scores converge at a low value, the model is underfitting and more data won't help. If there is a large gap, the model is overfitting, and more data or regularisation should help.</p>")
FAQ("Why put preprocessing inside a pipeline?", "<p>So each CV fold fits it on training rows only (no leakage), and the same fitted steps are applied at prediction time (no train-serve skew).</p>")
FAQ("What is nested cross-validation?", "<p>An outer CV loop estimates performance while an inner loop chooses hyper-parameters on each outer training part. It stops the tuning process from inflating the performance estimate.</p>")
FAQ("How should you search regularisation strength?", "<p>On a log scale, because the effect depends on orders of magnitude. If the best value falls on the edge of the grid, extend the range.</p>")
