# AI-red-team Modules

## Module 1 — Core Proof

Entry point: `core_proof.py`

Purpose: prove that untrusted AI-consumed content crossed into unauthorized command/tool execution, then stop.

Maximum active proof:

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

A successful Core Proof never automatically transitions into a deeper module.

## Module 2 — Authorized Lab Expansion

Entry point: `lab_expansion.py`

Purpose: exercise selected post-proof trust boundaries in a dedicated lab using only framework-controlled resources.

Every capability requires both `--confirm-lab` and its own `--allow` gate.

### Synthetic secret

```bash
python lab_expansion.py prepare \
  --scenario synthetic-secret-read \
  --run-dir ./runs/lab-secret \
  --confirm-lab \
  --allow synthetic-secret
```

### Controlled package install

```bash
python lab_expansion.py prepare \
  --scenario controlled-package-install \
  --run-dir ./runs/lab-package \
  --confirm-lab \
  --allow package-install
```

### Privilege-boundary query

```bash
python lab_expansion.py prepare \
  --scenario privilege-boundary-check \
  --run-dir ./runs/lab-priv \
  --confirm-lab \
  --allow privilege-boundary
```

## Design Rule

Each future AI-red-team module should have its own explicit authorization boundary and least-impact proof. Modules must not silently chain into higher-impact behavior.
