from __future__ import annotations

import re
from pathlib import Path
from typing import Generator

import allure
import pytest
from playwright.sync_api import Browser
from playwright.sync_api import BrowserContext
from playwright.sync_api import Page
from playwright.sync_api import Playwright
from playwright.sync_api import sync_playwright

from config.settings import Settings, get_settings


def _safe_test_name(nodeid: str) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9_.-]+", "_", nodeid)
    return sanitized.strip("_") or "test"


def _attach_failure_artifacts(
    page: Page,
    context: BrowserContext,
    nodeid: str,
) -> None:
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    screenshot = page.screenshot(full_page=True)
    allure.attach(
        screenshot,
        name="failure_screenshot",
        attachment_type=allure.attachment_type.PNG,
    )

    trace_path = artifacts_dir / f"trace_{_safe_test_name(nodeid)}.zip"
    context.tracing.stop(path=str(trace_path))
    allure.attach.file(
        str(trace_path),
        name="playwright_trace",
        attachment_type=allure.attachment_type.ZIP,
    )


def _get_browser(playwright: Playwright, settings: Settings) -> Browser:
    if settings.browser == "firefox":
        return playwright.firefox.launch(headless=settings.headless)
    return playwright.chromium.launch(headless=settings.headless)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item,
    call: pytest.CallInfo,
) -> Generator[None, None, None]:
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        item.rep_call = rep
        if rep.failed:
            page = getattr(item, "_page", None)
            context = getattr(item, "_context", None)
            if page is not None and context is not None:
                try:
                    _attach_failure_artifacts(page, context, item.nodeid)
                    item._artifacts_attached = True
                except Exception:
                    item._artifacts_attached = False


@pytest.fixture(scope="session")
def config() -> Settings:
    return get_settings()


@pytest.fixture(scope="session")
def base_url(config: Settings) -> str:
    return config.base_url


@pytest.fixture(scope="function")
def page(
    request: pytest.FixtureRequest,
    config: Settings,
) -> Generator[Page, None, None]:
    with sync_playwright() as playwright:
        browser = _get_browser(playwright, config)
        context = browser.new_context(base_url=config.base_url)
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page_obj = context.new_page()
        request.node._page = page_obj
        request.node._context = context
        request.node._artifacts_attached = False

        yield page_obj

        rep = getattr(request.node, "rep_call", None)
        if rep is not None and rep.failed and not request.node._artifacts_attached:
            try:
                _attach_failure_artifacts(page_obj, context, request.node.nodeid)
            except Exception:
                context.tracing.stop()
        else:
            context.tracing.stop()

        context.close()
        browser.close()
