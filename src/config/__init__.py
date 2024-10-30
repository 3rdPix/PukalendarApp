from .path_handler import PUCalendarAppPaths
import logging
from PyQt6.QtCore import QSettings
from typing import Any
from typing import TypeAlias
from enum import StrEnum


log = logging.getLogger("config")


class ApplicationSettings(QSettings):
    """
    Clase especial para manejar la posibilidad de perder configuraciones
    personalizadas y cargar las configuraciones por defecto en su lugar.
    No se encarga de verificar la integridad del archivo `defaults.conf`:
    hágase de este último un archivo de solo lectura durante la instalación
    para asegurar su integridad.
    """
    class Window(StrEnum):
        RECT: str = "Window/rect"

    class General(StrEnum):
        # IMPORTANTE: solo en este caso no anteponer "General" porque
        # QSettings es estúpido
        LOCALE: str = "locale"
    
    SettingOption: TypeAlias = Window | General

    def __init__(self) -> None:
        super().__init__("Pukalendar", "PukalendarApp")
        self.defaults = QSettings(PUCalendarAppPaths.Config.DEFAULTS,
                                  QSettings.Format.IniFormat)
    
    def value(self, key: SettingOption) -> Any:
        having: Any = super().value(key)
        # Si no se obtuvo valor de las configuraciones personalizadas
        # es necesario cargar el valor por defecto
        if having is not None: return having
        self.setValue(key, self.defaults.value(key))
        return self.defaults.value(key)
    
    def restore_defaults(self) -> None:
        [self.setValue(key, self.defaults.value(
            key)) for key in self.defaults.allKeys()]
        self.sync()

    def setValue(self, key: SettingOption, value: Any) -> None:
        super().setValue(key, value)
        self.sync()


Settings: ApplicationSettings = ApplicationSettings()
# Particularmente obtener locale para dárselo a Babel sin pasar por Qt
LOCALE: str = Settings.value(Settings.General.LOCALE)