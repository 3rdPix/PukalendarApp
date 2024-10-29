from .path_handler import PUCalendarAppPaths
from configparser import ConfigParser
import logging
from os.path import exists
from enum import StrEnum


class AppSettings(StrEnum):
    class General(StrEnum):
        LOCALE: str = "locale"
    
    class Window(StrEnum):
        WIDTH: str = "width"
        HEIGHT: str = "height"
        COORD_X: str = "X"
        COORD_Y: str = "Y"




log = logging.getLogger("config")
__configuration_loader = ConfigParser()
if exists(PUCalendarAppPaths.Config.WINDOW_CONF):
    __configuration_loader.read(PUCalendarAppPaths.Config.WINDOW_CONF)
else:
    # Carga valores por defecto
    log.warning("No window.conf file found, loading defaults")
    __configuration_loader["general"] = {
        "locale" : "es"
    }
    __configuration_loader["window"] = {
        "width" : 1024,
        "height" : 768,
        "X": 200,
        "Y": 200
    }

LOCALE = __configuration_loader["general"]["locale"]
WINDOW_WIDTH = __configuration_loader["window"]["width"]
WINDOW_HEIGHT = __configuration_loader["window"]["height"]


def dump_configuration() -> None:
    log.debug(f"Dumping settings into {PUCalendarAppPaths.Config.WINDOW_CONF}")
    with open(PUCalendarAppPaths.Config.WINDOW_CONF, "w") as raw_file:
        __configuration_loader.write(raw_file)


def setWindowWidth(w: int) -> None:
    __configuration_loader["window"]["width"] = w


def setWindowHeight(h: int) -> None:
    __configuration_loader["window"]["height"] = h

def setWindowX(x: int) -> None:
    __configuration_loader["window"]["X"] = x


def setWindowY(y: int) -> None:
    __configuration_loader["window"]["Y"] = y