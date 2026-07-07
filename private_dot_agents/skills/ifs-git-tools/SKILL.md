---
name: ifs-git-tools
description: Git commands for managing branches, worktrees, PRs, testing, and code quality in ECMWF IFS (Integrated Forecasting System) repositories
version: "1.0"
author: msleigh
tags:
  - git
  - ifs
  - worktree
  - pull-request
  - code-quality
  - norms
  - testing
  - branching
globs:
  - "**/ifs-bundle/**"
  - "**/ifs-defaults/**"
  - "**/ifs-nemo/**"
  - "**/ifs-scidoc/**"
  - "**/ifs-scripts/**"
  - "**/ifs-source/**"
  - "**/ifs-suites/**"
  - "**/ifs-citest/**"
  - "**/ifs-citest-framework/**"
triggers:
  - "git ifs"
  - "git ifsbranch"
  - "git ifscheck"
  - "git ifsdr"
  - "git echbranch"
  - "git ifsfindfiles"
  - "git ifsmvclone"
  - "git ifsnorms"
  - "git ifspr"
  - "git ifsremote"
  - "git ifsrm"
  - "git ifssetup"
  - "git ifstest"
  - "git ls"
  - "IFS branch"
  - "IFS pull request"
  - "IFS worktree"
  - "IFS coding norms"
  - "IFS testing"
  - "ifstest"
---

# IFS Git Tools — Agent Skill

You have access to the **ifs-git-tools** CLI package, a suite of Git commands for
working with the ECMWF IFS (Integrated Forecasting System) source code
repositories. Use these tools to manage branches, worktrees, pull requests,
testing, and code quality on behalf of the user.

## Usage Notice

Whenever you use this skill or any `git ifs*` command, prepend your response with:

> 🛠️ **Using skill: ifs-git-tools**

This lets the user know that your actions are informed by the ifs-git-tools skill.

---

## Activation

Before using any `git ifs*` command, ensure the tools are on `PATH`.
Detect the platform and activate accordingly:

### ECMWF HPC (hpc2020 / Atos)

```bash
module load ifs-git-tools
```

The `module` command is available on ECMWF HPC systems. You can detect this
platform by checking if the `module` command exists:

```bash
if command -v module &>/dev/null && module avail ifs-git-tools 2>&1 | grep -q ifs-git-tools; then
  module load ifs-git-tools
fi
```

### macOS / Personal Workstations

Export the PATH to the local clone of ifs-git-tools. The install location is
configurable via the environment variable `IFS_GIT_TOOLS_PATH` (defaults to
`~/projects/ifs-git-tools`):

```bash
IFS_GIT_TOOLS_PATH="${IFS_GIT_TOOLS_PATH:-$HOME/projects/ifs-git-tools}"
export PATH="${IFS_GIT_TOOLS_PATH}/bin:$PATH"
export MANPATH="${IFS_GIT_TOOLS_PATH}/man:${MANPATH:-}"
```

### Verifying Activation

After activation, confirm the tools are available:

```bash
command -v git-ifsbranch >/dev/null && echo "ifs-git-tools available" || echo "ifs-git-tools NOT found"
```

---

## IFS Repository Landscape

The IFS codebase is split across multiple repositories in the **ecmwf-ifs**
GitHub organization:

| Repository | Description |
|---|---|
| `ifs-bundle` | CMake bundle orchestrating all IFS repos |
| `ifs-defaults` | Default namelists and configuration |
| `ifs-nemo` | NEMO ocean model interface |
| `ifs-scidoc` | Scientific documentation |
| `ifs-scripts` | Build and job scripts |
| `ifs-source` | Core IFS Fortran source code |
| `ifs-suites` | ecFlow suite definitions |

Note: `ifs-test` existed as a separate repository on Bitbucket but was merged
into `ifs-source` at CY50R1 and does not exist on GitHub.

All tools default to GitHub (`github.com/ecmwf-ifs`). The central remote is
named `central`; the user's fork is `origin`.

Key branch names:
- `main` — production default branch
- `main_staging` — pre-release testing

