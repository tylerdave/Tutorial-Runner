import sys
import click
import pathlib
import pytest

from tutorial_runner.state import State


@click.group()
@click.pass_context
def tutorial(ctx):
    """Click tutorial runner."""
    ctx.ensure_object(dict)
    ctx.obj["state"] = State()


@tutorial.command()
def hint():
    """Get a hint for the current lesson."""
    click.echo("Hints coming soon!")


@tutorial.command()
@click.pass_obj
@click.option(
    "--config",
    type=click.Path(exists=True, dir_okay=False),
    default="tutorial.toml",
    help="Tutorial configuration file.",
)
@click.option(
    "--reinitialize",
    "-r",
    is_flag=True,
    help="Clear progress and reinitialize tutorial.",
)
def init(obj, config, reinitialize):
    """(Re-)Initialize the tutorial"""
    state = obj["state"]
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
@click.option("--part-id", "-p", type=click.INT, help="Specify part ID (defaults to current)")
def lesson(obj, lesson_id, part_id):
    """Switch to a specific lesson"""
    state = obj["state"]
    if part_id is None:
        part_id = state.get_current_part_id()
    state.set_current_lesson(part_id, lesson_id)


@tutorial.command()
@click.pass_obj
def status(obj):
    """Show the status of your progress."""
    state = obj["state"]
    lesson = state.get_current_lesson()
    click.echo("Current lesson\n--------------\n")
    click.echo("Part {:02d}, Lesson {:02d}: {}".format(lesson['part']['id'], lesson['id'], lesson['name']))
    click.echo(" Tutorial base dir: {}".format(lesson['tutorial_dir']))
    click.echo("       Working dir: {}".format(lesson['part']['dir']))
    click.echo("      Working file: {}".format(lesson['part']['file']))
    parts = state.list_parts()
    click.echo("\nAll lessons\n-----------")
    for part in parts:
        click.echo("\n-- Part {id:02d} - {name} --".format(**part))
        for lesson in part['lessons']:
            lesson['_status'] = state.get_lesson_status(part['id'], lesson['id'])
            click.echo("{id:02d} - {name:20} - {_status}".format(**lesson))

def run_lesson(lesson_test_file):
    result = pytest.main(['-vx', 'tutorial/{0}'.format(lesson_test_file)])
    if result == 0:
        return True
    else:
        return False

@tutorial.command()
@click.pass_obj
def check(obj):
    """Check your work for the current lesson."""
    state = obj['state']
    lesson = state.get_current_lesson()
    test_path = str(pathlib.Path(lesson['tutorial_dir'], lesson['part']['dir'], 'tests',lesson['test']))
    print(test_path)
    result = pytest.main(['-vx', test_path])
    if result == 0:
        print("Success!")
    else:
        print("Failed :-(")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
