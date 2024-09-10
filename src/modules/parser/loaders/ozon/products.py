import re
from typing import Optional

from pydantic import RootModel
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from dto.ozon.product import OzonProductCreateProperties
from ..abstract import LoadedData, ValidatedData
from .ozon import OzonLoader


class OzonProductList(RootModel):
    root: list[OzonProductCreateProperties]


class OzonProductsLoader(OzonLoader):
    """Loads products from a category page."""
    schema = OzonProductList
    wait_time = 5
    max_depth: int

    def __init__(self, *args, cat_id: int, max_depth: int = 40, **kwargs):
        super().__init__(*args, **kwargs)
        self.cat_id = cat_id
        self.depth = 1
        self.max_depth = max_depth

    def _load(self) -> Optional[LoadedData]:
        self.bypass_captcha()
        self.bypass_age_banner()

        product_cards = self.driver.find_elements(By.CLASS_NAME, "tile-root")
        self.logger.info("Fetched %s product cards", len(product_cards))

        products = []
        for card in product_cards:
            try:

                # URL
                url_el = card.find_elements(By.TAG_NAME, "a")[-1]
                url = url_el.get_attribute("href")
                url = url.split("?")[0]

                # SKU_ID
                sku_id = int(url.strip("/").split("-")[-1])

                # NAME
                name = url_el.text

                # PRIECES
                price_els = card.find_elements(By.CLASS_NAME, "c3015-a1")
                if len(price_els) == 1:
                    price = original_price = price_els[0].text
                else:
                    price = price_els[0].text
                    original_price = price_els[1].text
                price = int(price.replace("\u2009", "").replace("₽", ""))
                original_price = int(
                    original_price.replace("\u2009", "").replace("₽", "")
                )

                # STOCK
                try:
                    stock = card.find_element(By.CLASS_NAME, "e6012-a4").text
                    stock = int(re.search(r'\d+', stock).group())
                except NoSuchElementException:
                    stock = None

                # RATINGS
                try:
                    rating_els = card.find_element(
                        By.CLASS_NAME, "tsBodyMBold"
                    )
                    rating_els = rating_els.find_elements(By.CLASS_NAME, "q2")
                    rating = float(rating_els[0].text)
                    review_count = rating_els[1].text
                    review_count = review_count.replace("\u2009", "")
                    review_count = int(re.search(r'\d+', review_count).group())
                except NoSuchElementException:
                    rating = review_count = None

                # IMAGE URL
                image_el = card.find_element(By.TAG_NAME, "img")
                image_url = image_el.get_attribute("src")

                products.append(OzonProductCreateProperties(
                    sku_id=sku_id,
                    name=name,
                    price=price,
                    original_price=original_price,
                    stock=stock,
                    rating=rating,
                    review_count=review_count,
                    url=url,
                    image_url=image_url,
                    category_id=self.cat_id,
                ))

            except Exception as e:
                self.logger.warning("Bad card: %s, data: %s", e, card)
        self.depth += 1
        return products

    def _stop_expr(self, data: ValidatedData) -> bool:
        self.logger.info("Depth state %s/%s", self.depth, self.max_depth)
        if self.depth >= self.max_depth:
            return True
        try:
            # Check next page button
            self.driver.find_element(By.CLASS_NAME, value="qe2")
        except NoSuchElementException:
            return True
        return False

    def _init_next_page(self, data: LoadedData):
        self.logger.info("Loading next page...")
        next_page_btn_el = self.driver.find_element(By.CLASS_NAME, value="qe2")
        next_page_btn_el.click()
        self._wait()
