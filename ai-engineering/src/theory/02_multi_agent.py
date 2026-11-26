from lib import *

THEORY("Workflow vs agent", """
<table>
<tr><th></th><th>Workflow</th><th>Agent</th></tr>
<tr><td>Who decides the steps</td><td>your code</td><td>the model</td></tr>
<tr><td>Predictability</td><td>high</td><td>lower</td></tr>
<tr><td>Cost and latency</td><td>bounded</td><td>variable</td></tr>
<tr><td>Best for</td><td>well-understood tasks</td><td>open-ended tasks</td></tr>
</table>
""")

THEORY("Failure modes to design for", """
<ul>
<li><b>Loops</b>: repeating the same tool call — detect repeats, cap steps.</li>
<li><b>Drift</b>: forgetting the goal over a long run — restate the goal, summarise progress.</li>
<li><b>Error cascades</b>: one agent's mistake becomes another's input — validate between steps.</li>
<li><b>Conflicting writes</b> to shared state — versions or single ownership.</li>
<li><b>Runaway cost</b> — token, step and time budgets.</li>
<li><b>Over-delegation</b> — orchestrators that spawn too many workers for simple tasks.</li>
</ul>
""")

FAQ("When should you NOT use multi-agent systems?", "<p>When a single call, a prompt chain or one agent with good tools does the job. Multiple agents multiply tokens and failure modes; use them only when sub-tasks are independent or need separate specialisation or context.</p>")
FAQ("Router vs orchestrator?", "<p>A router classifies a request once and sends it to one handler. An orchestrator plans several sub-tasks at run time, delegates them to workers and combines the results.</p>")
FAQ("How do you stop an agent looping forever?", "<p>Cap steps and tokens, detect repeated identical tool calls, and give the model a way to stop (or escalate to a human) when it's stuck.</p>")
FAQ("What is a handoff?", "<p>Transferring the conversation from one agent to another more suitable one, along with the context it needs — ideally a summary plus recent messages.</p>")
FAQ("How do you evaluate a multi-agent system?", "<p>End to end on realistic tasks: success rate, cost, latency and number of steps, plus traces to find which agent caused each failure.</p>")
FAQ("Why does the critical path matter?", "<p>With parallel workers, total time is the longest chain of dependent tasks, not the sum of all tasks — so it tells you how much parallelism can actually speed things up.</p>")
