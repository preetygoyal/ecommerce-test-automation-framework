from playwright.sync_api import Page

from .base_page import BasePage


class PaymentPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.name_on_card_input = page.locator("input[data-qa='name-on-card']")
        self.card_number_input = page.locator("input[data-qa='card-number']")
        self.cvc_input = page.locator("input[data-qa='cvc']")
        self.expiry_month_input = page.locator("input[data-qa='expiry-month']")
        self.expiry_year_input = page.locator("input[data-qa='expiry-year']")
        self.pay_button = page.locator("button[data-qa='pay-button']")
        self.order_confirmation_text = page.get_by_text("Congratulations! Your order has been confirmed!")

    def pay_with_fake_card(self, name: str = "QA Automation"):
        self.name_on_card_input.fill(name)
        self.card_number_input.fill("4242424242424242")
        self.cvc_input.fill("123")
        self.expiry_month_input.fill("12")
        self.expiry_year_input.fill("2030")
        self.pay_button.click()
        return self

    def order_confirmed(self) -> bool:
        return self.is_visible(self.order_confirmation_text)
