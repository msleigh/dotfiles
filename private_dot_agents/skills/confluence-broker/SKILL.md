---
name: confluence-broker
description: Read and edit ECMWF Confluence (Data Center) through a local broker CLI whose Personal Access Token stays on the machine and is never sent to the model. Use when Michael asks to search the ECMWF wiki/Confluence, read a page, or create, update, or comment on Confluence pages.
---

# Confluence Broker

## Overview

This skill only loads guidance; it does not fetch anything itself. To read or
write Confluence you must then run the broker CLI via Bash (see **Invocation**).

`confluence-broker` is a small Bash CLI that talks to ECMWF Confluence
(`confluence.ecmwf.int`, Atlassian Data Center) over its REST API. It exists so
an agent can work with Confluence **without ever handling the credential**: the
Personal Access Token is read from a local file at run time and passed to `curl`
via a stdin config block, so it never appears in command arguments, `ps`, shell
history, logs, this public repository, or anything sent to the model. Only the
data you explicitly request is returned.

Page content you fetch *is* returned to the agent (that is the point of reading
it); only the token is kept local.

## Invocation

The executable is `scripts/confluence-broker` inside this skill directory
(deployed copy: `~/.agents/skills/confluence-broker/scripts/confluence-broker`).
Run it directly, e.g.:

```bash
scripts/confluence-broker whoami
```

## Commands

Read:

- `confluence-broker whoami` — confirm auth and show the current user.
- `confluence-broker search "<CQL>" [limit]` — search content; output is TSV `id type space title`.
- `confluence-broker page <ID>` — show a page: metadata plus its storage-format (XHTML) body.
- `confluence-broker find <SPACE> <TITLE>` — fetch a page by space key and exact title.
- `confluence-broker children <ID>` — list child pages; output is TSV `id title`.
- `confluence-broker get <api-path>` — raw GET under `rest/api/` for anything not covered (e.g. `get space/DOCS`).

Write (require `--yes`, only after the user confirms). The body argument may be a
literal string, a path to a file, or `-` to read from stdin, and must be
Confluence **storage format** (XHTML):

- `confluence-broker --yes create <SPACE> <TITLE> <body|file|-> [PARENT-ID]`
- `confluence-broker --yes update <ID> <body|file|->`
- `confluence-broker --yes comment <ID> <text>`

## Agent guidance

- **Reads are safe**; run them freely to answer questions.
- **Writes are gated.** Every write command refuses to run without `--yes`.
  Always show the user the exact page/space/title and the body you intend to
  write, and get explicit approval before adding `--yes`. Never pass `--yes`
  speculatively.
- Page bodies are Confluence storage format (XHTML), not Markdown. Write valid
  storage markup (e.g. `<p>…</p>`, `<h2>…</h2>`, `<ac:…>` macros). For anything
  non-trivial, put the body in a file and pass its path.
- `update` fetches the current version and increments it automatically; do not
  try to set the version yourself.
- To locate a page, prefer `search` (CQL) or `find <SPACE> <TITLE>` before
  fetching by ID.
- If a command reports "no PAT file" or "no base URL", the user needs to
  complete the one-time setup below — do not attempt to work around it.

## One-time setup (done by the user, not committed)

1. Base URL (already set by dotfiles):
   `~/.config/confluence/config` contains `base_url=https://confluence.ecmwf.int`.
2. Personal Access Token: create one in Confluence (Profile → Settings →
   Personal Access Tokens), then save the raw token (no surrounding whitespace)
   to a local file and lock it down:

   ```bash
   printf '%s' '<token>' > ~/.config/confluence/pat_$(hostname -s)
   chmod 600 ~/.config/confluence/pat_*
   ```

   The broker reads `~/.config/confluence/pat` or the first `pat_*` file it
   finds, or the path in `CONFLUENCE_PAT_FILE`. Never commit these files.
