from __future__ import annotations

from playwright.sync_api import Page

from config.settings import Settings
from pages.login_page import LoginPage


def test_valid_login(page: Page, config: Settings) -> None:
    login_page = LoginPage(page)
    login_page.open()

    username = config.app_username.get_secret_value()
    password = config.app_password.get_secret_value()
    inventory_page = login_page.login(username, password)

    assert inventory_page.is_inventory_visible(), "Inventory list should be visible."
