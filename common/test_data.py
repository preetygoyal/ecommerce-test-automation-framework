"""Helpers for generating unique, disposable test data."""
import random
import string
import time


def unique_email(prefix: str = "qa.automation") -> str:
    """Return a unique email so account-creation tests never collide (locally or in CI)."""
    stamp = int(time.time() * 1000)
    rand = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))
    return f"{prefix}.{stamp}.{rand}@mailinator.com"


def random_string(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def build_account_payload(email: str, password: str, name: str = "QA Automation") -> dict:
    """Full payload required by automationexercise's createAccount / signup form."""
    return {
        "name": name,
        "email": email,
        "password": password,
        "title": "Mr",
        "birth_date": "10",
        "birth_month": "5",
        "birth_year": "1995",
        "firstname": "QA",
        "lastname": "Automation",
        "company": "Acme Testing Co",
        "address1": "221B Baker Street",
        "address2": "",
        "country": "United States",
        "zipcode": "10001",
        "state": "New York",
        "city": "New York",
        "mobile_number": "5551234567",
    }
