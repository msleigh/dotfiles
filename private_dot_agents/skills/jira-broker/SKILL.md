---
name: jira-broker
description: Query and update ECMWF Jira (Data Center) through a local broker CLI whose Personal Access Token stays on the machine and is never sent to the model. Use when Michael asks about Jira issues or tickets (e.g. IFS-1234), wants a JQL search, or wants to read, comment on, create, transition, or assign issues.
---

# Jira Broker

## Overview

This skill only loads guidance; it does not fetch anything itself. To read or
write Jira you must then run the broker CLI via Bash (see **Invocation**).

`jira-broker` is a small Bash CLI that talks to ECMWF Jira (`jira.ecmwf.int`,
Atlassian Data Center) over its REST API. It exists so an agent can work with
Jira **without ever handling the credential**: the Personal Access Token is read
from a local file at run time and passed to `curl` via a stdin config block, so
it never appears in command arguments, `ps`, shell history, logs, this public
repository, or anything sent to the model. Only the data you explicitly request
is returned.

Content of the issues you fetch *is* returned to the agent (that is the point of
reading them); only the token is kept local.

## Invocation

The executable is `scripts/jira-broker` inside this skill directory (deployed
copy: `~/.agents/skills/jira-broker/scripts/jira-broker`). Run it directly, e.g.:

```bash
scripts/jira-broker whoami
```

## Commands

Read:

- `jira-broker whoami` — confirm auth and show the current user.
- `jira-broker search "<JQL>" [max]` — search issues; output is TSV `key status assignee summary`.
- `jira-broker issue <KEY>` — show one issue with its description.
- `jira-broker comments <KEY>` — list comments on an issue.
- `jira-broker get <api-path>` — raw GET under `rest/api/2/` for anything not covered (e.g. `get project/IFS`).

Write (require `--yes`, only after the user confirms):

- `jira-broker --yes comment <KEY> <text>`
- `jira-broker --yes create <PROJECT> <TYPE> <SUMMARY> [DESCRIPTION]`
- `jira-broker --yes transition <KEY> <TRANSITION-NAME>`
- `jira-broker --yes assign <KEY> <USERNAME>`

## Agent guidance

- **Reads are safe**; run them freely to answer questions.
- **Writes are gated.** Every write command refuses to run without `--yes`.
  Always describe the exact change to the user and get explicit approval before
  adding `--yes`. Never pass `--yes` speculatively.
- Prefer `search` with a focused JQL over fetching many issues individually.
- For fields or endpoints the wrapper does not expose, use `get <api-path>` and
  parse the JSON.
- If a command reports "no PAT file" or "no base URL", the user needs to
  complete the one-time setup below — do not attempt to work around it.

## One-time setup (done by the user, not committed)

1. Base URL (already set by dotfiles):
   `~/.config/jira/config` contains `base_url=https://jira.ecmwf.int`.
2. Personal Access Token: create one in Jira (Profile → Personal Access Tokens),
   then save the raw token (no surrounding whitespace) to a local file and lock
   it down:

   ```bash
   printf '%s' '<token>' > ~/.config/jira/pat_$(hostname -s)
   chmod 600 ~/.config/jira/pat_*
   ```

   The broker reads `~/.config/jira/pat` or the first `pat_*` file it finds, or
   the path in `JIRA_PAT_FILE`. Never commit these files.
