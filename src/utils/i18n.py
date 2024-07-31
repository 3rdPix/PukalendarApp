"""
Internacionalización del contenido
----------------------------------
Este módulo se encarga de instalar y cargar el contenido de locale
y aplicarlo a la interfaz.
"""
# import gettext
# import locale
# from config.static_paths import ApplicationPaths
# from config.static_paths import PathKey


# class I18n:
    # """
    # Clase objeto para la carga de los textos
    # """

    # def __init__(self, locale_path: str, domain: str) -> None:
        # locale.setlocale(locale.LC_ALL, '')
        # gettext.bindtextdomain(domain, locale_path)
        # gettext.textdomain(domain)
        # self.lang = gettext.translation(domain, localedir=locale_path, fallback=True)
        # self.lang.install()
        # self._ = self.lang.gettext

# # Dominio parece ser arbitrario
# i18n = I18n(ApplicationPaths.get_path(PathKey.LOCALE_DIR), 'PUCalendarApp')
# _ = i18n._

from config.static_paths import ApplicationPaths
from config.static_paths import PathKey
from config.text_keys import TextKey
from json import load
from os.path import join

class I18n:
    """
    Esta clase está implementada temporalmente debido a dificultades para
    utilizar `xgettext`
    """
    _language: dict = {}

    @classmethod
    def install_lang(cls, locale_path: str, lang: str='es') -> None:
        specific_lanuage_path = join(locale_path, lang + '.json')
        try:
            with open(specific_lanuage_path, 'r', encoding='utf-8') as raw_file:
                cls._language = load(raw_file)
        except FileNotFoundError:
            print(f'[ERROR] Couldn\'t load language... text might be missing')

    @classmethod
    def get_text(cls, text_key: TextKey) -> str:
        return cls._language.get(text_key.value) \
            if cls._language.get(text_key.value) \
            else '404'
    
# Carga el lenguaje en la importación
# De momento predeterminamos español
I18n.install_lang(ApplicationPaths.get_path(PathKey.LOCALE_DIR))
_ = I18n.get_text