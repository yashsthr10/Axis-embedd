# Design

Defines design principles and style for maintainable implementation.

## 1) Design principles

- Keep solutions simple and explicit.
- Separate domain logic from transport/infrastructure.
- Favor composition over inheritance when practical.
- Keep side-effects at boundaries.
- Make invalid states hard to represent.

## 2) Design constraints

- Performance expectations:
- Security expectations:
- Reliability expectations:
- Backward compatibility policy:

## 3) Interface design

- Clear input/output contracts.
- Validation at boundaries.
- Stable response/error schema.
- Versioning and compatibility strategy.

## 4) Data design

- Canonical entities and identifiers.
- Mutation and consistency rules.
- Auditability requirements.

## 5) Error and resilience design

- Error taxonomy and mapping strategy.
- Retry/idempotency policy.
- Timeout and circuit-breaker policy.

## 6) Testing design

- Unit tests for domain behavior.
- Integration tests for adapters and boundaries.
- Contract tests for external dependencies.
- End-to-end tests for critical journeys.

## 7) Link to reusable patterns

Implementation patterns are documented in `Patterns.md`.
