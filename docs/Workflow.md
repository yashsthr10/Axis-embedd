# Workflow

Defines runtime behavior: for each invocation type, how control and data flow through the code.

## 1) Purpose

- Explain what happens in the program for a given request/event/trigger.
- Make debugging and impact analysis faster.
- Keep execution behavior explicit across synchronous and asynchronous paths.

## 2) Workflow entry template

Use this template for each flow:

- **Workflow ID**: `WF-###`
- **Invocation type**: API request, event message, cron/scheduler, CLI/manual, webhook.
- **Trigger**:
- **Entry point**: file/module/function.
- **Pre-checks**: auth, validation, idempotency, feature flag checks.
- **Execution steps**: ordered list of function/module transitions.
- **State interactions**: database/cache/queue/external APIs touched.
- **Exit path**: response/event/side-effect.
- **Failure path**: retries, compensations, dead-letter, fallback.
- **Observability**: logs, metrics, traces, correlation fields.

## 3) API request workflow (sync)

### WF-001

- **Invocation type**: API request.
- **Trigger**: Client sends HTTP request.
- **Entry point**: Route/handler/controller.
- **Typical steps**:
  1. Parse and validate request.
  2. Authorize caller and apply guard checks.
  3. Execute application/domain service.
  4. Persist changes and publish optional events.
  5. Build and return response.
- **Failure path**:
  - Validation failure -> 4xx.
  - Domain conflict -> deterministic business error.
  - Dependency timeout -> retry or mapped 5xx.

## 4) Event/queue workflow (async)

### WF-002

- **Invocation type**: Queue/event consumer.
- **Trigger**: Message arrives on topic/queue.
- **Entry point**: Worker/consumer handler.
- **Typical steps**:
  1. Decode payload and validate schema.
  2. Check idempotency key/dedup guard.
  3. Execute processing service.
  4. Persist result and emit follow-up event.
  5. Ack/commit offset.
- **Failure path**:
  - Transient error -> retry with backoff.
  - Permanent error -> dead-letter + alert.

## 5) Scheduled workflow (batch/cron)

### WF-003

- **Invocation type**: Scheduled job.
- **Trigger**: Cron/timer scheduler.
- **Entry point**: Job runner function.
- **Typical steps**:
  1. Acquire lock to prevent duplicate runs.
  2. Load job scope/input window.
  3. Process in chunks with checkpoints.
  4. Persist progress and completion state.
  5. Emit summary metrics/notifications.
- **Failure path**:
  - Partial failure -> checkpoint resume.
  - Full failure -> alert + rerun policy.

## 6) Manual/CLI workflow

### WF-004

- **Invocation type**: CLI/manual trigger.
- **Trigger**: Operator command.
- **Entry point**: CLI command handler/script.
- **Typical steps**:
  1. Parse command options.
  2. Validate environment and permissions.
  3. Execute requested operation.
  4. Print result and write audit logs.
- **Failure path**:
  - Invalid args -> usage error.
  - Unsafe operation -> blocked unless explicit override.

## 7) How to keep this file updated

- Add a new workflow entry whenever a new invocation path is introduced.
- Update affected workflow steps when control flow changes across modules.
- Keep workflow IDs stable to make incident and PR references easy.
