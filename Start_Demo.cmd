@echo off
cd /d "%~dp0"
echo Open http://127.0.0.1:8090/ after the server starts.
echo Keep this window open. Press Ctrl+C to stop.
python -B scripts/serve_review_workbench.py --directory demo --port 8090
if errorlevel 1 pause
