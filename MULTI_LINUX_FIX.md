# Multi-Linux Container Support Fix

## Problem
Cibuildwheel was failing when trying to build musllinux wheels with the error:
```
sh: yum: not found
Error: cibuildwheel: Command ['sh', '-c', 'yum install -y gcc-c++'] failed with code 127.
```

## Root Cause
Cibuildwheel now builds for multiple Linux container types:
- **manylinux** containers: Use CentOS/AlmaLinux → `yum` package manager
- **musllinux** containers: Use Alpine Linux → `apk` package manager

The previous configuration only supported `yum`:
```toml
[tool.cibuildwheel.linux]
before-all = "yum install -y gcc-c++"
```

## Solution Applied

### Updated Linux Configuration
**Before:**
```toml
[tool.cibuildwheel.linux]
before-all = "yum install -y gcc-c++"
```

**After:**
```toml
[tool.cibuildwheel.linux]
before-all = "if command -v yum >/dev/null 2>&1; then yum install -y gcc-c++; elif command -v apk >/dev/null 2>&1; then apk add --no-cache g++; else echo 'No supported package manager found'; exit 1; fi"
```

### How It Works
1. **Check for yum**: `command -v yum >/dev/null 2>&1`
   - If available → Install with: `yum install -y gcc-c++`
2. **Check for apk**: `command -v apk >/dev/null 2>&1` 
   - If available → Install with: `apk add --no-cache g++`
3. **Fallback**: If neither found → Exit with error message

### Supported Containers
- ✅ **manylinux_2_28_x86_64**: CentOS/AlmaLinux → Uses `yum install -y gcc-c++`
- ✅ **musllinux_1_2_x86_64**: Alpine Linux → Uses `apk add --no-cache g++`
- ✅ **Future containers**: Automatically detects available package manager

## Benefits

### Broader Compatibility
- **manylinux wheels**: Work on most Linux distributions (glibc-based)
- **musllinux wheels**: Work on Alpine Linux and other musl-based distributions
- **Docker support**: Both standard and Alpine-based Docker images supported

### Automatic Detection
- No manual configuration needed
- Robust fallback mechanism
- Clear error messages if unsupported

### Package Manager Commands
| Container Type | OS Base | Package Manager | Install Command |
|---------------|---------|-----------------|-----------------|
| manylinux | CentOS/AlmaLinux | yum | `yum install -y gcc-c++` |
| musllinux | Alpine Linux | apk | `apk add --no-cache g++` |

## Expected Results

The GitHub Actions workflow should now:
1. ✅ **Build manylinux wheels** using yum for gcc-c++
2. ✅ **Build musllinux wheels** using apk for g++
3. ✅ **Support Python 3.8-3.12** on both container types
4. ✅ **Generate comprehensive Linux coverage** for maximum compatibility

## Alternative Approach
If you want to skip musllinux builds for faster CI (manylinux covers most use cases):
```toml
skip = "*-win32 *-manylinux_i686 *-musllinux*"
```

But the current approach provides maximum Linux compatibility! 🐧
