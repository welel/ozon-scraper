
import logging

from scrap.config import AppConfig
from scrap.repositories.ozon.category import OzonCategoriesRepo
from scrap.repositories.ozon.product import OzonProductsRepo

from ...loaders.ozon.products import OzonProductsLoader
from ..abstract import Scraper


class OzonCategoriesScraper(Scraper):
    logger = logging.getLogger(AppConfig.logger_prefix + __name__)

    def run(self) -> None:
        cat_repo = OzonCategoriesRepo()
        cats = cat_repo.get_list_on_parsing()
        self.logger.info("Fetch %s categories on parsing", len(cats))

        prod_repo = OzonProductsRepo()
        for cat in cats:
            self.logger.info("Scrape category: %s", cat.short_url)
            for product_batch in OzonProductsLoader(
                    str(cat.short_url), cat_id=cat.id
            ).iload():
                self.logger.info("Scraped %d products", len(product_batch))
                for product in product_batch:
                    prod_repo.create_or_update(product)
        self.logger.info("Finished parsing.")
