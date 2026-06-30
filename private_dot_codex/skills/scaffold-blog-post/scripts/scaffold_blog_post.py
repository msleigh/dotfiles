#!/usr/bin/env python3
"""Create a Markdown blog post scaffold for msleigh.io."""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import OrderedDict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path


POSTS_DIR = Path("docs/blog/posts")
DEFAULT_AUTHOR = "msleigh"


class ScaffoldError(ValueError):
    """Raised when scaffold options are internally inconsistent."""


@dataclass
class Section:
    title: str
    notes: list[str]
    snippets: list[str]


def split_values(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        for part in value.split(","):
            clean = part.strip()
            if clean:
                result.append(clean)
    return result


def slugify(value: str) -> str:
    normalised = unicodedata.normalize("NFKD", value)
    ascii_value = normalised.encode("ascii", "ignore").decode("ascii")
    ascii_value = ascii_value.lower().replace("&", " and ")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value)
    return re.sub(r"-{2,}", "-", slug).strip("-")


def parse_iso_date(value: str) -> str:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD") from exc


def decode_text(value: str) -> str:
    return value.replace("\\n", "\n")


def split_scoped(value: str, expected_parts: int, option: str) -> list[str]:
    parts = value.split("::", expected_parts - 1)
    if len(parts) != expected_parts or any(not part.strip() for part in parts):
        message = f"{option} must use {'::'.join(['PART'] * expected_parts)}"
        raise ScaffoldError(message)
    return [decode_text(part.strip()) for part in parts]


def find_repo_root(start: Path) -> Path:
    start = start.resolve()
    search_paths = [start, *start.parents]
    for path in search_paths:
        if (path / "mkdocs.yml").is_file() and (path / POSTS_DIR).is_dir():
            return path
    if (start / POSTS_DIR).is_dir():
        return start
    raise SystemExit(
        f"could not find {POSTS_DIR}; pass --root pointing at the site repository",
    )


def yaml_scalar(value: str) -> str:
    if value and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9 .,_'()/+-]*", value):
        if value.lower() not in {"true", "false", "null"} and ": " not in value:
            return value
    return json.dumps(value)


def front_matter(
    *,
    title: str,
    author: str,
    post_date: str,
    categories: list[str],
    tags: list[str],
    draft: bool,
) -> str:
    lines = [
        "---",
        f"title: {yaml_scalar(title)}",
        "authors:",
        f"  - {yaml_scalar(author)}",
        f"date: {post_date}",
        "categories:",
    ]
    lines.extend(f"  - {yaml_scalar(value)}" for value in categories)
    if not categories:
        lines.append("  -")
    lines.append("tags:")
    lines.extend(f"  - {yaml_scalar(value)}" for value in tags)
    if not tags:
        lines.append("  -")
    if draft:
        lines.append("draft: true")
    lines.append("---")
    return "\n".join(lines)


def read_body(path: Path | None) -> str:
    if path is None:
        return ""
    return path.read_text(encoding="utf-8").strip()


def ensure_section(sections: OrderedDict[str, Section], title: str) -> Section:
    if title not in sections:
        sections[title] = Section(title=title, notes=[], snippets=[])
    return sections[title]


def todo(text: str) -> str:
    clean = text.strip()
    if not clean:
        return "- TODO"
    return f"- TODO: {clean}"


def fenced(language: str, content: str) -> str:
    clean_language = language.strip() or "text"
    clean_content = content.rstrip()
    return f"```{clean_language}\n{clean_content}\n```"


