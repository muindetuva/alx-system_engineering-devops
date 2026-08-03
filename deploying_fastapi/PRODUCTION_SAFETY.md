# Why Reload Mode Is Unsafe in Production

## File-Watching Overhead

`--reload` continuously scans or subscribes to filesystem changes. That costs
CPU cycles, file descriptors, and I/O on a production host where immutable
application files should not change while the service is running. Those
resources should serve requests instead of supporting a development feedback
loop.

## Single-Process Design

The reload supervisor is designed around restarting a development worker when
source changes. It does not coordinate graceful replacement of four
Gunicorn-managed workers. Gunicorn's master process is responsible for worker
lifecycle, readiness, failure isolation, and graceful HUP reloads; combining
the two supervisors creates conflicting ownership of the same processes.

## Unintended Restarts

An unrelated write beneath a watched directory, such as a generated file or
stray log, can trigger a restart. The development reloader can terminate the
active worker immediately, dropping in-flight requests and briefly leaving no
worker ready to accept authentication traffic.

## Security Surface

A production release should be immutable and replaced through a controlled,
audited deployment. Expecting source files to change live gives an attacker or
misconfigured process a path to execute modified code automatically. Removing
file watching reduces privileges, filesystem activity, and unexpected code
execution paths.
