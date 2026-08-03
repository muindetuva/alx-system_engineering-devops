# Auth Service Pipeline Plan

## Manual Failure Mode

I once prepared a service image after changing token validation but forgot to
run the negative authentication tests. The image built successfully even
though malformed tokens were accepted. An automated **test** stage would have
caught that concrete regression before any deployable image was produced.

## CI vs CD vs CD

**Continuous Integration** runs linting and tests whenever auth-service code is
pushed or proposed in a pull request, giving rapid feedback while changes are
small. **Continuous Delivery** additionally builds and publishes a verified
image but keeps production release behind a deliberate approval. **Continuous
Deployment** would release every passing change automatically. This project
targets **Continuous Delivery**, not automatic Continuous Deployment.

## Pipeline Stages for auth-service

- **Lint:** install `requirements.txt` under Python 3.12 and run
  `ruff check .` against the flattened auth-service source and tests.
- **Test:** install the same dependencies and run pytest with line-by-line
  coverage reporting for `POST /token` and `GET /verify`.
- **Build:** after lint and test pass, build `Dockerfile`, tag the auth-service
  image with the exact Git commit SHA, authenticate with `GITHUB_TOKEN`, and
  push the immutable image to GitHub Container Registry.
- **Deploy:** after the image is published, pause at the protected `production`
  environment for manual approval before triggering release.
