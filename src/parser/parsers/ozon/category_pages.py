
import logging

from config import AppConfig
from repos.ozon_product import OzonProductsRepo
from repos.ozon_category import OzonCategoriesRepo
from loaders.ozon.products import OzonProductsLoader
from ..abstract import AbstractParser


class OzonCategoriesParser(AbstractParser):
    logger = logging.getLogger(AppConfig.logger_prefix + __name__)

    def run(self):
        cat_repo = OzonCategoriesRepo()
        cats = cat_repo.get_list_on_parsing()
        self.logger.info("Fetch %s categories on parsing", len(cats))
        urls = [str(cat.short_url) for cat in cats]

        prod_repo = OzonProductsRepo()
        for url in urls:
            self.logger.info("Parse category: %s", url)
            for product_batch in OzonProductsLoader(url).iload():
                for product in product_batch:
                    prod_repo.create_or_update(product)
        self.logger.info("Finished parsing.")
