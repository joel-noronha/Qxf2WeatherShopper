"""
Page object for the Weather Shopper payment page.
"""
import os
import time
import sys
from selenium.webdriver.common.keys import Keys
from utils import Wrapit
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import conf.locators_conf as locators
from core_helpers.web_app_helper import Web_App_Helper  


class WeatherShopper_PaymentPage(Web_App_Helper):
    "Page object for the WeatherShopper Stripe payment page"

    
    STRIPE_EMAIL = locators.ws_stripe_email       
    STRIPE_CARD_NUM = locators.ws_stripe_card_number 
    STRIPE_EXPIRY = locators.ws_stripe_card_expiry 
    STRIPE_CVV = locators.ws_stripe_card_cvv    
    STRIPE_ZIP = locators.ws_stripe_card_zip
    STRIPE_SUBMIT = locators.ws_stripe_submit_btn  

    
    PAYMENT_SUCCESS = locators.ws_payment_success_msg

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def _switch_to_stripe_iframe(self):
        "Switch driver context into the Stripe iframe."
        result_flag = self.switch_frame(name='stripe_checkout_app', wait_time=5)
        self.conditional_write(result_flag,
            positive="Switched into Stripe iframe",
            negative="Could not switch to Stripe iframe")
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def _switch_to_default(self):
        "Switch driver back to the main page content"
        self.driver.switch_to.default_content()
        self.write("Switched back to default content")

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def _fill_stripe_field(self, locator, value):
        element = self.get_element(locator)
        element.click()
        for char in value:
            element.send_keys(char)
            time.sleep(0.05)
        return True

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def fill_email(self, email):
        result_flag = self._fill_stripe_field(self.STRIPE_EMAIL, email)
        self.conditional_write(result_flag,
            positive=f"Entered email: {email}",
            negative="Could not enter email")
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def fill_card_number(self, card_number):
        result_flag = self._fill_stripe_field(self.STRIPE_CARD_NUM, card_number)
        self.conditional_write(result_flag,
            positive="Entered card number",
            negative="Could not enter card number")
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def fill_expiry(self, expiry):
        result_flag = self._fill_stripe_field(self.STRIPE_EXPIRY, expiry.replace('/', ''))
        self.conditional_write(result_flag,
            positive=f"Entered expiry: {expiry}",
            negative="Could not enter expiry")
        return result_flag
    
    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def fill_cvv(self, cvv):
        result_flag = self._fill_stripe_field(self.STRIPE_CVV, cvv)
        self.conditional_write(result_flag,
        positive="Entered CVV",
        negative="Could not enter CVV")
        return result_flag
    
    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def fill_zip(self, zip):
        result_flag = self._fill_stripe_field(self.STRIPE_ZIP, zip)
        self.conditional_write(result_flag,
        positive="Entered zip",
        negative="Could not enter zip")
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def submit_payment(self):
        "Click the Pay button inside the Stripe iframe. Returns True/False."
        result_flag = self.click_element(self.STRIPE_SUBMIT)
        self.conditional_write(result_flag,
            positive="Clicked the Pay / Submit button",
            negative="Could not click the Pay / Submit button")
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def fill_payment_details(self, email, card_number, expiry, cvv,zip):
        """
        fill all payment fields
        """
        result_flag  = self._switch_to_stripe_iframe()
        result_flag &= self.fill_email(email)
        result_flag &= self.fill_card_number(card_number)
        result_flag &= self.fill_expiry(expiry)
        result_flag &= self.fill_cvv(cvv)
        result_flag &= self.fill_zip(zip)
        result_flag &= self.submit_payment()
        self._switch_to_default()
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def verify_payment_success(self, expected_text):
        """
        Verify the payment success message is present
        """
        result_flag = self.smart_wait(self.PAYMENT_SUCCESS, wait_seconds=10)
        if result_flag:
            actual_text = self.get_text_by_locator(self.PAYMENT_SUCCESS)
            actual_text = actual_text.decode('utf-8') if isinstance(actual_text, bytes) else actual_text
            result_flag = expected_text.upper() in actual_text.upper()

        self.conditional_write(result_flag,
            positive=f"Payment success confirmed — found: '{expected_text}'",
            negative=f"Payment success message NOT found. Expected: '{expected_text}'")
        return result_flag