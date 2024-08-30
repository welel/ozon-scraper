import time
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.123 YaBrowser/23.9.1.962 Yowser/2.5 Safari/537.36"

# options = uc.ChromeOptions()
# options.add_argument(f"user-agent={USER_AGENT}")
# driver = uc.Chrome(options=options)
# driver = uc.Chrome(driver_executable_path="/usr/bin/chromedriver")


driver.get("https://www.ozon.ru/category/nizhnee-bele-zhenskoe-7538/")


print(1)

items = driver.find_elements(By.XPATH, value="//div[contains(@class, 'widget-search-result-container')]//a[contains(@class, 'tile-hover-target') and not(@data-prerender='true')]")
parsed_items = [{"title": item.text, "url": item.get_attribute("href")} for item in items]

images = driver.find_elements(By.XPATH, value="//div[contains(@class, 'widget-search-result-container')]//img")
for i, image in enumerate(images):
    if i >= len(parsed_items):
        break
    try:
        parsed_items[i]["image_url"] = image.get_attribute("src")
    except Exception:
        pass

with open("parsed_items_3.json", "w+") as json_file:
    json.dump(parsed_items, json_file, default=str, indent=2, ensure_ascii=False)
