"""Central configuration for the framework (UI + API)."""
import os

# --- Site under test ---
BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")
API_BASE_URL = f"{BASE_URL}/api"

# --- Timeouts ---
UI_DEFAULT_TIMEOUT_MS = int(os.getenv("UI_DEFAULT_TIMEOUT_MS", "15000"))
API_REQUEST_TIMEOUT_S = int(os.getenv("API_REQUEST_TIMEOUT_S", "15"))

# --- Headless mode for local debugging ---
HEADLESS = os.getenv("HEADLESS", "true").lower() != "false"
