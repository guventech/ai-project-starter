# Quality gates

## Starter checks (configured)
- `python scripts/validate_starter.py`: required files and Cursor metadata.
- `python -m unittest discover -s tests -v`: validator failure detection.
CI runs both on Linux and Windows using Python 3.12.

## Application checks (not configured)
After stack selection, record exact commands, prerequisites and owners for formatting,
linting, type checks if applicable, unit/integration tests, build, dependency scanning,
secrets scanning and critical user-flow tests. Wire them into CI before shipping an app.
For web projects include accessibility and browser checks; for data changes test migrations and rollback.
Missing checks are unconfigured, never implicitly passed. Require the relevant CI checks through repository settings.
