import os
import shlex
import subprocess

from core.policy_engine import load_policy
from core.skill_api import endpoint

DEFAULT_TIMEOUT = 30  # seconds


@endpoint("system.run.exec")
def exec(cmdline: str) -> str:
    pol = load_policy()
    parts = shlex.split(cmdline)
    if not parts:
        return "No command."
    cmd = parts[0]
    if cmd not in pol.allowed_commands:
        raise RuntimeError(f"Command '{cmd}' is not allowed by policy.")

    env = os.environ.copy()
    try:
        proc = subprocess.run(
            parts,
            capture_output=True,
            text=True,
            env=env,
            timeout=DEFAULT_TIMEOUT,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        prefix = "" if proc.returncode == 0 else f"[exit {proc.returncode}] "
        return (prefix + out.strip()) if out.strip() else (prefix + "(no output)")
    except subprocess.TimeoutExpired:
        return "[timeout] Command exceeded 30s."
