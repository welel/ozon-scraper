from .export import export_media
from .label_studio_import import import_label_studio_labels
from .loaders import load_ozon_categories_from_api_results
from .moderation_bot import start_moderation_bot
from .ozon_parsers import (
    parse_ozon_category_pages,
    parse_ozon_product_reviews,
)

import click


@click.group()
def cli():
    pass


cli.add_command(load_ozon_categories_from_api_results)
cli.add_command(parse_ozon_category_pages)
cli.add_command(parse_ozon_product_reviews)
cli.add_command(export_media)
cli.add_command(import_label_studio_labels)
cli.add_command(start_moderation_bot)
