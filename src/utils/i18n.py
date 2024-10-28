"""
Internacionalización del contenido
----------------------------------
Este módulo se encarga de instalar y cargar el contenido de locale
y aplicarlo a la interfaz.
"""
from config import PUCalendarAppPaths as pt
from babel.support import Translations
from config import LOCALE

locale_path = pt.Resources.FOLDER_LOCALE
lang = Translations.load(locale_path, locales=[LOCALE])
lang.install()
_ = lang.gettext