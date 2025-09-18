@echo off
title [DICE] MYNFINI Adventure Game Launcher
color 0A
echo.
echo    🎲 MYNFINI Adventure Game 🎲
echo    ===========================
echo.
echo    🚀 Starting your magical adventure in seconds...
echo.
echo    ✨ Zero setup required
necho    ✨ No complex choices to make
echo    ✨ Just click and play!
echo.

python simple_launcher.py --version >nul 2>&1
if %errorlevel% == 0 (
    echo    [OK] Python found! Launching MYNFINI directly...
    python simple_launcher.py
) else (
    echo    [FOUND] Using complex launcher as fallback...
    python launcher.py
)

echo.
echo    🎮 Your adventure begins now!
echo    🌐 A browser tab will open automatically
pause >nul
