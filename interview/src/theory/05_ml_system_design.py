from lib import *

THEORY("Questions you should be ready for", """
<table><tr><th>Prompt</th><th>Key ideas to bring up</th></tr>
<tr><td>Video or product recommendations</td><td>two-stage funnel, cold start, feedback loops</td></tr>
<tr><td>Search ranking</td><td>query understanding, learning to rank, nDCG, position bias</td></tr>
<tr><td>Fraud or abuse</td><td>imbalance, delayed labels, adversaries, costs</td></tr>
<tr><td>Ad click prediction</td><td>calibration, huge categorical features, online learning</td></tr>
<tr><td>Content moderation</td><td>human review, precision and recall per severity, appeals</td></tr>
<tr><td>Forecasting demand</td><td>time splits, seasonality, baselines, hierarchy</td></tr>
<tr><td>RAG chatbot</td><td>retrieval evaluation, faithfulness, prompt injection, cost</td></tr>
<tr><td>Agent</td><td>tools, permissions, step limits, evals</td></tr></table>
""")
FAQ("Should you always use ML?", "<p>No. Start by asking whether rules or a simple heuristic would do. ML adds data, monitoring and maintenance costs, so it should earn its place.</p>")
FAQ("Why start with a baseline?", "<p>It gives a number to beat, reveals data problems early, and sometimes it's good enough. Without one, you can't say what complexity is buying.</p>")
FAQ("Offline metric improved but online metric fell. Why?", "<p>Possible causes: training-serving skew, a metric that doesn't reflect the goal, leakage in offline evaluation, feedback loops, or latency hurting users. Investigate before trusting either.</p>")
FAQ("What is data drift vs concept drift?", "<p>Data drift means inputs change. Concept drift means the relationship between inputs and the label changes, as when fraudsters adapt. Concept drift needs labels to detect directly.</p>")
FAQ("What is training-serving skew?", "<p>A feature is computed differently in training and production. Share the feature logic, log features at serving time, and compare the same rows from both paths.</p>")
FAQ("How do you handle class imbalance?", "<p>Use metrics like PR-AUC, adjust class weights or the threshold, and possibly downsample negatives, correcting probabilities afterward.</p>")
FAQ("How do you handle cold start?", "<p>Use content features and popularity for new items and users, ask for preferences, and reserve exploration traffic.</p>")
FAQ("How do you serve a model with low latency?", "<p>Use a smaller or quantised model, pre-compute features and results, cache, batch requests, and use a two-stage cascade so the heavy model scores only a few items.</p>")
FAQ("What is a feature store?", "<p>A shared system that defines features once and serves them consistently for training and online use, including point-in-time correct values.</p>")
FAQ("How do you know it's time to retrain?", "<p>Monitor quality, drift and age. Retrain on a schedule or on triggers, and promote the new model only after it beats the current one.</p>")
FAQ("Fine-tune or RAG for an LLM product?", "<p>Use RAG for facts that change. Consider fine-tuning for stable style or format needs once prompts have been tried, with an eval to prove the gain.</p>")
FAQ("How would you evaluate an LLM feature?", "<p>A set of real examples with automatic checks, an LLM or human rubric for open-ended output, adversarial cases, and online metrics after launch.</p>")
FAQ("What's the biggest risk in your design?", "<p>Always have an answer. Name a realistic failure, how you'd detect it, and what you'd do. This shows the judgement that interviewers look for.</p>")
