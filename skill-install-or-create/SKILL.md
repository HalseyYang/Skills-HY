---
name: skill-install-or-create
description: Install third-party Codex or Claude-style skills from GitHub,
  npm/npx commands, local folders, or user-provided skill descriptions; when the
  source cannot be recognized, is too slow, has no valid SKILL.md, or the named
  skill is missing, synthesize a valid local Codex skill from README, docs,
  repository structure, or the user's description. Use when the user asks to
  install, add, clone, import, convert, create, or learn a skill from an
  external source.
---

# Skill Install Or Create

Use this workflow to avoid wasting time on slow or non-standard skill repositories. Prefer a working install when it is fast and reliable; otherwise create a local Codex skill that captures the useful behavior.

## Decision Flow

1. Identify the requested skill.
   - Extract repository URL, install command, skill name, branch, and target agent if provided.
   - If the request contains only a repository URL, inspect metadata and top-level files first.
   - If the user gives a desired behavior but no repo, create a local skill directly.

2. Try the official install path briefly.
   - Use the user's command when it is explicit, such as `npx skills add ... --skill ...`.
   - Stop if clone/download stalls, repeatedly times out, reports "No skills found", or cannot find the named skill.
   - Do not keep retrying whole-repository clones after the same network or structure failure.

3. Inspect the source without full clone.
   - Prefer GitHub API, README, package metadata, docs, and exact `SKILL.md` paths.
   - Search for the requested skill name and likely aliases.
   - If an exact standard skill directory is found, install just that directory.

4. Create a local skill when install is not clearly better.
   - Base it on the source's README, docs, examples, prompt text, directory names, and the user's stated intent.
   - Place it in `/Users/hanyueyang/.codex/skills/<skill-name>` unless the user asks for another location.
   - Use `skill-creator` conventions: required `SKILL.md`, optional `agents/openai.yaml`, and only useful references/scripts/assets.

5. Validate and report.
   - Run the skill validator.
   - Verify `SKILL.md` exists.
   - Tell the user what was installed or synthesized, where it lives, and whether Codex should be restarted.

## Time Budget

Use these default cutoffs unless the user asks to keep trying:

- `npx skills add` clone animation with no progress: stop after about 15-25 seconds.
- Git clone disconnect or timeout: do not retry more than once.
- Large zip downloads: avoid unless exact directory download is unavailable and the repo is small.
- Missing named skill after API/path search: create a local skill from available descriptions.

## Skill Synthesis Rules

When creating a replacement skill:

- Preserve the user's requested skill name when valid; normalize to lowercase hyphen-case.
- Write a broad but accurate `description` that includes trigger phrases.
- Put core workflow in `SKILL.md`.
- Put detailed checklists, matrices, examples, or standards in `references/`.
- Add scripts only when deterministic automation is genuinely useful.
- Do not claim the synthesized skill is the original upstream skill.
- Say clearly that it was generated locally from available descriptions.

## Source Inspection Checklist

Look for:

- `SKILL.md` files.
- `README.md`, docs, examples, prompts, agent files, command files, or templates.
- Package manifests mentioning skill paths.
- `.claude/skills`, `.codex/skills`, `skills/`, `agents/`, `commands/`, `templates/`, or domain folders.
- Existing install docs that name exact directories.

## Report Template

Use a short report:

```text
Done. I [installed/synthesized] <skill-name>.

Path: <absolute path>
Validation: <result>
Note: <anything important, such as "upstream install was not usable because ...">

Restart Codex to load it.
```
