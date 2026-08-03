# Docker Concepts

## Works On My Machine

A service passed locally but crashed in deployment because it used Python
3.12-only syntax while the server still ran Python 3.10. The implicit Python
version—not the application code—caused the difference. A Docker image records
the runtime and installed dependencies so both environments execute the same
artifact.

## Images vs Containers

An image is like a class: it is an immutable blueprint describing a filesystem
and default process. A container is like an instance of that class: it is a
running, isolated realization with its own writable layer. Running the same
`docker run` command twice creates two independent containers from one image;
it does not reuse an existing instance, just as constructing a class twice
creates two objects.

## Containers vs Virtual Machines

A container isolates processes, filesystems, networks, and resource limits
while sharing the host operating system's kernel. A virtual machine
virtualizes hardware and boots a complete guest operating system with its own
kernel. Containers start faster because they do not boot another kernel and
full OS before starting the application.

## What Docker Does Not Solve

- Docker does not correct application bugs or insecure business logic.
- Docker does not supply secrets or environment-specific configuration by
  itself; those values still need secure configuration management.
- Docker alone does not orchestrate many services, recover failed replicas, or
  design a reliable deployment strategy.
