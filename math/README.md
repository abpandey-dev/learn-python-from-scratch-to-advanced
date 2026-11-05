# Math for Data Science & Machine Learning

10 topics · theory with 55 theory questions · 103 lessons from basics to advanced · 200 practice questions with answers · Arithmetic, algebra, functions, vectors, matrices, eigenvectors and PCA, calculus, gradient descent, probability and distributions · taught from zero for someone learning math for the first time · every question is solved by hand in plain Python and again with NumPy or a formula, both shown running step by step with graphs.

**Live site:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/

Every solution is run against its test cases by `build.py` before the site is generated, and each animation is recorded from a real run of the code you see.

## Topics

- [Numbers & Arithmetic](#numbers-arithmetic) — The starting point: kinds of numbers, fractions, percentages, powers, roots, primes, rounding and the Σ notation every ML formula uses.
- [Algebra & Equations](#algebra-equations) — Letters that stand for numbers: expressions, solving equations, quadratics, polynomials, systems of equations, inequalities and sequences.
- [Functions & Graphs](#functions-graphs) — A function is a machine: input in, one output out. Lines and slope, parabolas, exponentials, logarithms, and the activation functions used in neural networks.
- [Vectors](#vectors) — Arrows and lists of numbers: adding and scaling, length, distance, the dot product, angles, cosine similarity and projections — how ML represents every data point.
- [Matrices](#matrices) — Tables of numbers that transform vectors: multiplication, transpose, determinant, inverse, solving systems, rank — and the matrix form of a neural-network layer and linear regression.
- [Eigenvectors, PCA & SVD](#eigenvectors-pca-svd) — The special directions a matrix only stretches. Eigenvalues, power iteration, principal component analysis, singular values, Markov steady states and PageRank.
- [Calculus: Derivatives & Integrals](#calculus-derivatives-integrals) — The math of change. Slopes of curves, the derivative rules, finding minimums and maximums, Newton's method, and areas under curves.
- [Gradients & Optimisation](#gradients-optimisation) — How machines learn: partial derivatives, the gradient, gradient descent and learning rates, fitting a line by descent, backpropagation through a neuron, logistic regression, Hessians and convexity.
- [Probability](#probability) — Measuring uncertainty: counting outcomes, permutations and combinations, the rules of probability, conditional probability, Bayes' theorem, independence and expected value.
- [Distributions & Information](#distributions-information) — The shapes randomness takes — Bernoulli, binomial, Poisson, uniform, normal, exponential — the central limit theorem, and the information theory behind ML losses: entropy, cross-entropy, KL divergence, softmax, log-loss, Gini and maximum likelihood.

## Numbers & Arithmetic

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Greatest Common Divisor](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/arithmetic/greatest-common-divisor) | Easy | Euclid's algorithm |
| 2 | [Least Common Multiple](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/arithmetic/least-common-multiple) | Easy | LCM = a·b / gcd |
| 3 | [Simplify a Fraction](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/arithmetic/simplify-a-fraction) | Easy | Lowest terms |
| 4 | [Add Two Fractions](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/arithmetic/add-two-fractions) | Easy | Common denominator |
| 5 | [Fraction to Decimal and Percent](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/arithmetic/fraction-to-decimal-and-percent) | Easy | Three ways to write a part |
| 6 | [Percent Change](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/arithmetic/percent-change) | Easy | (new − old) / old |
| 7 | [Is It Prime?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/arithmetic/is-it-prime) | Easy | Trial division to √n |
| 8 | [Prime Factorisation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/arithmetic/prime-factorisation) | Medium | Every number is a product of primes |
| 9 | [Power by Repeated Multiplication](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/arithmetic/power-by-repeated-multiplication) | Easy | Exponents |
| 10 | [Negative and Fractional Exponents](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/arithmetic/negative-and-fractional-exponents) | Medium | x⁻ⁿ = 1/xⁿ, x^(1/n) = ⁿ√x |
| 11 | [Square Root by Guessing](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/arithmetic/square-root-by-guessing) | Medium | Newton's method |
| 12 | [Scientific Notation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/arithmetic/scientific-notation) | Easy | a × 10ⁿ with 1 ≤ a < 10 |
| 13 | [Round to Significant Figures](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/arithmetic/round-to-significant-figures) | Medium | Precision |
| 14 | [Divide With Remainder](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/arithmetic/divide-with-remainder) | Easy | Quotient and remainder |
| 15 | [Share in a Ratio](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/arithmetic/share-in-a-ratio) | Easy | Ratios |
| 16 | [Whole Number to Binary](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/arithmetic/whole-number-to-binary) | Easy | Place value in base 2 |
| 17 | [Add 1 to n (Gauss's Trick)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/arithmetic/add-1-to-n-gausss-trick) | Easy | Σ k = n(n + 1)/2 |
| 18 | [Sigma Notation: Sum of Squares](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/arithmetic/sigma-notation-sum-of-squares) | Medium | Σ k² |
| 19 | [Factorial](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/arithmetic/factorial) | Easy | n! = n·(n−1)·…·1 |
| 20 | [Distance on the Number Line](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/arithmetic/distance-on-the-number-line) | Easy | Absolute value |

## Algebra & Equations

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Evaluate a Polynomial](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/algebra/evaluate-a-polynomial) | Easy | Substitution |
| 2 | [Solve a Linear Equation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/algebra/solve-a-linear-equation) | Easy | ax + b = c |
| 3 | [Variables on Both Sides](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/algebra/variables-on-both-sides) | Easy | ax + b = cx + d |
| 4 | [Rearrange a Formula](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/algebra/rearrange-a-formula) | Easy | Make y the subject |
| 5 | [How Many Real Solutions?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/algebra/how-many-real-solutions) | Easy | The discriminant |
| 6 | [Quadratic Formula](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/algebra/quadratic-formula) | Medium | x = (−b ± √D) / 2a |
| 7 | [Expand Two Brackets](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/algebra/expand-two-brackets) | Easy | (x + a)(x + b) |
| 8 | [Multiply Two Polynomials](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/algebra/multiply-two-polynomials) | Medium | Distribute every term |
| 9 | [Add Two Polynomials](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/algebra/add-two-polynomials) | Easy | Like terms |
| 10 | [Collect Like Terms](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/algebra/collect-like-terms) | Easy | Simplifying |
| 11 | [Solve Two Equations Together](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/algebra/solve-two-equations-together) | Medium | Simultaneous equations |
| 12 | [Which Values Satisfy an Inequality?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/algebra/which-values-satisfy-an-inequality) | Easy | ax + b > c |
| 13 | [Absolute Value Equation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/algebra/absolute-value-equation) | Easy | |x − a| = b |
| 14 | [Solve a Proportion](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/algebra/solve-a-proportion) | Easy | Cross-multiplying |
| 15 | [Compound Growth](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/algebra/compound-growth) | Easy | P(1 + r)ⁿ |
| 16 | [Years to Double](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/algebra/years-to-double) | Medium | Solving with a logarithm |
| 17 | [Find a Root by Halving](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/algebra/find-a-root-by-halving) | Medium | Bisection |
| 18 | [Arithmetic Sequence](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/algebra/arithmetic-sequence) | Easy | aₙ = a₁ + (n − 1)d |
| 19 | [Sum of a Geometric Series](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/algebra/sum-of-a-geometric-series) | Medium | a(1 − rⁿ)/(1 − r) |
| 20 | [Factor Out the Common Factor](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/algebra/factor-out-the-common-factor) | Easy | Factorising |

## Functions & Graphs

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Table of Values](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/functions/table-of-values) | Easy | Evaluating a function |
| 2 | [Slope Between Two Points](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/functions/slope-between-two-points) | Easy | Rise over run |
| 3 | [Equation of a Line Through Two Points](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/functions/equation-of-a-line-through-two-points) | Easy | y = mx + c |
| 4 | [Where Two Lines Meet](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/functions/where-two-lines-meet) | Medium | Intersection |
| 5 | [Is It a Function?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/functions/is-it-a-function) | Easy | One output per input |
| 6 | [Allowed Inputs (Domain)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/functions/allowed-inputs-domain) | Medium | √ and ÷ restrictions |
| 7 | [Vertex of a Parabola](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/functions/vertex-of-a-parabola) | Easy | x = −b / 2a |
| 8 | [Compose Two Functions](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/functions/compose-two-functions) | Medium | f(g(x)) |
| 9 | [Inverse of a Line](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/functions/inverse-of-a-line) | Easy | Undo the function |
| 10 | [Exponential Growth Table](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/functions/exponential-growth-table) | Easy | a · bˣ |
| 11 | [Logarithm by Counting](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/functions/logarithm-by-counting) | Easy | How many times do I multiply? |
| 12 | [Solve an Exponential Equation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/functions/solve-an-exponential-equation) | Medium | bˣ = n  ⇒  x = log n / log b |
| 13 | [Multiply Tiny Probabilities With Logs](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/functions/multiply-tiny-probabilities-with-logs) | Medium | log(ab) = log a + log b |
| 14 | [Sigmoid Function](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/functions/sigmoid-function) | Easy | Squash to (0, 1) |
| 15 | [ReLU Activation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/functions/relu-activation) | Easy | max(0, x) |
| 16 | [Shift and Stretch a Graph](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/functions/shift-and-stretch-a-graph) | Medium | a·f(x − h) + k |
| 17 | [Even, Odd or Neither?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/functions/even-odd-or-neither) | Medium | Symmetry |
| 18 | [Highest Point on a Grid](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/functions/highest-point-on-a-grid) | Easy | Maximum of a function |
| 19 | [Average Rate of Change](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/functions/average-rate-of-change) | Easy | Secant slope |
| 20 | [Piecewise Function: Tax Brackets](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/functions/piecewise-function-tax-brackets) | Medium | Different rules on different intervals |

## Vectors

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Add Two Vectors](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/vectors/add-two-vectors) | Easy | Tip to tail |
| 2 | [Scale a Vector](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/vectors/scale-a-vector) | Easy | Scalar multiplication |
| 3 | [Length of a Vector](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/vectors/length-of-a-vector) | Easy | Norm ‖v‖ |
| 4 | [Distance Between Two Points](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/vectors/distance-between-two-points) | Easy | Euclidean distance |
| 5 | [Manhattan Distance](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/vectors/manhattan-distance) | Easy | City-block distance |
| 6 | [Unit Vector](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/vectors/unit-vector) | Easy | Normalising |
| 7 | [Dot Product](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/vectors/dot-product) | Easy | u · v = Σ uᵢvᵢ |
| 8 | [Angle Between Two Vectors](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/vectors/angle-between-two-vectors) | Medium | cos θ = u·v / (‖u‖‖v‖) |
| 9 | [Cosine Similarity](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/vectors/cosine-similarity) | Medium | Direction, not size |
| 10 | [Are They Perpendicular?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/vectors/are-they-perpendicular) | Easy | Orthogonal ⇔ dot = 0 |
| 11 | [Project One Vector Onto Another](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/vectors/project-one-vector-onto-another) | Medium | Shadow of u on v |
| 12 | [Linear Combination](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/vectors/linear-combination) | Medium | c₁v₁ + c₂v₂ + … |
| 13 | [A Single Neuron](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/vectors/a-single-neuron) | Medium | w · x + b |
| 14 | [Nearest Neighbour](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/vectors/nearest-neighbour) | Medium | k-NN with k = 1 |
| 15 | [Centroid of Points](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/vectors/centroid-of-points) | Easy | Average vector |
| 16 | [Cross Product (3-D)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/vectors/cross-product-3-d) | Medium | A vector at right angles to both |
| 17 | [Min-Max Scaling](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/vectors/min-max-scaling) | Easy | Rescale to [0, 1] |
| 18 | [Element-wise Product](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/vectors/element-wise-product) | Easy | Hadamard product u ⊙ v |
| 19 | [Squared Error Between Two Vectors](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/vectors/squared-error-between-two-vectors) | Easy | ‖ŷ − y‖² |
| 20 | [Most Similar Word](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/vectors/most-similar-word) | Hard | Embeddings + cosine similarity |

## Matrices

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Transpose](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/matrices/transpose) | Easy | Rows become columns |
| 2 | [Add Two Matrices](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/matrices/add-two-matrices) | Easy | Entry by entry |
| 3 | [Matrix Times Vector](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/matrices/matrix-times-vector) | Easy | Each row · the vector |
| 4 | [Multiply Two Matrices](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/matrices/multiply-two-matrices) | Medium | Row × column |
| 5 | [Is It the Identity Matrix?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/matrices/is-it-the-identity-matrix) | Easy | 1s on the diagonal, 0s elsewhere |
| 6 | [Trace](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/matrices/trace) | Easy | Sum of the diagonal |
| 7 | [Determinant of a 2×2](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/matrices/determinant-of-a-2-2) | Easy | ad − bc |
| 8 | [Determinant of a 3×3](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/matrices/determinant-of-a-3-3) | Medium | Cofactor expansion |
| 9 | [Inverse of a 2×2](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/matrices/inverse-of-a-2-2) | Medium | Swap, negate, divide by det |
| 10 | [Solve A·x = b](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/matrices/solve-a-x-b) | Medium | Gaussian elimination |
| 11 | [Is It Symmetric?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/matrices/is-it-symmetric) | Easy | A = Aᵀ |
| 12 | [Matrix Power](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/matrices/matrix-power) | Medium | Aⁿ = A·A·…·A |
| 13 | [Rotate a Point](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/matrices/rotate-a-point) | Medium | Rotation matrix |
| 14 | [Rank of a Matrix](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/matrices/rank-of-a-matrix) | Hard | Independent rows |
| 15 | [Outer Product](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/matrices/outer-product) | Easy | u vᵀ |
| 16 | [Covariance Matrix](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/matrices/covariance-matrix) | Hard | Xᵀ X / (n − 1) after centring |
| 17 | [Linear Regression by the Normal Equation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/matrices/linear-regression-by-the-normal-equation) | Hard | w = (XᵀX)⁻¹Xᵀy |
| 18 | [A Neural-Network Layer](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/matrices/a-neural-network-layer) | Medium | ReLU(W·x + b) |
| 19 | [Markov Chain: Where Will We Be?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/matrices/markov-chain-where-will-we-be) | Medium | State × transition matrix |
| 20 | [Scale and Shear Shapes](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/matrices/scale-and-shear-shapes) | Medium | Transforming many points |

## Eigenvectors, PCA & SVD

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Is It an Eigenvector?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/eigen-pca/is-it-an-eigenvector) | Easy | A·v = λ·v |
| 2 | [Eigenvalues of a 2×2](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/eigen-pca/eigenvalues-of-a-2-2) | Medium | Characteristic equation |
| 3 | [Sum and Product of Eigenvalues](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/eigen-pca/sum-and-product-of-eigenvalues) | Easy | trace and determinant |
| 4 | [Power Iteration: Biggest Eigenvalue](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/eigen-pca/power-iteration-biggest-eigenvalue) | Medium | Repeatedly multiply |
| 5 | [Power Iteration: Main Direction](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/eigen-pca/power-iteration-main-direction) | Medium | Dominant eigenvector |
| 6 | [Eigenvalues of a Triangular Matrix](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/eigen-pca/eigenvalues-of-a-triangular-matrix) | Easy | Read them off the diagonal |
| 7 | [Centre the Data](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/eigen-pca/centre-the-data) | Easy | PCA step 1 |
| 8 | [First Principal Component](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/eigen-pca/first-principal-component) | Hard | Direction of greatest spread |
| 9 | [Project Onto the First Component](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/eigen-pca/project-onto-the-first-component) | Medium | PCA scores |
| 10 | [Explained Variance Ratio](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/eigen-pca/explained-variance-ratio) | Medium | How much each component keeps |
| 11 | [Compress and Rebuild With One Component](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/eigen-pca/compress-and-rebuild-with-one-component) | Hard | Dimensionality reduction |
| 12 | [Is the Matrix Orthogonal?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/eigen-pca/is-the-matrix-orthogonal) | Easy | QᵀQ = I |
| 13 | [Gram–Schmidt](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/eigen-pca/gram-schmidt) | Medium | Make vectors perpendicular |
| 14 | [Powers by Diagonalising](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/eigen-pca/powers-by-diagonalising) | Hard | Aⁿ = P Dⁿ P⁻¹ |
| 15 | [Markov Chain Steady State](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/eigen-pca/markov-chain-steady-state) | Medium | Eigenvector for λ = 1 |
| 16 | [Singular Values of a 2×2](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/eigen-pca/singular-values-of-a-2-2) | Medium | √ eigenvalues of AᵀA |
| 17 | [Condition Number](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/eigen-pca/condition-number) | Medium | σ_max / σ_min |
| 18 | [Error of the Best Rank-1 Approximation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/eigen-pca/error-of-the-best-rank-1-approximation) | Hard | Eckart–Young |
| 19 | [PageRank of a Tiny Web](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/eigen-pca/pagerank-of-a-tiny-web) | Hard | Eigenvector of the link matrix |
| 20 | [Fibonacci From Eigenvalues](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/eigen-pca/fibonacci-from-eigenvalues) | Hard | Binet's formula |

## Calculus: Derivatives & Integrals

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Derivative From the Definition](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/calculus/derivative-from-the-definition) | Easy | Shrinking the secant |
| 2 | [Derivative of sin x](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/calculus/derivative-of-sin-x) | Easy | Numerical vs exact |
| 3 | [Power Rule for Polynomials](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/calculus/power-rule-for-polynomials) | Easy | d/dx xⁿ = n·xⁿ⁻¹ |
| 4 | [Slope of a Curve at a Point](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/calculus/slope-of-a-curve-at-a-point) | Easy | f′(a) |
| 5 | [Tangent Line](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/calculus/tangent-line) | Medium | y = f′(a)(x − a) + f(a) |
| 6 | [Product Rule](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/calculus/product-rule) | Medium | (fg)′ = f′g + fg′ |
| 7 | [Chain Rule](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/calculus/chain-rule) | Medium | d/dx (ax + b)ⁿ |
| 8 | [Derivative of the Sigmoid](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/calculus/derivative-of-the-sigmoid) | Medium | σ′ = σ(1 − σ) |
| 9 | [Critical Points of a Cubic](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/calculus/critical-points-of-a-cubic) | Medium | Where f′(x) = 0 |
| 10 | [Maximum or Minimum?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/calculus/maximum-or-minimum) | Medium | Second-derivative test |
| 11 | [Second Derivative](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/calculus/second-derivative) | Easy | Curvature |
| 12 | [Newton's Method](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/calculus/newtons-method) | Medium | x ← x − f(x)/f′(x) |
| 13 | [Lowest Point of a Curve](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/calculus/lowest-point-of-a-curve) | Medium | Optimisation with f′ = 0 |
| 14 | [Area by Rectangles](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/calculus/area-by-rectangles) | Easy | Left Riemann sum |
| 15 | [Distance From Speed Readings](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/calculus/distance-from-speed-readings) | Easy | Trapezoid rule |
| 16 | [Antiderivative of a Polynomial](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/calculus/antiderivative-of-a-polynomial) | Easy | ∫ xⁿ dx = xⁿ⁺¹/(n + 1) |
| 17 | [Exact Area Under a Polynomial](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/calculus/exact-area-under-a-polynomial) | Medium | Fundamental theorem of calculus |
| 18 | [Average Value of a Function](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/calculus/average-value-of-a-function) | Medium | (1/(b − a)) ∫ f |
| 19 | [Area Between Two Curves](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/calculus/area-between-two-curves) | Hard | ∫ (top − bottom) |
| 20 | [Speed From Position Readings](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/calculus/speed-from-position-readings) | Medium | Derivative of data |

## Gradients & Optimisation

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Partial Derivatives](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/optimization/partial-derivatives) | Easy | ∂f/∂x and ∂f/∂y |
| 2 | [The Gradient Vector](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/optimization/the-gradient-vector) | Easy | ∇f |
| 3 | [Gradient of a Quadratic Form](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/optimization/gradient-of-a-quadratic-form) | Medium | ∇(vᵀAv) = (A + Aᵀ)v |
| 4 | [Directional Derivative](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/optimization/directional-derivative) | Medium | ∇f · u |
| 5 | [Steepest Downhill Direction](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/optimization/steepest-downhill-direction) | Easy | −∇f / ‖∇f‖ |
| 6 | [One Gradient-Descent Step](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/optimization/one-gradient-descent-step) | Easy | w ← w − lr·∇f |
| 7 | [Gradient Descent in 1-D](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/optimization/gradient-descent-in-1-d) | Easy | Walking downhill |
| 8 | [Is the Learning Rate Too Big?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/optimization/is-the-learning-rate-too-big) | Medium | Loss curve |
| 9 | [Descent in a Long Narrow Valley](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/optimization/descent-in-a-long-narrow-valley) | Medium | Different curvature per direction |
| 10 | [Mean Squared Error of a Line](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/optimization/mean-squared-error-of-a-line) | Easy | The loss |
| 11 | [Gradient of the MSE](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/optimization/gradient-of-the-mse) | Medium | ∂L/∂m and ∂L/∂b |
| 12 | [Fit a Line by Gradient Descent](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/optimization/fit-a-line-by-gradient-descent) | Hard | Training loop |
| 13 | [Chain Rule Through a Computation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/optimization/chain-rule-through-a-computation) | Medium | dy/dx of sin(3x² + 1) |
| 14 | [Backpropagation Through One Neuron](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/optimization/backpropagation-through-one-neuron) | Hard | ŷ = σ(wx + b), L = (ŷ − y)² |
| 15 | [One Step of Logistic Regression](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/optimization/one-step-of-logistic-regression) | Hard | Log-loss gradient |
| 16 | [The Hessian Matrix](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/optimization/the-hessian-matrix) | Medium | Second partial derivatives |
| 17 | [Is the Bowl Convex?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/optimization/is-the-bowl-convex) | Medium | Positive semi-definite Hessian |
| 18 | [Bottom of a Quadratic Bowl](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/optimization/bottom-of-a-quadratic-bowl) | Hard | ∇f = 0 ⇒ Av = b |
| 19 | [Mini-batch Gradient](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/optimization/mini-batch-gradient) | Medium | Averaging over a batch |
| 20 | [Newton's Method for a Minimum](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/optimization/newtons-method-for-a-minimum) | Hard | x ← x − f′/f″ |

## Probability

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Rolling a Total With Two Dice](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/probability/rolling-a-total-with-two-dice) | Easy | Count the outcomes |
| 2 | [At Least One Six](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/probability/at-least-one-six) | Easy | The complement rule |
| 3 | [Permutations](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/probability/permutations) | Easy | Order matters: n!/(n − k)! |
| 4 | [Combinations](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/probability/combinations) | Easy | Order doesn't matter: n choose k |
| 5 | [Arrangements With Repeated Letters](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/probability/arrangements-with-repeated-letters) | Medium | n! / (a!·b!·…) |
| 6 | [Drawing a Card: Or](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/probability/drawing-a-card-or) | Easy | Addition rule |
| 7 | [Conditional Probability From a Table](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/probability/conditional-probability-from-a-table) | Medium | P(A | B) |
| 8 | [Bayes' Theorem: Medical Test](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/probability/bayes-theorem-medical-test) | Medium | P(disease | positive) |
| 9 | [Law of Total Probability](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/probability/law-of-total-probability) | Easy | Weighted average over cases |
| 10 | [Expected Value](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/probability/expected-value) | Easy | E[X] = Σ x·P(x) |
| 11 | [Variance of a Random Variable](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/probability/variance-of-a-random-variable) | Medium | E[(X − μ)²] |
| 12 | [The Birthday Problem](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/probability/the-birthday-problem) | Medium | Surprisingly likely coincidences |
| 13 | [At Least k Heads](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/probability/at-least-k-heads) | Medium | Summing binomial counts |
| 14 | [All Parts Must Work](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/probability/all-parts-must-work) | Easy | Independent events multiply |
| 15 | [Are the Events Independent?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/probability/are-the-events-independent) | Medium | P(A and B) = P(A)·P(B) |
| 16 | [Marginal Probabilities](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/probability/marginal-probabilities) | Easy | Summing out a variable |
| 17 | [Monty Hall](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/probability/monty-hall) | Medium | Should you switch? |
| 18 | [Naive Bayes Spam Score](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/probability/naive-bayes-spam-score) | Hard | Multiply likelihoods, normalise |
| 19 | [Waiting for the First Success](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/probability/waiting-for-the-first-success) | Medium | Geometric distribution: E = 1/p |
| 20 | [Two Draws Without Replacement](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/probability/two-draws-without-replacement) | Easy | Multiplication rule |

## Distributions & Information

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Bernoulli Mean and Variance](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/distributions/bernoulli-mean-and-variance) | Easy | One yes/no trial |
| 2 | [Binomial Probability Table](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/distributions/binomial-probability-table) | Medium | k successes in n tries |
| 3 | [Poisson Probability](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/distributions/poisson-probability) | Easy | Counts of rare events |
| 4 | [Uniform Distribution](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/distributions/uniform-distribution) | Easy | Every value equally likely |
| 5 | [Height of the Normal Curve](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/distributions/height-of-the-normal-curve) | Easy | The bell curve's PDF |
| 6 | [Area Under the Normal Curve](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/distributions/area-under-the-normal-curve) | Medium | CDF: P(X ≤ x) |
| 7 | [The 68–95–99.7 Rule](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/distributions/the-68-95-99-7-rule) | Medium | P(a ≤ X ≤ b) |
| 8 | [Z-Score to Percentile](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/distributions/z-score-to-percentile) | Easy | Standardising |
| 9 | [Exponential Waiting Time](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/distributions/exponential-waiting-time) | Easy | P(wait ≤ t) |
| 10 | [Distribution of the Sum of Two Dice](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/distributions/distribution-of-the-sum-of-two-dice) | Easy | Convolution |
| 11 | [Sum of Three Dice](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/distributions/sum-of-three-dice) | Medium | Towards the bell curve |
| 12 | [Entropy](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/distributions/entropy) | Medium | Average surprise in bits |
| 13 | [Cross-Entropy](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/distributions/cross-entropy) | Medium | How well q predicts p |
| 14 | [KL Divergence](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/distributions/kl-divergence) | Medium | Extra bits from using the wrong distribution |
| 15 | [Softmax](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/distributions/softmax) | Medium | Scores → probabilities |
| 16 | [Binary Log-Loss](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/distributions/binary-log-loss) | Medium | The loss of logistic regression |
| 17 | [Gini Impurity](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/distributions/gini-impurity) | Easy | How mixed is a group? |
| 18 | [Information Gain of a Split](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/distributions/information-gain-of-a-split) | Hard | How decision trees choose questions |
| 19 | [Maximum Likelihood for a Coin](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/distributions/maximum-likelihood-for-a-coin) | Medium | Best p for the data |
| 20 | [Log-Likelihood Under a Normal Model](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/math/#/q/distributions/log-likelihood-under-a-normal-model) | Medium | Σ log f(xᵢ) |

## Build

```bash
python3 handbook/build.py --book math
```

Sources live in `math/src/`: `topics/` (questions and solutions), `lessons/` and `theory/`.
