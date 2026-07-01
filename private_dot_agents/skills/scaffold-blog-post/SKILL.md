---
name: scaffold-blog-post
description: Scaffold-only setup for Markdown blog posts for the msleigh.io MkDocs Material blog. Use when Codex is asked to write, scaffold, draft, or prepare a blog post, create a post file, create blog front matter, add headings, add the more divider, or turn notes into a post structure under docs/blog/posts. Do not write the post prose.
---

# Scaffold Blog Post

## Overview

Create Markdown blog post scaffolds for the msleigh.io MkDocs Material blog. Set up the file, front matter, divider, headings, reminders, and Markdown syntax; leave the actual prose for Michael to write.

This is a scaffolding-only skill. Never write paragraph content, a finished standfirst, or a completed section in Michael's voice. Use short `TODO` bullets and raw Markdown structures instead.

## Workflow

1. Inspect `git status --short --branch` and avoid overwriting unrelated user changes.
2. Work from the repository root when possible. For msleigh.io, posts live in `docs/blog/posts`.
3. Infer the post title and rough section structure from the request when clear. Ask one concise question only when the title or topic is genuinely ambiguous.
4. Use `scripts/scaffold_blog_post.py` to create the initial Markdown file. Run the script with `--help` if the options are not fresh in context.
5. Add requested commands, code blocks, links, URLs, images, and references in the relevant section as Markdown syntax only.
6. Run focused validation when practical, such as `pre-commit run --files <post-path>` or the site's documented build command.

## Blog Conventions

- Name new post files as `YYYY-MM-DD-slug.md`.
- Use `authors:` with `- msleigh` in block-list YAML style.
- Use ISO dates: `YYYY-MM-DD`.
- Use `draft: true` unless the user explicitly asks for a publish-ready post.
- Put short `TODO` bullets for the opening/excerpt immediately after the H1, then `<!-- more -->`.
- Keep `categories` broad and `tags` specific. Use lower-case terms unless a proper noun requires capitals.
- Preserve technical terms, commands, paths, links, URLs, references, and code blocks exactly.

## Helper Script

Create a scaffold:

```bash
python3 /path/to/scaffold-blog-post/scripts/scaffold_blog_post.py \
  --root /path/to/msleigh.io \
  --title "Post title" \
  --category category \
  --tag tag \
  --intro-note "Say what problem the post solves." \
  --heading "Context" \
  --section-note "Context::Mention the relevant starting point."
```

Useful options:

- `--date YYYY-MM-DD`: override the date used in the filename and front matter.
- `--slug slug-text`: override the generated slug.
- `--intro-note "Reminder"`: add a `TODO` bullet before `<!-- more -->`.
- `--heading "Section title"`: add one or more section headings.
- `--section-note "Section::Reminder"`: add a `TODO` bullet under a section.
- `--command "Section::command here"`: add a fenced `bash` command block.
- `--code "Section::language::code here"`: add a fenced code block.
- `--link "Section::Label::https://example.com"`: add a Markdown link bullet.
- `--image "Section::Alt text::path-or-url"`: add Markdown image syntax.
- `--reference "Section::Reference text"`: add a reference reminder bullet.
- `--publish`: omit `draft: true`.
- `--force`: overwrite an existing target file only when the user explicitly asked for that.

After creating the scaffold, open the file and continue editing in place. Do not regenerate the whole file if the user already has content in it.

## Scaffolding Rules

- Match nearby posts for front matter shape and Markdown style.
- Prefer a concrete title over a vague working title when the topic is clear.
- Do not draft prose, conclusions, explanations, or transitions.
- Do not mimic Michael's voice.
- Use short reminders such as `- TODO: Explain why this mattered.` rather than writing the explanation.
- Insert code blocks, commands, links, URLs, images, references, and placeholders where they are likely to belong.
- Use Markdown headings, fenced code blocks with language info strings, image syntax, link syntax, and inline code for commands, paths, and identifiers.
- Browse or ask only when current or factual claims are needed for the scaffold; do not add unverified facts as prose.
