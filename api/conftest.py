import pytest

from common.api_client import ApiClient
from common.test_data import build_account_payload, unique_email


@pytest.fixture(scope="session")
def api_client() -> ApiClient:
    return ApiClient()


@pytest.fixture
def new_account(api_client: ApiClient):
    """Create a disposable account via the API, yield its credentials, then clean it up."""
    email = unique_email()
    password = "P@ssw0rd123"
    payload = build_account_payload(email=email, password=password)

    response = api_client.create_account(payload)
    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 201, f"Account setup failed: {body}"

    yield {"email": email, "password": password, "payload": payload}

    # Best-effort cleanup: ignore failures if a test already deleted the account.
    try:
        api_client.delete_account(email=email, password=password)
    except Exception:
        pass