def build_sections(args: argparse.Namespace) -> OrderedDict[str, Section]:
    sections: OrderedDict[str, Section] = OrderedDict()
    for heading in args.heading:
        ensure_section(sections, heading.strip())

    for value in args.section_note:
        section_name, note = split_scoped(value, 2, "--section-note")
        ensure_section(sections, section_name).notes.append(note)

    for value in args.command:
        section_name, command = split_scoped(value, 2, "--command")
        ensure_section(sections, section_name).snippets.append(fenced("bash", command))

    for value in args.code:
        section_name, language, code = split_scoped(value, 3, "--code")
        ensure_section(sections, section_name).snippets.append(fenced(language, code))

    for value in args.link:
        section_name, label, url = split_scoped(value, 3, "--link")
        ensure_section(sections, section_name).snippets.append(f"- Link: [{label}]({url})")

    for value in args.image:
        section_name, alt_text, url = split_scoped(value, 3, "--image")
        ensure_section(sections, section_name).snippets.append(f"![{alt_text}]({url})")

    for value in args.reference:
        section_name, reference = split_scoped(value, 2, "--reference")
        ensure_section(sections, section_name).snippets.append(f"- Reference: {reference}")

    return sections


def post_content(args: argparse.Namespace) -> str:
    categories = split_values(args.category)
    tags = split_values(args.tag)
    intro_notes = args.intro_note or ["Write the opening/excerpt."]
    lines = [
        front_matter(
            title=args.title,
            author=args.author,
            post_date=args.date,
            categories=categories,
            tags=tags,
            draft=not args.publish,
        ),
        "",
        f"# {args.title}",
        "",
    ]
    lines.extend(todo(note) for note in intro_notes)
    lines.append("")
    lines.extend(["<!-- more -->", ""])

    body = read_body(args.body_file)
    if body:
        lines.extend([body, ""])
    else:
        for section in build_sections(args).values():
            lines.extend([f"## {section.title}", ""])
            section_notes = section.notes or [f"Add notes for {section.title}."]
            lines.extend(todo(note) for note in section_notes)
            if section.snippets:
                lines.append("")
                for snippet in section.snippets:
                    lines.extend([snippet, ""])
            else:
                lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a Markdown blog post scaffold for msleigh.io.",
    )
    parser.add_argument("--root", default=".", help="site repository root")
    parser.add_argument("--title", required=True, help="post title")
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        type=parse_iso_date,
        help="post date in YYYY-MM-DD format",
    )
    parser.add_argument("--slug", help="filename slug; generated from title by default")
    parser.add_argument("--author", default=DEFAULT_AUTHOR, help="front matter author")
    parser.add_argument(
        "--category",
        action="append",
        default=[],
        help="category value; repeat or comma-separate",
    )
    parser.add_argument(
        "--tag",
        action="append",
        default=[],
        help="tag value; repeat or comma-separate",
    )
    parser.add_argument(
        "--intro-note",
        action="append",
        default=[],
        help="TODO reminder before <!-- more -->; repeat as needed",
    )
    parser.add_argument(
        "--heading",
        action="append",
        default=[],
        help="section heading to append; repeat as needed",
    )
    parser.add_argument(
        "--section-note",
        action="append",
        default=[],
        help="section TODO reminder as Section::Reminder",
    )
    parser.add_argument(
        "--command",
        action="append",
        default=[],
        help="bash command block as Section::command",
    )
    parser.add_argument(
        "--code",
        action="append",
        default=[],
        help="fenced code block as Section::language::code",
    )
    parser.add_argument(
        "--link",
        action="append",
        default=[],
        help="Markdown link as Section::Label::URL",
    )
    parser.add_argument(
        "--image",
        action="append",
        default=[],
        help="Markdown image as Section::Alt text::path-or-url",
    )
    parser.add_argument(
        "--reference",
        action="append",
        default=[],
        help="reference bullet as Section::Reference text",
    )
    parser.add_argument(
        "--body-file",
        type=Path,
        help="prewritten scaffold-only Markdown to append",
    )
    parser.add_argument("--publish", action="store_true", help="omit draft: true")
    parser.add_argument("--force", action="store_true", help="overwrite target file")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    root = find_repo_root(Path(args.root))
    slug = args.slug or slugify(args.title)
    if not slug:
        parser.error("could not derive a slug; pass --slug")

    target = root / POSTS_DIR / f"{args.date}-{slug}.md"
    if target.exists() and not args.force:
        print(f"refusing to overwrite existing file: {target}", file=sys.stderr)
        return 1

    try:
        content = post_content(args)
    except ScaffoldError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    target.write_text(content, encoding="utf-8")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
