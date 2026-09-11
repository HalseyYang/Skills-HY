## Description:

WorkRally CLI gives agents command-line workflows for AIGC comic and video production, including image, video, audio, prompt optimization, project and series management, assets, canvas operations, uploads, and downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and agent operators use this skill to manage WorkRally projects and drive AI image, video, audio, prompt-optimization, media, and canvas workflows from the WorkRally CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives agents broad account-level WorkRally access and can invoke general WorkRally tools.

Mitigation: Install only for agents that should operate a real WorkRally account, and require explicit user confirmation before any `tools call` execution.

Risk: Delete and overwrite workflows can remove projects, series, shots, recycle-bin items, or canvas nodes.

Mitigation: Require explicit confirmation for recycle-bin permanent deletion, canvas node deletion, and any canvas command using `--mode overwrite`.

Risk: The WorkRally API key may be persisted in a local config file.

Mitigation: Avoid storing the API key on shared machines unless the config directory and file permissions are controlled; use `WORKRALLY_CONFIG_DIR` where isolation is needed.

## Reference(s):

- [WorkRally skill page](https://clawhub.ai/tencent-adm/skills/workrally)
- [Publisher profile](https://clawhub.ai/user/tencent-adm)
- [WorkRally homepage](https://workrally.qq.com)
- [WorkRally API key request](https://workrally.qq.com/open-api)
- [AI generation guide](references/ai-generation-guide.md)
- [Canvas guide](references/canvas-guide.md)
- [Common pitfalls](references/common-pitfalls.md)
- [Shotlist guide](references/shotlist-guide.md)
- [Upload and assets guide](references/upload-and-assets-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with WorkRally CLI commands, JSON command arguments, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [WorkRally CLI output is normally JSON for agent use, with table and text modes also supported.]

## Skill Version(s):

2.6.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
