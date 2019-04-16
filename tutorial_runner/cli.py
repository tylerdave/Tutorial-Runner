import sys
import click

from tutorial_runner import state


@click.group()
def tutorial(args=None):
    """Click tutorial runner."""


@tutorial.command()
def hint():
    """Get a hint for the current lesson."""
    click.echo("Hints coming soon!")


@tutorial.command()
@click.option(
    "--reinitialize",
    "-r",
    is_flag=True,
    help="Clear progress and reinitialize tutorial.",
)
def init(reinitialize):
    """(Re-)Initialize the tutorial"""
    if state.is_initialized() and reinitialize is not True:
        click.confirm(
            "Already initialized. Do you want to clear progress and start over?",
            abort=True,
        )
    state.initialize()
    click.echo("Tutorial initialized! Time to start your first lesson!")


@tutorial.command()
def status():
    """Show the status of your progress."""
    click.echo("OK")


@tutorial.command()
def verify():
    """Verify that your environment is set up correctly."""
    raise NotImplementedError()

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
