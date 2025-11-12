import typing
from .path_handler import PUCalendarAppPaths
import logging
from PyQt6.QtCore import QSettings
from typing import Any
from pathlib import Path


log = logging.getLogger("config")


class ApplicationSettings(QSettings):
    """
    Clase especial para manejar la posibilidad de perder configuraciones
    personalizadas y cargar las configuraciones por defecto en su lugar.
    No se encarga de verificar la integridad del archivo `defaults.conf`:
    hágase de este último un archivo de solo lectura durante la instalación
    para asegurar su integridad.
    """
    class Window:
        RECT: str = "Window/rect"

    class General:
        # IMPORTANTE: solo en este caso no anteponer "General" porque
        # QSettings es estúpido
        LOCALE: str = "locale"
        CONFIG_DIRECTORY = "config_directory"
        DATABASE_NAME = "db_name"
    
    def __init__(self) -> None:
        super().__init__("Pukalendar", "PukalendarApp")
        self.defaults = QSettings(PUCalendarAppPaths.Config.DEFAULTS,
                                  QSettings.Format.IniFormat)
    def value(self, key: str,
              defaultValue: typing.Any = ...,
              type: type = str
              ) -> typing.Any:
        having: Any = super().value(key)
        # Si no se obtuvo valor de las configuraciones personalizadas
        # es necesario cargar el valor por defecto
        if having is not None: return having
        elif key == self.General.CONFIG_DIRECTORY: return None
        self.setValue(key, self.defaults.value(key))
        return self.defaults.value(key)
    
    def restore_defaults(self) -> None:
        [self.setValue(key, self.defaults.value(
            key)) for key in self.defaults.allKeys()]
        self.sync()

    def setValue(self, key: str, value: Any) -> None:
        super().setValue(key, value)
        self.sync()


Settings: ApplicationSettings = ApplicationSettings()
# Particularmente obtener locale para dárselo a Babel sin pasar por Qt
LOCALE: str = Settings.value(Settings.General.LOCALE)
PUCalendarAppPaths.Config.USER_DIRECTORY = str(Path(Settings.fileName()).parent)
PUCalendarAppPaths.Config.DATABASE = str(
    Path(Settings.fileName()).parent
    / Settings.value(Settings.General.DATABASE_NAME))