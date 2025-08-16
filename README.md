# HelmOS — Agent-First OS Layer (Keyboard-First MVP)

HelmOS is an experimental, agent-driven layer that turns a terminal into a keyboard-first operating experience. It ships with a small set of "skills" (pluggable commands) and runs entirely on your machine.

## Topics
- agents
- operating-system
- automation
- cli

## Quick start
```bash
cd HelmOS
./scripts/install.sh
./scripts/run_dev.sh
```

### Windows quick start
```powershell
cd HelmOS
./scripts/install.ps1
./scripts/run_dev.ps1
```

## Uninstall
```
Delete the HelmOS/ folder.
```

## Built-in skills
- `skills.list` — enumerate registered skill endpoints
- `sys info` — report OS, CPU, memory, disk, and Python info

## Build a bootable ISO (Debian live)
To experiment with HelmOS as a live system, use the scripts under `os/debian-live/`:
```
cd os/debian-live
./prepare.sh   # copy project files into the image
./build.sh     # produce live-image-amd64.hybrid.iso
```

## Troubleshooting
- Set PowerShell execution policy if scripts won't run: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
- Activate the virtual environment manually: `source .venv/bin/activate` (bash) or `. .venv\Scripts\Activate.ps1` (PowerShell)
- Ensure Python 3.11+ is installed and on PATH
- On Windows, running from a terminal with administrator privileges may help with package installs

## Privacy
HelmOS runs entirely locally; no data leaves your machine. Memory keys live under `var/memory.key`.

## License
MIT – see [LICENSE](LICENSE).
