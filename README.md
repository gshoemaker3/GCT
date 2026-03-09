# `GCT` — CLI Reference

> Fast. Scriptable. No fluff.

---

## Developer Quickstart

_Get your environment set up to pull branches, make changes, and commit while staying compliant with the coding standard._

---

### Prerequisites

| Requirement | Minimum Version |
|---|---|
| Python | `>= 3.8` |
| Git | Any recent version |
| pip | Bundled with Python |

---

### 1 · Clone the Repository

```bash
git clone <repo-url>
```

---

### 2 · Install Dependencies

All dev dependencies are declared in `pyproject.toml`. Install the project in editable mode with the full dev dependency set:

```bash
pip install -e ".[dev]"
```

> 💡 Editable mode (`-e`) means changes you make to the source are reflected immediately without reinstalling. The `[dev]` extra pulls in `pytest`, `black`, `bandit`, `safety`, `pyinstaller`, `pdoc`, and `pre-commit`.

---

### 3 · Set Up Pre-Commit Hooks

This project uses `pre-commit` to enforce the coding standard automatically on every commit. The hooks are defined in `.pre-commit-config.yaml` and run the following checks:

| Hook | What it enforces |
|---|---|
| `check-yaml` | Valid YAML syntax |
| `check-toml` | Valid TOML syntax |
| `end-of-file-fixer` | All files end with a newline |
| `trailing-whitespace` | No trailing whitespace |
| `black` | Code formatting (Python 3.13) |
| `bandit` | Static security analysis (SAST) |
| `trufflehog` | Secret scanning — prevents credentials from being committed |

Install the hooks into your local git repo:

```bash
pre-commit install
```

> 💡 Once installed, the hooks run automatically on every `git commit`. You never have to invoke them manually.

Verify the hooks are wired up correctly by doing a dry run against all files:

```bash
pre-commit run --all-files
```

> ⚠️ The first run may take a moment — pre-commit downloads and sets up each hook environment on initial execution. Subsequent runs are fast.

---

### 4 · Run the Tests

Confirm your environment is fully working by running the test suite:

```bash
pytest tests/unit_tests
```

Test paths and options are configured in `pyproject.toml` under `[tool.pytest.ini_options]`.

> ⚠️ All tests must pass before opening a pull request. The CI pipeline enforces this on merge to `main`.

---

### 5 · Making Commits

Once your hooks are installed, a standard commit works as normal:

```bash
git add .
git commit -m "your message"
```

Pre-commit will run all hooks before the commit is finalized. If any hook fails, the commit is blocked and the output will tell you exactly what to fix.

```bash
# If black reformats files, simply stage the changes and re-commit
git add .
git commit -m "your message"
```

> ⚠️ Never use `--no-verify` to bypass the hooks. The same checks run in CI — bypassing them locally will result in a failed pipeline on your PR.

---

## CLI Usage Reference

| Command | Aliases | What it does |
|---|---|---|
| `--interactive` / `-i` | — | Launch interactive mode |
| `copy` | `cp` | Copy a file to a destination |
| `mkfile` | `mkf` | Create a new file |
| `merge` | `combine` | Merge two files into one |

---

## Global Flags

### `-i`, `--interactive`
Launches the tool in **interactive mode** — a REPL-style session for running commands without re-invoking the binary each time.

```bash
gct --interactive
```

> 💡 `--interactive` can be combined with a subcommand to launch interactive mode after an initial operation.

---

## Commands

---

### `copy` · `cp`
_Copy a file from a source path to a destination._

```
gct copy -s <SOURCE> [-d <DESTINATION>]
```

| Flag | Long form | Required | Description |
|---|---|---|---|
| `-s` | `--src` | ✅ | Path to the file being copied |
| `-d` | `--dest` | ❌ | Destination path. Uses **default path** if omitted |

**Examples**

```bash
# Copy with explicit destination
gct copy -s /home/user/report.txt -d /backup/report.txt

# Copy using alias, let the tool pick the destination
gct cp -s /home/user/report.txt
```

> ⚠️ If `-d` is omitted, the file is copied to the tool's configured default destination path.

---

### `mkfile` · `mkf`
_Create a new file at a specified location._

```
gct mkfile -n <FILENAME> [-d <DIRECTORY>]
```

| Flag | Long form | Required | Description |
|---|---|---|---|
| `-n` | `--name` | ✅ | File name **including extension** (e.g. `notes.txt`) |
| `-d` | `--dir` | ❌ | Directory to create the file in. Uses **default directory** if omitted |

**Examples**

```bash
# Create a file in a specific directory
gct mkfile -n report.csv -d /output/data/

# Create a file using alias, default directory used
gct mkf -n config.json
```

> ⚠️ The `-n` value must include the file extension — `report` ❌, `report.txt` ✅

---

### `merge` · `combine`
_Merge two files into a single new output file._

```
gct merge -f1 <FILE_1> -f2 <FILE_2>
```

| Flag | Long form | Required | Description |
|---|---|---|---|
| `-f1` | `--file-1` | ✅ | Path to the first source file |
| `-f2` | `--file-f2` | ✅ | Path to the second source file |

**Examples**

```bash
# Merge with a custom output directory
gct merge -f1 part1.txt -f2 part2.txt

# Merge using alias, save to default directory
gct combine -f1 chunk_a.log -f2 chunk_b.log
```

> ⚠️ File order matters — `FILE_1` content comes first, followed by `FILE_2`.

---

## Default Paths

When an optional destination or directory flag is omitted, `gct` falls back to these defaults:

| Operation | Default Path |
|---|---|
| `copy` destination | `<CWD>/files` |
| `mkfile` directory | `<CWD>/files` |
| `merge` output directory | `<CWD>/files` |

---

## Getting Help

```bash
# Top-level help
gct --help

# Command-specific help
gct copy --help
gct mkfile --help
gct merge --help
```

---

<sub>All paths must be absolute or relative to your working directory. Relative paths are resolved at runtime.</sub>
