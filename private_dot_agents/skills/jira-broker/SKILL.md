---
name: jira-broker
description: Query and update ECMWF Jira (Data Center) through a local broker CLI whose Personal Access Token stays on the machine and is never sent to the model. Use when the user asks about Jira issues or tickets (e.g. IFS-1234), wants a JQL search, or wants to read, comment on, create, transition, or assign issues, or edit their description or fields such as Fix Version, Affects Version, Component, Labels, or IFS Parts Affected.
---

# Jira Broker

## Overview

This skill only loads guidance; it does not fetch anything itself. To read or
write Jira you must then run the broker CLI via Bash (see **Invocation**).

`jira-broker` is a small Bash CLI that talks to ECMWF Jira (`jira.ecmwf.int`,
Atlassian Data Center) over its REST API. It exists so an agent can work with
Jira **without ever handling the credential**: the Personal Access Token is read
from a local file at run time and passed to `curl` via a stdin config block, so
it never appears in command arguments, `ps`, shell history, logs, source
control, or anything sent to the model. Only the data you explicitly request is
returned.

Content of the issues you fetch *is* returned to the agent (that is the point of
reading them); only the token is kept local.

## Invocation

The executable is `scripts/jira-broker` inside this skill directory. Run it by
its full path, e.g.:

```bash
<skill-dir>/scripts/jira-broker whoami
```

It requires `bash`, `curl` (7.76 or later), and `jq`.

## Commands

Read:

- `jira-broker whoami` — confirm auth and show the current user.
- `jira-broker search "<JQL>" [max]` — search issues; output is TSV `key status assignee summary`.
- `jira-broker issue <KEY>` — show one issue with its components, versions, and
  description.
- `jira-broker comments <KEY>` — list comments on an issue.
- `jira-broker fields <KEY> [FIELD]` — list the fields editable on an issue (TSV
  `id name type operations`), or, given a field, its allowed values.
- `jira-broker get <api-path>` — raw GET under `rest/api/2/` for anything not covered (e.g. `get project/IFS`).

Write (require `--yes`, only after the user confirms):

- `jira-broker --yes comment <KEY> <text>`
- `jira-broker --yes create <PROJECT> <TYPE> <SUMMARY> [DESCRIPTION]`
- `jira-broker --yes set-description <KEY> <text|->` — replace the description;
  `-` reads it from stdin (use a heredoc for multi-line text).
- `jira-broker --yes edit <KEY> <FIELD> <set|add|remove|clear> [VALUE[,VALUE...]]`
  — edit a field. `set` replaces all values, `add` and `remove` change only
  the values given, and `clear` empties the field. Multi-value fields take a
  comma-separated list; single-value fields take the value as-is.
- `jira-broker --yes transition <KEY> <TRANSITION-NAME>`
- `jira-broker --yes assign <KEY> <USERNAME>`

`FIELD` may be a field ID (`fixVersions`, `customfield_12111`), a display name
(`'Fix Version/s'`), or one of these aliases: `fix`, `affects`, `components`,
`labels`, `parts` (IFS Parts Affected), `epic` (Epic Link: `set` takes the
epic's key, `clear` removes the issue from its epic). For example:

```bash
jira-broker --yes edit IFS-1234 fix add CY51R1
jira-broker --yes edit IFS-1234 affects set 'CY50R1,CY50R2'
jira-broker --yes edit IFS-1234 parts remove ifs-scripts
jira-broker --yes edit FORGE-123 epic set FORGE-45
```

Issue creation accepts comma-separated field values through
`JIRA_COMPONENTS`, `JIRA_FIX_VERSIONS`, and `JIRA_IFS_PARTS_AFFECTED`.
For example:

```bash
JIRA_COMPONENTS='Forecast' \
JIRA_FIX_VERSIONS='Cy50r1' \
JIRA_IFS_PARTS_AFFECTED='Dynamics,Physics' \
  jira-broker --yes create IFS Task 'Summary' 'Description'
```

Epics also need an Epic Name. It defaults to the summary; set
`JIRA_EPIC_NAME` to use a shorter name:

```bash
JIRA_EPIC_NAME='Code pruning' \
  jira-broker --yes create FORGE Epic 'Code pruning: workflow code' 'Description'
```

## Agent guidance

- **Reads are safe**; run them freely to answer questions.
- **Writes are gated.** Every write command refuses to run without `--yes`.
  Always describe the exact change to the user and get explicit approval before
  adding `--yes`. Never pass `--yes` speculatively.
- Prefer `search` with a focused JQL over fetching many issues individually.
- `set-description` replaces the whole description. To edit part of it, fetch
  the current text exactly with
  `get 'issue/<KEY>?fields=description' | jq -r .fields.description`, make the
  change, show the user the result (or a diff), and then write back the full
  text. Descriptions use Jira wiki markup, not Markdown.
- `edit` checks the field and values against the issue's edit screen before
  the `--yes` gate, so running it without `--yes` is a safe way to validate a
  change. Version names are case-sensitive (IFS uses e.g. `CY50R2`); check with
  `fields <KEY> fix`. Prefer `add`/`remove` over `set` so other values are kept.
- A field missing from `fields <KEY>` is not on that issue's edit screen. In the
  IFS project, for example, Affects Version/s is editable on Bugs only.
- IFS tickets require **Component**, **Fix Version**, and **IFS Parts Affected**.
  Before proposing or creating one, determine all three values and pass them via
  `JIRA_COMPONENTS`, `JIRA_FIX_VERSIONS`, and `JIRA_IFS_PARTS_AFFECTED`.
- For fields or endpoints the wrapper does not expose, use `get <api-path>` and
  parse the JSON.
- If a command reports "no PAT file", or a request fails with `401
  Unauthorized`, the user needs to complete (or redo) the one-time setup below
  — the token is missing, wrong, or expired. Do not attempt to work around it,
  and never ask the user to paste the token into the conversation.

## One-time setup (done by the user, not committed)

1. Create a Personal Access Token in Jira: click your avatar (top right) →
   **Profile** → **Personal Access Tokens** → **Create token**. Give it a name
   and an expiry date, click **Create**, and copy the token straight away — it
   is shown only once.
2. Save it. This prompts for the token without echoing it or recording it in
   shell history, and creates the file readable only by you (works in bash and
   zsh):

   ```bash
   mkdir -p ~/.config/jira
   (umask 077; printf 'Paste Jira token: '; read -rs t; printf '%s' "${t}" > ~/.config/jira/pat); echo
   ```

   The broker reads `~/.config/jira/pat` or the first `pat_*` file it finds, or
   the path in `JIRA_PAT_FILE`. Never commit these files.
3. Check it: `<skill-dir>/scripts/jira-broker whoami` should print your name.
   When the token expires, create a new one and repeat step 2.
4. Base URL (optional): defaults to `https://jira.ecmwf.int`. To use another
   instance, set `JIRA_BASE_URL` or add `base_url=<url>` to
   `~/.config/jira/config`.
