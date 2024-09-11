import asyncio
import click

from modules.moderation_bot.bot import start


@click.command("start_moderation_bot", help="Start moderation bot.")
def start_moderation_bot():
    try:
        asyncio.run(start())
    except (KeyboardInterrupt, SystemExit):
        click.echo("Moderation bot stopped.")
