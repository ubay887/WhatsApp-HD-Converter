@echo off
echo ========================================
echo Pre-Deployment Verification
echo ========================================
echo.

REM Check required files
echo Checking required files...
call :check_file "app.py"
call :check_file "requirements.txt"
call :check_file "Dockerfile"
call :check_file "Procfile"
call :check_file "templates\index.html"
echo.

REM Check deployment configs
echo Checking deployment configs...
call :check_file "railway.toml"
call :check_file "render.yaml"
call :check_file "fly.toml"
call :check_file "runtime.txt"
call :check_file ".dockerignore"
echo.

REM Check documentation
echo Checking documentation...
call :check_file "DEPLOYMENT_GUIDE.md"
call :check_file "DEPLOY_README.md"
call :check_file "CLEANUP_SYSTEM.md"
echo.

REM Check tools
echo Checking required tools...
call :check_command "git"
call :check_command "python"
call :check_command "docker"
echo.

REM Check Python dependencies
echo Checking Python dependencies...
if exist requirements.txt (
    echo Dependencies in requirements.txt:
    type requirements.txt
    echo.
)

REM Check git status
echo Checking git status...
if exist .git (
    echo [OK] Git repository initialized
    
    REM Check uncommitted changes
    git status --porcelain > nul 2>&1
    if errorlevel 1 (
        echo [WARNING] You have uncommitted changes
        echo Run: git add . ^&^& git commit -m "Ready for deployment"
    ) else (
        echo [OK] All changes committed
    )
    
    REM Check remote
    git remote -v | findstr origin > nul 2>&1
    if errorlevel 1 (
        echo [WARNING] No git remote configured
        echo Run: git remote add origin ^<your-repo-url^>
    ) else (
        echo [OK] Git remote configured
        git remote -v
    )
) else (
    echo [ERROR] Git not initialized
    echo Run: git init
)
echo.

REM Test Docker build
echo Docker build test...
set /p test_docker="Test Docker build? (y/n): "
if /i "%test_docker%"=="y" (
    echo Building Docker image...
    docker build -t whatsapp-converter-test .
    if errorlevel 1 (
        echo [ERROR] Docker build failed
    ) else (
        echo [OK] Docker build successful
    )
)
echo.

REM Summary
echo ========================================
echo Verification Summary
echo ========================================
echo.
echo Next steps:
echo 1. Fix any issues marked with [ERROR]
echo 2. Commit all changes if needed
echo 3. Push to GitHub
echo 4. Deploy to your chosen platform
echo.
echo Quick deploy:
echo   Run: deploy.bat
echo.
echo Or manually:
echo   git push origin main
echo   Then deploy on platform dashboard
echo.
pause
goto :eof

REM Functions
:check_file
if exist %1 (
    echo [OK] %~1 exists
) else (
    echo [ERROR] %~1 missing
)
goto :eof

:check_command
where %1 >nul 2>&1
if errorlevel 1 (
    echo [ERROR] %1 not installed
) else (
    echo [OK] %1 installed
)
goto :eof
