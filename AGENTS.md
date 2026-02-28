# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal dotfiles repository, forked from [mathiasbynens/dotfiles](https://github.com/mathiasbynens/dotfiles). Managed via **GNU Stow**, which creates symlinks from `$HOME` into this repo.

## Commands

```bash
# Install/update dotfiles (creates symlinks via stow)
bash bootstrap.sh        # prompts for confirmation
bash bootstrap.sh -f     # skip confirmation

# Install Homebrew packages
bash brew.sh

# Check what would change (diff repo vs $HOME)
bash check.sh

# Apply macOS system defaults (requires sudo)
bash .macos
```

## Architecture

### Stow-based symlink management

`bootstrap.sh` runs:
```
stow --dotfiles --dir=.. --target="${HOME}" --verbose=1 dotfiles
```

Stow maps every file in this repo to the corresponding path under `$HOME`. Files listed in `.stow-local-ignore` are excluded from symlinking (e.g. `bootstrap.sh`, `brew.sh`, `check.sh`, `init/`, `README.*`, `LICENSE.*`, `bin/subl`).

### Shell configuration loading order

`.bash_profile` sources these files in order:
1. `.path` — PATH additions (`$HOME/bin`, Cargo, Pipx)
2. `.bash_prompt` — Solarized Dark prompt with git status
3. `.exports` — environment variables
4. `.aliases` — command aliases
5. `.functions` — shell functions
6. `~/.extra` — machine-local config (not tracked; for secrets/overrides)

### Key files

| File | Purpose |
|------|---------|
| `.gitconfig` | Extensive git aliases; see `[alias]` section for full list |
| `.vimrc` | Vundle plugins (gruvbox, editorconfig, rust.vim, copilot.vim), templates, Copilot bindings |
| `.tmux.conf` | Prefix=Ctrl-A, vi mode, TPM plugins (sensible, resurrect) |
| `.macos` | macOS `defaults write` settings — most lines commented out for safety |
| `.exports` | Sets `EDITOR=vim`, locale (en_GB.UTF-8), history size (32K), Homebrew no-analytics |

### Vim templates

`.vimrc` has file template support triggered by `Space+t` (bash skeleton) and `F4` (copyright header). Templates live in `.vim/templates/bash/`.

### Machine-local customization

Create `~/.extra` for anything not committed here (tokens, machine-specific aliases, `git config user.email`, etc.).

## Branch structure

`main` contains platform-independent config that applies everywhere. Platform-specific branches carry additional commits on top:

| Branch | Purpose |
|--------|---------|
| `machome` | Home Mac |
| `macwork` | Work Mac |
| `atos` | ATOS environment |

Keep as much as possible in `main`. When `main` changes, rebase the platform branches onto it:

```bash
git checkout machome && git rebase main
git checkout macwork && git rebase main
git checkout atos    && git rebase main
```

## Upstream

Upstream remote is `https://github.com/mathiasbynens/dotfiles.git` — pull upstream changes with `git fetch upstream`.
