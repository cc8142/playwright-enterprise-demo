from __future__ import annotations

import pytest
from playwright.sync_api import Page

from config.settings import get_settings
from pages.login_page import LoginPage


def test_standard_user_login_success(page: Page) -> None:
    settings = get_settings()
    login_page = LoginPage(page)
    login_page.open()

    username = settings.app_username.get_secret_value()
    password = settings.app_password.get_secret_value()
    login_page.login(username, password)

    assert "inventory.html" in page.url, "Login should redirect to inventory page."
