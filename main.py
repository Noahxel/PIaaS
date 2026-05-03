from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, HTTPException, Request, Security
from pydantic import BaseModel, field_validator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from auth import require_api_key
from config import RATE_LIMIT
from signals import compute
from model import train, infer

_clf = None


def _key_from_api_key(request: Request) -> str:
    return request.headers.get("X-API-Key", request.client.host)


limiter = Limiter(key_func=_key_from_api_key)


class PredictRequest(BaseModel):
    prices: list[float]

    @field_validator("prices")
    @classmethod
    def check_length(cls, v: list[float]) -> list[float]:
        if len(v) < 6:
            raise ValueError("Need at least 6 price points")
        return v


router = APIRouter(prefix="/v1")


@router.get("/health")
def health():
    return {"status": "ok", "model": "ready" if _clf is not None else "not loaded"}


@router.post("/predict")
@limiter.limit(RATE_LIMIT)
def predict(request: Request, req: PredictRequest, _key: str = Security(require_api_key)):
    try:
        feat = compute(req.prices)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return infer(_clf, feat)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _clf
    print("Training model on mock data…")
    _clf = train()
    print("Model ready.")
    yield


app = FastAPI(title="PIaaS", version="1.0.0", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.include_router(router)
