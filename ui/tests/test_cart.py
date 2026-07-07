"""UI cart flows: adding a product, seeing it reflected in the cart, and empty-cart state."""
import pytest

from ui.pages.cart_page import CartPage
from ui.pages.products_page import ProductsPage


@pytest.mark.ui
def test_add_single_product_to_cart(page):
    products_page = ProductsPage(page).open()
    products_page.add_first_product_to_cart()
    products_page.go_to_cart_from_modal()

    cart_page = CartPage(page)
    assert cart_page.item_count() == 1


@pytest.mark.ui
def test_add_multiple_products_to_cart(page):
    products_page = ProductsPage(page).open()

    products_page.add_product_to_cart_by_index(0)
    products_page.continue_shopping()
    products_page.add_product_to_cart_by_index(1)
    products_page.go_to_cart_from_modal()

    cart_page = CartPage(page)
    assert cart_page.item_count() == 2


@pytest.mark.ui
def test_empty_cart_shows_no_items(page):
    cart_page = CartPage(page).open()
    assert cart_page.item_count() == 0
