"""API 5 & 6: POST /searchProduct, with and without the required parameter."""
import pytest


@pytest.mark.api
def test_search_product_with_valid_term_returns_matches(api_client):
    response = api_client.search_product("top")
    assert response.status_code == 200

    body = response.json()
    assert body["responseCode"] == 200
    assert isinstance(body["products"], list)
    assert len(body["products"]) > 0


@pytest.mark.api
def test_search_product_missing_param_returns_400(api_client):
    response = api_client.search_product_missing_param()
    assert response.status_code == 200  # site wraps the error in a 200 envelope
    body = response.json()
    assert body["responseCode"] == 400
    assert "search_product parameter is missing" in body["message"]
