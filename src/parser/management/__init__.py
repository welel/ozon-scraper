from .loaders import load_ozon_categories_from_api_results
from .ozon_parsers import (
    parse_ozon_category_pages,
)

import click


@click.group()
def cli():
    pass


cli.add_command(load_ozon_categories_from_api_results)
cli.add_command(parse_ozon_category_pages)
