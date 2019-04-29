import sys
import click
import pathlib
import pkg_resources
import pytest
import shutil

from datetime import datetime

from tutorial_runner.state import State


@click.group(name='tutorial-runner')
@click.pass_context
def tutorial(ctx):
    """Click tutorial runner."""
    ctx.ensure_object(dict)
    ctx.obj["state"] = State()

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
@click.option(
    "--lesson-id", "-l", type=click.INT, help="Specify lesson ID (defaults to current)"
)
@click.option(
    "--part-id", "-p", type=click.INT, help="Specify part ID (defaults to current)"
)
def lesson(obj, lesson_id, part_id):
    """Switch to a specific lesson"""
    state = obj["state"]
    if part_id is None:
        part_id = state.get_current_part_id()
    if lesson_id is None:
        lesson_id = state.get_current_lesson_id()
    state.set_current_lesson(part_id, lesson_id)
    lesson = state.get_current_lesson()
    working_path = pathlib.Path(
        lesson["tutorial_dir"], lesson["part"]["dir"], lesson["part"]["file"]
    )

    click.echo("Currently working on Part {:02d}, Lesson {:02d} - {}".format(part_id, lesson_id, lesson['name']))
    click.echo("\nWorking file: {}".format(working_path))
    if lesson.get("doc-urls"):
        click.echo("Related docs: {}".format(lesson.get('doc-urls')))
    if lesson.get("objectives"):
        click.echo("\nObjectives:\n{}".format(lesson.get('objectives')))


@tutorial.command()
@click.pass_obj
def status(obj):
    """Show the status of your progress."""
    state = obj["state"]
    lesson = state.get_current_lesson()
    click.echo("Current lesson\n--------------\n")
    click.echo(
        "Part {:02d}, Lesson {:02d}: {}".format(
            lesson["part"]["id"], lesson["id"], lesson["name"]
        )
    )
    click.echo(" Tutorial base dir: {}".format(lesson["tutorial_dir"]))
    click.echo("       Working dir: {}".format(lesson["part"]["dir"]))
    click.echo("      Working file: {}".format(lesson["part"]["file"]))
    parts = state.list_parts()
    click.echo("\nAll lessons\n-----------")
    for part in parts:
        click.echo("\n-- Part {id:02d} - {name} --".format(**part))
        for lesson in part["lessons"]:
            lesson["_status"] = state.get_lesson_status(part["id"], lesson["id"])
            click.echo("{id:02d} - {name:20} - {_status}".format(**lesson))


def run_lesson(lesson_test_file):
    result = pytest.main(["-vx", "{0}".format(lesson_test_file)])
    if result == 0:
        return True
    else:
        return False


@tutorial.command()
@click.pass_obj
@click.pass_context
def check(ctx, obj):
    """Check your work for the current lesson."""
    state = obj["state"]
    current_lesson = state.get_current_lesson()
    test_path = str(
        pathlib.Path(
            current_lesson["tutorial_dir"],
            current_lesson["part"]["dir"],
            "tests",
            current_lesson["test"],
        )
    )
    result = run_lesson(test_path)
    if result:
        click.secho("All tests passed! ✨🐍✨", fg="green")
        next_lesson = state.complete_lesson(
            current_lesson["part"]["id"], current_lesson["id"]
        )
        if next_lesson is not None:
            click.echo("Ready to proceed to Part {}, Lesson {}!".format(*next_lesson))
            click.echo("Continue by running `tutorial lesson`")
        else:
            click.echo("Last lesson complete! 🎉")
    else:
        click.secho("Some tests failed. 🤔", fg="red")
        click.echo(
            "Review the lesson instructions and the test output above and try again!"
        )


@tutorial.command()
@click.pass_obj
def peek(obj):
    """Look at the solution file without overwriting your work."""
    state = obj["state"]
    lesson = state.get_current_lesson()
    solution_path = str(
        pathlib.Path(
            lesson["tutorial_dir"],
            lesson["part"]["dir"],
            "solutions",
            lesson["solution"],
        )
    )
    with open(solution_path) as solutionfile:
        solution_source = solutionfile.read()
    click.echo("Solution in {}:\n --------------------".format(solution_path))
    click.echo(solution_source)
    click.echo(" --------------------\n")


@tutorial.command()
@click.pass_obj
@click.option('--yes', '-y', is_flag=True)
def solve(obj, yes):
    """Copy the solution file to the working file."""
    state = obj["state"]
    lesson = state.get_current_lesson()
    solution_path = pathlib.Path(
        lesson["tutorial_dir"], lesson["part"]["dir"], "solutions", lesson["solution"]
    )
    working_path = pathlib.Path(
        lesson["tutorial_dir"], lesson["part"]["dir"], lesson["part"]["file"]
    )
    backup_filename = lesson["part"]["file"].replace(
        ".py", ".{}.py".format(datetime.now().strftime("%Y-%m-%d.%H-%M-%S"))
    )
    backup_path = pathlib.Path(
        lesson["tutorial_dir"], lesson["part"]["dir"], backup_filename
    )
    click.echo(
        "This will make a backup of the working file and then copy the solution file into place."
    )
    click.echo("  Working file: {}".format(working_path))
    click.echo("   Backup file: {}".format(backup_path))
    click.echo(" Solution file: {}".format(solution_path))
    if not yes:
        click.confirm("Do you wish to proceed?", abort=True)
    click.echo("Making backup file: {}".format(backup_path))
    shutil.copy(str(working_path), str(backup_path))
    click.echo("Copying solution into place...")
    shutil.copy(str(solution_path), str(working_path))
    click.echo("You may now complete the lesson by running `tutorial check`.")

@tutorial.command()
def version():
    """Display the version of this command."""
    click.echo("Tutorial-Runner {}".format(pkg_resources.get_distribution("tutorial-runner").version))


if __name__ == "__main__":
    sys.exit(tutorial())