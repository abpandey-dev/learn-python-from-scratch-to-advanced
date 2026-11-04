from lib import *

THEORY("Classification metrics", """
<table>
<tr><th>Metric</th><th>Formula</th><th>Use when</th></tr>
<tr><td>Accuracy</td><td>(TP + TN)/n</td><td>balanced classes, equal costs</td></tr>
<tr><td>Precision</td><td>TP/(TP + FP)</td><td>false positives are costly (spam filter)</td></tr>
<tr><td>Recall / TPR</td><td>TP/(TP + FN)</td><td>misses are costly (disease, fraud)</td></tr>
<tr><td>Specificity / TNR</td><td>TN/(TN + FP)</td><td>medical screening (with sensitivity)</td></tr>
<tr><td>F1 / Fβ</td><td>(1 + β²)PR/(β²P + R)</td><td>β &gt; 1 favours recall</td></tr>
<tr><td>Balanced accuracy</td><td>mean per-class recall</td><td>imbalanced data</td></tr>
<tr><td>MCC</td><td>(TP·TN − FP·FN)/√(…)</td><td>imbalanced binary; uses all four cells</td></tr>
<tr><td>Cohen's κ</td><td>(p_o − p_e)/(1 − p_e)</td><td>agreement corrected for chance</td></tr>
<tr><td>ROC AUC</td><td>P(score₊ &gt; score₋)</td><td>ranking quality, threshold-free</td></tr>
<tr><td>Average precision</td><td>Σ(Rₙ − Rₙ₋₁)Pₙ</td><td>rare positives</td></tr>
<tr><td>Log-loss, Brier</td><td>−mean log p, mean (p − y)²</td><td>probability quality / calibration</td></tr>
</table>
""")

THEORY("Validation strategies", """
<ul>
<li><b>Hold-out</b>: one train/test split — simple, high variance on small data.</li>
<li><b>k-fold CV</b>: k estimates, report mean ± std; k = 5 or 10 typical.</li>
<li><b>Stratified</b> folds for classification; <b>grouped</b> folds for repeated subjects; <b>time-series</b> splits for temporal data.</li>
<li><b>Nested CV</b>: inner loop tunes hyper-parameters, outer loop estimates performance — avoids optimistic bias from tuning on the evaluation folds.</li>
<li>The test set is used once; reusing it for decisions turns it into a validation set.</li>
</ul>
""")

THEORY("Diagnosing models", """
<table>
<tr><th>Symptom</th><th>Diagnosis</th><th>Remedies</th></tr>
<tr><td>Train and validation error both high</td><td>underfitting (bias)</td><td>more features, more complex model, less regularisation</td></tr>
<tr><td>Train error low, validation high</td><td>overfitting (variance)</td><td>more data, regularisation, simpler model, ensembling, early stopping</td></tr>
<tr><td>Validation suspiciously high</td><td>leakage</td><td>audit features and preprocessing order</td></tr>
<tr><td>Good offline, bad in production</td><td>data drift / train-serve skew</td><td>monitor inputs, retrain, same pipeline in both</td></tr>
</table>
<p>Learning curves (score vs training size) show whether more data would help; validation curves (score vs a hyper-parameter) show the bias–variance trade-off.</p>
""")

FAQ("Precision vs recall?", "<p>Precision: of the items flagged positive, the share that truly are. Recall: of the truly positive items, the share that were flagged. Raising the threshold usually increases precision and decreases recall.</p>")
FAQ("Why is accuracy misleading for imbalanced data?", "<p>If 99% of transactions are legitimate, predicting 'legitimate' always gives 99% accuracy while catching zero fraud. Use recall, precision, F1, PR-AUC, balanced accuracy or MCC.</p>")
FAQ("What does ROC AUC mean?", "<p>The probability that the model scores a randomly chosen positive higher than a randomly chosen negative. 0.5 is random, 1.0 is perfect ranking.</p>")
FAQ("ROC AUC vs PR AUC?", "<p>ROC AUC can look high on heavily imbalanced data because the many true negatives keep the false positive rate low. PR AUC focuses on the positive class and is more informative when positives are rare.</p>")
FAQ("Why use cross-validation?", "<p>It uses all data for both training and evaluation, gives a more stable estimate than a single split, and shows variability across folds.</p>")
FAQ("What is the difference between validation and test sets?", "<p>The validation set (or CV) guides choices — model, features, hyper-parameters. The test set is held back for one final, unbiased estimate after all choices are made.</p>")
