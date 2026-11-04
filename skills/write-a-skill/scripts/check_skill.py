#!/usr/bin/env python3
"""Mechanical checks for a skill directory.

Usage: python3 check_skill.py <skill-dir>
Prints OK when every check passes; otherwise one line per problem, exit 1.
Lines starting with "note:" are heuristics for the author to weigh; they never
block OK.
"""
import re
import sys
from pathlib import Path

MAX_LINES = 500
MAX_DESCRIPTION = 1024
TOC_THRESHOLD = 300
COMPLETION_WORDS = r"完成条件|完成标准|done when|done:|complete when|completion|finished when"


def numbered_steps(body):
    """Headings written as a numbered step, a sign of a fixed flow."""
    return [h for h in re.findall(r"^#{1,6}\s+(.*)$", body, re.M) if re.match(r"\d+[.、)]", h)]


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fields, key = {}, None
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        kv = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if kv:
            key, value = kv.group(1), kv.group(2).strip()
            fields[key] = "" if value in (">-", ">", "|", "|-") else value.strip("\"'")
        elif key and line.startswith((" ", "\t")):
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip())
        return 2
    root = Path(sys.argv[1]).resolve()
    skill = root / "SKILL.md"
    problems = []
    if not skill.is_file():
        print(f"missing {skill}")
        return 1

    text = skill.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        problems.append("SKILL.md has no frontmatter block (--- ... ---) at the top")
        fm = {}
    name = fm.get("name", "")
    description = fm.get("description", "")
    if not name:
        problems.append("frontmatter has no name")
    elif name != root.name:
        problems.append(f"name '{name}' differs from directory '{root.name}'")
    if not description:
        problems.append("frontmatter has no description")
    elif len(description) > MAX_DESCRIPTION:
        problems.append(f"description is {len(description)} chars (limit {MAX_DESCRIPTION})")

    lines = text.count("\n") + 1
    if lines > MAX_LINES:
        problems.append(f"SKILL.md is {lines} lines (limit {MAX_LINES})")

    # Every relative path the skill points at must exist.
    body = re.sub(r"^```.*?^```", "", text, flags=re.S | re.M)
    refs = set(re.findall(r"`((?:references|scripts|assets|agents|evals)/[^`\s<>*]+)`", body))
    refs |= set(re.findall(r"\]\(((?!https?:|#)[^)\s]+)\)", body))
    for ref in sorted(refs):
        if not (root / ref).exists():
            problems.append(f"referenced path does not exist: {ref} (if it belongs to the skill's output, write it as `<output>/{ref}`)")

    ref_docs = sorted((root / "references").glob("*.md")) if (root / "references").is_dir() else []
    for md in ref_docs:
        content = md.read_text(encoding="utf-8")
        if content.count("\n") + 1 > TOC_THRESHOLD and not re.search(r"(?im)^#+\s*(目录|contents|table of contents)", content):
            problems.append(f"{md.relative_to(root)} is over {TOC_THRESHOLD} lines without a table of contents")
        # A reference nothing points at never gets read.
        others = [text] + [o.read_text(encoding="utf-8") for o in ref_docs if o != md]
        if not any(md.name in other for other in others):
            problems.append(f"{md.relative_to(root)} is not mentioned by SKILL.md or another reference")

    notes = []
    if fm.get("disable-model-invocation", "").lower() == "true" and re.search(r"use when", description, re.I):
        notes.append("manual skill's description has trigger wording ('Use when'); a one-line summary for people is usually enough")
    shouted = sorted(set(re.findall(r"\b(?:MUST|ALWAYS|NEVER)\b", body)))
    if shouted:
        notes.append(f"all-caps {', '.join(shouted)} in SKILL.md; explaining the reason usually works better")
    steps = numbered_steps(body)
    if len(steps) >= 4:
        notes.append(f"{len(steps)} numbered steps; keep a fixed order only where the order itself is required, and state the rest as results and acceptance")
    if not re.search(COMPLETION_WORDS, body, re.I):
        notes.append("no recognizable completion criterion; say how to tell each result is done")

    for n in notes:
        print(f"note: {n}")
    if problems:
        for p in problems:
            print(p)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
