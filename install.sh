#!/usr/bin/env bash
# Install skills from this repo globally: canonical copy in ~/.agents/skills,
# symlinked into ~/.claude/skills.
#
# `npx skills add` copies straight into ~/.claude/skills when Claude Code is
# the only target agent, so we also pass the `universal` agent (~/.agents/skills)
# to force symlink mode. The verify step repairs the link if the CLI ever
# falls back to copying.
#
# Usage:
#   ./install.sh              # install every skill in this repo
#   ./install.sh explain      # install only the named skill(s)
set -euo pipefail

REPO="isToThyMoon/skills"
AGENTS_DIR="$HOME/.agents/skills"
CLAUDE_DIR="$HOME/.claude/skills"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ "$#" -gt 0 ]; then
  skills=("$@")
else
  skills=()
  for d in "$REPO_DIR"/skills/*/; do
    [ -f "$d/SKILL.md" ] && skills+=("$(basename "$d")")
  done
fi

echo "==> installing: ${skills[*]}"
npx -y skills add "$REPO" -g -y -a claude-code universal --skill "${skills[@]}"

mkdir -p "$CLAUDE_DIR"
echo "==> verifying $CLAUDE_DIR links"
for s in "${skills[@]}"; do
  src="$AGENTS_DIR/$s"
  dst="$CLAUDE_DIR/$s"
  if [ ! -d "$src" ]; then
    echo "  !! $s: missing from $AGENTS_DIR" >&2
    exit 1
  fi
  if [ -L "$dst" ] && [ "$(cd "$dst" && pwd -P)" = "$(cd "$src" && pwd -P)" ]; then
    echo "  ok      $s -> $(readlink "$dst")"
  elif [ -e "$dst" ] && [ ! -L "$dst" ]; then
    echo "  replace $s (was a plain copy)"
    rm -rf "$dst" && ln -s "$src" "$dst"
  else
    echo "  link    $s -> $src"
    ln -sfn "$src" "$dst"
  fi
done
