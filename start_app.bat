@echo off
echo Installing Python dependencies...
py -m pip install -r dependencies.txt

echo Starting the backend...
start cmd /k "python server.py"
start cmd /k "python aiquiz.py"

echo Installing frontend dependencies...
cd Fluent
if not exist node_modules (
    echo Running npm install...
    npm install
)

echo Starting the frontend...
start cmd /k "npm run dev"

echo All processes started!
