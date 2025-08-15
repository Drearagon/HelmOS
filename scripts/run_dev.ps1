$env:VENV = ".venv/"
. $env:VENV\Scripts\Activate.ps1
python -m cli.palette
Read-Host "Press Enter to exit"
