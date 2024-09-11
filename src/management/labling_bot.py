import asyncio
import click

from modules.labling_bot.bot import start


@click.command(
    "start_labling_bot",
    help="Start media review labling bot.",
)
def start_labling_bot():
    try:
        asyncio.run(start())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
