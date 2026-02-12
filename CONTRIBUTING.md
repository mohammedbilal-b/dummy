# Contributing to Policy Rating Module

Thank you for considering contributing to the Policy Rating Module! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/dummy.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Install development dependencies: `pip install -r requirements-dev.txt`

## Development Workflow

### Setting Up Your Environment

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### Making Changes

1. Make your changes in a feature branch
2. Write or update tests for your changes
3. Ensure all tests pass: `pytest`
4. Format your code: `black src tests`
5. Lint your code: `flake8 src tests`
6. Check types: `mypy src`

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=policy_rating --cov-report=html

# Run specific test file
pytest tests/test_policy_rater.py

# Run specific test
pytest tests/test_policy_rater.py::TestPolicyRater::test_calculate_premium_low_risk
```

### Code Style

- Follow PEP 8 style guidelines
- Use Black for code formatting (line length: 100)
- Use type hints where appropriate
- Write docstrings for all public modules, classes, and functions
- Keep functions focused and modular

### Commit Messages

- Use clear and descriptive commit messages
- Start with a verb in present tense (e.g., "Add", "Fix", "Update")
- Keep the first line under 72 characters
- Add a blank line and more details if needed

Example:
```
Add support for additional policy types

- Implement Travel insurance policy type
- Add tests for new policy type
- Update documentation
```

### Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update tests to cover your changes
3. Ensure all tests pass and code quality checks pass
4. Update documentation if you've changed APIs
5. Submit a pull request with a clear description of the changes

### What We're Looking For

- Bug fixes
- New features that fit the project scope
- Documentation improvements
- Test coverage improvements
- Performance improvements
- Code quality improvements

### Testing Guidelines

- Write unit tests for all new functions and methods
- Write integration tests for new features
- Aim for high test coverage (>90%)
- Test edge cases and error conditions
- Use descriptive test names that explain what is being tested

### Documentation Guidelines

- Update README.md for user-facing changes
- Add docstrings to all public APIs
- Include examples in docstrings where helpful
- Keep documentation clear and concise

## Questions?

Feel free to open an issue for any questions or concerns.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
