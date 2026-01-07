from __future__ import annotations

from playwright.sync_api import Page

from config.settings import get_settings
from pages.login_page import LoginPage


def test_standard_user_can_complete_checkout(page: Page) -> None:
    settings = get_settings()
    login_page = LoginPage(page)
    login_page.open()

    username = settings.app_username.get_secret_value()
    password = settings.app_password.get_secret_value()
    inventory_page = login_page.login(username, password)

    inventory_page.add_to_cart("Sauce Labs Backpack")
    checkout_page = inventory_page.go_to_cart()

    checkout_page.checkout()
    checkout_page.fill_information(
        first_name="John",
        last_name="Doe",
        zip_code="12345",
    )
    checkout_page.finish_checkout()

    assert (
        checkout_page.get_complete_header() == "Thank you for your order!"
    ), "Checkout should complete successfully."
