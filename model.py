import numpy as np
from sklearn.linear_model import LogisticRegression

from signals import Features, compute


def _generate_dataset(n: int = 2000, seed: int = 42) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    X, y = [], []
    for _ in range(n):
        # Random-walk price series of length 7
        prices = [100.0]
        for _ in range(6):
            prices.append(prices[-1] * (1 + rng.normal(0, 0.015)))
        feat = compute(prices)
        X.append([feat.ma_ratio, feat.momentum, feat.volatility])
        # Label: does price go up at step 7?
        next_price = prices[-1] * (1 + rng.normal(0, 0.015))
        y.append(1 if next_price > prices[-1] else 0)
    return np.array(X), np.array(y)


def train() -> LogisticRegression:
    X, y = _generate_dataset()
    clf = LogisticRegression(max_iter=200)
    clf.fit(X, y)
    return clf


def infer(clf: LogisticRegression, feat: Features) -> dict:
    X = np.array([[feat.ma_ratio, feat.momentum, feat.volatility]])
    prob_up = float(clf.predict_proba(X)[0][1])

    if prob_up >= 0.6:
        action = "BUY"
    elif prob_up <= 0.4:
        action = "SELL"
    else:
        action = "HOLD"

    confidence = round(max(prob_up, 1 - prob_up), 4)
    ev = round(prob_up - (1 - prob_up), 4)          # simplified: +1 if up, -1 if down
    risk = round(min(feat.volatility * 15, 1.0), 4)  # scale vol to 0–1
    signal_strength = round(abs(prob_up - 0.5) * 2, 4)

    signals = []
    if feat.momentum > 0.01:
        signals.append(f"positive momentum ({feat.momentum:+.2%})")
    elif feat.momentum < -0.01:
        signals.append(f"negative momentum ({feat.momentum:+.2%})")
    else:
        signals.append("flat momentum")

    if feat.ma_ratio > 0.005:
        signals.append(f"price above MA5 ({feat.ma_ratio:+.2%})")
    elif feat.ma_ratio < -0.005:
        signals.append(f"price below MA5 ({feat.ma_ratio:+.2%})")

    if feat.volatility < 0.008:
        signals.append("low volatility")
    elif feat.volatility > 0.02:
        signals.append("high volatility — elevated risk")

    return {
        "action": action,
        "confidence": confidence,
        "expected_value": ev,
        "risk_score": risk,
        "signal_strength": signal_strength,
        "time_horizon": "short",
        "reasoning_signals": signals,
    }
