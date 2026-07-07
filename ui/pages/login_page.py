from playwright.sync_api import Page

from .base_page import BasePage


class LoginPage(BasePage):
    """Handles the '/login' page, which hosts BOTH the login form and the
    initial (name + email) signup form side by side."""

    def __init__(self, page: Page):
        super().__init__(page)
        # Login form
        self.login_email_input = page.locator("input[data-qa='login-email']")
        self.login_password_input = page.locator("input[data-qa='login-password']")
        self.login_button = page.locator("button[data-qa='login-button']")
        self.login_error = page.get_by_text("Your email or password is incorrect!")

        # Signup form (name + email only, step 1)
        self.signup_name_input = page.locator("input[data-qa='signup-name']")
        self.signup_email_input = page.locator("input[data-qa='signup-email']")
        self.signup_button = page.locator("button[data-qa='signup-button']")
        self.signup_error = page.get_by_text("Email Address already exist!")

    def open(self) -> "LoginPage":
        self.goto("/login")
        return self

    def login(self, email: str, password: str):
        self.login_email_input.fill(email)
        self.login_password_input.fill(password)
        self.login_button.click()
        return self

    def start_signup(self, name: str, email: str):
        self.signup_name_input.fill(name)
        self.signup_email_input.fill(email)
        self.signup_button.click()
        return self

    def has_login_error(self) -> bool:
        return self.is_visible(self.login_error)
