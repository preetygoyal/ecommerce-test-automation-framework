"""Full multi-step UI signup form -- exercised separately from login/checkout
so the heavier account-creation form is still covered by real browser
interaction at least once, not just via the API."""
import pytest

from common.test_data import build_account_payload, unique_email
from ui.pages.home_page import HomePage
from ui.pages.login_page import LoginPage
from ui.pages.signup_page import SignupPage


@pytest.mark.ui
def test_new_user_can_sign_up_through_the_full_form(page):
    email = unique_email()
    payload = build_account_payload(email=email, password="P@ssw0rd123", name="QA Signup")

    login_page = LoginPage(page).open()
    login_page.start_signup(name=payload["name"], email=email)

    signup_page = SignupPage(page)
    signup_page.complete_signup(payload)
    assert signup_page.is_visible(signup_page.account_created_banner)
    signup_page.confirm_and_continue()

    home_page = HomePage(page)
    assert home_page.is_logged_in_as(payload["name"])

    # Cleanup via API so we don't leave the account behind.
    from common.api_client import ApiClient
    ApiClient().delete_account(email=email, password="P@ssw0rd123")
