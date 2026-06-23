# dotfiles

My personal dotfiles, managed with [chezmoi](https://www.chezmoi.io/) and
templated per machine across macOS and Linux.

## Installation

### Prerequisites

Install chezmoi. On macOS with Homebrew:

```bash
brew install chezmoi
```

On Linux without admin access:

```bash
sh -c "$(curl -fsLS get.chezmoi.io)" -- -b ~/.local/bin
```

### Set up machine config

Create `~/.config/chezmoi/chezmoi.toml` — this file is not tracked in the repo:

```toml
sourceDir = "/path/to/this/repo"

[data]
    machine = "home"   # one of: home, work, serv, atos
```

### Apply

```bash
chezmoi apply
```

This deploys all dotfiles to `$HOME`, rendering any machine-specific templates
for the declared machine. To preview changes before applying:

```bash
chezmoi diff
```

## Ongoing use

```bash
# Preview what apply would change (also the way to check $HOME for drift)
chezmoi diff

# Check whether $HOME matches the source state (non-zero exit if it differs)
chezmoi verify

# Re-deploy after pulling changes
chezmoi apply

# Edit a managed file (applies on save)
chezmoi edit ~/.aliases

# Install Homebrew packages
bash ~/brew.sh

# Apply macOS system defaults
bash ~/.macos
```

## Machine-local customisation

Create `~/.extra` for anything that shouldn't be committed: API tokens,
machine-specific aliases, etc. It is sourced by `~/.bash_profile` after all
other dotfiles.

## Secret scanning

This repo is public, so commits are scanned for secrets with
[gitleaks](https://github.com/gitleaks/gitleaks) via a
[pre-commit](https://pre-commit.com/) hook (`.pre-commit-config.yaml`).
pre-commit manages its own pinned gitleaks binary, so no separate gitleaks
install is required.

After cloning, arm the hook once:

```bash
pre-commit install
```

Run it manually across all files at any time:

```bash
pre-commit run --all-files
```

The config is excluded from deployment in `.chezmoiignore`, so it stays in the
repo and is never written to `$HOME`.

## Structure

Machine-specific differences are handled via Go templates rather than branches.
Five files are templated (`dot_path.tmpl`, `dot_exports.tmpl`,
`dot_aliases.tmpl`, `dot_gitconfig.tmpl`, `executable_brew.sh.tmpl`); the rest
are plain files renamed with chezmoi's `dot_` prefix convention. See
`AGENTS.md` for full architecture details.

## Provenance

Originally forked from [Mathias Bynens'
dotfiles](https://github.com/mathiasbynens/dotfiles) — a long-running and
widely used macOS dotfiles project — and since rewritten around chezmoi with
per-machine templating. With thanks to Mathias, and to the wider dotfiles
community his repository drew on, for the foundations.

Upstream has seen little activity since 2024 but is still tracked for
reference:

```bash
git fetch upstream   # tracks https://github.com/mathiasbynens/dotfiles.git
```
