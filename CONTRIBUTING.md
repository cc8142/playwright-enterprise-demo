# Contributing

Thanks for your interest in contributing.

## Development setup

- Install dependencies: `poetry install --no-interaction --no-root`
- Install Playwright browsers: `poetry run playwright install --with-deps`

## Run tests

- `poetry run pytest`

## Code quality

- Lint/format: `poetry run ruff check .` and `poetry run black .`
- Import order: `poetry run isort .`
- Type checks: `poetry run mypy .`

## Pre-commit

- Install hooks: `poetry run pre-commit install`
- Run on all files: `poetry run pre-commit run --all-files`
