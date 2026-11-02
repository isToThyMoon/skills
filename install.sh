#!/usr/bin/env bash
# Install skills from this repo globally: canonical copy in ~/.agents/skills,
# symlinked into ~/.claude/skills.
#
# `npx skills add` copies straight into ~/.claude/skills when Claude Code is
# the only target agent, so we also pass the `universal` agent (~/.agents/skills)
# to force symlink mode. The verify step repairs the link if the CLI ever
# falls back to copying.
#
# Before installing, it checks for commits on main not yet on origin/main and
# asks whether to push them (the install pulls from GitHub, not this checkout).
#
# Usage:
#   ./install.sh              # install every skill in this repo
#   ./install.sh anti-slop    # install only the named skill(s)
set -euo pipefail

REPO="isToThyMoon/skills"
AGENTS_DIR="$HOME/.agents/skills"
CLAUDE_DIR="$HOME/.claude/skills"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

# `npx skills add` installs from GitHub, so local commits on main that are not
# pushed yet would be silently missing. Offer to push them first.
if git -C "$REPO_DIR" rev-parse --verify -q origin/main >/dev/null; then
  git -C "$REPO_DIR" fetch -q origin main || echo "  !! fetch failed, comparing with the last known origin/main" >&2
  unpushed="$(git -C "$REPO_DIR" log --oneline origin/main..main)"
  if [ -n "$unpushed" ]; then
    echo "==> main has commits not on origin/main:"
    echo "$unpushed" | sed 's/^/  /'
    answer=""
    if [ -t 0 ]; then
      read -r -p "Push them to origin and install? [y/N] " answer
    fi
    case "$answer" in
      y|Y|yes) git -C "$REPO_DIR" push origin main ;;
      *) echo "aborted: install would use the old version on GitHub" >&2; exit 1 ;;
    esac
  fi
else
  echo "  !! no origin/main, skipping unpushed-commit check" >&2
fi

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
