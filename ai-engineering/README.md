# AI Engineering

9 topics · theory with 54 theory questions · 47 lessons from basics to advanced · 180 practice questions with answers · MCP, multi-agent systems, context engineering and memory, reasoning models, LLM serving, observability and evals, fine-tuning with LoRA and DPO, multimodal AI, and shipping AI products · every idea is built from scratch in plain Python so you can see inside it, then written the efficient way, both shown running step by step.

**Live site:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/

Every solution is run against its test cases by `build.py` before the site is generated, and each animation is recorded from a real run of the code you see.

## Topics

- [MCP: Connecting AI to Tools and Data](#mcp-connecting-ai-to-tools-and-data) — The Model Context Protocol from the wire up: JSON-RPC messages, the stdio transport, the initialize handshake, tools, resources and prompts, input-schema validation, errors, pagination, permissions, and turning MCP tools into LLM tool definitions.
- [Agents & Multi-Agent Orchestration](#agents-multi-agent-orchestration) — How agent systems really work: the tool loop, routing, planning with dependencies, parallel fan-out, orchestrator–workers, handoffs, shared state, evaluator–optimizer loops, budgets, loop detection, worker pools and graph workflows like LangGraph.
- [Context Engineering & Agent Memory](#context-engineering-agent-memory) — Decide what the model sees: token budgets, trimming and compaction, ordering for prompt caching, 'lost in the middle', clearing old tool results, just-in-time retrieval, and long-term memory — extracting facts, add/update/skip decisions, recall with recency, and resolving conflicts.
- [Reasoning Models & Test-Time Compute](#reasoning-models-test-time-compute) — Models that think before answering: what thinking tokens cost, effort levels, when reasoning helps, self-consistency voting, best-of-N with verifiers, pass@k, process vs outcome checks, routing easy and hard questions, and checking a model's working.
- [Serving LLMs: Inference Optimisation](#serving-llms-inference-optimisation) — What it takes to run models yourself: memory for weights and the KV cache, batching (static vs continuous), prefill vs decode, speculative decoding, quantisation, paged KV memory and prefix sharing, scheduling, rate limits, fallbacks and the self-host vs API cost decision.
- [Observability, Tracing & Evals in Production](#observability-tracing-evals-in-production) — See what your AI system is doing and whether it's good: traces and spans, self time and the critical path, cost per feature, error rates, trace sampling, redacting secrets, LLM-as-judge, judge–human agreement, pairwise comparisons without position bias, faithfulness, regression gates and online feedback.
- [Fine-Tuning in Practice: LoRA, QLoRA & DPO](#fine-tuning-in-practice-lora-qlora-dpo) — Adapt open models yourself: when to fine-tune, LoRA maths and merging, memory for full vs LoRA vs QLoRA, chat templates and loss masking, packing, cleaning and de-duplicating data, schedules and batch sizes, preference data and the DPO loss, early stopping and checking for forgetting.
- [Multimodal AI: Images, Documents & Speech](#multimodal-ai-images-documents-speech) — Build with images, PDFs and audio: how images become tokens and what they cost, resizing and patches, sending images to an API, document AI (reading order, tables, field validation, page routing), speech (framing, chunking, WER, subtitles), CLIP-style zero-shot labels, voice-agent latency and video frames.
- [Shipping AI Products: Streaming, Coding Agents & Guardrails](#shipping-ai-products-streaming-coding-agents-guardrails) — Turn a prototype into a product: streaming responses and tool input, structured output and repair, retries and fallbacks, coding-agent tools (edits, diffs, the test-fix loop), sandboxing and computer use, semantic caching, budgets, guardrails, prompt versioning and cost planning.

## MCP: Connecting AI to Tools and Data

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Write a JSON-RPC Request](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/mcp/write-a-json-rpc-request) | Easy | Message shape |
| 2 | [Read Messages from stdio](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/mcp/read-messages-from-stdio) | Easy | Newline-delimited JSON |
| 3 | [What Kind of Message Is This?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/mcp/what-kind-of-message-is-this) | Easy | Requests, notifications, responses |
| 4 | [Answer With the Right Error](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/mcp/answer-with-the-right-error) | Easy | JSON-RPC error codes |
| 5 | [Validate Tool Arguments](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/mcp/validate-tool-arguments) | Medium | inputSchema |
| 6 | [Describe Python Functions as Tools](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/mcp/describe-python-functions-as-tools) | Medium | tools/list from code |
| 7 | [Handle tools/call](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/mcp/handle-tools-call) | Medium | Results and isError |
| 8 | [Agree on a Protocol Version](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/mcp/agree-on-a-protocol-version) | Easy | initialize |
| 9 | [Which Features Can Be Used?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/mcp/which-features-can-be-used) | Easy | Capability negotiation |
| 10 | [Route a Resource URI](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/mcp/route-a-resource-uri) | Medium | Resource templates |
| 11 | [Read a Resource](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/mcp/read-a-resource) | Easy | resources/read |
| 12 | [Paginate tools/list](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/mcp/paginate-tools-list) | Medium | Cursors |
| 13 | [MCP Tools → Claude API Tools](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/mcp/mcp-tools-claude-api-tools) | Easy | Bridging protocols |
| 14 | [Avoid Name Clashes Across Servers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/mcp/avoid-name-clashes-across-servers) | Medium | Namespacing |
| 15 | [Match Responses to Requests](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/mcp/match-responses-to-requests) | Medium | Out-of-order replies |
| 16 | [Fill a Prompt Template](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/mcp/fill-a-prompt-template) | Easy | prompts/get |
| 17 | [Decide Which Calls Need Approval](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/mcp/decide-which-calls-need-approval) | Medium | Tool annotations · permissions |
| 18 | [Keep Tool Output Within Budget](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/mcp/keep-tool-output-within-budget) | Easy | Context hygiene |
| 19 | [Progress Notifications](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/mcp/progress-notifications) | Easy | Long-running tools |
| 20 | [A Whole MCP Session](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/mcp/a-whole-mcp-session) | Hard | Putting it together |

## Agents & Multi-Agent Orchestration

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Run the Agent Loop](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multi-agent/run-the-agent-loop) | Easy | Tool use until done |
| 2 | [Route to a Specialist](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multi-agent/route-to-a-specialist) | Easy | Router pattern |
| 3 | [Order a Plan](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multi-agent/order-a-plan) | Medium | Dependencies · topological sort |
| 4 | [How Long With Parallel Workers?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multi-agent/how-long-with-parallel-workers) | Medium | Fan-out · critical path |
| 5 | [Combine Worker Answers by Vote](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multi-agent/combine-worker-answers-by-vote) | Easy | Orchestrator–workers |
| 6 | [Follow the Handoffs](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multi-agent/follow-the-handoffs) | Medium | Handoff pattern |
| 7 | [Shared State Without Lost Updates](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multi-agent/shared-state-without-lost-updates) | Medium | Blackboard · optimistic locking |
| 8 | [Deliver Messages Between Agents](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multi-agent/deliver-messages-between-agents) | Medium | Inboxes · queues |
| 9 | [Evaluator–Optimizer Loop](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multi-agent/evaluator-optimizer-loop) | Easy | Generate, critique, retry |
| 10 | [Stay Within the Token Budget](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multi-agent/stay-within-the-token-budget) | Easy | Cost control |
| 11 | [What Do Extra Agents Cost?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multi-agent/what-do-extra-agents-cost) | Medium | Token multiplication |
| 12 | [Catch an Agent Going in Circles](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multi-agent/catch-an-agent-going-in-circles) | Easy | Loop detection |
| 13 | [Each Agent Only Gets Its Own Tools](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multi-agent/each-agent-only-gets-its-own-tools) | Easy | Least privilege |
| 14 | [Workers That Time Out](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multi-agent/workers-that-time-out) | Easy | Partial results |
| 15 | [Map–Reduce Over a Long Document](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multi-agent/map-reduce-over-a-long-document) | Medium | How many model calls? |
| 16 | [Hand Off Only What's Needed](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multi-agent/hand-off-only-whats-needed) | Easy | Context on handoff |
| 17 | [A Pool of Workers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multi-agent/a-pool-of-workers) | Hard | Concurrency limits |
| 18 | [Run a Graph Workflow](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multi-agent/run-a-graph-workflow) | Hard | State machines (LangGraph style) |
| 19 | [Merge Sources From Workers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multi-agent/merge-sources-from-workers) | Easy | Citations |
| 20 | [Pick the Simplest Pattern That Works](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multi-agent/pick-the-simplest-pattern-that-works) | Easy | Design judgement |

## Context Engineering & Agent Memory

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Estimate Tokens](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/context-memory/estimate-tokens) | Easy | Budgets start with counting |
| 2 | [Fit the History Into the Window](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/context-memory/fit-the-history-into-the-window) | Medium | Trimming |
| 3 | [Compact the Conversation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/context-memory/compact-the-conversation) | Medium | Summarise the oldest turns |
| 4 | [Avoid 'Lost in the Middle'](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/context-memory/avoid-lost-in-the-middle) | Medium | Ordering documents |
| 5 | [Put Stable Content First](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/context-memory/put-stable-content-first) | Easy | Cache-friendly order |
| 6 | [What Does Caching Save?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/context-memory/what-does-caching-save) | Medium | Prompt-cache pricing |
| 7 | [Clear Old Tool Results](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/context-memory/clear-old-tool-results) | Easy | Context editing |
| 8 | [Share the Budget Between Sections](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/context-memory/share-the-budget-between-sections) | Medium | Allocation |
| 9 | [Choose Few-Shot Examples](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/context-memory/choose-few-shot-examples) | Medium | Dynamic examples |
| 10 | [Load Files Just in Time](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/context-memory/load-files-just-in-time) | Easy | Preload vs on-demand |
| 11 | [The Hidden Cost of Long Chats](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/context-memory/the-hidden-cost-of-long-chats) | Medium | History is re-sent every turn |
| 12 | [Extract Facts to Remember](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/context-memory/extract-facts-to-remember) | Medium | Memory extraction |
| 13 | [Add, Update or Skip?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/context-memory/add-update-or-skip) | Medium | Memory consolidation |
| 14 | [Recall the Right Memories](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/context-memory/recall-the-right-memories) | Medium | Relevance × recency |
| 15 | [Short-Term Buffer, Long-Term Store](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/context-memory/short-term-buffer-long-term-store) | Easy | Memory tiers |
| 16 | [A Notes File the Agent Keeps](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/context-memory/a-notes-file-the-agent-keeps) | Easy | Structured note-taking |
| 17 | [Newest Fact Wins](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/context-memory/newest-fact-wins) | Easy | Conflicting memories |
| 18 | [Assemble the Final Prompt](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/context-memory/assemble-the-final-prompt) | Medium | Putting it together |
| 19 | [Is the Prefix Cached?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/context-memory/is-the-prefix-cached) | Medium | Cache hits |
| 20 | [What's Eating the Window?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/context-memory/whats-eating-the-window) | Easy | Context audits |

## Reasoning Models & Test-Time Compute

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [What Does Thinking Cost?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/reasoning/what-does-thinking-cost) | Easy | Thinking is billed as output |
| 2 | [How Long Will the User Wait?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/reasoning/how-long-will-the-user-wait) | Easy | Latency |
| 3 | [Majority Voting Helps — How Much?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/reasoning/majority-voting-helps-how-much) | Medium | Self-consistency |
| 4 | [How Many Samples for Best-of-N?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/reasoning/how-many-samples-for-best-of-n) | Easy | Verifiers |
| 5 | [Unbiased pass@k](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/reasoning/unbiased-pass-k) | Medium | Evaluating code models |
| 6 | [Find the Final Answer](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/reasoning/find-the-final-answer) | Easy | Parsing reasoning |
| 7 | [Separate Thinking From the Answer](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/reasoning/separate-thinking-from-the-answer) | Easy | Response blocks |
| 8 | [Choose the Effort Level](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/reasoning/choose-the-effort-level) | Easy | Cheapest level that's good enough |
| 9 | [Route Easy and Hard Questions](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/reasoning/route-easy-and-hard-questions) | Medium | Reasoning only where it pays |
| 10 | [Judge the Steps, Not Just the Answer](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/reasoning/judge-the-steps-not-just-the-answer) | Medium | Process vs outcome scoring |
| 11 | [Check the Arithmetic in the Working](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/reasoning/check-the-arithmetic-in-the-working) | Medium | Verifying reasoning |
| 12 | [Combine Numeric Estimates](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/reasoning/combine-numeric-estimates) | Easy | Median beats mean |
| 13 | [Know When to Abstain](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/reasoning/know-when-to-abstain) | Medium | Agreement as confidence |
| 14 | [Accuracy Per Dollar](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/reasoning/accuracy-per-dollar) | Easy | Is reasoning worth it here? |
| 15 | [Sampling Many Times, Cheaply](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/reasoning/sampling-many-times-cheaply) | Medium | Caching the shared prompt |
| 16 | [Beam Search Over Reasoning Steps](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/reasoning/beam-search-over-reasoning-steps) | Hard | Search with a verifier |
| 17 | [Stop Thinking at the Budget](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/reasoning/stop-thinking-at-the-budget) | Easy | Budget control |
| 18 | [Prompt for Reasoning Without a Reasoning Model](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/reasoning/prompt-for-reasoning-without-a-reasoning-model) | Easy | Chain-of-thought prompts |
| 19 | [Does More Thinking Pay Off?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/reasoning/does-more-thinking-pay-off) | Medium | Diminishing returns |
| 20 | [Normalise Before You Vote](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/reasoning/normalise-before-you-vote) | Medium | Free-form answers |

## Serving LLMs: Inference Optimisation

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Memory for the Weights](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/serving/memory-for-the-weights) | Easy | Will it fit on the GPU? |
| 2 | [How Big Is the KV Cache?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/serving/how-big-is-the-kv-cache) | Medium | Memory grows with tokens |
| 3 | [How Many Users at Once?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/serving/how-many-users-at-once) | Medium | Concurrency on one GPU |
| 4 | [Static vs Continuous Batching](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/serving/static-vs-continuous-batching) | Hard | Why vLLM is fast |
| 5 | [Prefill vs Decode](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/serving/prefill-vs-decode) | Easy | Where the time goes |
| 6 | [Speculative Decoding: Expected Speed-Up](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/serving/speculative-decoding-expected-speed-up) | Medium | Draft and verify |
| 7 | [Verify a Draft](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/serving/verify-a-draft) | Medium | Accepting the matching prefix |
| 8 | [Quantise to int8](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/serving/quantise-to-int8) | Medium | Smaller and faster |
| 9 | [Why Group-Wise Scales Help](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/serving/why-group-wise-scales-help) | Medium | Outliers in quantisation |
| 10 | [Paged KV Memory](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/serving/paged-kv-memory) | Medium | PagedAttention |
| 11 | [Share the System Prompt's Cache](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/serving/share-the-system-prompts-cache) | Easy | Prefix caching |
| 12 | [How Many GPUs for the Traffic?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/serving/how-many-gpus-for-the-traffic) | Medium | Little's law |
| 13 | [Throughput vs Per-User Speed](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/serving/throughput-vs-per-user-speed) | Easy | Picking a batch size |
| 14 | [Cost per Million Tokens, Self-Hosted](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/serving/cost-per-million-tokens-self-hosted) | Easy | Unit economics |
| 15 | [Self-Host or Use an API?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/serving/self-host-or-use-an-api) | Medium | Break-even volume |
| 16 | [Shortest Job First](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/serving/shortest-job-first) | Medium | Scheduling |
| 17 | [A Token Bucket Rate Limiter](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/serving/a-token-bucket-rate-limiter) | Medium | Tokens per minute |
| 18 | [Fall Back When a Model Fails](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/serving/fall-back-when-a-model-fails) | Easy | Resilience |
| 19 | [Many Fine-Tunes on One GPU](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/serving/many-fine-tunes-on-one-gpu) | Easy | Serving LoRA adapters |
| 20 | [Longest Context That Fits](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/serving/longest-context-that-fits) | Medium | Memory budgeting |

## Observability, Tracing & Evals in Production

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Draw the Trace Tree](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/observability/draw-the-trace-tree) | Medium | Spans and parents |
| 2 | [Where Did the Time Go?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/observability/where-did-the-time-go) | Medium | Self time |
| 3 | [What Did This Request Cost?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/observability/what-did-this-request-cost) | Easy | Token roll-up |
| 4 | [Cost and Errors per Feature](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/observability/cost-and-errors-per-feature) | Easy | Dashboards |
| 5 | [Which Traces to Keep?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/observability/which-traces-to-keep) | Medium | Sampling |
| 6 | [Never Log Secrets](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/observability/never-log-secrets) | Medium | Redaction |
| 7 | [Parse the Judge's Verdict](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/observability/parse-the-judges-verdict) | Medium | LLM-as-judge plumbing |
| 8 | [Does the Judge Agree With Humans?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/observability/does-the-judge-agree-with-humans) | Medium | Cohen's kappa |
| 9 | [Pairwise Comparison Without Position Bias](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/observability/pairwise-comparison-without-position-bias) | Hard | A vs B |
| 10 | [Is the Answer Grounded?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/observability/is-the-answer-grounded) | Medium | Faithfulness |
| 11 | [Gate the Release on Regressions](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/observability/gate-the-release-on-regressions) | Medium | Regression tests for prompts |
| 12 | [Token F1 Against a Reference](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/observability/token-f1-against-a-reference) | Easy | Cheap automatic scoring |
| 13 | [Weighted Rubric Score](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/observability/weighted-rubric-score) | Easy | Structured grading |
| 14 | [Thumbs Up Rate per Prompt Version](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/observability/thumbs-up-rate-per-prompt-version) | Easy | Online feedback |
| 15 | [Alert When Quality Slips](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/observability/alert-when-quality-slips) | Medium | Monitoring a metric |
| 16 | [Build a Balanced Eval Set](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/observability/build-a-balanced-eval-set) | Medium | Stratified sampling |
| 17 | [Standard Attributes for an LLM Span](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/observability/standard-attributes-for-an-llm-span) | Easy | OpenTelemetry GenAI conventions |
| 18 | [Replay a Conversation From Events](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/observability/replay-a-conversation-from-events) | Easy | Debugging sessions |
| 19 | [Which Step Type Eats the Time?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/observability/which-step-type-eats-the-time) | Easy | Latency breakdown |
| 20 | [Flag Prompt-Injection Attempts](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/observability/flag-prompt-injection-attempts) | Medium | Security monitoring |

## Fine-Tuning in Practice: LoRA, QLoRA & DPO

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [How Small Is a LoRA Adapter?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/fine-tuning/how-small-is-a-lora-adapter) | Easy | Parameter counts |
| 2 | [Trainable Share of a Whole Model](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/fine-tuning/trainable-share-of-a-whole-model) | Medium | Choosing target modules |
| 3 | [The LoRA Forward Pass](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/fine-tuning/the-lora-forward-pass) | Medium | x W + (α/r) x A B |
| 4 | [Merge the Adapter for Serving](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/fine-tuning/merge-the-adapter-for-serving) | Medium | W' = W + (α/r)·A·B |
| 5 | [Why B Starts at Zero](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/fine-tuning/why-b-starts-at-zero) | Easy | Safe initialisation |
| 6 | [Will Training Fit on the GPU?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/fine-tuning/will-training-fit-on-the-gpu) | Medium | Full vs LoRA vs QLoRA memory |
| 7 | [Apply a Chat Template](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/fine-tuning/apply-a-chat-template) | Easy | Formatting training data |
| 8 | [Only Learn From the Assistant's Words](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/fine-tuning/only-learn-from-the-assistants-words) | Medium | Loss masking |
| 9 | [Pack Short Examples Together](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/fine-tuning/pack-short-examples-together) | Medium | Packing |
| 10 | [Clean the Training Set](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/fine-tuning/clean-the-training-set) | Medium | Data quality |
| 11 | [Warm-Up Then Cosine](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/fine-tuning/warm-up-then-cosine) | Easy | Learning-rate schedule |
| 12 | [Batch Size and Steps](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/fine-tuning/batch-size-and-steps) | Easy | Gradient accumulation |
| 13 | [The DPO Loss for One Pair](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/fine-tuning/the-dpo-loss-for-one-pair) | Medium | Preference tuning |
| 14 | [A Batch of Preference Pairs](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/fine-tuning/a-batch-of-preference-pairs) | Medium | DPO metrics |
| 15 | [Build Preference Pairs From Ratings](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/fine-tuning/build-preference-pairs-from-ratings) | Medium | Preference data |
| 16 | [Stop Before It Overfits](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/fine-tuning/stop-before-it-overfits) | Easy | Early stopping |
| 17 | [Did It Forget Everything Else?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/fine-tuning/did-it-forget-everything-else) | Easy | Catastrophic forgetting |
| 18 | [Prompt, RAG or Fine-Tune?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/fine-tuning/prompt-rag-or-fine-tune) | Medium | Choosing the technique |
| 19 | [What Does a Distillation Dataset Cost?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/fine-tuning/what-does-a-distillation-dataset-cost) | Easy | Synthetic data |
| 20 | [Choose the LoRA Rank](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/fine-tuning/choose-the-lora-rank) | Easy | Good enough, smallest |

## Multimodal AI: Images, Documents & Speech

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [What Does an Image Cost?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multimodal/what-does-an-image-cost) | Easy | Image tokens |
| 2 | [Resize Before Sending](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multimodal/resize-before-sending) | Easy | Keep the aspect ratio |
| 3 | [How Many Patches?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multimodal/how-many-patches) | Easy | Vision transformers |
| 4 | [Cut an Image Into Patch Vectors](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multimodal/cut-an-image-into-patch-vectors) | Medium | From pixels to tokens |
| 5 | [Normalise Pixels](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multimodal/normalise-pixels) | Easy | Model input preprocessing |
| 6 | [Build an Image Content Block](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multimodal/build-an-image-content-block) | Easy | Sending images to the API |
| 7 | [Slice Audio Into Frames](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multimodal/slice-audio-into-frames) | Easy | Speech features |
| 8 | [Chunk Long Audio for Transcription](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multimodal/chunk-long-audio-for-transcription) | Medium | Overlapping windows |
| 9 | [Word Error Rate](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multimodal/word-error-rate) | Medium | Scoring transcripts |
| 10 | [Write Subtitles](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multimodal/write-subtitles) | Easy | Timestamps |
| 11 | [Put OCR Words in Reading Order](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multimodal/put-ocr-words-in-reading-order) | Medium | Document layout |
| 12 | [Table Rows to Markdown](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multimodal/table-rows-to-markdown) | Easy | Giving tables to an LLM |
| 13 | [Validate Extracted Invoice Fields](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multimodal/validate-extracted-invoice-fields) | Medium | Don't trust extraction blindly |
| 14 | [Text or Image for Each Page?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multimodal/text-or-image-for-each-page) | Easy | Multimodal RAG routing |
| 15 | [Find Similar Images](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multimodal/find-similar-images) | Easy | Image embeddings |
| 16 | [Zero-Shot Labels, CLIP Style](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multimodal/zero-shot-labels-clip-style) | Medium | Images meet text |
| 17 | [A Voice Agent's Latency Budget](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multimodal/a-voice-agents-latency-budget) | Medium | Speech in, speech out |
| 18 | [How Many Video Frames to Send?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multimodal/how-many-video-frames-to-send) | Medium | Video as images |
| 19 | [Chunk a PDF and Keep Page Numbers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multimodal/chunk-a-pdf-and-keep-page-numbers) | Easy | Citable document chunks |
| 20 | [Detect the End of the User's Turn](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/multimodal/detect-the-end-of-the-users-turn) | Medium | Voice activity |

## Shipping AI Products: Streaming, Coding Agents & Guardrails

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Parse a Server-Sent Event Stream](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/shipping/parse-a-server-sent-event-stream) | Medium | SSE |
| 2 | [Assemble Streamed Text](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/shipping/assemble-streamed-text) | Easy | Text deltas |
| 3 | [Stream a Tool Call's Arguments](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/shipping/stream-a-tool-calls-arguments) | Medium | Partial JSON |
| 4 | [Measure Streaming Speed](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/shipping/measure-streaming-speed) | Easy | TTFT and tokens/s |
| 5 | [Rescue JSON From a Reply](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/shipping/rescue-json-from-a-reply) | Medium | Structured output |
| 6 | [What to Do About an API Error](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/shipping/what-to-do-about-an-api-error) | Easy | Retry policy |
| 7 | [A Safe Edit Tool](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/shipping/a-safe-edit-tool) | Medium | Unique string replacement |
| 8 | [Apply a Diff Hunk](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/shipping/apply-a-diff-hunk) | Medium | Patches |
| 9 | [The Test–Fix Loop](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/shipping/the-test-fix-loop) | Medium | How coding agents converge |
| 10 | [Which Shell Commands May the Agent Run?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/shipping/which-shell-commands-may-the-agent-run) | Medium | Sandboxing |
| 11 | [Scale a Computer-Use Click](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/shipping/scale-a-computer-use-click) | Easy | Screenshots vs screens |
| 12 | [A Semantic Cache](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/shipping/a-semantic-cache) | Medium | Don't pay twice for the same question |
| 13 | [A Daily Budget per User](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/shipping/a-daily-budget-per-user) | Easy | Cost guards |
| 14 | [Input Guardrail](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/shipping/input-guardrail) | Easy | Before the model |
| 15 | [Output Guardrail](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/shipping/output-guardrail) | Medium | After the model |
| 16 | [Save and Restore a Conversation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/shipping/save-and-restore-a-conversation) | Easy | Persistence |
| 17 | [Roll Out a New Prompt Version](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/shipping/roll-out-a-new-prompt-version) | Medium | Prompt versioning |
| 18 | [What Will This Feature Cost per Month?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/shipping/what-will-this-feature-cost-per-month) | Easy | Planning |
| 19 | [Ready to Launch?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/shipping/ready-to-launch) | Easy | Release checklist |
| 20 | [Send Chunks to the Browser](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/ai-engineering/#/q/shipping/send-chunks-to-the-browser) | Easy | Server-side streaming |

## Build

```bash
python3 handbook/build.py --book ai-engineering
```

Sources live in `ai-engineering/src/`: `topics/` (questions and solutions), `lessons/` and `theory/`.
