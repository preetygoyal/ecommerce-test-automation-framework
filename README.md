# E-Commerce End-to-End Test Automation Framework

[![E2E Test Suite](https://github.com/preetygoyal/ecommerce-test-automation-framework/actions/workflows/ci.yml/badge.svg)](https://github.com/preetygoyal/ecommerce-test-automation-framework/actions/workflows/ci.yml)

A single framework that covers **UI automation**, **API testing**, and **CI/CD**
for an e-commerce site, built against the public practice site
[automationexercise.com](https://automationexercise.com) (chosen because it exposes
both a real UI and a [documented REST API](https://automationexercise.com/api_list)).

Instead of three thin, disconnected projects, this repo demonstrates how the
layers work together: UI tests seed test accounts through the API for speed,
and the same `common/` client is reused by both suites.

## Tech stack

| Layer | Tools |
|---|---|
| UI automation | Playwright (Python), Page Object Model, pytest-playwright |
| API automation | pytest, `requests` |
| CI/CD | GitHub Actions (runs on every push/PR to `main`) |
| Reporting | pytest-html |

## Project structure

```
.
├── common/                  # Shared config, API client, test-data generators
│   ├── api_client.py        # Wrapper around automationexercise's REST API
│   ├── config.py            # Base URLs, timeouts, headless toggle
│   └── test_data.py         # Unique email/account payload generators
├── api/
│   ├── conftest.py          # api_client + new_account fixtures
│   └── tests/                 # Products, brands, search, account lifecycle
├── ui/
│   ├── conftest.py           # registered_user fixture (seeds account via API)
│   ├── pages/                # Page Object Model (Home, Login, Signup, Products,
│   │                           Cart, Checkout, Payment)
│   └── tests/                # Login, cart, checkout, signup flows
├── .github/workflows/ci.yml  # CI pipeline: API job -> UI job (Playwright)
├── pytest.ini
└── requirements.txt
```

## What's covered

**UI (Playwright + POM)**
- Login with valid/invalid credentials, logout
- Add single/multiple products to cart, empty-cart state
- Full checkout: login -> add to cart -> checkout -> pay with a test card -> order confirmation
- Full multi-step signup form (the one flow not shortcut via the API)

**API (pytest + requests)**, against `automationexercise.com/api_list`
- `GET /productsList`, `GET /brandsList`
- `POST /searchProduct` (valid term + missing-parameter error)
- `POST /verifyLogin` (valid, invalid, missing params)
- `POST /createAccount`, `PUT /updateAccount`, `DELETE /deleteAccount`, `GET /getUserDetailByEmail`

All tests that create accounts clean up after themselves (via fixture teardown),
so the suite is safe to re-run and safe to run concurrently in CI.

## Running locally

```bash
# 1. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
playwright install --with-deps chromium

# 3. Run everything
pytest

# ...or just one suite
pytest api/tests -m api
pytest ui/tests -m ui -v

# Run UI tests with a visible browser instead of headless
HEADLESS=false pytest ui/tests -m ui --headed
```

An HTML report can be generated with `pytest --html=report.html --self-contained-html`.

## CI/CD

`.github/workflows/ci.yml` runs on every push and pull request to `main`:

1. **api-tests** job — installs dependencies and runs the full API suite.
2. **ui-tests** job — installs Playwright's Chromium browser and runs the full UI suite (after the API job passes).

Both jobs upload their HTML reports as workflow artifacts; the UI job also uploads
Playwright traces on failure for debugging.

## Design notes

- **Page Object Model** keeps locators out of test files — if the site's markup
  changes, only the relevant page object needs updating.
- **Shared `common/api_client.py`** is used by both suites: the API suite tests
  it directly, and the UI suite uses it to seed/clean up accounts, avoiding
  slow, redundant UI signups for tests that only need to *be logged in*.
- **Unique, disposable test data** (`common/test_data.py`) means tests never
  collide with each other, even when run in parallel or repeatedly in CI.
