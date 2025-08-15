import re
from pathlib import Path
from core.skill_api import autoload_skills, registry
from core.audit_log import log
ROOT = Path(__file__).resolve().parents[2]
autoload_skills(ROOT)
HELP = "Commands:\n  search <q>\n  run <cmd>\n  note add <t>\n  note list\n  help\n  exit\n"
def handle(text: str) -> str:
    t = text.strip()
    if not t: return ""
    if t in ("help","?"): return HELP
    if t == "exit": return "__EXIT__"
    m = re.match(r"^search\s+(.+)$", t, re.I)
    if m:
        q = m.group(1); log("cortex", f"file.search '{q}'", reason="user")
        res = registry.call("file.search.search", query=q)
        if not res.ok: return f"Error: {res.error}"
        items = res.data[:10]
        return "\n".join([f"- {i['path']}: {i['snippet']}" for i in items]) if items else "No results."
    m = re.match(r"^run\s+(.+)$", t, re.I)
    if m:
        cmd = m.group(1); log("cortex", f"system.run '{cmd}'", reason="user")
        res = registry.call("system.run.exec", cmdline=cmd)
        return res.data if res.ok else f"Error: {res.error}"
    if t.startswith("note "):
        args = t.split(" ", 2)
        if len(args)==2 and args[1]=="list":
            res = registry.call("notes.list"); return res.data if res.ok else f"Error: {res.error}"
        if len(args)>=3 and args[1]=="add":
            res = registry.call("notes.add", text=args[2]); return res.data if res.ok else f"Error: {res.error}"
        return "Usage: note add <text> | note list"
    return "Unknown command. Type 'help'."
