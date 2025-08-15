from pathlib import Path
import os


def data_root() -> Path:
    # Prefer a writable per-user data dir (works in live ISO)
    xdg = os.environ.get("XDG_DATA_HOME")
    if xdg:
        return Path(xdg) / "helmos"
    home = Path.home()
    return home / ".local" / "share" / "helmos"


def var_path(name: str) -> Path:
    p = data_root()
    p.mkdir(parents=True, exist_ok=True)
    return p / name
