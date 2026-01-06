from __future__ import annotations

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage


@pytest.mark.parametrize(
    "username,password",
    [("standard_user", "secret_sauce")],
)
def test_standard_user_can_checkout(page: Page, username: str, password: str) -> None:
    login_page = LoginPage(page)
    login_page.open()

    inventory_page = login_page.login(username, password)
    assert inventory_page.is_inventory_visible(), "Inventory list should be visible."

    inventory_page.add_item_to_cart("Sauce Labs Backpack")
    cart_page = inventory_page.open_cart()
    assert cart_page.is_cart_visible(), "Cart should be visible."

    checkout_info_page = cart_page.checkout()
    checkout_overview_page = checkout_info_page.submit_customer_info(
        first_name="John",
        last_name="Doe",
        postal_code="12345",
    )
    checkout_complete_page = checkout_overview_page.finish_checkout()

    assert checkout_complete_page.is_order_complete(), "Checkout should complete."
