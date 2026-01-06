from __future__ import annotations

import re
from pathlib import Path
from typing import Generator

import allure
import pytest
from playwright.sync_api import Browser
from playwright.sync_api import BrowserContext
from playwright.sync_api import Page
from playwright.sync_api import sync_playwright


def _safe_test_name(nodeid: str) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9_.-]+", "_", nodeid)
    return sanitized.strip("_") or "test"


def _attach_failure_artifacts(page: Page, context: BrowserContext, nodeid: str) -> None:
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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> Generator[None, None, None]:
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        item.rep_call = rep


@pytest.fixture(scope="function")
def page(request: pytest.FixtureRequest) -> Generator[Page, None, None]:
    with sync_playwright() as playwright:
        browser: Browser = playwright.chromium.launch(headless=True)
        context: BrowserContext = browser.new_context()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page_obj: Page = context.new_page()

        yield page_obj

        rep = getattr(request.node, "rep_call", None)
        if rep is not None and rep.failed:
            try:
                _attach_failure_artifacts(page_obj, context, request.node.nodeid)
            except Exception:
                context.tracing.stop()
        else:
            context.tracing.stop()

        context.close()
        browser.close()
