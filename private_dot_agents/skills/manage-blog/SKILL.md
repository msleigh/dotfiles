---
name: manage-blog
description: Inspect and preview the msleigh.io MkDocs Material blog. Use when Michael asks to list posts or drafts, show blog tags or categories, report blog statistics, preview or serve the blog locally, or validate posts before publishing. Delegates to the blog CLI; this skill is read-mostly and never commits or pushes.
---

# Manage Blog

## Overview

Answer questions about the blog and preview it locally, using the blog CLI so results are
deterministic. This skill is read-mostly: it lists, inspects, serves, and validates, but
never edits posts, commits, or pushes. For creating a post use `scaffold-blog-post`; for
publishing use `publish-blog-post`.

The CLI is:

```bash
uv run ~/projects/blog/blog.py   # aliased to `blog` in interactive shells
```

Add `--json` to `drafts`, `list`, `tags`, and `stats` for machine-readable output.

## Which command answers which question

- "What drafts are outstanding?" → `drafts` (or `drafts --json`)
- "What posts exist and are they published?" → `list` (or `list --json`)
- "What tags/categories are in use?" → `tags` (or `tags --json`)
- "How many posts, by month, most-used tags?" → `stats` (or `stats --json`)
- "Open a post to edit" → `open` (add `--all` to pick from every post)
- "Preview the site locally" → `serve` (add `--no-browser` to skip opening a browser)
- "Are the posts clean and does the site build?" → `validate` (add `--build` for a strict build)

## Examples

```bash
uv run ~/projects/blog/blog.py drafts --json
uv run ~/projects/blog/blog.py list
uv run ~/projects/blog/blog.py stats
uv run ~/projects/blog/blog.py serve --no-browser
uv run ~/projects/blog/blog.py validate --build
```

## House rules

- Stay read-only: do not change `draft:` status, commit, or push from this skill.
- Prefer `--json` output when feeding results into further steps.
- Route publishing to `publish-blog-post` and post creation to `scaffold-blog-post`.
