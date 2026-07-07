"""
Thin wrapper around automationexercise.com's public REST API
(https://automationexercise.com/api_list).

Used directly by the API test suite (api/tests/) AND by the UI suite
(ui/conftest.py) to seed/clean up a real account before driving the browser,
so we don't burn UI time re-testing signup on every scenario.
"""
from __future__ import annotations

import requests

from common.config import API_BASE_URL, API_REQUEST_TIMEOUT_S


class ApiClient:
    def __init__(self, base_url: str = API_BASE_URL, timeout: int = API_REQUEST_TIMEOUT_S):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    # ---- Products / Brands ----
    def get_products_list(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/productsList", timeout=self.timeout)

    def post_products_list(self) -> requests.Response:
        """Products list only supports GET; used to assert the 405-style response."""
        return self.session.post(f"{self.base_url}/productsList", timeout=self.timeout)

    def get_brands_list(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/brandsList", timeout=self.timeout)

    # ---- Search ----
    def search_product(self, search_term: str) -> requests.Response:
        return self.session.post(
            f"{self.base_url}/searchProduct",
            data={"search_product": search_term},
            timeout=self.timeout,
        )

    def search_product_missing_param(self) -> requests.Response:
        return self.session.post(f"{self.base_url}/searchProduct", timeout=self.timeout)

    # ---- Auth ----
    def verify_login(self, email: str, password: str) -> requests.Response:
        return self.session.post(
            f"{self.base_url}/verifyLogin",
            data={"email": email, "password": password},
            timeout=self.timeout,
        )

    def verify_login_missing_params(self) -> requests.Response:
        return self.session.post(f"{self.base_url}/verifyLogin", timeout=self.timeout)

    # ---- Account lifecycle ----
    def create_account(self, payload: dict) -> requests.Response:
        return self.session.post(f"{self.base_url}/createAccount", data=payload, timeout=self.timeout)

    def update_account(self, payload: dict) -> requests.Response:
        return self.session.put(f"{self.base_url}/updateAccount", data=payload, timeout=self.timeout)

    def delete_account(self, email: str, password: str) -> requests.Response:
        return self.session.delete(
            f"{self.base_url}/deleteAccount",
            data={"email": email, "password": password},
            timeout=self.timeout,
        )

    def get_user_detail_by_email(self, email: str) -> requests.Response:
        return self.session.get(
            f"{self.base_url}/getUserDetailByEmail",
            params={"email": email},
            timeout=self.timeout,
        )
