"""Protected item API that delegates token verification to auth-service."""

import httpx
from fastapi import FastAPI, Header, HTTPException

from config import Settings


settings = Settings()
app = FastAPI(title="Data Service")

AUTH_VERIFY_URL = "http://auth:8000/verify"
ITEMS = [
    {"id": 1, "name": "Notebook"},
    {"id": 2, "name": "Mechanical keyboard"},
]


@app.get("/health")
def health() -> dict[str, str]:
    """Return the data service's health status."""
    return {"status": "ok"}


async def verify_with_auth_service(token: str) -> bool:
    """Verify a caller through the Compose-resolved auth service name."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            AUTH_VERIFY_URL,
            params={"token": token},
            timeout=5.0,
        )
    return response.status_code == 200 and response.json().get("valid", False)


@app.get("/items")
async def get_items(authorization: str = Header(default="")) -> list[dict]:
    """Return protected items after auth-service validates the bearer token."""
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=401, detail="Bearer token required")
    if not await verify_with_auth_service(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    return ITEMS
