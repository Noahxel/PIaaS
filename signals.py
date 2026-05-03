import numpy as np
from dataclasses import dataclass


@dataclass
class Features:
    ma_ratio: float    # (price - MA5) / MA5
    momentum: float    # (price[-1] - price[-6]) / price[-6]
    volatility: float  # std of last 5 returns


def compute(prices: list[float]) -> Features:
    if len(prices) < 6:
        raise ValueError("Need at least 6 prices")
    p = np.array(prices[-6:], dtype=float)
    returns = np.diff(p) / p[:-1]
    ma5 = p[:5].mean()
    return Features(
        ma_ratio=float((p[-1] - ma5) / ma5),
        momentum=float((p[-1] - p[0]) / p[0]),
        volatility=float(returns.std()),
    )
