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


LESSON("Basics", "What vector operations mean for data", """
<p>Treat each house as a vector: [size, rooms, age].</p>
<table><tr><th>Operation</th><th>Example</th><th>Meaning</th></tr>
<tr><td>Subtract</td><td>[120, 3, 5] − [100, 2, 15] = [20, 1, −10]</td><td>how they differ</td></tr>
<tr><td>Add, then divide</td><td>mean of two houses = [110, 2.5, 10]</td><td>the average house (a k-means centre)</td></tr>
<tr><td>Scale</td><td>0.5 × [120, 3, 5] = [60, 1.5, 2.5]</td><td>shrink all features together</td></tr>
<tr><td>Dot with weights</td><td>[2, 10, −1]·[120, 3, 5] = 265</td><td>a linear model's prediction</td></tr></table>
<p><b>Sizes must match.</b> Adding a 3-feature house to a 2-feature one is meaningless, and it's the most common shape error in practice.</p>
<p>A word embedding, an image and a customer are all vectors. Everything you learn here works in any number of dimensions, even though we only draw two.</p>
""", practice=["Add Two Vectors", "Scale a Vector", "Centroid of Points", "A Single Neuron"])


@LD
def house_vectors():
    a = np.array([120.0, 3, 5])
    b = np.array([100.0, 2, 15])
    difference = a - b
    average = (a + b) / 2
    half = 0.5 * a
    weights = np.array([2.0, 10, -1])
    prediction = weights @ a


LESSON("Core", "The dot product and angle, worked", """
<p>u = (3, 4) and v = (4, 3).</p>
<ol><li><b>Dot product:</b> 3·4 + 4·3 = 24.</li>
<li><b>Lengths:</b> ‖u‖ = √(9 + 16) = 5 and ‖v‖ = 5.</li>
<li><b>Cosine:</b> 24 / (5 × 5) = 0.96.</li>
<li><b>Angle:</b> arccos(0.96) = <b>16.26°</b>. They point in similar directions.</li></ol>
<table><tr><th>Cosine</th><th>Angle</th><th>Meaning</th></tr>
<tr><td>1</td><td>0°</td><td>same direction</td></tr><tr><td>0</td><td>90°</td><td>unrelated (perpendicular)</td></tr><tr><td>−1</td><td>180°</td><td>opposite</td></tr></table>
<h4>Why u·v = ‖u‖‖v‖cos θ?</h4>
<p>Think of shadows. The dot product is the length of u's shadow on v, multiplied by v's length. When they're perpendicular there's no shadow, so the result is 0.</p>
<p><b>Length itself comes from the dot product:</b> v·v = ‖v‖². That's why squared errors and vector lengths look alike.</p>
""", practice=["Dot Product", "Angle Between Two Vectors", "Cosine Similarity", "Are They Perpendicular?", "Project One Vector Onto Another"])


@LD
def dot_worked():
    u, v = np.array([3.0, 4.0]), np.array([4.0, 3.0])
    dot = u @ v
    lengths = (np.linalg.norm(u), np.linalg.norm(v))
    cosine = dot / (lengths[0] * lengths[1])
    degrees = math.degrees(math.acos(cosine))
    self_dot = v @ v


LESSON("Core", "Three ways to measure length", """
<p>For v = (3, −4):</p>
<table><tr><th>Norm</th><th>Formula</th><th>Value</th><th>Think of it as</th></tr>
<tr><td>L1 (Manhattan)</td><td>|3| + |−4|</td><td>7</td><td>walking a street grid</td></tr>
<tr><td>L2 (Euclidean)</td><td>√(9 + 16)</td><td>5</td><td>straight line</td></tr>
<tr><td>L∞ (max)</td><td>max(3, 4)</td><td>4</td><td>the single largest change</td></tr></table>
<p>The chart draws all points with length 1 under each norm. L2 gives a circle, L1 a diamond, and L∞ a square.</p>
<h4>Why ML cares</h4>
<ul><li><b>L2 penalty (Ridge):</b> shrinks all weights smoothly.</li>
<li><b>L1 penalty (Lasso):</b> sets some weights to exactly 0. The diamond's corners lie on the axes, where a weight is 0.</li>
<li><b>Distances:</b> L1 is less sensitive to one huge difference, since it isn't squared.</li></ul>
""", practice=["Length of a Vector", "Manhattan Distance", "Unit Vector", "Distance Between Two Points", "Nearest Neighbour", "Min-Max Scaling"])


