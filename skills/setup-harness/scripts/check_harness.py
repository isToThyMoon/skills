#!/usr/bin/env python3
"""Mechanical checks for a project's harness.

Usage: python3 check_harness.py <repo> --check-cmd "<command>"
           [--expect-output <regex>] [--timeout <seconds>] [--glossary <file>] [--tokens <file>]...
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
GLOSSARY_NAMES = ("GLOSSARY.md", "CONTEXT.md")


def is_ignored(root, rel):
    """Local-only paths such as secrets or SDK dirs are legitimately absent from a checkout."""
    for candidate in (rel, rel + "/"):
        if subprocess.run(["git", "check-ignore", "-q", "--", candidate], cwd=root, capture_output=True).returncode == 0:
            return True
    return False


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
        from_dir = str((path.parent / clean).relative_to(root))
        if is_ignored(root, clean) or is_ignored(root, from_dir):
            continue
        first = clean.split("/")[0]
        if (path.parent / first).exists() or (root / first).exists():
            problems.append(f"{rel} mentions a missing path: {ref}")
        else:
            notes.append(f"{rel} mentions {ref}, which is not in the repo (fine if it is planned or not a path)")


def check_glossary(root, name, text, problems):
    """Every identifier the glossary names must be findable, or the bridge to grep is broken."""
    for term, ids in re.findall(r"\*\*([^*\n]+)\*\*\s*[(（]([^)）\n]*`[^)）\n]*)[)）]", text):
        for ident in re.findall(r"`([^`]+)`", ids):
            if ident == "待定":
                continue
            found = subprocess.run(
                ["git", "grep", "--untracked", "-q", "-F", ident, "--", ".", f":!{name}"],
                cwd=root,
            )
            if found.returncode != 0:
                problems.append(f"{name}: {term} names `{ident}`, which grep cannot find in the repo")


def check_command(root, args, agents_text, problems):
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
        tail = "\n".join(output.strip().splitlines()[-15:])
        problems.append(f"check command exited {run.returncode}:\n{tail}")
    if args.expect_output and not re.search(args.expect_output, output):
        problems.append(f"check command output has no match for: {args.expect_output}")


def check_tokens(root, agents_text, tokens_args, problems, notes):
    design = root / "DESIGN.md"
    if "DESIGN.md" not in agents_text:
        problems.append("AGENTS.md does not point to DESIGN.md")
    if not design.is_file():
        problems.append("DESIGN.md is missing")
        return
    design_text = design.read_text(encoding="utf-8")
    if PLACEHOLDER.search(design_text):
        problems.append(f"DESIGN.md still has template placeholders: {PLACEHOLDER.search(design_text).group(0)}")

    token_text = ""
    for tokens_arg in tokens_args:
        tokens = root / tokens_arg
        if not tokens.is_file():
            problems.append(f"token file not found: {tokens_arg}")
            continue
        token_text += tokens.read_text(encoding="utf-8").lower()
        if tokens_arg not in design_text:
            problems.append(f"DESIGN.md does not mention the token file {tokens_arg}")

    front = re.match(r"^---\n(.*?)\n---\n", design_text, re.S)
    if not front:
        problems.append("DESIGN.md has no YAML front matter")
        return
    # Tokens may be RGB floats or asset names, so a text match can neither prove nor disprove sync.
    missing = [c for c in sorted(set(HEX_COLOR.findall(front.group(1)))) if c.lower() not in token_text]
    if missing:
        notes.append(f"DESIGN.md colors not found as hex in the token files: {', '.join(missing)}; compare by hand")
    notes.append("color sync is only a hex text match; compare non-hex tokens with DESIGN.md by hand")


def main():
    parser = argparse.ArgumentParser(description="Mechanical checks for a project's harness.")
    parser.add_argument("repo")
    parser.add_argument("--check-cmd", required=True, help="the project's single check command")
    parser.add_argument("--expect-output", help="regex the check command's output must match, proving it really ran")
    parser.add_argument("--glossary", help=f"glossary file, when it is not one of {', '.join(GLOSSARY_NAMES)}")
    parser.add_argument(
        "--tokens",
        action="append",
        help="code token file, relative to the repo; repeat for each one when the project has a UI",
    )
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

    names = (args.glossary,) if args.glossary else GLOSSARY_NAMES
    glossary_name = next((n for n in names if (root / n).is_file()), None)
    if glossary_name is None:
        problems.append(f"no glossary found: {' or '.join(names)}")
    else:
        if glossary_name not in agents_text:
            problems.append(f"AGENTS.md does not point to {glossary_name}")
        glossary_text = (root / glossary_name).read_text(encoding="utf-8")
        if PLACEHOLDER.search(glossary_text):
            problems.append(f"{glossary_name} still has template placeholders")
        check_glossary(root, glossary_name, glossary_text, problems)

    check_command(root, args, agents_text, problems)

    if args.tokens:
        check_tokens(root, agents_text, args.tokens, problems, notes)

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
