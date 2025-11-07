#!/bin/bash
set -e  # Faz o script parar se algo der errado

echo "Creating trudag virtual environment..."
python3 -m venv venv

echo "🔧 Activating environment..."
# Ativa o ambiente virtual
source venv/bin/activate

echo "⬆ Upgrading pip and installing dependencies..."
pip install --upgrade pip pyyaml

echo "Installing Trudag (Trustable tool)..."
pip install trustable --index-url https://gitlab.com/api/v4/projects/66600816/packages/pypi/simple

echo "Verifying installation..."
trudag --version

echo ""
echo "Environment ready!"
echo "run source .venv/bin/activate to join environment"
echo "To exit, run: deactivate"
echo ""
