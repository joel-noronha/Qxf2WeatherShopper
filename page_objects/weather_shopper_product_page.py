"""
Page object for the Weather Shopper product pages.
Handles both /moisturizer and /sunscreen — they share identical HTML structure.
"""
import os
import sys
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import Wrapit
import conf.locators_conf as locators
from core_helpers.web_app_helper import Web_App_Helper  


class WeatherShopper_ProductPage(Web_App_Helper):
    "Page object for the WeatherShopper Moisturizers / Sunscreens product page"

   
    PRODUCT_NAMES  = locators.ws_product_names   
    PRODUCT_PRICES = locators.ws_product_prices  
    ADD_BUTTONS  = locators.ws_add_buttons      
    CART_BUTTON = locators.ws_cart_button      
    CART_TITLE  = locators.ws_cart_title       

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def _parse_price(self, price_text):
        "Extract the numeric price from a string"
        digits = re.findall(r'\d+', price_text)
        return int(digits[-1]) if digits else 0

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_all_products(self):
        """
        Return a list of dicts
        """
        products   = []
        name_elems  = self.get_elements(self.PRODUCT_NAMES)
        price_elems = self.get_elements(self.PRODUCT_PRICES)

        for idx, (name_el, price_el) in enumerate(zip(name_elems, price_elems)):
            name  = self.get_text(name_el,  dom_element_flag=True)
            price = self.get_text(price_el, dom_element_flag=True)
            name  = name.decode('utf-8')  if isinstance(name,  bytes) else name
            price = price.decode('utf-8') if isinstance(price, bytes) else price
            products.append({
                'name' : name.strip(),
                'price': self._parse_price(price),
                'index': idx
            })

        self.write(f"Found {len(products)} products on the page")
        return products

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_cheapest_and_most_expensive(self, products):
        "products list"
        cheapest      = min(products, key=lambda p: p['price'])
        most_expensive = max(products, key=lambda p: p['price'])
        self.write(f"Cheapest item    : {cheapest['name']} @ {cheapest['price']}")
        self.write(f"Most expensive   : {most_expensive['name']} @ {most_expensive['price']}")
        return cheapest, most_expensive

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def add_item_to_cart(self, item):
        "Click the Add button for the item at the given index."
        add_buttons = self.get_elements(self.ADD_BUTTONS)
        result_flag = False

        if item['index'] < len(add_buttons):
            try:
                add_buttons[item['index']].click()
                result_flag = True
                self.write(f"Added to cart: {item['name']} @ {item['price']}")
            except Exception as e:                              
                self.write(f"Could not click Add for {item['name']}: {str(e)}", 'critical')
                self.exceptions.append(f"Failed to add item: {item['name']}")
        else:
            self.write(f"Add button index {item['index']} out of range", 'critical')

        self.conditional_write(result_flag,
            positive=f"Successfully added '{item['name']}' to cart",
            negative=f"Failed to add '{item['name']}' to cart")
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def add_items_to_cart(self, items):
        "Add a list of item dicts to the cart."
        result_flag = True
        for item in items:
            result_flag &= self.add_item_to_cart(item)
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_cart_button(self):
        "Click the Cart button in the navbar. "
        result_flag = self.click_element(self.CART_BUTTON)
        self.conditional_write(result_flag,
            positive="Clicked the Cart button",
            negative="Could not click the Cart button")
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def verify_cart_page(self):
        "Verify automation landed on the cart page."
        result_flag = self.smart_wait(self.CART_TITLE, wait_seconds=5)
        self.conditional_write(result_flag,
            positive="Confirmed: now on the Cart / Checkout page",
            negative="Could not confirm landing on the Cart page")
        if result_flag:
            self.switch_page('weathershopper cart')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def go_to_cart(self):
        "Click Cart button and verify cart page."
        result_flag  = self.click_cart_button()
        result_flag &= self.verify_cart_page()
        return result_flag