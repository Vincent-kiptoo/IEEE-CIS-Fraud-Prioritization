# Fraud Risk Scoring for Investigation Prioritization

## Cost-Constrained Decisioning on the IEEE-CIS Fraud Detection Benchmark

### Introduction

Transaction-level Kenyan mobile-money fraud data is not publicly available at sufficient granularity for reproducible machine-learning research. This project therefore uses the IEEE-CIS Fraud Detection dataset as a technical benchmark rather than as a representation of Kenyan mobile-money fraud.

The IEEE-CIS benchmark consists of anonymized online transaction data and associated identity information. The transaction and identity datasets are joined through `TransactionID`, while not all transactions have corresponding identity records. The dataset also contains temporal and anonymized behavioral features, including `TransactionDT`, which represents a timedelta from a reference point rather than an actual timestamp.

The fraud typology represented by IEEE-CIS is not assumed to be equivalent to M-Pesa fraud, SIM-swap fraud, account takeover, or other Kenyan payment-fraud typologies. Instead, the benchmark provides a controlled environment in which to develop transferable fraud-analytics capabilities: handling severe class imbalance, preventing temporal and feature leakage, modeling behavioral signals, ranking risk under limited investigation capacity, making economically informed decisions, and producing investigator-facing explanations.

The Kenyan context provides the business motivation. Safaricom reported that M-PESA processed approximately KSh 40.24 trillion in transaction value and 28.33 billion transactions during FY2024, illustrating the scale at which digital-payment risk management operates. This establishes why fraud-risk management is economically important; it does not imply that an IEEE-CIS-trained model would perform directly on M-Pesa data.

---

## Business Problem

Digital-payment platforms process large volumes of transactions in which fraudulent activity represents a minority of events but can create disproportionate financial and operational costs.

The problem addressed by this project is therefore not simply:

> **“Can we predict whether a transaction is fraudulent?”**

It is:

> **“Can we produce a ranked stream of transaction-risk scores that enables a fraud operations team to allocate limited investigation capacity toward transactions with the greatest expected economic value?”**

The system is designed around the reality that a fraud team cannot investigate every transaction. Risk scoring must therefore support prioritization rather than merely produce a binary fraud label.

---

## Stakeholders and Decision

### Primary stakeholder

**Fraud Operations Analyst**

The analyst investigates transactions prioritized by the risk-scoring system and may release, restrict, escalate, or otherwise handle a transaction according to organizational procedures.

### Operational stakeholder

**Fraud Operations Manager**

The manager owns investigation capacity and determines the volume of transactions that can realistically be reviewed.

### Decision supported by the model

The model supports the decision:

> **Which transactions should be investigated first when investigation capacity is limited?**

The system does **not** automatically block transactions and does not replace the final operational decision made by a human investigator or fraud operations team.

---

## Cost Asymmetry

Fraudulent and legitimate transactions do not have equal economic consequences.

For this project, transaction value will be used as a proxy for gross financial exposure rather than being treated as observed financial loss. Any transaction-value statistics used in the economic model will be calculated directly from the IEEE-CIS training data during the dataset-audit stage.

An illustrative investigation cost will also be modeled using an assumed investigator compensation range and an assumed average investigation duration. These values are **project assumptions rather than observed Kenyan industry costs**.

The economic framework will therefore explicitly distinguish:

* observed transaction values;
* assumed investigation costs;
* assumed fraud-prevention or recovery rates; and
* estimated economic outcomes.

The project will use sensitivity analysis rather than treating any single assumption as a known fact.

The central implication is that the economically relevant objective is not recall alone. A useful operating point depends jointly on fraudulent transaction value, investigation capacity, false-positive burden, investigation cost, and assumptions concerning prevented or recovered fraud losses.

---

## Project Objective

The primary objective is to develop an end-to-end fraud-risk scoring system that:

1. estimates transaction-level fraud risk;
2. uses only information that is available at or before the scoring decision;
3. incorporates temporal and behavioral information without introducing leakage;
4. ranks transactions for investigation;
5. operates under explicit investigation-capacity constraints; and
6. translates model scores into economically interpretable operational decisions.

