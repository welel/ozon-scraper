import json
import os

import click
from pydantic import BaseModel, RootModel, ValidationError

from database import get_session
from database.models.labling import OzonReviewMediaLabel


class LabelSchema(BaseModel):
    image: str
    choice: str | None = None


class LabelListSchema(RootModel):
    root: list[LabelSchema]


@click.command(
    "import_label_studio_labels",
    help="Import image labels from JSON-MINI Label Studio export JSON file.",
)
@click.option(
    "--file-path",
    type=str,
    required=True,
    help="Path to the JSON-MINI file.",
)
def import_label_studio_labels(file_path: str):
    if not os.path.exists(file_path):
        click.echo(f"Error: The specified path '{file_path}' does not exist.")
        return
    if not os.path.isfile(file_path):
        click.echo(
            f"Error: The specified path '{file_path}' isn't a file."
        )
        return

    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
    except json.decoder.JSONDecodeError:
        click.echo("Invalid json file content", err=True)
        return

    try:
        labels = LabelListSchema(data).root
    except ValidationError as e:
        click.echo(f"Invalid file content: {e.json()}", err=True)
        return

    db_labels = []
    review_media_ids = []
    for label in labels:
        try:
            media_id = label.image.split("/")[-1].split(".")[0].split("-")[-1]
            choice = int(label.choice)
            db_labels.append(
                OzonReviewMediaLabel(review_media_id=media_id, label=choice)
            )
            review_media_ids.append(media_id)
        except Exception as e:
            click.echo(f"Failed to save label: {label}. Error: {e}")

    with get_session() as session:

        query = session.query(OzonReviewMediaLabel).filter(
            OzonReviewMediaLabel.review_media_id.in_(review_media_ids),
        ).all()
        existing_labels = {el.review_media_id: el for el in query}

        for label in db_labels:
            if existing_label := existing_labels.get(label.review_media_id):
                existing_label.label = label.label
            else:
                session.add(label)
        session.commit()
    click.echo(f"All imported: {len(labels)}")
