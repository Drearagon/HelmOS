import re
import shlex
import os
import subprocess
import shutil
from pathlib import Path

import yaml

from core.audit_log import log
from core.error_log import log as log_error
from core.skill_api import autoload_skills, registry

ROOT = Path(__file__).resolve().parents[2]
autoload_skills(ROOT)
HELP = (
    "Commands:\n"
    "  search <q>\n"
    "  run <cmd>\n"
    "  note add <t>\n"
    "  note list\n"
    "  git status|branches|switch <name>\n"
    "  sys info|system info|status\n"
    "  policy show\n"
    "  policy set <key> <value>\n"
    "  policy edit\n"
    "  skills\n"
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
    if t in ("skills", "skill list"):
        endpoints = sorted(list(registry._endpoints.keys()))
        return "Skills:\n- " + "\n- ".join(endpoints) if endpoints else "(no skills)"
    m = re.match(r"^search\s+(.+)$", t, re.I)
    if m:
        q = m.group(1)
        log("cortex", f"file.search '{q}'", reason="user")
        try:
            res = registry.call("file.search.search", query=q)
        except Exception as e:
            log_error(e)
            return f"Error: {e}"
        if not res.ok:
            log_error(res.error)
            return f"Error: {res.error}"
        items = res.data[:10]
        if not items:
            return "No results."
        return "\n".join([f"- {i['path']}: {i['snippet']}" for i in items])
    m = re.match(r"^run\s+(.+)$", t, re.I)
    if m:
        cmd = m.group(1)
        log("cortex", f"system.run '{cmd}'", reason="user")
        try:
            res = registry.call("system.run.exec", cmdline=cmd)
        except Exception as e:
            log_error(e)
            return f"Error: {e}"
        if res.ok:
            return res.data
        log_error(res.error)
        return f"Error: {res.error}"
    if t.startswith("note "):
        args = t.split(" ", 2)
        if len(args) == 2 and args[1] == "list":
            try:
                res = registry.call("notes.list")
            except Exception as e:
                log_error(e)
                return f"Error: {e}"
            if res.ok:
                return res.data
            log_error(res.error)
            return f"Error: {res.error}"
        if len(args) >= 3 and args[1] == "add":
            try:
                res = registry.call("notes.add", text=args[2])
            except Exception as e:
                log_error(e)
                return f"Error: {e}"
            if res.ok:
                return res.data
            log_error(res.error)
            return f"Error: {res.error}"
        return "Usage: note add <text> | note list"
    if t in ("sys info", "system info", "status"):
        try:
            res = registry.call("sys.info.get")
        except Exception as e:
            log_error(e)
            return f"Error: {e}"
        if res.ok:
            return res.data
        log_error(res.error)
        return f"Error: {res.error}"
    if t == "git status":
        try:
            res = registry.call("git.status")
        except Exception as e:
            log_error(e)
            return f"Error: {e}"
        if res.ok:
            return res.data
        log_error(res.error)
        return f"Error: {res.error}"
    if t == "git branches":
        try:
            res = registry.call("git.branches")
        except Exception as e:
            log_error(e)
            return f"Error: {e}"
        if res.ok:
            return res.data
        log_error(res.error)
        return f"Error: {res.error}"
    m = re.match(r"^git switch\s+(.+)$", t, re.I)
    if m:
        name = m.group(1)
        try:
            res = registry.call("git.switch", name=name)
        except Exception as e:
            log_error(e)
            return f"Error: {e}"
        if res.ok:
            return res.data
        log_error(res.error)
        return f"Error: {res.error}"
    if t == "policy show":
        try:
            res = registry.call("config.policy.get")
        except Exception as e:
            log_error(e)
            return f"Error: {e}"
        if res.ok:
            return yaml.safe_dump(res.data)
        log_error(res.error)
        return f"Error: {res.error}"
    m = re.match(r"^policy\s+set\s+(\w+)\s+(.+)$", t, re.I)
    if m:
        key, val = m.group(1), m.group(2)
        try:
            res = registry.call("config.policy.set", key=key, value=val)
        except Exception as e:
            log_error(e)
            return f"Error: {e}"
        if res.ok:
            return res.data
        log_error(res.error)
        return f"Error: {res.error}"
    if t.startswith("policy edit"):
        editor = os.environ.get("EDITOR") or (
            "code" if shutil.which("code") else "nano"
        )
        cmd = f"{editor} configs/policies/default.yaml"
        try:
            subprocess.run(shlex.split(cmd), check=False)
            return "Opened policy for editing."
        except Exception as e:
            return f"Error opening editor: {e}"
    return "Unknown command. Type 'help'."
