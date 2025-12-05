AutoSAGE

AI platform that transforms raw data into diagnosis, modeling, explainability, and actionable recommendations — fully automated, integrated, and production-ready.

🚀 Overview

AutoSAGE automates the full pipeline:

connect → ingest → diagnose → audit → explore → model → explain → recommend → expose via API

Created for companies that need clarity, speed, and data-driven decision-making — with or without a specialized team.

💰 Investor Pitch

(kept — only enriched to match architectural evolution)

AutoSAGE exists because 80% of data science work is wasted cleaning, diagnosing, and explaining data — not modeling.

No leading platform solves this gap with:

transparency

explainability

auditability

end-to-end autonomy

With its new modular architecture (DCP → EDA → ML → ORC), AutoSAGE has evolved into a scientific automation platform, not just AutoML.

✨ Key Features
🔌 Connectivity & Ingestion

Native connector for Postgres

Direct reading of any table (schema.table)

Automatic schema and type detection

Secure loading via secrets

Support for DataFrame, CSV, and SQL (roadmap)

New (v2025): DCP architecture with fully automated ingestion

📥 Intelligent Ingestion

Column standardization

Automatic target detection

Robust date and encoding conversion

Initial schema validation

Pipeline orchestrated through the DCP → EDA modules

🩺 Data Diagnosis & Quality

Missing values

Outliers (Z-score, IQR, robust stats)

Cardinality and structure

Structural drift

Descriptive statistics and distributions

🔬 Auto-EDA

Correlations (Pearson, Spearman, Cramér’s V)

Hypothesis tests (t-test, ANOVA, χ²)

Pre-modeling insights

Detection of weak variables

Automatic visualizations

Export is now 100% PARQUET (new official standard)

🤖 Automatic Model Selection

Classification: Logistic, SVM, Random Forest, Gradient Boosting

Regression: Linear, Ridge, Random Forest, XGBoost

Selection based on bias–variance, stability, and interpretability

Integrated with a new ML module fully isolated and versioned

🏋️ Training

Stratified train/test split

Automatic normalization and encoding

Cross-validation

Simple hyperparameter search

Reproducible pipeline

Current architecture executes the entire training inside the ML container autonomously

📊 Metrics & Comparisons

Classification → AUC, F1, Precision, Recall

Regression → RMSE, MAE, R², MAPE

Mandatory baseline comparison

Automatically generated full HTML reports

🔎 Explainability

Feature importance

SHAP values

Model behavior analysis

Bias detection

📦 Export & Registry

Automatic saving of the best model (/models/)

Exported artifacts:

Model

Metrics

Feature importance

Logs

PARQUET files

Internal versioning via execution hash

Unified registry shared between modules via Docker volumes

📡 Inference API (implemented)

FastAPI in src/app/main.py

/predict endpoint

Automatic validation with Pydantic

Model loading from registry

Response includes prediction + explainability

Structured logging per request

📈 Monitoring & Logs

Logs persisted under /logs/

Execution IDs

Drift warnings

Full pipeline audit trail

Trace ID propagated across all modules (ORC → DCP → EDA → ML)

🆕 🔧 DCP Connector Module

The DCP (Data Connector Pipeline) is the new AutoSAGE layer that connects to external databases and ingests tables automatically, without relying on manual uploads.

What has been implemented

Fully functional Postgres connector

Direct ingestion of the customer_churn table from the dcp database

Secure credential loading via Secrets Manager

Internal configuration registry

Structured and standardized logs

/ingest endpoint to trigger data collection

Automatic pipeline DCP → EDA → ML

Manual upload removed by strategic decision

Ready for expansion

MySQL

SQL Server

BigQuery

S3

External REST APIs

Philosophy

Plug-and-play connectors

Orchestrated and safe execution

Architecture designed for enterprise environments

🆕 Modular Architecture 2025

ORC (Orchestrator): controls and guarantees the entire data flow

DCP: collects and standardizes

EDA: diagnoses, audits, and prepares artifacts

ML: models, evaluates, and generates reports

All connected by versioned registry + distributed trace ID

🔬 Scientific Methodology

(kept exactly as original — only updated where necessary)

1️⃣ Ingestion & Standardization

Automatic typing

Column normalization

Date conversion and validation

Standardized pipeline inside the DCP module

2️⃣ Statistical Diagnosis

Distributions and densities

Descriptive statistics

Cardinality

Artifacts now exported as PARQUET

3️⃣ Quality Audit

Missing values

Outliers

Semantic inconsistencies

Structural drift

4️⃣ Relationships & Statistical Signal

Correlations

Hypothesis tests

Preliminary feature importance

5️⃣ Intelligent Model Selection

Based on target and variable structure

6️⃣ Reproducible Training

Stratified splits

Automatic encoding and scaling

Cross-validation

Execution isolated inside the ML module

7️⃣ Transparent Metrics

Complete classification and regression metrics

8️⃣ Explainability

SHAP

Feature importance

Bias detection

9️⃣ Actionable Recommendations

Suggested next steps

Recommended interventions

Risks and limitations

⚔️ Strategic Comparison

(kept — unchanged structurally)

🎯 Target Market

(unchanged)

💵 Monetization

(unchanged)

🧠 Strategic Advantages

(unchanged — now strengthened by the new modular core)

🌎 Vision

If data exists, clarity should exist.
And clarity should be automatic.

We are building the universal interpretation layer between data and decision — now with a distributed, scalable, production-ready architecture.

📊 Documentation

(unchanged)

🛡️ License

MIT

💡 Contact

🔗 LinkedIn — https://www.linkedin.com/in/sergiofonsecasilva

📩 sergiofs.u1tec@gmail.com

📞 +55 11 9 3767-8996