![Python](https://img.shields.io/badge/python-3.10+-blue)
![API](https://img.shields.io/badge/API-REST-green)
# PIaaS (Prediction Infrastructure as a Service)

**Turn any price series into structured decision signals via a simple API.**
Prices → Features → Model → Decision

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
  "expected_value": -0.01,
  "risk_score": 0.18,
  "signal_strength": 0.01,
  "time_horizon": "short",
  "reasoning_signals": ["positive momentum (+1.90%)", "price above MA5 (+0.55%)"]
}
```

No ML setup. No external data source. Running in under a minute.

---

## Run it

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Default API key: `dev-key-1234` — no config needed to start.

---

## Use case

You have a price series (crypto, stock, any asset). You want to know: **buy, sell, or hold?**

PIaaS computes momentum, volatility, and moving-average signals, then returns a structured decision with a confidence score and human-readable reasoning. No ML expertise required — just send prices, get a signal.

---

## Python SDK

```python
from sdk.client import PIaaSClient

client = PIaaSClient("http://localhost:8000", api_key="dev-key-1234")

signal = client.predict([100, 101.5, 99.8, 102.3, 103.1, 101.9])
# → {"action": "HOLD", "confidence": 0.51, ...}
```

---

## Configuration

```bash
cp .env.example .env
```

| Variable | Default | Description |
|---|---|---|
| `API_KEYS` | `dev-key-1234` | Comma-separated valid API keys |
| `RATE_LIMIT` | `60/minute` | Per-key rate limit |

---

## API reference

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/v1/health` | — | Server status |
| `POST` | `/v1/predict` | `X-API-Key` header | Get a signal |

Full interactive docs at `http://localhost:8000/docs`.
