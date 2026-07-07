"""
API 1 & 2 from automationexercise.com/api_list:
  GET  /productsList  -> 200 + product list
  POST /productsList  -> method not supported
"""
import pytest


@pytest.mark.api
def test_get_products_list_returns_200_and_products(api_client):
    response = api_client.get_products_list()
    assert response.status_code == 200

    body = response.json()
    assert body["responseCode"] == 200
    assert isinstance(body["products"], list)
    assert len(body["products"]) > 0

    first_product = body["products"][0]
    for field in ("id", "name", "price", "brand", "category"):
        assert field in first_product


@pytest.mark.api
def test_products_list_does_not_support_post(api_client):
    response = api_client.post_products_list()
    # The site still returns HTTP 200 but signals the error inside the payload.
    assert response.status_code == 200
    body = response.json()
    assert body["responseCode"] == 405
    assert "not supported" in body["message"].lower()
