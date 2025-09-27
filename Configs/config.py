# config.py - Configuration file for Crypto Liquidity Forecasting Project

# Paths
RAW_DATA_DIR = "data/raw/"
MODEL_DIR = "artifacts/models/"
METRICS_DIR = "artifacts/metrics/"
TEMPLATES_DIR = "templates/"
STATIC_DIR = "static/"

# File names
MODEL_FILENAME = "best_model.pkl"
METRICS_FILENAME = "metrics.json"

# Data processing settings
TARGET_COLUMN = "log_target"  # target variable
DATE_COLUMN = "timestamp"
FEATURE_COLUMNS = ["price", "volume", "moving_avg_5", "moving_avg_10", "lag_1", "lag_2", "returns"]

# Feature engineering
MA_WINDOWS = [5, 10, 20]       # moving average windows
LAG_FEATURES = [1, 2, 3]       # lag periods
LOG_TRANSFORM_COLS = ["price", "volume"]

# Model parameters
RANDOM_FOREST_PARAMS = {
    "n_estimators": 100,
    "max_depth": 8,
    "random_state": 42
}

XGBOOST_PARAMS = {
    "n_estimators": 200,
    "max_depth": 6,
    "learning_rate": 0.1,
    "random_state": 42
}

LINEAR_REG_PARAMS = {
    "fit_intercept": True
}

# Training settings
TRAIN_TEST_SPLIT_RATIO = 0.8
RANDOM_STATE = 42

# Flask settings
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
DEBUG_MODE = True
