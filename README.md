![Python](https://img.shields.io/badge/python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-REST-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

# PIaaS — Trading Signal API for Developers

**Send a price series. Get a structured BUY / SELL / HOLD signal with confidence score, risk score, and explainable reasoning.**

PIaaS is a lightweight REST API that converts a price series into structured trading signals — no ML expertise or external data required.

Works with any price series — crypto, stocks, commodities, synthetic data.

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
  "expected_value": -0.01,
  "risk_score": 0.18,
  "signal_strength": 0.01,
  "reasoning_signals": [
    "positive momentum (+1.90%)",
    "price above MA5 (+0.55%)"
  ]
}
```

---

## How it works

```
prices[ ] → feature extraction → logistic regression → signal + reasoning
```

- Extracts **momentum**, **volatility**, and **moving-average** features from the last N prices
- Model trains once on first startup and is persisted to disk — subsequent starts are instant

---

## Why developers use this

- **Algorithmic trading bots** — call the API in a loop, no ML pipeline to build or maintain
- **Financial dashboards** — surface structured signals alongside raw price data
- **Strategy prototyping** — get a working signal endpoint in under 5 minutes

---

## Quickstart

```bash
git clone https://github.com/your-username/PIaaS
cd PIaaS
pip install -r requirements.txt
uvicorn main:app --reload
```

Default API key: `dev-key-1234` — no config needed to start.

---

## Python SDK

```python
from sdk.client import PIaaSClient

client = PIaaSClient("http://localhost:8000", api_key="dev-key-1234")
signal = client.predict([100, 101.5, 99.8, 102.3, 103.1, 101.9])

if signal["action"] == "BUY" and signal["confidence"] > 0.65:
    place_order(size=compute_position(signal["risk_score"]))
```

---

## Response fields

| Field | Type | Description |
|---|---|---|
| `action` | `BUY · SELL · HOLD` | Recommended decision |
| `confidence` | `0.0 – 1.0` | Model confidence in the prediction |
| `expected_value` | `float` | P(up) − P(down) |
| `risk_score` | `0.0 – 1.0` | Volatility-based risk estimate |
| `signal_strength` | `0.0 – 1.0` | Distance from neutral (0 = no signal, 1 = strong) |
| `reasoning_signals` | `list[str]` | Human-readable explanation of the decision |

---

## Why this is different

- `deterministic` — identical inputs always produce identical outputs — no stochastic inference
- `local-first` — zero network calls at inference time — runs entirely in your process
- `transparent` — logistic regression, not a black box — every signal is traceable to a feature
- `self-contained` — no third-party API key, no data broker, no external rate limit

---

## What this is not

- Not financial advice — outputs are developer signals, not investment recommendations
- Not a prediction guarantee — confidence scores reflect the model, not market certainty
- Not a managed service — designed to run in your own infrastructure

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
| `GET` | `/v1/health` | — | Server and model status |
| `POST` | `/v1/predict` | `X-API-Key` header | Get a trading signal from a price series |

Interactive docs: `http://localhost:8000/docs`

---

## License

MIT
