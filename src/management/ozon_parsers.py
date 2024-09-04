import click

from modules.parser.parsers.ozon.category_pages import OzonCategoriesParser
# from parsers.ozon.product_reviews import OzonReviewsParser


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


# @click.command(
#     "parse_ozon_product_reviews",
#     help="Parses products reviews.",
# )
# def parse_ozon_product_reviews():
#     parser = OzonReviewsParser()
#     click.echo(f"Parser created: {parser}. Starting parsing...")
#     try:
#         parser.run()
#     except Exception as e:
#         click.echo(f"Error while parsing: {e}")
#         raise
