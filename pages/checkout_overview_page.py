from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.checkout_complete_page import CheckoutCompletePage


class CheckoutOverviewPage(BasePage):
    """Page object for the SauceDemo checkout overview page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._maps.update(
            {
                "finish_button": "[data-test='finish']",
            }
        )

    def finish_checkout(self, timeout_ms: int = 5000) -> CheckoutCompletePage:
        """Finish checkout and return the completion page."""
        self.click("finish_button", timeout_ms=timeout_ms)
        return CheckoutCompletePage(self.page)
