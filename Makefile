SHELL := /bin/bash

.PHONY: install test report lint format typecheck pre-commit

install:
	poetry install --no-interaction --no-root
	poetry run playwright install --with-deps

test:
	poetry run pytest

report:
	allure generate allure-results -o allure-report --clean

lint:
	poetry run ruff check .
	poetry run isort --check-only .

format:
	poetry run black .
	poetry run isort .

typecheck:
	poetry run mypy .

pre-commit:
	poetry run pre-commit run --all-files
