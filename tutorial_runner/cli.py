import sys
import click

from tutorial_runner.state import State


@click.group()
@click.pass_context
def tutorial(ctx):
    """Click tutorial runner."""
    ctx.ensure_object(dict)
    ctx.obj['state'] = State()

@tutorial.command()
def hint():
    """Get a hint for the current lesson."""
    click.echo("Hints coming soon!")


@tutorial.command()
@click.pass_obj
@click.option("--config", type=click.File(), default='tutorial.toml', help="Tutorial configuration file.")
@click.option(
    "--reinitialize",
    "-r",
    is_flag=True,
    help="Clear progress and reinitialize tutorial.",
)
def init(obj, config, reinitialize):
    """(Re-)Initialize the tutorial"""
    state = obj['state']
    if state.is_initialized() and reinitialize is not True:
        click.confirm(
            "Already initialized. Do you want to clear progress and start over?",
            abort=True,
        )
    state.initialize(config)
    click.echo("Tutorial initialized! Time to start your first lesson!")


@tutorial.command()
@click.pass_obj
@click.argument("lesson-id", type=click.INT)
@click.option("--part", "-p")
def lesson(obj, lesson_id, part):
    """Set the current lesson ID"""
    state = obj['state']
    if part is None:
        part = state.get_current_part()
    

@tutorial.command()
@click.pass_obj
def status(obj):
    """Show the status of your progress."""
    state = obj['state']
    click.echo("OK")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
