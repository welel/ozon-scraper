from typing import Optional

from pydantic import BaseModel
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from dto.ozon_product import OzonProduct
from dto.ozon_review import CreateOzonReviewProperties
from dto.ozon_review_media import CreateOzonReviewMediaProperties
from ..abstract import LoadedData, ValidatedData
from .ozon import OzonLoader


class OzonReviewsData(BaseModel):
    review: CreateOzonReviewProperties
    media: CreateOzonReviewMediaProperties


class OzonReviewsLoader(OzonLoader):
    """Loads reviews and its media from product reviews."""
    schema = OzonReviewsData
    wait_time = 5

    def __init__(self, *args, product: OzonProduct, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = product
        self.media_number = 0

        # Get to media review section if exists
        section_url_els = self.driver.find_elements(By.CLASS_NAME, "e8014-a5")
        last_url_el = section_url_els[-1]
        url = last_url_el.get_attribute("href") or ""
        if url.strip("/").endswith("videos"):
            self.max_media_number = int(
                last_url_el.find_element(By.CLASS_NAME, "e8014-a9").text
            )
            last_url_el.click()
            self._wait()
            self._scroll_down_until_bottom(step=700, step_in_row=3)
        else:
            self.max_media_number = 0

    def _load(self) -> Optional[LoadedData]:
        if self.max_media_number == 0:
            self.logger.info("No media for %s product", self.product.sku_id)
            return None

        self.bypass_captcha()
        self.bypass_age_banner()

        try:
            left = self.driver.find_element(By.CLASS_NAME, "ys7_29")
            right = self.driver.find_element(By.CLASS_NAME, "sy2_29")

            # review_uuid
            review_uuid = right.find_element(
                By.CLASS_NAME, "q0t_29"
            ).get_attribute("data-review-uuid")

            # review_puuid
            review_puuid = None

            # rating
            rating_el = self.driver.find_element(By.CLASS_NAME, "a5d14-a")
            star_style = "color: rgb(255, 168, 0);"
            svgs = rating_el.find_elements(By.TAG_NAME, "svg")
            rating = 0
            for svg in svgs:
                rating += svg.get_attribute("style") == star_style

            # user_name
            user_name = right.find_element(By.CLASS_NAME, "z0p_29").text

            # user_image_url
            try:
                user_image_url = right.find_element(
                    By.CLASS_NAME, "vp5_29"
                ).get_attribute("src")
            except NoSuchElementException:
                user_image_url = None

            # comment_count
            comment_count = int(
                right.find_element(By.CLASS_NAME, "s3y_29").text
            )

            # Expand review button
            expand_btn = right.find_element(By.CLASS_NAME, "q3t_29")
            ActionChains(self.driver).move_to_element(expand_btn).perform()
            expand_btn.click()

            # url
            popup_el = left.find_element(By.CLASS_NAME, "ag015-a0")
            ActionChains(self.driver).move_to_element(popup_el).perform()
            copy_url_btn = self.driver.find_elements(
                By.CLASS_NAME, "tsHeadline500Small"
            )[-1]
            copy_url_btn.click()
            url = self._get_clipboard_text()

            # like/dislike count
            like_btns = right.find_elements(By.CLASS_NAME, "b2113-a8")
            like_count = int(like_btns[0].text.split()[-1])
            dislike_count = int(like_btns[1].text.split()[-1])

            texts = {
                "text": None,
                "advantages_text": None,
                "disadvantages_text": None,
            }

            review_text_el = right.find_element(By.CLASS_NAME, "tq2_29")
            review_text_sections = review_text_el.find_elements(
                By.CLASS_NAME, "sq5_29"
            )
            for text_section in review_text_sections:
                text = text_section.find_element(By.TAG_NAME, "span").text
                try:
                    header_el = text_section.find_element(
                        By.CLASS_NAME, "q5s_29"
                    )
                except NoSuchElementException:
                    texts["text"] = text
                    break

                header = header_el.text.strip()

                if header == "Достоинства":
                    texts["advantages_text"] = text
                elif header == "Недостатки":
                    texts["disadvantages_text"] = text
                else:
                    texts["text"] = text

            review = CreateOzonReviewProperties(
                parsed_by_product_id=self.product.id,
                sku_id=self.product.sku_id,
                review_uuid=review_uuid,
                review_puuid=review_puuid,
                rating=rating,
                user_name=user_name,
                user_image_url=user_image_url,
                comment_count=comment_count,
                url=url,
                like_count=like_count,
                dislike_count=dislike_count,
                text=texts["text"],
                advantages_text=texts["advantages_text"],
                disadvantages_text=texts["disadvantages_text"],
            )

            # template_url
            template_url = None

            try:
                video_el = left.find_element(By.TAG_NAME, "video-player")
                type_ = "video"
                url = video_el.get_attribute("src")
            except NoSuchElementException:
                type_ = "image"
                url = left.find_element(
                    By.TAG_NAME, "img"
                ).get_attribute("src")

            extension = url.split(".")[-1]

            review_media = CreateOzonReviewMediaProperties(
                review_id=1,
                type=type_,
                url=url,
                template_url=template_url,
                extension=extension,
            )
            return OzonReviewsData(review=review, media=review_media)
        except Exception as e:
            self.logger.exception("Invalid product review: %s", e)
            self._init_next_page(None)
            return self.load()
        finally:
            self.media_number += 1  # No right (stack overflow)

    def _stop_expr(self, data: ValidatedData) -> bool:
        self.logger.info(
            "Media number state %s/%s",
            self.media_number,
            self.max_media_number,
        )
        return self.media_number >= self.max_media_number
    
        # also check existance of next button

    def _init_next_page(self, data: LoadedData):
        self.logger.info("Loading next page...")
        right = self.driver.find_element(By.CLASS_NAME, "sy2_29")
        ActionChains(self.driver).move_to_element(right).click().perform()
        ActionChains(self.driver).send_keys(Keys.ARROW_RIGHT).perform()
        self._wait(10)
