@echo off
echo ===================================================
echo     Compression Algorithm Comparison Tool
echo     Running the complete comparison pipeline
echo ===================================================

python main.py run-all %*

if %ERRORLEVEL% NEQ 0 (
    echo Error occurred while running the comparison.
    exit /b %ERRORLEVEL%
)

echo.
echo Comparison completed successfully!
echo.
pause 