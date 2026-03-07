# `GCT` — CLI Reference

> Fast. Scriptable. No fluff.

---

## Quick Reference

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
