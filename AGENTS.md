# AGENTS.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal dotfiles repository, forked from [mathiasbynens/dotfiles](https://github.com/mathiasbynens/dotfiles). Managed via **chezmoi**, which templates and deploys dotfiles from this repo to `$HOME`.

## Commands

```bash
# Deploy dotfiles to $HOME
chezmoi apply

# Preview what would change
chezmoi diff

# Edit a managed file (opens in $EDITOR, applies on save)
chezmoi edit ~/.aliases

# Install Homebrew packages (deployed to ~/brew.sh by chezmoi)
bash ~/brew.sh

# Install command-line tools via uv (deployed to ~/uv.sh by chezmoi)
bash ~/uv.sh

# Apply macOS system defaults (requires sudo)
bash ~/.macos
```

## Architecture

### chezmoi source layout

chezmoi's source directory is this repo. Files are named with chezmoi conventions:

- `dot_foo` → `~/.foo` (plain dotfile)
- `dot_foo.tmpl` → `~/.foo` (templated dotfile, rendered before deployment)
- `executable_foo.tmpl` → `~/foo` (executable script, rendered before deployment)

Files listed in `.chezmoiignore` are not deployed (e.g. `AGENTS.md`, `README.md`).

### Machine config

Each machine carries one untracked file that declares its identity:

```toml
# ~/.config/chezmoi/chezmoi.toml
sourceDir = "/path/to/dotfiles"

[data]
    machine = "home"   # one of: home, work, serv, atos
```

This file is never committed. chezmoi reads `.machine` from it when rendering templates.

### Templated files

Five files vary per machine and use Go template syntax:

| Source file | Deployed as | Varies by machine |
|---|---|---|
| `dot_path.tmpl` | `~/.path` | GNU tool paths, ruby, Python, bats, pocket |
| `dot_exports.tmpl` | `~/.exports` | `$PERM` variable (work only) |
| `dot_aliases.tmpl` | `~/.aliases` | `pn` alias (work), `prun` alias (atos) |
| `dot_gitconfig.tmpl` | `~/.gitconfig` | `[include]` for ifs-git-tools (work, atos) |
| `executable_brew.sh.tmpl` | `~/brew.sh` | package list varies per machine |

### Agent skills

Personal agent skills live under `private_dot_agents/skills`, which deploys to
`~/.agents/skills`. Add future skills there as one directory per skill, each
with a `SKILL.md`.

`run_after_sync_agent_skills.sh.tmpl` links every deployed skill into the
harness-specific compatibility directories used by Claude Code, legacy Codex,
OpenCode, and goose. The script leaves differing local directories alone
instead of overwriting them.

| Harness | Skill paths covered |
|---|---|
| Agent Skills clients, including Codex and goose | `~/.agents/skills` |
| Claude Code | `~/.claude/skills` |
| Legacy Codex | `~/.codex/skills` |
| OpenCode | `~/.config/opencode/skills` |
| goose compatibility | `~/.config/goose/skills`, `~/.config/agents/skills` |

### Shell configuration loading order

`~/.bash_profile` sources these files in order:
1. `~/.path` — PATH additions
2. `~/.bash_prompt` — Solarized Dark prompt with git status
3. `~/.exports` — environment variables
4. `~/.aliases` — command aliases
5. `~/.functions` — shell functions
6. `~/.extra` — machine-local config (not tracked; for secrets/overrides)

### Key files

| File | Purpose |
|------|---------|
| `dot_gitconfig.tmpl` | Extensive git aliases; see `[alias]` section for full list |
| `dot_vimrc` | Vundle plugins (gruvbox, editorconfig, rust.vim, copilot.vim), templates, Copilot bindings |
| `dot_tmux.conf` | Prefix=Ctrl-A, vi mode, TPM plugins (sensible, resurrect) |
| `dot_macos` | macOS `defaults write` settings — most lines commented out for safety |
| `dot_exports.tmpl` | Sets `EDITOR=vim`, locale (en_GB.UTF-8), history size (32K), Homebrew no-analytics |

### Vim templates

`dot_vimrc` has file template support triggered by `Space+t` (bash skeleton). Templates live in `dot_vim/templates/bash/`.

### Machine-local customization

Create `~/.extra` for anything not committed here (tokens, `git config user.email`, machine-specific aliases, etc.).

## Upstream

Upstream remote is `https://github.com/mathiasbynens/dotfiles.git` — pull upstream changes with `git fetch upstream`.
