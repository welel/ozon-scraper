from .loaders import load_ozon_categories_from_api_results

import click


@click.group()
def cli():
    pass


cli.add_command(load_ozon_categories_from_api_results)
