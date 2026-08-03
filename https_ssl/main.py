"""Demonstrate secure-cookie handling behind an HTTPS reverse proxy."""

from typing import Dict

from fastapi import FastAPI, Request, Response


app = FastAPI(title="HTTPS-aware auth-service")


@app.get("/health")
def health() -> Dict[str, str]:
    """Return a small liveness response."""
    return {"status": "healthy"}


@app.post("/session")
def create_session(request: Request, response: Response) -> Dict[str, bool]:
    """Set the session cookie securely when the original request was HTTPS."""
    is_secure = request.headers.get("x-forwarded-proto") == "https"

    if is_secure:
        response.set_cookie(
            key="session",
            value="example-session-token",
            secure=True,
            httponly=True,
            samesite="lax",
        )
    else:
        response.set_cookie(
            key="session",
            value="example-session-token",
            secure=False,
            httponly=True,
            samesite="lax",
        )

    return {"secure": is_secure}
