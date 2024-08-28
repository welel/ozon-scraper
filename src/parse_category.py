import time
import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

from config import CHROME_DRIVER_PATH


def get_parsed_items(driver):
    items = driver.find_elements(By.XPATH, value="//div[contains(@class, 'widget-search-result-container')]//a[contains(@class, 'tile-hover-target') and not(@data-prerender='true')]")

    parsed_items = []
    for item in items:
        try:
            url = item.get_attribute("href")
            parsed_items.append({
                "title": item.text,
                "url": url,
                "id": url.split("?")[0].strip("/").split("-")[-1],
            })
        except:
            print("Bad item.")

    images = driver.find_elements(By.XPATH, value="//div[contains(@class, 'widget-search-result-container')]//img")
    for i, image in enumerate(images):
        if i >= len(parsed_items):
            break
        try:
            parsed_items[i]["image_url"] = image.get_attribute("src")
        except Exception:
            parsed_items[i]["image_url"] = None
    return parsed_items


CATEGORY_URL = "https://www.ozon.ru/category/bodi-i-korsazhi-zhenskie-31309"
PAGE_NUM = 5
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.123 YaBrowser/23.9.1.962 Yowser/2.5 Safari/537.36"

if __name__ == "__main__":
    # options = Options()
    # # options.add_argument('--headless=new')
    # options.add_argument("window-size=1920,1080")
    # service = webdriver.ChromeService(executable_path=CHROME_DRIVER_PATH)
    # driver = webdriver.Chrome(options=options, service=service)

    options = uc.ChromeOptions()
    options.add_argument(f"user-agent={USER_AGENT}")
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = uc.Chrome(options=options, driver_executable_path=CHROME_DRIVER_PATH)

    parsed_items = []
    json_file = open("parsed_items_page.json", "w+")

    try:
        driver.get(CATEGORY_URL)

        time.sleep(10)

        while True:
            try:
                el = driver.find_element(by=By.CLASS_NAME, value="rb")
                print(f"Reload btn found: {el.get_attribute('outerHTML')}")
                el.click()
                print(driver.get_log('browser'))
                print(driver.get_log('driver'))
                time.sleep(5)
            except NoSuchElementException:
                print("Reload btn isn't found")
                break

        for i in range(PAGE_NUM):
            time.sleep(5)
            print(i)
            driver.get_screenshot_as_file(f'screen_{i}.png')
            parsed_items_batch = get_parsed_items(driver)
            # print(f"Parsed: {parsed_items_batch}")
            parsed_items.extend(parsed_items_batch)

            next_page_btn_el = driver.find_element(By.CLASS_NAME, value="q1e")
            next_page_btn_el.click()
    finally:
        # print(f"Write: {parsed_items}")
        json.dump(parsed_items, json_file, default=str, indent=2, ensure_ascii=False)
        json_file.close()
