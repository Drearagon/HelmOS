from pathlib import Path

from cryptography.fernet import Fernet

KEY_PATH = Path("var/memory.key")
MEMO_PATH = Path("var/memory.txt.enc")


def ensure_key():
    KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not KEY_PATH.exists():
        KEY_PATH.write_bytes(Fernet.generate_key())


def append_memory(text: str):
    ensure_key()
    key = KEY_PATH.read_bytes()
    f = Fernet(key)
    current = MEMO_PATH.read_bytes() if MEMO_PATH.exists() else b""
    data = f.decrypt(current) if current else b""
    data += (text + "\n").encode()
    MEMO_PATH.write_bytes(f.encrypt(data))


def read_memory() -> str:
    ensure_key()
    key = KEY_PATH.read_bytes()
    f = Fernet(key)
    if not MEMO_PATH.exists():
        return ""
    return f.decrypt(MEMO_PATH.read_bytes()).decode()
