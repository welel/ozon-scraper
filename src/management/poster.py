import asyncio

import click

from modules.poster import init_scheudler


@click.command(
    "start_poster",
    help="Starts scheduler with post jobs from db.",
)
def start_poster():
    click.echo("Starting poster...")
    scheduler = init_scheudler()
    try:
        scheduler.start()
        for job in scheduler.get_jobs():
            click.echo(
                f"name: {job.name}, trigger: {job.trigger}, "
                f"next run: {job.next_run_time}, handler: {job.func}"
            )
        asyncio.get_event_loop().run_forever()
    except Exception as e:
        scheduler.shutdown()
        click.echo(f"Error while poster run jobs: {e}")
        raise
