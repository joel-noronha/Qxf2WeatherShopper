


ws_temperature          = "id,temperature"
ws_buy_moisturizers_btn = "xpath,//a[contains(@href,'/moisturizer')]"
ws_buy_sunscreens_btn   = "xpath,//a[contains(@href,'/sunscreen')]"

ws_product_names        = "xpath,//div[contains(@class,'container')]//p[contains(text(),'rice')]/preceding-sibling::p[1]"

ws_product_prices       = "xpath,//div[contains(@class,'container')]//p[contains(text(),'rice')]"

ws_add_buttons          = "xpath,//button[contains(text(),'Add')]"

ws_cart_button          = "xpath,//button[contains(text(),'Cart')]"


ws_cart_title           = "xpath,//h2[contains(text(),'Checkout')]"
ws_cart_item_names  = "xpath,//table[@class='table table-striped']//tbody/tr/td[1]"
ws_cart_item_prices = "xpath,//table[@class='table table-striped']//tbody/tr/td[2]"
ws_cart_total       = "id,total"
ws_pay_with_card_btn    = "xpath,//button[@type='submit']"


ws_stripe_email         = "xpath,//input[@placeholder='Email']"
ws_stripe_card_number   = "xpath,//input[@placeholder='Card number']"
ws_stripe_card_expiry   = "xpath,//input[@placeholder='MM / YY']"
ws_stripe_card_cvv      = "xpath,//input[@placeholder='CVC']"
ws_stripe_card_zip      = "xpath,//input[@id='billing-zip']"
ws_stripe_submit_btn    = "xpath,//button[@type='submit']"

ws_payment_success_msg  = "xpath,//h2[contains(text(),'PAYMENT')]"