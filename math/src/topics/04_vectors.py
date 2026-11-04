from lib import *
import math
import numpy as np

TOPIC(
    id="vectors", title="Vectors", glyph="→",
    blurb="Arrows and lists of numbers: adding and scaling, length, distance, the dot product, angles, cosine similarity and projections — how ML represents every data point.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">u, v = np.array([1, 2]), np.array([3, 1])
u + v, 3 * u, u - v                  # add, scale, subtract
np.linalg.norm(u)                    # length ‖u‖ = √(1² + 2²)
np.linalg.norm(u - v)                # Euclidean distance
np.abs(u - v).sum()                  # Manhattan distance
u @ v  (or np.dot(u, v))             # dot product = 1·3 + 2·1 = 5
u @ v / (norm(u) * norm(v))          # cosine similarity
np.degrees(np.arccos(cos))           # angle
(u @ v / (v @ v)) * v                # projection of u onto v
np.cross([1, 0, 0], [0, 1, 0])       # [0, 0, 1]</code></pre>
""")


Q(None, "Add Two Vectors", "Easy", "Tip to tail",
  "Return u + v.",
  [(([1, 2], [3, 1]), [4, 3]), (([1, -1, 0], [2, 2, 2]), [3, 1, 2])],
  ("Add matching components one by one.", "O(n)", "O(n)"),
  ("<code>np.array(u) + np.array(v)</code>.", "O(n)", "O(n)"))


@B
def add(u, v):
    out = []
    for i in range(len(u)):
        out.append(u[i] + v[i])
    return out


@O
def add(u, v):
    return np.array(u) + np.array(v)


Q(None, "Scale a Vector", "Easy", "Scalar multiplication",
  "Return k·v.",
  [((3, [1, -2]), [3, -6]), ((0.5, [4, 2, 6]), [2.0, 1.0, 3.0])],
  ("Multiply every component by k.", "O(n)", "O(n)"),
  ("<code>k * np.array(v)</code>.", "O(n)", "O(n)"))


@B
def scale(k, v):
    return [k * x for x in v]


@O
def scale(k, v):
    return k * np.array(v)


Q(None, "Length of a Vector", "Easy", "Norm ‖v‖",
  "Return ‖v‖ = √(v₁² + v₂² + …), rounded to 4 decimals.",
  [(([3, 4],), 5.0), (([1, 1, 1],), 1.7321), (([0, 0],), 0.0)],
  ("Pythagoras: square, add, square-root.", "O(n)", "O(1)"),
  ("<code>np.linalg.norm(v)</code>.", "O(n)", "O(1)"))


@B
def length(v):
    total = 0
    for x in v:
        total += x * x
    return round(math.sqrt(total), 4)


@O
def length(v):
    return round(np.linalg.norm(v), 4)


Q(None, "Distance Between Two Points", "Easy", "Euclidean distance",
  "Return the straight-line distance between points p and q, rounded to 4 decimals.",
  [(([0, 0], [3, 4]), 5.0), (([1, 2, 3], [4, 6, 3]), 5.0), (([1, 1], [2, 2]), 1.4142)],
  ("Subtract component-wise, square, add, square-root.", "O(n)", "O(1)"),
  ("<code>np.linalg.norm(p - q)</code>.", "O(n)", "O(n)"))


@B
def distance(p, q):
    total = 0
    for a, b in zip(p, q):
        total += (a - b) ** 2
    return round(total ** 0.5, 4)


@O
def distance(p, q):
    return round(np.linalg.norm(np.array(p) - np.array(q)), 4)


Q(None, "Manhattan Distance", "Easy", "City-block distance",
  "Return Σ|pᵢ − qᵢ| — the distance walking along a street grid.",
  [(([0, 0], [3, 4]), 7), (([1, 5, 2], [4, 1, 2]), 7)],
  ("Add up absolute differences in a loop.", "O(n)", "O(1)"),
  ("<code>np.abs(p - q).sum()</code>.", "O(n)", "O(n)"))


@B
def manhattan(p, q):
    total = 0
    for a, b in zip(p, q):
        total += abs(a - b)
    return total


@O
def manhattan(p, q):
    return np.abs(np.array(p) - np.array(q)).sum()


Q(None, "Unit Vector", "Easy", "Normalising",
  "Return v scaled to length 1 (v ≠ 0), components rounded to 4 decimals.",
  [(([3, 4],), [0.6, 0.8]), (([0, 5, 0],), [0.0, 1.0, 0.0]), (([1, 1],), [0.7071, 0.7071])],
  ("Find the length by hand, divide each component by it.", "O(n)", "O(n)"),
  ("<code>v / np.linalg.norm(v)</code>.", "O(n)", "O(n)"))


@B
def unit(v):
    n = math.sqrt(sum(x * x for x in v))
    return [round(x / n, 4) for x in v]


@O
def unit(v):
    v = np.array(v, dtype=float)
    return (v / np.linalg.norm(v)).round(4)


Q(None, "Dot Product", "Easy", "u · v = Σ uᵢvᵢ",
  "Return the dot product of u and v.",
  [(([1, 2], [3, 1]), 5), (([1, 2, 3], [4, -5, 6]), 12), (([1, 0], [0, 1]), 0)],
  ("Multiply matching components and add.", "O(n)", "O(1)"),
  ("<code>u @ v</code> (NumPy's matrix-multiply operator).", "O(n)", "O(1)"))


@B
def dot(u, v):
    total = 0
    for a, b in zip(u, v):
        total += a * b
    return total


@O
def dot(u, v):
    return np.array(u) @ np.array(v)


Q(None, "Angle Between Two Vectors", "Medium", "cos θ = u·v / (‖u‖‖v‖)",
  "Return the angle between u and v in degrees, rounded to 2 decimals.",
  [(([1, 0], [0, 1]), 90.0), (([1, 0], [1, 1]), 45.0), (([1, 2], [-2, -4]), 180.0)],
  ("Dot product and lengths by hand, then arccos.", "O(n)", "O(1)"),
  ("NumPy dot, norms, <code>np.arccos</code> and <code>np.degrees</code> (clip to [−1, 1] for safety).", "O(n)", "O(1)"))


@B
def angle(u, v):
    d = sum(a * b for a, b in zip(u, v))
    nu = math.sqrt(sum(a * a for a in u))
    nv = math.sqrt(sum(b * b for b in v))
    cos = max(-1.0, min(1.0, d / (nu * nv)))
    return round(math.degrees(math.acos(cos)), 2)


@O
def angle(u, v):
    u, v = np.array(u, dtype=float), np.array(v, dtype=float)
    cos = u @ v / (np.linalg.norm(u) * np.linalg.norm(v))
    return round(np.degrees(np.arccos(np.clip(cos, -1, 1))), 2)


Q(None, "Cosine Similarity", "Medium", "Direction, not size",
  "Return u·v / (‖u‖‖v‖), rounded to 4 decimals: 1 = same direction, 0 = unrelated, −1 = opposite.",
  [(([1, 2, 3], [2, 4, 6]), 1.0), (([1, 0], [0, 3]), 0.0), (([3, 1], [1, 3]), 0.6)],
  ("Three sums in one loop: u·v, u·u, v·v.", "O(n)", "O(1)"),
  ("NumPy dot and norms.", "O(n)", "O(1)"))


@B
def cosine(u, v):
    uv = uu = vv = 0
    for a, b in zip(u, v):
        uv += a * b
        uu += a * a
        vv += b * b
    return round(uv / math.sqrt(uu * vv), 4)


@O
def cosine(u, v):
    u, v = np.array(u, dtype=float), np.array(v, dtype=float)
    return round(u @ v / (np.linalg.norm(u) * np.linalg.norm(v)), 4)


Q(None, "Are They Perpendicular?", "Easy", "Orthogonal ⇔ dot = 0",
  "Return True if u and v are at right angles (dot product 0).",
  [(([1, 2], [-2, 1]), True), (([1, 1], [1, 2]), False), (([1, 0, 0], [0, 0, 5]), True)],
  ("Compute the dot product with a loop and compare to 0.", "O(n)", "O(1)"),
  ("<code>np.isclose(u @ v, 0)</code> — safe for floats.", "O(n)", "O(1)"))


@B
def perpendicular(u, v):
    total = 0
    for a, b in zip(u, v):
        total += a * b
    return total == 0


@O
def perpendicular(u, v):
    return bool(np.isclose(np.array(u) @ np.array(v), 0))


Q(None, "Project One Vector Onto Another", "Medium", "Shadow of u on v",
  "Return the projection of u onto v: (u·v / v·v)·v, components rounded to 4 decimals.",
  [(([2, 3], [1, 0]), [2.0, 0.0]), (([1, 2], [2, 2]), [1.5, 1.5]), (([3, 4], [0, 5]), [0.0, 4.0])],
  ("Two dot products in loops, then scale v.", "O(n)", "O(n)"),
  ("<code>(u @ v) / (v @ v) * v</code>.", "O(n)", "O(n)"))


@B
def project(u, v):
    uv = sum(a * b for a, b in zip(u, v))
    vv = sum(b * b for b in v)
    k = uv / vv
    return [round(k * b, 4) for b in v]


@O
def project(u, v):
    u, v = np.array(u, dtype=float), np.array(v, dtype=float)
    return ((u @ v) / (v @ v) * v).round(4)


Q(None, "Linear Combination", "Medium", "c₁v₁ + c₂v₂ + …",
  "Return the weighted sum of the vectors with the given weights.",
  [(([2, -1], [[1, 0], [0, 1]]), [2, -1]), (([1, 2, 3], [[1, 1], [0, 1], [1, 0]]), [4, 3])],
  ("Scale each vector by its weight and add them up component by component.", "O(k·n)", "O(n)"),
  ("Stack the vectors as rows of a matrix: <code>weights @ M</code>.", "O(k·n)", "O(n)"))


@B
def combine(weights, vectors):
    out = [0] * len(vectors[0])
    for w, vec in zip(weights, vectors):
        for i in range(len(vec)):
            out[i] += w * vec[i]
    return out


@O
def combine(weights, vectors):
    return np.array(weights) @ np.array(vectors)


Q(None, "A Single Neuron", "Medium", "w · x + b",
  "A neuron computes w·x + b and passes it through ReLU. Return its output.",
  [(([0.5, -1.0, 2.0], [2, 1, 3], 0.5), 6.5), (([1, 1], [-3, 1], 0), 0), (([0.2, 0.4], [1, 1], -0.1), 0.5)],
  ("Dot product in a loop, add the bias, clamp at 0.", "O(n)", "O(1)"),
  ("<code>max(0, w @ x + b)</code>.", "O(n)", "O(1)"),
  names=["w", "x", "b"])


@B
def neuron(w, x, b):
    z = b
    for wi, xi in zip(w, x):
        z += wi * xi
    if z < 0:
        z = 0
    return z


@O
def neuron(w, x, b):
    return np.maximum(0, np.array(w) @ np.array(x) + b)


Q(None, "Nearest Neighbour", "Medium", "k-NN with k = 1",
  "Return the index of the point closest (Euclidean) to the query.",
  [(([[0, 0], [5, 5], [1, 2]], [2, 2]), 2), (([[1, 1], [10, 10]], [9, 8]), 1)],
  ("Compute each distance in a loop, track the smallest.", "O(n·d)", "O(1)"),
  ("Broadcast: <code>np.linalg.norm(points - q, axis=1).argmin()</code>.", "O(n·d)", "O(n)"))


@B
def nearest(points, q):
    best_i, best_d = -1, None
    for i, p in enumerate(points):
        d = sum((a - b) ** 2 for a, b in zip(p, q))
        if best_d is None or d < best_d:
            best_i, best_d = i, d
    return best_i


@O
def nearest(points, q):
    P = np.array(points)
    return np.linalg.norm(P - np.array(q), axis=1).argmin()


Q(None, "Centroid of Points", "Easy", "Average vector",
  "Return the centre (mean position) of the points, rounded to 4 decimals.",
  [(([[0, 0], [4, 0], [2, 6]],), [2.0, 2.0]), (([[1, 2, 3], [3, 2, 1]],), [2.0, 2.0, 2.0])],
  ("Add the vectors, divide by how many there are.", "O(n·d)", "O(d)"),
  ("<code>points.mean(axis=0)</code> — the centre step of k-means.", "O(n·d)", "O(d)"))


@B
def centroid(points):
    total = [0] * len(points[0])
    for p in points:
        for i, x in enumerate(p):
            total[i] += x
    return [round(t / len(points), 4) for t in total]


@O
def centroid(points):
    return np.array(points, dtype=float).mean(axis=0).round(4)


Q(None, "Cross Product (3-D)", "Medium", "A vector at right angles to both",
  "Return u × v for 3-D vectors.",
  [(([1, 0, 0], [0, 1, 0]), [0, 0, 1]), (([1, 2, 3], [4, 5, 6]), [-3, 6, -3])],
  ("Formula (u₂v₃ − u₃v₂, u₃v₁ − u₁v₃, u₁v₂ − u₂v₁).", "O(1)", "O(1)"),
  ("<code>np.cross(u, v)</code>.", "O(1)", "O(1)"))


@B
def cross(u, v):
    return [u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0]]


@O
def cross(u, v):
    return np.cross(u, v)


Q(None, "Min-Max Scaling", "Easy", "Rescale to [0, 1]",
  "Rescale the vector so its smallest value becomes 0 and its largest 1 (values rounded to 4 decimals).",
  [(([10, 20, 15, 30],), [0.0, 0.5, 0.25, 1.0]), (([5, 7],), [0.0, 1.0])],
  ("Find min and max with a loop, then (x − min)/(max − min) for each.", "O(n)", "O(n)"),
  ("Vectorised in one line.", "O(n)", "O(n)"))


@B
def min_max(v):
    lo = hi = v[0]
    for x in v:
        lo = min(lo, x)
        hi = max(hi, x)
    return [round((x - lo) / (hi - lo), 4) for x in v]


@O
def min_max(v):
    v = np.array(v, dtype=float)
    return ((v - v.min()) / (v.max() - v.min())).round(4)


Q(None, "Element-wise Product", "Easy", "Hadamard product u ⊙ v",
  "Return the component-by-component product (not the dot product).",
  [(([1, 2, 3], [4, 5, 6]), [4, 10, 18]), (([2, 0], [3, 9]), [6, 0])],
  ("Multiply matching components into a new list.", "O(n)", "O(n)"),
  ("<code>u * v</code> on NumPy arrays (while <code>u @ v</code> is the dot product).", "O(n)", "O(n)"))


@B
def hadamard(u, v):
    return [a * b for a, b in zip(u, v)]


@O
def hadamard(u, v):
    return np.array(u) * np.array(v)


Q(None, "Squared Error Between Two Vectors", "Easy", "‖ŷ − y‖²",
  "Return the sum of squared differences between predictions and targets.",
  [(([2.5, 0.0, 2.0], [3.0, -0.5, 2.0]), 0.5), (([1, 2, 3], [1, 2, 3]), 0)],
  ("Loop: subtract, square, add.", "O(n)", "O(1)"),
  ("The squared length of the difference vector: <code>d @ d</code>.", "O(n)", "O(n)"),
  names=["pred", "target"])


@B
def squared_error(pred, target):
    total = 0
    for p, t in zip(pred, target):
        total += (p - t) ** 2
    return total


@O
def squared_error(pred, target):
    d = np.array(pred) - np.array(target)
    return d @ d


Q(None, "Most Similar Word", "Hard", "Embeddings + cosine similarity",
  "Words are vectors (embeddings). Return the word (other than the query itself) with the highest cosine similarity to the query word.",
  [(({"king": [0.9, 0.8, 0.1], "queen": [0.85, 0.9, 0.15], "apple": [0.1, 0.2, 0.9], "man": [0.7, 0.3, 0.1]}, "king"), "queen"),
   (({"cat": [1, 0], "dog": [0.9, 0.2], "car": [0, 1]}, "car"), "dog")],
  ("Loop over every other word, compute cosine similarity by hand, keep the best.", "O(n·d)", "O(1)"),
  ("Normalise all vectors into a matrix, one matrix-vector product gives every similarity; argmax.", "O(n·d)", "O(n·d)"))


@B
def most_similar(emb, word):
    q = emb[word]
    best, best_sim = None, -2
    for w, v in emb.items():
        if w == word:
            continue
        dotp = sum(a * b for a, b in zip(q, v))
        sim = dotp / (math.sqrt(sum(a * a for a in q)) * math.sqrt(sum(b * b for b in v)))
        if sim > best_sim:
            best, best_sim = w, sim
    return best


@O
def most_similar(emb, word):
    words = [w for w in emb if w != word]
    M = np.array([emb[w] for w in words], dtype=float)
    M /= np.linalg.norm(M, axis=1, keepdims=True)
    q = np.array(emb[word], dtype=float)
    sims = M @ (q / np.linalg.norm(q))
    return words[sims.argmax()]
