#!/bin/bash

# Update system packages
sudo pacman -Syu --noconfirm

# Install Python and pip
sudo pacman -S python python-pip --noconfirm

# Install PyQt5 via pacman
sudo pacman -S python-pyqt5 --noconfirm

# Create and activate a virtual environment for non-Arch packages
python -m venv wecap_env
source wecap_env/bin/activate

# Install win11toast in the virtual environment
pip install --upgrade pip
pip install win11toast

echo "Virtual environment created. To run the program, activate the virtual environment with:"
echo "source wecap_env/bin/activate"
echo "All requirements installed. You can now run the Wecap program."

