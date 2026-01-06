from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.checkout_information_page import CheckoutInformationPage


class CartPage(BasePage):
    """Page object for the SauceDemo cart page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._maps.update(
            {
                "cart_list": "[data-test='cart-list']",
                "checkout_button": "[data-test='checkout']",
            }
        )

    def is_cart_visible(self, timeout_ms: int = 5000) -> bool:
        """Return True when the cart list is visible."""
        locator = self.get_element("cart_list", timeout_ms=timeout_ms)
        try:
            locator.wait_for(state="visible", timeout=timeout_ms)
        except TimeoutError:
            return False
        return True

    def checkout(self, timeout_ms: int = 5000) -> CheckoutInformationPage:
        """Proceed to checkout and return the checkout information page."""
        self.click("checkout_button", timeout_ms=timeout_ms)
        return CheckoutInformationPage(self.page)
