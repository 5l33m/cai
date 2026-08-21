# Two-Module Operating Model

The framework is intentionally split into two independent execution modules.

## Module 1 — Core Proof

Entry point: `core_proof.py`

Purpose: prove that untrusted content crossed into command execution, then stop.

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

This module does not authorize or request secret access, persistence, privilege escalation, package installation, destructive actions, or exfiltration.

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

Creates a randomized fake canary file. The generated agent instruction permits reading only that file and requires an immediate stop afterward.

### Controlled package install

```bash
python lab_expansion.py prepare \
  --scenario controlled-package-install \
  --run-dir ./runs/lab-package \
  --confirm-lab \
  --allow package-install
```

Generates a local no-network test package intended only for a disposable virtual environment. Remote repositories and system-wide installs are out of scope.

### Privilege-boundary query

```bash
python lab_expansion.py prepare \
  --scenario privilege-boundary-check \
  --run-dir ./runs/lab-priv \
  --confirm-lab \
  --allow privilege-boundary
```

Permits only a non-mutating privilege query such as `sudo -n -l` in a dedicated lab account. It explicitly forbids executing any listed privileged command or attempting escalation.

## Permanently excluded from both modules

- destructive actions;
- persistence;
- credential dumping;
- real secret collection when a synthetic canary can prove the boundary;
- uncontrolled or third-party exfiltration;
- privilege escalation;
- remote or system-wide package installation;
- autonomous propagation.

The split is deliberate: a Core Proof success never automatically transitions into Module 2. The operator must start Module 2 separately and opt into one capability at a time.
