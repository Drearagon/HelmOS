from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from pathlib import Path
from ai.cortex.main import handle
HIST = Path("var/history.txt"); HIST.parent.mkdir(parents=True, exist_ok=True)
def main():
    session = PromptSession(message=lambda: "HelmOS> ", history=FileHistory(str(HIST)))
    print("HelmOS — Keyboard Palette (type 'help' or 'exit')")
    while True:
        try:
            text = session.prompt()
        except KeyboardInterrupt:
            print("^C"); continue
        out = handle(text)
        if out == "__EXIT__": print("Bye."); break
        if out: print(out)
if __name__ == "__main__":
    main()
