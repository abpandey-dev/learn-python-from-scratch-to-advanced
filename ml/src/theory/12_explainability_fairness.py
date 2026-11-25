from lib import *

THEORY("Explanation methods", """
<table>
<tr><th>Method</th><th>Scope</th><th>Model</th><th>Note</th></tr>
<tr><td>Coefficients</td><td>global + local</td><td>linear</td><td>scale features first to compare</td></tr>
<tr><td>Impurity importance</td><td>global</td><td>trees</td><td>biased to high-cardinality features</td></tr>
<tr><td>Permutation importance</td><td>global</td><td>any</td><td>use validation data; correlated features share credit</td></tr>
<tr><td>Partial dependence / ICE</td><td>global</td><td>any</td><td>assumes the feature can vary independently</td></tr>
<tr><td>SHAP</td><td>local → global</td><td>any (fast for trees)</td><td>additive, consistent</td></tr>
<tr><td>LIME</td><td>local</td><td>any</td><td>fits a simple model around one point</td></tr>
<tr><td>Counterfactuals</td><td>local</td><td>any</td><td>actionable "what if"</td></tr>
</table>
""")

THEORY("Shapley value formula", """
<p>φᵢ = Σ over subsets S not containing i of |S|! (n − |S| − 1)! / n! × [v(S ∪ {i}) − v(S)]</p>
<p>Properties: <b>efficiency</b> (values add up to v(all) − v(none)), <b>symmetry</b>, <b>dummy</b> (no effect → 0) and <b>additivity</b>.</p>
""")

THEORY("Fairness metrics", """
<table>
<tr><th>Metric</th><th>Definition</th></tr>
<tr><td>Demographic parity difference</td><td>max − min of P(ŷ=1 | group)</td></tr>
<tr><td>Disparate impact ratio</td><td>min ÷ max of P(ŷ=1 | group); &lt; 0.8 is a red flag</td></tr>
<tr><td>Equal opportunity difference</td><td>gap in TPR = P(ŷ=1 | y=1, group)</td></tr>
<tr><td>Equalized odds</td><td>gaps in both TPR and FPR</td></tr>
<tr><td>Predictive parity</td><td>equal precision P(y=1 | ŷ=1, group)</td></tr>
</table>
""")

THEORY("Imbalanced classification toolkit", """
<ul>
<li>Metrics: precision, recall, F1, PR-AUC, balanced accuracy — not accuracy.</li>
<li>Stratified splits so each fold keeps the class ratio.</li>
<li>Class weights or resampling inside the training fold only.</li>
<li>Threshold chosen on validation data for the business cost.</li>
<li>Calibrate if you resampled, because resampling distorts probabilities.</li>
</ul>
""")

FAQ("Permutation importance vs impurity importance?", "<p>Permutation importance measures the drop in a chosen score when a feature is shuffled, works for any model and on held-out data. Impurity importance is computed from training splits of trees and favours features with many distinct values.</p>")
FAQ("What are SHAP values?", "<p>Shapley values from game theory applied to features: each feature's average marginal contribution over all orders of adding features. They add up exactly from the average prediction to this prediction.</p>")
FAQ("Can a model be fair if it doesn't use gender?", "<p>Not necessarily. Other features (pincode, name, shopping habits) can act as proxies. Fairness must be measured on outcomes per group.</p>")
FAQ("Why can't all fairness criteria be satisfied together?", "<p>When groups have different base rates, a calibrated model can't also have equal false-positive and false-negative rates across groups (except for a perfect model). You have to choose which notion matters for the decision.</p>")
FAQ("How do you handle a 1:99 class imbalance?", "<p>Use precision/recall or PR-AUC, stratified splits, class weights or resampling on training data only, and pick the decision threshold from validation data using the real costs of each error.</p>")
FAQ("What does it mean for a model to be calibrated?", "<p>Its predicted probabilities match observed frequencies: among cases scored 0.3, about 30% are positive. Check with reliability curves, Brier score or ECE.</p>")
