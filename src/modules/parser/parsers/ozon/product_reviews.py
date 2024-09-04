
import logging

from config import AppConfig
from repos.ozon_product import OzonProductsRepo
from repos.ozon_review import OzonReviewRepo
from repos.ozon_review_media import OzonReviewMediaRepo
from loaders.ozon.reviews import OzonReviewsLoader
from ..abstract import AbstractParser


class OzonReviewsParser(AbstractParser):
    logger = logging.getLogger(AppConfig.logger_prefix + __name__)

    def run(self):
        products_repo = OzonProductsRepo()
        products = products_repo.get_list_on_parsing()
        self.logger.info("Fetch %s products on parsing", len(products))

        reviews_repo = OzonReviewRepo()
        reviews_media_repo = OzonReviewMediaRepo()
        for product in list(reversed(products))[60:]:
            self.logger.info("Parse product: %s", product.url)
            reviews_url = (
                f"https://www.ozon.ru/product/{product.sku_id}/reviews"
            )
            for review_data in OzonReviewsLoader(
                    reviews_url, product=product
            ).iload():
                reviews_repo.create_or_update(review_data.review)
                reviews_media_repo.create_or_update(review_data.media)
        self.logger.info("Finished parsing.")
