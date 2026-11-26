from lib import *

LESSON("Basics", "What makes something an agent", """
<p>An <b>agent</b> is a model in a loop: it looks at the goal and what has happened so far, decides on an action (usually a tool call), sees the result, and repeats until it decides it's done. The model chooses the steps — that's the difference from a <b>workflow</b>, where your code fixes the steps in advance.</p>
<pre><code class="py">import anthropic
client = anthropic.Anthropic()
messages = [{"role": "user", "content": goal}]
for step in range(MAX_STEPS):
    reply = client.messages.create(model="claude-opus-5-5", max_tokens=2000, tools=TOOLS, messages=messages)
    messages.append({"role": "assistant", "content": reply.content})
    if reply.stop_reason != "tool_use":
        break                                          # the model gave its final answer
    results = [{"type": "tool_result", "tool_use_id": b.id, "content": run_tool(b.name, b.input)}
               for b in reply.content if b.type == "tool_use"]
    messages.append({"role": "user", "content": results})</code></pre>
<p>Always cap the number of steps: a confused agent will otherwise loop, burning tokens. The Claude SDKs also ship a tool runner and the Claude Agent SDK, which run this loop for you.</p>
""", practice=["Run the Agent Loop", "Catch an Agent Going in Circles"])

LESSON("Core", "Patterns, from simple to autonomous", """
<table>
<tr><th>Pattern</th><th>How it works</th><th>Use when</th></tr>
<tr><td><b>Prompt chain</b></td><td>fixed steps, each call uses the last one's output</td><td>the steps are known (outline → draft → translate)</td></tr>
<tr><td><b>Router</b></td><td>classify, then send to a specialised prompt or model</td><td>distinct kinds of request (billing vs tech support)</td></tr>
<tr><td><b>Parallel fan-out</b></td><td>independent sub-tasks at once, then combine (or vote)</td><td>parts don't depend on each other; you want speed or several opinions</td></tr>
<tr><td><b>Orchestrator–workers</b></td><td>a lead model plans sub-tasks at run time and delegates</td><td>you can't know the sub-tasks in advance (research, big code changes)</td></tr>
<tr><td><b>Evaluator–optimizer</b></td><td>one model drafts, another critiques, repeat</td><td>clear quality criteria and iteration helps</td></tr>
<tr><td><b>Autonomous agent</b></td><td>model loops with tools until done</td><td>open-ended tasks with an unknown number of steps</td></tr>
</table>
<p>The golden rule: <b>use the simplest pattern that solves the problem</b>. Each step up adds cost, latency and failure modes. Many "agents" in production are a router plus two prompt chains.</p>
""", practice=["Pick the Simplest Pattern That Works", "Route to a Specialist", "Combine Worker Answers by Vote", "Evaluator–Optimizer Loop"])

LESSON("Core", "Planning, dependencies and parallelism", """
<p>An orchestrator first <b>plans</b>: it breaks the goal into sub-tasks and notes which depend on which. That's a graph, so the run order is a <b>topological sort</b>, and independent tasks can run at the same time. The time to finish is the <b>critical path</b> (the longest chain of dependent tasks), not the sum of all tasks.</p>
<pre><code class="py">import asyncio
async def run_level(tasks):                       # everything whose dependencies are done
    return await asyncio.gather(*(worker(t) for t in tasks))</code></pre>
<p>Real systems also cap concurrency (API rate limits), so workers form a <b>pool</b>, and they set <b>timeouts</b> so one slow worker doesn't hold up the answer — returning partial results is usually better than waiting.</p>
""", practice=["Order a Plan", "How Long With Parallel Workers?", "A Pool of Workers", "Workers That Time Out", "Map–Reduce Over a Long Document"])

LESSON("Core", "Handoffs, shared state and messages", """
<p>Agents coordinate in three main ways:</p>
<ul>
<li><b>Handoffs</b>: the current agent transfers the conversation to a specialist (triage → billing → refunds). Guard against ping-pong loops and endless chains, and pass a <b>summary plus recent messages</b>, not the whole history.</li>
<li><b>Shared state</b> (a "blackboard"): agents read and write a common store. Concurrent writers can overwrite each other, so use versions (optimistic locking) or a single owner per key.</li>
<li><b>Messages</b>: agents send each other messages through inboxes — flexible but hard to debug, so log every message.</li>
</ul>
""", practice=["Follow the Handoffs", "Hand Off Only What's Needed", "Shared State Without Lost Updates", "Deliver Messages Between Agents", "Merge Sources From Workers"])

LESSON("Advanced", "Graph workflows (LangGraph and friends)", """
<p>Frameworks such as LangGraph model an agent system as a <b>state machine</b>: nodes are steps (often model calls), edges say what comes next, and <b>conditional edges</b> decide based on the state. This makes loops, retries and human approval steps explicit, and the state can be saved (checkpointed) so a run can pause and resume.</p>
<pre><code class="py">from langgraph.graph import StateGraph, START, END
g = StateGraph(State)
g.add_node("draft", draft); g.add_node("review", review)
g.add_edge(START, "draft"); g.add_edge("draft", "review")
g.add_conditional_edges("review", lambda s: END if s["score"] &gt;= 8 else "draft")
app = g.compile(); app.invoke({"topic": "MCP"})</code></pre>
<p>Whatever the framework, the ideas are the ones you build by hand in this topic — knowing them lets you debug any framework, or skip it.</p>
""", practice=["Run a Graph Workflow"])

LESSON("Advanced", "Cost, safety and when multi-agent is worth it", """
<ul>
<li><b>Cost multiplies</b>: each agent re-reads context. A four-worker system can easily use five times the tokens of one agent. It pays off when sub-tasks are truly independent and parallelism or specialisation improves quality.</li>
<li><b>Budgets</b>: cap tokens, steps and wall-clock time per run, and per agent.</li>
<li><b>Least privilege</b>: each agent gets only the tools it needs; a researcher doesn't need write access.</li>
<li><b>Observability</b>: log every model call, tool call and handoff with a shared trace id (see the Observability topic) — multi-agent bugs are invisible otherwise.</li>
<li><b>Evaluate the whole system</b> on real tasks, not each agent in isolation.</li>
</ul>
""", practice=["What Do Extra Agents Cost?", "Stay Within the Token Budget", "Each Agent Only Gets Its Own Tools"])
