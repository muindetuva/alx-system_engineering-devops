# CI/CD Workflows for the Microservice Cluster

This project applies one GitHub Actions workflow to both services from the
Containerized Microservice Cluster. The flattened project root is
`auth-service`; `data-service/` contains the second independently deployable
service.

## Pipeline coverage

The shared `.github/workflows/ci.yml` independently **lints, tests, builds, and
deploys both auth-service and data-service**:

- `lint` and `test` validate auth-service in parallel.
- `build` depends on both auth checks, tags the Docker image with the immutable
  commit SHA, and publishes it to the auth-service GHCR path.
- `deploy` waits for the build and uses the protected `production` environment.
- `lint-data-service` and `test-data-service` validate data-service in parallel.
- `build-data-service` has its own two-job gate and publishes a separate
  data-service image.
- `deploy-data-service` uses the same manual production approval boundary.

This is Continuous Delivery: every passing change creates deployable artifacts,
but the GitHub `production` environment must be configured with required
reviewers before either deployment job can proceed.

See `PIPELINE_NOTES.md` for the design mapping and `BRANCH_PROTECTION.md` for
the required repository settings.
