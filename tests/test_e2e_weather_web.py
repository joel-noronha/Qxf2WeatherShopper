"""
End-to-end test for the Weather Shopper app.

run using "python -m pytest tests/test_e2e_weather_web.py"
"""

import os
import sys
import time
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from page_objects.PageFactory import PageFactory                  
import conf.weather_shopper_conf as conf              

@pytest.mark.GUI
def test_weather_shopper_e2e(test_obj):
    "End-to-end test for the Weather Shopper application"
    try:
        
        #* counter for pass
         
        expected_pass = 0
        actual_pass   = -1
        start_time    = int(time.time())

        
        #* 1. Get page object for the home page
        
        test_obj = PageFactory.get_page_object(
            "weathershopper main page",
            base_url=test_obj.base_url)

        
        #* 2. Verify temperature is visible
  
        result_flag = test_obj.verify_temperature_visible()
        test_obj.log_result(result_flag,
            positive="Temperature is visible on the home page",
            negative="Temperature is NOT visible on the home page",
            level="critical")
        test_obj.write('Script duration: %d seconds\n' % (int(time.time() - start_time)))


        #* 3. Read temperature and decide product type
        temperature  = test_obj.get_temperature()
        product_type = ""

        if temperature <= 19:
            product_type = "moisturizers"
        elif temperature >= 34:
            product_type = "sunscreens"
        else:
            product_type = "moisturizers"
            test_obj.write(
                f"Temperature {temperature} is between 20-33; default product_type is moisturizers")

        test_obj.write(f"Temperature: {temperature} → buying: {product_type}")

        
        #* 4. Click Buy button and navigate to product page
        
        result_flag = test_obj.click_buy_button(product_type)
        test_obj.log_result(result_flag,
            positive=f"Navigated to the {product_type} page",
            negative=f"Failed to navigate to the {product_type} page",
            level="critical")

        
        #* 5. Get all products and pick cheapest + most expensive
        all_products = test_obj.get_all_products()
        cheapest, most_expensive = test_obj.get_cheapest_and_most_expensive(all_products)
        items_to_add = [cheapest, most_expensive]
        if cheapest['index'] == most_expensive['index']:
            items_to_add = [cheapest]
            test_obj.write("Cheapest and most expensive are the same item — adding once")

        
        #* 6. Add items to cart
        
        result_flag = test_obj.add_items_to_cart(items_to_add)
        test_obj.log_result(result_flag,
            positive="Successfully added cheapest and most expensive items to cart",
            negative="Failed to add one or more items to the cart",
            level="critical")

        
        #* 7. Go to cart
        
        result_flag = test_obj.go_to_cart()
        test_obj.log_result(result_flag,
            positive="Navigated to the cart page",
            negative="Failed to navigate to the cart page",
            level="critical")

       
        #* 8. Verify item names in cart
        
        result_flag = test_obj.verify_item_names_in_cart(items_to_add)
        test_obj.log_result(result_flag,
            positive="All expected item names are present in the cart",
            negative="One or more expected item names are missing from the cart")


        
        #* 10. Verify cart total
        result_flag = test_obj.verify_cart_total(items_to_add)
        test_obj.log_result(result_flag,
            positive="Cart total matches the sum of item prices",
            negative="Cart total does NOT match the sum of item prices")

        
        #* 11. Proceed to payment
        
        result_flag = test_obj.click_pay_with_card()
        test_obj.log_result(result_flag,
            positive="Clicked 'Pay with Card' — Stripe payment form opened",
            negative="Failed to open Stripe payment form",
            level="critical")

        
        #* 12. Fill payment details and submit
    
        payment = conf.payment_details
        result_flag = test_obj.fill_payment_details(
            email      = payment['email'],
            card_number= payment['card_no'],
            expiry     = payment['expiry'],
            cvv        = payment['cvv'],
            zip        = payment['zip'])
        test_obj.log_result(result_flag,
            positive="Payment details submitted successfully",
            negative="Failed to fill or submit payment details",
            level="critical")

        
        #* 13. Verify payment success
       
        result_flag = test_obj.verify_payment_success(conf.payment_success_text)
        test_obj.log_result(result_flag,
            positive="Payment SUCCESS confirmed on the page",
            negative="Payment success message was NOT found")

        
        #* test ends
       
        test_obj.write(f"Script duration: {int(time.time() - start_time)} seconds\n")
        test_obj.write_test_summary()

        expected_pass = test_obj.result_counter
        actual_pass   = test_obj.pass_counter

    except Exception as e:                         
        print(f"Exception when trying to run test: {__file__}")
        print(f"Python says:{str(e)}")

    if expected_pass != actual_pass:
        raise AssertionError(f"Test failed: {__file__}")