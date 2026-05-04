# PIaaS — Time Series Signal API

**Turn a price series into structured decision signals.**

PIaaS is a lightweight REST API that converts numeric time-series data into:
- BUY / SELL / HOLD decisions
- confidence score
- risk estimate
- optional explanatory signals

No external data required. Runs locally in seconds.

---

## Example

```bash
curl -X POST http://localhost:8000/v1/predict \
  -H "X-API-Key: dev-key-1234" \
  -H "Content-Type: application/json" \
  -d '{"prices": [100, 101.5, 99.8, 102.3, 103.1, 101.9]}'
```

```json
{
  "action": "HOLD",
  "confidence": 0.51,
  "risk_score": 0.18,
  "signals": [
    "momentum positive",
    "price above short-term average"
  ]
}
```

---

## What it does

PIaaS extracts simple features from price series:
- momentum
- volatility
- moving averages

Then produces a structured signal:

- **action** → BUY / SELL / HOLD  
- **confidence** → model certainty  
- **risk_score** → estimated volatility  
- **signals** → optional explainability layer  

---

## Why this exists

When building trading bots, dashboards, or simulations, you often need:

> a simple decision signal from raw time-series data

Instead of building a full ML pipeline, PIaaS provides a lightweight API that returns structured outputs instantly.

Works with:
- crypto prices
- stock data
- any numeric time series

---

## Trust & Design Principles

Model is deterministic for identical inputs.

No external data required. Runs locally.

```
prices → feature extraction → model → signal
```

---

## Typical use cases

- prototyping trading strategies  
- signal generation for dashboards  
- ML experimentation on time series data  

---

## Quickstart

```bash
git clone https://github.com/your-username/PIaaS
cd PIaaS
pip install -r requirements.txt
uvicorn main:app --reload
```

Default API key: `dev-key-1234`

Model is trained once on first run and persisted locally for instant startup next time.

---

## Python SDK

```python
from sdk.client import PIaaSClient

client = PIaaSClient("http://localhost:8000", api_key="dev-key-1234")

signal = client.predict([100, 101.5, 99.8, 102.3, 103.1, 101.9])

if signal["action"] == "BUY" and signal["confidence"] > 0.65:
    print("execute trade")
```

---

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/health` | Service status |
| POST | `/v1/predict` | Generate signal from price series |

Interactive docs: http://localhost:8000/docs

---

## Configuration

```bash
API_KEYS=dev-key-1234
RATE_LIMIT=60/minute
```

---

## Roadmap

- model persistence ✔  
- input validation ✔  
- API improvements (next)  

---

## License

MIT