---

## Research Question

> **How much can leakage-safe, point-in-time temporal and behavioral feature engineering improve fraud-risk prioritization compared with transaction-level features alone under chronological evaluation and limited investigation capacity?**

A secondary objective is to determine whether improvements in statistical discrimination translate into improvements in **fraud value captured per unit of investigation capacity**.

---

## Scope

### In scope

* Transaction-level fraud-risk scoring using the IEEE-CIS benchmark.
* Transaction attributes such as transaction amount and product information.
* Card, address, and email-domain information.
* Anonymized behavioral and temporal signals.
* Identity and device-related signals where available.
* Analysis of missing identity information.
* Point-in-time and leakage-safe feature engineering.
* Chronological validation and temporal generalization.
* Entity and behavioral aggregation where historical availability can be established.
* Class-imbalance analysis.
* Probability scoring and ranking.
* Capacity-constrained investigation prioritization.
* Cost and economic sensitivity analysis.
* Probability calibration.
* Investigator-facing explanations.

The underlying IEEE-CIS competition evaluates submissions using ROC-AUC, but this project will extend evaluation beyond the original competition objective toward operationally meaningful ranking and economic metrics.

### Stretch goals (not required for the core deliverable)

* API-based near-real-time scoring and empirical latency benchmarking.
* Monitoring concepts relevant to model and data drift.
* Cloud-based data infrastructure (BigQuery/GCP).

These represent a realistic *next step beyond* the core project, not part of what "done" means for this deliverable. They are listed here so the ambition is on record, not implied as default scope. Building them is a deliberate later decision, made explicitly, not something the project quietly grows into.

### Out of scope

* Automatic transaction blocking.
* Claims that the system detects Kenyan mobile-money fraud directly.
* Claims of production performance on M-Pesa or other Kenyan payment platforms.
* Account-takeover or SIM-swap detection as a separately defined problem.
* Chargeback processing or fraud-claims resolution.
* Combining IEEE-CIS data with private Kenyan transaction data.
* Treating the IEEE-CIS benchmark as geographically or operationally representative of Kenya.

---

## Technical Constraints

### 1. Temporal integrity

No feature may use information that would only become available after the transaction's scoring decision.

Historical aggregates, frequencies, entity statistics, and other behavioral features must be generated using only information available up to the relevant prediction time.

Potentially leakage-prone engineered features will be explicitly audited rather than automatically assumed to be safe.

### 2. Validation integrity

The primary evaluation framework will reflect future-like prediction rather than relying exclusively on random train/test splits.

Chronological validation will be used to evaluate:

* temporal generalization;
* feature stability;
* model degradation over time; and
* behavior on previously observed versus less familiar entities where such distinctions can be established.

### 3. Investigation-capacity constraint

The system will be evaluated across investigation-capacity scenarios, initially ranging from approximately:

```text
0.5% → 1% → 2% → 5%
```

of scored transactions.

These values are operating scenarios rather than claims about actual fraud-team capacity.

### 4. Latency

The target end-to-end scoring latency is:

> **<200 ms**

for the scoring path, including feature preparation and model inference.

Where explanations are generated synchronously, explanation generation will also be benchmarked as part of the request path.

Performance will be measured empirically using:

* P50 latency;
* P95 latency; and
* P99 latency.

No latency target will be considered achieved merely because it is theoretically plausible.

### 5. Explainability

TreeSHAP will be evaluated as a candidate explanation method for tree-based models because of its compatibility with tree ensembles.

However, technical attribution alone is insufficient. Explanations must be understandable to a fraud investigator and should ideally communicate meaningful behavioral concepts rather than only expose anonymized feature names.

Explainability quality will therefore be considered alongside computational cost and human readability.

---

## Evaluation Framework

Evaluation will be divided into three levels.

### 1. Model-level metrics

**Primary discrimination metric:**

* PR-AUC

**Secondary discrimination metric:**

* ROC-AUC

Additional analysis:

