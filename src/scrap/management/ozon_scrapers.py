import click

from scrap.scrapers.ozon.category_pages import OzonCategoriesScraper
from scrap.scrapers.ozon.product_reviews import OzonReviewsStateScraper


@click.command(
    "parse_ozon_category_pages",
    help="Parses products from category pages.",
)
def scrape_ozon_category_pages():
    parser = OzonCategoriesScraper()
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
def scrape_ozon_product_reviews():
    parser = OzonReviewsStateScraper()
    click.echo(f"Parser created: {parser}. Starting parsing...")
    try:
        parser.run()
    except Exception as e:
        click.echo(f"Error while parsing: {e}")
        raise
