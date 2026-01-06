from __future__ import annotations

from typing import Dict, Optional

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Locator
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from config.settings import get_settings

DEFAULT_TIMEOUT_MS = get_settings().timeout


class BasePage:
    """Base page object providing robust element interactions."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self._maps: Dict[str, str] = {}

    def map(self, name: str) -> str:
        """Return the selector mapped to a logical name."""
        try:
            return self._maps[name]
        except KeyError as exc:
            raise KeyError(f"Selector map missing for '{name}'.") from exc

    def get_element(
        self,
        name_or_selector: str,
        *,
        use_map: bool = True,
        timeout_ms: Optional[int] = None,
    ) -> Locator:
        """Return a locator, waiting for the element to be attached."""
        if timeout_ms is None:
            timeout_ms = DEFAULT_TIMEOUT_MS
        selector = self.map(name_or_selector) if use_map else name_or_selector
        locator = self.page.locator(selector)
        try:
            locator.wait_for(state="attached", timeout=timeout_ms)
        except PlaywrightTimeoutError as exc:
            raise TimeoutError(f"Element not attached: {selector}") from exc
        return locator

    def _wait_for_actionable(
        self,
        locator: Locator,
        selector: str,
        timeout_ms: Optional[int],
    ) -> None:
        if timeout_ms is None:
            timeout_ms = DEFAULT_TIMEOUT_MS
        try:
            locator.wait_for(state="visible", timeout=timeout_ms)
        except PlaywrightTimeoutError as exc:
            raise TimeoutError(f"Element not visible: {selector}") from exc
        try:
            handle = locator.element_handle()
            if handle is None:
                raise RuntimeError(f"Element handle not available: {selector}")
            self.page.wait_for_function(
                "(el) => !el.hasAttribute('disabled') && el.getAttribute('aria-disabled') !== 'true'",
                arg=handle,
                timeout=timeout_ms,
            )
        except PlaywrightTimeoutError as exc:
            raise TimeoutError(f"Element not enabled: {selector}") from exc

    def _highlight(self, locator: Locator) -> None:
        try:
            handle = locator.element_handle()
            if handle is None:
                return
            self.page.evaluate(
                "(el) => { el.style.outline = '3px solid #ff6a00'; el.style.outlineOffset = '2px'; }",
                handle,
            )
            self.page.wait_for_timeout(150)
        except PlaywrightError:
            return

    def click(
        self,
        name_or_selector: str,
        *,
        use_map: bool = True,
        timeout_ms: Optional[int] = None,
    ) -> None:
        """Wait for and click an element with a visible highlight."""
        if timeout_ms is None:
            timeout_ms = DEFAULT_TIMEOUT_MS
        selector = self.map(name_or_selector) if use_map else name_or_selector
        locator = self.page.locator(selector)
        self._wait_for_actionable(locator, selector, timeout_ms)
        self._highlight(locator)
        try:
            locator.click(timeout=timeout_ms)
        except PlaywrightTimeoutError as exc:
            raise TimeoutError(f"Timed out clicking: {selector}") from exc
        except PlaywrightError as exc:
            raise RuntimeError(f"Failed clicking: {selector}") from exc

    def fill(
        self,
        name_or_selector: str,
        value: str,
        *,
        use_map: bool = True,
        timeout_ms: Optional[int] = None,
    ) -> None:
        """Wait for and fill an input element with a visible highlight."""
        if timeout_ms is None:
            timeout_ms = DEFAULT_TIMEOUT_MS
        selector = self.map(name_or_selector) if use_map else name_or_selector
        locator = self.page.locator(selector)
        self._wait_for_actionable(locator, selector, timeout_ms)
        self._highlight(locator)
        try:
            locator.fill(value, timeout=timeout_ms)
        except PlaywrightTimeoutError as exc:
            raise TimeoutError(f"Timed out filling: {selector}") from exc
        except PlaywrightError as exc:
            raise RuntimeError(f"Failed filling: {selector}") from exc
