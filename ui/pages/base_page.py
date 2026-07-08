"""Base class every page object inherits from: common waits/actions live here
so individual page objects stay focused on their own locators."""
from __future__ import annotations

from playwright.sync_api import Page, expect

from common.config import BASE_URL, UI_DEFAULT_TIMEOUT_MS


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.page.set_default_timeout(UI_DEFAULT_TIMEOUT_MS)
        self.page.set_default_navigation_timeout(UI_DEFAULT_TIMEOUT_MS)

    def goto(self, path: str = "/"):
        self.page.goto(f"{BASE_URL}{path}", wait_until="load")
        return self

    def is_visible(self, locator) -> bool:
        try:
            return locator.is_visible()
        except Exception:
            return False

    def assert_url_contains(self, fragment: str):
        expect(self.page).to_have_url(lambda url: fragment in url)
