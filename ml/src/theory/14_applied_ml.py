from lib import *

THEORY("Which encoder for which column?", """
<table>
<tr><th>Column</th><th>Encoding</th></tr>
<tr><td>few categories, no order</td><td>one-hot</td></tr>
<tr><td>many categories (ids, cities)</td><td>target encoding (cross-fitted), hashing, or embeddings</td></tr>
<tr><td>ordered categories (S/M/L)</td><td>ordinal integers</td></tr>
<tr><td>dates and times</td><td>parts (weekday, month, hour) + recency</td></tr>
<tr><td>text</td><td>counts/TF-IDF, or embeddings from a language model</td></tr>
</table>
<p>Tree models (gradient boosting) need less scaling and handle interactions themselves; linear models and k-NN need scaled, well-encoded inputs.</p>
""")

THEORY("Detection metrics", """
<ul>
<li><b>IoU ≥ 0.5</b> is the classic match threshold (PASCAL VOC); COCO averages mAP over IoU 0.5–0.95.</li>
<li><b>Precision</b>: how many predicted boxes were right. <b>Recall</b>: how many objects were found.</li>
<li><b>mAP</b>: area under the precision–recall curve, averaged over classes.</li>
</ul>
""")

FAQ("What is target leakage and how do you catch it?", "<p>A feature that contains information unavailable at prediction time — often something recorded after the outcome. Catch it by checking when each column is created, by suspiciously high single-feature scores, and by a time-based validation split.</p>")
FAQ("How do you detect anomalies without labels?", "<p>Start with robust statistics (IQR, MAD) per feature, then multivariate methods such as k-NN distance or Isolation Forest; review the top-scored cases with domain experts and turn their feedback into labels for evaluation.</p>")
FAQ("Why not trust distances in a t-SNE plot?", "<p>t-SNE preserves local neighbourhoods, not global distances or densities, so cluster sizes and gaps can be misleading. Check trustworthiness and compare with PCA.</p>")
FAQ("When would you use Naive Bayes over a transformer?", "<p>As a fast, cheap baseline with little data or compute, or when you need speed and interpretability. A fine-tuned transformer wins when accuracy matters and you have labelled data and GPU budget.</p>")
FAQ("What does non-maximum suppression do?", "<p>It removes duplicate detections of the same object by keeping the highest-scoring box and discarding others that overlap it beyond an IoU threshold.</p>")
FAQ("Why freeze layers in transfer learning?", "<p>The pretrained layers already detect general features (edges, textures, shapes). Freezing them means fewer parameters to train, so you need far less data and avoid overfitting; unfreeze top layers later to fine-tune.</p>")
