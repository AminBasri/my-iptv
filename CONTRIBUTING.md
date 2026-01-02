# Contributing to Malaysian IPTV

Thank you for your interest in contributing to Malaysian IPTV! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/my-iptv.git`
3. Run setup: `./setup.sh`
4. Create a branch: `git checkout -b feature/your-feature-name`

## Project Structure

- `app/api/` - API route handlers
- `app/core/` - Core configuration and utilities
- `app/models/` - Pydantic data models
- `app/parsers/` - M3U8 and EPG parsers
- `app/services/` - Business logic layer
- `app/static/` - Frontend assets (CSS, JS)
- `app/templates/` - HTML templates

## Coding Standards

### Python Code

- Follow PEP 8 style guidelines
- Use type hints where possible
- Write docstrings for functions and classes
- Keep functions focused and small
- Use async/await for I/O operations

Example:
```python
async def fetch_channels(source: str) -> List[Channel]:
    """
    Fetch and parse channels from M3U8 source.
    
    Args:
        source: URL or file path to M3U8 playlist
        
    Returns:
        List of parsed Channel objects
    """
    ...
```

### JavaScript Code

- Use ES6+ features
- Follow consistent naming conventions
- Add comments for complex logic
- Keep functions small and focused

### CSS

- Use consistent naming (BEM or similar)
- Group related styles together
- Add comments for complex layouts
- Ensure responsive design

## Making Changes

### Adding New Features

1. Create a new branch
2. Implement your feature
3. Add/update tests if applicable
4. Update documentation
5. Submit a pull request

### Fixing Bugs

1. Create an issue describing the bug
2. Create a branch: `fix/bug-description`
3. Fix the bug
4. Add tests to prevent regression
5. Submit a pull request

## API Development

### Adding New Endpoints

1. Create model in `app/models/`
2. Add business logic in `app/services/`
3. Create route handler in `app/api/`
4. Update API documentation
5. Test the endpoint

Example:
```python
# app/api/new_feature.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/new", tags=["new"])

@router.get("/")
async def get_items():
    """Get all items."""
    return {"items": []}
```

## Frontend Development

### Adding UI Features

1. Update HTML in `app/templates/`
2. Add styles in `app/static/css/`
3. Add functionality in `app/static/js/`
4. Test in multiple browsers
5. Ensure responsive design

## Testing

### Manual Testing

```bash
# Start development server
python run.py

# Test in browser
http://localhost:8000

# Test API
http://localhost:8000/docs
```

### Testing Endpoints

```bash
# Health check
curl http://localhost:8000/health

# List channels
curl http://localhost:8000/api/channels

# Search channels
curl http://localhost:8000/api/channels/search?q=tv3
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to Python code
- Update API documentation
- Add examples where helpful

## Pull Request Process

1. Update documentation
2. Ensure code follows style guidelines
3. Test your changes thoroughly
4. Write clear commit messages
5. Create pull request with description

### PR Title Format

- `feat: Add new feature`
- `fix: Fix bug description`
- `docs: Update documentation`
- `style: Code style improvements`
- `refactor: Code refactoring`
- `test: Add or update tests`

### PR Description

Include:
- What changes were made
- Why the changes were needed
- How to test the changes
- Any breaking changes
- Screenshots (if UI changes)

## Code Review

- Be respectful and constructive
- Explain reasoning for suggestions
- Focus on code quality and maintainability
- Test the changes locally

## Getting Help

- Open an issue for questions
- Check existing issues and PRs
- Read the documentation

## Feature Requests

1. Check if feature already requested
2. Create detailed issue describing:
   - Use case
   - Expected behavior
   - Potential implementation
   - Why it's valuable

## Bug Reports

Include:
- Clear description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details
- Error messages/logs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Maintain professional communication

## Areas for Contribution

### High Priority
- Authentication system
- User management
- Advanced EPG features
- Stream quality selection
- Recording/DVR functionality

### Medium Priority
- Additional streaming protocols
- Mobile app
- Better error handling
- Performance optimizations
- Internationalization

### Nice to Have
- Social features
- Recommendations
- Watch history
- Parental controls
- Multiple user profiles

## Development Tips

### Hot Reload

```bash
uvicorn app.main:app --reload
```

### Debug Mode

Set `DEBUG=True` in `.env`

### Logging

```python
from app.core import get_logger

logger = get_logger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

## Questions?

Feel free to open an issue for any questions or clarifications needed.

Thank you for contributing! 🎉
