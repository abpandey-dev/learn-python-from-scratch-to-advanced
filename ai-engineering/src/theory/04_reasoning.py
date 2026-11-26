from lib import *

THEORY("Ways to spend test-time compute", """
<table>
<tr><th>Method</th><th>How</th><th>Needs</th></tr>
<tr><td>Thinking</td><td>longer internal reasoning</td><td>a reasoning model</td></tr>
<tr><td>Chain-of-thought prompt</td><td>ask a standard model to reason first</td><td>nothing extra</td></tr>
<tr><td>Self-consistency</td><td>sample n, majority vote</td><td>answers you can compare</td></tr>
<tr><td>Best-of-N</td><td>sample n, verifier picks</td><td>a verifier (tests, checker, reward model)</td></tr>
<tr><td>Search (beam, tree)</td><td>expand and prune steps</td><td>a step-level verifier</td></tr>
<tr><td>Refinement</td><td>draft, critique, revise</td><td>clear criteria</td></tr>
</table>
""")

THEORY("When reasoning helps", """
<ul>
<li>Helps: multi-step maths, code, planning, logic puzzles, analysing long documents with many constraints, agentic tool use with many decisions.</li>
<li>Doesn't help much: fact lookup, simple classification, extraction, short rewrites, chit-chat.</li>
<li>Can hurt: latency-critical UIs, very high volume cheap tasks.</li>
</ul>
""")

FAQ("Why are reasoning models expensive?", "<p>They generate many thinking tokens before the answer, and those are billed as output tokens, which cost more than input. Latency also grows with the thinking length.</p>")
FAQ("What is self-consistency?", "<p>Sampling several answers and taking the most common. It improves accuracy when each sample is more likely right than wrong, and agreement doubles as a confidence signal.</p>")
FAQ("Best-of-N vs majority vote?", "<p>Majority vote needs no verifier but needs most samples to agree. Best-of-N needs a verifier but only needs one correct sample, so it scales better when a reliable check exists.</p>")
FAQ("What is pass@k and why the special formula?", "<p>The chance that at least one of k samples passes the tests. Estimating it from n ≥ k samples with 1 − C(n−c,k)/C(n,k) is unbiased and lower-variance than drawing exactly k samples.</p>")
FAQ("How do you decide whether to use a reasoning model?", "<p>Evaluate on your own tasks at different effort levels and models, then choose by accuracy per dollar and latency. Route only hard requests to reasoning.</p>")
FAQ("Process vs outcome reward?", "<p>Outcome rewards score only the final answer; process rewards score each step. Process signals catch right answers reached by wrong reasoning and help search.</p>")
