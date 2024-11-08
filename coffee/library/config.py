from os import path
from dynaconf import Dynaconf

current_dir = path.dirname(path.abspath(__file__))
project_root = path.abspath(path.join(current_dir, "..", "config"))

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[
        path.join(project_root, "settings.toml"),
        path.join(project_root, ".secrets.toml"),
    ],
)
