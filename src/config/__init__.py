from .path_handler import PUCalendarAppPaths
from configparser import ConfigParser
import logging
from os.path import exists


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

LOCALE = __configuration_loader["general"]["locale"]