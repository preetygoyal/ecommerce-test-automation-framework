"""Central configuration for the framework (UI + API)."""
import os

# --- Site under test ---
BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")
API_BASE_URL = f"{BASE_URL}/api"

# --- Timeouts ---
# automationexercise.com is a free public practice site shared by QA learners
# worldwide; it's noticeably slower/less consistent under load than a real
# production app, especially from shared CI runner IPs. 30s gives real page
# loads enough headroom without masking genuine bugs (a real defect still
# fails, it just doesn't get caught by a too-tight timeout on a slow site).
UI_DEFAULT_TIMEOUT_MS = int(os.getenv("UI_DEFAULT_TIMEOUT_MS", "30000"))
API_REQUEST_TIMEOUT_S = int(os.getenv("API_REQUEST_TIMEOUT_S", "20"))

# --- Headless mode for local debugging ---
HEADLESS = os.getenv("HEADLESS", "true").lower() != "false"
