from playwright.sync_api import Page

from .base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_rows = page.locator("#cart_info_table tbody tr")
        self.proceed_to_checkout_button = page.get_by_text("Proceed To Checkout")
        self.register_login_link_in_modal = page.locator(".modal-body a[href='/login']")

    def open(self) -> "CartPage":
        self.goto("/view_cart")
        return self

    def item_count(self) -> int:
        return self.cart_rows.count()

    def has_product(self, product_name: str) -> bool:
        return self.is_visible(self.page.get_by_text(product_name))

    def proceed_to_checkout(self):
        self.proceed_to_checkout_button.click()
        return self
