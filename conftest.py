from __future__ import annotations

import re
from pathlib import Path
from typing import Generator, Optional

import allure
import pytest
from playwright.sync_api import Browser
from playwright.sync_api import BrowserContext
from playwright.sync_api import Page
from playwright.sync_api import Playwright
from playwright.sync_api import sync_playwright

from config.settings import Settings, get_settings


ARTIFACTS_DIR = Path("artifacts")
TRACE_DIR = ARTIFACTS_DIR / "traces"
VIDEO_DIR = ARTIFACTS_DIR / "videos"


def _safe_test_name(nodeid: str) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9_.-]+", "_", nodeid)
    return sanitized.strip("_") or "test"


def _attach_failure_screenshot(page: Page) -> None:
    screenshot = page.screenshot(full_page=True)
    allure.attach(
        screenshot,
        name="failure_screenshot",
        attachment_type=allure.attachment_type.PNG,
    )


def _save_trace(context: BrowserContext, nodeid: str) -> Path:
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    trace_path = TRACE_DIR / f"trace_{_safe_test_name(nodeid)}.zip"
    context.tracing.stop(path=str(trace_path))
    allure.attach.file(
        str(trace_path),
        name="playwright_trace",
        attachment_type=allure.attachment_type.ZIP,
    )
    return trace_path


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
            if page is not None:
                try:
                    _attach_failure_screenshot(page)
                    item._screenshot_attached = True
                except Exception:
                    item._screenshot_attached = False


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
        record_video_dir: Optional[Path] = None
        if config.video_mode != "off":
            VIDEO_DIR.mkdir(parents=True, exist_ok=True)
            record_video_dir = VIDEO_DIR

        context = browser.new_context(
            base_url=config.base_url,
            record_video_dir=str(record_video_dir) if record_video_dir else None,
        )

        if config.trace_mode != "off":
            context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page_obj = context.new_page()
        request.node._page = page_obj
        request.node._screenshot_attached = False

        yield page_obj

        rep = getattr(request.node, "rep_call", None)
        failed = rep is not None and rep.failed

        if failed and not request.node._screenshot_attached:
            try:
                _attach_failure_screenshot(page_obj)
            except Exception:
                pass

        if config.trace_mode != "off":
            if failed or config.trace_mode == "on":
                try:
                    _save_trace(context, request.node.nodeid)
                except Exception:
                    context.tracing.stop()
            else:
                context.tracing.stop()

        context.close()

        if config.video_mode == "retain-on-failure" and not failed:
            try:
                if page_obj.video:
                    video_path = page_obj.video.path()
                    Path(video_path).unlink(missing_ok=True)
            except Exception:
                pass

        browser.close()
