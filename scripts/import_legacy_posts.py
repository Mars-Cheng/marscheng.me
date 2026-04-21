#!/usr/bin/env python3
from __future__ import annotations

import re
from html import unescape
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = Path("/Users/mars/Desktop/blog/_posts")
TARGET_DIR = REPO_ROOT / "content" / "blog"


def slugify(value: str) -> str:
    value = value.lower()
    value = value.replace("_", " ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value


def parse_front_matter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        raise ValueError("Expected YAML front matter")

    _, remainder = text.split("---\n", 1)
    front_matter_raw, body = remainder.split("\n---\n", 1)

    data: dict[str, object] = {}
    current_list_key: str | None = None

    for raw_line in front_matter_raw.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue

        if line.startswith("- ") and current_list_key:
            data.setdefault(current_list_key, [])
            assert isinstance(data[current_list_key], list)
            data[current_list_key].append(line[2:].strip())
            continue

        current_list_key = None
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if not value:
            data[key] = []
            current_list_key = key
            continue

        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        data[key] = value

    return data, body.lstrip()


def strip_markup(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^>\s?", "", text, flags=re.MULTILINE)
    text = text.replace("`", " ")
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def derive_summary(subtitle: str, body: str) -> str:
    if subtitle.strip():
        return subtitle.strip()

    cleaned = strip_markup(body)
    return cleaned[:177].rstrip() + "..." if len(cleaned) > 180 else cleaned


def build_front_matter(meta: dict[str, object], slug: str, date: str, summary: str) -> str:
    title = str(meta.get("title", slug))
    author = str(meta.get("author", "Mars Cheng"))
    tags = meta.get("tags", [])
    if not isinstance(tags, list):
        tags = []

    escaped_title = title.replace('"', '\\"')
    escaped_author = author.replace('"', '\\"')
    escaped_summary = summary.replace('"', '\\"')

    year = date.split("-", 1)[0]
    aliases = [f"/blog/{year}/{slug}/", f"/{year}/{slug}/"]

    lines = [
        "---",
        f'title: "{escaped_title}"',
        f"date: {date}",
        f'author: "{escaped_author}"',
        f'summary: "{escaped_summary}"',
        f'translationKey: "{slug}"',
        f'slug: "{slug}"',
        "aliases:",
    ]

    for alias in aliases:
        lines.append(f"  - {alias}")

    if tags:
        lines.append("tags:")
        for tag in tags:
            escaped_tag = str(tag).replace('"', '\\"')
            lines.append(f'  - "{escaped_tag}"')

    lines.append("---")
    return "\n".join(lines)


def import_post(path: Path) -> list[Path]:
    match = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)\.md$", path.name)
    if not match:
        raise ValueError(f"Unexpected post filename: {path.name}")

    date, title_from_filename = match.groups()
    slug = slugify(title_from_filename)

    meta, body = parse_front_matter(path.read_text(encoding="utf-8"))
    summary = derive_summary(str(meta.get("subtitle", "")), body)
    front_matter = build_front_matter(meta, slug, date, summary)
    rendered = f"{front_matter}\n\n{body.rstrip()}\n"

    created_paths = []
    for lang_suffix in ("en", "zh-tw"):
        target_path = TARGET_DIR / f"{slug}.{lang_suffix}.md"
        target_path.write_text(rendered, encoding="utf-8")
        created_paths.append(target_path)

    return created_paths


def main() -> None:
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    imported: list[Path] = []
    for path in sorted(SOURCE_DIR.glob("*.md")):
        imported.extend(import_post(path))

    print(f"Imported {len(imported)} files.")
    for path in imported:
        print(path.relative_to(REPO_ROOT))


if __name__ == "__main__":
    main()
