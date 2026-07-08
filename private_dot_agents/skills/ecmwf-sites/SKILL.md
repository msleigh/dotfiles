---
name: ecmwf-sites
description: Manage websites on the ECMWF Sites service (sites.ecmwf.int) through the official `sitesctl` command-line tool. Use when Michael asks to create, list, or delete an ECMWF site, upload/download/list/delete site content, publish charts or HTML to a site, manage a site's sharing/access, or work with site tokens and signed URLs. Site tokens stay in a local config file and are never passed inline or echoed to the model.
---

# ECMWF Sites

## Overview

This skill only loads guidance; it does not do anything itself. To manage a site
you must then run the `sitesctl` CLI via Bash (see [Command reference](#command-reference)).

**ECMWF Sites** (`sites.ecmwf.int`) is a "websites as a service" platform for
ECMWF staff and visiting scientists. A site is a bucket of files served at a URL
like `https://sites.ecmwf.int/<space>/<name>/`. HTML files render as web pages;
a directory serves its `index.html`, or a file listing if none exists. Sites can
be public or restricted to named users and groups.

This skill drives the platform through the **official `sitesctl` CLI**, which is
the scriptable, agent-friendly interface. The web hub at
`https://sites.ecmwf.int/hub/list/` does the same things through a browser; use
it only for interactive setup steps the CLI cannot do (e.g. first login).

Full upstream reference: `https://sites.ecmwf.int/docs/sites/cli/`. When a flag
or subcommand is not covered here, run the relevant `... --help` rather than
guessing.

## Credentials — the one rule that matters

Two kinds of secret exist:

- **Master Token / HTTP Access Token** — per-site, authorises content and
  admin operations on one site.
- **Hub credentials** — your ECMWF login, needed to *create*, *delete*, or
  *list* sites you own.

Keep every secret out of the model's view. In practice:

- **Never pass a token inline.** Do not run `sitesctl ... --token <value>` with a
  literal token, and never write a token into a file, a command argument, or the
  conversation. Inline tokens leak into the transcript, `ps`, and shell history.
- **Rely on the stored per-site token instead.** `sitesctl` reads a token saved
  in `~/.sites-cli` for each `<space>/<name>`, so content and admin commands run
  with no `--token` flag at all. Setting that token is a one-time user action
  (see [Setup](#one-time-setup-done-by-the-user)) — you don't need to see it.
- **Do not run commands that print secrets.** `master-token show`,
  `master-token rotate`, and `access-token create` emit a token to stdout, which
  would then sit in the transcript. If Michael needs one of these, ask him to
  run it himself with the `!` prefix so the output stays in his session, not the
  model's.
- **`auth login` is interactive** (it prompts for a password). Ask Michael to
  run it himself; don't attempt to script credential entry.

## Prerequisites

`sitesctl` is not installed by default. Check first:

```bash
command -v sitesctl
```

If missing, install the latest build for the platform (from
`https://get.ecmwf.int/service/rest/repository/browse/sites-cli/`). On Linux,
e.g. ATOS HPCF:

```bash
curl -o ~/bin/sitesctl -L "https://get.ecmwf.int/service/rest/v1/search/assets/download?sort=name&direction=desc&q=linux&repository=sites-cli"
chmod +x ~/bin/sitesctl
```

Pick `q=macos`/`q=darwin` on a Mac. Confirm `~/bin` is on `PATH`.

## Command reference

Content and site-admin commands take `--space <space> --name <name>` to identify
the site, and use the token stored in `~/.sites-cli` (no `--token` flag).
Global flags include `-o/--output {table,json,yaml}` for machine-readable output
and `-f/--force` to skip confirmation prompts.

### Discover sites (needs hub login)

```bash
sitesctl list                 # sites you can access
sitesctl list health          # operational status
sitesctl auth whoami          # who am I logged in as
```

### Content operations (safe reads / gated writes)

```bash
# List — safe, run freely
sitesctl site --space <space> --name <name> content list --path / --recursive

# Upload — WRITE, confirm first
sitesctl site --space <space> --name <name> content upload --source ./public --recursive

# Download — pulls remote files locally
sitesctl site --space <space> --name <name> content download --path <remote> --destination <local>

# Delete — WRITE, confirm first
sitesctl site --space <space> --name <name> content delete --path <remote-path>

# Integrity check
sitesctl site --space <space> --name <name> content checksum --path <remote-path>
```

Uploading an `index.html` at a directory turns it into that directory's landing
page. Confirm the exact `--source`/`--path` with Michael before any upload or
delete, and show what will change.

### Create / delete a site (needs hub login)

```bash
sitesctl create --name <name> --template <type> --quota <GB>   # quota defaults low (1 GB) — set it deliberately
sitesctl delete --space <space> --name <name>
```

Creating and deleting sites are high-impact; always confirm before running, and
treat `delete` as irreversible.

### Sharing / access control

Access is managed with `sitesctl site ... update`:

```bash
sitesctl site --space <space> --name <name> update set:share:accessusers  <user>[,<user>...]
sitesctl site --space <space> --name <name> update set:share:accessgroups <group>   # e.g. ecmwf_staff
sitesctl site --space <space> --name <name> update set:share:adminusers   <user>
sitesctl site --space <space> --name <name> update set:share:admingroups  <group>
```

A site with no access users/groups and public access is world-readable; adding
access users/groups restricts it to ECMWF-authenticated members of that list.
Changing who can see or administer a site is outward-facing — confirm the exact
users/groups with Michael first. Verify the current sharing settings on the web
hub's **Sharing** tab if in doubt.

### Signed URLs (time-limited access to a private file)

```bash
sitesctl site --space <space> --name <name> signed-urls create --url <path> --duration <seconds>
sitesctl site --space <space> --name <name> signed-urls verify --url <signed-url>
```

### Keeping a site alive

Each site has a review/retention date (default one year from creation); past it,
visitors see an "outdated" notice. Extend it on the web hub's **Settings →
Retention Date**, or check `sitesctl site ... --help` for a CLI equivalent.

## Agent guidance

- **Reads are safe** — `list`, `content list`, `checksum`, `whoami`, `signed-urls
  verify`. Run them freely to answer questions and to check state before a write.
- **Writes are gated.** Before any `content upload`, `content delete`, `create`,
  `delete`, or `update set:share:*`, show Michael the exact site, paths, and
  values, and get explicit approval. `-f/--force` only skips `sitesctl`'s own
  prompt; it does not replace Michael's confirmation.
- **Prefer stored tokens.** If a command fails for lack of a token, don't
  work around it by putting a token on the command line — point Michael at the
  [Setup](#one-time-setup-done-by-the-user) step.
- **Use `-o json`** when you need to parse output; `table` is for humans.
- **Verify before destructive actions.** List a site's content before deleting
  from it, and never assume a path — confirm it exists first.

## One-time setup (done by the user)

1. **Install `sitesctl`** and put it on `PATH` (see [Prerequisites](#prerequisites)).
2. **Log in to the hub** (for create/delete/list), interactively:

   ```bash
   sitesctl auth login --username <your-ecmwf-username>
   ```

3. **Store a per-site token** so content/admin commands need no inline secret.
   Get the site's **Space** and **Name** from its Site View Page (Details tab)
   and a **Master Token** or **HTTP Access Token** (Settings tab) at
   `https://sites.ecmwf.int/hub/list/`, then:

   ```bash
   sitesctl config site-token --space <space> --name <name> --value="<token>"
   ```

   Prefer an **HTTP Access Token** with the least privilege needed (Read unless
   Read/Write is required) over the Master Token. Run this step yourself — in
   this session, prefix it with `!` so the token stays in your shell and never
   reaches the model. Tokens can be revoked any time from the site's dashboard.
