# Methodology

## 1. Project Method

The project follows:

```text
Problem
   ↓
Hypothesis
   ↓
Data Audit
   ↓
Feature Design
   ↓
Validation
   ↓
Modeling
   ↓
Error Analysis
   ↓
Economic Evaluation
   ↓
Decision Policy
   ↓
Deployment Prototype
```

Each stage produces evidence used to inform the next.

## 2. Data Source

The project uses the IEEE-CIS Fraud Detection benchmark.

Primary files:

- `train_transaction.csv`
- `train_identity.csv`
- `test_transaction.csv`
- `test_identity.csv`

The sample submission file is used only when submission-format verification is required.

The raw data is not committed to version control.

## 3. Data Access Architecture

During local research, DuckDB is used to query the raw CSV files directly.

The notebook layer uses SQL through JupySQL where practical.

Conceptually:

```text
Raw CSV
   ↓
DuckDB view
   ↓
SQL analysis
   ↓
Python analysis / feature engineering
```

This avoids unnecessary conversion of the full dataset into memory during the initial audit.

**Stretch goal, not core:** Google BigQuery is a candidate for a later, optional cloud-oriented extension of the project, not part of the core data-access plan. MySQL and DuckDB carry the entire core deliverable.

## 4. Data Integration

Transaction data is the base observation table.

Identity information is joined by:

```text
TransactionID
```

The default enrichment operation is a left join from transactions to identity records because not all transactions have corresponding identity rows.

The project will explicitly analyze the effect of missing identity information.

## 5. Unit of Prediction

The prediction unit is:

> one transaction

The initial target is:

```text
isFraud
```

with binary labels:

```text
0 = legitimate
1 = fraudulent
```

## 6. Temporal Ordering

`TransactionDT` provides relative temporal ordering.

Chronological evaluation will preserve that ordering.

Derived temporal features must not introduce future information.

Where rolling or historical features are created, they must use only observations available before the current transaction.

## 7. Point-in-Time Feature Engineering

A feature is considered point-in-time valid when its value can be reconstructed using only information available at scoring time.

For example:

```text
For transaction t:

historical_count(t)
=
number of qualifying events before t
```

not:

```text
number of qualifying events across the complete dataset
```

This distinction is central to the project.

### Read-before-update principle

For online-style historical features:

```text
1. Read prior state
2. Generate feature
3. Score transaction
4. Update historical state
```

The current transaction must not influence the feature used to score itself.

## 8. Validation Strategy

### Exploratory validation

Random splits may be used temporarily for debugging and baseline comparisons.

They are not the primary estimate of production-like generalization.

### Primary validation

Chronological holdouts will be the main evaluation framework.

Conceptually:

```text
Earlier period
    ↓
Training

Later period
    ↓
Validation

Latest period
    ↓
Final holdout
```

The exact boundaries will be established during the dataset audit.

### Additional validation

Where feasible, entity-aware evaluation will be used to examine performance on:

- repeated/familiar entities;
- less-familiar entities;
- entities with limited history.

## 9. Class Imbalance

The fraud class is substantially smaller than the legitimate class.

The project will not optimize for accuracy.

Primary discrimination metric:

```text
PR-AUC
```

Secondary:

```text
ROC-AUC
```

Operational metrics will be evaluated at fixed investigation capacities.

Class handling methods may include:

- class weights;
- careful sampling where justified;
- model-specific imbalance controls.

Any resampling must preserve temporal validity.

## 10. Feature Development

Feature engineering will proceed incrementally.

### Layer 1 — Raw transaction features

Examples:

- transaction amount;
- product information;
- card attributes;
- address attributes;
- email-domain information.

### Layer 2 — Temporal features

Examples:

- relative time;
- historical intervals;
- recent activity.

### Layer 3 — Entity behavior

Examples:

- prior transaction frequency;
- historical amount statistics;
- recent transaction counts;
- deviation from historical behavior.

