from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.metrics import silhouette_score

rng = np.random.default_rng(3)
BLOBS = np.vstack([rng.normal(c, 0.6, (25, 2)) for c in ([1, 1], [5, 5], [1, 6])])

LESSON("Basics", "Unsupervised learning and k-means", """
<p>No labels this time — just data. <b>Clustering</b> groups similar rows: customer segments, document topics, image regions.</p>
<p><b>k-means</b> finds k groups:</p>
<ol>
<li>Pick k starting centres.</li>
<li><b>Assign</b> each point to its nearest centre.</li>
<li><b>Update</b> each centre to the mean of its points.</li>
<li>Repeat 2–3 until nothing changes.</li>
</ol>
<p>It minimises <b>inertia</b> (sum of squared distances to centres). The result depends on the start, so sklearn runs several starts (<code>n_init</code>) with smart <b>k-means++</b> initialisation and keeps the best.</p>
""", practice=["Assign Points to the Nearest Centre", "Move Each Centre to Its Points' Mean", "k-Means From Scratch", "Inertia", "Predict the Cluster of New Points", "Cluster Sizes"])


@LD
def kmeans_steps():
    centers = BLOBS[[0, 1, 2]].copy()
    fig, axes = plt.subplots(1, 3, figsize=(8.5, 2.7))
    for step, ax in enumerate(axes):
        d = ((BLOBS[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
        labels = d.argmin(axis=1)
        ax.scatter(BLOBS[:, 0], BLOBS[:, 1], c=labels, cmap="tab10", s=10)
        ax.scatter(centers[:, 0], centers[:, 1], marker="X", s=120, color="black")
        ax.set_title(f"iteration {step + 1}", fontsize=8)
        centers = np.array([BLOBS[labels == c].mean(axis=0) for c in range(3)])
    fig.tight_layout()


LESSON("Core", "How many clusters?", """
<p>k-means needs k up front. Two common guides:</p>
<ul>
<li><b>Elbow</b>: plot inertia against k. It always falls; look for the bend where adding clusters stops helping much.</li>
<li><b>Silhouette</b>: for each point, a = mean distance to its own cluster, b = mean distance to the nearest other cluster; s = (b − a)/max(a, b). Near 1 = well placed, near 0 = on a border, negative = probably in the wrong cluster. Pick the k with the highest average.</li>
</ul>
<p>Domain knowledge matters too — "three customer tiers" may be the useful answer even if the math prefers four.</p>
""", practice=["The Elbow Curve", "Silhouette of Each Point", "Silhouette Score", "Choose k by Silhouette"])


@LD
def elbow_silhouette():
    ks = range(2, 8)
    inertias, sils = [], []
    for k in ks:
        km = KMeans(n_clusters=k, n_init=5, random_state=0).fit(BLOBS)
        inertias.append(km.inertia_)
        sils.append(silhouette_score(BLOBS, km.labels_))
    fig, (left, right) = plt.subplots(1, 2, figsize=(7.5, 2.8))
    left.plot(list(ks), inertias, "o-")
    left.set_title("elbow at k = 3", fontsize=9)
    right.plot(list(ks), sils, "o-", color="#b45309")
    right.set_title("silhouette peaks at k = 3", fontsize=9)
    fig.tight_layout()


LESSON("Core", "Hierarchical clustering", """
<p>Start with every point as its own cluster and repeatedly <b>merge the two closest clusters</b>. The merge history forms a tree (a <b>dendrogram</b>); cut it at any level to get that many clusters. "Closest" is the <b>linkage</b>:</p>
<table><tr><th>Linkage</th><th>Distance between clusters</th><th>Behaviour</th></tr>
<tr><td>single</td><td>closest pair of members</td><td>follows chains, odd shapes; sensitive to noise</td></tr>
<tr><td>complete</td><td>farthest pair</td><td>compact clusters</td></tr>
<tr><td>average</td><td>mean of all pairs</td><td>in between</td></tr>
<tr><td>ward</td><td>increase in within-cluster SSE</td><td>like k-means; the default</td></tr></table>
""", practice=["Hierarchical Clustering: Single Linkage", "Hierarchical Clustering: Complete Linkage", "Hierarchical Clustering: Ward"])


@LD
def moons_linkage():
    t = np.linspace(0, np.pi, 40)
    moons = np.vstack([np.column_stack([np.cos(t), np.sin(t)]), np.column_stack([1 - np.cos(t), 0.5 - np.sin(t)])])
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 2.6))
    for ax, link in zip(axes, ["single", "ward"]):
        labels = AgglomerativeClustering(n_clusters=2, linkage=link).fit_predict(moons)
        ax.scatter(moons[:, 0], moons[:, 1], c=labels, cmap="coolwarm", s=10)
        ax.set_title(f"{link} linkage", fontsize=9)
    fig.tight_layout()


LESSON("Advanced", "DBSCAN: density, shapes and noise", """
<p><b>DBSCAN</b> defines clusters as dense regions:</p>
<ul>
<li>A <b>core point</b> has at least min_samples points within distance eps.</li>
<li>Clusters grow from core points through their neighbours; border points join but don't spread it further.</li>
<li>Points reachable from no core point are <b>noise</b> (label −1) — built-in outlier detection.</li>
</ul>
<p>No need to choose k, finds any shape, but struggles when clusters have very different densities. Choose eps from a "k-distance plot" (distance to each point's k-th neighbour, sorted — look for the knee).</p>
""", practice=["DBSCAN", "DBSCAN Core Points", "Distance-Based Outliers"])


@LD
def dbscan_vs_kmeans():
    t = np.linspace(0, np.pi, 50)
    moons = np.vstack([np.column_stack([np.cos(t), np.sin(t)]), np.column_stack([1 - np.cos(t), 0.5 - np.sin(t)]), [[2.5, 1.5], [-1.2, -0.6]]])
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 2.6))
    for ax, (name, model) in zip(axes, [("k-means", KMeans(n_clusters=2, n_init=5, random_state=0)), ("DBSCAN", DBSCAN(eps=0.25, min_samples=3))]):
        labels = model.fit_predict(moons)
        ax.scatter(moons[:, 0], moons[:, 1], c=labels, cmap="coolwarm", s=10)
        ax.set_title(f"{name}" + (" (grey = noise)" if name == "DBSCAN" else ""), fontsize=9)
    fig.tight_layout()


