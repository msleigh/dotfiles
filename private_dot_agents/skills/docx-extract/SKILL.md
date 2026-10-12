---
name: docx-extract
description: Convert a Word (.docx) file to Markdown including its comments — each comment thread with author, date, open/resolved status, the text it is anchored to, and its replies. Use when the user wants to read, review, summarise, or track the comments or discussion in a Word document, or wants a Markdown text extract of a .docx (optionally without comments, for committing). Read-only; does not create or edit Word files.
---

# docx-extract

## Overview

`docx-extract` prints a `.docx` file as Markdown:

- a short header: when and by whom the document was last modified, how many
  comments and threads it has (open and resolved), and how many tracked changes
  are pending;
- the body: headings, lists, and tables, with a marker such as `[C3]` where
  each comment thread is anchored;
- a **Comments** section listing each thread with its author, date,
  open/resolved status, the anchored text, and its replies in date order.

Tracked changes are shown as if accepted (insertions kept, deletions dropped).

It complements, rather than replaces, `pandoc -t markdown`: pandoc can show
comments inline but does not read `commentsExtended.xml`, so it loses reply
threading and resolved status. Use this script when comments matter.

## Invocation

The executable is `scripts/docx-extract` inside this skill directory. Run it by
its full path:

```bash
<skill-dir>/scripts/docx-extract file.docx               # to stdout
<skill-dir>/scripts/docx-extract file.docx -o out.md     # to a file
<skill-dir>/scripts/docx-extract --body-only file.docx   # without comments
```

It needs only `uv` (it is a standard-library-only Python script run through
`uv run --script`).

## Agent guidance

- The file is read locally; nothing is sent anywhere.
- Comments are colleagues' attributed remarks. When the extract is going to be
  committed or shared, consider `--body-only` and summarise the comment
  substance separately rather than copying it verbatim.
- The body can contain links to personal OneDrive documents, whose URLs include
  the owner's username; strip or replace them before committing an extract if
  that matters in the destination.
- To track a document over time, keep the extract at a fixed path and
  overwrite it on each refresh, so version control shows what changed.
- Footnotes, endnotes, headers, footers, and images are not extracted; text in
  text boxes appears inline in its paragraph. For those, or for layout, fall
  back to the `docx` skill (pandoc or rendering).
