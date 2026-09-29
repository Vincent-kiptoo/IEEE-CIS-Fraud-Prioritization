# Fraud Risk Scoring for Investigation Prioritization
### Cost-Constrained Decisioning on the IEEE-CIS Fraud Detection Benchmark

> An end-to-end fraud-analytics project on temporal/behavioral feature engineering, leakage-safe validation, severe class imbalance, capacity-constrained prioritization, economic decision-making, and investigator-facing explainability using IEEE-CIS as a research benchmark, with Kenya's digital-payment ecosystem as the motivating context.

Full scope, assumptions, and methodology: [`docs/project-statement.md`](docs/project-statement.md)

---

## Status

| Phase | Description | Status |
|---|---|---|
| 0 | Problem framing | Done |
| 1 | Dataset audit & environment setup | In progress |
| 2 | Hypothesis-driven EDA | Not started |
| 3 | Point-in-time feature engineering | Not started |
| 4 | Baseline → tree-ensemble modeling | Not started |
| 5 | Threshold optimization & economic evaluation | Not started |
| 6 | Explainability & error analysis | Not started |
| 7 | Write-up | Not started |

**Phase 1 so far:** competition access, local dataset download, virtual environment, DuckDB + JupySQL setup, initial views over the raw CSVs. No model trained yet.

---

## The Problem

Digital-payment platforms process high transaction volumes where fraud is a small but costly minority, and fraud teams operate under finite investigation capacity. A useful system needs to do more than output a binary label — it needs to produce a **ranked stream of transaction risk scores** that lets investigators focus limited capacity on transactions with the greatest expected economic value.

```
Transaction → Point-in-Time Features → Fraud-Risk Model → Calibrated Score
   → Investigation Ranking → Capacity Constraint → Human Investigation
```

The model prioritizes. It does not block transactions automatically.

## Research Question

> How much does leakage-safe, point-in-time temporal and behavioral feature engineering improve fraud-risk prioritization over transaction-level features alone, under chronological evaluation and limited investigation capacity?

Secondary question: do gains in statistical discrimination (PR-AUC) actually translate into more fraud value captured per unit of investigation capacity — the metric that matters to the business?

## Why IEEE-CIS

Kenyan mobile-money fraud data isn't publicly available at the transaction level. IEEE-CIS provides a real-world-shaped benchmark genuine class imbalance (~3.5% fraud), temporal structure, missing identity records, anonymized behavioral feature for developing transferable fraud-analytics skills, without claiming its data represents Kenyan payment fraud. See [Limitations](#important-limitations).

[Competition page](https://www.kaggle.com/competitions/ieee-fraud-detection) · [Data](https://www.kaggle.com/competitions/ieee-fraud-detection/data)

## Core Principles

1. **Point-in-time correctness** — features use only information available at or before scoring time.
2. **Temporal validation** — chronological train/validation/test split, not random.
3. **Behavioral modeling** — frequency, amount behavior, entity reuse, device/identity signals, missingness patterns.
4. **Capacity-constrained prioritization** — evaluated at multiple investigation-capacity levels (0.5%–5%), not just the default 0.5 threshold.
5. **Human-in-the-loop** — the model informs a decision; it doesn't make one.
6. **Economic evaluation** — fraud value captured, investigation cost, and net economic benefit, all with explicit, sensitivity-tested assumptions — never presented as observed Kenyan industry data.

## Evaluation

| Level | Metrics |
|---|---|
| **Model** | PR-AUC (primary), ROC-AUC, precision, recall, calibration |
| **Ranking** (at fixed capacity) | Precision@K, Recall@K, fraud value captured@K, at 0.5%/1%/2%/5% review capacity |
| **Business** | Fraud value captured, investigation cost, estimated loss avoided, net economic benefit |

PR-AUC and ROC-AUC are model diagnostics, not business outcomes the threshold that ships is the one maximizing net economic benefit under the capacity constraint.

## Technical Constraints

- **No leakage:** no post-transaction information in features; leakage-prone aggregates audited explicitly.
- **Latency target:** <200ms end-to-end (feature prep + inference), benchmarked at P50/P95/P99 — measured, not assumed. This is a design target for the conceptual architecture, not a deployed SLA (see Stretch Goals).
- **Explainability:** TreeSHAP for tree-based models, aimed at investigator-legible output, not raw feature-contribution math.

## Tech Stack (Core)

**Data & analytics:** Python, MySQL, DuckDB (fast local querying during EDA), SQL, pandas, NumPy
**Modeling:** scikit-learn, LightGBM / XGBoost
**Explainability:** SHAP (TreeExplainer)

## Stretch Goals (not required for the core deliverable)

Serving the model behind an API (FastAPI), containerizing it (Docker), and moving the pipeline to a cloud analytical warehouse (BigQuery/GCP) are realistic *next steps beyond this project*, not part of the core scope. Listed here so the ambition isn't lost, but building them is a deliberate later decision, not a default — the core deliverable is the modeling and decision-analysis work above.

## Repository Structure

```
├── docs/
│   ├── project-statement.md       # full Phase 0 framing, assumptions, sensitivity analysis
│   ├── data-dictionary.md
│   ├── methodology.md
│   └── experiments.md
├── notebooks/
│   ├── 01_dataset_audit.ipynb
│   ├── 02_temporal_analysis.ipynb
│   ├── 03_missingness_analysis.ipynb
│   └── 04_baseline.ipynb
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   └── evaluation/
├── tests/
├── configs/
├── reports/
├── requirements.txt
└── README.md
```

*(`src/` grows as reusable logic moves out of notebooks — don't scaffold folders you're not populating this week.)*

## Research Workflow

```
Problem → Hypothesis → Data Audit → Assumptions → Feature Design
   → Temporal Validation → Model → Error Analysis
   → Economic Evaluation → Decision Policy
```

Notebooks are for exploration; reusable logic moves into tested modules under `src/`.

## Important Limitations

This project does **not** claim:
- IEEE-CIS represents Kenyan mobile-money fraud, or that results transfer to M-Pesa
- transaction value equals actual financial loss
- the assumed recovery/investigation-cost figures reflect observed industry data
- higher AUC implies better business outcomes

Every economic result is reported with its assumptions and sensitivity range.

## Data Use

IEEE-CIS data is subject to [Kaggle's competition rules](https://www.kaggle.com/competitions/ieee-fraud-detection/rules) and is kept out of version control — not redistributed through this repo.
