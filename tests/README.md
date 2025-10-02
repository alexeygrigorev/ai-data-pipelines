# Testing Structure for AI Data Pipelines

This directory contains comprehensive tests for the AI data pipelines project using pytest.

## Structure

```
tests/
├── __init__.py
├── conftest.py                    # Pytest configuration and fixtures
├── common/                        # Tests for common utilities
│   ├── __init__.py
│   ├── test_chunking.py          # Tests for document chunking
│   └── test_indexing.py          # Tests for document indexing
└── [module_name]/                 # Tests for each module
    ├── __init__.py
    └── test_[module_name].py
```

## Running Tests

### Run all tests
```bash
uv run pytest
```

### Run tests for a specific module
```bash
uv run pytest tests/common/ -v
```

### Run tests with coverage
```bash
uv run pytest --cov=common tests/common/
```

### Run a specific test
```bash
uv run pytest tests/common/test_chunking.py::TestSlidingWindow::test_sliding_window_with_string -v
```

## Test Categories

### Unit Tests
- Test individual functions and methods
- Use real dependencies (not mocked) where practical
- Focus on edge cases and error conditions

### Integration Tests
- Test module interactions
- Test with actual external dependencies
- Verify end-to-end functionality

## Writing Tests

Each module should have corresponding tests that:

1. **Test the happy path** - Normal usage scenarios
2. **Test edge cases** - Empty inputs, boundary conditions
3. **Test error conditions** - Invalid inputs, exceptions
4. **Test different input types** - Various data formats where applicable
5. **Test integration** - How functions work together

### Example Test Structure

```python
"""
Tests for [module_name] module.
"""

from [module_name] import main_function


class TestMainFunction:
    """Test cases for the main_function."""

    def test_basic_functionality(self):
        """Test basic usage."""
        result = main_function("test input")
        assert result is not None
        
    def test_edge_cases(self):
        """Test edge cases."""
        result = main_function("")
        assert result == expected_empty_result
        
    def test_error_conditions(self):
        """Test error handling."""
        with pytest.raises(ValueError):
            main_function(None)
```

## Dependencies

- `pytest>=8.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- All project dependencies are available for testing

## Configuration

Test configuration is in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"
python_classes = "Test*"
```