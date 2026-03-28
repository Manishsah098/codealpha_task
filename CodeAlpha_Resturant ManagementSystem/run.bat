@echo off
echo Starting Backend Server...
start cmd.exe /k "cd backend && venv\Scripts\python.exe manage.py runserver"

echo Starting Frontend Server...
start cmd.exe /k "cd frontend && python -m http.server 3000"

echo Both servers are starting in new windows.
echo Frontend will be available at: http://localhost:3000/
echo.
echo Note: Close the newly opened terminal windows to stop the servers.
pause
