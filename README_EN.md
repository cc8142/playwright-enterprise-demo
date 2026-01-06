# Playwright Enterprise Demo

This repository showcases a production-ready UI automation framework built with
Playwright (Sync API), Pytest, and Allure, following strict POM, type safety,
and robust base abstractions suitable for enterprise teams.

## Tech Stack

- Python 3.10+
- Playwright (Sync API)
- Pytest
- Allure
- Poetry

## Project Structure

```
.
├── .github/workflows/playwright.yml
├── config/
├── pages/
├── tests/
├── utils/
├── conftest.py
├── pyproject.toml
├── requirements.txt
└── README_EN.md
```

## Key Engineering Practices

- Strict POM: no raw selectors in tests
- BasePage encapsulates explicit waits, error handling, and element highlighting
- Auto screenshot + trace on failure (Allure attachments)
- CI uploads `allure-results` and Playwright `artifacts`

## Local Setup

### Install dependencies with Poetry

```
poetry install --no-interaction --no-root
poetry run playwright install --with-deps
```

### Run tests

```
poetry run pytest -q --alluredir=allure-results
```

### Generate Allure report

```
allure generate allure-results -o allure-report --clean
```

## CI / DevOps (GitHub Actions)

Workflow: `.github/workflows/playwright.yml`

- Triggers on push/PR to `main`
- Installs Poetry and dependencies
- Installs Playwright browsers
- Runs Pytest
- Uploads `allure-results` and `artifacts` as workflow artifacts

To generate Allure HTML in CI, add:

```
allure generate allure-results -o allure-report --clean
```

and upload `allure-report` as an artifact.
