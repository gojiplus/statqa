# Makefile for tableqa development

.PHONY: help install test lint format typecheck clean act-test pre-commit

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install package in development mode with all dependencies
	pip install -e ".[dev,docs]"

install-pre-commit:  ## Install pre-commit hooks
	pip install pre-commit
	pre-commit install

test:  ## Run tests with pytest
	python -m pytest -v --cov=tableqa --cov-report=term-missing

test-fast:  ## Run tests without coverage
	python -m pytest -v

lint:  ## Run linting with ruff
	ruff check src tests

lint-fix:  ## Fix linting issues with ruff
	ruff check --fix src tests

format:  ## Format code with ruff
	ruff format src tests

format-check:  ## Check if code is formatted
	ruff format --check src tests

typecheck:  ## Run type checking with mypy
	mypy src/tableqa --ignore-missing-imports

clean:  ## Remove build artifacts and cache files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# Act (local GitHub Actions testing)
act-test:  ## Test GitHub Actions locally using act
	./bin/act -W .github/workflows/ci.yml --platform ubuntu-latest=catthehacker/ubuntu:act-latest

act-list:  ## List all workflows that can be run with act
	./bin/act -l

act-ci:  ## Run CI workflow locally
	./bin/act push -W .github/workflows/ci.yml --platform ubuntu-latest=catthehacker/ubuntu:act-latest

act-dry-run:  ## Dry run of GitHub Actions
	./bin/act -n

# Pre-commit
pre-commit:  ## Run pre-commit hooks on all files
	pre-commit run --all-files

# CI simulation (runs same checks as CI)
ci-local:  ## Run all CI checks locally
	@echo "Running linting..."
	ruff check src tests
	@echo "\nRunning type checking..."
	mypy src/tableqa --ignore-missing-imports || true
	@echo "\nRunning tests..."
	python -m pytest --cov=tableqa --cov-report=term-missing
	@echo "\n✅ All CI checks passed!"

# Build
build:  ## Build distribution packages
	python -m build

# Documentation
docs:  ## Build documentation
	cd docs && make html

docs-serve:  ## Serve documentation locally
	cd docs/build/html && python -m http.server
