import time
import json

from selenium import webdriver
from selenium.webdriver.common.by import By

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


if __name__ == "__main__":
    service = webdriver.ChromeService(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service)

    cat_url = "https://www.ozon.ru/category/bodi-i-korsazhi-zhenskie-31309"

    driver.get(cat_url)

    time.sleep(15)

    for i in range(5):
        time.sleep(5)
        print(i)
        parsed_items = get_parsed_items(driver)
        with open(f"parsed_items_page_{i}.json", "w+") as json_file:
            json.dump(parsed_items, json_file, default=str, indent=2, ensure_ascii=False)

        next_page_btn_el = driver.find_element(By.CLASS_NAME, value="q1e")
        next_page_btn_el.click()
