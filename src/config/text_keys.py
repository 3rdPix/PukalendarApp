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
    INFOBOX_AGENDA_TITLE: str = 'infobox_agenda'
    INFOBOX_COURSES_TITLE: str = 'infobox_courses'
    INFOBOX_SETTINGS_TITLE: str = 'infobox_settings'
    INFOBOX_DANGERS_TITLE: str = 'infobox_dangers'
    INFOBOX_EXTERNAL_TITLE: str = 'infobox_external'
    INFOBOX_TIME_TITLE: str = 'infobox_time'
    COMMAND_BAR_ADD_NEW: str = 'cb_add'
    COMMAND_BAR_DEL: str = 'cb_del'
    COMMAND_BAR_SCALE: str = 'cb_scale'
    COMMAND_BAR_EDIT: str = 'cb_edit'
    NO_CLASS_CREATED_LABEL: str = 'no_class'
    PROFESSOR_LABEL: str = 'prof'
    PROFESSOR_MAIL_LABEL: str = 'prof_mail'
    SECTION_LABEL: str = 'section'
    CURRENT_GRADE_LABEL: str = 'curr_grade'
    CLASS_CODE_LABEL: str = 'class_code'
    NEW_CLASS_DIALOG_SEARCH_LABEL: str = "new_class_search_label"
    NEW_CLASS_DIALOG_SEARCH_PLACEHOLDER: str = "new_class_search_placeholder"
    NEW_CLASS_DIALOG_ALIAS_LABEL: str = "new_class_alias_label"
    NEW_CLASS_DIALOG_ALIAS_PLACEHOLDER: str = "new_class_alias_placeholder"
    NEW_CLASS_DIALOG_COLOR_LABEL: str = "new_class_color_label"
    NEW_CLASS_DIALOG_COLOR_SELECTOR_TITLE: str = "new_class_color_title"
    NEW_CLASS_DIALOG_CONFIRM_BUTTON: str = "new_class_confirm"
    NEW_CLASS_DIALOG_CANCEL_BUTTON: str = "new_class_cancel"