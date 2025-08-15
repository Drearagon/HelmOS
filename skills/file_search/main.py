import os
import re
from pathlib import Path

from core.policy_engine import load_policy
from core.skill_api import endpoint


@endpoint("file.search.search")
def search(query: str, limit: int = 50):
    pol = load_policy()
    rx = re.compile(re.escape(query), re.I)
    results = []
    allowed = [os.path.expandvars(p) for p in pol.allowed_paths]
    denied = [os.path.expandvars(p) for p in pol.denied_paths]
    for base in allowed:
        for root, _, files in os.walk(base):
            # skip denied paths
            skip = False
            for d in denied:
                root_posix = Path(root).resolve().as_posix()
                if root_posix.startswith(Path(d).resolve().as_posix()):
                    skip = True
                    break
            if skip:
                continue
            for f in files:
                path = Path(root) / f
                try:
                    if path.suffix.lower() in (
                        ".txt",
                        ".md",
                        ".py",
                        ".c",
                        ".cpp",
                        ".h",
                        ".ini",
                        ".cfg",
                        ".json",
                        ".yaml",
                        ".yml",
                    ):
                        with open(path, "r", errors="ignore") as fh:
                            text = fh.read()
                        m = rx.search(text)
                        if m:
                            start = max(m.start() - 40, 0)
                            end = min(m.end() + 40, len(text))
                            snippet = text[start:end].replace("\n", " ")
                            results.append({"path": str(path), "snippet": snippet})
                            if len(results) >= limit:
                                return results
                except Exception:
                    continue
    return results
