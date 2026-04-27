"""
Page object for the Weather Shopper main (home) page.
URL: https://weathershopper.pythonanywhere.com/

"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import Wrapit
import conf.locators_conf as locators
from core_helpers.web_app_helper import Web_App_Helper  


class WeatherShopper_MainPage(Web_App_Helper):
    "Page object for the WeatherShopper home page"

   
    TEMPERATURE  = locators.ws_temperature          

    
    BUY_MOISTURIZERS = locators.ws_buy_moisturizers_btn
    BUY_SUNSCREENS   = locators.ws_buy_sunscreens_btn
    PAGE_HEADING = "xpath,//h2[contains(text(),'%s')]"

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def start(self):
        "Open the WeatherShopper home page"
        self.open('/')

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def verify_temperature_visible(self):
        "Verify the temperature element is present and visible on the page"
        result_flag = self.check_element_present(self.TEMPERATURE)
        self.conditional_write(result_flag,
            positive="Temperature element is visible on the page",
            negative="Temperature element is NOT visible on the page")
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_temperature(self):
        "Read and return the numeric temperature as an integer"
        temp_bytes = self.get_text_by_locator(self.TEMPERATURE)
        temp_text  = temp_bytes.decode('utf-8') if isinstance(temp_bytes, bytes) else temp_bytes
        temperature = int(''.join(filter(str.isdigit, temp_text)))
        self.write(f"Current temperature on page: {temperature}")
        return temperature

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_buy_button(self, product_type):
        result_flag  = False
        product_type = product_type.lower()

        if product_type == 'moisturizers':
            locator = self.BUY_MOISTURIZERS
        elif product_type == 'sunscreens':
            locator = self.BUY_SUNSCREENS
        else:
            self.write(f"Unknown product type: {product_type}", 'critical')
            return False

        result_flag = self.click_element(locator)
        self.conditional_write(result_flag,
            positive=f"Clicked the Buy button for: {product_type}",
            negative=f"Could not click the Buy button for: {product_type}")

        

        if result_flag:
            self.switch_page(product_type)

        return result_flag