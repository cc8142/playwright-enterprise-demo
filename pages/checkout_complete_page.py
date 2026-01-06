from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    """Page object for the SauceDemo checkout complete page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._maps.update(
            {
                "complete_header": "[data-test='complete-header']",
            }
        )

    def is_order_complete(self, timeout_ms: int = 5000) -> bool:
        """Return True when the completion header is visible."""
        locator = self.get_element("complete_header", timeout_ms=timeout_ms)
        try:
            locator.wait_for(state="visible", timeout=timeout_ms)
        except TimeoutError:
            return False
        return True
