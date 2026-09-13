#!/usr/bin/env bash
# Wire anti-slop into Claude Code (user level). Safe to re-run.
#
#   ./install.sh                      sync rules.md into CLAUDE.md, register measure hooks
#   ./install.sh --uninstall          remove the CLAUDE.md block and the hooks, keep logs
#   ./install.sh --uninstall --purge  also delete ~/.claude/anti-slop (logs)
#
# Hooks are recognized by the "anti-slop/hooks/" path in their command; the
# CLAUDE.md block by its begin/end markers. Nothing else is touched.
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
SETTINGS="$CLAUDE_HOME/settings.json"
MEMORY="$CLAUDE_HOME/CLAUDE.md"
DATA="$CLAUDE_HOME/anti-slop"
BEGIN="<!-- anti-slop:begin -->"
END="<!-- anti-slop:end -->"
MARK="anti-slop/hooks/"

uninstall=0 purge=0
for arg in "$@"; do
  case "$arg" in
    --uninstall) uninstall=1 ;;
    --purge) purge=1 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

command -v jq >/dev/null || { echo "jq is required" >&2; exit 1; }
mkdir -p "$CLAUDE_HOME"

strip_block() {
  [ -f "$MEMORY" ] || return 0
  awk -v b="$BEGIN" -v e="$END" '$0==b{skip=1;next} $0==e{skip=0;next} !skip' "$MEMORY" > "$MEMORY.tmp"
  mv "$MEMORY.tmp" "$MEMORY"
  perl -0pi -e 's/\s+\z/\n/; s/\A\n\z//' "$MEMORY"
}

strip_hooks() {
  [ -f "$SETTINGS" ] || return 0
  cp "$SETTINGS" "$SETTINGS.bak"
  jq --arg mark "$MARK" '
    if .hooks then
      .hooks |= (with_entries(
        .value |= (map(.hooks |= map(select((.command // "") | contains($mark) | not)))
                   | map(select(.hooks | length > 0)))
      ) | with_entries(select(.value | length > 0)))
      | if .hooks == {} then del(.hooks) else . end
    else . end' "$SETTINGS" > "$SETTINGS.tmp"
  mv "$SETTINGS.tmp" "$SETTINGS"
}

strip_block
strip_hooks

if [ "$uninstall" = 1 ]; then
  if [ "$purge" = 1 ]; then rm -rf "$DATA"; echo "removed $DATA"; fi
  echo "anti-slop removed from $MEMORY and $SETTINGS (backup: $SETTINGS.bak)"
  exit 0
fi

{
  [ -s "$MEMORY" ] && printf '\n'
  printf '%s\n' "$BEGIN"
  cat "$DIR/rules.md"
  printf '%s\n' "$END"
} >> "$MEMORY"

PY="$DIR/hooks/measure.py"
CMD="[ -f '$PY' ] && python3 '$PY' || true"
[ -f "$SETTINGS" ] || echo '{}' > "$SETTINGS"
jq --arg cmd "$CMD" '
  .hooks.Stop += [{hooks: [{type: "command", command: $cmd}]}]
  | .hooks.PostToolUse += [{matcher: "Write|Edit", hooks: [{type: "command", command: $cmd}]}]
' "$SETTINGS" > "$SETTINGS.tmp"
mv "$SETTINGS.tmp" "$SETTINGS"

echo "rules  -> $MEMORY"
echo "hooks  -> $SETTINGS (Stop, PostToolUse Write|Edit)"
echo "log    -> $DATA/log.jsonl   report: python3 '$PY' report"
echo "note:  new sessions pick up the change; review it under /hooks if prompted"
