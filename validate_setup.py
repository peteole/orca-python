#!/usr/bin/env python3
"""
Validation script for ORCA Python package setup
"""

import sys
from pathlib import Path


def check_files():
    """Check if all required files are present"""
    required_files = [
        "setup.py",
        "pyproject.toml",
        "README.md",
        "LICENSE",
        "Makefile",
        "requirements-dev.txt",
        "src/orca.cpp",
        "src/orca.h",
        "python/pybind11_wrapper.cpp",
        ".github/workflows/build.yml",
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print("❌ Missing files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    else:
        print("✅ All required files present")
        return True


def check_setup_py():
    """Check setup.py configuration"""
    try:
        with open("setup.py", "r") as f:
            content = f.read()

        checks = [
            ("Tomaz Hocevar", "Original author"),
            ("GPLv3", "GPL license"),
            ("pybind11", "pybind11 dependency"),
            ("orca-graphlets", "Package name"),
            ("python/pybind11_wrapper.cpp", "Wrapper file"),
        ]

        all_good = True
        for check, description in checks:
            if check in content:
                print(f"✅ {description} found in setup.py")
            else:
                print(f"❌ {description} missing from setup.py")
                all_good = False

        return all_good

    except Exception as e:
        print(f"❌ Error reading setup.py: {e}")
        return False


def check_pyproject_toml():
    """Check pyproject.toml configuration"""
    try:
        with open("pyproject.toml", "r") as f:
            content = f.read()

        checks = [
            ("pybind11", "pybind11 build dependency"),
            ("[tool.uv]", "uv configuration"),
            ("[tool.cibuildwheel]", "cibuildwheel configuration"),
            ("GPL-3.0", "GPL license"),
        ]

        all_good = True
        for check, description in checks:
            if check in content:
                print(f"✅ {description} found in pyproject.toml")
            else:
                print(f"❌ {description} missing from pyproject.toml")
                all_good = False

        return all_good

    except Exception as e:
        print(f"❌ Error reading pyproject.toml: {e}")
        return False


def main():
    """Run all validation checks"""
    print("🔍 Validating ORCA Python package setup...")
    print("=" * 50)

    checks = [
        ("File structure", check_files),
        ("setup.py configuration", check_setup_py),
        ("pyproject.toml configuration", check_pyproject_toml),
    ]

    all_passed = True
    for check_name, check_func in checks:
        print(f"\n📋 Checking {check_name}:")
        if not check_func():
            all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All validation checks passed!")
        print("\n📋 Next steps:")
        print("1. Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("2. Create venv: uv venv --python 3.11")
        print("3. Install deps: uv pip install -r requirements-dev.txt")
        print("4. Build: make build")
        print("5. Test: make test")
    else:
        print("❌ Some validation checks failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
