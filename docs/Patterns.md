# Patterns

Document recurring implementation patterns to promote consistency.

## 1) Pattern template

- **Pattern name**:
- **When to use**:
- **When not to use**:
- **Structure**:
- **Example locations**:

## 2) Repository Pattern

- **Use for**: abstracting persistence from domain logic.
- **Benefits**: testability, swap-friendly storage adapters.

## 3) Service Pattern

- **Use for**: application-level orchestration of domain operations.
- **Benefits**: keeps handlers/controllers thin.

## 4) Event-Driven Pattern

- **Use for**: decoupled asynchronous processing.
- **Benefits**: scalability and isolation of side-effects.

## 5) Dependency Injection Pattern

- **Use for**: wiring interfaces/implementations cleanly.
- **Benefits**: easier testing and runtime composition.

## 6) Pattern guardrails

- Reuse existing patterns before introducing new abstractions.
- New patterns require an entry in `Decisions.md`.
