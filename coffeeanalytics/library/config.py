""" Module to initialize Dynaconf Configuration."""

from os import path
from dynaconf import Dynaconf

current_dir = path.dirname(path.abspath(__file__))
project_root = path.abspath(path.join(current_dir, "..", "config"))

settings = Dynaconf(
    environments=True,
    settings_files=[path.join(project_root, "settings.toml")],
)
