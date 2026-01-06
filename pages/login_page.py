from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    """Page object for the SauceDemo login page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._maps.update(
            {
                "username_input": "[data-test='username']",
                "password_input": "[data-test='password']",
                "login_button": "[data-test='login-button']",
            }
        )

    def open(self, base_url: str) -> None:
        """Navigate to the login page."""
        self.page.goto(base_url, wait_until="domcontentloaded")

    def login(self, username: str, password: str) -> InventoryPage:
        """Log in and return the inventory page object."""
        self.fill("username_input", username)
        self.fill("password_input", password)
        self.click("login_button")
        return InventoryPage(self.page)
