"""
UI login flows. The valid-credentials test reuses an account seeded through
the API (see ui/conftest.py) -- a good example of API + UI working together
instead of the UI suite re-doing signup from scratch every time.
"""
import pytest

from ui.pages.home_page import HomePage
from ui.pages.login_page import LoginPage


@pytest.mark.ui
def test_login_with_valid_credentials(page, registered_user):
    login_page = LoginPage(page).open()
    login_page.login(registered_user["email"], registered_user["password"])

    home_page = HomePage(page)
    assert home_page.is_logged_in_as(registered_user["name"])


@pytest.mark.ui
def test_login_with_invalid_credentials_shows_error(page):
    login_page = LoginPage(page).open()
    login_page.login("not-a-real-user@mailinator.com", "wrong-password")

    assert login_page.has_login_error()


@pytest.mark.ui
def test_logout_returns_to_login_page(page, registered_user):
    login_page = LoginPage(page).open()
    login_page.login(registered_user["email"], registered_user["password"])

    home_page = HomePage(page)
    assert home_page.is_logged_in_as(registered_user["name"])

    home_page.logout()
    page.wait_for_url("**/login")
    assert "/login" in page.url
