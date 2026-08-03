# Alert Triage for auth-service

## Alert Fatigue

Over-alerting trains responders to treat every notification as noise. Repeated
low-value interruptions consume attention, slow investigation, and reduce trust
in the alerting system. Eventually engineers mute channels, delay acknowledgment,
or apply shallow fixes, so the genuinely critical page receives a slower and
less careful response. Alert fatigue therefore degrades operational safety; it
is not merely annoying.

The triage framework asks the same three questions for every signal:

1. Is it affecting real users right now?
2. Is it newly worsening or likely to become user-impacting soon?
3. Is it a known, stable, low-impact condition with an existing owner?

## Scenario 1

`/token` is returning HTTP 500 for 35% of production requests and users cannot
sign in.

- Affecting real users right now? **Yes.** Authentication is actively failing.
- Newly worsening? **Yes.** The rate jumped from its 0.2% baseline after the
  latest deploy.
- Known, stable, and low impact? **No.** The blast radius is large and growing.

**Urgency decision:** Page the on-call engineer immediately, open an incident,
and consider rolling back the tagged release while evidence is collected.

## Scenario 2

Connection-pool utilization has risen from its normal 35% to 72% over two hours,
but errors and user latency remain within objectives.

- Affecting real users right now? **No.** Requests still succeed normally.
- Newly worsening? **Yes.** The sustained rise deviates from baseline and could
  become exhaustion.
- Known, stable, and low impact? **No.** It is a new trend without an owner.

**Urgency decision:** Create a high-priority investigation for the working team
and notify the service owner now, but do not wake the overnight on-call engineer
unless utilization reaches the critical threshold or users become affected.

## Scenario 3

A low-traffic internal admin endpoint produces the same handled validation error
three times per week, matching a documented issue scheduled for the next sprint.

- Affecting real users right now? **No.** The public authentication flow is not
  involved.
- Newly worsening? **No.** Frequency and impact are stable over several months.
- Known, stable, and low impact? **Yes.** The issue has an owner and tracking ID.

**Urgency decision:** Do not page. Keep the events grouped in Sentry and review
them during routine backlog triage while the existing owner completes the fix.
