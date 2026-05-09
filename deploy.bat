@echo off
echo ========================================
echo WhatsApp HD Converter - Quick Deploy
echo ========================================
echo.

REM Check if git is initialized
if not exist .git (
    echo Initializing git repository...
    git init
    git add .
    git commit -m "Initial commit - Ready for deployment"
) else (
    echo Git repository already initialized
)

echo.
echo Choose deployment platform:
echo 1. Railway (Recommended)
echo 2. Render
echo 3. Fly.io
echo 4. Exit
echo.
set /p choice="Enter choice (1-4): "

if "%choice%"=="1" goto railway
if "%choice%"=="2" goto render
if "%choice%"=="3" goto flyio
if "%choice%"=="4" goto exit
goto invalid

:railway
echo.
echo Deploying to Railway...
echo.
echo Steps:
echo 1. Push code to GitHub
echo 2. Go to https://railway.app
echo 3. Click 'New Project' - 'Deploy from GitHub repo'
echo 4. Select your repository
echo 5. Wait for deployment
echo 6. Generate domain in Settings
echo.
set /p push="Push to GitHub now? (y/n): "
if /i "%push%"=="y" (
    set /p repo_url="Enter GitHub repo URL: "
    git remote add origin %repo_url%
    git branch -M main
    git push -u origin main
    echo Code pushed to GitHub!
    echo Now go to Railway and deploy from GitHub
)
goto end

:render
echo.
echo Deploying to Render...
echo.
echo Steps:
echo 1. Push code to GitHub
echo 2. Go to https://render.com
echo 3. Click 'New' - 'Web Service'
echo 4. Connect GitHub repository
echo 5. Select 'Docker' environment
echo 6. Click 'Create Web Service'
echo.
set /p push="Push to GitHub now? (y/n): "
if /i "%push%"=="y" (
    set /p repo_url="Enter GitHub repo URL: "
    git remote add origin %repo_url%
    git branch -M main
    git push -u origin main
    echo Code pushed to GitHub!
    echo Now go to Render and deploy from GitHub
)
goto end

:flyio
echo.
echo Deploying to Fly.io...
echo.
echo Please install Fly CLI first:
echo https://fly.io/docs/hands-on/install-flyctl/
echo.
echo Then run these commands:
echo   fly auth login
echo   fly launch --no-deploy
echo   fly deploy
echo   fly open
echo.
pause
goto end

:invalid
echo Invalid choice
goto end

:exit
echo Exiting...
goto end

:end
echo.
echo ========================================
echo Deployment process completed!
echo ========================================
echo.
echo Next steps:
echo 1. Test your deployment
echo 2. Check logs for any errors
echo 3. Setup custom domain (optional)
echo 4. Monitor usage
echo.
echo For detailed instructions, see DEPLOYMENT_GUIDE.md
echo.
pause
