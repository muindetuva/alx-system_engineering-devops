# Why Multi-Stage Builds Matter

## The single-stage problem

Some Python packages need `gcc` and `python3-dev` while `pip install` compiles
native extensions. The finished wheels and installed modules no longer invoke
the compiler or need development headers at runtime. Leaving those tools in a
single-stage production image wastes space, increases download time, and adds
unnecessary packages to the attack surface.

## The `COPY --from` mechanism

A named builder stage may contain the compiler and every temporary build
artifact. A later clean stage starts from a new base image. The instruction
`COPY --from=builder /root/.local /root/.local` transfers only the completed
user-site installation; everything not explicitly copied forward is absent
from the final image. The result retains runtime dependencies and discards the
build toolchain.
