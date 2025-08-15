# HelmOS — Agent‑First OS Layer (Keyboard‑First MVP)

Quick start:
```bash
cd HelmOS
./scripts/install.sh
./scripts/run_dev.sh
```

Windows quick start:
```powershell
cd HelmOS
./scripts/install.ps1
./scripts/run_dev.ps1
```

Uninstall:
```
Delete the HelmOS/ folder.
```

Troubleshooting:

- Set PowerShell execution policy if scripts won't run: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
- Activate the virtual environment manually: `source .venv/bin/activate` (bash) or `. .venv\Scripts\Activate.ps1` (PowerShell)
- Ensure Python 3.11+ is installed and on PATH.

Privacy: HelmOS runs entirely locally; no data leaves your machine. Memory keys live under `var/memory.key`.
