.PHONY: help install install-dev test coverage lint format clean run-example

help:
	@echo "Policy Rating Module - Development Commands"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install       Install package in production mode"
	@echo "  install-dev   Install package with development dependencies"
	@echo "  test          Run tests"
	@echo "  coverage      Run tests with coverage report"
	@echo "  lint          Run linting checks"
	@echo "  format        Format code with black"
	@echo "  clean         Remove build artifacts and cache files"
	@echo "  run-example   Run the example script"

install:
	pip install -e .

install-dev:
	pip install -e .
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v

coverage:
	pytest tests/ -v --cov=src/policy_rating --cov-report=html --cov-report=term
	@echo ""
	@echo "Coverage report generated in htmlcov/index.html"

lint:
	@echo "Running flake8..."
	flake8 src tests
	@echo "Running black check..."
	black --check src tests
	@echo "All linting checks passed!"

format:
	@echo "Formatting code with black..."
	black src tests
	@echo "Code formatted successfully!"

clean:
	@echo "Cleaning up..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "Cleanup complete!"

run-example:
	python example.py
