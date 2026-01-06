from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.checkout_overview_page import CheckoutOverviewPage


class CheckoutInformationPage(BasePage):
    """Page object for the SauceDemo checkout information page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._maps.update(
            {
                "first_name_input": "[data-test='firstName']",
                "last_name_input": "[data-test='lastName']",
                "postal_code_input": "[data-test='postalCode']",
                "continue_button": "[data-test='continue']",
            }
        )

    def submit_customer_info(
        self,
        first_name: str,
        last_name: str,
        postal_code: str,
        timeout_ms: int = 5000,
    ) -> CheckoutOverviewPage:
        """Fill customer info and continue to the overview page."""
        self.fill("first_name_input", first_name, timeout_ms=timeout_ms)
        self.fill("last_name_input", last_name, timeout_ms=timeout_ms)
        self.fill("postal_code_input", postal_code, timeout_ms=timeout_ms)
        self.click("continue_button", timeout_ms=timeout_ms)
        return CheckoutOverviewPage(self.page)