LESSON("Advanced", "Evaluating clusters and reducing dimensions", """
<p>Without labels, use internal scores (silhouette, Davies–Bouldin). If true classes exist for a sample, compare with external scores: a <b>contingency table</b>, the <b>Rand index</b> (share of point pairs treated the same way; the adjusted version corrects for chance), homogeneity and completeness. Cluster numbers are arbitrary — only the grouping matters.</p>
<p><b>PCA</b> (from the math course) is the other classic unsupervised tool: compress many correlated features into a few components, often before clustering or to plot data in 2-D. t-SNE and UMAP make prettier 2-D maps but distort distances.</p>
""", practice=["Rand Index", "Contingency Table", "PCA Explained Variance", "Project Onto the First Component"])


@LD
def pca_then_cluster():
    from sklearn.decomposition import PCA
    data = np.hstack([BLOBS, BLOBS @ np.array([[0.5, 0.2], [0.1, 0.7]]) + rng.normal(0, 0.1, BLOBS.shape)])
    reduced = PCA(n_components=2).fit_transform(data)
    labels = KMeans(n_clusters=3, n_init=5, random_state=0).fit_predict(reduced)
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.scatter(reduced[:, 0], reduced[:, 1], c=labels, cmap="tab10", s=10)
    ax.set_title("4 features → PCA → 2-D, then k-means", fontsize=8)


