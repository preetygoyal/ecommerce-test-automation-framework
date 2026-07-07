from playwright.sync_api import Page

from .base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.signup_login_link = page.get_by_text("Signup / Login")
        self.products_link = page.locator("a[href='/products']")
        self.cart_link = page.locator("a[href='/view_cart']")
        self.logged_in_indicator = page.get_by_text("Logged in as", exact=False)
        self.logout_link = page.locator("a[href='/logout']")

    def open(self) -> "HomePage":
        self.goto("/")
        return self

    def go_to_signup_login(self):
        self.signup_login_link.click()
        return self

    def go_to_products(self):
        self.products_link.first.click()
        return self

    def go_to_cart(self):
        self.cart_link.first.click()
        return self

    def is_logged_in_as(self, name: str) -> bool:
        return self.is_visible(self.page.get_by_text(f"Logged in as {name}"))

    def logout(self):
        self.logout_link.click()
        return self
