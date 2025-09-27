from flask import Flask, render_template, request
import joblib
import numpy as np
from pathlib import Path

app = Flask(__name__)

# --- Load trained (log-target) model ---
BASE = Path(__file__).resolve().parent
MODEL_PATH = BASE / "artifacts" / "models" / "RidgeCV_logtarget.joblib"   # change if you saved a different name
model = joblib.load(MODEL_PATH)

# Model feature order (must match training)
FEATURES = [
    "price","1h","24h","7d","24h_volume","mkt_cap",
    "price_ma_3","price_ma_5","vol_3d",
    "liquidity_ratio_lag1","price_lag1","24h_volume_lag1","mkt_cap_lag1",
    "price_ret_1d","vol_chg_1d","mcap_chg_1d",
    "log_price","log_vol","log_mcap"
]

def _f(x):
    try:
        return float(x)
    except:
        return None

def build_feature_row(form):
    """
    Build a 1x19 feature row from minimal inputs.
    We only ask for the core six; everything else is safely inferred or defaulted.
    """
    price = _f(form.get("price"))
    ch_1h = _f(form.get("h1"))
    ch_24h = _f(form.get("h24"))
    ch_7d = _f(form.get("d7"))
    vol_24h = _f(form.get("vol24h"))
    mcap = _f(form.get("mcap"))

    # Optional previous day inputs (for better lags)
    price_prev = _f(form.get("price_prev"))
    vol_prev = _f(form.get("vol24h_prev"))
    mcap_prev = _f(form.get("mcap_prev"))
    lr_prev = None

    # If user gave prev-day volume & mcap, compute prev-day liquidity ratio
    if vol_prev is not None and mcap_prev is not None and mcap_prev not in (0, None):
        lr_prev = vol_prev / mcap_prev
    else:
        # Or allow direct input if you want to expose it (kept hidden for now)
        lr_prev = _f(form.get("lr_prev"))

    # --- engineered approximations when history isn't given ---
    # price moving averages: fall back to current price
    price_ma_3 = price if price is not None else 0.0
    price_ma_5 = price if price is not None else 0.0

    # 3-day volatility unknown here → assume 0 (neutral)
    vol_3d = 0.0

    # Lag raw values
    price_lag1 = price_prev if price_prev is not None else 0.0
    vol_lag1 = vol_prev if vol_prev is not None else 0.0
    mcap_lag1 = mcap_prev if mcap_prev is not None else 0.0

    # Returns / changes (safe if previous provided, else 0)
    def safe_ret(curr, prev):
        if curr is None or prev in (None, 0):
            return 0.0
        return (curr - prev) / prev

    price_ret_1d = safe_ret(price, price_prev)
    vol_chg_1d   = safe_ret(vol_24h, vol_prev)
    mcap_chg_1d  = safe_ret(mcap, mcap_prev)

    # Log features
    def log1p_safe(v):
        if v is None or v < -1:
            return 0.0
        return float(np.log1p(v))
    log_price = log1p_safe(price if price is not None else 0.0)
    log_vol   = log1p_safe(vol_24h if vol_24h is not None else 0.0)
    log_mcap  = log1p_safe(mcap if mcap is not None else 0.0)

    # liquidity_ratio_lag1 default to 0 if unknown
    lr_lag1 = lr_prev if (lr_prev is not None and np.isfinite(lr_prev)) else 0.0

    row = [
        price or 0.0, ch_1h or 0.0, ch_24h or 0.0, ch_7d or 0.0, vol_24h or 0.0, mcap or 0.0,
        price_ma_3, price_ma_5, vol_3d,
        lr_lag1, price_lag1, vol_lag1, mcap_lag1,
        price_ret_1d, vol_chg_1d, mcap_chg_1d,
        log_price, log_vol, log_mcap
    ]
    return np.array([row])

def interpret_liquidity(lr):
    """
    Make a simple, human-friendly label from the predicted liquidity ratio.
    Thresholds can be tuned from your data distribution.
    """
    if lr < 0.02:
        label = "Very Low"
        color = "danger"
        tip = "Market liquidity appears thin—beware of slippage and price gaps."
    elif lr < 0.06:
        label = "Low"
        color = "warning"
        tip = "Liquidity is limited; moderate slippage likely on larger orders."
    elif lr < 0.15:
        label = "Moderate"
        color = "info"
        tip = "Liquidity is acceptable; typical spreads and execution."
    elif lr < 0.40:
        label = "High"
        color = "success"
        tip = "High activity vs market cap; orders likely to fill smoothly."
    else:
        label = "Very High"
        color = "success"
        tip = "Exceptional liquidity—tight spreads, fast execution."
    return label, color, tip

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", result=None)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        X = build_feature_row(request.form)
        # model trained on log1p(target)
        pred_log = model.predict(X)[0]
        pred = float(np.expm1(pred_log))
        label, color, tip = interpret_liquidity(pred)

        return render_template(
            "index.html",
            result={
                "pred": round(pred, 6),
                "label": label,
                "color": color,
                "tip": tip
            }
        )
    except Exception as e:
        return render_template("index.html", error=str(e), result=None)

if __name__ == "__main__":
    app.run(debug=True)
