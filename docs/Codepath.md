# Code Paths

Documents how important flows move through the system.

## 1) Path template

- **Path ID**: `CP-###`
- **Trigger**:
- **Entry point**:
- **Core steps**:
- **Exit points**:
- **Failure points**:
- **Observability fields**:

## 2) Request path example

- **Path ID**: `CP-001`
- **Trigger**: HTTP request
- **Entry point**: interface/controller
- **Core steps**:
  1. Validate request and auth.
  2. Execute application use-case.
  3. Persist and emit side-effects.
  4. Build and return response.
- **Failure points**: validation, dependency timeout, write conflict.

## 3) Async path example

- **Path ID**: `CP-002`
- **Trigger**: queue/event message
- **Entry point**: worker consumer
- **Core steps**:
  1. Parse payload and validate schema.
  2. Execute idempotent processing.
  3. Persist state and ack message.
- **Failure strategy**: retry with backoff, dead-letter routing.

## 4) Why this matters

- Faster debugging and incident triage.
- Better impact analysis before changes.
