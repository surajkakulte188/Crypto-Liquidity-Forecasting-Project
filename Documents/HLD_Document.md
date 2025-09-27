# High-Level Design (HLD) — Cryptocurrency Liquidity Prediction System

## Document version
- Project: Cryptocurrency Liquidity Prediction for Market Stability
- Prepared for: Suraj R Kakulte
- Date: September 27, 2025
- Version: 1.0

## 1. Purpose & Scope
**Purpose:**
This High-Level Design (HLD) describes the architecture, components, data flows, technology choices, non-functional requirements, and operational considerations for the Cryptocurrency Liquidity Prediction system. The system predicts short-to-medium term liquidity levels for selected cryptocurrencies to help traders and exchanges detect and respond to liquidity stress.

**Scope:**
- Ingest historical and live crypto market data (price, volume, market cap).
- Preprocess and engineer liquidity-related features.
- Train and serve machine learning models that forecast liquidity levels (numeric and categorical: High/Medium/Low).
- Provide a simple web UI (Flask or Streamlit) for upload, visualization, and prediction.
- Provide documentation, reproducible scripts, and optional Docker deployment.

## 2. High-level goals & success metrics
**Goals:**
- Provide interpretable liquidity forecasts that flag potential liquidity crises.
- Maintain a reproducible pipeline from raw data → model → prediction.
- Deliver a lightweight web interface to run predictions and visualize results.

**Success metrics:**
- Model performance: RMSE, MAE, R² (target R² ≥ 0.7 on holdout / scaled data depending on baseline).
- Prediction latency: < 1 second for single-instance inference (model loaded in memory).
- Reproducibility: Full pipeline runnable with requirements.txt and scripts or Docker.
- Usability: UI allows data upload, model run, and visualizations with no errors for typical CSV formats.

## 3. System Overview (Logical components)
**1. Data Layer:**
- Raw data storage (CSV files or small DB).
- Processed data storage (engineered CSVs).

**2. Ingestion Layer:**
- Scripts to fetch historical exports (CoinGecko/other) and optionally live API fetchers.

**3. Preprocessing & Feature Engineering:**
- Cleaning, missing value handling, timestamp alignment, scaling.
- Feature creation: rolling means, volatility (std of returns), liquidity ratio (volume/market_cap), lag features, transaction-frequency proxies, sentiment score (optional).

**4. Modeling Layer:**
- Training scripts and notebooks for candidate models (RandomForest, XGBoost, LightGBM, LSTM).
- Hyperparameter tuning modules.

**5. Evaluation & Validation:**
- Cross-validation and time-series-aware splits, performance reporting, calibration.

**6. Deployment / Serving:**
- Lightweight web app (Flask or Streamlit) that loads a serialized model and returns predictions + plots.
- Optionally Dockerized service for reproducible deployment.

**7. Visualization & Reporting:**
- EDA visualizations, diagnostic plots, and final report export.
**8. Monitoring & Logging:**
- Basic logging for app usage and model predictions; local logs for training runs; model versioning.

## 4. Component-level responsibilities
**4.1 Data Collector:**
Input: CSVs from CoinGecko / exported historical files.
Responsibilities:
- Normalize column names and timestamps.
- Save raw copies (for auditability) in /data/raw/.

**4.2 Preprocessor:**
Input: raw CSVs.
Responsibilities:
- Handle missing values (interpolate / forward-fill / drop as required).
- Convert timestamps to common timezone (UTC).
- Remove duplicates and erroneous rows.
- Save processed dataset to /data/processed/.

**4.3 Feature Engineer:**
Input: processed dataset.
Responsibilities:
- Create rolling features: 7-day, 14-day, 30-day moving averages for volume & price.
- Volatility: rolling std of returns.
- Liquidity ratio: volume / market_cap (or normalized variant).
- Lag features: previous-day, previous-3, previous-7 values.
- Encode categorical variables and scale numerical features (MinMax or Standard).
- Output files: engineered_features.csv, engineered_features_lag.csv.

**4.4 Model Trainer:**
Input: engineered features.
Responsibilities:
- Split data with time-series aware splitting (no future leakage).
- Train candidate models (RF, XGBoost, LSTM).
- Save best model artifact as model.pkl or a TensorFlow SavedModel.
- Save training logs, hyperparameters, metrics.

**4.5 Model Evaluator:**
Input: trained models and holdout/test splits.
Responsibilities:
- Compute RMSE, MAE, R² and confusion matrix if class labels used (High/Medium/Low).
- Generate evaluation plots: predicted vs actual, residuals over time.

**4.6 API / UI:**
Input: user CSV or tickers for live fetch.
Responsibilities:
- Accept input, run preprocessing & feature generation for input, call model, return prediction.
- Display time-series plots, forecast, and a summary (confidence, risk flag).
- Provide downloadable results and screenshots.

**4.7 Storage & Config:**
- Config file: configs/config.yaml for paths, model names, feature lists.
- Use requirements.txt or environment.yml for reproducibility.

## 5. Data Flow Diagram

```mermaid
flowchart LR
    A["Raw CSVs (data/raw)"] --> B["Preprocess & Merge<br>(clean + label)"]
    B --> C["Feature Engineering<br>(MAs, lags, returns, logs)"]
    C --> D["Modeling & Selection<br>(log-target)"]
    D --> E["Export Best Model<br>(artifacts/models)"]
    C --> F["Evaluation & Plots<br>(artifacts/metrics)"]
    E --> G["Flask Inference (app.py)"]
    G --> H["Web UI<br>(templates + static)"]

## 6. Technology Stack (recommended)
Language: Python 3.9+
Data: pandas, numpy
Modeling: scikit-learn, xgboost, lightgbm, tensorflow/keras (optional LSTM)
EDA/Visuals: matplotlib, seaborn, plotly (optional interactive)
Web UI: Streamlit (recommended for speed) or Flask + HTML/CSS/Jinja2
Serialization: joblib / pickle for sklearn models; tf.saved_model for TF.
Config & Logging: yaml, python logging
Reproducibility: requirements.txt, or environment.yml, optionally Dockerfile
Version Control / Repo: GitHub (include README + docs)

## 7. Non-functional requirements
- Performance: Inference latency < 1s for single prediction.
- Scalability: Local deployment for portfolio; dockerization for cloud.
- Reliability: Save model and data artifacts with timestamps and checksums.
- Security: No PII; secure storage of any API keys (not in repo; use env vars).
- Usability: Simple UI with upload, run, and visualization options

## 8. Deployment & Delivery options
**Local / Portfolio (quick):**
Use Streamlit: easier to deploy on Streamlit Cloud or Hugging Face Spaces. Provide streamlit_app.py, requirements.txt.

**Containerized deployment (professional):**
Dockerfile: base python image, install requirements.txt, expose port, run app. Host on Render/Heroku/AWS Elastic Beanstalk.

## 9. Testing & validation plan
- Unit tests: small tests for data preprocessing functions (missing handling, scaling).
- Integration tests: run preprocessing → feature engineering → single prediction end-to-end.
- Model tests: check model prediction range, avoid NaNs.
- UI tests: sanity checks for upload and display flows.

## 10. Monitoring & maintenance
- Errors & exceptions: capture stack traces, notify via email (manual) or log files.
- Model drift checks: periodically retrain (monthly or when new data available) and compare performance.
- Reproducibility: keep training notebooks and seed values documented.
