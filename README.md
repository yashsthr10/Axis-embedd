# Repository Documentation System

This repository is a reusable documentation framework for software projects.
It is designed so both humans and AI coding agents can quickly understand intent, constraints, and implementation style.

## Why this exists

- Reduce repeated architecture/process questions.
- Keep decisions and rules explicit.
- Make new contributors productive quickly.
- Improve consistency across repositories.

## Start here

Read these files in order:

1. `docs/RepositoryGuide.md`
2. `docs/Architecture.md`
3. `docs/Structure.md`
4. `docs/Rules.md`
5. `docs/Workflow.md`

## Documentation map

- `docs/RepositoryGuide.md` - one-file onboarding guide.
- `docs/SPECS.md` - what must be built and validated.
- `docs/Architecture.md` - high-level component and boundary design.
- `docs/Design.md` - principles and design approach.
- `docs/LLD.md` - low-level implementation details.
- `docs/Structure.md` - folder conventions and ownership boundaries.
- `docs/Modules.md` - module map and responsibilities.
- `docs/Codepath.md` - key execution and data flow paths.
- `docs/Workflow.md` - branch, review, CI/CD, and release process.
- `docs/Rules.md` - hard requirements that must be followed.
- `docs/Conventions.md` - preferred style and team defaults.
- `docs/Patterns.md` - recurring implementation patterns to reuse.
- `docs/Decisions.md` - major technical decisions and rationale.
- `docs/Dependencies.md` - internal and external dependency map.
- `docs/Examples.md` - implementation examples and starter flows.
- `docs/Glossary.md` - shared domain definitions.
- `docs/FAQ.md` - commonly asked repo questions.
- `docs/Changelog.md` - documentation/system change history.

## Usage in new repositories

1. Copy this structure.
2. Replace placeholders with project-specific details.
3. Keep docs updated whenever behavior or architecture changes.
4. Add new decisions and patterns before expanding implementation.

## Maintenance rule

If code changes without corresponding documentation updates, consider the work incomplete.
