from lib import *

THEORY("Clustering algorithms", """
<table>
<tr><th>Algorithm</th><th>Needs k?</th><th>Shapes</th><th>Noise</th><th>Scale</th></tr>
<tr><td>k-means</td><td>yes</td><td>round, similar size</td><td>no</td><td>very large (MiniBatchKMeans)</td></tr>
<tr><td>Gaussian mixture</td><td>yes</td><td>ellipses, soft assignments</td><td>no</td><td>medium</td></tr>
<tr><td>Agglomerative</td><td>yes (or a distance cut)</td><td>depends on linkage</td><td>no</td><td>O(n²) memory</td></tr>
<tr><td>DBSCAN / HDBSCAN</td><td>no (eps, min_samples)</td><td>arbitrary</td><td>yes</td><td>large with an index</td></tr>
<tr><td>Mean shift</td><td>no (bandwidth)</td><td>blobs</td><td>no</td><td>small</td></tr>
<tr><td>Spectral</td><td>yes</td><td>non-convex, graphs</td><td>no</td><td>small–medium</td></tr>
</table>
""")

THEORY("k-means in detail", """
<p>Objective: minimise inertia J = Σᵢ ‖xᵢ − μ_{c(i)}‖². Lloyd's algorithm alternates assignment and centroid update; each step can only lower J, so it converges — but to a <b>local</b> minimum. k-means++ picks spread-out initial centres (each new centre chosen with probability ∝ squared distance to the nearest existing centre). Assumes spherical, equally sized clusters; sensitive to scale and outliers. Complexity O(n·k·d) per iteration.</p>
""")

THEORY("Cluster validation", """
<table>
<tr><th>Score</th><th>Needs labels?</th><th>Meaning</th></tr>
<tr><td>Inertia (elbow)</td><td>no</td><td>compactness; always falls with k</td></tr>
<tr><td>Silhouette</td><td>no</td><td>(b − a)/max(a, b), −1 … 1</td></tr>
<tr><td>Davies–Bouldin</td><td>no</td><td>lower is better</td></tr>
<tr><td>Calinski–Harabasz</td><td>no</td><td>between/within dispersion, higher better</td></tr>
<tr><td>Rand / adjusted Rand</td><td>yes</td><td>pair agreement (ARI: 0 = chance, 1 = identical)</td></tr>
<tr><td>Normalised mutual information</td><td>yes</td><td>shared information, 0 … 1</td></tr>
<tr><td>Homogeneity / completeness / V-measure</td><td>yes</td><td>each cluster one class / each class one cluster</td></tr>
</table>
""")

THEORY("Other unsupervised tasks", """
<ul>
<li><b>Dimensionality reduction</b>: PCA (linear, keeps variance), truncated SVD (sparse text), t-SNE / UMAP (visualisation), autoencoders.</li>
<li><b>Anomaly detection</b>: distance to k-th neighbour, Local Outlier Factor, Isolation Forest, One-class SVM, DBSCAN noise.</li>
<li><b>Association rules</b>: frequent itemsets (market baskets), support / confidence / lift.</li>
<li><b>Density estimation</b>: kernel density estimates, Gaussian mixtures.</li>
</ul>
""")

FAQ("How does k-means work?", "<p>It alternates assigning each point to the nearest centroid and moving each centroid to the mean of its points, until assignments stop changing, minimising within-cluster squared distance.</p>")
FAQ("How do you choose k?", "<p>Elbow of the inertia curve, highest silhouette, information criteria for Gaussian mixtures, stability across resamples, and what is useful for the business problem.</p>")
FAQ("What are k-means' limitations?", "<p>Needs k; assumes round, similar-sized clusters; sensitive to initialisation, scaling and outliers; only finds local optima; can't model noise or odd shapes.</p>")
FAQ("When would you use DBSCAN instead of k-means?", "<p>When clusters have irregular shapes, when you don't know k, or when you need to flag noise points — provided clusters have similar density.</p>")
FAQ("Single vs complete vs Ward linkage?", "<p>Single merges by nearest members (finds chains, prone to 'chaining' noise); complete by farthest members (compact clusters); Ward by the smallest increase in variance (balanced, k-means-like).</p>")
FAQ("How do you evaluate clustering without labels?", "<p>Internal measures such as silhouette, Davies–Bouldin and Calinski–Harabasz, plus visual inspection (e.g. PCA plots) and checking whether clusters are stable and meaningful to domain experts.</p>")