LESSON("Basics", "k-means by hand", """
<p>Six numbers on a line: 1, 2, 3, 10, 11, 12. Use k = 2 with a poor start: centres at 1 and 2.</p>
<table><tr><th>Round</th><th>Centres</th><th>Cluster A</th><th>Cluster B</th><th>New centres</th><th>Inertia</th></tr>
<tr><td>1</td><td>1, 2</td><td>1</td><td>2, 3, 10, 11, 12</td><td>1, 7.6</td><td>89.2</td></tr>
<tr><td>2</td><td>1, 7.6</td><td>1, 2, 3</td><td>10, 11, 12</td><td>2, 11</td><td>4.0</td></tr>
<tr><td>3</td><td>2, 11</td><td>1, 2, 3</td><td>10, 11, 12</td><td>2, 11</td><td>4.0 (no change: stop)</td></tr></table>
<p>Check round 2: 3 is 2 from centre 1 and 4.6 from centre 7.6, so it joins A. Check the final inertia: each cluster contributes 1 + 0 + 1 = 2, for a total of 4.</p>
<h4>Why it always stops</h4>
<p>Assigning points to the nearest centre can only lower inertia, and so can moving a centre to the mean (the mean minimises squared distance). There are finitely many groupings, so it must stop.</p>
<p>But stopping isn't the same as finding the best answer. It only reaches a <b>local</b> minimum, so <code>n_init</code> runs it from several starts and keeps the lowest inertia.</p>
""", practice=["Assign Points to the Nearest Centre", "Move Each Centre to Its Points' Mean", "k-Means From Scratch", "Inertia"])


@LD
def kmeans_by_hand():
    points = np.array([1.0, 2, 3, 10, 11, 12])
    centres = np.array([1.0, 2.0])
    history = []
    for round_number in range(4):
        labels = np.abs(points[:, None] - centres).argmin(axis=1)
        new_centres = np.array([points[labels == k].mean() for k in range(2)])
        inertia = ((points - new_centres[labels]) ** 2).sum()
        history.append((new_centres.tolist(), float(inertia)))
        if (new_centres == centres).all():
            break
        centres = new_centres


LESSON("Core", "When k-means fails", """
<p>k-means assumes round, similar-sized clusters, because each point simply joins its nearest centre. The boundary between two centres is always a straight line.</p>
<table><tr><th>Data</th><th>What goes wrong</th><th>Try</th></tr>
<tr><td>Stretched clusters</td><td>cuts across them</td><td>Gaussian mixture, or rescale</td></tr>
<tr><td>Rings or moons</td><td>can't follow shapes</td><td>DBSCAN, spectral clustering</td></tr>
<tr><td>A small cluster beside a large one</td><td>splits the large one</td><td>Gaussian mixture, DBSCAN</td></tr>
<tr><td>Features on different scales</td><td>the largest feature decides everything</td><td>standardise first</td></tr>
<tr><td>Outliers</td><td>drag the means away</td><td>remove them first, k-medoids, DBSCAN</td></tr></table>
<h4>k-means++</h4>
<p>Starting centres matter. k-means++ chooses the first at random, then picks each next one with probability proportional to its <b>squared distance</b> from the nearest centre already chosen. This spreads them out, and it's sklearn's default.</p>
<h4>Soft clustering</h4>
<p>A <b>Gaussian mixture</b> treats each cluster as a bell curve with its own shape, and gives probabilities: "70% cluster A, 30% cluster B".</p>
""", practice=["The Elbow Curve", "Cluster Sizes", "Predict the Cluster of New Points"])


@LD
def kmeans_failures():
    from sklearn.mixture import GaussianMixture
    from sklearn.metrics import adjusted_rand_score
    r = np.random.default_rng(0)
    centres = np.array([[-2.4, 1.2], [0, -2.4], [2.4, 1.2]])
    round_blobs = np.vstack([r.normal(c, 0.6, (100, 2)) for c in centres])
    stretched = round_blobs @ np.array([[1, -0.9], [-0.8, 1]])
    truth = np.repeat([0, 1, 2], 100)
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 2.8), sharey=True)
    models = [("k-means", KMeans(n_clusters=3, n_init=5, random_state=0)), ("Gaussian mixture", GaussianMixture(n_components=3, random_state=0))]
    for ax, (name, model) in zip(axes, models):
        labels = model.fit_predict(stretched)
        ax.scatter(stretched[:, 0], stretched[:, 1], c=labels, cmap="tab10", s=8)
        ax.set_title(f"{name}: agreement with truth {adjusted_rand_score(truth, labels):.2f}", fontsize=8)
    fig.tight_layout()


