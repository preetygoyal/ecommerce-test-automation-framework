"""
API 7, 8, 10, 11, 12, 13 from automationexercise.com/api_list:
  POST   /verifyLogin           (valid creds / invalid creds / missing params)
  POST   /createAccount
  PUT    /updateAccount
  DELETE /deleteAccount
  GET    /getUserDetailByEmail

`new_account` (api/conftest.py) creates a disposable account before each test
that needs one and deletes it afterwards, so the suite never leaves junk data
behind and can run concurrently / repeatedly in CI without collisions.
"""
import pytest

from common.test_data import build_account_payload, unique_email


@pytest.mark.api
def test_create_account_success(api_client):
    email = unique_email()
    payload = build_account_payload(email=email, password="P@ssw0rd123")

    response = api_client.create_account(payload)
    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 201
    assert body["message"] == "User created!"

    # cleanup
    api_client.delete_account(email=email, password="P@ssw0rd123")


@pytest.mark.api
def test_verify_login_with_valid_credentials(api_client, new_account):
    response = api_client.verify_login(new_account["email"], new_account["password"])
    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 200
    assert body["message"] == "User exists!"


@pytest.mark.api
def test_verify_login_with_invalid_credentials(api_client, new_account):
    response = api_client.verify_login(new_account["email"], "wrong-password")
    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 404
    assert body["message"] == "User not found!"


@pytest.mark.api
def test_verify_login_missing_params_returns_400(api_client):
    response = api_client.verify_login_missing_params()
    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 400
    assert "missing" in body["message"].lower()


@pytest.mark.api
def test_get_user_detail_by_email(api_client, new_account):
    response = api_client.get_user_detail_by_email(new_account["email"])
    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 200
    assert body["user"]["email"] == new_account["email"]


@pytest.mark.api
def test_update_account(api_client, new_account):
    updated_payload = dict(new_account["payload"])
    updated_payload["firstname"] = "Updated"
    updated_payload["company"] = "Updated Co"

    response = api_client.update_account(updated_payload)
    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 200
    assert body["message"] == "User updated!"

    detail = api_client.get_user_detail_by_email(new_account["email"]).json()
    assert detail["user"]["first_name"] == "Updated"


@pytest.mark.api
def test_delete_account_removes_user(api_client):
    email = unique_email()
    password = "P@ssw0rd123"
    api_client.create_account(build_account_payload(email=email, password=password))

    delete_response = api_client.delete_account(email=email, password=password)
    assert delete_response.status_code == 200
    assert delete_response.json()["responseCode"] == 200

    # Account should no longer authenticate.
    verify_response = api_client.verify_login(email, password)
    assert verify_response.json()["responseCode"] == 404
