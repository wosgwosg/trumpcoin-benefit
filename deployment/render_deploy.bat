@echo off
REM Script to deploy the TrumpCoin Benefit application to Render.com from Windows

echo ===== TrumpCoin Benefit Render.com Deployment Script =====
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: git is not installed. Please install git and try again.
    exit /b 1
)

REM Check if we're in the project root directory
if not exist "manage.py" (
    echo Error: This script must be run from the project root directory.
    exit /b 1
)

if not exist "trumpcoin_benefit" (
    echo Error: This script must be run from the project root directory.
    exit /b 1
)

echo Step 1: Collecting static files locally to verify they work
python manage.py collectstatic --noinput
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to collect static files. Please fix the errors and try again.
    exit /b 1
)
echo Static files collected successfully.
echo.

echo Step 2: Checking for uncommitted changes
git status

echo.
set /p commit_changes="Do you want to commit these changes? (y/n): "

if /i "%commit_changes%"=="y" (
    set /p commit_message="Enter commit message: "
    
    git add .
    git commit -m "%commit_message%"
    
    echo Changes committed successfully.
) else (
    echo Skipping commit. Make sure to commit your changes before pushing.
)

echo.
echo Step 3: Push to GitHub
set /p push_changes="Do you want to push to GitHub now? (y/n): "

if /i "%push_changes%"=="y" (
    set /p branch_name="Enter branch name (default: main): "
    if "%branch_name%"=="" set branch_name=main
    
    git push origin %branch_name%
    
    if %ERRORLEVEL% neq 0 (
        echo Error: Failed to push to GitHub. Please check your credentials and try again.
        exit /b 1
    )
    
    echo Changes pushed to GitHub successfully.
    echo Render.com will automatically deploy the new changes.
) else (
    echo Skipping push. Remember to push your changes to GitHub to trigger a deployment on Render.com.
)

echo.
echo Step 4: Deployment Checklist
echo [✓] Updated render.yaml to include collectstatic command
echo [✓] Added diagnostic views for troubleshooting
echo [✓] Created test HTML and CSS files
echo [✓] Updated render_settings.py with improved configuration
echo [✓] Added inline styles to base_render.html template

echo.
echo After deployment, check the following URLs:
echo 1. /static/test.html - Basic static file test
echo 2. /static/test-with-css.html - CSS loading test
echo 3. /debug-info/ - Environment and configuration information
echo 4. /test-template/ - Template rendering test

echo.
echo If you encounter any issues:
echo 1. Check the Render.com logs for error messages
echo 2. Verify that the staticfiles directory exists on the server
echo 3. Make sure WhiteNoise is configured correctly
echo 4. Check that the CSS files are being loaded properly

echo.
echo Deployment preparation completed successfully!
pause
