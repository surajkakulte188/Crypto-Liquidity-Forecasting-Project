# Crypto Liquidity Forecasting

## Project Overview
This project predicts cryptocurrency liquidity using historical trading data. It includes an end-to-end pipeline: data preprocessing, feature engineering, model training, evaluation, and deployment via a Flask web interface.

## Table of Contents
- [Project Overview](#project-overview)
- [Folder Structure](#folder-structure)
- [Config File](#config-file)
- [Pipeline Overview](#pipeline-overview)
- [UI Screenshots](#ui-screenshots)
- [How to Run](#how-to-run)
- [Notes](#notes)
- [References](#references)

## Folder Structure

```
crypto_liquidity_project/
├── data/
│   ├── raw/                          # CoinGecko CSVs (input)
│   └── processed/
│       ├── merged_coin_gecko.csv
│       └── engineered_features_lag.csv
├── notebooks/
│   ├── data_preparation.ipynb
│   ├── eda.ipynb
│   ├── feature_engineering.ipynb
│   ├── modeling.ipynb
│   └── evaluation_testing.ipynb
├── artifacts/
│   ├── models/
│   │   └── RidgeCV_logtarget.joblib  # best model (log-target)
│   └── metrics/
│       └── results.csv               # model comparison
├── templates/
│   └── index.html                    # Flask UI (minimal inputs)
├── static/
│   └── style.css                     # modern glass UI
├── app.py                            # Flask server (inference)
├── docs/
│   ├── HLD.md
│   ├── LLD.md
│   └── PIPELINE_ARCHITECTURE.md
└── reports/
    ├── EDA_REPORT.md
    └── FINAL_REPORT.md
```

## Config File
The project uses `config.py` for paths, feature columns, model parameters, and Flask settings.

**Usage Example:**
```python
from config import RAW_DATA_DIR, MODEL_DIR, XGBOOST_PARAMS
import pandas as pd
from xgboost import XGBRegressor

# Load data
data = pd.concat([pd.read_csv(RAW_DATA_DIR + f) for f in os.listdir(RAW_DATA_DIR)])

# Initialize XGBoost model
model = XGBRegressor(**XGBOOST_PARAMS)
```

## Pipeline Overview
1. Load raw CSVs → `src/data_loader.py`
2. Preprocess & label → `src/preprocessing.py`
3. Feature engineering → `src/feature_engineering.py`
4. Model training & selection → `src/modeling.py`
5. Evaluation & plots → `src/evaluation.py`
6. Export best model → `src/model_export.py`
7. Real-time inference → `app.py` (Flask)
8. Web UI → `templates/` & `static/`

```mermaid
flowchart LR
    A["Raw CSVs (data/raw)"] --> B["Preprocess & Merge\n(clean + label)"]
    B --> C["Feature Engineering\n(MAs, lags, returns, logs)"]
    C --> D["Modeling & Selection\n(log-target)"]
    D --> E["Export Best Model\n(artifacts/models)"]
    C --> F["Evaluation & Plots\n(artifacts/metrics)"]
    E --> G["Flask Inference (app.py)"]
    G --> H["Web UI\n(templates + static)"]
```
## Orchestration (sequence)
```mermaid
sequenceDiagram
  participant NB as Notebooks
  participant DS as data/processed
  participant AR as artifacts
  participant SV as Flask
  NB->>DS: merged_coin_gecko.csv
  NB->>DS: engineered_features_lag.csv
  NB->>AR: results.csv + RidgeCV_logtarget.joblib
  SV->>AR: Load model
  SV->>SV: Derive features → predict (expm1)
  SV-->>User: Liquidity ratio + label
```

## UI Screenshots
### Home Page
<img src="Web_Application_UI/1. Project_Homepage.png" alt="Home Page"/>

### Data Inserting Page
<img src="Web_Application_UI/2. Data_Uploading.png" alt="Data Uploading Page"/>

### Data Visualization Page
<img src="Web_Application_UI/3. EDA_Visualization.png" alt="Data Visualization Page"/>

### Prediction UI
<img src="Web_Application_UI/4. Prediction_Result.png" alt="Result Prediction"/>

### Final Output UI
<img src="Web_Application_UI/5. Final_Output.png" alt="Prediction Outcomes"/>

## How to Run
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Update `config.py` paths or model parameters if needed.
3. Train models via `src/modeling.py`.
4. Start Flask app:
```bash
python app.py
```
5. Access Web UI at `http://127.0.0.1:5000`

## ✅ Submission Checklist

- [ ] Source code (notebooks, `app.py`, templates, CSS, artifacts)
- [ ] EDA Report
- [ ] HLD & LLD
- [ ] Pipeline Architecture
- [ ] Final Report
- [ ] Best model (`artifacts/models/*.joblib`) + metrics CSV
- [ ] Processed data CSVs (`data/processed/*.csv`)

## Notes
- Keep sensitive credentials out of `config.py`; use `.env` if needed.
- All artifacts (models, metrics) are stored in `artifacts/`.
- Ensure all raw CSV files are placed in data/raw/.

## References
- scikit-learn, XGBoost, pandas, Flask documentation
- Project HLD, LLD, and EDA reports
