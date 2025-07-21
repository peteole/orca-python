# GitHub Actions Troubleshooting

## Issue: `No module named cibuildwheel`

### Root Cause
The GitHub Actions workflow was not properly setting up the virtual environment before trying to run cibuildwheel.

### Solution
The workflow now properly:

1. **Creates virtual environment**: `uv venv --python 3.11`
2. **Installs dependencies**: `uv pip install -r requirements-dev.txt` 
3. **Runs cibuildwheel**: `uv run python -m cibuildwheel --output-dir wheelhouse`

### Key Changes Made

#### `.github/workflows/build.yml`
```yaml
- name: Create virtual environment and install dependencies
  run: |
    uv venv --python 3.11
    uv pip install -r requirements-dev.txt

- name: Build wheels
  run: |
    uv run python -m cibuildwheel --output-dir wheelhouse
```

### Makefile Usage
For local development, you can now run:

```bash
# Setup development environment
make dev

# Build wheels for all platforms
make ci-wheels
```

### Verification
The workflow ensures that:
- ✅ uv creates a proper virtual environment
- ✅ All dev dependencies (including cibuildwheel) are installed
- ✅ cibuildwheel runs in the correct environment
- ✅ Wheels are built for all target platforms

### Local Testing
You can test the setup locally with:
```bash
./test_cibuildwheel.sh
```

This will verify that cibuildwheel is properly available and working.
