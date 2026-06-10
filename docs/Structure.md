# Structure

Defines where code should go and how directories are organized.

## 1) Top-level layout

- `src/` - source code.
- `tests/` - unit/integration/e2e tests.
- `scripts/` - development and operational scripts.
- `docs/` - repository knowledge and design documents.
- `config/` - static configuration templates.

## 2) Internal source layout (example)

- `src/domain/` - core business logic.
- `src/application/` - use-cases and orchestration.
- `src/interfaces/` - API/CLI/event handlers.
- `src/infrastructure/` - persistence and external integrations.
- `src/shared/` - shared helpers/types.

## 3) Placement rules

- Business rules belong in `domain`.
- Side-effectful integration code belongs in `infrastructure`.
- Interface adapters do not contain business rules.
- Shared utilities should not become implicit dumping grounds.

## 4) Ownership

Module ownership and boundaries are in `Modules.md`.
