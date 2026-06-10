# Rules (Must Follow)

These are mandatory. Violations require explicit approval.

## 1) Architectural rules

- Do not place business logic in controller/handler/UI layers.
- Do not bypass module boundaries with direct cross-layer calls.
- Do not access persistence directly when repository/service boundaries exist.

## 2) Reliability and correctness rules

- No silent exception swallowing.
- No non-idempotent retries without protection.
- No schema-breaking changes without migration strategy.

## 3) Security rules

- Never hardcode secrets or tokens.
- Always validate untrusted input.
- Never weaken authentication/authorization checks without approval.

## 4) Testing rules

- New behavior must include tests.
- Bug fixes must include regression tests.
- Critical path changes require integration or end-to-end coverage.

## 5) Documentation rules

- Update docs for architecture, flow, or behavior changes.
- Record major technical choices in `Decisions.md`.
- Keep `Codepath.md` updated for critical execution changes.

## 6) Do not change without explicit agreement

- Public API contracts without a versioning/migration plan.
- Security boundaries and data classification behavior.
- Audit/compliance logging fields used by downstream systems.