---

## ECMWF Conventions

### Branch Naming

IFS branches follow this naming convention:

```
<user>_<cycle>_<descriptive-name>[.<Jira-issue>[...]]
```

- `<user>` — the developer's username (auto-detected)
- `<cycle>` — the IFS release cycle (e.g., `CY49R2`)
- `<descriptive-name>` — alphanumeric with `.`, `_`, `-` only
- `<Jira-issue>` — optional Jira ticket ID(s)

Example: `user_CY49R2_fix-radiation.IFS-1234`

### Worktree Workflow

IFS development uses **Git worktrees** — each branch gets its own directory on
disk rather than switching branches in a single clone. Worktree locations:

- **ECMWF HPC**: `$PERM/git/<repo>/<branch>/`
- **Elsewhere**: `$HOME/ifs-worktrees/git/<repo>/<branch>/`

The root is configurable via the `$IFSWORKTREEROOT` environment variable.

### Multi-Repository Operations

Many `git ifs*` commands can operate across multiple repositories simultaneously
using aliases configured by `git ifssetup`:

- `git source <cmd>` — run in ifs-source
- `git scripts <cmd>` — run in ifs-scripts
- `git suites <cmd>` — run in ifs-suites
- `git bndl <cmd>` — run in ifs-bundle (named `bndl` to avoid conflict with native `git bundle`)
- `git defaults <cmd>` — run in ifs-defaults
- `git nemo <cmd>` — run in ifs-nemo
- `git scidoc <cmd>` — run in ifs-scidoc
- `git main <cmd>` — run across bndl, defaults, nemo, scripts, source, suites
- `git both <cmd>` — run across scripts, source
- `git all <cmd>` — run across all 8 repositories (including ifs-test)
- `git some <repos> <cmd>` — run across specified repos (comma-separated)

---

## Command Reference

### git ifs

Package overview. Displays help about all available IFS Git Tools commands.

```bash
git ifs --help
```

---

### git ifsbranch

Create branches and worktrees following ECMWF naming conventions.

**Create a new branch from a parent:**
```bash
git ifsbranch -p <parent-branch> -n <descriptive-name> [-j <jira-issue>] [-J]
```

**Check out existing branches as worktrees:**
```bash
git ifsbranch <branch> [<branch>...]
```

| Option | Description |
|---|---|
| `-p, -B <parent>` | Parent branch to branch off (local, remote, or from added remotes) |
| `-n, -b <name>` | Descriptive name for the branch (alphanumeric, `.`, `_`, `-`) |
| `-c` | Create branch only (no worktree) |
| `-d` | Branch from the latest dot-release of a release cycle |
| `-f` | Force — skip confirmation prompts |
| `-j <issue>` | Jira issue ID (repeatable for multiple issues) |
| `-J` | Explicitly create without a Jira issue |
| `-v` | Verbose output |

**Examples:**
```bash
# Create a branch from CY49R2 main with a Jira ticket
git ifsbranch -p CY49R2 -n fix-convection -j IFS-5678

# Create branch without Jira issue
git ifsbranch -p main -n experiment-new-physics -J

# Check out an existing remote branch as a local worktree
git ifsbranch origin/user_CY49R2_fix-convection.IFS-5678
```

**Agent guidance:**
- Always ask the user for the parent branch and descriptive name if not provided.
- Always ask whether to attach a Jira issue; use `-J` only if the user explicitly declines.
- The `-d` flag is useful when the user says "branch from the latest CY49R2".

---

### git ifscheck

Check if a branch is behind its originating release cycle.

```bash
git ifscheck [-q] [-r <cycle>] [<branch>...]
```

| Option | Description |
|---|---|
| `-q` | Quiet — show only commit hashes |
| `-r <cycle>` | Specify reference cycle explicitly (overrides auto-detection) |

With no arguments, checks the current branch.

**Example:**
```bash
# Check if my branch needs rebasing
git ifscheck

# Check a specific branch against a specific cycle
git ifscheck -r CY49R2 user_CY49R2_fix-convection.IFS-5678
```

