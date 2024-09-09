import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import click
import requests

from repositories.ozon.review_media import OzonReviewMediaRepo


def download_file(filename: str, url: str, out_path_: str) -> None:
    """Downloads a file from a URL to a specified dir."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        content = response.content
        filepath = os.path.join(out_path_, filename)
        with open(filepath, 'wb') as file:
            file.write(content)
        click.echo(f"Downloaded {filename} to {out_path_}")
    except requests.exceptions.RequestException as e:
        click.echo(f"Failed to download {url}. Error: {e}")


@click.command(
    "export_media",
    help="Export review media to a dir in format `<file_id>.<ext>`.",
)
@click.option(
    "--out-path",
    type=str,
    required=True,
    help="Output directory path.",
)
@click.option(
    "--media-type",
    type=click.Choice(["video", "image"]),
    required=True,
    help="Media type to export.",
)
@click.option(
    "--comment-count-ge",
    type=int,
    default=0,
    help="Review media comment count greather than X. Default: 0."
)
@click.option(
    "--like-count-ge",
    type=int,
    default=0,
    help="Review media like count greather than X. Default: 0."
)
@click.option(
    "--max-files",
    type=int,
    default=1_000,
    help="Max files to download. Default: 1000."
)
def export_media(
        out_path: str,
        media_type: str,
        comment_count_ge: int,
        like_count_ge: int,
        max_files: int,
):
    if not os.path.exists(out_path):
        click.echo(f"Error: The specified path '{out_path}' does not exist.")
        return
    if not os.path.isdir(out_path):
        click.echo(
            f"Error: The specified path '{out_path}' isn't a directory."
        )
        return

    repo = OzonReviewMediaRepo()
    media = repo.get_to_export(
        media_type,
        comment_count_ge,
        like_count_ge,
        max_files,
    )

    click.echo(f"Download {len(media)} medias")
    with ThreadPoolExecutor(max_workers=25) as executor:
        futures = [
            executor.submit(
                download_file,
                f"{media.id}.{media.extension}",
                media.url,
                out_path,
            )
            for media in media
        ]

    [_ for _ in as_completed(futures)]
    click.echo(f"All downloaded: {len(media)}")
