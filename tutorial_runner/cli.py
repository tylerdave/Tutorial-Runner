# -*- coding: utf-8 -*-

"""Console script for tutorial_runner."""
import sys
import click


@click.command()
def tutorial(args=None):
    """Console script for tutorial_runner."""
    click.echo("Replace this message by putting your code into "
               "tutorial_runner.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    sys.exit(tutorial())  # pragma: no cover
