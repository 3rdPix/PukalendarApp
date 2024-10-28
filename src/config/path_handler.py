"""
Paths
---------
Todas las rutas a los recursos relevantes son entregados desde este módulo
al resto del programa
"""
from dataclasses import dataclass
from os.path import join
from os.path import abspath
from os.path import dirname

# Start from /
base_directory: str = abspath(join(dirname(__file__), "..", ".."))
def build_path(*args) -> str: return join(base_directory, *args)

class PUCalendarAppPaths:
    """
    Clase principal que contiene las rutas a los recursos de interfaz
    """
    @dataclass
    class Resources:
        APPLICATION_ICON: str = build_path("resources", "images", "logo.png")
        DIALOG_ABOUT_IMAGE: str = build_path("resources", "images", "campus3.png")
        VIEW_COURSES_NO_BOOK: str = build_path("resources", "images", "no_book.png")
        FOLDER_LOCALE: str = build_path("resources", "locale")

    @dataclass
    class Qss:
        MAIN_WINDOW: str = build_path("resources", "qss", "main_window.qss")
        HOME_VIEW: str = build_path("resources", "qss", "home_view.qss")

    @dataclass
    class Config:
        WINDOW_CONF: str = build_path("usr", "window.conf")
        USER_COURSES: str = build_path("usr", "courses.pkl")