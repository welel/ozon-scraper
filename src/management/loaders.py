import json
import os
from typing import Any
from urllib.parse import urljoin

import click
from sqlalchemy.orm import Session

from config import OzonScraperConfig
from database import get_session
from database.models.scraper import ScraperOzonCategoryMeta
from dto.ozon.category import OzonCategoryCreateProperties
from repositories.ozon.category import OzonCategoriesRepo


@click.command(
    "load_ozon_categories_from_api_results",
    help="Gets path to Ozon category pages, parses and loads to the db.",
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
    with get_session() as session:
        for filename in os.listdir(path):

            click.echo(f"Found file: {filename}")
            if filename.endswith(".json"):
                file_path = os.path.join(path, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        click.echo(f"Processing file: {file_path}")
                        data = json.load(file)
                        process_category_data(data.get("data"), repo, session)
                        session.commit()
                except json.JSONDecodeError as e:
                    click.echo(
                        f"Error decoding JSON in file '{file_path}': {e}"
                    )
                except Exception as e:
                    click.echo(
                        f"Unexpected error processing file '{file_path}': {e}"
                    )
                    session.rollback()


def process_category_data(
        data: dict[str, Any],
        repo: OzonCategoriesRepo,
        session: Session,
) -> None:
    if not data:
        click.echo("Error: No 'data' found in JSON.")
        return

    def recursive_parse(
            categories: list[dict[str, Any]],
            parent_id: int = None,
            level: int = 1,
    ):
        for cat in categories:
            try:
                cat_id = int(cat["url"].split("-")[-1].strip("/"))
                category_props = OzonCategoryCreateProperties(
                    id=cat_id,
                    parent_id=parent_id,
                    level=level,
                    url=urljoin(OzonScraperConfig.domain, cat["url"]),
                    short_url=OzonScraperConfig.short_category_url.format(
                        cat_id=cat_id
                    ),
                    name=cat.get("title"),
                    image_url=cat.get("image"),
                )
                repo.create_or_update(category_props)
                session.add(
                    ScraperOzonCategoryMeta(category_id=category_props.id)
                )
                click.echo(f"Processed category: {category_props.name}")

                if "categories" in cat:
                    recursive_parse(
                        cat["categories"],
                        parent_id=category_props.id,
                        level=level + 1,
                    )
            except Exception as e:
                click.echo(
                    f"Error processing category '{cat.get('title')}': {e}"
                )

    root_category = OzonCategoryCreateProperties(
        id=data["id"],
        level=1,
        url=urljoin(OzonScraperConfig.domain, data["url"]),
        short_url=OzonScraperConfig.short_category_url.format(
            cat_id=data["id"]
        ),
        name=data["title"],
        image_url=data["image"],
    )
    repo.create_or_update(root_category)
    session.add(ScraperOzonCategoryMeta(category_id=root_category.id))

    if "columns" in data:
        for column in data["columns"]:
            recursive_parse(
                column.get("categories", []),
                root_category.id,
                level=2,
            )
    else:
        click.echo("Error: No 'columns' found in the data.")
