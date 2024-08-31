import click

from parsers.ozon.category_pages import OzonCategoriesParser


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
