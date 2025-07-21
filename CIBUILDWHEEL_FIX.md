# Cibuildwheel Linux Build Fix

## Problem
The cibuildwheel process was failing on Linux with:
```
Error: cibuildwheel: Command ['sh', '-c', 'yum install -y gcc-c++ || apt-get update && apt-get install -y g++'] failed with code 127.
```

## Root Cause
The `before-all` command in the Linux cibuildwheel configuration was using improper shell logic:
```bash
yum install -y gcc-c++ || apt-get update && apt-get install -y g++
```

The issue was that:
1. `yum install -y gcc-c++` succeeded (exit code 0)
2. But then `apt-get` command doesn't exist on AlmaLinux (manylinux containers)
3. The `||` operator still tried to execute the `apt-get` part
4. `apt-get` command not found resulted in exit code 127
5. This caused the entire step to fail

## Solution Applied

### 1. Fixed pyproject.toml cibuildwheel configuration

**Before:**
```toml
[tool.cibuildwheel.linux]
before-all = "yum install -y gcc-c++ || apt-get update && apt-get install -y g++"
```

**After:**
```toml
[tool.cibuildwheel.linux]
before-all = "yum install -y gcc-c++"
```

### 2. Enhanced dependency installation

**Before:**
```toml
before-build = "pip install pybind11[global]"
```

**After:**
```toml
before-build = "pip install pybind11[global] numpy"
```

### 3. Cleaned up GitHub Actions workflow

Removed duplicate `CIBW_BEFORE_BUILD` from the workflow since it's now properly configured in `pyproject.toml`.

## Why This Fix Works

1. **Simplified approach**: Since manylinux containers use AlmaLinux/CentOS (yum-based), we only need `yum`
2. **Proper separation**: Platform-specific commands are handled in the appropriate sections
3. **Complete dependencies**: Both pybind11 and numpy are installed before building
4. **Clean configuration**: All cibuildwheel settings are centralized in pyproject.toml

## Expected Result

The Linux wheel building should now:
1. ✅ Install gcc-c++ using yum (AlmaLinux package manager)
2. ✅ Install pybind11 and numpy before building
3. ✅ Compile the C++ extension successfully
4. ✅ Generate manylinux wheels for Python 3.8-3.12

## Testing

You can test this locally with:
```bash
make ci-wheels
```

Or verify the configuration:
```bash
uv run python -c "import cibuildwheel; print('✅ cibuildwheel available')"
```
