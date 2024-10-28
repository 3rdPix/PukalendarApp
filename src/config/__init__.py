from .path_handler import PUCalendarAppPaths
from configparser import ConfigParser
import logging
from os.path import exists

__configuration_loader = ConfigParser()
if exists(PUCalendarAppPaths.Config.WINDOW_CONF):
    __configuration_loader.read(PUCalendarAppPaths.Config.WINDOW_CONF)
else:
    # load defaults
    logging.warning("No window.conf file found, loading defaults")
    __configuration_loader["general"] = {
        "locale" : "es"
    }

LOCALE = __configuration_loader["general"]["locale"]