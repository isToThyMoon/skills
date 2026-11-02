#!/usr/bin/env python3
"""Mechanical checks for a project's harness.

Usage: python3 check_harness.py <repo> --check-cmd "<command>"
           [--expect-output <regex>] [--allow-check-failure] [--tokens <file>]
Prints OK when every check passes; otherwise one line per problem, exit 1.
Lines starting with "note:" are heuristics to weigh; they never block OK.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

SOFT_LINES = 100  # OpenAI's harness post: a map of roughly 100 lines.
HARD_LINES = 200  # Claude Code memory docs: target under 200 lines per file.
SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", "Pods", ".venv", "venv", "target"}
PLACEHOLDER = re.compile(r"\{\{[^{}\n]*\}\}")
HEX_COLOR = re.compile(r"#[0-9a-fA-F]{3,8}\b")


def find_agents_files(root):
    found = []
    for path in root.rglob("AGENTS.md"):
        if not SKIP_DIRS.intersection(path.relative_to(root).parts):
            found.append(path)
    return sorted(found)


def check_agents_file(path, root, problems, notes):
    rel = path.relative_to(root)
    text = path.read_text(encoding="utf-8")
    lines = text.count("\n") + 1
    if lines > HARD_LINES:
        problems.append(f"{rel} is {lines} lines (limit {HARD_LINES}); move detail to docs or nested AGENTS.md")
    elif lines > SOFT_LINES:
        notes.append(f"{rel} is {lines} lines; aim for about {SOFT_LINES}")

    if re.search(r"[├└]──", text):
        notes.append(f"{rel} contains a directory tree; keep only what ls cannot show")
    if PLACEHOLDER.search(text):
        problems.append(f"{rel} still has template placeholders: {PLACEHOLDER.search(text).group(0)}")

    sibling = path.with_name("CLAUDE.md")
    if not sibling.is_file():
        problems.append(f"{sibling.relative_to(root)} is missing; create it with the single line @AGENTS.md")
    elif sibling.read_text(encoding="utf-8").strip() != "@AGENTS.md":
        problems.append(f"{sibling.relative_to(root)} should contain only @AGENTS.md; move the rest into AGENTS.md")

    # Markdown links must resolve.
    for target in re.findall(r"\]\((?!https?:|#|mailto:)([^)\s]+)\)", text):
        if not (path.parent / target.split("#")[0]).exists():
            problems.append(f"{rel} links to a missing path: {target}")

    # Backticked paths: a known first segment with a missing tail is probably stale.
    for ref in set(re.findall(r"`([^`\s]+)`", text)):
        if not re.search(r"/|\.(md|json|ya?ml|toml|sh|py|ts|tsx|js|css|swift|kt|dart)$", ref):
            continue
        if ref.startswith(("/", "@", "http", "$", "<", "-")) or re.search(r"[*?{}<>=]", ref):
            continue
        clean = ref.rstrip("/")
        if (path.parent / clean).exists() or (root / clean).exists():
            continue
        first = clean.split("/")[0]
        if (path.parent / first).exists() or (root / first).exists():
            problems.append(f"{rel} mentions a missing path: {ref}")
        else:
            notes.append(f"{rel} mentions {ref}, which is not in the repo (fine if it is planned or not a path)")


def check_glossary(root, text, problems):
    """Every identifier the glossary names must be findable, or the bridge to grep is broken."""
    for term, ids in re.findall(r"\*\*([^*\n]+)\*\*\s*[(（]([^)）\n]*`[^)）\n]*)[)）]", text):
        for ident in re.findall(r"`([^`]+)`", ids):
            if ident == "待定":
                continue
            found = subprocess.run(
                ["git", "grep", "--untracked", "-q", "-F", ident, "--", ".", ":!GLOSSARY.md"],
                cwd=root,
            )
            if found.returncode != 0:
                problems.append(f"GLOSSARY.md: {term} names `{ident}`, which grep cannot find in the repo")


def check_command(root, args, agents_text, problems, notes):
    if args.check_cmd not in agents_text:
        problems.append(f"AGENTS.md does not list the check command: {args.check_cmd}")
    try:
        run = subprocess.run(
            args.check_cmd, shell=True, cwd=root, capture_output=True, text=True, timeout=args.timeout
        )
    except subprocess.TimeoutExpired:
        problems.append(f"check command ran longer than {args.timeout}s")
        return
    output = run.stdout + run.stderr
    if run.returncode != 0:
        if args.allow_check_failure:
            notes.append(f"check command exited {run.returncode}; report these as pre-existing failures")
        else:
            tail = "\n".join(output.strip().splitlines()[-15:])
            problems.append(f"check command exited {run.returncode}:\n{tail}")
    if args.expect_output and not re.search(args.expect_output, output):
        problems.append(f"check command output has no match for: {args.expect_output}")


def check_tokens(root, agents_text, tokens_arg, problems):
    tokens = root / tokens_arg
    design = root / "DESIGN.md"
    if not tokens.is_file():
        problems.append(f"token file not found: {tokens_arg}")
    if not design.is_file():
        problems.append("DESIGN.md is missing")
    if "DESIGN.md" not in agents_text:
        problems.append("AGENTS.md does not point to DESIGN.md")
    if not (tokens.is_file() and design.is_file()):
        return
    design_text = design.read_text(encoding="utf-8")
    if PLACEHOLDER.search(design_text):
        problems.append(f"DESIGN.md still has template placeholders: {PLACEHOLDER.search(design_text).group(0)}")
    if tokens_arg not in design_text:
        problems.append(f"DESIGN.md does not mention the token file {tokens_arg}")

    # The token file is the source of truth, so DESIGN.md's colors must exist there.
    front = re.match(r"^---\n(.*?)\n---\n", design_text, re.S)
    if not front:
        problems.append("DESIGN.md has no YAML front matter")
        return
    token_text = tokens.read_text(encoding="utf-8").lower()
    for color in sorted(set(HEX_COLOR.findall(front.group(1)))):
        if color.lower() not in token_text:
            problems.append(f"DESIGN.md color {color} is not in {tokens_arg}; sync the two")


def main():
    parser = argparse.ArgumentParser(description="Mechanical checks for a project's harness.")
    parser.add_argument("repo")
    parser.add_argument("--check-cmd", required=True, help="the project's single check command")
    parser.add_argument("--expect-output", help="regex the check command's output must match, proving tests ran")
    parser.add_argument(
        "--allow-check-failure",
        action="store_true",
        help="downgrade a failing check command to a note; only for failures that predate the harness",
    )
    parser.add_argument("--tokens", help="code token file, relative to the repo; pass it when the project has a UI")
    parser.add_argument("--timeout", type=int, default=600, help="seconds allowed for the check command")
    args = parser.parse_args()

    root = Path(args.repo).resolve()
    problems, notes = [], []

    agents = root / "AGENTS.md"
    if not agents.is_file():
        print(f"missing {agents}")
        return 1
    for path in find_agents_files(root):
        check_agents_file(path, root, problems, notes)
    agents_text = agents.read_text(encoding="utf-8")

    glossary = root / "GLOSSARY.md"
    if not glossary.is_file():
        problems.append("GLOSSARY.md is missing")
    else:
        if "GLOSSARY.md" not in agents_text:
            problems.append("AGENTS.md does not point to GLOSSARY.md")
        glossary_text = glossary.read_text(encoding="utf-8")
        if PLACEHOLDER.search(glossary_text):
            problems.append("GLOSSARY.md still has template placeholders")
        check_glossary(root, glossary_text, problems)

    check_command(root, args, agents_text, problems, notes)

    if args.tokens:
        check_tokens(root, agents_text, args.tokens, problems)

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
