#!/usr/bin/env python3
"""Count test code against source code in a git repo.

Usage: python3 test_inventory.py <repo> [--list]
Prints totals, per-area counts and the largest test files. --list adds every
test file, for an audit to mark one by one.
"""
import argparse
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

CODE_EXT = {
    ".c", ".cc", ".cpp", ".cs", ".dart", ".ex", ".exs", ".go", ".h", ".hpp", ".java", ".js", ".jsx",
    ".kt", ".kts", ".m", ".mm", ".mjs", ".php", ".py", ".rb", ".rs", ".scala", ".svelte", ".swift",
    ".ts", ".tsx", ".vue", ".xaml",
}
TEST_DIRS = {
    "test", "tests", "__tests__", "__test__", "spec", "specs", "e2e", "integration_test",
    "androidtest", "unittest", "uitest", "uitests",
}
TEST_NAME = re.compile(
    r"(^test_.*|.*_test|.*_spec|.*\.test|.*\.spec|.*(Tests?|Spec|TestCase|Tests?Support))$"
)
TEST_DIR_SUFFIX = re.compile(r"(Tests?|\.Tests?)$")


def is_test(path):
    parts = path.parts[:-1]
    if any(p.lower() in TEST_DIRS or TEST_DIR_SUFFIX.search(p) for p in parts):
        return True
    return bool(TEST_NAME.match(path.stem))


def count_lines(path):
    """Line count, or None for binary files such as .ts video samples that share a code extension."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if b"\0" in data[:8192]:
        return None
    return data.count(b"\n")


def area(path):
    return "/".join(path.parts[:2]) if len(path.parts) > 2 else (path.parts[0] if len(path.parts) > 1 else ".")


def main():
    parser = argparse.ArgumentParser(description="Count test code against source code in a git repo.")
    parser.add_argument("repo")
    parser.add_argument("--list", action="store_true", help="list every test file")
    args = parser.parse_args()

    root = Path(args.repo).resolve()
    listed = subprocess.run(
        ["git", "ls-files", "-z", "-co", "--exclude-standard"], cwd=root, capture_output=True, text=True
    )
    if listed.returncode != 0:
        print(listed.stderr.strip() or f"{root} is not a git repository")
        return 1

    tests, src_files, src_lines = [], 0, 0
    area_tests, area_src = Counter(), Counter()
    for name in filter(None, listed.stdout.split("\0")):
        rel = Path(name)
        if rel.suffix.lower() not in CODE_EXT or not (root / rel).is_file():
            continue
        lines = count_lines(root / rel)
        if lines is None:
            continue
        if is_test(rel):
            tests.append((lines, name))
            area_tests[area(rel)] += lines
        else:
            src_files += 1
            src_lines += lines
            area_src[area(rel)] += lines

    test_lines = sum(n for n, _ in tests)
    ratio = f"{test_lines / src_lines:.2f}" if src_lines else "n/a"
    print(f"source: {src_files} files, {src_lines} lines")
    print(f"tests:  {len(tests)} files, {test_lines} lines")
    print(f"test/source line ratio: {ratio}")

    if tests:
        print("\nby area (test lines / source lines):")
        for name, lines in area_tests.most_common():
            print(f"  {name}: {lines} / {area_src[name]}" if area_src[name] else f"  {name}: {lines} (test-only area)")
        print("\nlargest test files:")
        for lines, name in sorted(tests, reverse=True)[:20]:
            print(f"  {lines:>7}  {name}")
    if args.list:
        print("\nall test files:")
        for lines, name in sorted(tests, key=lambda t: t[1]):
            print(f"  {lines:>7}  {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
