from playwright.sync_api import Page

from .base_page import BasePage


class ProductsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.product_cards = page.locator(".product-image-wrapper")
        self.add_to_cart_buttons = page.locator(".product-image-wrapper .add-to-cart")
        self.continue_shopping_button = page.get_by_text("Continue Shopping")
        self.view_cart_link = page.locator("a[href='/view_cart']")
        self.search_input = page.locator("#search_product")
        self.search_button = page.locator("#submit_search")

    def open(self) -> "ProductsPage":
        self.goto("/products")
        return self

    def add_first_product_to_cart(self):
        self.add_to_cart_buttons.first.click()
        return self

    def add_product_to_cart_by_index(self, index: int):
        self.add_to_cart_buttons.nth(index).click()
        return self

    def continue_shopping(self):
        self.continue_shopping_button.click()
        return self

    def go_to_cart_from_modal(self):
        self.view_cart_link.click()
        return self

    def search(self, term: str):
        self.search_input.fill(term)
        self.search_button.click()
        return self

    def product_count(self) -> int:
        return self.product_cards.count()
