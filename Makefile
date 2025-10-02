# Makefile for ai-data-pipelines
# 
# This Makefile provides convenient commands for development, testing, and maintenance.

.PHONY: help install install-dev test test-coverage clean

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Installation
install: ## Install project dependencies
	uv sync

install-dev: ## Install project with development dependencies
	uv sync --dev

# Testing
test: ## Run all tests
	uv run pytest tests/ -v

test-coverage: ## Run tests with coverage report
	uv run pytest --cov=. tests/ --cov-report=term-missing --cov-report=html

# Cleaning
clean: ## Clean up generated files
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete