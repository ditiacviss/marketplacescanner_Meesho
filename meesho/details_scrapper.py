import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import re

def details_scrapper(url):
    # Set up Chrome options
    chrome_options = Options()
    # Uncomment the lines below to run in headless mode
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--window-size=1920x1080")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # driver = webdriver.Chrome(options=chrome_options)
    # service = Service("meesho/chromedriver.exe")
    # driver = webdriver.Chrome(service=service)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    print("Product URL is --->", url)

    # getting product name
    try:
        name = driver.find_element(By.XPATH, "//div[contains(@class, 'ShippingInfo__DetailCard')]/span").text.strip()
    except Exception as e:
        name = None

    try:
        rating_value = driver.find_element(By.XPATH,"//div[contains(@class,'CountWrapper__AverageRating-sc-fa0m6i-3')]/h1").text.strip()
    except Exception as e:
        rating_value = None

    try:
        price_discounted=driver.find_element(By.XPATH,"//div[contains(@class, 'ShippingInfo__PriceRow-sc-frp12n-1')]/h4").text.strip()
        price_discounted = re.sub(r'[^\d]', '', price_discounted)
    except Exception as e:
        price_discounted = None

    # getting actual price
    try:
        price_actual=driver.find_element(By.XPATH,"//div[contains(@class, 'ShippingInfoMobilestyles__PriceContainer-sc-b8wrmp-14')] | //div[contains(@class, 'ShippingInfo__PriceRow-sc-frp12n-1')]/p").text.strip()
        price_actual = re.sub(r'[^\d]', '', price_actual)
    except Exception as e:
        price_actual = None

    # getting discount
    try:
        # Discount_percentage = driver.find_element(By.XPATH,"//div[contains(@class,'ShippingInfo__PriceRow-sc-frp12n-1')]/span")
        Discount_percentage = driver.find_element(By.XPATH,"//div[contains(@class,'ShippingInfo__PriceRow-sc-frp12n-1')]/span[@class='sc-eDvSVe dOqdSt']")
        discount_text = Discount_percentage.text
    except Exception as e:
        discount_text = None

    # getting seller name
    try:
        seller_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ShopCardstyled__RightSection-sc-du9pku-3')]/span"))).text.strip()
    except Exception as e:
        print("getting seller name", e)
        seller_name = None

    # getting image link
    try:
        image_element = driver.find_element(By.XPATH, '//div[@class="ProductDesktopImage__ImageWrapperDesktop-sc-8sgxcr-0 iEMJCd"]//img')
        image_url = image_element.get_attribute("src")
    except Exception as e:
        image_url = None

    try:
        list_service = []
        span_tags = driver.find_elements(
            By.XPATH,
            "//div[@class='sc-ftTHYK eHVGcU DeliveryBadge__BadgeRow-sc-skvcwk-4 cyQxGW DeliveryBadge__BadgeRow-sc-skvcwk-4 cyQxGW'] | //div[@class='sc-ftTHYK eHVGcU Marketing__TagCardStyled-sc-1ngqanf-1 eAgvXz Marketing__TagCardStyled-sc-1ngqanf-1 eAgvXz']/span | //div[@class='sc-bqWxrE hupGZf DeliveryBadge__BadgeRow-sc-skvcwk-4 cyQxGW DeliveryBadge__BadgeRow-sc-skvcwk-4 cyQxGW'] | //div[@class='sc-bqWxrE hupGZf Marketing__TagCardStyled-sc-1ngqanf-1 eAgvXz Marketing__TagCardStyled-sc-1ngqanf-1 eAgvXz']/span"
        )        # Extract text from each span and append to the list
        for span in span_tags:
            list_service.append(span.text.strip())
    except Exception as e:
        list_service = None

    # getting product description
    try:
        product_description_elements = driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'ProductDescription__DetailsCardStyled-sc-1l1jg0i-0')]/p"
        )
        product_description_text = [element.text for element in product_description_elements]

    except Exception as e:
        product_description_text = None

    # getting seller_rating
    try:
        seller_rating = driver.find_element(By.XPATH, "//div[@class='sc-ftTHYK blMPnz ShopCardstyled__ValuePropCard-sc-du9pku-11 ioZPYn ShopCardstyled__ValuePropCard-sc-du9pku-11 ioZPYn']/span/span | //div[@class='sc-jrcTuL iLAawV ShopCardstyled__ValuePropCard-sc-du9pku-11 ioZPYn ShopCardstyled__ValuePropCard-sc-du9pku-11 ioZPYn']/span/span").text.strip()

    except Exception as e:
        seller_rating = None


    # Step 4: Close the browser
    driver.quit()
    return name, rating_value, price_discounted, price_actual, seller_name, list_service, seller_rating, image_url, product_description_text,discount_text
