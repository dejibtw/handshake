# Handshake Technical Assessments

This repository contains technical assessment work completed as part of Handshake's engineering interview process.

## Repository Structure

```
dynamo/
    log-report/
```

### Current Assessments

| Assessment | Status |
|------------|--------|
| Dynamo - Log Report | Complete |

## Technologies

- Python
- Docker
- Harbor (Terminal-Bench 2)
- Pytest

Each assessment is organized into its own directory with its associated task files, verifier, solution, and environment configuration.

# Dynamo Log Report — Fixed Harbor Task

This directory contains the repaired Terminal-Bench 2 (Harbor) task.

## Repository layout

```text
log-report/
├── task.toml
├── instruction.md
├── environment/
│   ├── Dockerfile
│   └── access.log
├── solution/
│   ├── solve.sh
│   └── solve.py
└── tests/
    ├── test.sh
    └── test_outputs.py
```

The leaked `environment/solution_hint.py` from the broken task has been removed.

## Required validation

From the parent directory containing `log-report/`, run:

```bash
harbor run -p log-report -a oracle
harbor run -p log-report --agent nop
```

Expected rewards:

- Oracle: `/logs/verifier/reward.txt` contains `1`.
- Nop: `/logs/verifier/reward.txt` contains `0`.

Use the real output from your Harbor installation in the assessment evidence fields.

## Wrong-solution check

Temporarily change this line in `solution/solve.py`:

```python
"total_requests": total,
```

to:

```python
"total_requests": total + 1,
```

Run the oracle again. The verifier should report one failed test and reward `0`. Restore the correct line afterward.

## GitHub upload

Create an empty public repository, then run from this directory:

```bash
git init
git add .
git commit -m "Fix Dynamo Harbor log-report task"
git branch -M main
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```

Keep the repository public until the assessment has been reviewed, then make it private as requested.
