import os
import subprocess
from pathlib import Path

from core.policy_engine import load_policy
from core.skill_api import endpoint


def _check_cwd(pol):
    cwd = Path.cwd().resolve()
    for base in pol.allowed_paths:
        base_path = Path(os.path.expandvars(base)).resolve()
        if str(cwd).startswith(str(base_path)):
            for deny in pol.denied_paths:
                deny_path = Path(os.path.expandvars(deny)).resolve()
                if str(cwd).startswith(str(deny_path)):
                    raise RuntimeError("Path is denied by policy.")
            return
    raise RuntimeError("Path not allowed by policy.")


def _git(args):
    proc = subprocess.run(["git", *args], capture_output=True, text=True)
    out = (proc.stdout + proc.stderr).strip() or "(no output)"
    if proc.returncode != 0:
        out = f"[exit {proc.returncode}] {out}"
    return out


@endpoint("git.status")
def status():
    pol = load_policy()
    _check_cwd(pol)
    return _git(["status"])


@endpoint("git.diff_stat")
def diff_stat():
    pol = load_policy()
    _check_cwd(pol)
    return _git(["diff", "--stat"])


@endpoint("git.branch")
def branch():
    pol = load_policy()
    _check_cwd(pol)
    return _git(["branch", "--show-current"])


@endpoint("git.branches")
def branches():
    pol = load_policy()
    _check_cwd(pol)
    return _git(["branch", "--all", "--verbose", "--color=always"])


@endpoint("git.switch")
def switch(name: str):
    pol = load_policy()
    _check_cwd(pol)
    return _git(["switch", name])
