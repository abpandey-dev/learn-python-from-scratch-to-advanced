from lib import *
import numpy as np
import matplotlib.pyplot as plt

LESSON("Basics", "Feature engineering", """
<p>Models only see numbers, and how you build them often matters more than which model you pick.</p>
<ul>
<li><b>Categories</b>: one-hot for a few values; <b>target encoding</b> (mean target per category, smoothed and computed out-of-fold) for many values like city or product id; never plain integer codes for unordered categories in linear models.</li>
<li><b>Dates</b>: weekday, month, holiday flags, and <i>recency</i> (days since the last event) usually beat the raw date.</li>
<li><b>Ratios and interactions</b>: spend per visit, price × quantity — domain knowledge turned into columns.</li>
<li><b>Selection</b>: drop constant and near-duplicate columns; check importance on held-out data.</li>
<li><b>Leakage</b>: any column recorded after the outcome (a refund flag when predicting churn) makes offline scores great and production useless. A near-perfect single feature is a red flag.</li>
</ul>
<pre><code class="py">from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, TargetEncoder, StandardScaler
prep = ColumnTransformer([
    ("few", OneHotEncoder(handle_unknown="ignore"), ["plan", "region"]),
    ("many", TargetEncoder(), ["city"]),            # cross-fitted internally to avoid leakage
    ("num", StandardScaler(), ["tenure", "spend"]),
])</code></pre>
""", practice=["One-Hot Encode Categories", "Smoothed Target Encoding", "Features From Dates", "Drop Useless and Redundant Features", "Spot Leaky Features"])

LESSON("Core", "Finding anomalies", """
<p>Fraud, faulty sensors and data bugs are rare and usually unlabelled. Start simple, then add context:</p>
<table>
<tr><th>Method</th><th>Good for</th><th>Watch out</th></tr>
<tr><td>z-score</td><td>roughly normal data</td><td>a huge outlier inflates the std and hides others</td></tr>
<tr><td>IQR fences / MAD</td><td>skewed data, robust</td><td>one feature at a time</td></tr>
<tr><td>k-NN distance</td><td>several clusters, many features</td><td>needs scaling; slow on big data without an index</td></tr>
<tr><td>Isolation Forest</td><td>many features, big data</td><td>random; set <code>random_state</code></td></tr>
<tr><td>Seasonal baselines</td><td>time series</td><td>see the time-series topic</td></tr>
</table>
<p>Evaluate with labelled examples when you have some: precision@k (how many of the top alerts are real) and average precision — never accuracy.</p>
<pre><code class="py">from sklearn.ensemble import IsolationForest
iso = IsolationForest(contamination=0.01, random_state=0).fit(X)
scores = -iso.score_samples(X)          # higher = more anomalous</code></pre>
""", practice=["Z-Score Outliers", "Tukey's IQR Fences", "Robust Z-Scores With the MAD", "Anomalies by Distance to Neighbours", "Score an Anomaly Detector"])


@LD
def outlier_picture():
    amounts = np.array([120, 95, 130, 110, 105, 98, 2400, 115, 101, 125, 90, 108, 15, 112, 99, 118, 1050, 104])
    q1, q3 = np.percentile(amounts, [25, 75])
    hi = q3 + 1.5 * (q3 - q1)
    fig, ax = plt.subplots(figsize=(6, 2.4))
    ax.scatter(range(len(amounts)), amounts, c=["#b91c1c" if a > hi or a < q1 - 1.5 * (q3 - q1) else "#0f766e" for a in amounts])
    ax.axhline(hi, ls="--", color="#94a3b8")
    ax.set_yscale("log"); ax.set_title("IQR fences flag the red points")


LESSON("Core", "Pictures of high-dimensional data", """
<p><b>PCA</b> is linear and keeps global structure. <b>t-SNE</b> and <b>UMAP</b> are non-linear and great at showing clusters — but they can stretch distances and invent closeness. Cluster sizes and gaps between clusters in a t-SNE plot mean little. Check a picture with <b>trustworthiness</b> (are 2-D neighbours real neighbours?) before drawing conclusions.</p>
<pre><code class="py">from sklearn.manifold import TSNE, trustworthiness
emb = TSNE(n_components=2, perplexity=30, random_state=0).fit_transform(X)
trustworthiness(X, emb, n_neighbors=10)      # close to 1 = faithful
import umap; emb = umap.UMAP(n_neighbors=15, min_dist=0.1).fit_transform(X)</code></pre>
""", practice=["Can You Trust That t-SNE Plot?"])

LESSON("Core", "Classic NLP", """
<p>Before reaching for an LLM, try the fast baselines: they're cheap, explainable and often good enough.</p>
<ul>
<li><b>Bag of words / n-grams</b> → counts or TF-IDF → <b>Naive Bayes</b> or logistic regression. Bigrams capture "not good" and "fast delivery".</li>
<li><b>Named-entity recognition</b> labels tokens with BIO tags and is scored on whole entities.</li>
<li><b>Transformers</b> (BERT-style) fine-tuned on your labels beat both when data and budget allow; LLMs with a prompt work with no training data.</li>
</ul>
<pre><code class="py">from sklearn.pipeline import make_pipeline
clf = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), min_df=2), LogisticRegression(max_iter=1000)).fit(texts, y)

import spacy; [(e.text, e.label_) for e in spacy.load("en_core_web_sm")("Asha flew to Pune").ents]
from transformers import pipeline; pipeline("sentiment-analysis")("Great battery!")</code></pre>
""", practice=["Bag of Words", "Classify Text With Naive Bayes", "Most Common Bigrams", "Tag Entities With BIO Labels", "Score Entity Predictions"])

LESSON("Advanced", "Computer vision: detection and transfer learning", """
<p><b>Object detection</b> predicts boxes with classes and scores. Three ideas run through every detector (YOLO, Faster R-CNN, DETR):</p>
<ul>
<li><b>IoU</b> measures box overlap.</li>
<li><b>Non-maximum suppression</b> removes duplicate boxes for one object.</li>
<li>Predictions are <b>matched</b> to ground truth at an IoU threshold to count TP/FP/FN; averaging precision over recall levels and classes gives <b>mAP</b>.</li>
</ul>
<p><b>Transfer learning</b> starts from a model pretrained on millions of images, freezes most of it, and trains a small head on your few hundred labelled images — far less data and compute.</p>
<pre><code class="py">import torchvision
model = torchvision.models.resnet50(weights="IMAGENET1K_V2")
for p in model.parameters():
    p.requires_grad = False                          # freeze the backbone
model.fc = torch.nn.Linear(model.fc.in_features, 5)  # new head for 5 classes

from torchvision.ops import box_iou, nms
keep = nms(boxes, scores, iou_threshold=0.5)
from ultralytics import YOLO; YOLO("yolo11n.pt")("street.jpg")</code></pre>
""", practice=["Intersection over Union", "Non-Maximum Suppression", "Match Detections to Ground Truth", "Transfer Learning: What Gets Trained?"])
