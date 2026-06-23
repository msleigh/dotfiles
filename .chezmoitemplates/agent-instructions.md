# Git

## General

- Always use version control, even for small projects, non-code projects, etc.
- Always use Git for version control.
- Use Git worktrees.
- Don't use `git add -A`

## Config

- Keep user name and email in local config only, never global or system.
- Use either:
  - "Michael Sleigh" and my ECMWF work email for ECMWF work, or
  - "msleigh" and "msleigh@users.noreply.github.com" for personal work.

## Commit messages

- Don't add co-authors to commit messages unless I explicitly request it.

# Writing

## General rules

- Use British English.
- Use the Oxford comma.
- Use plain English.
- Value brevity.

## Specific rules

- Don't use "invite" as a noun, it's a verb; use "invitation".

# Code

## General

- Preferred languages are Bash, Python, Fortran.
- Rust is acceptable for personal projects, but not for ECMWF work.
- Only consider Rust where there's a significant advantage over preferred languages.
- Value brevity, readability, and maintainability.
- Use Markdown for documentation, never ReStructuredText or other formats.
- Spaces not tabs for indentation.

## General Tooling

- Use Pre-commit for code quality checks and formatting.
- Use Zensical for documentation.
- Use Quarto for presentations and reports.
  - Presentations should be rendered to HTML unless otherwise requested.
  - HTML presentations should be standalone.

## Python

- Python work should always be in a virtual environment.
- Use:
  - uv for dependency management;
  - ruff for linting and formatting;
  - pyproject.toml for project configuration;
  - pytest for testing.

## Shell

- Use Bash for shell scripting and commands.
- Use shfmt for shell script formatting.
- Use shellcheck for shell script linting.
- Start all scripts with a shebang.
- Use `set -euo pipefail` in all scripts.
- Use functions in scripts to improve readability and maintainability.
- Use `[[` for conditional expressions in Bash scripts, never `[` or `test`.
- Use `$(...)` for command substitution, never backticks.
- Use `source` to include other scripts, never `.`.
- Be pedantic about quoting variables in shell scripts.
- Always use braces around variable names in shell scripts, even when not necessary.

## Fortran

- Write Fortran in free format.
- Use Ford for Fortran documentation.

# File System

- No spaces ever in file or directory names, use underscores or hyphens instead.
- All projects should go in ~/projects.
- Each project in ~/projects should be a Git repository.
- Presentation files live in ~/projects/work_notes/presentations

## Dotfiles

- Dotfiles are managed in a Git repository at ~/projects/dotfiles.
- Do not edit dotfiles directly outside of this repo.
- User-level (as opposed to project-specific) agent instructions files such as
  AGENTS.md, CLAUDE.md, and copilot-instructions.md are also managed via
  dotfiles; do not edit versions outside that repo.

# IFS

- "IFS" (the system) stands for "Integrated Forecasting System".
- My job title is "Head of Integrated Forecast Systems" (plural, no "-ing").
- My section is "Integrated Forecast Systems Section" (plural, no "-ing").
- For IFS cycles use "Cy51r1" or "51r1". Use all-upper-case "CY51R1" only when
  referring to the Git branch.
