# Makefile for ORCA Python package with uv

.PHONY: install dev build test clean wheel sdist publish help

help:  ## Show this help message
	@echo "ORCA Python Package - uv-based build system"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install package in development mode
	uv pip install -e .

dev:  ## Install development dependencies
	uv pip install -r requirements-dev.txt

build:  ## Build package in-place for development
	uv run python setup.py build_ext --inplace

test:  ## Run tests
	uv run python test_orca.py

example:  ## Run example script
	uv run python example.py

wheel:  ## Build wheel
	uv run python setup.py bdist_wheel

sdist:  ## Build source distribution
	uv run python -m build --sdist

clean:  ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info/ __pycache__/ .pytest_cache/
	find . -name "*.pyc" -delete
	find . -name "*.so" -delete

publish-test:  ## Publish to TestPyPI
	uv run python -m twine upload --repository testpypi dist/*

publish:  ## Publish to PyPI
	uv run python -m twine upload dist/*

ci-wheels:  ## Build wheels for all platforms (requires cibuildwheel)
	uv run python -m cibuildwheel --output-dir wheelhouse

setup-uv:  ## Install uv if not present
	curl -LsSf https://astral.sh/uv/install.sh | sh

venv:  ## Create virtual environment
	uv venv --python 3.11

all: clean dev build test wheel  ## Full development setup
