from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import time

# Function to extract comments
def extract_comments(driver):
    """Extract all comments visible on the current page."""
    comment_list = []
    try:
        comments_scrapped = driver.find_elements(
            By.XPATH, "//div[contains(@class, 'sc-bqWxrE odKwF Comment__FlexRow-sc-1ju5q0e-1 cTbiMl Comment__FlexRow-sc-1ju5q0e-1 cTbiMl')][1]"
        )
        for comment in comments_scrapped:
            comment_list.append(comment.text)
    except Exception as e:
        print(f"Error extracting comments: {e}")
    return comment_list

# Main function for scraping reviews
def review_scrapper_seller(data_dict):
    """Scrape reviews for products listed in data_dict."""
    chrome_options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    wait = WebDriverWait(driver, 10)  # Adjust timeout as needed

    product_comments = {}

    for key, value in data_dict.items():
        url = value.get("Product_url")
        seller_name = value["details"].get("seller_name", "Unknown")
        seller_rating = value["details"].get("seller_rating", "Unknown")

        # Initialize product data
        product_comments[key] = {
            "seller_name": seller_name,
            "seller_rating": seller_rating,
            "url": url,
            "reviews": [],
        }

        try:
            driver.get(url)
            time.sleep(2)  # Allow the page to load

            comments_data = []
            scraped_comments = set()

            # Wait for the "Load Comments" button and click it
            load_comments = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='sc-ftTHYK lcmpLa ShopCardstyled__BottomSection-sc-du9pku-5 hPfDac ShopCardstyled__BottomSection-sc-du9pku-5 hPfDac']/div[1] | //div[@class='sc-jrcTuL iLAawV ShopCardstyled__ValuePropCard-sc-du9pku-11 ioZPYn ShopCardstyled__ValuePropCard-sc-du9pku-11 ioZPYn'][1]"))
            )
            if load_comments.is_displayed():
                load_comments.click()
                time.sleep(2)

            count = 0
            while count < 10:
                # time.sleep(5)
                comments_list = extract_comments(driver)
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
                    time.sleep(2)  # Wait for new comments to load
                    count+=1
                except TimeoutException:
                    print("The 'View more' button was not found. Stopping pagination.")
                    break

                # Save comments to the dictionary
                product_comments[key]["reviews"] = comments_data

        except Exception as e:
            print(f"Error processing product {key}: {e}")

    driver.quit()
    return product_comments