### Layer 4 — Identity/device behavior

Examples:

- device reuse;
- identity coverage;
- historical device-related patterns.

### Layer 5 — Missingness and novelty

Examples:

- missing identity indicators;
- unseen values;
- historical familiarity.

Each layer should be evaluated through ablation rather than added indiscriminately.

## 11. Modeling

Candidate model progression:

```text
Logistic Regression
      ↓
LightGBM / XGBoost
      ↓
CatBoost
      ↓
Optional advanced models
```

The purpose of the progression is to establish increasingly expressive baselines while preserving interpretability of experimental improvements.

## 12. Ranking and Decisioning

The model produces:

```text
P(fraud | transaction)
```

The score is used to rank transactions.

Investigation capacity then determines how many transactions enter the review queue.

Example:

```text
100,000 scored transactions
capacity = 1%
        ↓
top 1,000 transactions by fraud-risk score
        ↓
investigation queue
```

The project therefore separates:

```text
prediction
```

from:

```text
operational decision
```

## 13. Economic Model

Transaction value is treated as a proxy for gross exposure.

It is not automatically treated as realized fraud loss.

A scenario-based framework will estimate:

```text
estimated_loss_avoided
=
fraud_value_captured × assumed_prevention_or_recovery_rate
```

and:

```text
net_economic_benefit
=
estimated_loss_avoided − investigation_cost
```

These values are scenario estimates.

Sensitivity analysis must be reported for the recovery/prevention assumptions and investigation-cost assumptions.

## 14. Calibration

Because operating decisions may depend on risk probabilities, calibration will be evaluated.

Candidate techniques:

- Platt scaling;
- isotonic regression.

Calibration must be performed using data separate from the final holdout and under a temporally valid procedure.

## 15. Explainability

TreeSHAP is the initial candidate for tree-based model explanations.

However, we will distinguish between:

1. mathematically faithful explanations; and
2. explanations that are useful to human investigators.

Where anonymized feature names reduce interpretability, we will investigate feature-group or concept-level summaries.

## 16. Error Analysis

Error analysis will be performed on:

- false positives;
- false negatives;
- high-value false negatives;
- high-score legitimate transactions;
- low-score fraudulent transactions;
- familiar entities;
- less-familiar entities;
- transactions with and without identity information.

The aim is to understand failure modes rather than simply count errors.

## 17. Latency

The target scoring latency is:

```text
< 200 ms
```

Measurements:

- P50;
- P95;
- P99.

The benchmark will distinguish:

- feature preparation;
- model inference;
- explanation generation;
- total request latency.

## 18. Reproducibility

Every major experiment should record:

- dataset version/location;
- feature version;
- code version;
- validation period;
- random seed where applicable;
- model parameters;
- evaluation metrics.

Raw competition data is excluded from Git.

## 19. Deployment Philosophy (Stretch Goal — Conceptual)

This section describes a conceptual target architecture for a possible future extension. It is not part of the core deliverable, and its absence does not mean the project is incomplete. The core deliverable ends at a calibrated, explainable, economically-evaluated risk score — see [Intended System](project-statement.md#intended-system).

The final prototype, if this extension is pursued, should represent a realistic path:

```text
Incoming transaction
       ↓
Feature state lookup
       ↓
Point-in-time feature generation
       ↓
Model inference
       ↓
Risk score
       ↓
Investigation prioritization
       ↓
Explanation
       ↓
API response
```

The prototype is intended to demonstrate production-oriented engineering principles, not to claim readiness for deployment in a Kenyan financial institution.

## 20. Scientific Boundaries

The project must not:

- claim that IEEE-CIS represents Kenyan mobile-money fraud;
- infer production performance from benchmark AUC alone;
- use post-event information in historical features;
- report assumed economic parameters as observed facts;
- select a model solely because it has the highest leaderboard score.

All conclusions must be bounded by the dataset, validation design, and assumptions used.
