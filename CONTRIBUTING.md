# Contributing to TableQA

Thank you for your interest in contributing to TableQA! This document provides guidelines and instructions for development.

## Development Setup

### 1. Install Dependencies

```bash
# Install the package in development mode with all dependencies
pip install -e ".[dev,docs]"

# Or use the Makefile
make install
```

### 2. Install Pre-commit Hooks

Pre-commit hooks ensure code quality by running checks before each commit:

```bash
# Install pre-commit
pip install pre-commit

# Install the hooks
pre-commit install

# Or use the Makefile
make install-pre-commit
```

The pre-commit hooks will automatically:
- Run ruff linting and formatting
- Run type checking with mypy
- Run all tests with pytest
- Check for trailing whitespace, file endings, etc.

You can also run pre-commit manually:

```bash
# Run on all files
pre-commit run --all-files

# Or use the Makefile
make pre-commit
```

## Testing

### Local Testing

```bash
# Run all tests with coverage
make test

# Run tests without coverage (faster)
make test-fast

# Or directly with pytest
python -m pytest -v
```

### Testing GitHub Actions Locally with Act

We use [act](https://github.com/nektos/act) to test GitHub Actions workflows locally before pushing:

```bash
# List all available workflows
make act-list

# Run the CI workflow
make act-ci

# Dry run (see what would run)
make act-dry-run

# Or use act directly
./bin/act push -W .github/workflows/ci.yml
```

**Note**: Act requires Docker to be running.

## Code Quality

### Linting

```bash
# Check for linting issues
make lint

# Automatically fix linting issues
make lint-fix
```

### Formatting

```bash
# Format code with ruff
make format

# Check if code is formatted
make format-check
```

### Type Checking

```bash
# Run type checking with mypy
make typecheck
```

### Run All CI Checks Locally

Before pushing, you can run all CI checks locally:

```bash
make ci-local
```

This will run:
1. Ruff linting
2. Type checking with mypy
3. All tests with coverage

## Development Workflow

### Recommended Workflow

1. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and ensure they follow the code style:
   ```bash
   make format
   ```

3. **Run tests** to ensure nothing broke:
   ```bash
   make test
   ```

4. **Test locally with act** (optional but recommended):
   ```bash
   make act-ci
   ```

5. **Run all CI checks**:
   ```bash
   make ci-local
   ```

6. **Commit your changes** (pre-commit hooks will run automatically):
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

   If the pre-commit hooks fail, fix the issues and try again.

7. **Push your changes**:
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request** on GitHub

### Tips

- The pre-commit hooks will prevent commits if tests fail or code doesn't meet quality standards
- Use `git commit --no-verify` to bypass hooks if absolutely necessary (not recommended)
- Run `make ci-local` before pushing to catch issues early
- Use `make act-ci` to test GitHub Actions workflows locally

## Common Commands

```bash
make help          # Show all available commands
make install       # Install package in development mode
make test          # Run tests with coverage
make lint          # Check for linting issues
make format        # Format code
make clean         # Remove build artifacts
make ci-local      # Run all CI checks locally
make act-ci        # Test GitHub Actions locally
```

## Code Style

- We use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting
- Line length: 100 characters
- Follow PEP 8 with Ruff's recommended rules
- Use type hints for all functions
- Write docstrings for all public functions and classes

## Testing Guidelines

- Write tests for all new features
- Maintain or improve code coverage
- Use descriptive test names
- Use fixtures from `conftest.py` where applicable

## Questions?

If you have questions or need help, please:
- Open an issue on GitHub
- Check existing issues and discussions
- Review the documentation

Thank you for contributing to TableQA!
