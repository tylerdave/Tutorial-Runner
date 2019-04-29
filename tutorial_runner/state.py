import click
import pytoml

from codecs import open
from pathlib import Path

APP_NAME = "Tutorial Runner"


class State:
    def __init__(self):
        self.app_dir = click.get_app_dir(APP_NAME)
        self.state_file_path = str(Path(self.app_dir, "tutorial-state.toml"))

    def save(self, new_state):
        with open(self.state_file_path, mode="w", encoding="utf-8") as statefile:
            pytoml.dump(new_state, statefile)

    def load(self):
        try:
            with open(self.state_file_path, mode="r", encoding="utf-8") as statefile:
                return pytoml.load(statefile)
        except FileNotFoundError as e:
            raise click.ClickException(
                "Tutorial status file not found. You probably need to run `tutorial init`. \nDetails: {}".format(
                    e
                )
            )

    def initialize(self, config_filename):
        with open(config_filename) as configfile:
            config_data = pytoml.load(configfile)
        tutorial_dir = str(Path(config_filename).resolve().parent)
        if not Path(self.app_dir).exists():
            Path(self.app_dir).mkdir(parents=True, exist_ok=True)
        default_state = {
            "name": config_data.get("name"),
            "parts": config_data.get("parts"),
            "tutorial_dir": tutorial_dir,
            "current": {"part": 1, "lesson": 1},
            "progress": {"1.1": "in-progress"},
        }
        self.save(default_state)

    def is_initialized(self):
        try:
            state = self.load()
        except click.ClickException:
            return False
        except:
            raise
        if "parts" in state:
            return True
        else:
            return False

    def get_lesson_status(self, part, lesson):
        progress_key = "{}.{}".format(part, lesson)
        state = self.load()
        return state["progress"].get(progress_key, "incomplete")

    def set_lesson_status(self, part_id, lesson_id, status):
        progress_key = "{}.{}".format(part_id, lesson_id)
        state = self.load()
        state["progress"][progress_key] = status
        self.save(state)

    def get_next_lesson_id(self, part_id, lesson_id):
        state = self.load()
        part = [p for p in state["parts"] if p["id"] == part_id][0]
        try:
            lesson = [l for l in part["lessons"] if l["id"] == lesson_id + 1][0]
            return (part["id"], lesson["id"])
        except IndexError:
            try:
                part = [p for p in state["parts"] if p["id"] == part_id + 1][0]
                return (part["id"], 1)
            except IndexError:
                return None, None

    def complete_lesson(self, part_id, lesson_id):
        self.set_lesson_status(part_id, lesson_id, "complete")
        next_part_id, next_lesson_id = self.get_next_lesson_id(part_id, lesson_id)
        if next_lesson_id is not None:
            self.set_current_lesson(next_part_id, next_lesson_id)
            return next_part_id, next_lesson_id
        else:
            return None

    def get_current_part_id(self):
        state = self.load()
        return state.get("current", {}).get("part")

    def get_current_lesson_id(self):
        state = self.load()
        return state.get("current", {}).get("lesson")

    def get_current_lesson(self):
        part_id = self.get_current_part_id()
        lesson_id = self.get_current_lesson_id()
        state = self.load()
        part = [p for p in state["parts"] if p["id"] == part_id][0]
        lesson = [l for l in part["lessons"] if l["id"] == lesson_id][0]
        lesson["part"] = part
        lesson["tutorial_dir"] = state["tutorial_dir"]
        return lesson

    def set_current_lesson(self, part_id, lesson_id):
        state = self.load()
        try:
            part = [p for p in state["parts"] if p["id"] == part_id][0]
        except IndexError:
            raise click.ClickException(
                "{} is not a valid part ID. See `tutorial status` for a list of parts and lessons.".format(
                    part_id
                )
            )
        try:
            lesson = [l for l in part["lessons"] if l["id"] == lesson_id][0]
        except IndexError:
            raise click.ClickException(
                "{} is not a valid lesson ID for part {:02d}. See `tutorial status` for a list of parts and lessons.".format(
                    lesson_id, part_id
                )
            )
        state["current"] = {"part": part_id, "lesson": lesson_id}
        self.save(state)
        self.set_lesson_status(part_id, lesson_id, "in-progress")

    def list_parts(self):
        state = self.load()
        return state["parts"]
