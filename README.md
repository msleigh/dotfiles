# dotfiles

Personal dotfiles, forked from [mathiasbynens/dotfiles](https://github.com/mathiasbynens/dotfiles) and adapted for use across multiple machines. Managed with [chezmoi](https://www.chezmoi.io/).

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

This deploys all dotfiles to `$HOME`, rendering any machine-specific templates for the declared machine. To preview changes before applying:

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

Create `~/.extra` for anything that shouldn't be committed: API tokens, `git config user.email`, machine-specific aliases, etc. It is sourced by `~/.bash_profile` after all other dotfiles.

## Secret scanning

This repo is public, so commits are scanned for secrets with [gitleaks](https://github.com/gitleaks/gitleaks) via a [pre-commit](https://pre-commit.com/) hook (`.pre-commit-config.yaml`). pre-commit manages its own pinned gitleaks binary, so no separate gitleaks install is required.

After cloning, arm the hook once:

```bash
pre-commit install
```

Run it manually across all files at any time:

```bash
pre-commit run --all-files
```

The config is excluded from deployment in `.chezmoiignore`, so it stays in the repo and is never written to `$HOME`.

## Structure

Machine-specific differences are handled via Go templates rather than branches. Six files are templated (`dot_path.tmpl`, `dot_bash_profile.tmpl`, `dot_exports.tmpl`, `dot_aliases.tmpl`, `dot_gitconfig.tmpl`, `executable_brew.sh.tmpl`); the rest are plain files renamed with chezmoi's `dot_` prefix convention. See `AGENTS.md` for full architecture details.

## Upstream

```bash
git fetch upstream
```

Remote `upstream` tracks `https://github.com/mathiasbynens/dotfiles.git`.

## Thanks to…

* @ptb and [his _macOS Setup_ repository](https://github.com/ptb/mac-setup)
* [Ben Alman](http://benalman.com/) and his [dotfiles repository](https://github.com/cowboy/dotfiles)
* [Cătălin Mariș](https://github.com/alrra) and his [dotfiles repository](https://github.com/alrra/dotfiles)
* [Gianni Chiappetta](https://butt.zone/) for sharing his [amazing collection of dotfiles](https://github.com/gf3/dotfiles)
* [Jan Moesen](http://jan.moesen.nu/) and his [ancient `.bash_profile`](https://gist.github.com/1156154) + [shiny _tilde_ repository](https://github.com/janmoesen/tilde)
* [Matijs Brinkhuis](https://matijs.brinkhu.is/) and his [dotfiles repository](https://github.com/matijs/dotfiles)
* [Nicolas Gallagher](http://nicolasgallagher.com/) and his [dotfiles repository](https://github.com/necolas/dotfiles)
* [Sindre Sorhus](https://sindresorhus.com/)
* [Tom Ryder](https://sanctum.geek.nz/) and his [dotfiles repository](https://sanctum.geek.nz/cgit/dotfiles.git/about)
* [Kevin Suttle](http://kevinsuttle.com/) and his [dotfiles repository](https://github.com/kevinSuttle/dotfiles) and [macOS-Defaults project](https://github.com/kevinSuttle/macOS-Defaults)
* [Haralan Dobrev](https://hkdobrev.com/)
* Anyone who [contributed a patch](https://github.com/mathiasbynens/dotfiles/contributors) or [made a helpful suggestion](https://github.com/mathiasbynens/dotfiles/issues)
