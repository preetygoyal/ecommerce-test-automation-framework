from playwright.sync_api import Page

from .base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.address_section = page.locator("#address_delivery")
        self.order_comment_textarea = page.locator("textarea[name='message']")
        self.place_order_button = page.get_by_text("Place Order")

    def is_loaded(self) -> bool:
        return self.is_visible(self.address_section)

    def enter_comment(self, comment: str):
        self.order_comment_textarea.fill(comment)
        return self

    def place_order(self):
        self.place_order_button.click()
        return self
