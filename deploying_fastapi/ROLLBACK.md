# Rollback Strategy for auth-service

## Redeploying a Known-Good Image

The CI/CD pipeline publishes each successful image as
`ghcr.io/example/auth-service:<commit-sha>`. Keep the currently deployed SHA in
the release record. If a new deployment is bad, select the previous known-good
SHA, pull that immutable tag, update the deployment reference, and perform the
same health-checked rolling reload. No image rebuild is required because the
exact tested artifact already exists in `ghcr.io`.

## Revert and Redeploy

Alternatively, create a Git revert of the bad commit, review and push that new
commit, and let the normal CI/CD pipeline run tests, build a fresh image, push
its new SHA tag, and deploy it. This preserves a clear repository history and
is appropriate when the fix must become the new forward-moving baseline.

## Which One and When

Redeploying a known-good image is faster during an incident because it skips
checkout, dependency installation, testing, image construction, and registry
upload. Use it first to restore service within minutes. Follow with a revert
and normal redeploy when the repository must reflect the rollback permanently
and there is time to run the full tested pipeline.
