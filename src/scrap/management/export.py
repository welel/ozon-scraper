from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import click
import requests

from scrap.repositories.ozon.review_media import OzonReviewMediaRepository


def download_file(filename: str, url: str, out_path_: str) -> None:
    """Downloads a file from a URL to a specified dir."""
    timeout = 10
    try:
        response = requests.get(url, timeout=timeout, stream=True)
        response.raise_for_status()
        content = response.content
        filepath = Path(out_path_ / filename)
        with Path.open(filepath, "wb") as file:
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
    help="Review media comment count greather than X. Default: 0.",
)
@click.option(
    "--like-count-ge",
    type=int,
    default=0,
    help="Review media like count greather than X. Default: 0.",
)
@click.option(
    "--max-files",
    type=int,
    default=1_000,
    help="Max files to download. Default: 1000.",
)
@click.option(
    "--dir-batch",
    type=int,
    default=None,
    help=(
        "Split files by directories, `dir-batch` files in each directory. "
        "Default: None - all files."
    ),
)
def export_media(
    out_path: str,
    media_type: str,
    comment_count_ge: int,
    like_count_ge: int,
    max_files: int,
    dir_batch: int | None,
) -> None:
    out_path = Path(out_path)
    if not Path.exists(out_path):
        click.echo(f"Error: The specified path '{out_path}' does not exist.")
        return
    if not Path.is_dir(out_path):
        click.echo(
            f"Error: The specified path '{out_path}' isn't a directory."
        )
        return

    repo = OzonReviewMediaRepository()
    media_list = repo.get_to_export(
        media_type,
        comment_count_ge,
        like_count_ge,
        max_files,
    )

    click.echo(f"Download {len(media_list)} medias")

    with ThreadPoolExecutor(max_workers=25) as executor:
        futures = []

        current_dir = out_path

        if dir_batch is not None:
            current_dir = Path(out_path / "1")
            Path.mkdir(current_dir)

        for i, media in enumerate(media_list, start=1):
            futures.append(
                executor.submit(
                    download_file,
                    f"{media.id}.{media.extension}",
                    media.url,
                    current_dir,
                )
            )

            if i % dir_batch == 0:
                current_dir_num = int(current_dir.parts[-1])
                current_dir = Path(out_path / str(current_dir_num + 1))
                Path.mkdir(current_dir)

    list(as_completed(futures))
    click.echo(f"All downloaded: {len(media_list)}")
