import asyncio
import click

from modules.moderation_bot.services.post import PostService


@click.command(
    "post_content",
    help="Post available content to a telegram channel.",
)
def post_content():
    click.echo("Sending post...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(PostService().send_post())
    loop.close()
