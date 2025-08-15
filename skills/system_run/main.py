import os
import shlex
import subprocess
from pathlib import Path

from core.policy_engine import load_policy
from core.skill_api import endpoint

ROOT = Path(__file__).resolve().parents[2]
DENYLIST = {"rm", "sudo", "powershell"}


@endpoint("system.run.exec")
def exec(cmdline: str, timeout: int = 30) -> str:
    pol = load_policy()
    parts = shlex.split(cmdline)
    if not parts:
        return "No command."
    cmd = parts[0]
    if cmd in DENYLIST or cmd in getattr(pol, "denied_commands", []):
        raise RuntimeError(f"Command '{cmd}' is denied by policy.")
    if pol.allowed_commands and cmd not in pol.allowed_commands:
        raise RuntimeError(f"Command '{cmd}' is not allowed by policy.")
    env = os.environ.copy()
    try:
        proc = subprocess.run(
            parts,
            capture_output=True,
            text=True,
            env=env,
            cwd=str(ROOT),
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError("Command timed out.")
    out = (proc.stdout + proc.stderr).strip() or "(no output)"
    if proc.returncode != 0:
        out = f"[exit {proc.returncode}] {out}"
    return out
