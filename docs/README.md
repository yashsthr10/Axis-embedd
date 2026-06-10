# docs

Repository knowledge base. The most important folder.

**Owner**: Friend

## Files

| File | Purpose |
|------|---------|
| `Architecture.md` | System design, component boundaries, data flow diagram |
| `Design.md` | Principles, interface contracts, what not to do |
| `Dataset.md` | Data pipeline stages and output schema |
| `Training.md` | Training loop, checkpointing, resume |
| `Evaluation.md` | Benchmark suites and when to run them |
| `Inference.md` | Serving layer, API contract, performance targets |
| `Decisions.md` | Major technical choices with rationale |
| `Roadmap.md` | Phased plan and milestones |
| `Structure.md` | Folder conventions and placement rules |
| `Modules.md` | Module map, ownership, dependency direction |

## Maintenance rule

Update docs before or alongside code changes. If behavior changes without a doc update, the work is incomplete.

## Decision log

Every major choice goes in `Decisions.md`:

- MLA vs MHA
- SentencePiece vs BPE
- INT8 vs INT4
- Loss function, pooling strategy, etc.

Use the DEC-NNN template defined at the top of that file.