**Agent guidance:**
- Run this before starting a rebase to inform the user what's behind.
- If the output is empty, the branch is up to date.

---

### git ifsdr

Set up and repair a development repository (GitHub fork configuration, rulesets,
remotes, permissions, hooks).

```bash
git ifsdr [-v] [-w | -W]
```

| Option | Description |
|---|---|
| `-v` | Verbose output |
| `-w` | Enable worktree repair (repair from clone, repair individual worktrees, set worktree parent permissions) |
| `-W` | Enable worktree repair (as `-w`) PLUS set permissions on all worktrees (slow) |

**What it does:**
1. Sets GitHub fork default branch to `main`
2. Adds IFS team as collaborator on the fork
3. Sets repository rulesets on the fork
4. Sets `central` remote pointing to ecmwf-ifs
5. Fetches `main` branch
6. Sets clone default branch to `main`
7. Deletes official/managed branches from fork and clone
8. Sets clone permissions
9. Sets path permissions
10. Sets Git hooks
11. Optionally handles Bitbucket migration (if upgraded clone detected)
12. Optionally repairs worktrees and sets permissions (with `-w`/`-W`)

**Agent guidance:**
- This is run once per repository fork for initial setup, but also serves as a repair/fixer tool that can be re-run safely.
- Use `-w` when worktree paths need repairing; use `-W` for a thorough permissions fix across all worktrees (slow).

---

### git ifsmvclone

Safely move a clone to a new filesystem location, updating all internal
references and worktree metadata.

```bash
git ifsmvclone [-f] [-w] -n <new-path> [-o <old-path>] [<repository>...]
```

| Option | Description |
|---|---|
| `-f` | Force — skip confirmation |
| `-n <path>` | New location (required) |
| `-o <path>` | Old location (if not auto-detected) |
| `-w` | Skip worktree metadata updates |

**Agent guidance:**
- This is a potentially disruptive operation. Always confirm the new path with the user.
- Without `-w`, worktree paths are also updated — this is usually what you want.

---

### git ifsnorms

Check IFS source code against ECMWF coding standards.

```bash
git ifsnorms [-c <commit-ish>] [-f] [-g] [-i] [-m <suppress>] [-n <ignore>] \
             [-p <project>] [-s <whitelist>] [-v] [-w] [-x] [<branch>...]
```

| Option | Description |
|---|---|
| `-c <commit>` | Commit to check against |
| `-f` | Use fork point as reference |
| `-g` | Generate whitelist file |
| `-i` | Generate information messages (normally suppressed) |
| `-m <list>` | Suppress specific warnings |
| `-n <list>` | Ignore specific file patterns |
| `-p <project>` | Project name (default: `arpifs`; automatically set to `ifs` for pre-CY48R1 branches) |
| `-s <file>` | Custom whitelist file |
| `-v` | Verbose |
| `-w` | Suppress warning messages (normally enabled) |
| `-x` | Test mode |

**Examples:**
```bash
# Check norms on current branch
git ifsnorms

# Check with information messages enabled
git ifsnorms -i

# Generate a whitelist for approved violations
git ifsnorms -g
```

**Agent guidance:**
- This is typically run on HPC systems where the norm-checking tools (icheck, wcheck, fcm) are available.
- If running on macOS and the command fails, inform the user that norms checking requires the HPC environment.

---

### git ifspr

Create and list GitHub Pull Requests for IFS repositories.

**Create a PR:**
```bash
git ifspr -t <title> [-a <assignees>] [-d] [-m <description>] [-n] [-r <reviewers>] \
          [-R <repos>] [-T <target>] [-w] [[-S] <source>]
```

**List PRs:**
```bash
git ifspr -l [-a <assignees>] [-A <author>] [-R <repos>] [-s <state>] \
           [-T <target>] [[-S] <source>]
```