LESSON("Core", "Silhouette by hand", """
<p>Clusters {1, 2, 3} and {10, 11, 12}. Calculate the silhouette for two points.</p>
<h4>Point 1</h4>
<ul><li>a = mean distance to its own cluster: (1 + 2) / 2 = 1.5</li>
<li>b = mean distance to the other cluster: (9 + 10 + 11) / 3 = 10</li>
<li>s = (10 − 1.5) / 10 = <b>0.85</b></li></ul>
<h4>Point 3 (nearer the other cluster)</h4>
<ul><li>a = (2 + 1) / 2 = 1.5</li>
<li>b = (7 + 8 + 9) / 3 = 8</li>
<li>s = (8 − 1.5) / 8 = <b>0.8125</b></li></ul>
<table><tr><th>s</th><th>Meaning</th></tr>
<tr><td>Near 1</td><td>tight, well separated</td></tr><tr><td>Near 0</td><td>on the border between clusters</td></tr><tr><td>Negative</td><td>closer to another cluster: possibly misplaced</td></tr></table>
<p>Inertia always falls as k grows, so it can't choose k alone. Silhouette can go up or down, so it can. The average can hide a poor cluster, so a <b>silhouette plot</b> (one bar per point) shows each cluster separately.</p>
""", practice=["Silhouette of Each Point", "Silhouette Score", "Choose k by Silhouette"])


@LD
def silhouette_plot():
    from sklearn.metrics import silhouette_samples
    labels = KMeans(n_clusters=3, n_init=5, random_state=0).fit_predict(BLOBS)
    values = silhouette_samples(BLOBS, labels)
    fig, ax = plt.subplots(figsize=(4.6, 3))
    y = 0
    for c in range(3):
        part = np.sort(values[labels == c])
        ax.barh(np.arange(y, y + len(part)), part, height=1)
        y += len(part) + 4
    ax.axvline(values.mean(), ls="--", color="black")
    ax.set_xlabel("silhouette (dashed line = average)")
    ax.set_yticks([])


LESSON("Advanced", "Hierarchical clustering by hand", """
<p>Five points: 1, 2, 4, 8, 9. Start with each alone, and merge the closest pair each time.</p>
<table><tr><th>Step</th><th>Single linkage merges</th><th>At distance</th><th>Complete linkage merges</th><th>At distance</th></tr>
<tr><td>1</td><td>{1} + {2}</td><td>1</td><td>{1} + {2}</td><td>1</td></tr>
<tr><td>2</td><td>{8} + {9}</td><td>1</td><td>{8} + {9}</td><td>1</td></tr>
<tr><td>3</td><td>{1, 2} + {4}</td><td>2 (from 2 to 4)</td><td>{1, 2} + {4}</td><td>3 (from 1 to 4)</td></tr>
<tr><td>4</td><td>{1, 2, 4} + {8, 9}</td><td>4 (from 4 to 8)</td><td>{1, 2, 4} + {8, 9}</td><td>8 (from 1 to 9)</td></tr></table>
<h4>Reading a dendrogram</h4>
<p>The height of each join is the distance at which clusters merged. <b>To choose clusters, cut horizontally across a large gap.</b> Here the jump from 2 to 4 under single linkage suggests two clusters: {1, 2, 4} and {8, 9}.</p>
<p>You don't need to decide k in advance, and the tree shows structure at every level. But it needs O(n²) memory and merges can never be undone.</p>
""", practice=["Hierarchical Clustering: Single Linkage", "Hierarchical Clustering: Complete Linkage", "Hierarchical Clustering: Ward"])


@LD
def dendrogram_demo():
    from scipy.cluster.hierarchy import dendrogram, linkage
    points = np.array([[1.0], [2.0], [4.0], [8.0], [9.0]])
    merges = linkage(points, method="single")
    fig, ax = plt.subplots(figsize=(4.6, 2.9))
    dendrogram(merges, labels=["1", "2", "4", "8", "9"], ax=ax)
    ax.axhline(3, ls="--", color="gray")
    ax.set_ylabel("merge distance")
    ax.set_title("Cutting at the dashed line gives two clusters", fontsize=9)


