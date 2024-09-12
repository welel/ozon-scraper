import click


@click.command(
    "post_content",
    help="Post available content to a telegram channel.",
)
def post_content():
    click.echo("Post content :)")
