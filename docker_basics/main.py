"""Minimal FastAPI application used by the Docker exercises."""
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def root():
    """Return a greeting from the containerized service."""
    return {"message": "Hello from Docker!"}


@app.get("/health")
def health():
    """Return a simple container health signal."""
    return {"status": "healthy"}
