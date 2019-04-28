import click
import pytoml

from codecs import open
from pathlib import Path

APP_NAME = "Tutorial Runner"

class State:
    def __init__(self):
        self.app_dir = click.get_app_dir(APP_NAME)
        self.state_file_path = Path(self.app_dir, "tutorial-state.toml")

    def save(self, new_state):
        with open(self.state_file_path, mode="w", encoding="utf-8") as statefile:
            pytoml.dump(new_state, statefile)

    def load(self):
        with open(self.state_file_path, mode="r", encoding="utf-8") as statefile:
            return pytoml.load(statefile)

    def initialize(self, config):
        config_data = pytoml.load(config)
        if not Path(self.app_dir).exists():
            Path(self.app_dir).mkdir(parents=True, exist_ok=True)
        default_state = {
            "name": config_data.get('name'),
            "parts": config_data.get('parts'),
            "current": {'part': 1, 'lesson': 1},
            "progress": {},
        }
        self.save(default_state)

    def is_initialized(self):
        try:
            state = self.load()
        except FileNotFoundError:
            return False
        except:
            raise
        if "parts" in state:
            return True
        else:
            return False
    
    def get_lesson_status(self, part, lesson):
        state = self.load()


    def get_current_part(self):
        state = self.load()
        return state.get('current', {}).get('part')

    def get_current_lesson(self):
        state = self.load()
        return state.get('current', {}).get('part')

    
