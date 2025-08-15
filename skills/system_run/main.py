import shlex, subprocess, os
from core.skill_api import endpoint
from core.policy_engine import load_policy
@endpoint("system.run.exec")
def exec(cmdline: str) -> str:
    pol = load_policy()
    parts = shlex.split(cmdline)
    if not parts: return "No command."
    cmd = parts[0]
    if cmd not in pol.allowed_commands:
        raise RuntimeError(f"Command '{cmd}' is not allowed by policy.")
    env = os.environ.copy()
    proc = subprocess.run(parts, capture_output=True, text=True, env=env)
    out = proc.stdout + proc.stderr
    return out.strip() if out.strip() else "(no output)"
