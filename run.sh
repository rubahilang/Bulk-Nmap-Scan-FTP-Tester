#!/bin/bash

# Save the current directory
CURRENT_DIR=$(dirname "$0")

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python not found. Installing Python..."
    if [ -f /etc/debian_version ]; then
        sudo apt-get update
        sudo apt-get install -y python3
    elif [ -f /etc/redhat-release ]; then
        sudo yum install -y python3
    elif [ -f /etc/arch-release ]; then
        sudo pacman -S --noconfirm python
    else
        echo "[ERROR] Unsupported Linux distribution."
        exit 1
    fi
else
    echo "Python is already installed."
fi

# Run the Python script from the saved directory
python3 "$CURRENT_DIR/scan.py"
