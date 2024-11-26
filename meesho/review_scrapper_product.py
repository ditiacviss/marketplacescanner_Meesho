# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import time
#
#
# def extract_comments(driver):
#     """Extract all comments visible on the current page."""
#     comment_list = []
#     comments_scrapped = driver.find_elements(By.XPATH,"//div[@class='sc-bqWxrE odKwF Comment__FlexRow-sc-1ju5q0e-1 cTbiMl Comment__FlexRow-sc-1ju5q0e-1 cTbiMl'][1]")
#     for comment in comments_scrapped:
#         comment_list.append(comment.text)
#     return comment_list
#
# def review_scrapper_product(data_dict):
#     """Scrape reviews for products listed in data_dict."""
#     # chrome_driver_path = "meesho/chromedriver.exe"
#     # service = Service(chrome_driver_path)
#     chrome_options = Options()
#
#     # driver = webdriver.Chrome(service=service)
#     # driver = webdriver.Chrome(ChromeDriverManager().install())
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#
#     product_comments = {}
#
#     for key, value in data_dict.items():
#         product_comments[key] = {}
#         product_url = value.get("Product_url")
#         driver.get(product_url)
#         print(f"Processing product: {key}, URL: {product_url}")
#         time.sleep(5)
#
#         try:
#             # Locate and click the "All Reviews" button
#             all_reviews_button = WebDriverWait(driver, 15).until(
#                     EC.element_to_be_clickable((By.XPATH, "//div/span[contains(text(), 'all reviews')]")))
#             driver.execute_script("arguments[0].click();", all_reviews_button)
#             # all_reviews_button.click()
#             if all_reviews_button.is_displayed():
#                 all_reviews_button.click()
#                 time.sleep(10)
#
#         except TimeoutException:
#             print(f"The 'All Reviews' button was not found for {key}. Skipping...")
#             continue
#
#         comments_data = []
#         scraped_comments = set()
#
#         count=0
#         while count < 20:
#             comments_list = extract_comments(driver)
#             new_comments = [comment for comment in comments_list if comment not in scraped_comments]
#             if new_comments:
#                 comments_data.extend(new_comments)
#                 scraped_comments.update(new_comments)
#             else:
#                 print("No new comments found, stopping pagination.")
#                 break
#
#             try:
#                 next_button = WebDriverWait(driver, 10).until(
#                     EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'View more')]]"))
#                 )
#                 driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
#                 next_button.click()
#                 time.sleep(10)
#                 count += 1
#
#             except TimeoutException:
#                 print("The 'View more' button was not found. Stopping pagination.")
#                 break
#
#         # Save comments to the result dictionary
#         product_comments[key]["Product_url"] = product_url
#         product_comments[key]["reviews"] = comments_data
#
#     driver.quit()
#     return product_comments
#
#


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def extract_comments(driver):
    comment_list = []
    try:
        comments_scrapped = driver.find_elements(By.XPATH,"//div[@class='sc-bqWxrE odKwF Comment__FlexRow-sc-1ju5q0e-1 cTbiMl Comment__FlexRow-sc-1ju5q0e-1 cTbiMl'][1]")
        for comment in comments_scrapped:
            comment_list.append(comment.text)
    except Exception as e:
        print(f"Error extracting comments: {e}")
    return comment_list

# Main function for scraping reviews
def review_scrapper_product(data_dict):
    """Scrape reviews for products listed in data_dict."""
    chrome_options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    product_comments = {}

    for key, value in data_dict.items():
        product_comments[key] = {}
        product_url = value.get("Product_url")
        driver.get(product_url)
        print(f"Processing product: {key}, URL: {product_url}")

        try:
            time.sleep(2)  # Allow the page to load

            all_reviews_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div/span[contains(text(), 'all reviews')]")))
            driver.execute_script("arguments[0].click();", all_reviews_button)
            if all_reviews_button.is_displayed():
                all_reviews_button.click()
                time.sleep(5)

        except TimeoutException:
            print(f"The 'All Reviews' button was not found for {key}. Skipping...")
            continue

        comments_data = []
        scraped_comments = set()

        count = 0
        while count < 10:
            time.sleep(5)
            comments_list = extract_comments(driver)
            # time.sleep(5)
            new_comments = [comment for comment in comments_list if comment not in scraped_comments]
            if new_comments:
                comments_data.extend(new_comments)
                scraped_comments.update(new_comments)
            else:
                print("No new comments found, stopping pagination.")
                break

            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'View more')]]"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                next_button.click()
                time.sleep(5)
                count += 1

            except TimeoutException:
                print("The 'View more' button was not found. Stopping pagination.")
                break

            product_comments[key]["Product_url"] = product_url
            product_comments[key]["reviews"] = comments_data

    driver.quit()
    return product_comments




