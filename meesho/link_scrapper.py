import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def product_url_scrapper(meesho_url, search_string, country_code):

    # chrome_driver_path = "meesho/chromedriver.exe"
    chrome_options = Options()

    # service = Service(chrome_driver_path)
    # driver = webdriver.Chrome(service=service)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(meesho_url)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    search_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Search by Product Code')]"))
    )
    search_input.send_keys(search_string)

    search_input.send_keys(Keys.RETURN)

    start_time = time.time()
    product_links = []

    while True:
        elapsed_time = time.time() - start_time  # Calculate elapsed time
        if elapsed_time > 3:  # Stop if more than 10 minutes (600 seconds)
            print("Scraping stopped after 10 minutes.")
            break

        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            product_elements = driver.find_elements(By.XPATH,
                                                    '//div[@class="sc-dkrFOg ggMaSF"]//div[@class="sc-dkrFOg ProductList__GridCol-sc-8lnc8o-0 cokuZA eCJiSA"]//a')
            for product in product_elements:
                link = product.get_attribute('href')
                if link not in product_links:
                    product_links.append(link)

        except:
            print("No more pages to scrape.")
            break

    driver.quit()
    return product_links
