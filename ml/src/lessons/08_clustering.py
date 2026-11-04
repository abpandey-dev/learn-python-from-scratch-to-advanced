from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
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
