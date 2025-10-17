# Contributing to AIDeveloperTool

Thank you for your interest in contributing to AIDeveloperTool! This guide will help you get started.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip

### Setting Up Development Environment

1. **Fork and Clone the Repository**

```bash
git clone https://github.com/holbizmetrics/AIBuilderHub.git
cd AIBuilderHub
```

2. **Create a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Development Dependencies**

```bash
pip install -e ".[dev]"
```

4. **Verify Installation**

```bash
pytest tests/
```

## Project Structure

```
AIBuilderHub/
├── src/aidevelopertool/     # Main package
│   ├── core/                # Core components
│   ├── setup/               # Setup automation
│   ├── context/             # Context management
│   ├── feedback/            # Feedback tracking
│   └── pipeline/            # Pipeline management
├── tests/                   # Test suite
├── examples/                # Usage examples
├── docs/                    # Documentation
└── setup.py                 # Package configuration
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Write code following the existing style
- Add tests for new functionality
- Update documentation as needed

### 3. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=aidevelopertool tests/

# Run specific test file
pytest tests/test_core.py -v
```

### 4. Format and Lint Code

```bash
# Format code
black src/ tests/

# Check code style
flake8 src/

# Type checking
mypy src/
```

### 5. Commit Changes

```bash
git add .
git commit -m "Add feature: description of your changes"
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Adding a New Component

To add a new component to AIDeveloperTool:

1. **Create Component Class**

```python
# src/aidevelopertool/mymodule/component.py
from ..core.component import Component
from typing import Dict, Any, Optional

class MyComponent(Component):
    """Description of your component."""
    
    def __init__(self, name: str = "mycomponent", config: Optional[Dict[str, Any]] = None):
        super().__init__(name, config)
        # Initialize your component-specific attributes
    
    def initialize(self) -> bool:
        """Initialize the component."""
        # Your initialization logic
        self._initialized = True
        return True
    
    def validate(self) -> bool:
        """Validate component state."""
        # Your validation logic
        return True
    
    def get_status(self) -> Dict[str, Any]:
        """Get component status."""
        return {
            "enabled": self.is_enabled(),
            "initialized": self.is_initialized(),
            # Your custom status fields
        }
```

2. **Add Module Init**

```python
# src/aidevelopertool/mymodule/__init__.py
"""My module initialization."""
from .component import MyComponent

__all__ = ["MyComponent"]
```

3. **Export in Main Package**

```python
# src/aidevelopertool/__init__.py
from .mymodule.component import MyComponent

__all__ = [
    # ... existing exports
    "MyComponent",
]
```

4. **Add Tests**

```python
# tests/test_mycomponent.py
import pytest
from aidevelopertool.mymodule import MyComponent

def test_component_creation():
    """Test component creation."""
    comp = MyComponent()
    assert comp.name == "mycomponent"
    assert comp.initialize()

# Add more tests...
```

5. **Update Documentation**

Add your component to:
- README.md (features section)
- docs/API.md (API reference)
- docs/CONFIGURATION.md (configuration options)

## Code Style Guidelines

### Python Style

- Follow PEP 8
- Use type hints
- Write docstrings for all public functions/classes
- Maximum line length: 100 characters

### Docstring Format

```python
def my_function(param1: str, param2: int) -> bool:
    """Short description of function.
    
    Longer description if needed. Explain what the function does,
    any important notes, etc.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When this happens
    """
    pass
```

### Test Guidelines

- One test file per module (test_module.py)
- Descriptive test names (test_function_does_something)
- Use pytest fixtures for common setup
- Aim for high test coverage
- Test both success and failure cases

## Types of Contributions

### Bug Reports

When reporting bugs, include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/stack traces

### Feature Requests

When requesting features:
- Describe the problem you're trying to solve
- Explain your proposed solution
- Consider how it fits with existing functionality
- Provide examples of usage

### Documentation

Documentation improvements are always welcome:
- Fix typos or unclear explanations
- Add examples
- Improve API documentation
- Write tutorials

### Code Contributions

Code contributions should:
- Solve a clear problem
- Include tests
- Update documentation
- Follow code style guidelines
- Not break existing functionality

## Testing

### Running Specific Tests

```bash
# Run one test file
pytest tests/test_core.py

# Run one test function
pytest tests/test_core.py::test_component_creation

# Run tests matching a pattern
pytest -k "environment"
```

### Writing Tests

```python
import pytest
from aidevelopertool.mymodule import MyComponent

def test_basic_functionality():
    """Test basic component functionality."""
    comp = MyComponent()
    comp.initialize()
    assert comp.is_initialized()

def test_with_config():
    """Test component with configuration."""
    config = {"setting": "value"}
    comp = MyComponent(config=config)
    assert comp.config["setting"] == "value"

def test_error_handling():
    """Test error handling."""
    comp = MyComponent()
    with pytest.raises(ValueError):
        comp.invalid_operation()
```

## Review Process

1. All contributions go through code review
2. Tests must pass
3. Code must follow style guidelines
4. Documentation must be updated
5. At least one maintainer approval required

## Questions?

If you have questions:
- Check existing documentation
- Look at examples
- Review existing code
- Ask in GitHub issues/discussions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
