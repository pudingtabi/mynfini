#!/bin/bash

echo "[STAR] MYNFINI Adventure Game Launcher"
echo "==================================="
echo ""
echo "Welcome to your magical adventure!"
echo ""

# Check for Python
if command -v python3 &> /dev/null; then
    echo "[OK] Python found! Starting your adventure..."
    python3 launcher.py
elif command -v python &> /dev/null; then
    echo "[OK] Python found! Starting your adventure..."
    python launcher.py
else
    echo "[MISSING] Python not found. Please install Python 3.9 or newer:"
    echo ""
    echo "1. Visit: https://www.python.org/downloads/"
    echo "2. Download Python 3.9 or newer for Mac"
    echo "3. Run this launcher again"
    echo ""
    read -p "Press Enter to open the Python download page, or Ctrl+C to exit..."
    open https://www.python.org/downloads/
fi

echo ""
echo "Press Enter to close..."
read -p ""