* precision;
* recall;
* F1 where useful for descriptive comparison;
* probability calibration;
* threshold sensitivity.

PR-AUC will be emphasized because fraudulent transactions constitute a minority of observations and precision-recall behavior is directly relevant to investigation workload.

### 2. Ranking-level metrics

Because the operational objective is investigation prioritization, models will also be evaluated at fixed investigation capacities.

Key metrics include:

* Precision@K;
* Recall@K;
* fraud value captured@K;
* fraud value captured per investigation;
* investigation volume;
* fraud value captured at 0.5%, 1%, 2%, and 5% review capacity.

This allows the model to be evaluated according to the question:

> **Given a fixed investigation budget, how much fraud value is concentrated into the transactions selected for review?**

### 3. Business-level metrics

The project will estimate:

* fraud value captured;
* investigation cost;
* scenario-based loss avoided;
* estimated net economic benefit.

A scenario-based economic model will be defined as:

> **Estimated net economic benefit = estimated loss avoided − investigation cost**

where estimated loss avoided depends on explicitly stated assumptions about fraud prevention or recovery.

Sensitivity analysis will be performed across plausible recovery/prevention assumptions rather than presenting a single assumed value as ground truth.

---

## Operating-Point Selection

The project will not use the default classification threshold of 0.5 as the operating decision rule.

Nor will the primary operating point be selected by maximizing F1-score.

Instead, the system will prioritize investigation according to model risk scores and evaluate operating points under explicit investigation-capacity constraints.

Threshold selection will therefore be treated as an operational decision derived from:

```text
fraud-risk score
        +
investigation capacity
        +
economic assumptions
        ↓
investigation queue
```

The selected operating configuration will be evaluated against the same chronological holdout used for final model assessment.

---

## Data and Leakage Principles

The IEEE-CIS dataset will be treated as a temporal behavioral dataset rather than simply as an independent collection of rows.

The project will explicitly investigate:

* repeated entities;
* historical transaction behavior;
* missing identity information;
* temporal patterns;
* feature availability;
* potential leakage from future observations;
* differences between familiar and less-familiar entities.

Any historical feature must satisfy the following principle:

> **At transaction time `t`, only information that would have been available by time `t` may be used to produce the feature.**

This principle will govern feature engineering, validation, offline experimentation, and the eventual API-scoring design.

---

## Intended System

The core deliverable demonstrates the following pipeline, ending at a decision-ready output rather than a served response:

```text
Raw IEEE-CIS Data
        ↓
Data Validation
        ↓
Transaction + Identity Integration
        ↓
Point-in-Time Feature Generation
        ↓
Fraud-Risk Model
        ↓
Calibrated Risk Score
        ↓
Capacity-Constrained Ranking
        ↓
Investigation Priority
        ↓
Human-Readable Explanation
```

*(Stretch goal: wrapping this pipeline in an API response for near-real-time serving — see Stretch Goals above.)*

The project therefore demonstrates not merely model training but the transition from:

> **raw transaction → behavioral representation → risk score → operational decision support**

---

## What This Project Demonstrates

This project does **not** claim to build a system that detects Kenyan fraud.

Instead, it demonstrates the engineering and analytical principles required to design a fraud-risk prioritization system:

* severe class-imbalance management;
* temporal validation;
* leakage prevention;
* point-in-time behavioral feature engineering;
* entity-aware analysis;
* cost and capacity asymmetry;
* economic decision analysis;
* probability calibration;
* investigator-facing explainability;
* latency-aware model serving; and
* production-oriented fraud-scoring architecture.

The IEEE-CIS dataset provides the experimental substrate. Kenya's digital-payment ecosystem provides the motivating business context.

The project's conclusions will therefore be limited to what can be supported by the IEEE-CIS benchmark and the stated assumptions. No performance result obtained from this project will be interpreted as direct evidence of performance on Kenyan mobile-money data without an appropriate Kenyan dataset and separate validation.

### Data-use note

The IEEE-CIS competition data is subject to Kaggle's competition rules, which restrict its use and redistribution. The dataset will therefore be kept locally and will not be redistributed through the project repository.