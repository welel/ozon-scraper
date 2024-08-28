import random
import time
import json

from selenium import webdriver
from selenium.webdriver.common.by import By

from config import CHROME_DRIVER_PATH


service = webdriver.ChromeService(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

url_0 = "https://www.ozon.ru/product/754160802/videos/"
url_1 = "https://www.ozon.ru/product/1467398550/videos/"
url = "https://www.ozon.ru/product/1624319419/videos/"

driver.get(url)

time.sleep(50)
print("Parsing starts after 10 seconds...")
time.sleep(10)
print(1)

# with open("reviews_imgs.json", "w+") as json_file:
#     imgs = driver.find_elements(By.TAG_NAME, value="img")
#     img_urls = []
#     for img in imgs:
#         try:
#             img_urls.append(img.get_attribute("src").replace("wc300", "wc1000"))
#         except:
#             pass
#     json.dump(imgs, json_file, default=str, indent=2, ensure_ascii=False)



total_review_el = driver.find_elements(By.CLASS_NAME, value="e8014-a9")[-1]
total_review = int(total_review_el.text) if total_review_el.text.isdigit() else 0
print(f"Total reviews: {total_review}")

with open("reviews.json", "w+") as json_file:
    data = []
    try:
        for _ in range(total_review):

            print("Open card")
            card = driver.find_element(By.CLASS_NAME, value="s1y_29")

            comment_num_el = card.find_element(By.CLASS_NAME, value="y2s_29")
            comment_num = int(comment_num_el.text) if comment_num_el.text.isdigit() else 0

            try:
                player = card.find_element(By.TAG_NAME, "video-player")
                video_url = player.get_attribute("src")
            except:
                video_url = None

            try:
                img = card.find_element(By.TAG_NAME, "img")
                imgae_url = img.get_attribute("src")
            except:
                imgae_url = None

            review_uuid_el = card.find_element(By.CLASS_NAME, value="sy7_29")
            review_puuid = review_uuid_el.get_attribute("uuid")
            review_uuid = review_uuid_el.get_attribute("reviewuuid")
            review_url = f"{url[:-8]}?reviewUuid={review_uuid}&reviewPuuid={review_puuid}"

            user_name_el = card.find_element(By.CLASS_NAME, value="p0z_29")
            user_name = user_name_el.text

            data.append({
                "url": url,
                "review_puuid": review_puuid,
                "review_uuid": review_uuid,
                "review_url": review_url,
                "video_url": video_url,
                "image_url": imgae_url,
                "comments_count": comment_num,
                "user_name": user_name,
            })
            print("Card added: %s", data[-1])

            next_btn = driver.find_element(By.XPATH, value="//button[contains(@aria-label, 'Next')]")
            next_btn.click()
            print("Click Next")
            time.sleep(random.randint(2, 4))

    finally:
        json.dump(data, json_file, default=str, indent=2, ensure_ascii=False)
