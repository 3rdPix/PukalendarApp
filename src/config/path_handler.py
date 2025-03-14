"""
# Rutas

Módulo donde se almacenan y construyen las rutas a los recursos del programa.
"""
from dataclasses import dataclass
from os.path import join
from os.path import abspath
from os.path import dirname

__all__ = {"PUCalendarAppPaths"}

# Start from /
base_directory: str = abspath(join(dirname(__file__), "..", ".."))
def build_path(*args) -> str: return join(base_directory, *args)

class PUCalendarAppPaths:
    """
    Clase principal que contiene catálogo con las rutas a los
    recursos de la aplicación.

    Dentro de esta clase se declaran diferentes `@dataclass` que contienen
    las rutas organizadas según categoría.
    """
    @dataclass
    class Resources:
        """@private"""
        APPLICATION_ICON: str = build_path("resources", "images", "pukalendar_logo.png")
        DIALOG_ABOUT_IMAGE: str = build_path("resources", "images", "campus3.png")
        VIEW_COURSES_NO_BOOK: str = build_path("resources", "images", "no_book.png")
        FOLDER_LOCALE: str = build_path("resources", "locale")
        ICON_CALENDAR_NORMAL: str = build_path("resources", "images", "calendar_normal.png")
        ICON_CALENDAR_SELECTED: str = build_path("resources", "images", "calendar_selected.png")
        ICON_COURSES_NORMAL: str = build_path("resources", "images", "courses_normal.png")
        ICON_COURSES_SELECTED: str = build_path("resources", "images", "courses_selected.png")
        ICON_HOME_NORMAL: str = build_path("resources", "images", "home_normal.png")
        ICON_HOME_SELECTED: str = build_path("resources", "images", "home_selected.png")
        ICON_TODO_NORMAL: str = build_path("resources", "images", "todo_normal.png")
        ICON_TODO_SELECTED: str = build_path("resources", "images", "todo_selected.png")
        IMAGE_EMPTY_BOX: str = build_path("resources", "images", "empty.png")
        ICON_ABOUT_NORMAL: str = build_path("resources", "images", "about_normal.png")
        ICON_ABOUT_SELECTED: str = build_path("resources", "images", "about_selected.png")

    @dataclass
    class Qss:
        """@private"""
        MAIN_WINDOW: str = build_path("resources", "qss", "main_window.qss")
        HOME_VIEW: str = build_path("resources", "qss", "home_view.qss")

    @dataclass
    class Config:
        """@private"""
        DEFAULTS: str = build_path("src", "config", "defaults.ini")
        USER_COURSES: str = build_path("usr", "courses.csv")
        BASE_COURSE_SESSIONS: str = build_path("usr", "")