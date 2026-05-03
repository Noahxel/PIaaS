import requests


class PIaaSClient:
    """Minimal Python client for the PIaaS prediction API."""

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self._session = requests.Session()
        self._session.headers.update({"X-API-Key": api_key})

    def health(self) -> dict:
        r = self._session.get(f"{self.base_url}/v1/health")
        r.raise_for_status()
        return r.json()

    def predict(self, prices: list[float]) -> dict:
        r = self._session.post(
            f"{self.base_url}/v1/predict",
            json={"prices": prices},
        )
        r.raise_for_status()
        return r.json()
