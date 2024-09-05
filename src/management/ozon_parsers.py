import click

from modules.parser.parsers.ozon.category_pages import OzonCategoriesParser
from modules.parser.parsers.ozon.product_reviews import OzonReviewsStateParser


@click.command(
    "parse_ozon_category_pages",
    help="Parses products from category pages.",
)
def parse_ozon_category_pages():
    parser = OzonCategoriesParser()
    click.echo(f"Parser created: {parser}. Starting parsing...")
    try:
        parser.run()
    except Exception as e:
        click.echo(f"Error while parsing: {e}")
        raise


@click.command(
    "parse_ozon_product_reviews_from_state",
    help=(
        "Parses products reviews from data-state html object "
        "(only first 15 reviews and media)."
    ),
)
def parse_ozon_product_reviews():
    parser = OzonReviewsStateParser()
    click.echo(f"Parser created: {parser}. Starting parsing...")
    try:
        parser.run()
    except Exception as e:
        click.echo(f"Error while parsing: {e}")
        raise
