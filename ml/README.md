# Machine Learning from Scratch

9 topics · theory with 49 theory questions · 36 lessons from basics to advanced · 180 practice questions with answers · Data preparation, linear and logistic regression, model evaluation, k-NN, Naive Bayes and SVM, decision trees, ensembles, clustering, tuning and pipelines, and neural networks · every algorithm is built from scratch in plain Python and NumPy, then done again with scikit-learn, both shown running step by step.

**Live site:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/

Every solution is run against its test cases by `build.py` before the site is generated, and each animation is recorded from a real run of the code you see.

## Topics

- [ML Basics & Data Preparation](#ml-basics-data-preparation) — What a model learns from, splitting data honestly, baselines, scaling, encoding categories, filling missing values, creating and selecting features, and folds for cross-validation.
- [Linear Regression](#linear-regression) — The first model to learn: fitting a line by least squares and by gradient descent, multiple features, regression metrics, polynomial features, overfitting, and Ridge / Lasso regularisation.
- [Logistic Regression & Classification](#logistic-regression-classification) — Predicting categories: the sigmoid, odds and log-odds, log-loss, training by Newton's method, decision boundaries, thresholds, regularisation, softmax for many classes, and the perceptron.
- [Model Evaluation & Validation](#model-evaluation-validation) — Measuring a model honestly: the confusion matrix, precision, recall, F1, ROC and PR curves, MCC and kappa, choosing thresholds, and cross-validation strategies.
- [k-NN, Naive Bayes & SVM](#k-nn-naive-bayes-svm) — Three classic classifiers: k-nearest neighbours (vote of the closest examples), Naive Bayes (Bayes' rule with an independence shortcut) and support vector machines (the widest possible margin, plus kernels).
- [Decision Trees](#decision-trees) — Models that ask a sequence of yes/no questions: impurity (Gini, entropy, MSE), finding the best split, growing and stopping, predictions, depth and leaves, feature importance, and overfitting.
- [Ensembles: Bagging, Forests & Boosting](#ensembles-bagging-forests-boosting) — Many models beat one: voting, bootstrap samples and bagging, random forests from the inside, gradient boosting built from scratch, AdaBoost's weights, and why averaging reduces variance.
- [Clustering & Unsupervised Learning](#clustering-unsupervised-learning) — Finding structure without labels: k-means step by step, choosing k with the elbow and silhouette, hierarchical clustering, DBSCAN for odd shapes and noise, comparing clusterings, PCA, and distance-based outliers.
- [Tuning, Pipelines & Regularisation](#tuning-pipelines-regularisation) — Turning a model into a reliable system: hyper-parameter grids and grid search, validation and learning curves, choosing regularisation by CV, ColumnTransformer and pipelines, avoiding leakage, custom scorers and target transforms.

## ML Basics & Data Preparation

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Train / Test Split Without Shuffling](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/basics/train-test-split-without-shuffling) | Easy | Holding data back |
| 2 | [Majority-Class Baseline](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/basics/majority-class-baseline) | Easy | The score to beat |
| 3 | [Mean Baseline for Regression](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/basics/mean-baseline-for-regression) | Easy | Predict the average |
| 4 | [Standard Scaling (Fit on Train Only)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/basics/standard-scaling-fit-on-train-only) | Medium | z = (x − mean) / std |
| 5 | [Min-Max Scaling](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/basics/min-max-scaling) | Easy | Squeeze into [0, 1] |
| 6 | [Robust Scaling](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/basics/robust-scaling) | Medium | Median and IQR resist outliers |
| 7 | [One-Hot Encoding](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/basics/one-hot-encoding) | Easy | Categories → 0/1 columns |
| 8 | [Label Encoding](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/basics/label-encoding) | Easy | Classes → 0, 1, 2, … |
| 9 | [Ordinal Encoding With an Order](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/basics/ordinal-encoding-with-an-order) | Easy | Low < Medium < High |
| 10 | [Fill Missing Values With the Mean](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/basics/fill-missing-values-with-the-mean) | Easy | Imputation |
| 11 | [Fill Missing Categories With the Mode](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/basics/fill-missing-categories-with-the-mode) | Easy | Most frequent value |
| 12 | [Polynomial Features](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/basics/polynomial-features) | Medium | x₁, x₂ → x₁, x₂, x₁², x₁x₂, x₂² |
| 13 | [Equal-Width Binning](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/basics/equal-width-binning) | Medium | Numbers → bins |
| 14 | [Log Transform a Skewed Feature](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/basics/log-transform-a-skewed-feature) | Easy | log(1 + x) |
| 15 | [Balanced Class Weights](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/basics/balanced-class-weights) | Medium | Help the rare class |
| 16 | [Drop Near-Constant Features](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/basics/drop-near-constant-features) | Easy | Variance threshold |
| 17 | [Select the k Best Features](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/basics/select-the-k-best-features) | Medium | Correlation with the target |
| 18 | [K-Fold Splits](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/basics/k-fold-splits) | Medium | Every row is tested once |
| 19 | [Normalise Each Row](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/basics/normalise-each-row) | Easy | Unit-length samples |
| 20 | [A Scale-Then-Fit Pipeline](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/basics/a-scale-then-fit-pipeline) | Medium | Pipelines prevent leakage |

## Linear Regression

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Fit a Line](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/linear-regression/fit-a-line) | Easy | Least squares |
| 2 | [Predict New Values](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/linear-regression/predict-new-values) | Easy | Using the fitted line |
| 3 | [Multiple Linear Regression](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/linear-regression/multiple-linear-regression) | Medium | Several features |
| 4 | [Mean Squared Error](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/linear-regression/mean-squared-error) | Easy | MSE |
| 5 | [Root Mean Squared Error](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/linear-regression/root-mean-squared-error) | Easy | RMSE — error in the target's units |
| 6 | [Mean Absolute Error](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/linear-regression/mean-absolute-error) | Easy | MAE — robust to outliers |
| 7 | [R² Score](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/linear-regression/r-score) | Medium | Share of variance explained |
| 8 | [Mean Absolute Percentage Error](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/linear-regression/mean-absolute-percentage-error) | Easy | MAPE |
| 9 | [Adjusted R²](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/linear-regression/adjusted-r) | Medium | Penalise useless features |
| 10 | [Residuals](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/linear-regression/residuals) | Easy | What the line missed |
| 11 | [Train by Gradient Descent](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/linear-regression/train-by-gradient-descent) | Medium | Same answer, found by walking downhill |
| 12 | [Polynomial Regression](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/linear-regression/polynomial-regression) | Medium | Curves with a linear model |
| 13 | [Overfitting: Test Error by Degree](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/linear-regression/overfitting-test-error-by-degree) | Hard | Too simple vs too complex |
| 14 | [Ridge Regression (One Feature)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/linear-regression/ridge-regression-one-feature) | Medium | L2 penalty shrinks the slope |
| 15 | [Ridge Path: Stronger Penalty, Smaller Slope](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/linear-regression/ridge-path-stronger-penalty-smaller-slope) | Easy | Effect of α |
| 16 | [Lasso Regression (One Feature)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/linear-regression/lasso-regression-one-feature) | Hard | L1 penalty can zero a weight |
| 17 | [Elastic Net (One Feature)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/linear-regression/elastic-net-one-feature) | Hard | L1 + L2 together |
| 18 | [Which Feature Matters Most?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/linear-regression/which-feature-matters-most) | Medium | Standardised coefficients |
| 19 | [Weighted Least Squares](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/linear-regression/weighted-least-squares) | Medium | Some points count more |
| 20 | [Interaction Features](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/linear-regression/interaction-features) | Hard | x₁·x₂ as a feature |

## Logistic Regression & Classification

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Sigmoid Probabilities](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/logistic-regression/sigmoid-probabilities) | Easy | Score → probability |
| 2 | [Odds and Log-Odds](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/logistic-regression/odds-and-log-odds) | Easy | p → p/(1 − p) → log |
| 3 | [Predict With Given Weights](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/logistic-regression/predict-with-given-weights) | Easy | Which side of the line? |
| 4 | [Binary Log-Loss](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/logistic-regression/binary-log-loss) | Easy | The training loss |
| 5 | [Train Logistic Regression (One Feature)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/logistic-regression/train-logistic-regression-one-feature) | Hard | Newton's method |
| 6 | [Train Logistic Regression (Two Features)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/logistic-regression/train-logistic-regression-two-features) | Hard | Regularised, C = 1 |
| 7 | [Probabilities for New Points](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/logistic-regression/probabilities-for-new-points) | Medium | predict_proba |
| 8 | [Find the Decision Boundary](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/logistic-regression/find-the-decision-boundary) | Medium | Where p = 0.5 |
| 9 | [Odds Ratio of a Feature](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/logistic-regression/odds-ratio-of-a-feature) | Medium | Interpreting a coefficient |
| 10 | [Accuracy](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/logistic-regression/accuracy) | Easy | Share of correct predictions |
| 11 | [Move the Threshold](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/logistic-regression/move-the-threshold) | Easy | Trading precision for recall |
| 12 | [Stronger Regularisation, Smaller Weight](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/logistic-regression/stronger-regularisation-smaller-weight) | Hard | The C parameter |
| 13 | [Class-Weighted Logistic Regression](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/logistic-regression/class-weighted-logistic-regression) | Hard | Imbalanced data |
| 14 | [Softmax for Many Classes](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/logistic-regression/softmax-for-many-classes) | Easy | Scores → class probabilities |
| 15 | [Multiclass Prediction From Weights](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/logistic-regression/multiclass-prediction-from-weights) | Medium | Highest score wins |
| 16 | [Multiclass Log-Loss](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/logistic-regression/multiclass-log-loss) | Medium | Categorical cross-entropy |
| 17 | [One-vs-Rest Targets](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/logistic-regression/one-vs-rest-targets) | Easy | One binary problem per class |
| 18 | [Count the Mistakes](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/logistic-regression/count-the-mistakes) | Easy | Zero-one loss |
| 19 | [Gradient of the Log-Loss](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/logistic-regression/gradient-of-the-log-loss) | Medium | Xᵀ(p − y) / n |
| 20 | [Train a Perceptron](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/logistic-regression/train-a-perceptron) | Hard | The original neural unit |

## Model Evaluation & Validation

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Confusion Matrix](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/evaluation/confusion-matrix) | Easy | Where the mistakes are |
| 2 | [Precision](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/evaluation/precision) | Easy | Of the predicted positives, how many are right? |
| 3 | [Recall](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/evaluation/recall) | Easy | Of the real positives, how many did we catch? |
| 4 | [F1 Score](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/evaluation/f1-score) | Easy | Harmonic mean of precision and recall |
| 5 | [Specificity](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/evaluation/specificity) | Easy | True negative rate |
| 6 | [Macro vs Weighted F1](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/evaluation/macro-vs-weighted-f1) | Medium | Averaging over classes |
| 7 | [Per-Class Precision and Recall](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/evaluation/per-class-precision-and-recall) | Medium | The classification report |
| 8 | [Balanced Accuracy](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/evaluation/balanced-accuracy) | Easy | Average recall over classes |
| 9 | [ROC Curve Points](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/evaluation/roc-curve-points) | Medium | Every threshold at once |
| 10 | [ROC AUC](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/evaluation/roc-auc) | Medium | How well scores rank positives above negatives |
| 11 | [Average Precision (PR AUC)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/evaluation/average-precision-pr-auc) | Hard | Area under precision–recall |
| 12 | [Matthews Correlation Coefficient](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/evaluation/matthews-correlation-coefficient) | Medium | One balanced number |
| 13 | [Cohen's Kappa](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/evaluation/cohens-kappa) | Medium | Agreement beyond chance |
| 14 | [Brier Score](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/evaluation/brier-score) | Easy | Squared error of probabilities |
| 15 | [Best Threshold for F1](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/evaluation/best-threshold-for-f1) | Hard | Tuning the cut-off |
| 16 | [Top-k Accuracy](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/evaluation/top-k-accuracy) | Easy | Right answer among the top guesses |
| 17 | [Cost of Mistakes](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/evaluation/cost-of-mistakes) | Easy | Business-aware evaluation |
| 18 | [Cross-Validated R²](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/evaluation/cross-validated-r) | Medium | Score on every fold |
| 19 | [Leave-One-Out Error](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/evaluation/leave-one-out-error) | Medium | n folds of size 1 |
| 20 | [Time-Series Splits](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/evaluation/time-series-splits) | Medium | Never train on the future |

## k-NN, Naive Bayes & SVM

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Distances to Every Training Point](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/knn-nb-svm/distances-to-every-training-point) | Easy | The heart of k-NN |
| 2 | [Classify One Point With k-NN](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/knn-nb-svm/classify-one-point-with-k-nn) | Easy | Majority vote of the k closest |
| 3 | [k-NN for Many Points](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/knn-nb-svm/k-nn-for-many-points) | Medium | Predicting a whole test set |
| 4 | [k-NN Regression](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/knn-nb-svm/k-nn-regression) | Easy | Average of the neighbours |
| 5 | [Distance-Weighted k-NN](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/knn-nb-svm/distance-weighted-k-nn) | Medium | Closer neighbours count more |
| 6 | [k-NN With Manhattan Distance](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/knn-nb-svm/k-nn-with-manhattan-distance) | Easy | Changing the metric |
| 7 | [Choose k on a Validation Set](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/knn-nb-svm/choose-k-on-a-validation-set) | Medium | Tuning k |
| 8 | [Class Priors](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/knn-nb-svm/class-priors) | Easy | P(class) before seeing features |
| 9 | [Gaussian Naive Bayes: Means per Class](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/knn-nb-svm/gaussian-naive-bayes-means-per-class) | Easy | What GaussianNB learns |
| 10 | [Gaussian Naive Bayes: Variances per Class](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/knn-nb-svm/gaussian-naive-bayes-variances-per-class) | Easy | The width of each bell curve |
| 11 | [Gaussian Naive Bayes: Predict Probabilities](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/knn-nb-svm/gaussian-naive-bayes-predict-probabilities) | Hard | Bayes' rule with bell curves |
| 12 | [Word Probabilities With Laplace Smoothing](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/knn-nb-svm/word-probabilities-with-laplace-smoothing) | Medium | Never multiply by zero |
| 13 | [Multinomial Naive Bayes Classifier](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/knn-nb-svm/multinomial-naive-bayes-classifier) | Hard | Text classification |
| 14 | [Bernoulli Naive Bayes](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/knn-nb-svm/bernoulli-naive-bayes) | Hard | Word present or absent |
| 15 | [Hinge Loss](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/knn-nb-svm/hinge-loss) | Easy | The SVM's loss |
| 16 | [Widest Margin Between Two Points](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/knn-nb-svm/widest-margin-between-two-points) | Hard | Hard-margin SVM |
| 17 | [Margin Width](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/knn-nb-svm/margin-width) | Medium | 2 / ‖w‖ |
| 18 | [Points Inside the Margin](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/knn-nb-svm/points-inside-the-margin) | Medium | Support vectors and violations |
| 19 | [RBF Kernel](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/knn-nb-svm/rbf-kernel) | Easy | Similarity that fades with distance |
| 20 | [The Kernel Trick](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/knn-nb-svm/the-kernel-trick) | Hard | A dot product in a bigger space, without going there |

## Decision Trees

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Gini Impurity of a Node](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/trees/gini-impurity-of-a-node) | Easy | How mixed are the labels? |
| 2 | [Entropy of a Node](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/trees/entropy-of-a-node) | Easy | Impurity in bits |
| 3 | [Weighted Gini of a Given Split](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/trees/weighted-gini-of-a-given-split) | Easy | Scoring one candidate question |
| 4 | [Best Split Threshold](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/trees/best-split-threshold) | Medium | The root question |
| 5 | [Impurity Decrease of the Best Split](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/trees/impurity-decrease-of-the-best-split) | Medium | Information gain (Gini) |
| 6 | [Which Feature Splits Best?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/trees/which-feature-splits-best) | Medium | Choosing the question |
| 7 | [Predict With a Stump](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/trees/predict-with-a-stump) | Easy | One question, two answers |
| 8 | [Leaf Probabilities](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/trees/leaf-probabilities) | Easy | Class shares inside a leaf |
| 9 | [A Depth-2 Tree](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/trees/a-depth-2-tree) | Hard | Growing recursively |
| 10 | [How Deep Does It Grow?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/trees/how-deep-does-it-grow) | Medium | Unlimited depth |
| 11 | [Best-First Growth With a Leaf Budget](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/trees/best-first-growth-with-a-leaf-budget) | Hard | max_leaf_nodes |
| 12 | [Training Accuracy by Depth](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/trees/training-accuracy-by-depth) | Medium | Deeper = memorises more |
| 13 | [Feature Importances](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/trees/feature-importances) | Hard | Mean decrease in impurity |
| 14 | [Minimum Samples per Leaf](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/trees/minimum-samples-per-leaf) | Medium | A brake on overfitting |
| 15 | [Gini vs Entropy](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/trees/gini-vs-entropy) | Medium | Do they pick the same question? |
| 16 | [Which Leaf Does Each Row Reach?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/trees/which-leaf-does-each-row-reach) | Easy | apply() |
| 17 | [Samples in Each Leaf](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/trees/samples-in-each-leaf) | Easy | How the data is divided |
| 18 | [Regression Stump](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/trees/regression-stump) | Medium | Split to reduce squared error |
| 19 | [Regression Tree Predictions](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/trees/regression-tree-predictions) | Medium | Step-shaped curves |
| 20 | [Majority Class at the Root](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/trees/majority-class-at-the-root) | Easy | A tree with no questions |

## Ensembles: Bagging, Forests & Boosting

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Hard Voting by Hand](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/ensembles/hard-voting-by-hand) | Medium | Majority of three models |
| 2 | [Soft Voting](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/ensembles/soft-voting) | Medium | Average the probabilities |
| 3 | [A Bootstrap Sample](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/ensembles/a-bootstrap-sample) | Easy | Sampling with replacement |
| 4 | [Out-of-Bag Rows](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/ensembles/out-of-bag-rows) | Easy | Free validation data |
| 5 | [Chance a Row Is Left Out](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/ensembles/chance-a-row-is-left-out) | Easy | ≈ 1/e ≈ 36.8% |
| 6 | [Forest Probability = Average of Its Trees](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/ensembles/forest-probability-average-of-its-trees) | Medium | Inside a random forest |
| 7 | [Count the Trees' Votes](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/ensembles/count-the-trees-votes) | Easy | How confident is the forest? |
| 8 | [Forest Feature Importances](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/ensembles/forest-feature-importances) | Medium | Averaged over trees |
| 9 | [Bagging = Average of Trees](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/ensembles/bagging-average-of-trees) | Medium | Bagging for regression |
| 10 | [Features Tried at Each Split](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/ensembles/features-tried-at-each-split) | Easy | max_features |
| 11 | [Boosting Starts From the Mean](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/ensembles/boosting-starts-from-the-mean) | Easy | The initial guess |
| 12 | [The First Tree Fits the Residuals](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/ensembles/the-first-tree-fits-the-residuals) | Medium | Learning from mistakes |
| 13 | [Gradient Boosting From Scratch](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/ensembles/gradient-boosting-from-scratch) | Hard | Add stumps that fix the residuals |
| 14 | [Watching Boosting Improve](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/ensembles/watching-boosting-improve) | Medium | Staged predictions |
| 15 | [Learning Rate vs Training Error](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/ensembles/learning-rate-vs-training-error) | Medium | Shrinkage |
| 16 | [Weighted Error of a Weak Learner](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/ensembles/weighted-error-of-a-weak-learner) | Easy | AdaBoost, step 1 |
| 17 | [AdaBoost: How Much Say Does a Model Get?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/ensembles/adaboost-how-much-say-does-a-model-get) | Medium | α = ln((1 − err)/err) + ln(K − 1) |
| 18 | [AdaBoost: Reweight the Mistakes](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/ensembles/adaboost-reweight-the-mistakes) | Medium | Focus on the hard rows |
| 19 | [Why Averaging Helps](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/ensembles/why-averaging-helps) | Medium | Variance of an average of models |
| 20 | [Stacking: Learn How to Blend](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/ensembles/stacking-learn-how-to-blend) | Hard | A model on top of models |

## Clustering & Unsupervised Learning

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Assign Points to the Nearest Centre](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/clustering/assign-points-to-the-nearest-centre) | Easy | k-means step 1 |
| 2 | [Move Each Centre to Its Points' Mean](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/clustering/move-each-centre-to-its-points-mean) | Easy | k-means step 2 |
| 3 | [k-Means From Scratch](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/clustering/k-means-from-scratch) | Hard | Repeat assign + update until stable |
| 4 | [Inertia](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/clustering/inertia) | Easy | Within-cluster sum of squares |
| 5 | [The Elbow Curve](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/clustering/the-elbow-curve) | Medium | Inertia for k = 1 … K |
| 6 | [Cluster Sizes](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/clustering/cluster-sizes) | Easy | How many points in each cluster? |
| 7 | [Predict the Cluster of New Points](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/clustering/predict-the-cluster-of-new-points) | Easy | Using a fitted k-means |
| 8 | [Silhouette of Each Point](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/clustering/silhouette-of-each-point) | Medium | (b − a) / max(a, b) |
| 9 | [Silhouette Score](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/clustering/silhouette-score) | Easy | One number for cluster quality |
| 10 | [Choose k by Silhouette](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/clustering/choose-k-by-silhouette) | Medium | Best number of clusters |
| 11 | [Hierarchical Clustering: Single Linkage](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/clustering/hierarchical-clustering-single-linkage) | Medium | Merge the closest pair of points |
| 12 | [Hierarchical Clustering: Complete Linkage](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/clustering/hierarchical-clustering-complete-linkage) | Medium | Merge by the farthest members |
| 13 | [Hierarchical Clustering: Ward](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/clustering/hierarchical-clustering-ward) | Hard | Merge with the smallest rise in SSE |
| 14 | [DBSCAN](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/clustering/dbscan) | Hard | Clusters of any shape, plus noise |
| 15 | [DBSCAN Core Points](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/clustering/dbscan-core-points) | Medium | Who has enough neighbours? |
| 16 | [Rand Index](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/clustering/rand-index) | Medium | Do two clusterings agree? |
| 17 | [Contingency Table](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/clustering/contingency-table) | Easy | True classes vs found clusters |
| 18 | [PCA Explained Variance](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/clustering/pca-explained-variance) | Medium | How much each direction keeps |
| 19 | [Project Onto the First Component](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/clustering/project-onto-the-first-component) | Medium | Dimensionality reduction |
| 20 | [Distance-Based Outliers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/clustering/distance-based-outliers) | Medium | Far from your k-th neighbour |

## Tuning, Pipelines & Regularisation

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Expand a Parameter Grid](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/tuning/expand-a-parameter-grid) | Easy | Every combination |
| 2 | [Grid Search by Hand](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/tuning/grid-search-by-hand) | Medium | Pick k with cross-validation |
| 3 | [Mean and Spread of CV Scores](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/tuning/mean-and-spread-of-cv-scores) | Easy | Report mean ± std |
| 4 | [Validation Curve](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/tuning/validation-curve) | Medium | Train vs validation score per setting |
| 5 | [Learning Curve](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/tuning/learning-curve) | Medium | Would more data help? |
| 6 | [Choose the Polynomial Degree by CV](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/tuning/choose-the-polynomial-degree-by-cv) | Medium | Grid search over a pipeline step |
| 7 | [Ridge With Several Features](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/tuning/ridge-with-several-features) | Medium | Closed form vs library |
| 8 | [RidgeCV: Pick α by Leave-One-Out](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/tuning/ridgecv-pick-by-leave-one-out) | Hard | Built-in efficient CV |
| 9 | [ColumnTransformer: Numbers and Categories](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/tuning/columntransformer-numbers-and-categories) | Medium | Different steps per column |
| 10 | [A Full Preprocessing Pipeline](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/tuning/a-full-preprocessing-pipeline) | Medium | Impute → scale → model |
| 11 | [Leakage From Feature Selection](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/tuning/leakage-from-feature-selection) | Hard | Why selection belongs inside the pipeline |
| 12 | [What the Scaler Learns in Each Fold](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/tuning/what-the-scaler-learns-in-each-fold) | Medium | Pipelines refit per fold |
| 13 | [How Many Models Does a Grid Search Train?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/tuning/how-many-models-does-a-grid-search-train) | Easy | The cost of tuning |
| 14 | [A Custom Scorer](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/tuning/a-custom-scorer) | Easy | Negative MAE |
| 15 | [Predict on a Log Scale](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/tuning/predict-on-a-log-scale) | Medium | TransformedTargetRegressor |
| 16 | [Combine Feature Sets](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/tuning/combine-feature-sets) | Easy | FeatureUnion |
| 17 | [Missing-Value Indicator Columns](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/tuning/missing-value-indicator-columns) | Easy | Keep the fact that it was missing |
| 18 | [Tune C for Logistic Regression](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/tuning/tune-c-for-logistic-regression) | Medium | Regularisation strength by CV |
| 19 | [Refit the Winner and Predict](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/tuning/refit-the-winner-and-predict) | Medium | best_estimator_ |
| 20 | [LassoCV: Pick α by K-Fold](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ml/#/q/tuning/lassocv-pick-by-k-fold) | Hard | Sparse model, tuned |

## Build

```bash
python3 handbook/build.py --book ml
```

Sources live in `ml/src/`: `topics/` (questions and solutions), `lessons/` and `theory/`.
