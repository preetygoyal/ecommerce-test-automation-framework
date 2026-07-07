"""API 3 from automationexercise.com/api_list: GET /brandsList."""
import pytest


@pytest.mark.api
def test_get_brands_list_returns_200_and_brands(api_client):
    response = api_client.get_brands_list()
    assert response.status_code == 200

    body = response.json()
    assert body["responseCode"] == 200
    assert isinstance(body["brands"], list)
    assert len(body["brands"]) > 0
    assert "id" in body["brands"][0]
    assert "brand" in body["brands"][0]
