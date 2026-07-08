from playwright.sync_api import Page

from .base_page import BasePage


class ProductsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.product_cards = page.locator(".product-image-wrapper")
        self.add_to_cart_buttons = page.locator(".product-image-wrapper .add-to-cart")
        self.continue_shopping_button = page.get_by_text("Continue Shopping")
        # The nav bar's cart icon link and the modal's "View Cart" link share the
        # same href, so a plain href selector matches both (strict-mode violation).
        # An exact accessible-name match disambiguates: the nav link's name is
        # " Cart" (icon + text), the modal link's is "View Cart".
        self.view_cart_link = page.get_by_role("link", name="View Cart", exact=True)
        self.search_input = page.locator("#search_product")
        self.search_button = page.locator("#submit_search")

    def open(self) -> "ProductsPage":
        self.goto("/products")
        return self

    def add_first_product_to_cart(self):
        button = self.add_to_cart_buttons.first
        button.scroll_into_view_if_needed()
        button.click()
        return self

    def add_product_to_cart_by_index(self, index: int):
        button = self.add_to_cart_buttons.nth(index)
        button.scroll_into_view_if_needed()
        button.click()
        return self

    def continue_shopping(self):
        self.continue_shopping_button.click()
        # Wait for the modal to fully close before the caller interacts with
        # the page again -- clicking immediately after can hit the page mid
        # reflow/animation and land on the wrong element.
        self.continue_shopping_button.wait_for(state="hidden")
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
