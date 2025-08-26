#!/bin/bash

# Ensure pyenv is installed
if ! command -v pyenv &> /dev/null; then
    echo "pyenv not found. Please install pyenv first."
    exit 1
fi

# Ensure Python 3.11 is installed with pyenv
if ! pyenv versions --bare | grep -q "^3.11"; then
    echo "Installing Python 3.11 with pyenv..."
    pyenv install 3.11.0
fi

# Set local Python version to 3.11
pyenv local 3.11

# Create virtual environment if not present
if [ ! -d ".venv" ]; then
    python -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install requirements
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found."
    exit 1
fi
