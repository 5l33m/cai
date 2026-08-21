# AI-red-team

`AI-red-team` is an extensible adversarial-testing skill for AI agents and tool-using LLM systems.

This is the stable skill name. The first implementation focuses on agent trust boundaries and prompt-injection-driven tool abuse, with room to add broader AI red-team modules later.

## Start here

### Core Proof

Use Core Proof first. It proves unauthorized command execution and stops at one of:

- `whoami`
- `id`
- `hostname`

Example:

```bash
python core_proof.py test \
  --agent codex \
  --scenario github-issue-whoami \
  --run-dir ./runs/core-001
```

### Authorized Lab Expansion

Start this separately only after an explicit ROE decision.

```bash
python lab_expansion.py prepare \
  --scenario synthetic-secret-read \
  --run-dir ./runs/lab-secret \
  --confirm-lab \
  --allow synthetic-secret
```

Supported lab gates currently include:

- synthetic-secret
- package-install
- privilege-boundary

## Invocation examples

- `Use AI-red-team to assess this coding agent. Start with Core Proof.`
- `Use AI-red-team to map the trust boundaries for this MCP-enabled workflow.`
- `Use AI-red-team against this GitHub issue flow and stop at whoami.`
- `Use AI-red-team for an authorized lab expansion using synthetic secrets only.`

## Architecture

```text
AI-red-team
   |
   +-- Core Proof
   |     +-- whoami
   |     +-- id
   |     +-- hostname
   |     +-- STOP
   |
   +-- Authorized Lab Expansion
         +-- synthetic secret
         +-- isolated local package install
         +-- privilege-boundary query
         +-- STOP
```

The current engine is shared with the original trust-boundary implementation while `AI-red-team` becomes the stable public entry point for future modules.

See `SKILL.md` for the full operating rules and `MODULES.md` for the two-module execution model.