| Option | Description |
|---|---|
| `-t <title>` | PR title (required for create) |
| `-l` | List mode |
| `-a <assignees>` | Comma-separated assignees (ECMWF or GitHub usernames) |
| `-A <author>` | Filter by author (list mode) |
| `-b` | Bitbucket compatibility mode |
| `-d` | Create as draft PR; in list mode, list only draft PRs |
| `-m <desc>` | PR body/description |
| `-n` | Dry run — show what would be done without creating the PR |
| `-r <reviewers>` | Comma-separated reviewers |
| `-R <repos>` | Target repositories (comma-separated) |
| `-s <state>` | Filter by state (`open`, `closed`, `merged`, `all`) |
| `-S <source>` | Source branch |
| `-T <target>` | Target branch (default: `main_staging`) |
| `-w` | Open in web browser after creation |

**Examples:**
```bash
# Create a PR to main_staging (the default target)
git ifspr -t "Fix convection parameterization" -m "Resolves IFS-5678" -r reviewer1,reviewer2

# Create a draft PR targeting a release cycle
git ifspr -t "WIP: New physics" -d -T CY49R2

# List open PRs by a specific author
git ifspr -l -A user -s open

# List PRs across multiple repos
git ifspr -l -R ifs-source,ifs-scripts
```

**Agent guidance:**
- The tool translates ECMWF usernames to GitHub usernames automatically.
- Always ask the user for a PR title and target branch if not provided.
- Use `-d` (draft) when the user indicates work is in progress.
- Jira issue IDs are automatically extracted from branch names for the PR description.

---

### git ifsremote

Add and manage remotes for IFS repositories.

```bash
git ifsremote [-b | -c | -g] [-f] [-n | -N] [-p] [-q] [-r] <user-or-remote>
```

