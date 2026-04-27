"""
Page object for the Weather Shopper cart / checkout page.
URL: https://weathershopper.pythonanywhere.com/cart

Responsibilities:
    - Verify product names in cart match what was added
    - Verify product prices in cart match what was added
    - Verify cart total equals sum of item prices
    - Click Pay with Card to proceed to payment
"""
import os
import sys
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import Wrapit

import conf.locators_conf as locators
from core_helpers.web_app_helper import Web_App_Helper 


class WeatherShopper_CartPage(Web_App_Helper):
    "Page object for the WeatherShopper cart / checkout page"

   
    CART_TITLE = locators.ws_cart_title        
    CART_ITEM_NAMES  = locators.ws_cart_item_names   
    CART_ITEM_PRICES = locators.ws_cart_item_prices  
    CART_TOTAL = locators.ws_cart_total        
    PAY_WITH_CARD = locators.ws_pay_with_card_btn 

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def _parse_price(self, price_text):
        "Extract numeric value from a price string"
        digits = re.findall(r'\d+', price_text)
        return int(digits[-1]) if digits else 0

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def _decode(self, text):
        "Decode bytes to str if needed"
        return text.decode('utf-8') if isinstance(text, bytes) else text

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_cart_item_names(self):
        "Return list of item name strings currently in the cart"
        name_elems = self.get_elements(self.CART_ITEM_NAMES)
        names = []
        for el in name_elems:
            text = self.get_text(el, dom_element_flag=True)
            names.append(self._decode(text).strip())
        self.write(f"Cart item names: {names}")
        return names

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_cart_item_prices(self):
        "Return list of item prices (int) currently in the cart"
        price_elems = self.get_elements(self.CART_ITEM_PRICES)
        prices = []
        for el in price_elems:
            text = self.get_text(el, dom_element_flag=True)
            prices.append(self._parse_price(self._decode(text)))
        self.write(f"Cart item prices: {prices}")
        return prices

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_cart_total(self):
        "Return the displayed cart total as an integer"
        total_text = self.get_text_by_locator(self.CART_TOTAL)
        total_text = self._decode(total_text)
        total = self._parse_price(total_text)
        self.write(f"Cart total displayed: {total}")
        return total

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def verify_item_names_in_cart(self, expected_items):
        """
        Verify each expected item name appears in the cart.
        expected_items: list of dicts with key 'name'
        """
        cart_names  = self.get_cart_item_names()
        result_flag = True

        for item in expected_items:
            found = any(item['name'] in cart_name for cart_name in cart_names)
            self.conditional_write(found,
                positive=f"Found expected item in cart: '{item['name']}'",
                negative=f"Expected item NOT found in cart: '{item['name']}'")
            result_flag &= found

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def verify_item_prices_in_cart(self, expected_items):
        """
        Verify each expected item price appears in the cart prices list.
        expected_items: list of dicts with key 'price'
        """
        cart_prices = self.get_cart_item_prices()
        result_flag = True

        for item in expected_items:
            found = item['price'] in cart_prices
            self.conditional_write(found,
                positive=f"Found expected price in cart: {item['price']}",
                negative=f"Expected price NOT found in cart: {item['price']}")
            result_flag &= found

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def verify_cart_total(self, expected_items):
        """
        Verify displayed total equals sum of expected item prices.
        expected_items: list of dicts with key 'price'
        """
        expected_total  = sum(item['price'] for item in expected_items)
        displayed_total = self.get_cart_total()
        result_flag     = (displayed_total == expected_total)
        self.conditional_write(result_flag,
            positive=f"Cart total is correct: {displayed_total}",
            negative=f"Cart total mismatch — expected {expected_total}, got {displayed_total}")
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_pay_with_card(self):
        "Click the Pay with Card button."
        result_flag = self.click_element(self.PAY_WITH_CARD)
        self.conditional_write(result_flag,
            positive="Clicked 'Pay with Card' button",
            negative="Could not click 'Pay with Card' button")
        if result_flag:
            self.switch_page('weathershopper payment')
        return result_flag