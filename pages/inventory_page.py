from __future__ import annotations

from playwright.sync_api import Locator
from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.cart_page import CartPage


class InventoryPage(BasePage):
    """Page object for the SauceDemo inventory page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._maps.update(
            {
                "inventory_list": "[data-test='inventory-list']",
                "inventory_item": "[data-test='inventory-item']",
                "cart_link": "[data-test='shopping-cart-link']",
            }
        )

    def is_inventory_visible(self, timeout_ms: int = 5000) -> bool:
        """Return True when the inventory list is visible."""
        locator = self.get_element("inventory_list", timeout_ms=timeout_ms)
        try:
            locator.wait_for(state="visible", timeout=timeout_ms)
        except TimeoutError:
            return False
        return True

    def add_item_to_cart(self, item_name: str, timeout_ms: int = 5000) -> None:
        """Add a specific item to the cart by product name."""
        list_locator = self.get_element("inventory_list", timeout_ms=timeout_ms)
        try:
            list_locator.wait_for(state="visible", timeout=timeout_ms)
        except TimeoutError as exc:
            raise TimeoutError("Inventory list not visible.") from exc

        item_locator: Locator = (
            self.page.locator(self.map("inventory_item"))
            .filter(has_text=item_name)
            .first
        )

        button_locator: Locator = item_locator.locator(
            "button[data-test^='add-to-cart']"
        )
        self._wait_for_actionable(button_locator, "add-to-cart button", timeout_ms)
        self._highlight(button_locator)
        button_locator.click(timeout=timeout_ms)

    def open_cart(self, timeout_ms: int = 5000) -> CartPage:
        """Open the shopping cart and return the cart page object."""
        self.click("cart_link", timeout_ms=timeout_ms)
        return CartPage(self.page)
