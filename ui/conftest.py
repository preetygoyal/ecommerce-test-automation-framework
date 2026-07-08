"""
UI-suite fixtures.

Notably: `registered_user` seeds a real, disposable account through the
public API (common/api_client.py) instead of driving the multi-step signup
form for every single test that needs to be logged in. This keeps UI tests
fast and focused on what they're actually verifying, while `test_checkout.py`
still exercises the full UI signup form at least once end-to-end.
"""
import pytest

from common.api_client import ApiClient
from common.test_data import build_account_payload, unique_email


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """pytest-playwright's default viewport (1280x720) is narrow enough that
    automationexercise.com's 'All Products' heading overlaps the top row of
    the product grid, intermittently intercepting clicks on those cards in
    CI. A wider viewport avoids that responsive-layout overlap."""
    return {**browser_context_args, "viewport": {"width": 1600, "height": 1000}}


@pytest.fixture
def registered_user():
    """Create an account via the API, yield its credentials, delete it afterwards."""
    client = ApiClient()
    email = unique_email()
    password = "P@ssw0rd123"
    payload = build_account_payload(email=email, password=password, name="QA Automation")

    response = client.create_account(payload)
    assert response.json()["responseCode"] == 201, "Failed to seed UI test account via API"

    yield {"email": email, "password": password, "name": payload["name"], "payload": payload}

    try:
        client.delete_account(email=email, password=password)
    except Exception:
        pass
