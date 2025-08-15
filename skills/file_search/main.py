import os, re
from pathlib import Path
from core.skill_api import endpoint
from core.policy_engine import load_policy
@endpoint("file.search.search")
def search(query: str, limit: int = 50):
    pol = load_policy()
    rx = re.compile(re.escape(query), re.I)
    results = []
    for base in pol.allowed_paths:
        base = os.path.expandvars(base)
        for root, _, files in os.walk(base):
            for f in files:
                path = Path(root) / f
                try:
                    if path.suffix.lower() in (".txt",".md",".py",".c",".cpp",".h",".ini",".cfg",".json",".yaml",".yml"):
                        with open(path, "r", errors="ignore") as fh:
                            text = fh.read()
                        m = rx.search(text)
                        if m:
                            start = max(m.start()-40, 0); end = min(m.end()+40, len(text))
                            snippet = text[start:end].replace("\n"," ")
                            results.append({"path": str(path), "snippet": snippet})
                            if len(results) >= limit: return results
                except Exception:
                    continue
    return results
