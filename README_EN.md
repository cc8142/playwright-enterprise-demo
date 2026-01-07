# Playwright Enterprise Demo

This repo showcases a production-grade UI automation framework built with
Playwright (Sync API), Pytest, and Allure. It emphasizes strict POM, type safety,
robust waits, and enterprise-ready failure evidence.

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
├── pytest.ini
└── README_EN.md
```

## Key Engineering Practices

- Strict POM: no raw selectors in tests
- BasePage wraps waits, error handling, and highlight for demo visibility
- Failure evidence policy (default on):
  - screenshot: only-on-failure
  - trace: retain-on-failure
  - video: retain-on-failure (optional)
- CI uploads `allure-results` and `artifacts`

## Configuration (multi-env)

Supports `config/{dev,staging,prod}.yaml` and `ENV=staging` selection.
YAML uses the same `APP_*` keys as environment variables (e.g. `APP_BASE_URL`).
`dev` includes public SwagLabs demo credentials for clone-and-run; override via env or `.env`.
Secrets should be injected via environment variables or GitHub Secrets:

```
APP_BASE_URL=https://www.saucedemo.com/
APP_TIMEOUT=10000
APP_HEADLESS=true
APP_BROWSER=chromium
APP_USERNAME=CHANGEME
APP_PASSWORD=CHANGEME
APP_TRACE_MODE=retain-on-failure
APP_VIDEO_MODE=off
APP_ENV=dev
```

For local runs, copy `.env.example` to `.env` (not committed).

## Local Run

### Install dependencies with Poetry

```
poetry install --no-interaction --no-root
poetry run playwright install --with-deps
```

### Run tests

```
poetry run pytest
```

### Generate Allure report

```
allure generate allure-results -o allure-report --clean
```

## CI / DevOps (GitHub Actions)

Workflow: `.github/workflows/playwright.yml`

- Triggers on push/PR to `main`
- Poetry and Playwright browser cache
- Parallel execution with pytest-xdist (`-n auto`)
- Uploads `allure-results` and `artifacts`
- Generates Allure HTML and publishes to GitHub Pages
