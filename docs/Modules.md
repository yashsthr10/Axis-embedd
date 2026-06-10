# Modules

High-level map of codebase modules and ownership.

## 1) Module catalog

For each module:

- **Module name**:
- **Path**:
- **Purpose**:
- **Owns**:
- **Depends on**:
- **Owned by**:

## 2) Example module map

- `api/` - request handling and response formatting.
- `business/` - domain services and core logic.
- `storage/` - database repositories and migrations.
- `workers/` - async/background processing.

## 3) Ownership rules

- Each module has a clear owner.
- Cross-module writes require explicit contracts.
- Shared abstractions require documented consumers.

## 4) Placement decision guide

Before adding new code:

1. Identify owning module.
2. Verify dependency direction in `Dependencies.md`.
3. Follow pattern examples in `Patterns.md` and `Examples.md`.
