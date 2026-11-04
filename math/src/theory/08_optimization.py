from lib import *

THEORY("Multivariable calculus", """
<ul>
<li><b>Partial derivative</b> ∂f/∂xᵢ: derivative with respect to xᵢ, all other variables held constant.</li>
<li><b>Gradient</b> ∇f = (∂f/∂x₁, …, ∂f/∂xₙ): direction of steepest ascent; ‖∇f‖ is the steepest slope; ∇f ⟂ level curves.</li>
<li><b>Directional derivative</b> D_u f = ∇f·u for a unit vector u.</li>
<li><b>Jacobian</b>: for a vector-valued function, the matrix of all first partials (one row per output).</li>
<li><b>Hessian</b> H: the matrix of second partials, Hᵢⱼ = ∂²f/∂xᵢ∂xⱼ (symmetric for smooth f).</li>
<li><b>Multivariable chain rule</b>: dL/dx = Σ (∂L/∂uᵢ)(∂uᵢ/∂x) — sum over every path.</li>
</ul>
<table><tr><th>f(x)</th><th>∇f</th></tr>
<tr><td>aᵀx</td><td>a</td></tr><tr><td>xᵀAx</td><td>(A + Aᵀ)x</td></tr><tr><td>‖x‖²</td><td>2x</td></tr><tr><td>‖Xw − y‖²</td><td>2Xᵀ(Xw − y)</td></tr></table>
""")

THEORY("Optimality conditions", """
<ul>
<li>First order: at an interior minimum ∇f = 0 (a <b>stationary point</b>).</li>
<li>Second order: H positive definite (all eigenvalues &gt; 0) ⇒ local minimum; negative definite ⇒ maximum; mixed signs ⇒ <b>saddle point</b> (common in deep learning).</li>
<li><b>Convex</b> f (H ⪰ 0 everywhere): every local minimum is global. MSE linear regression and log-loss logistic regression are convex; neural networks are not.</li>
</ul>
""")

THEORY("Gradient-based algorithms", """
<table>
<tr><th>Method</th><th>Update</th><th>Notes</th></tr>
<tr><td>Gradient descent</td><td>w ← w − η∇L(w)</td><td>η = learning rate; converges for η &lt; 2/λ_max on quadratics</td></tr>
<tr><td>Stochastic / mini-batch GD</td><td>gradient on a random batch</td><td>cheap, noisy steps; the default for big data</td></tr>
<tr><td>Momentum</td><td>v ← βv + ∇L; w ← w − ηv</td><td>damps zig-zags in narrow valleys</td></tr>
<tr><td>Adam</td><td>momentum + per-weight step sizes</td><td>default optimiser for deep learning</td></tr>
<tr><td>Newton</td><td>w ← w − H⁻¹∇L</td><td>very fast near the minimum, but H is expensive</td></tr>
</table>
<p>Practical tips: scale features, watch the loss curve, lower η if the loss oscillates or explodes, use learning-rate schedules, and add L2 regularisation λ‖w‖² (gradient term 2λw) to fight overfitting.</p>
""")

THEORY("Backpropagation", """
<p>A network computes a chain x → z₁ → a₁ → z₂ → … → L. Backprop stores the forward values, then walks backwards multiplying local derivatives (the chain rule), reusing each intermediate result, so the full gradient costs about as much as one forward pass. Frameworks (PyTorch, TensorFlow, JAX) do this automatically — <b>automatic differentiation</b>. Vanishing gradients happen when many local derivatives &lt; 1 (e.g. sigmoid's max is 0.25) are multiplied together — a reason ReLU became popular.</p>
""")

FAQ("What is a gradient in plain words?", "<p>An arrow pointing uphill on the loss landscape, with one component per weight saying how much the loss changes if you nudge that weight.</p>")
FAQ("Why do we move against the gradient?", "<p>The gradient points to steepest increase; we want the loss to decrease, so we step in the opposite direction.</p>")
FAQ("What happens if the learning rate is too high?", "<p>Steps overshoot the minimum. The loss oscillates or grows (diverges), sometimes until it becomes NaN.</p>")
FAQ("Batch vs stochastic vs mini-batch gradient descent?", "<p>Batch uses all data per step (accurate, slow); stochastic uses one example (fast, very noisy); mini-batch uses a small group (the practical middle ground, and GPU-friendly).</p>")
FAQ("What is a saddle point?", "<p>A stationary point that is a minimum in some directions and a maximum in others, like a horse saddle. The gradient is zero but it is not a minimum.</p>")
FAQ("What is a gradient check?", "<p>Comparing an analytic gradient against a numerical one, (L(w + h) − L(w − h))/2h, for a few weights; a mismatch reveals a bug in backprop code.</p>")
