# Contributing to System Monitor API

Thank you for considering contributing to System Monitor API! We welcome contributions from everyone.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (OS, Python version, etc.)
- Any relevant logs or error messages

### Suggesting Features

Feature requests are welcome! Please open an issue with:
- A clear description of the feature
- Why this feature would be useful
- Any implementation ideas you have

### Code Contributions

1. **Fork the repository** and create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clean, readable code
   - Follow PEP 8 style guidelines
   - Add docstrings to functions and classes
   - Add type hints where appropriate

3. **Test your changes**:
   - Ensure existing tests pass
   - Add new tests for new features
   - Test on multiple platforms if possible

4. **Commit your changes**:
   ```bash
   git commit -m "Add feature: brief description"
   ```
   - Use clear, descriptive commit messages
   - Reference issue numbers if applicable

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**:
   - Provide a clear description of the changes
   - Reference any related issues
   - Ensure CI checks pass

## Code Style

- Follow [PEP 8](https://pep8.org/) Python style guide
- Use meaningful variable and function names
- Keep functions small and focused
- Add comments for complex logic
- Use type hints for function parameters and return values

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/navuluri/system-monitor-backend.git
   cd system-monitor-backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `config.ini` file from the example:
   ```bash
   cp config.ini.example config.ini
   ```

5. Run the application:
   ```bash
   python -m system_monitor.main
   ```

## Testing

Run tests with:
```bash
pytest
```

## Documentation

- Update README.md if you add new features or change functionality
- Add docstrings to new functions and classes
- Update API documentation comments

## Questions?

Feel free to open an issue with the label "question" if you need help or clarification.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions

Thank you for contributing! 🎉

