import os

from dotenv import load_dotenv

load_dotenv()

API_KEYS: set[str] = set(os.getenv("API_KEYS", "dev-key-1234").split(","))
RATE_LIMIT: str = os.getenv("RATE_LIMIT", "60/minute")
