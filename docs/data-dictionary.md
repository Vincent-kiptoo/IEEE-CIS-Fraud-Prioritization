# IEEE-CIS Data Dictionary

## Purpose

This document records the working understanding of the IEEE-CIS Fraud Detection dataset.

It is a **living document**. Feature meanings, types, missingness patterns, and temporal availability will be verified during the dataset audit rather than assumed from third-party notebooks.

## Dataset Files

| File | Role |
|---|---|
| `train_transaction.csv` | Training transaction-level observations with `isFraud` |
| `train_identity.csv` | Identity/device-related information for some training transactions |
| `test_transaction.csv` | Test transaction-level observations without the target |
| `test_identity.csv` | Identity/device-related information for some test transactions |
| `sample_submission.csv` | Required prediction-submission structure |

## Unit of Observation

The primary unit of observation is a **transaction**.

The transaction table uses:

```text
TransactionID
```

as the transaction identifier.

The identity tables also contain `TransactionID`, allowing transaction-level enrichment through a join.

## Target

### `isFraud`

Binary target:

```text
0 = legitimate transaction
1 = fraudulent transaction
```

The target is available only in the training transaction data.

## Major Feature Groups

The IEEE-CIS dataset contains anonymized and semi-anonymized feature groups. Exact business meanings are not fully disclosed.

### Transaction Features

Examples:

- `TransactionID`
- `TransactionDT`
- `TransactionAmt`
- `ProductCD`

These describe transaction identity, relative time, monetary value, and product/category context.

### Card Features

Examples:

- `card1`
- `card2`
- `card3`
- `card4`
- `card5`
- `card6`

These are anonymized card-related attributes.

### Address Features

Examples:

- `addr1`
- `addr2`

These represent anonymized address-related signals.

### Distance Features

Examples:

- `dist1`
- `dist2`

These represent anonymized distance-related signals.

Their exact underlying definitions are not assumed.

### C Features

```text
C1 ... C14
```

These are anonymized counting/relationship-style features supplied by the dataset.

Their exact business definitions are not known and must not be over-interpreted.

### D Features

```text
D1 ... D15
```

These are anonymized temporal/delta-style features.

Because temporal availability matters to this project, their behavior must be investigated carefully for leakage and stability.

### M Features

```text
M1 ... M9
```

These are anonymized match/comparison indicators.

### V Features

```text
V1 ... V339
```

These are anonymized Vesta-derived features.

The project will investigate redundancy, missingness, stability, and usefulness rather than assuming every V feature is independently meaningful.

### Email Features

Examples:

- `P_emaildomain`
- `R_emaildomain`

These contain anonymized purchaser/recipient email-domain information.

### Identity Features

The identity table contains features such as:

```text
id_01 ... id_38
DeviceType
DeviceInfo
```

These provide additional device/identity-related signals where identity information exists.

## Temporal Variable

### `TransactionDT`

`TransactionDT` is a relative timedelta rather than an absolute calendar timestamp.

For this project it is important because it gives us a temporal ordering for:

- chronological validation;
- temporal feature engineering;
- drift analysis;
- point-in-time historical aggregates.

Derived calendar-like features may be explored, but their interpretation must respect the fact that the original reference date is not directly supplied.

## Missingness

Missing values are expected throughout the IEEE-CIS dataset, especially in the identity data.

Missingness must not automatically be treated as an error.

We will investigate:

- missingness by feature group;
- missingness over time;
- missingness conditional on fraud;
- missingness conditional on entity familiarity;
- whether missingness itself contains predictive signal.

## Join Relationship

The intended enrichment relationship is:

```text
train_transaction
        |
        | TransactionID
        |
        v
train_identity
```

and similarly for the test data.

The identity table does not contain a row for every transaction. Therefore the expected join type for the enriched transaction dataset is a **left join from transactions to identity information**.

## Feature Availability Rule

For any feature used in the production-oriented pipeline:

> At scoring time `t`, the feature must only use information that would have been available at or before `t`.

This applies particularly to:

- historical counts;
- entity aggregates;
- fraud rates;
- rolling windows;
- frequency encodings;
- target encodings;
- entity-level behavioral statistics.

## Planned Audit Fields

The dataset audit will establish, from the local data:

- exact row counts;
- exact column counts;
- inferred DuckDB types;
- null counts;
- unique counts;
- target prevalence;
- temporal range;
- fraud prevalence over time;
- transaction amount distribution;
- identity coverage;
- cardinality of key categorical variables.

## Important Caution

Anonymous feature names do not justify strong semantic claims.