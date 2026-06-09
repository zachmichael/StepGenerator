#!/usr/bin/env bash
set -e

echo "Creating virtual environment..."
python3 -m venv venv

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Setup complete! The virtual environment is ready."
echo "To activate it in the future, run: source venv/bin/activate"
