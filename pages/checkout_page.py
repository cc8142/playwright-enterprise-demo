from __future__ import annotations

from typing import Optional

from playwright.sync_api import Page

from config.settings import get_settings
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page object for cart and checkout flow."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._maps.update(
            {
                "checkout_button": "[data-test='checkout']",
                "first_name_input": "[data-test='firstName']",
                "last_name_input": "[data-test='lastName']",
                "postal_code_input": "[data-test='postalCode']",
                "continue_button": "[data-test='continue']",
                "finish_button": "[data-test='finish']",
                "complete_header": "[data-test='complete-header']",
            }
        )

    def checkout(self, timeout_ms: Optional[int] = None) -> None:
        """Click checkout button from the cart page."""
        if timeout_ms is None:
            timeout_ms = get_settings().timeout
        self.click("checkout_button", timeout_ms=timeout_ms)

    def fill_information(
        self,
        first_name: str,
        last_name: str,
        zip_code: str,
        timeout_ms: Optional[int] = None,
    ) -> None:
        """Fill checkout information and continue."""
        if timeout_ms is None:
            timeout_ms = get_settings().timeout
        self.fill("first_name_input", first_name, timeout_ms=timeout_ms)
        self.fill("last_name_input", last_name, timeout_ms=timeout_ms)
        self.fill("postal_code_input", zip_code, timeout_ms=timeout_ms)
        self.click("continue_button", timeout_ms=timeout_ms)

    def finish_checkout(self, timeout_ms: Optional[int] = None) -> None:
        """Finish checkout."""
        if timeout_ms is None:
            timeout_ms = get_settings().timeout
        self.click("finish_button", timeout_ms=timeout_ms)

    def get_complete_header(self, timeout_ms: Optional[int] = None) -> str:
        """Return the checkout success header text."""
        if timeout_ms is None:
            timeout_ms = get_settings().timeout
        locator = self.get_element("complete_header", timeout_ms=timeout_ms)
        try:
            locator.wait_for(state="visible", timeout=timeout_ms)
        except TimeoutError:
            return ""
        text = locator.text_content()
        return text.strip() if text else ""
