import json
import re
import shlex
from pathlib import Path

import yaml

from core.audit_log import log
from core.skill_api import autoload_skills, registry

ROOT = Path(__file__).resolve().parents[2]
autoload_skills(ROOT)
HELP = (
    "Commands:\n"
    "  search <q>\n"
    "  run <cmd>\n"
    "  note add <t>\n"
    "  note list\n"
    "  git status|diff|branch|switch <name>\n"
    "  sysinfo\n"
    "  policy show\n"
    "  policy set <key> <value>\n"
    "  policy edit\n"
    "  skill list\n"
    "  help\n"
    "  exit\n"
)


def handle(text: str) -> str:
    t = text.strip()
    if not t:
        return ""
    if t in ("help", "?"):
        return HELP
    if t == "exit":
        return "__EXIT__"
    m = re.match(r"^search\s+(.+)$", t, re.I)
    if m:
        q = m.group(1)
        log("cortex", f"file.search '{q}'", reason="user")
        res = registry.call("file.search.search", query=q)
        if not res.ok:
            return f"Error: {res.error}"
        items = res.data[:10]
        if not items:
            return "No results."
        return "\n".join([f"- {i['path']}: {i['snippet']}" for i in items])
    m = re.match(r"^run\s+(.+)$", t, re.I)
    if m:
        cmd = m.group(1)
        log("cortex", f"system.run '{cmd}'", reason="user")
        res = registry.call("system.run.exec", cmdline=cmd)
        return res.data if res.ok else f"Error: {res.error}"
    if t.startswith("note "):
        args = t.split(" ", 2)
        if len(args) == 2 and args[1] == "list":
            res = registry.call("notes.list")
            return res.data if res.ok else f"Error: {res.error}"
        if len(args) >= 3 and args[1] == "add":
            res = registry.call("notes.add", text=args[2])
            return res.data if res.ok else f"Error: {res.error}"
        return "Usage: note add <text> | note list"
    if t == "sysinfo":
        res = registry.call("system.info.get")
        return json.dumps(res.data, indent=2) if res.ok else f"Error: {res.error}"
    m = re.match(r"^git\s+(status|diff|branch|switch)(.*)$", t, re.I)
    if m:
        cmd = m.group(1).lower()
        rest = shlex.split(m.group(2))
        if cmd == "status":
            res = registry.call("git.status")
        elif cmd == "diff":
            res = registry.call("git.diff_stat")
        elif cmd == "branch":
            res = registry.call("git.branch")
        elif cmd == "switch" and rest:
            res = registry.call("git.switch", name=rest[0])
        else:
            return "Usage: git status | git diff | git branch | git switch <name>"
        return res.data if res.ok else f"Error: {res.error}"
    if t == "policy show":
        res = registry.call("config.policy.get")
        return yaml.safe_dump(res.data) if res.ok else f"Error: {res.error}"
    m = re.match(r"^policy\s+set\s+(\w+)\s+(.+)$", t, re.I)
    if m:
        key, val = m.group(1), m.group(2)
        res = registry.call("config.policy.set", key=key, value=val)
        return res.data if res.ok else f"Error: {res.error}"
    if t == "policy edit":
        res = registry.call("config.policy.edit")
        return res.data if res.ok else f"Error: {res.error}"
    if t == "skill list":
        return "\n".join(registry.list_endpoints())
    return "Unknown command. Type 'help'."
