"""
End-to-end checkout: log in -> add product to cart -> checkout -> pay -> confirm.
This is the flagship UI scenario, stitching together every page object.
"""
import pytest

from ui.pages.cart_page import CartPage
from ui.pages.checkout_page import CheckoutPage
from ui.pages.login_page import LoginPage
from ui.pages.payment_page import PaymentPage
from ui.pages.products_page import ProductsPage


@pytest.mark.ui
def test_full_checkout_flow_places_order(page, registered_user):
    # 1. Log in with an account seeded via the API.
    LoginPage(page).open().login(registered_user["email"], registered_user["password"])

    # 2. Add a product to the cart.
    products_page = ProductsPage(page).open()
    products_page.add_first_product_to_cart()
    products_page.go_to_cart_from_modal()

    cart_page = CartPage(page)
    assert cart_page.item_count() == 1
    cart_page.proceed_to_checkout()

    # 3. Review order & add a comment.
    checkout_page = CheckoutPage(page)
    assert checkout_page.is_loaded()
    checkout_page.enter_comment("Please deliver in the morning. (Automated test order)")
    checkout_page.place_order()

    # 4. Pay with a fake card (test site only).
    payment_page = PaymentPage(page)
    payment_page.pay_with_fake_card(name=registered_user["name"])

    # 5. Confirm.
    assert payment_page.order_confirmed()
