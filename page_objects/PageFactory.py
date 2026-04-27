"""
PageFactory uses the factory design pattern.
get_page_object() returns the appropriate page object.
Add elif clauses as and when you implement new pages.
Pages implemented so far:
1. Tutorial main page
2. Tutorial redirect page
3. Contact Page
4. Bitcoin main page
5. Bitcoin price page
"""
# pylint: disable=import-outside-toplevel, E0401
from conf import base_url_conf as url_conf

class PageFactory():
    "PageFactory uses the factory design pattern."
    @staticmethod
    def get_page_object(page_name,base_url=url_conf.ui_base_url):
        "Return the appropriate page object based on page_name"
        test_obj = None
        page_name = page_name.lower()
        if page_name in ["zero","zero page","agent zero"]:
            from .zero_page import Zero_Page
            test_obj = Zero_Page(base_url=base_url)
        elif page_name in ["zero mobile","zero mobile page"]:
            from .zero_mobile_page import Zero_Mobile_Page
            test_obj = Zero_Mobile_Page()
        elif page_name == "weathershopper main page":
            from .weather_shopper_main import WeatherShopper_MainPage
            test_obj = WeatherShopper_MainPage(base_url=base_url)
        elif page_name in ["moisturizers", "sunscreens"]:
            from .weather_shopper_product_page import WeatherShopper_ProductPage
            test_obj = WeatherShopper_ProductPage(base_url=base_url)
        elif page_name == "weathershopper cart":
            from .weather_shopper_cart_page import WeatherShopper_CartPage
            test_obj = WeatherShopper_CartPage(base_url=base_url)
        elif page_name == "weathershopper payment":
            from .weather_shopper_payment_page import WeatherShopper_PaymentPage
            test_obj = WeatherShopper_PaymentPage(base_url=base_url)
        return test_obj
