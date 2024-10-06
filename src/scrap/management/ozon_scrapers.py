import click

from scrap.scrapers.ozon.category_pages import OzonCategoriesScraper
from scrap.scrapers.ozon.product_reviews import OzonReviewsStateScraper


@click.command(
    "scrape_ozon_category_pages",
    help="Scrapes products from category pages.",
)
def scrape_ozon_category_pages():
    scraper = OzonCategoriesScraper()
    click.echo(f"Scraper created: {scraper}. Starting parsing...")
    try:
        scraper.run()
    except Exception as e:
        click.echo(f"Error while parsing: {e}")
        raise


@click.command(
    "scrape_ozon_product_reviews_from_state",
    help=(
        "Scrapes products reviews from data-state html object "
        "(only first 15 reviews and media)."
    ),
)
def scrape_ozon_product_reviews():
    scraper = OzonReviewsStateScraper()
    click.echo(f"Scraper created: {scraper}. Starting parsing...")
    try:
        scraper.run()
    except Exception as e:
        click.echo(f"Error while parsing: {e}")
        raise
