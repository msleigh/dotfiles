---
name: confluence-broker
description: Read and edit ECMWF Confluence (Data Center) through a local broker CLI whose Personal Access Token stays on the machine and is never sent to the model. Use when the user asks to search the ECMWF wiki/Confluence, read a page, or create, update, or comment on Confluence pages.
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
history, logs, source control, or anything sent to the model. Only the data you
explicitly request is returned.

Page content you fetch *is* returned to the agent (that is the point of reading
it); only the token is kept local.

## Invocation

The executable is `scripts/confluence-broker` inside this skill directory. Run
it by its full path, e.g.:

```bash
<skill-dir>/scripts/confluence-broker whoami
```

It requires `bash`, `curl` (7.76 or later), and `jq`.

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
- If a command reports "no PAT file" or "token not accepted", or a request
  fails with `401 Unauthorized`, the user needs to complete (or redo) the
  one-time setup below — the token is missing, wrong, or expired. Do not
  attempt to work around it, and never ask the user to paste the token into the
  conversation.
- Confluence does not reject a bad token: it answers as an anonymous user, so
  reads may succeed but return only public content. If results look
  unexpectedly sparse, run `whoami` first.

## One-time setup (done by the user, not committed)

1. Create a Personal Access Token in Confluence: click your avatar (top right)
   → **Settings** → **Personal Access Tokens** → **Create token**. Give it a
   name and an expiry date, click **Create**, and copy the token straight away
   — it is shown only once.
2. Save it. This prompts for the token without echoing it or recording it in
   shell history, and creates the file readable only by you (works in bash and
   zsh):

   ```bash
   mkdir -p ~/.config/confluence
   (umask 077; printf 'Paste Confluence token: '; read -rs t; printf '%s' "${t}" > ~/.config/confluence/pat); echo
   ```

   The broker reads `~/.config/confluence/pat` or the first `pat_*` file it
   finds, or the path in `CONFLUENCE_PAT_FILE`. Never commit these files.
3. Check it: `<skill-dir>/scripts/confluence-broker whoami` should print your
   name. When the token expires, create a new one and repeat step 2.
4. Base URL (optional): defaults to `https://confluence.ecmwf.int`. To use
   another instance, set `CONFLUENCE_BASE_URL` or add `base_url=<url>` to
   `~/.config/confluence/config`.
