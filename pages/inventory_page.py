from __future__ import annotations

from typing import Optional

from playwright.sync_api import Locator
from playwright.sync_api import Page

from config.settings import get_settings
from pages.base_page import BasePage
from pages.checkout_page import CheckoutPage


class InventoryPage(BasePage):
    """Page object for the SauceDemo inventory page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._maps.update(
            {
                "inventory_list": "[data-test='inventory-list']",
                "inventory_item": "[data-test='inventory-item']",
                "cart_link": "[data-test='shopping-cart-link']",
                "products_title": ".title",
            }
        )

    def is_inventory_visible(self, timeout_ms: Optional[int] = None) -> bool:
        """Return True when the inventory list is visible."""
        if timeout_ms is None:
            timeout_ms = get_settings().timeout
        locator = self.get_element("inventory_list", timeout_ms=timeout_ms)
        try:
            locator.wait_for(state="visible", timeout=timeout_ms)
        except TimeoutError:
            return False
        return True

    def is_products_title_visible(self, timeout_ms: Optional[int] = None) -> bool:
        """Return True when the Products title is visible."""
        if timeout_ms is None:
            timeout_ms = get_settings().timeout
        locator = self.get_element("products_title", timeout_ms=timeout_ms)
        try:
            locator.wait_for(state="visible", timeout=timeout_ms)
        except TimeoutError:
            return False
        return True

    def add_item_to_cart(self, item_name: str, timeout_ms: Optional[int] = None) -> None:
        """Add a specific item to the cart by product name."""
        if timeout_ms is None:
            timeout_ms = get_settings().timeout
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

    def add_to_cart(self, item_name: str, timeout_ms: Optional[int] = None) -> None:
        """Add a specific item to the cart by product name."""
        self.add_item_to_cart(item_name, timeout_ms=timeout_ms)

    def go_to_cart(self, timeout_ms: Optional[int] = None) -> CheckoutPage:
        """Open the shopping cart and return the checkout page object."""
        if timeout_ms is None:
            timeout_ms = get_settings().timeout
        self.click("cart_link", timeout_ms=timeout_ms)
        return CheckoutPage(self.page)

    def open_cart(self, timeout_ms: Optional[int] = None) -> CheckoutPage:
        """Open the shopping cart and return the checkout page object."""
        if timeout_ms is None:
            timeout_ms = get_settings().timeout
        self.click("cart_link", timeout_ms=timeout_ms)
        return CheckoutPage(self.page)
