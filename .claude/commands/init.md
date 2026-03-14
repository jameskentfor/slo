---
description: Initialize or update CLAUDE.md for a project directory
argument-hint: [directory]
allowed-tools: [Read, Write, Glob, Grep, Bash]
---

Initialize a `CLAUDE.md` file for a project directory.

**Raw argument:** `$ARGUMENTS`

## Step 1 — Resolve the target directory

Parse `$ARGUMENTS` to get the target path:

- If `$ARGUMENTS` is empty, use the current working directory (run `pwd` to get it)
- If `$ARGUMENTS` starts with `@`, strip the leading `@` character to get the path
- Otherwise use `$ARGUMENTS` as-is

Confirm the directory exists:
```
test -d "<resolved-path>" && echo "exists" || echo "not found"
```

If the directory does not exist, stop and tell the user.

## Step 2 — Check for an existing CLAUDE.md

Look for `<resolved-path>/CLAUDE.md`. If it exists, read it so you can update rather than overwrite it. Inform the user whether you are creating or updating the file.

## Step 3 — Explore the project

Use Glob and Read to understand the project. Prioritize these files if present:

- `README.md` / `README` — project description
- `package.json` / `package-lock.json` / `bun.lockb` — Node project metadata and scripts
- `Cargo.toml` — Rust project
- `pyproject.toml` / `setup.py` / `requirements.txt` — Python project
- `go.mod` — Go project
- `pom.xml` / `build.gradle` — Java/Kotlin project
- `Makefile` / `CMakeLists.txt` — C/C++ or generic build
- `.github/workflows/*.yml` — CI pipelines (reveals test/build commands)
- `Dockerfile` / `docker-compose.yml` — containerization details
- `tsconfig.json` / `.eslintrc*` / `.prettierrc*` — TypeScript/JS tooling config
- Top-level `src/` or `lib/` directory structure

Also run:
```bash
ls -la <resolved-path>
```
to see all top-level files including hidden ones.

## Step 4 — Write CLAUDE.md

Write `<resolved-path>/CLAUDE.md` with the following sections, populated from what you discovered. Omit any section for which you found no relevant information. Keep descriptions concise — this file is read by Claude on every session start.

```markdown
# <Project Name>

<One or two sentence description of what this project does and its purpose.>

## Tech Stack

- **Language**: ...
- **Framework/Runtime**: ...
- **Key dependencies**: ...
- **Package manager**: ...

## Common Commands

### Install dependencies
```shell
...
```

### Build
```shell
...
```

### Run
```shell
...
```

### Test
```shell
...
```

### Lint / Format
```shell
...
```

## Project Structure

Brief description of the key directories and their roles:

- `src/` — ...
- `tests/` — ...
- ...

## Architecture Notes

<Important architectural decisions, patterns, or constraints Claude should know about.>

## Coding Conventions

<Style rules, naming conventions, or patterns observed in the codebase.>
```

## Step 5

If the given directory is not the parent directory, include an @ reference to the added CLAUDE.md file in the appropriate location in the parent directory's main CLAUDE.md file

After writing the file, confirm the path and show the user the generated content.
