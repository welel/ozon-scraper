
import logging

from config import AppConfig
from repositories.ozon.product import OzonProductsRepo
from repositories.ozon.review import OzonReviewsRepo
from repositories.ozon.review_media import OzonReviewMediaRepo

from ...loaders.ozon.reviews import OzonReviewsLoader
from ..abstract import AbstractParser


class OzonReviewsStateParser(AbstractParser):
    logger = logging.getLogger(AppConfig.logger_prefix + __name__)

    def run(self):
        products_repo = OzonProductsRepo()
        products = products_repo.get_list_on_parsing()
        self.logger.info("Fetch %s products on parsing", len(products))

        reviews_repo = OzonReviewsRepo()
        reviews_media_repo = OzonReviewMediaRepo()
        for product in products:
            try:
                self.logger.info("Parse product: %s", product.url)
                reviews_url = (
                    f"https://www.ozon.ru/product/{product.sku_id}/reviews"
                )
                data = OzonReviewsLoader(reviews_url, product=product).load()
                if data is None:
                    continue
                self.logger.info(
                    "Parsed %d reviews and %d media",
                    len(data.reviews), len(data.media)
                )
                for review in data.reviews:
                    reviews_repo.create_or_update(review)
                for media in data.media:
                    reviews_media_repo.create_or_update(media)
            except Exception as e:
                self.logger.exception(
                    "Failed to parse product %s: %s", product, e
                )
        self.logger.info("Finished parsing.")