LESSON("Advanced", "DBSCAN by hand, and choosing eps", """
<p>Points: 1, 1.5, 2, 2.2, 8, 8.3, 8.5, 15, with eps = 0.6 and min_samples = 3 (counting the point itself).</p>
<table><tr><th>Point</th><th>Within 0.6</th><th>Count</th><th>Type</th><th>Result</th></tr>
<tr><td>1</td><td>1, 1.5</td><td>2</td><td>border</td><td>cluster 0</td></tr>
<tr><td>1.5</td><td>1, 1.5, 2</td><td>3</td><td>core</td><td>cluster 0</td></tr>
<tr><td>2</td><td>1.5, 2, 2.2</td><td>3</td><td>core</td><td>cluster 0</td></tr>
<tr><td>2.2</td><td>2, 2.2</td><td>2</td><td>border</td><td>cluster 0</td></tr>
<tr><td>8, 8.3, 8.5</td><td>all three</td><td>3</td><td>core</td><td>cluster 1</td></tr>
<tr><td>15</td><td>15</td><td>1</td><td>noise</td><td>−1</td></tr></table>
<p>Clusters spread only through core points. Point 1 joins because it's within reach of core point 1.5, but it can't extend the cluster further.</p>
<h4>Choosing the settings</h4>
<ol><li>min_samples: start at about 2 × the number of features.</li>
<li>For each point, find the distance to its (min_samples)-th neighbour, then sort and plot these.</li>
<li>Look for the <b>knee</b>: dense points sit on the flat part, and noise on the steep part. Set eps at the knee.</li></ol>
<p>Always scale features first, since eps is a single distance applied to all of them.</p>
""", practice=["DBSCAN", "DBSCAN Core Points", "Distance-Based Outliers"])


@LD
def k_distance_plot():
    from sklearn.neighbors import NearestNeighbors
    r = np.random.default_rng(0)
    data = np.vstack([r.normal([0, 0], 0.3, (80, 2)), r.normal([4, 4], 0.3, (80, 2)), r.uniform(-3, 7, (15, 2))])
    distances, _ = NearestNeighbors(n_neighbors=4).fit(data).kneighbors(data)
    curve = np.sort(distances[:, 3])
    labels = DBSCAN(eps=0.5, min_samples=4).fit_predict(data)
    fig, (left, right) = plt.subplots(1, 2, figsize=(7.5, 2.8))
    left.plot(curve)
    left.axhline(0.5, ls="--", color="gray")
    left.set_title("sorted 4th-neighbour distance: knee near 0.5", fontsize=8)
    right.scatter(data[:, 0], data[:, 1], c=labels, cmap="coolwarm", s=10)
    right.set_title("DBSCAN result (−1 is noise)", fontsize=8)
    fig.tight_layout()


LESSON("Advanced", "Making clusters useful", """
<p>A clustering score doesn't tell you whether clusters mean anything. A real project continues with:</p>
<ol><li><b>Profile them:</b> compare each cluster's feature averages with the overall average.</li>
<li><b>Name them:</b> "young, frequent, low spend" is something a team can act on.</li>
<li><b>Test stability:</b> rerun with other seeds or a sample of the data. Do the same groups come back?</li>
<li><b>Link to action:</b> do the groups differ in an outcome that matters, such as churn?</li></ol>
<h4>Common mistakes</h4>
<ul><li>Clustering unscaled data, or data with many irrelevant features.</li>
<li>Believing clusters exist because an algorithm returned them. k-means always returns k groups, <b>even for pure noise</b>.</li>
<li>Reading meaning into a t-SNE or UMAP plot's cluster sizes or the distances between them.</li></ul>
""", practice=["Rand Index", "Contingency Table"])


@LD
def cluster_profile():
    r = np.random.default_rng(0)
    df = pd.DataFrame({"age": np.r_[r.normal(25, 3, 50), r.normal(55, 5, 50)], "spend": np.r_[r.normal(200, 40, 50), r.normal(900, 100, 50)]})
    scaled = (df - df.mean()) / df.std()
    df["cluster"] = KMeans(n_clusters=2, n_init=5, random_state=0).fit_predict(scaled)
    profile = df.groupby("cluster").mean().round(1)
    sizes = df["cluster"].value_counts().sort_index()
    noise = r.uniform(size=(300, 2))
    noise_labels = KMeans(n_clusters=4, n_init=5, random_state=0).fit_predict(noise)
    fig, ax = plt.subplots(figsize=(3.6, 3))
    ax.scatter(noise[:, 0], noise[:, 1], c=noise_labels, cmap="tab10", s=8)
    ax.set_title("k-means 'finds' 4 clusters in pure noise", fontsize=8)
