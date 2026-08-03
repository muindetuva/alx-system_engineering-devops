"""Authentication service with production monitoring instrumentation."""

from datetime import datetime, timedelta, timezone

import jwt
import sentry_sdk
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from config import settings


sentry_sdk.init(
    dsn=settings.sentry_dsn,
    environment=settings.environment,
    traces_sample_rate=0.1,
)

app = FastAPI(title="Authentication Service")

DEMO_USERNAME = "learner"
DEMO_PASSWORD = "container-ready"
ALGORITHM = "HS256"


class TokenRequest(BaseModel):
    """Describe demo credentials submitted for a token."""

    username: str
    password: str


@app.middleware("http")
async def add_sentry_context(request: Request, call_next):
    """Attach non-sensitive request metadata before handling a request."""
    sentry_sdk.set_context(
        "request_body",
        {
            "path": request.url.path,
            "query_params": dict(request.query_params),
        },
    )
    return await call_next(request)


# Also polled every few minutes by an external uptime monitor.
@app.get("/health")
def health_check() -> dict[str, str]:
    """Return healthy only after required configuration has loaded."""
    jwt_secret_key = settings.jwt_secret_key
    if not jwt_secret_key:
        return {"status": "unhealthy"}
    return {"status": "ok"}


@app.post("/token")
def issue_token(credentials: TokenRequest) -> dict[str, str]:
    """Issue a short-lived token for the demonstration user."""
    sentry_sdk.set_user({"id": credentials.username})
    if (
        credentials.username != DEMO_USERNAME
        or credentials.password != DEMO_PASSWORD
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)
    token = jwt.encode(
        {"sub": credentials.username, "exp": expires_at},
        settings.jwt_secret_key,
        algorithm=ALGORITHM,
    )
    return {"access_token": token, "token_type": "bearer"}


@app.get("/verify")
def verify_token(token: str) -> dict[str, object]:
    """Return whether a token was signed by this service."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[ALGORITHM],
        )
    except jwt.PyJWTError:
        return {"valid": False}
    return {"valid": True, "subject": payload.get("sub")}
