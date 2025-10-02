"""
Pytest configuration and fixtures for ai-data-pipelines tests.

This module provides common test configuration and fixtures that can be
used across all test modules.
"""

import sys
from pathlib import Path

# Add the project root to the Python path so imports work
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))