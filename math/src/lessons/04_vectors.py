from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def arrows(ax, vecs, labels, colors, origin=(0, 0)):
    for (x, y), lab, c in zip(vecs, labels, colors):
        ax.annotate("", xy=(origin[0] + x, origin[1] + y), xytext=origin, arrowprops=dict(arrowstyle="->", color=c, lw=2))
        ax.text(origin[0] + x, origin[1] + y, " " + lab, color=c)


LESSON("Basics", "What is a vector?", """
<p>A <b>vector</b> is an ordered list of numbers. You can picture it two ways:</p>
<ul>
<li>As an <b>arrow</b> from the origin: v = [3, 2] means "3 right, 2 up". It has a direction and a length.</li>
<li>As a <b>data point</b>: a house = [size 120, rooms 3, age 15]. Every row of a dataset is a vector.</li>
</ul>
<p>The number of components is the <b>dimension</b>. We can't draw 300-dimensional vectors, but the math is identical to 2-D, so we build intuition with arrows on paper.</p>
<p>In Python: <code>v = np.array([3, 2])</code>.</p>
""", practice=["Length of a Vector", "Distance Between Two Points", "Manhattan Distance"])


@LD
def vector_demo():
    v = np.array([3, 2])
    length = np.linalg.norm(v)
    fig, ax = plt.subplots(figsize=(3.6, 3))
    ax.annotate("", xy=(3, 2), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#0f766e", lw=2))
    ax.plot([3, 3], [0, 2], "--", color="gray")
    ax.text(1.5, -0.4, "3 right")
    ax.text(3.1, 1, "2 up")
    ax.set_xlim(-0.5, 4)
    ax.set_ylim(-0.8, 3)
    ax.set_title(f"v = [3, 2],  length = {length:.2f}")
    ax.grid(alpha=0.3)


LESSON("Basics", "Adding and scaling vectors", """
<p><b>Add</b> component by component: [1, 2] + [3, 1] = [4, 3]. As arrows: put the second arrow's tail on the first arrow's tip ("tip to tail"); the sum goes from start to finish.</p>
<p><b>Scale</b> by multiplying every component: 2·[1, 2] = [2, 4] (twice as long, same direction); −1·v points the opposite way.</p>
<p>A <b>linear combination</b> c₁v₁ + c₂v₂ mixes vectors with weights — every prediction of a linear model is a linear combination of features.</p>
""", practice=["Add Two Vectors", "Scale a Vector", "Linear Combination", "Centroid of Points", "Element-wise Product"])


@LD
def add_demo():
    u, v = np.array([1, 2]), np.array([3, 1])
    total = u + v
    fig, ax = plt.subplots(figsize=(4, 3))
    arrows(ax, [u], ["u"], ["#0f766e"])
    arrows(ax, [v], ["v"], ["#b45309"], origin=tuple(u))
    arrows(ax, [total], ["u + v"], ["#4338ca"])
    ax.set_xlim(-0.5, 5)
    ax.set_ylim(-0.5, 4)
    ax.grid(alpha=0.3)


LESSON("Core", "Length and distance", """
<p>The <b>length</b> (norm) of v = [3, 4] comes from Pythagoras: ‖v‖ = √(3² + 4²) = 5. In any dimension: ‖v‖ = √(v₁² + v₂² + … + vₙ²).</p>
<p>The <b>distance</b> between points p and q is the length of p − q. This is <b>Euclidean</b> distance (as the crow flies); <b>Manhattan</b> distance adds |differences| instead (along a street grid).</p>
<p>Dividing a vector by its length gives a <b>unit vector</b> (length 1) — pure direction. Distances power k-nearest-neighbours and k-means clustering; that's why features should be on similar scales (min-max scaling).</p>
""", practice=["Unit Vector", "Nearest Neighbour", "Min-Max Scaling", "Squared Error Between Two Vectors"])


@LD
def distance_demo():
    p, q = np.array([1, 1]), np.array([4, 5])
    euclid = np.linalg.norm(p - q)
    manhattan = np.abs(p - q).sum()
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(*zip(p, q), "o-", label=f"Euclidean {euclid:.0f}")
    ax.plot([1, 4, 4], [1, 1, 5], "--", label=f"Manhattan {manhattan}")
    ax.legend()
    ax.grid(alpha=0.3)


LESSON("Core", "The dot product and angles", """
<p>The <b>dot product</b> multiplies matching components and adds: [1, 2]·[3, 1] = 1·3 + 2·1 = 5. It is the most important operation in ML.</p>
<p>Geometrically: <b>u·v = ‖u‖‖v‖ cos θ</b>, where θ is the angle between them. So:</p>
<table><tr><th>u·v</th><th>Angle</th><th>Meaning</th></tr>
<tr><td>&gt; 0</td><td>&lt; 90°</td><td>point the same-ish way</td></tr>
<tr><td>= 0</td><td>90°</td><td><b>perpendicular</b> (orthogonal)</td></tr>
<tr><td>&lt; 0</td><td>&gt; 90°</td><td>point opposite-ish ways</td></tr></table>
<p><b>Cosine similarity</b> = u·v / (‖u‖‖v‖) ignores length and compares direction — search engines and ChatGPT-style embeddings use it to find similar text. A <b>neuron</b> is a dot product plus a bias: w·x + b.</p>
""", practice=["Dot Product", "Angle Between Two Vectors", "Cosine Similarity", "Are They Perpendicular?", "A Single Neuron", "Most Similar Word"])


@LD
def dot_demo():
    u = np.array([3, 1])
    vs = {"same way": np.array([2, 1]), "right angle": np.array([-1, 3]), "opposite": np.array([-2, -1])}
    results = {}
    for name, v in vs.items():
        results[name] = int(u @ v)
    fig, ax = plt.subplots(figsize=(4, 3))
    arrows(ax, [u] + list(vs.values()), ["u"] + [f"{k}: u·v = {results[k]}" for k in vs], ["black", "#0f766e", "#4338ca", "#b91c1c"])
    ax.set_xlim(-3, 6)
    ax.set_ylim(-2, 4)
    ax.grid(alpha=0.3)


LESSON("Advanced", "Projection and the cross product", """
<p>The <b>projection</b> of u onto v is u's "shadow" on the line of v: proj = (u·v / v·v)·v. What's left over, u − proj, is perpendicular to v. Projection is the heart of linear regression (projecting the targets onto the space of features) and of PCA (projecting data onto its main direction).</p>
<p>In 3-D only, the <b>cross product</b> u × v gives a vector perpendicular to both, with length equal to the area of the parallelogram they span — used in graphics and physics more than ML.</p>
""", practice=["Project One Vector Onto Another", "Cross Product (3-D)"])


@LD
def projection_demo():
    u, v = np.array([2, 3]), np.array([4, 1])
    proj = (u @ v) / (v @ v) * v
    residual = u - proj
    check = residual @ v
    fig, ax = plt.subplots(figsize=(4, 3))
    arrows(ax, [u, v, proj], ["u", "v", "proj of u on v"], ["#0f766e", "black", "#b45309"])
    ax.plot([u[0], proj[0]], [u[1], proj[1]], ":", color="gray")
    ax.set_xlim(-0.5, 5)
    ax.set_ylim(-0.5, 3.5)
    ax.set_aspect("equal")
