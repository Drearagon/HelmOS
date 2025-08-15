import os, subprocess
from pathlib import Path
from core.skill_api import endpoint
from core.policy_engine import load_policy

def _check_path(path: Path, pol):
    path = path.resolve()
    for base in pol.allowed_paths:
        base_path = Path(os.path.expandvars(base)).resolve()
        if str(path).startswith(str(base_path)):
            for deny in pol.denied_paths:
                deny_path = Path(os.path.expandvars(deny)).resolve()
                if str(path).startswith(str(deny_path)):
                    raise RuntimeError("Path is denied by policy.")
            return
    raise RuntimeError("Path not allowed by policy.")

def _git(args, cwd):
    proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "git error")
    return proc.stdout.strip() or "(no output)"

@endpoint("git.clone")
def clone(url: str, path: str):
    pol = load_policy()
    dest = Path(path).expanduser()
    _check_path(dest, pol)
    return _git(["clone", url, str(dest)], cwd=None)

@endpoint("git.status")
def status(path: str):
    pol = load_policy()
    repo = Path(path).expanduser()
    _check_path(repo, pol)
    return _git(["status"], cwd=str(repo))

@endpoint("git.commit")
def commit(path: str, message: str):
    pol = load_policy()
    repo = Path(path).expanduser()
    _check_path(repo, pol)
    _git(["add", "-A"], cwd=str(repo))
    return _git(["commit", "-m", message], cwd=str(repo))
