---
name: publish-blog-post
description: Publish a drafted Markdown blog post for the msleigh.io MkDocs Material blog. Use when Michael asks to publish, ship, or release a post or draft, flip a post from draft to published, or commit and push a finished post under docs/blog/posts. Delegates to the blog CLI; do not hand-edit front matter or craft git commands directly. Do not write, complete, or polish the post prose.
---

# Publish Blog Post

## Overview

Take a finished draft under `docs/blog/posts` from `draft: true` to published, commit it,
and (with confirmation) push. All of the work is done by the blog CLI so the steps are
deterministic and reproducible. This skill only routes intent to the right CLI call and
enforces house rules; it does not edit files or run raw git commands.

The CLI is:

```bash
uv run ~/projects/blog/blog.py   # aliased to `blog` in interactive shells
```

## Workflow

1. Identify the target post. If it is ambiguous, list candidates:

    ```bash
    uv run ~/projects/blog/blog.py drafts --json
    ```

2. Validate before publishing:

    ```bash
    uv run ~/projects/blog/blog.py validate          # pre-commit on changed posts
    uv run ~/projects/blog/blog.py validate --build   # also mkdocs build --strict
    ```

3. Preview the intended actions without changing anything:

    ```bash
    uv run ~/projects/blog/blog.py publish -f docs/blog/posts/<file>.md --yes --dry-run
    ```

4. Publish. Commit only by default; push only when Michael has clearly asked to:

    ```bash
    # commit locally, do not push
    uv run ~/projects/blog/blog.py publish -f docs/blog/posts/<file>.md --yes --no-push

    # commit and push (only with explicit go-ahead)
    uv run ~/projects/blog/blog.py publish -f docs/blog/posts/<file>.md --yes
    ```

## Command reference

- `publish -f <path>` — publish a specific post; repeat `-f` for several.
- `publish --all` — publish every new or modified post under `docs/blog/posts`.
- `publish --yes` — skip the interactive checkbox (needed when scripting).
- `publish --dry-run` — report what would happen; make no changes.
- `publish -m "message"` — override the auto commit message (`Publish: <titles>`).
- `publish --no-push` — commit only, skip the push.

## House rules

- Publish posts as written. Never write, complete, or polish the prose, and never fill in
  `TODO` placeholders — if a draft looks unfinished, flag it to Michael rather than
  completing it. Do not mimic Michael's voice.
- Confirm the exact post(s) with Michael before publishing.
- Default to `--no-push`; treat pushing as an outward-facing action that needs a clear
  go-ahead.
- Commit messages are British English and plain; never add co-authors.
- Work in a git worktree, not directly on a shared checkout.
- Prefer one `publish` call over hand-editing `draft:` or running `git` yourself.
