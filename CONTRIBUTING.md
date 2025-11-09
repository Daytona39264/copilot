# Contributing to School Activities AI Project

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Submitting Changes](#submitting-changes)
- [Resources](#resources)

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- Docker (optional, for containerized development)
- Anthropic API key (optional, for AI features)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/copilot.git
   cd copilot
   ```
3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/Daytona39264/copilot.git
   ```

## 💻 Development Setup

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 4. Run Tests

```bash
python test_all.py
```

## 📁 Project Structure

```
.
├── src/                    # Main application code
│   ├── app.py             # FastAPI application with AI endpoints
│   └── static/            # Static files
├── examples/              # Example implementations
│   ├── anthropic_sdk/     # Anthropic SDK examples
│   ├── mcp_server/        # MCP server implementations
│   └── docker/            # Docker configurations
├── tests/                 # Test files
│   ├── test_ai_features.py
│   └── test_mcp_server.py
├── AI_FEATURES.md         # AI features documentation
├── TESTING_GUIDE.md       # Testing documentation
└── test_all.py            # Comprehensive test runner
```

## 🔧 Making Changes

### Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### Types of Changes

- **Features**: New functionality
- **Bugfixes**: Bug fixes
- **Docs**: Documentation updates
- **Tests**: Test additions or improvements
- **Refactor**: Code refactoring

### Commit Messages

Follow this format:

```
<type>: <subject>

<body>

<footer>
```

**Example:**
```
feat: Add AI-powered activity recommendations

- Implement personalized suggestions based on student interests
- Add new /ai/suggest-activities endpoint
- Include comprehensive tests

Closes #123
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `style`: Code style changes
- `chore`: Build process or auxiliary tool changes

## 🧪 Testing

### Run All Tests

```bash
python test_all.py
```

### Run Specific Test Suites

```bash
# AI features tests
python -m pytest tests/test_ai_features.py -v

# MCP server tests
python -m pytest tests/test_mcp_server.py -v

# Run with coverage
python -m pytest --cov=src --cov=examples/mcp_server --cov-report=html
```

### Manual Testing

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed manual testing procedures.

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Use descriptive test names
- Include docstrings explaining what the test does
- Test both success and failure cases

**Example:**
```python
def test_ai_status_endpoint():
    """Test that AI status endpoint returns correct format"""
    response = client.get("/ai/status")
    assert response.status_code == 200
    data = response.json()
    assert "ai_enabled" in data
    assert "message" in data
```

## 📝 Code Style

### Python Style Guide

- Follow [PEP 8](https://pep8.org/)
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use meaningful variable names

### Code Formatting

```bash
# Format code with black (recommended)
pip install black
black src/ examples/ tests/

# Check code style
pip install flake8
flake8 src/ examples/ tests/
```

### Documentation

- Add docstrings to all functions and classes
- Use Google-style docstrings
- Update relevant README files
- Include examples in docstrings

**Example:**
```python
def calculate_availability(activity_name: str) -> dict:
    """
    Calculate availability for an activity.

    Args:
        activity_name: Name of the activity to check

    Returns:
        Dictionary with availability details including:
        - has_availability: boolean
        - available_spots: int
        - total_capacity: int

    Raises:
        ValueError: If activity_name is not found

    Example:
        >>> calculate_availability("Chess Club")
        {'has_availability': True, 'available_spots': 10, 'total_capacity': 12}
    """
    # Implementation
```

## 📤 Submitting Changes

### Before Submitting

1. **Update your branch:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run all tests:**
   ```bash
   python test_all.py
   ```

3. **Check code style:**
   ```bash
   flake8 src/ examples/ tests/
   ```

4. **Update documentation** if needed

### Create Pull Request

1. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Go to GitHub and create a Pull Request

3. Fill in the PR template:
   - **Title**: Clear, descriptive title
   - **Description**: What changes were made and why
   - **Testing**: How the changes were tested
   - **Screenshots**: If applicable

4. Link related issues

### PR Review Process

- Maintainers will review your PR
- Address any feedback
- Once approved, your PR will be merged

## 📚 Resources

### Documentation

- [AI Features Guide](AI_FEATURES.md)
- [Testing Guide](TESTING_GUIDE.md)
- [Anthropic SDK Examples](examples/anthropic_sdk/README.md)
- [MCP Server Guide](examples/mcp_server/README.md)
- [Docker Deployment](examples/docker/README.md)

### External Resources

- [Anthropic Documentation](https://docs.anthropic.com)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Pytest Documentation](https://docs.pytest.org)
- [Docker Documentation](https://docs.docker.com)

## 🤝 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

## 💡 Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Open a GitHub Issue
- **Security**: Email the maintainers directly

## 🎉 Recognition

Contributors will be recognized in:
- GitHub contributors page
- Release notes
- Project documentation

Thank you for contributing! 🚀
