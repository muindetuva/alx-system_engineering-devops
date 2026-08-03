# Reading Performance Data

## Why Percentiles, Not Just Averages

Percentiles describe the distribution of request times. p50 is the median: half
of requests are faster and half are slower. p95 is the value under which 95% of
requests finish, while p99 describes the boundary for 99% and exposes the slow
tail experienced by roughly one request in a hundred.

An average blends fast and slow requests and can look healthy when a small but
important group is suffering. Ninety-nine requests at 100 ms and one request at
10 seconds average about 199 ms, yet the p99 reveals a genuinely bad tail. The
team should compare p50, p95, and p99 against baselines and service objectives
rather than trusting one average.

## A Post-Deploy Slowdown

Suppose `/verify` p95 rises sharply immediately after commit `a3f9c21` is
deployed. Sentry tracing shows one database lookup for every permission attached
to a token instead of a single batched lookup. The timing relationship to the
deploy and dozens of repeated query spans per request point to an N+1 query
pattern introduced by the new permission expansion. The fix is to batch or
preload permissions and add a query-count regression test.

## A Consistently Slow Endpoint

Suppose `/audit-history` has remained slow but stable for months across releases
and load levels. Its trace contains one database query that repeatedly scans a
large audit table by `user_id`. That shape points to a missing database index,
not a newly introduced code path. Adding and measuring an index on `user_id`,
after checking write and storage cost, addresses the consistent bottleneck.
