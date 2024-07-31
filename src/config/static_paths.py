"""
Rutas de aplicación
-----------------
Este módulo maneja la carga y creación de las rutas a todos
los archivos que la aplicación necesita. 

Inicialmente, las rutas se encuentran relativas al directorio
principal del proyecto (donde se encuentra `src/`).

La clase principal, `ApplicationPaths` se encarga de transformar
esas rutas relativas a rutas absolutas cargadas de forma dinámica.

Todo el proceso asume que el archivo `paths.json` se encuentra en
el mismo directorio que este módulo.
"""
from enum import Enum
from json import load
from os.path import join
from os.path import abspath
from os.path import dirname

class PathKey(Enum):
    """
    Clase *Enum* que contiene los valores de las llaves referentes a 
    los distintos archivos.
    """
    APPLICATION_ICON: str = 'application_icon'
    QSS_MAIN_WINDOW: str = 'main_win_qss'
    LOCALE_DIR: str = 'locale_dir'

class ApplicationPaths:
    """
    Clase principal que carga las rutas relativas y las transforma en
    rutas absolutas cargadas de forma dinámica. Además, provee un
    método para la lectura de las rutas.
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
        Transforma de ruta relativa a ruta absoluta
        """
        base_dir = abspath(join(dirname(__file__), '..', '..'))
        for key, path in cls._paths_map.items():
            cls._paths_map[key] = abspath(join(base_dir, *path))

    @classmethod
    def get_path(cls, key: PathKey) -> str:
        """
        Obtener la ruta al archivo que la llave refiere
        """
        if key.value not in cls._paths_map:
            raise KeyError(f"[ERROR] Key '{key.value}' not found in paths map.")
        return cls._paths_map.get(key.value)

# Inicializa la carga de rutas cuando el módulo sea cargado
ApplicationPaths._load_paths_from_json(
    join(abspath(dirname(__file__)), "paths.json"))