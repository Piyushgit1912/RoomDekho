@echo off

echo Starting Django Backend...
start cmd /k "cd backend && python manage.py runserver"

echo Starting Frontend Server...
start cmd /k "py -m http.server 5500"

echo Opening Browser...
timeout /t 3 >nul
start http://localhost:5500/frontend/index.html