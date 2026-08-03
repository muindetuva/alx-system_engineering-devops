"""Authentication boundary for the containerized service cluster."""

from datetime import datetime, timedelta, timezone

import jwt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from config import Settings


settings = Settings()
app = FastAPI(title="Authentication Service")

DEMO_USERNAME = "learner"
DEMO_PASSWORD = "container-ready"
ALGORITHM = "HS256"


class TokenRequest(BaseModel):
    """Describe demo credentials submitted for a token."""

    username: str
    password: str


@app.get("/health")
def health() -> dict[str, str]:
    """Return the authentication service's health status."""
    return {"status": "ok"}


@app.post("/token")
def issue_token(credentials: TokenRequest) -> dict[str, str]:
    """Issue a short-lived token for the hardcoded demonstration user."""
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
    """Return whether a supplied token was signed by this service."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[ALGORITHM],
        )
    except jwt.PyJWTError:
        return {"valid": False}
    return {"valid": True, "subject": payload.get("sub")}
