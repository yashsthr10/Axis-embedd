# Dependencies

Maps internal and external dependencies and their impact.

## 1) Internal dependency map

For each module:

- **Module**:
- **Depends on**:
- **Used by**:
- **Allowed dependency direction**:

## 2) External dependencies

For each dependency:

- **Name**:
- **Type**: database, queue, API, cloud service, library.
- **Used by module(s)**:
- **Criticality**: low, medium, high.
- **Failure impact**:
- **Fallback strategy**:

## 3) Contract dependencies

- Upstream contracts depended on:
- Downstream consumers depending on us:
- Versioning/compatibility notes:

## 4) Change impact checklist

Before changing a component:

1. Check who depends on it.
2. Check compatibility requirements.
3. Check migration and rollback plan.
4. Update `Decisions.md` if trade-offs changed.
