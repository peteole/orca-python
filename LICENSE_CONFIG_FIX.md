# License Configuration Fix for Cibuildwheel

## Problem
Cibuildwheel was failing with a configuration error in the `pyproject.toml` file:

```
configuration error: `project.license` must be valid exactly by one definition (2 matches found)
```

The error occurred because the license was configured as:
```toml
license = "GPL-3.0"
```

But the modern pyproject.toml specification requires license to be either:
1. `{text = "SPDX-License-Expression"}` 
2. `{file = "path/to/license/file"}`

## Solution Applied

### Fixed License Configuration
**Before:**
```toml
license = "GPL-3.0"
```

**After:**
```toml
license = {text = "GPL-3.0-only"}
```

### Why This Works
- ✅ **Valid format**: Uses the `{text = "..."}` structure required by PEP 621
- ✅ **SPDX compliant**: `GPL-3.0-only` is a valid SPDX license expression
- ✅ **Cibuildwheel compatible**: Now passes validation during wheel building
- ✅ **Backward compatible**: Maintains GPL-3.0 licensing intent

### Additional Cleanup
- **Removed build artifacts**: Cleaned all `.so` files that could interfere with cibuildwheel
- **Used `make clean`**: Ensures clean build environment

## Testing Results

### Local Build Success ✅
```bash
make clean && make wheel
# Successfully creates: dist/orca_graphlets-0.1.0-cp312-cp312-macosx_14_0_arm64.whl
```

### Configuration Validation ✅
```bash
uv run python -c "import toml; print(toml.load('pyproject.toml')['project']['license'])"
# Output: {'text': 'GPL-3.0-only'}
```

## Expected Cibuildwheel Result

The GitHub Actions workflow should now:

1. ✅ **Pass validation**: No more license configuration errors
2. ✅ **Build Linux wheels**: manylinux_2_28_x86_64 for Python 3.8-3.12
3. ✅ **Build macOS wheels**: x86_64 and arm64 for Python 3.8-3.12  
4. ✅ **Build Windows wheels**: x64 for Python 3.8-3.12
5. ✅ **Generate clean artifacts**: No interference from previous builds

## Key Learnings

- **PEP 621 compliance**: Modern Python packaging requires specific license formats
- **SPDX expressions**: Use `-only` suffix for precise GPL licensing
- **Clean builds**: Always clean artifacts before running cibuildwheel
- **Testing locally**: Verify fixes with `make wheel` before pushing to CI

The cibuildwheel process should now complete successfully on all platforms! 🎉