@LD
def norm_shapes():
    v = np.array([3.0, -4.0])
    l1 = np.abs(v).sum()
    l2 = math.sqrt((v ** 2).sum())
    linf = np.abs(v).max()
    t = np.linspace(0, 2 * np.pi, 400)
    circle = np.column_stack([np.cos(t), np.sin(t)])
    fig, ax = plt.subplots(figsize=(3.4, 3.4))
    for p, name in [(1, "L1"), (2, "L2"), (50, "L∞")]:
        scale = (np.abs(circle) ** p).sum(axis=1) ** (1 / p)
        ax.plot(circle[:, 0] / scale, circle[:, 1] / scale, label=name)
    ax.set_aspect("equal")
    ax.legend(fontsize=8)
    ax.set_title("All points of length 1", fontsize=9)


LESSON("Advanced", "Independence, span and basis", """
<h4>Span: everywhere you can reach</h4>
<p>Combining vectors with weights, c₁v₁ + c₂v₂, reaches a set of points called their <b>span</b>.</p>
<ul><li>(1, 0) and (0, 1) reach every point of the plane.</li>
<li>(1, 2) and (2, 4) only reach one line, since the second is just 2 × the first.</li></ul>
<h4>Linear independence</h4>
<p>Vectors are <b>independent</b> if none can be built from the others. (1, 2) and (2, 4) are dependent, so the second adds no new direction.</p>
<p><b>In data:</b> a "price in rupees" column and a "price in dollars" column are dependent. The second adds no information, and it causes unstable regression.</p>
<h4>Basis: a coordinate system</h4>
<p>A basis is a minimal set of independent vectors that reaches everything. The point (3, 5) can be written in two ways:</p>
<ul><li>Using (1, 0), (0, 1): 3(1, 0) + 5(0, 1)</li>
<li>Using (1, 1), (1, −1): 4(1, 1) − 1(1, −1) = (3, 5)</li></ul>
<p>It's the same point with different coordinates. <b>PCA is choosing a better basis</b> for your data.</p>
""", practice=["Linear Combination", "Cross Product (3-D)"])


@LD
def basis_demo():
    dependent_rank = np.linalg.matrix_rank([[1, 2], [2, 4]])
    independent_rank = np.linalg.matrix_rank([[1, 0], [0, 1]])
    new_basis = np.array([[1, 1], [1, -1]]).T
    coordinates = np.linalg.solve(new_basis, [3, 5])
    rebuilt = coordinates[0] * np.array([1, 1]) + coordinates[1] * np.array([1, -1])


LESSON("Advanced", "Similarity search, the idea behind embeddings", """
<p>Modern AI turns text into vectors called <b>embeddings</b>, placing similar meanings close together. Finding similar items is then simple maths.</p>
<h4>Cosine or distance?</h4>
<p>Compare a = (1, 2) with b = (2, 4), a longer vector in the same direction.</p>
<ul><li>Euclidean distance: √(1 + 4) = 2.236, so they seem different.</li>
<li>Cosine similarity: 10 / (2.236 × 4.472) = 1, so they seem identical.</li></ul>
<p>A long document and a short one on one topic have different lengths and the same direction, so cosine suits text.</p>
<h4>A speed trick</h4>
<p>If all vectors are scaled to length 1, the dot product <b>is</b> the cosine. So similarity against a million items becomes one matrix–vector multiply. That's how retrieval in a RAG system works, and vector databases add indexes to make it faster still.</p>
""", practice=["Most Similar Word", "Cosine Similarity", "Squared Error Between Two Vectors", "Element-wise Product"])


@LD
def similarity_search():
    words = ["king", "queen", "apple", "banana"]
    vectors = np.array([[0.9, 0.8, 0.1], [0.85, 0.9, 0.15], [0.1, 0.2, 0.9], [0.15, 0.1, 0.95]])
    unit = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
    query = unit[0]
    scores = (unit @ query).round(3)
    ranked = [words[i] for i in np.argsort(-scores)]
    a, b = np.array([1.0, 2.0]), np.array([2.0, 4.0])
    distance = np.linalg.norm(a - b)
    cosine = a @ b / (np.linalg.norm(a) * np.linalg.norm(b))
