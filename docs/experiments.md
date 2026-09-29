# Experiments

## Purpose

This document records the experiments conducted during the project.

Each experiment should answer a specific question and should be reproducible from the repository.

The purpose is not to collect model scores. The purpose is to build evidence for or against engineering and modeling decisions.

## Experiment Record Template

Every substantive experiment should record:

```text
Experiment ID
Date
Question
Hypothesis
Dataset / split
Feature set
Model
Hyperparameters
Validation strategy
Metrics
Result
Interpretation
Decision
Reproducibility notes
```

## Experiment Naming

Use:

```text
EXP-001
EXP-002
EXP-003
...
```

Keep experiment IDs stable even when the code changes.

## Phase 0 — Dataset Audit

### EXP-001 — Dataset Structure

**Question:** What are the exact sizes and schemas of the transaction and identity datasets?

**Status:** Pending

Metrics / outputs:

- row counts;
- column counts;
- inferred data types;
- primary identifiers;
- target column;
- identity coverage.

---

### EXP-002 — Fraud Prevalence

**Question:** What proportion of training transactions are fraudulent?

**Status:** Pending

Outputs:

- total transactions;
- fraudulent transactions;
- legitimate transactions;
- fraud rate.

---

### EXP-003 — Fraud Over Time

**Question:** How does fraud prevalence and volume change across the temporal ordering represented by `TransactionDT`?

**Status:** Pending

Outputs:

- fraud counts by time period;
- fraud rate by time period;
- transaction volume by time period;
- candidate temporal split boundaries.

---

### EXP-004 — Missingness Analysis

**Question:** Is missingness concentrated in particular feature groups, time periods, or fraud classes?

**Status:** Pending

Outputs:

- null percentage by feature;
- null percentage by feature group;
- missingness over time;
- fraud rate conditional on selected missingness patterns.

---

### EXP-005 — Identity Coverage

**Question:** How much transaction coverage is provided by `train_identity`, and does identity availability vary over time?

**Status:** Pending

Outputs:

- proportion of transactions with identity records;
- identity coverage over time;
- fraud rate with vs. without identity records.

---

## Phase 1 — Baselines

### EXP-006 — Minimal Transaction Baseline

**Question:** How well can a simple model perform using only a deliberately small set of transaction-level features?

**Hypothesis:** A simple baseline will establish a lower bound against which engineered features can be evaluated.

Candidate metrics:

- PR-AUC;
- ROC-AUC;
- Precision@K;
- Recall@K.

---

### EXP-007 — Random vs. Chronological Validation

**Question:** How different are model estimates under random splitting and chronological splitting?

**Hypothesis:** Random validation may produce an optimistic estimate relative to future-like chronological evaluation.

**Status:** Planned

---

## Phase 2 — Feature Engineering

### EXP-008 — Temporal Features

Test derived temporal features based on `TransactionDT`.

Possible features:

- relative day;
- relative hour;
- time-of-period;
- elapsed time between transactions where valid.

The feature-generation method must not use future information.

---

### EXP-009 — Frequency Features

Test point-in-time frequency features for candidate entities and categorical signals.

Examples:

- prior transaction count;
- prior occurrence count;
- recent activity count.

The baseline implementation must use read-before-update logic.

---

### EXP-010 — Behavioral Aggregates

Test historical behavioral features such as:

- prior average transaction amount;
- amount deviation from historical behavior;
- transaction frequency;
- recent activity;
- historical diversity.

---

## Phase 3 — Model Comparison

Candidate models:

- Logistic Regression baseline;
- LightGBM;
- XGBoost;
- CatBoost.

The comparison must use the same validation design and feature availability assumptions.

Primary comparison metric:

- PR-AUC.

Secondary and operational metrics:

- ROC-AUC;
- Precision@K;
- Recall@K;
- fraud value captured@K;
- calibration.

---

## Phase 4 — Capacity-Constrained Evaluation

Evaluate model rankings under:

```text
0.5%
1%
2%
5%
```

investigation capacity scenarios.

For each capacity, calculate:

- number of investigations;
- legitimate reviews;
- fraudulent transactions selected;
- fraud value captured;
- fraud value captured per investigation;
- estimated investigation cost;
- scenario-based economic benefit.

---

## Phase 5 — Calibration

Compare:

- uncalibrated probabilities;
- calibrated probabilities.

Candidate methods:

- Platt scaling;
- isotonic regression.

Calibration evaluation should use appropriate chronological validation and should avoid fitting calibration on the final test period.

---

## Phase 6 — Explainability

Investigate:

- TreeSHAP;
- feature-group summaries;
- investigator-oriented reason codes.

The goal is to determine whether model explanations remain useful after anonymized feature names and feature interactions are considered.

---

## Phase 7 — Serving and Latency (Stretch Goal)

This phase is optional and out of the core experiment sequence (Phases 0–6). It only applies if the API-serving stretch goal in `project-statement.md` is pursued. The core project's final comparison and write-up do not depend on it.

Benchmark the final candidate pipeline under realistic request conditions.

Record:

- P50;
- P95;
- P99 latency;
- cold-start behavior where applicable;
- feature lookup time;
- model inference time;
- explanation time.

Target:

```text
< 200 ms
```

The target is measured, not assumed.

---

## Experiment Discipline

Do not change multiple important dimensions without recording them.

For example, if PR-AUC changes, we should be able to tell whether the change came from:

- validation strategy;
- feature engineering;
- model family;
- class handling;
- hyperparameters;
- calibration;
- thresholding.

No experiment should be reported using a metric without recording the corresponding data split and feature-generation rules.

---

## Final Comparison

The final model comparison should not be a single leaderboard table.

It should include:

1. discrimination;
2. ranking performance;
3. economic implications;
4. calibration;
5. latency;
6. stability across time;
7. explainability;
8. implementation complexity.

A model with the highest AUC is not automatically selected.
