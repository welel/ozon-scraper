import json
import os
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import click
from sqlalchemy.orm import Session

from scrap.config import OzonScraperConfig, ProjectConfig
from scrap.database import get_session
from scrap.database.models.scraper import ScraperOzonCategoryMeta
from scrap.dto.ozon.category import OzonCategoryCreateProperties
from scrap.repositories.ozon.category import OzonCategoriesRepository


@click.command(
    "load_ozon_categories_from_api_results",
    help="Gets path to Ozon category pages, parses and loads to the db.",
)
@click.option(
    "--path",
    type=str,
    default=ProjectConfig.categories_data_dir,
    help=(
        "Path to a directory, that contains JSON files with results of "
        "https://www.ozon.ru/api/composer-api.bx/_action/v2/categoryChildV3 "
        "Ozon API call, that contains information about categories. "
        f"Default: {ProjectConfig.categories_data_dir}."
    ),
)
@click.option(
    "--category_id",
    "-c",
    type=str,
    multiple=True,
    default=None,
    help=(
        "Root category ID (file name `<cat_id>.json`) to load "
        "from the directory. All children loads as well. Default: "
        "all files from the directory."
    ),
)
def load_ozon_categories_from_api_results(
    path: str, category_id: tuple[str] | None
) -> None:
    path = Path(path)
    if not Path.exists(path):
        click.echo(f"Error: The specified path '{path}' does not exist.")
        return
    if not Path.is_dir(path):
        click.echo(f"Error: The specified path '{path}' isn't a directory.")
        return

    category_id = set(category_id)

    repo = OzonCategoriesRepository()
    with get_session() as session:
        for filename in os.listdir(path):
            is_json_file = filename.endswith(".json")
            if not category_id:
                is_included = True
            else:
                cat_id = filename[: -len(".json")]
                is_included = cat_id in category_id

            if is_json_file and is_included:
                click.echo(f"Process file: {filename}")
            else:
                continue

            file_path = Path(path / filename)
            try:
                with Path.open(file_path, encoding="utf-8") as file:
                    data = json.load(file)
                    process_category_data(data.get("data"), repo, session)
                    session.commit()
            except json.JSONDecodeError as e:
                click.echo(f"Error decoding JSON in file '{file_path}': {e}")
            except Exception as e:
                click.echo(
                    f"Unexpected error processing file '{file_path}': {e}"
                )
                session.rollback()


def create_meta(cat_id: int, session: Session) -> None:
    meta = (
        session.query(ScraperOzonCategoryMeta)
        .filter(ScraperOzonCategoryMeta.category_id == cat_id)
        .first()
    )
    if meta is None:
        session.add(ScraperOzonCategoryMeta(category_id=cat_id))


def process_category_data(
    data: dict[str, Any],
    repo: OzonCategoriesRepository,
    session: Session,
) -> None:
    if not data:
        click.echo("Error: No 'data' found in JSON.")
        return

    def recursive_parse(
        categories: list[dict[str, Any]],
        parent_id: int | None = None,
        level: int = 1,
    ) -> None:
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
                create_meta(category_props.id, session)

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
    create_meta(root_category.id, session)

    if "columns" in data:
        for column in data["columns"]:
            recursive_parse(
                column.get("categories", []),
                root_category.id,
                level=2,
            )
    else:
        click.echo("Error: No 'columns' found in the data.")
