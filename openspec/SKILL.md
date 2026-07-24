---
name: openspec
description: Use when the user asks for OpenSpec, spec-driven development, SDD,
  OPSX commands, product/engineering proposals, requirements/spec changes,
  implementation plans tied to specs, validating implementation against specs,
  or archiving completed changes. Provides workflow guidance for Fission-AI
  OpenSpec and the installed `openspec` CLI.
disable: true
---

# OpenSpec

Use this skill for OpenSpec-style spec-driven development.

Installed CLI:

```bash
openspec --version
```

Local upstream source:

`/Users/hanyueyang/.codex/vendor/OpenSpec`

## When To Use

Use OpenSpec when the user wants to:

- Start or manage a spec-driven development workflow.
- Convert an idea into proposal, requirements, design, and tasks.
- Initialize OpenSpec in a repo.
- Validate current changes/specs.
- Inspect OpenSpec specs or changes.
- Archive completed changes into the source-of-truth specs.
- Use `/opsx:*` commands or asks about OpenSpec/OPSX.

## Core Workflow

Default quick path:

1. Explore uncertainty with `/opsx:explore` style dialogue when the request is unclear.
2. Propose a change with `/opsx:propose <change>` or equivalent artifacts.
3. Implement with `/opsx:apply` only after the plan/spec artifacts are ready.
4. Validate with `openspec validate --all` or targeted validation before claiming completion.
5. Sync/archive with `/opsx:sync` and `/opsx:archive` when work is complete.

Expanded workflow:

- `/opsx:new` creates a change scaffold.
- `/opsx:continue` creates the next ready artifact.
- `/opsx:ff` creates all planning artifacts.
- `/opsx:verify` checks implementation against artifacts.
- `/opsx:bulk-archive` archives multiple completed changes.
- `/opsx:onboard` runs a guided tutorial.

## CLI Use

Initialize a project:

```bash
openspec init --tools codex
```

Update project instructions after CLI upgrade:

```bash
openspec update
```

Inspect state:

```bash
openspec list --json
openspec status --json
openspec show <item> --json
openspec instructions --json
```

Validate:

```bash
openspec validate --all --json
```

Archive:

```bash
openspec archive <change-name>
```

## Agent Discipline

- Prefer OpenSpec artifacts over long-lived chat memory for requirements.
- Do not implement substantial feature work before the proposal/spec/design/tasks are clear.
- Use official CLI JSON output when available rather than parsing terminal text.
- For existing repos, inspect whether `openspec/` already exists before initializing.
- If OpenSpec is not initialized and the user asks for a spec workflow, initialize only after confirming the target repo/path is correct.
- Cross-reference Superpowers-style TDD/review skills when implementation starts.

## References

- CLI reference: `/Users/hanyueyang/.codex/vendor/OpenSpec/docs/cli.md`
- Slash commands: `/Users/hanyueyang/.codex/vendor/OpenSpec/docs/commands.md`
- Concepts: `/Users/hanyueyang/.codex/vendor/OpenSpec/docs/concepts.md`
- Workflows: `/Users/hanyueyang/.codex/vendor/OpenSpec/docs/workflows.md`
- OPSX: `/Users/hanyueyang/.codex/vendor/OpenSpec/docs/opsx.md`
- Getting started: `/Users/hanyueyang/.codex/vendor/OpenSpec/docs/getting-started.md`
