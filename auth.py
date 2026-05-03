from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from config import API_KEYS

_header = APIKeyHeader(name="X-API-Key", auto_error=True)


def require_api_key(key: str = Security(_header)) -> str:
    if key not in API_KEYS:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key")
    return key
