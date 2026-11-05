from lib import *

THEORY("Types of machine learning", """
<table>
<tr><th>Type</th><th>Learns from</th><th>Goal</th><th>Algorithms</th></tr>
<tr><td>Supervised — regression</td><td>(X, numeric y)</td><td>predict a number</td><td>linear regression, trees, gradient boosting</td></tr>
<tr><td>Supervised — classification</td><td>(X, class y)</td><td>predict a category</td><td>logistic regression, k-NN, SVM, random forest</td></tr>
<tr><td>Unsupervised</td><td>X only</td><td>find structure</td><td>k-means, DBSCAN, PCA</td></tr>
<tr><td>Semi-/self-supervised</td><td>few labels / labels made from the data</td><td>use unlabelled data</td><td>pre-training of LLMs</td></tr>
<tr><td>Reinforcement learning</td><td>rewards from actions</td><td>learn a policy</td><td>Q-learning, policy gradients, RLHF</td></tr>
</table>
""")

THEORY("The ML workflow", """
<ol>
<li>Define the problem and the metric that matters (and a baseline).</li>
<li>Collect and explore data (EDA): types, missing values, distributions, target balance, leakage.</li>
<li>Split: train / validation (or cross-validation) / test — before any fitting.</li>
<li>Preprocess and engineer features — fitted on training data only, inside a pipeline.</li>
<li>Train candidate models; tune hyper-parameters with cross-validation.</li>
<li>Evaluate once on the test set; analyse errors.</li>
<li>Deploy, monitor for <b>data drift</b>, retrain.</li>
</ol>
<p><b>Parameters</b> are learned from data (weights); <b>hyper-parameters</b> are chosen by you (learning rate, tree depth, k).</p>
""")

THEORY("Preprocessing reference", """
<table>
<tr><th>Problem</th><th>Technique</th><th>sklearn</th></tr>
<tr><td>Different scales</td><td>standardise / min-max / robust</td><td>StandardScaler, MinMaxScaler, RobustScaler</td></tr>
<tr><td>Skewed numbers</td><td>log, Box-Cox, Yeo-Johnson</td><td>FunctionTransformer, PowerTransformer</td></tr>
<tr><td>Unordered categories</td><td>one-hot</td><td>OneHotEncoder(handle_unknown="ignore")</td></tr>
<tr><td>Ordered categories</td><td>ordinal</td><td>OrdinalEncoder(categories=[…])</td></tr>
<tr><td>High-cardinality categories</td><td>target / frequency encoding, hashing</td><td>TargetEncoder</td></tr>
<tr><td>Missing values</td><td>mean / median / mode / KNN / indicator</td><td>SimpleImputer, KNNImputer, MissingIndicator</td></tr>
<tr><td>Non-linear effects</td><td>polynomial features, binning, splines</td><td>PolynomialFeatures, KBinsDiscretizer, SplineTransformer</td></tr>
<tr><td>Mixed column types</td><td>different steps per column</td><td>ColumnTransformer</td></tr>
</table>
""")

THEORY("Data leakage", """
<p><b>Leakage</b> is when information that would not be available at prediction time sneaks into training, giving great validation scores and poor real results. Common causes:</p>
<ul>
<li>Fitting scalers, imputers or feature selection on the full dataset before splitting.</li>
<li>Features derived from the target (e.g. "refund issued" when predicting fraud).</li>
<li>Duplicate or near-duplicate rows across train and test.</li>
<li>Random splits of time-series data (the model sees the future) — use time-based splits.</li>
<li>Rows from the same patient/user in both train and test — use GroupKFold.</li>
</ul>
""")

FAQ("What is the difference between a parameter and a hyper-parameter?", "<p>Parameters (weights, split thresholds) are learned from training data. Hyper-parameters (learning rate, tree depth, regularisation strength, k) are set before training and tuned with validation.</p>")
FAQ("Why fit the scaler only on the training set?", "<p>Using test-set statistics to transform training data leaks information about the test set, so the test score becomes optimistic. The pipeline must be learned only from what you'd have at training time.</p>")
FAQ("One-hot vs label encoding for features?", "<p>One-hot for unordered categories, because label encoding (0, 1, 2) invents an order and distances that linear models and k-NN will take literally. Tree models tolerate ordinal codes better.</p>")
FAQ("Why do we need a baseline?", "<p>It tells you whether the model learned anything. Accuracy of 90% means nothing if predicting the majority class already gives 90%.</p>")
FAQ("Which models need feature scaling?", "<p>Distance- and gradient-based ones: k-NN, k-means, SVM, linear/logistic regression with regularisation, neural networks, PCA. Tree-based models (decision trees, random forests, gradient boosting) don't.</p>")
FAQ("What is a pipeline and why use it?", "<p>An object chaining preprocessing steps and a model. It guarantees the same transforms at train and predict time and that each fold of cross-validation fits preprocessing only on its training part, preventing leakage.</p>")

THEORY("Common beginner mistakes", """
<table>
<tr><th>Mistake</th><th>Why it hurts</th><th>Do this instead</th></tr>
<tr><td>Judging a model on its training data</td><td>rewards memorising</td><td>score on held-out data</td></tr>
<tr><td>Skipping the baseline</td><td>you can't tell if it learned anything</td><td>compare with a dummy model</td></tr>
<tr><td>Preprocessing before splitting</td><td>leakage inflates the score</td><td>put preprocessing in a pipeline</td></tr>
<tr><td>Only reporting accuracy on imbalanced data</td><td>hides total failure on the rare class</td><td>recall, precision, PR-AUC</td></tr>
<tr><td>Tuning repeatedly against the test set</td><td>the test score becomes optimistic</td><td>tune with CV, test once</td></tr>
<tr><td>Trying fancy models first</td><td>harder to debug, often no better</td><td>simple model first, then add complexity</td></tr>
</table>
""")
