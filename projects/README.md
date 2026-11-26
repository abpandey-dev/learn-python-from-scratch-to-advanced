# Industry Projects

Ten end-to-end projects that turn the courses into portfolio work, each modelled on a real job task. Every project has a business brief, realistic data, 6–8 milestones whose answers are **checked automatically**, hints, a hidden reference solution, how to present it, resume bullets and the interview questions you'll be asked about it.

**Web page:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/projects/

| # | Project | Role | Level | Hours | Skills | Open |
|---|---|---|---|---|---|---|
| 1 | [Retail Sales Analysis & Forecast](01_retail-sales-analysis.ipynb) | Data Analyst | Beginner–Intermediate | 6–8 | pandas, data cleaning, KPIs, SQL (sqlite3), Pareto analysis | [Colab](https://colab.research.google.com/github/abpandey-dev/learn-python-from-scratch-to-advanced/blob/main/projects/01_retail-sales-analysis.ipynb) |
| 2 | [Checkout Redesign: A/B Test Readout](02_checkout-ab-test.ipynb) | Product / Data Analyst | Intermediate | 5–7 | A/B testing, funnels, sample ratio mismatch, two-proportion z-test, confidence intervals | [Colab](https://colab.research.google.com/github/abpandey-dev/learn-python-from-scratch-to-advanced/blob/main/projects/02_checkout-ab-test.ipynb) |
| 3 | [Predict Churn for a Subscription App](03_subscription-churn.ipynb) | Data Scientist | Intermediate | 8–10 | EDA, train/test split, scikit-learn pipelines, logistic regression, gradient boosting | [Colab](https://colab.research.google.com/github/abpandey-dev/learn-python-from-scratch-to-advanced/blob/main/projects/03_subscription-churn.ipynb) |
| 4 | [Predictive Maintenance from Sensor Data](04_predictive-maintenance.ipynb) | ML Engineer | Intermediate–Advanced | 8–10 | time-series features, label engineering, leakage, time-based validation, random forests | [Colab](https://colab.research.google.com/github/abpandey-dev/learn-python-from-scratch-to-advanced/blob/main/projects/04_predictive-maintenance.ipynb) |
| 5 | ["You Might Also Like": A Store Recommender](05_store-recommender.ipynb) | ML Engineer | Intermediate | 7–9 | implicit feedback, leave-last-out evaluation, hit rate, item-item collaborative filtering, cosine similarity | [Colab](https://colab.research.google.com/github/abpandey-dev/learn-python-from-scratch-to-advanced/blob/main/projects/05_store-recommender.ipynb) |
| 6 | [Fair Credit-Risk Scoring](06_fair-credit-scoring.ipynb) | Data Scientist | Advanced | 8–10 | logistic regression, calibration, Brier score, approval policy, fairness metrics | [Colab](https://colab.research.google.com/github/abpandey-dev/learn-python-from-scratch-to-advanced/blob/main/projects/06_fair-credit-scoring.ipynb) |
| 7 | [Ship It: Serve and Monitor the Churn Model](07_ship-the-churn-model.ipynb) | MLOps / ML Engineer | Advanced | 8–10 | joblib, request validation, FastAPI, Docker, batch scoring | [Colab](https://colab.research.google.com/github/abpandey-dev/learn-python-from-scratch-to-advanced/blob/main/projects/07_ship-the-churn-model.ipynb) |
| 8 | [Customer-Support Assistant with RAG](08_support-rag-assistant.ipynb) | AI Engineer | Advanced | 8–10 | RAG, chunking, BM25, retrieval evaluation, hit@k / MRR | [Colab](https://colab.research.google.com/github/abpandey-dev/learn-python-from-scratch-to-advanced/blob/main/projects/08_support-rag-assistant.ipynb) |
| 9 | [Multi-Agent Support Analyst over an MCP Server](09_mcp-multi-agent-assistant.ipynb) | AI Engineer | Advanced | 8–10 | MCP, JSON-RPC, tool schemas, multi-agent orchestration, citations | [Colab](https://colab.research.google.com/github/abpandey-dev/learn-python-from-scratch-to-advanced/blob/main/projects/09_mcp-multi-agent-assistant.ipynb) |
| 10 | [Fine-Tune With LoRA: Adapt a Model to a New Domain](10_lora-fine-tuning.ipynb) | AI / ML Engineer | Advanced | 8–10 | LoRA, full vs parameter-efficient fine-tuning, gradient descent, data cleaning and leakage, catastrophic forgetting | [Colab](https://colab.research.google.com/github/abpandey-dev/learn-python-from-scratch-to-advanced/blob/main/projects/10_lora-fine-tuning.ipynb) |

## How to do a project

1. Open it in Colab (nothing to install) or run it locally with Jupyter.
2. Run the first cell, read the brief, then work milestone by milestone. Each ✅ check tells you when you're right.
3. Write the short report at the end in your own words, and publish the notebook on your GitHub.

Suggested order: projects 1–2 after **Python for Data Science**, 3–6 after **Machine Learning**, 7 after the **MLOps** topic, 8 after **Deep Learning & LLMs**, and 9–10 after **AI Engineering**.

## Rebuild

```bash
python3 projects/build_projects.py verify
```

The data is synthetic but realistic, generated with fixed seeds and saved in [data/](data/), so every learner gets the same numbers.
