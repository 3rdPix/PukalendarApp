"""
ApplicationPaths
-----------------
This module handles the loading and creation of relative paths
to different files needed in the app.

All of the paths are initially loaded relative to the project 
directory where `src/` is located. The main class in this module
transforms those relative paths into absolute paths once the 
project is located.

The process assumes there exists the `paths.json` file in the
same directory as this module
"""
from enum import Enum
from json import load
from os.path import join
from os.path import abspath
from os.path import dirname

class PathKey(Enum):
    """
    Enum class containing the key-value names for the different files.
    """
    APPLICATION_ICON: str = 'application_icon'

class ApplicationPaths:
    """
    Main class that loads the relative paths and transforms them into
    absolute paths.
    """
    _paths_map: dict = {}

    @classmethod
    def _load_paths_from_json(cls, json_file: str) -> None:
        with open(json_file, 'r', encoding='utf-8') as raw_file:
            cls._paths_map = load(raw_file)
        cls._normalize_paths()

    @classmethod
    def _normalize_paths(cls):
        """
        Normalize all paths to ensure they are absolute paths.
        """
        base_dir = abspath(join(dirname(__file__), '..', '..'))
        for key, path in cls._paths_map.items():
            cls._paths_map[key] = abspath(join(base_dir, *path))

    @classmethod
    def get_path(cls, key: PathKey) -> str:
        """
        Get the normalized path for the given key.
        """
        if key.value not in cls._paths_map:
            raise KeyError(f"Key '{key.value}' not found in paths map.")
        return cls._paths_map.get(key.value)

# Initialize the paths map on module load
ApplicationPaths._load_paths_from_json(
    join(abspath(dirname(__file__)), "paths.json"))