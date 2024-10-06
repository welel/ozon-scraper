import hashlib
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel
from selenium.webdriver.common.by import By

from dto.ozon.product import OzonProduct
from dto.ozon.review import OzonReviewCreateProperties
from dto.ozon.review_media import OzonReviewMediaCreateProperties

from ..abstract import LoadedData
from .ozon import OzonLoader
from .schemas import ReviewsDataState


class OzonReviewsData(BaseModel):
    reviews: list[OzonReviewCreateProperties]
    media: list[OzonReviewMediaCreateProperties]


def time_to_seconds(time_str: str) -> int | None:
    try:
        time_obj = datetime.strptime(time_str, "%M:%S")
        return time_obj.hour * 3600 + time_obj.minute * 60
    except ValueError:
        return None


def to_md5(data: Any) -> str:
    return hashlib.md5(str(data).encode()).hexdigest()


class OzonReviewsLoader(OzonLoader):
    """Loads reviews and its media from product reviews."""
    schema = OzonReviewsData
    wait_time = 5

    def __init__(self, *args, product: OzonProduct, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = product
        self.media_number = 0

        # Get to media review section if exists
        section_url_els = self.driver.find_elements(By.CLASS_NAME, "e8016-a")
        last_url_el = section_url_els[-1]
        url = last_url_el.get_attribute("href") or ""
        if url.strip("/").endswith("videos"):
            self.media_number = int(
                last_url_el.find_element(By.CLASS_NAME, "e8016-a4").text
            )
            last_url_el.click()
            self._wait()
            self._scroll_down_until_bottom(
                step_px=700, step_in_row=2, max_step=4
            )
        else:
            self.media_number = 0

    def _load(self) -> Optional[LoadedData]:
        if self.media_number == 0:
            self.logger.info("No media for %s product", self.product.sku_id)
            self._shutdown()
            return None

        self.bypass_captcha()
        self.bypass_age_banner()

        try:
            reviews_state_el = self.driver.find_element(
                By.XPATH,
                value="//*[starts-with(@id, 'state-webReviewGallery-')]",
            )
            data = reviews_state_el.get_attribute("data-state")
            data = ReviewsDataState.model_validate_json(data)

            reviews_data = []
            for review in data.reviews.values():

                if review.is_anonymous:
                    user_name = None
                else:
                    user_name = review.author.first_name.strip()

                reviews_data.append(OzonReviewCreateProperties(
                    uuid=review.uuid,
                    product_sku_id=self.product.sku_id,
                    rating=review.content.score,
                    user_name=user_name,
                    user_image_url=review.author.avatar_url or None,
                    comment_count=review.comments.total_count,
                    url=review.sharing.url,
                    like_count=review.usefulness.useful,
                    dislike_count=review.usefulness.unuseful,
                    comment_text=review.content.comment,
                    advantages_text=review.content.positive,
                    disadvantages_text=review.content.negative,
                ))

            media_data = []
            for media in data.media:
                media_data.append(OzonReviewMediaCreateProperties(
                    id=to_md5(media.url),
                    review_uuid=media.review_uuid,
                    type=media.type.lower(),
                    url=media.url,
                    extension=media.url.split(".")[-1],
                    video_duration_sec=time_to_seconds(media.video_duration),
                    width=media.size.width,
                    height=media.size.height,
                ))

            return OzonReviewsData(reviews=reviews_data, media=media_data)

        except Exception as e:
            self.logger.exception("Invalid product review: %s", e)
