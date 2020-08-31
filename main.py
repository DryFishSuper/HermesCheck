import random
import time

from utils import *

base_url = "https://bck.hermes.com/product-page?locale=us_en&productsku=%s"
# herbag_url = "https://bck.hermes.com/product-page?locale=us_en&productsku=H068675CKAD"
# picotin_url = "https://bck.hermes.com/product-page?locale=us_en&productsku=H056289CC18"
# redeo_url = "https://bck.hermes.com/product-page?locale=us_en&productsku=H064929CAAJ"


def main():
    sku = "PRODUCT_SKU"
    from_email = "YOUR_GMAIL_ACCOUNT"
    password = "YOUR_PASSWORD"
    to_email = "TO_EMAIL"
    url = base_url % sku
    sleep_time = random.randint(14 * 60, 16 * 60)
    count = 1
    while True:
        if has_stock(url, count):
            send_email(fromEmail=from_email, password=password, toEmail=to_email)
        time.sleep(sleep_time)
        count += 1


if __name__ == "__main__":
    main()
