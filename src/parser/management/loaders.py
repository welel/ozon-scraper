import json
import os
from typing import Any
from urllib.parse import urljoin

import click

from config import OzonParserConfig
from dto.ozon_category import CreateOzonCategoryProperties
from repos.ozon_category import OzonCategoriesRepo


@click.command(
    "load_ozon_categories_from_api_results",
    help="Gets path to ozon category pages, parses and loads to the db.",
)
@click.option(
    "--path",
    type=str,
    required=True,
    help=(
        "Path to a directory, that contains JSON files with results of "
        "https://www.ozon.ru/api/composer-api.bx/_action/v2/categoryChildV3 "
        "Ozon API call, that contains information about categories."
    ),
)
def load_ozon_categories_from_api_results(path: str):
    if not os.path.exists(path):
        click.echo(f"Error: The specified path '{path}' does not exist.")
        return
    if not os.path.isdir(path):
        click.echo(
            f"Error: The specified path '{path}' isn't a directory."
        )
        return

    repo = OzonCategoriesRepo()

    for filename in os.listdir(path):
        click.echo(filename)
        if filename.endswith(".json"):
            file_path = os.path.join(path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    click.echo(f"Processing file: {file_path}")
                    process_category_data(data.get("data"), repo)
            except json.JSONDecodeError as e:
                click.echo(f"Error decoding JSON in file '{file_path}': {e}")
            except Exception as e:
                click.echo(
                    f"Unexpected error processing file '{file_path}': {e}"
                )
                raise


def process_category_data(data: dict[str, Any], repo: OzonCategoriesRepo):
    if not data:
        click.echo("Error: No 'data' found in JSON.")
        return

    def recursive_parse(
            categories: list[dict[str, Any]], parent_id: int = None
    ):
        for category in categories:
            try:
                cat_id = int(category["url"].split("-")[-1].strip("/"))
                category_props = CreateOzonCategoryProperties(
                    id=cat_id,
                    parent_id=parent_id,
                    url=urljoin(OzonParserConfig.domain, category["url"]),
                    short_url=OzonParserConfig.short_cat_url.format(
                        cat_id=cat_id
                    ),
                    name=category.get("title"),
                    image_url=category.get("image"),
                )
                repo.create_or_update(category_props)
                click.echo(f"Processed category: {category_props.name}")

                # Recurse into subcategories if they exist
                if "categories" in category:
                    recursive_parse(
                        category["categories"], parent_id=category_props.id,
                    )
            except Exception as e:
                click.echo(
                    f"Error processing category '{category.get('title')}': {e}"
                )

    root_category = CreateOzonCategoryProperties(
        id=data["id"],
        url=urljoin(OzonParserConfig.domain, data["url"]),
        short_url=OzonParserConfig.short_cat_url.format(cat_id=data["id"]),
        name=data["title"],
        image_url=data["image"],
    )
    repo.create_or_update(root_category)

    if "columns" in data:
        for column in data["columns"]:
            recursive_parse(column.get("categories", []), root_category.id)
    else:
        click.echo("Error: No 'columns' found in the data.")
