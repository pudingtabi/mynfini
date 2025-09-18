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
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "Fedora/RHEL: sudo dnf install python3 python3-pip"
    echo "Arch: sudo pacman -S python python-pip"
    echo ""
    read -p "Press Enter after installing Python, or Ctrl+C to exit..."
fi

echo ""
echo "Press Enter to close..."
read -p ""