| Option | Description |
|---|---|
| `-b` | Source from Bitbucket (`bb-` prefix remote) |
| `-c` | Source from clone (`cl-` prefix remote, for local Atos clones) |
| `-g` | Source from GitHub (default) |
| `-f` | Force — overwrite existing remote |
| `-n` | Exclude tags from fetch |
| `-N` | No fetch (add remote only) |
| `-p` | Print remote URL only (don't fetch) |
| `-q` | Quiet |
| `-r` | Print remote name only |

**Examples:**
```bash
# Add a colleague's fork as a remote (from GitHub)
git ifsremote colleague_username

# Add a colleague's clone remote (Atos local clones)
git ifsremote -c colleague_username

# Just print the URL without fetching
git ifsremote -p colleague_username
```

---

### git ifsrm

Delete branches, worktrees, and builds.

```bash
git ifsrm [-b] [-f] [-l] [-r] [-w] <branch> [<branch>...]
```

| Option | Description |
|---|---|
| `-b` | Delete build only |
| `-f` | Force — skip confirmation |
| `-l` | Delete local branch |
| `-r` | Delete remote branch |
| `-w` | Delete worktree only |
| (none) | Delete everything (local branch, remote branch, worktree, and build) |

**Examples:**
```bash
# Delete a branch and all associated worktrees/builds
git ifsrm user_CY49R2_fix-convection.IFS-5678

# Delete only the worktree (keep the branch)
git ifsrm -w user_CY49R2_fix-convection.IFS-5678

# Delete the remote branch too
git ifsrm -r user_CY49R2_fix-convection.IFS-5678
```

**Agent guidance:**
- **This is a destructive operation.** Always confirm with the user before running.
- Never use `-f` unless the user explicitly requests it.
- Inform the user what will be deleted (branch, worktree, and/or build).

---

### git ifssetup

Initial setup for the IFS Git workflow: SSH keys, GitHub authentication,
configuration, and repository forking/cloning.

```bash
git ifssetup [-f | -i] [-s [-l]] [-c] [-g] [-x] [<repo>...]
```

| Option | Description |
|---|---|
| `-f` | Force mode — accept all defaults, no prompts |
| `-i` | Interactive mode (default) — prompt for each setting |
| `-s` | Add SSH key and login to GitHub |
| `-l` | Logout before re-login (with `-s`) |
| `-c` | Deprecated (was curl config); now triggers `-s` |
| `-g` | Git configuration (user details, aliases, SSH settings) |
| `-x` | Fork and clone repositories |

**Setup steps** (if no flags given, all steps run):
1. SSH key setup and GitHub login (`-s`)
2. Git configuration — user details, aliases, SSH settings (`-g`)
3. Repository forking and cloning (`-x`)

**Examples:**
```bash
# Full interactive setup
git ifssetup

# Just set up SSH and GitHub login
git ifssetup -s

# Fork and clone specific repos only
git ifssetup -x ifs-source ifs-scripts
```

**Agent guidance:**
- This is interactive by default. When running on behalf of a user, prefer `-i` (interactive) so the user can confirm choices.
- Running with `-f` skips all prompts — only use if the user explicitly asks.
- If the user is new to IFS development, run the full setup without flags.

---

### git ifstest

Execute IFS compilation and QA test suite.

**Configure dependencies:**
```bash
git ifstest -c [-j <threads>] [-B <bundle-branch>] [-E <test-branch>] \
            [-N <nemo-branch>] [-S <source-branch>] [<worktree>...]
```

**Build:**
```bash
git ifstest -b [-i] [-I] [-j <threads>] [-m <mem>] [-d <build>...] [-p] [-r] \
            [-S <source-branch>] [<worktree>...]
```

**Test:**
```bash
git ifstest -t [-i] [-I] [-j <threads>] [-M <mem>] [-d <build>...] \
            [-L <pattern>] [-R <pattern>] [-x <pattern>] [-X <pattern>] \
            [-S <source-branch>] [<worktree>...]
```

**Other:**
```bash
git ifstest -b -D [-S <source-branch>] [<worktree>...]   # List build directories
git ifstest -b -r [-S <source-branch>] [<worktree>...]   # Remove/clean existing build
git ifstest -t -l [-S <source-branch>] [<worktree>...]   # List tests
```

| Option | Description |
|---|---|
| `-c` | Configure step |
| `-b` | Build step |
| `-t` | Test step |
| `-D` | List build directories (with `-b`) |
| `-G` | Find most recent tag in ifs-source history and use matching ifs-bundle tag |
| `-l` | List available tests (with `-t`) |
| `-i` | Interactive mode |
| `-I` | Force non-interactive |
| `-j <n>` | Number of parallel threads |
| `-m, -M <mem>` | Memory limit |
| `-d <build>` | Specific build(s) (repeatable) |
| `-B <branch>` | ifs-bundle branch |
| `-E <branch>` | ifs-test branch (deprecated at CY50R1; ifs-test merged into ifs-source) |
| `-N <branch>` | ifs-nemo branch |
| `-S <branch>` | ifs-source branch |
| `-L <pattern>` | Run tests matching label pattern |
| `-R <pattern>` | Run tests matching name pattern |
| `-x <pattern>` | Exclude tests matching name pattern |
| `-X <pattern>` | Exclude tests matching label pattern |
| `-p` | Preserve command-line build arguments for incremental builds |
| `-r` | Remove/clean existing build (with `-b`) |

**Typical workflow:**
```bash
# 1. Configure, build, and test in one command (flags can be combined)
git ifstest -cbt -j 8

# Or run steps separately:

# 1. Configure
git ifstest -c

# 2. Build
git ifstest -b -j 8

# 3. List available tests
git ifstest -t -l

# 4. Run all tests
git ifstest -t -j 4
```

**Agent guidance:**
- The configure → build → test sequence is the standard workflow. Always run them in order.
- This is primarily an HPC command. Building IFS requires HPC resources and compilers.
- Use `-j` to control parallelism; typical values are 4–16 on HPC.
- If running interactively on HPC, the tool auto-detects SLURM allocation.

---

### git ls

Enhanced `ls -l` showing Git commit information alongside file metadata.

```bash
git ls
```

**Output columns:** permissions, committer name, size, timestamp, filename,
commit message, git status.

No options — run it in any Git repository.

---

### git echbranch

Create branches and Jira issues for the **echydro** repository (hydrology group).

```bash
git echbranch [-x] [-p <parent>] [-j <jira-issue>] [-e <efas-issue>] \
              [-l] [-f <fields>] <descriptive-name>
```

Branch naming format:
```
[feature|hotfix]/<user>_<descriptive_name>.<jira-issue>
```

| Option | Description |
|---|---|
| `-p <parent>` | Parent branch (default: `develop`) |
| `-x` | Create a hotfix branch (prefix `hotfix/` instead of `feature/`) |
| `-j <issue>` | Use an existing Jira issue instead of creating a new one |
| `-e <issue>` | Link an EFAS-COMS Jira issue |
| `-l` | List available Jira fields |
| `-f <fields>` | Extra Jira fields to set |

**Examples:**
```bash
# Create a feature branch with a new Jira issue
git echbranch fix-river-routing

# Create a hotfix branch with an existing Jira issue
git echbranch -x -j ECHYDRO-123 urgent-fix

# Branch from a specific parent
git echbranch -p main new-feature
```

**Agent guidance:**
- This is specific to the echydro repository; do not use it for IFS repos.
- By default creates a `feature/` branch from `develop`; use `-x` for `hotfix/` branches.

---

### git ifsfindfiles

List files added, modified, or deleted in an IFS Git branch (compared to a
reference cycle). Optionally produces LaTeX-formatted output for FLUB
documentation.

```bash
git ifsfindfiles [-l] [-o] [-q] [-r <cycle>] [-s] [<branch>...]
```

| Option | Description |
|---|---|
| `-l` | LaTeX output (for FLUB documentation) |
| `-o` | Local only — do not fetch from remote |
| `-q` | Quiet |
| `-r <cycle>` | Reference cycle (overrides auto-detection) |
| `-s` | Short output (file names only) |

**Examples:**
```bash
# List changed files on the current branch
git ifsfindfiles

# List changes relative to a specific cycle
git ifsfindfiles -r CY49R2

# Generate LaTeX output for documentation
git ifsfindfiles -l
```

---

## Common Workflows

### Starting a New Feature

```bash
# 1. Ensure tools are loaded
module load ifs-git-tools   # HPC
# or
export PATH=~/projects/ifs-git-tools/bin:$PATH   # macOS

# 2. Create a branch with Jira issue
git source ifsbranch -p CY49R2 -n my-feature -j IFS-1234

# 3. Work on the code in the worktree
cd $IFSWORKTREEROOT/ifs-source/user_CY49R2_my-feature.IFS-1234/

# 4. Check norms
git ifsnorms

# 5. Build and test (HPC)
git ifstest -c && git ifstest -b -j 8 && git ifstest -t

# 6. Create PR
git ifspr -t "My feature" -m "Description" -r reviewer1
```

### Checking Branch Status

```bash
# Check if branch needs rebasing
git ifscheck

# List open PRs
git ifspr -l -s open
```

### Cleanup

```bash
# Delete a merged branch and its worktree
git ifsrm user_CY49R2_my-feature.IFS-1234
```

---

## Safety Rules

1. **Never create branches manually.** Do not use `git branch` or `git checkout -b`
   to create IFS branches. Always use `git ifsbranch`, which enforces the IFS
   naming convention (`<user>_<cycle>_<name>[.<jira>]`) and sets up the
   corresponding worktree automatically. Manual branch names will violate
   conventions and cause problems with other IFS tools.
2. **Destructive operations** (`git ifsrm`, `-f` flags): Always confirm with the
   user before executing. Never use force flags autonomously.
3. **Setup operations** (`git ifssetup`, `git ifsdr`): These modify user
   configuration and GitHub settings. Always inform the user what will change.
4. **Credentials**: Never store, display, or transmit GitHub tokens, SSH keys, or
   Jira tokens. These are managed by `git ifssetup` in standard locations.
5. **HPC-only commands**: `git ifstest` and `git ifsnorms` (with `-i`/`-w`)
   require HPC resources. If running on macOS, inform the user that these commands
   need the HPC environment.
6. **Multi-repo operations**: Commands using `git all`, `git main`, etc. affect
   multiple repositories simultaneously. Confirm the scope with the user.
