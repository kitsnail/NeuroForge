import click
from core.parser import Parser
from core.registry import PluginRegistry
from core.scheduler import Scheduler
from core.pipeline import Pipeline

@click.group()
def cli():
    pass


@cli.command()
@click.argument("markdown_path")
def run(markdown_path):
    PluginRegistry.load_plugins()

    parser = Parser()
    meta, scenes = parser.parse(markdown_path)

    scheduler = Scheduler(PluginRegistry)
    pipeline = Pipeline(scheduler)
    pipeline.run(meta, scenes)


if __name__ == "__main__":
    cli()
