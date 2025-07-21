#!/bin/bash

# Build script for ORCA Python package using uv

echo "🔨 Building ORCA Python package with uv..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Create and activate virtual environment with uv
echo "🐍 Creating virtual environment..."
uv venv --python 3.11
source .venv/bin/activate

# Install build dependencies
echo "📦 Installing build dependencies..."
uv pip install -U pip setuptools wheel pybind11 numpy build

# Build the package in development mode
echo "🔧 Building package in development mode..."
python setup.py build_ext --inplace

# Run tests
echo "🧪 Running tests..."
python test_orca.py

echo "✅ Development build complete!"
echo ""
echo "Available commands:"
echo "  🏗️  Build wheel:     uv run python setup.py bdist_wheel"
echo "  📊  Run example:     uv run python example.py"
echo "  🧪  Run tests:       uv run python test_orca.py"
echo "  📦  Build for PyPI:  uv run python -m build"
echo ""
echo "For CI/CD wheel building:"
echo "  uv pip install cibuildwheel"
echo "  uv run python -m cibuildwheel --output-dir wheelhouse"
