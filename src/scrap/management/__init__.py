import click

from .export import export_media
from .loaders import load_ozon_categories_from_api_results
from .ozon_scrapers import (
    scrape_ozon_category_pages,
    scrape_ozon_product_reviews,
)


@click.group()
def cli() -> None:
    pass


cli.add_command(load_ozon_categories_from_api_results)
cli.add_command(scrape_ozon_category_pages)
cli.add_command(scrape_ozon_product_reviews)
cli.add_command(export_media)
