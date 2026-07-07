from playwright.sync_api import Page

from .base_page import BasePage


class SignupPage(BasePage):
    """The 'Enter Account Information' page shown after step 1 of signup."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.password_input = page.locator("#password")
        self.days_select = page.locator("#days")
        self.months_select = page.locator("#months")
        self.years_select = page.locator("#years")
        self.first_name_input = page.locator("#first_name")
        self.last_name_input = page.locator("#last_name")
        self.address1_input = page.locator("#address1")
        self.country_select = page.locator("#country")
        self.state_input = page.locator("#state")
        self.city_input = page.locator("#city")
        self.zipcode_input = page.locator("#zipcode")
        self.mobile_number_input = page.locator("#mobile_number")
        self.create_account_button = page.locator("button[data-qa='create-account']")
        self.account_created_banner = page.get_by_text("Account Created!")
        self.continue_button = page.locator("a[data-qa='continue-button']")

    def complete_signup(self, payload: dict) -> "SignupPage":
        self.password_input.fill(payload["password"])
        self.days_select.select_option(payload["birth_date"])
        self.months_select.select_option(payload["birth_month"])
        self.years_select.select_option(payload["birth_year"])
        self.first_name_input.fill(payload["firstname"])
        self.last_name_input.fill(payload["lastname"])
        self.address1_input.fill(payload["address1"])
        self.country_select.select_option(payload["country"])
        self.state_input.fill(payload["state"])
        self.city_input.fill(payload["city"])
        self.zipcode_input.fill(payload["zipcode"])
        self.mobile_number_input.fill(payload["mobile_number"])
        self.create_account_button.click()
        return self

    def confirm_and_continue(self):
        self.continue_button.click()
        return self
