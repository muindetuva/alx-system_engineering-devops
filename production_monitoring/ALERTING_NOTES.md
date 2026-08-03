# Alerting Rules and Baselines

## Alert Rule

**WHEN** a new Sentry issue is created or the same issue exceeds 10 events in 5
minutes

**AND** the event belongs to `auth-service`, has level `error` or higher, and is
tagged with the `production` environment

**THEN** notify the on-call channel immediately with the issue link, release
commit, affected endpoint, event count, and first-seen time.

Warnings and informational events remain searchable but do not page the team.

## Establishing a Baseline

Before choosing the event threshold, observe at least two representative weeks
of `auth-service` traffic. Record its typical error rate by endpoint and error
type; p50, p95, and p99 response times; and request volume by hour of day and day
of week. Separate normal weekday peaks, quiet overnight periods, deploy windows,
and known batch traffic. Then set warning and critical thresholds relative to
these measured patterns and validate them against prior incidents.

## Why a Threshold Without a Baseline Is a Guess

Without a baseline, the team cannot distinguish an anomaly from normal variation.
A threshold below normal peaks creates constant false alarms and teaches the
team to ignore pages. A threshold far above normal behavior misses real problems
until users are already affected. Baseline data turns a generic number into an
evidence-based signal tailored to this service and its traffic pattern.
