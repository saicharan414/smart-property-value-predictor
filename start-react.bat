@echo off
echo 🚀 Setting up SPVP React Frontend...

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js first.
    pause
    exit /b 1
)

REM Navigate to React frontend
cd react-frontend

REM Install dependencies
echo 📦 Installing dependencies...
npm install

REM Start the React development server
echo 🌐 Starting React development server...
npm start

pause
