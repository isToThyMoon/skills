#!/usr/bin/env python3
"""Count anti-slop patterns in Claude's prose. Measurement only: never blocks.

  measure.py                 hook mode: read hook JSON on stdin, append to log
  measure.py report [DAYS]   summarize the log (default: all time)
  measure.py baseline [DAYS] scan existing transcripts in ~/.claude/projects
  measure.py test TEXT       show which patterns match TEXT
"""
import json
import os
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
PATTERNS = SKILL_DIR / "patterns.json"
HOME = Path(os.environ.get("ANTI_SLOP_HOME", Path.home() / ".claude" / "anti-slop"))
LOG = HOME / "log.jsonl"
PROSE_EXT = {".md", ".mdx", ".markdown", ".txt"}
FENCE = re.compile(r"```.*?```", re.S)
INLINE_CODE = re.compile(r"`[^`\n]*`")


def load_groups():
    data = json.loads(PATTERNS.read_text(encoding="utf-8"))
    for g in data["groups"]:
        for p in g["patterns"]:
            p["re"] = re.compile(p["regex"])
    return data["groups"]


def prose(text):
    return INLINE_CODE.sub("", FENCE.sub("", text))


def size(text):
    return len(re.sub(r"\s", "", text))


def count(groups, text):
    text = prose(text)
    hits, snippets = {}, []
    for g in groups:
        for p in g["patterns"]:
            for m in p["re"].finditer(text):
                hits.setdefault(g["id"], {}).setdefault(p["id"], 0)
                hits[g["id"]][p["id"]] += 1
                a, b = max(0, m.start() - 20), min(len(text), m.end() + 20)
                snippets.append({"pattern": p["id"], "text": text[a:b].replace("\n", " ")})
    return size(text), hits, snippets


def is_prompt(entry):
    if entry.get("type") != "user" or entry.get("isMeta") or entry.get("isSidechain"):
        return False
    content = entry.get("message", {}).get("content")
    if isinstance(content, str):
        return True
    return isinstance(content, list) and all(b.get("type") == "text" for b in content)


def assistant_text(entry):
    if entry.get("type") != "assistant" or entry.get("isSidechain"):
        return ""
    content = entry.get("message", {}).get("content")
    if not isinstance(content, list):
        return ""
    return "\n".join(b.get("text", "") for b in content if b.get("type") == "text")


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                yield json.loads(line)
            except ValueError:
                continue


def last_turn_text(transcript):
    parts = []
    for entry in read_jsonl(transcript):
        if is_prompt(entry):
            parts = []
        else:
            t = assistant_text(entry)
            if t:
                parts.append(t)
    return "\n".join(parts)


def hook():
    event = json.load(sys.stdin)
    name = event.get("hook_event_name")
    if name == "Stop":
        text = event.get("last_assistant_message") or ""
        if not text and event.get("transcript_path"):
            text = last_turn_text(event["transcript_path"])
        source = "chat"
    elif name == "PostToolUse":
        tool_input = event.get("tool_input", {})
        path = tool_input.get("file_path", "")
        if Path(path).suffix.lower() not in PROSE_EXT:
            return
        text = tool_input.get("content") or tool_input.get("new_string") or ""
        source = path
    else:
        return
    if not text.strip():
        return
    chars, hits, snippets = count(load_groups(), text)
    HOME.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": int(time.time()),
        "event": name,
        "session": event.get("session_id"),
        "source": source,
        "chars": chars,
        "hits": hits,
        "snippets": snippets,
    }
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def summarize(records, groups, title):
    chars = defaultdict(int)
    hits = defaultdict(lambda: defaultdict(int))
    snippets = []
    for r in records:
        kind = "chat" if r["source"] == "chat" else "file"
        chars[kind] += r["chars"]
        for gid, ps in r["hits"].items():
            for pid, n in ps.items():
                hits[kind][(gid, pid)] += n
        snippets.extend(r["snippets"])
    print(f"# {title}  records={len(records)}")
    for kind in ("chat", "file"):
        if not chars[kind]:
            continue
        print(f"\n## {kind}  chars={chars[kind]}")
        for g in groups:
            total = sum(n for (gid, _), n in hits[kind].items() if gid == g["id"])
            print(f"{g['name']}: {total}  ({total * 1000 / chars[kind]:.2f} / 千字)")
            for p in g["patterns"]:
                n = hits[kind][(g["id"], p["id"])]
                if n:
                    print(f"  {p['id']}: {n}")
    if snippets:
        print("\n## 最近命中")
        for s in snippets[-15:]:
            print(f"- [{s['pattern']}] …{s['text']}…")


def cutoff(argv):
    return time.time() - float(argv[0]) * 86400 if argv else 0


def report(argv):
    if not LOG.exists():
        print(f"no log yet: {LOG}")
        return
    since = cutoff(argv)
    records = [r for r in read_jsonl(LOG) if r["ts"] >= since]
    summarize(records, load_groups(), f"log {LOG}")


def baseline(argv):
    groups, since, records = load_groups(), cutoff(argv), []
    for path in (Path.home() / ".claude" / "projects").glob("*/*.jsonl"):
        if path.stat().st_mtime < since:
            continue
        for entry in read_jsonl(path):
            text = assistant_text(entry)
            if text.strip():
                chars, hits, snippets = count(groups, text)
                records.append({"source": "chat", "chars": chars, "hits": hits, "snippets": snippets})
    summarize(records, groups, "baseline from transcripts")


def test(argv):
    chars, hits, snippets = count(load_groups(), " ".join(argv))
    print(json.dumps({"chars": chars, "hits": hits, "snippets": snippets}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    commands = {"report": report, "baseline": baseline, "test": test}
    if len(sys.argv) > 1 and sys.argv[1] in commands:
        commands[sys.argv[1]](sys.argv[2:])
    else:
        try:
            hook()
        except Exception as exc:  # a measurement hook must never disturb the session
            HOME.mkdir(parents=True, exist_ok=True)
            with open(HOME / "errors.log", "a", encoding="utf-8") as f:
                f.write(f"{time.ctime()} {exc!r}\n")
