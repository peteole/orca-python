#!/bin/bash
# Test script to verify cibuildwheel works locally

echo "🔧 Setting up environment for cibuildwheel test..."

# Ensure we have a clean environment
echo "📦 Installing dependencies..."
uv venv --python 3.11
uv pip install -r requirements-dev.txt

echo "🛠️ Testing cibuildwheel availability..."
if uv run python -c "import cibuildwheel; print('✅ cibuildwheel available')"; then
    echo "✅ cibuildwheel is properly installed"
else
    echo "❌ cibuildwheel not available"
    exit 1
fi

echo "🎯 Testing the make target..."
make ci-wheels

echo "✅ Test completed successfully!"
