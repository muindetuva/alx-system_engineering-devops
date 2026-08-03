# auth-service Elevated Login Failure Rate

## Incident Summary

On 18 July 2026 from 14:02 to 14:34 UTC, `auth-service` returned HTTP 500
responses from the `/token` endpoint for approximately 31% of login attempts.
Affected users could not sign in or refresh expired sessions, while requests
with still-valid tokens continued to work through `/verify`. The incident was
caused by a database connection leak introduced in commit `a3f9c21`, combined
with a missing failure-path integration test that allowed the defect to reach
production.

## Why This Warrants a Postmortem

This was a production outage with measurable user impact: nearly one third of
login attempts failed for 32 minutes, blocking access to dependent services.
Authentication is also security-sensitive infrastructure, so degraded behavior
at this boundary deserves careful review even though no data was lost and no
credentials were exposed. This was not a routine, already-triaged, low-impact
issue; it crossed the error-rate alert threshold, required an on-call response,
and required a rollback to restore service.

## Blameless Framing

This document focuses on the systems and process conditions that allowed the
incident, not on which individual wrote, reviewed, deployed, or responded to a
change. The engineers involved acted using the information, tests, and
deployment controls available to them at the time. The goal is to improve those
controls so the organization is less likely to repeat the incident.

## What This Document Produces

The rest of this document provides:

1. an evidence-anchored timeline reconstructed from deployment, Sentry,
   performance, alerting, and notification records;
2. a systemic root cause reached through the 5 whys; and
3. concrete, owned, and verifiable corrective and preventative action items.

## Timeline

- 14:02 UTC -- Deploy of commit `a3f9c21` completes for `auth-service`
  (CI/CD deployment record).
- 14:05 UTC -- Sentry captures the first `PoolTimeout` error from `/token`
  (Sentry issue `AUTH-431`).
- 14:07 UTC -- p95 response time for `/token` begins rising above the 240 ms
  baseline and active database connections begin climbing (Sentry performance
  tracing dashboard).
- 14:12 UTC -- `/token` reaches a 10% HTTP 500 error rate while `/health` still
  reports healthy (Sentry performance monitoring).
- 14:15 UTC -- The production error-rate alert fires after the five-minute
  threshold is breached (alerting system history).
- 14:18 UTC -- The on-call engineer acknowledged the alert and opened incident
  `INC-2026-0718` (notification and acknowledgment history).
- 14:23 UTC -- Sentry traces correlate failed requests with exhausted database
  connections introduced after commit `a3f9c21` (Sentry trace comparison and
  deployment tag).
- 14:27 UTC -- The on-call engineer starts redeploying the previous known-good
  image tagged with commit `7bd19ef` (CI/CD deployment record).
- 14:31 UTC -- Health-check-verified rolling restart completes on every worker
  (deployment health-check log).
- 14:34 UTC -- `/token` error rate, connection utilization, and p95 latency are
  confirmed back at baseline (Sentry and performance monitoring dashboards).

## Detection vs Onset

The true onset preceded detection. Sentry recorded the first error at 14:05 UTC
and performance monitoring showed response latency and open connections
deviating from baseline at 14:07 UTC, but the threshold alert did not fire until
14:15 UTC. A dashboard comparing connection utilization and p95 latency with
their normal baselines reveals this eight-minute detection gap before the
five-minute error-rate threshold was satisfied.

## Root Cause Analysis

Symptom: Users received HTTP 500 responses when requesting tokens from the
`auth-service` `/token` endpoint.

Why #1: Why did `/token` return HTTP 500 responses? -> Gunicorn workers timed
out while waiting for an available database connection.

Why #2: Why were no database connections available? -> An exception path in
the new token-audit write opened a connection but did not release it when the
write failed validation.

Why #3: Why did that exception path reach production? -> The integration suite
tested successful audit writes but had no test that repeatedly exercised the
validation-failure path and asserted that the connection returned to the pool.

Why #4: Why was the failure-path test absent? -> The service's pull-request
checklist required endpoint response tests but did not require resource-cleanup
assertions for new database access paths.

Why #5: Why did existing safeguards not catch the leak before user impact? ->
The health check verified only that configuration loaded, and monitoring had no
early alert for sustained connection-pool utilization.

The systemic root cause was a testing and review-process gap: changes that
acquired shared resources were not required to prove cleanup on both success
and failure paths. A monitoring gap delayed detection after that defect was
deployed.

## Why This Isn't a Surface-Level Fix

Restarting the service drained the exhausted connection pool and temporarily
stopped the errors, but it would not prevent recurrence. The same exception
path would leak connections again as soon as invalid audit events accumulated.
Likewise, asking an engineer to "be more careful" provides no automated,
repeatable protection. Preventing recurrence requires a code fix, a regression
test enforced by CI/CD, a stronger review checklist, and earlier monitoring.

## Corrective and Preventative Measures

- Category: Code fix. Wrap the token-audit database operation in a context
  manager that releases its connection on success and exception, and add an
  integration test that sends 200 invalid audit events while asserting stable
  pool utilization.
  Owner: @amina
  Tracking: `AUTH-512`. Due: 22 July 2026.
- Category: Monitoring gap. Add a warning alert when database connection-pool
  utilization remains above 70% for three minutes, with a critical page at 85%,
  and display the metric beside `/token` error rate and p95 latency.
  Owner: @kwame
  Tracking: `OBS-284`. Due: 24 July 2026.
- Category: Process improvement. Update the pull-request checklist so every new
  resource-acquisition path must include success-path and failure-path cleanup
  tests before merge.
  Owner: @zuri
  Tracking: `ENG-191`. Due: 26 July 2026.
- Category: Resilience improvement. Extend `/health` with a readiness check that
  verifies the application can briefly acquire and release a database
  connection without exposing credentials or query data.
  Owner: @tunde
  Tracking: `AUTH-517`. Due: 29 July 2026.

## Closing the Loop

The code-fix action begins in pull request `AUTH-512`, where the context-manager
change and connection-release regression test are reviewed together. The PR
triggers the CI/CD pipeline to run linting, unit tests, the new failure-path
integration test, and the full service test suite. After approval and merge,
CI/CD builds and publishes an image tagged with the merge commit SHA rather
than a mutable `latest` tag.

Deployment uses the existing health-check-verified rolling restart so each new
worker must become ready before the prior worker is removed. The deployment
record links the commit SHA, image digest, and test run to the incident action
item. After release, Sentry performance tracing and the new pool-utilization
alert are watched through one normal traffic peak and for seven days. The item
is closed only when Sentry shows no recurrence of `AUTH-431`, connection-pool
utilization remains at baseline, and `/token` error rate and p95 latency remain
within their service objectives.
