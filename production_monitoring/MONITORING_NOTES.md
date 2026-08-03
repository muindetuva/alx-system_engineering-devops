# Why auth-service Needs Production Monitoring

## The Local-vs-Production Gap

Passing local tests and CI proves behavior only for known inputs and controlled
resources. Production traffic supplies unpredictable input shapes, request
ordering, and volumes that the test suite may never have exercised. For
example, many simultaneous token requests can exhaust worker or connection
capacity even when each isolated request passes locally.

Production also depends on real infrastructure: DNS, TLS renewal, Nginx,
Gunicorn workers, network latency, host memory, disk space, and provider
availability. A CI runner does not reproduce those dependencies or the
long-running state in which resource leaks accumulate. Monitoring closes this
gap by observing the deployed `auth-service` under real concurrency, real
input, and real infrastructure conditions.

## Three Distinct Categories

- **Error tracking** records failures such as exceptions, stack traces, release
  tags, and affected requests so engineers can diagnose what broke.
- **Performance monitoring** measures latency and resource timing through
  transactions and spans, revealing slow endpoints even when they return 200.
- **Usage monitoring** measures traffic volume, endpoint adoption, active users,
  and behavior patterns so the team understands how the system is used.

The axes can disagree. `/token` might have a healthy p50 latency while a rare
validation exception fails for 2% of users, which is an error-tracking problem.
Conversely, it can have zero exceptions but an unhealthy p99 latency, which is
a performance problem. Both can look healthy while usage drops sharply because
clients cannot resolve the domain.

## Why Not Just Wait for Reports

User reports are a biased sample: many affected users abandon a request rather
than report it, while a vocal minority may overrepresent one workflow. Reports
usually arrive without a stack trace, release identifier, timing spans, or host
metrics, so they lack the technical context required for diagnosis. They are
also a lagging signal that arrives after users have already experienced harm.
Automated monitoring detects leading deviations and supplies evidence before a
support report is written.
