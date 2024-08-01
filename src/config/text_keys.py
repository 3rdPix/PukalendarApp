"""
Llaves de texto
---------------
El contenido de texto es manejado a través de la internacionalización
*i18n* y el cuerpo se encuentra en los recursos de la aplicación.

Este módulo ofrece la clase principal que contiene las llaves de
referencia a los diferentes textos.
"""
from enum import Enum


class TextKey(Enum):
    """
    Clase *Enum* que contiene los valores de las llaves de referencia
    a las cadenas de texto especificadas en los archivos locale.
    """
    HOME_LABEL: str = 'home_ico_txt'
    COURSES_LABEL: str = 'courses_ico_txt'
    CALENDAR_LABEL: str = 'calendar_ico_txt'
    AGENDA_LABEL: str = 'agenda_ico_txt'
    ABOUT_DESCRIPTION: str = 'abt_description'
    WINDOW_TITLE: str = 'win_title'
    ABOUT_LABEL: str = 'abt_title'