# Playwright Enterprise Test Framework

![Build Status](https://img.shields.io/github/actions/workflow/status/cc8142/playwright-enterprise-demo/playwright.yml?branch=main)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Playwright](https://img.shields.io/badge/Playwright-Sync-green.svg)

A production-ready UI automation framework built with **Playwright (Sync)**, **Pytest**, and **Allure**.
Designed for scalability, stability, and maintainability, demonstrating strict **Page Object Model (POM)** and enterprise-grade configuration management.

## Key Features

- **Strict POM Architecture**: Enforces separation of concerns; no raw selectors in test logic.
- **Robust Interactions**: `BasePage` encapsulation handles dynamic elements, auto-waiting, and visual highlighting.
- **Type Safety**: Fully typed Python code (Type Hints) for better IDE support and fewer bugs.
- **Configuration Management**: Powered by `pydantic-settings` to handle multiple environments (Dev/Staging/Prod) securely.
- **Observability**:
  - Automatic screenshot capture on failure.
  - Playwright Traces attached to Allure reports for "time-travel" debugging.
- **CI/CD Integration**: GitHub Actions workflow with artifact retention and automated reporting.

## Project Structure

```text
.
├── .github/workflows/  # CI/CD pipelines
├── config/             # Environment configurations (YAML + Pydantic)
├── pages/              # Page Objects (Business Logic)
├── tests/              # Test Cases (Pytest)
├── utils/              # Shared utilities
├── conftest.py         # Global fixtures & hooks
├── pyproject.toml      # Dependency management (Poetry)
└── README.md
