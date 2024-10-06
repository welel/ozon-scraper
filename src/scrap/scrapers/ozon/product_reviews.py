
import logging

from scrap.config import AppConfig
from scrap.repositories.ozon.product import OzonProductsRepository
from scrap.repositories.ozon.review import OzonReviewsRepository
from scrap.repositories.ozon.review_media import OzonReviewMediaRepository

from ...loaders.ozon.reviews import OzonReviewsLoader
from ..abstract import Scraper


class OzonReviewsStateScraper(Scraper):
    logger = logging.getLogger(AppConfig.logger_prefix + __name__)

    def run(self) -> None:
        products_repo = OzonProductsRepository()
        products = products_repo.get_list_on_parsing()
        self.logger.info("Fetch %s products on parsing", len(products))

        reviews_repo = OzonReviewsRepository()
        reviews_media_repo = OzonReviewMediaRepository()
        for product in products:
            try:
                self.logger.info("Scrape product: %s", product.url)
                reviews_url = (
                    f"https://www.ozon.ru/product/{product.sku_id}/reviews"
                )
                data = OzonReviewsLoader(reviews_url, product=product).load()
                if data is None:
                    continue
                self.logger.info(
                    "Scraped %d reviews and %d media",
                    len(data.reviews), len(data.media)
                )
                for review in data.reviews:
                    reviews_repo.create_or_update(review)
                for media in data.media:
                    reviews_media_repo.create_or_update(media)
            except Exception as e:
                self.logger.exception(
                    "Failed to scrape product %s: %s", product, e
                )
        self.logger.info("Finished parsing.")
