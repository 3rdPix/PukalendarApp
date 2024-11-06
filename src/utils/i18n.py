"""
# Internacionalización del contenido

Módulo de carga del texto en la interfaz. Basado en el paquete de idiomas
[Babel](https://pypi.org/project/babel/) para la extracción e instalación.
"""
from config import PUCalendarAppPaths as pt
from babel.support import Translations
from config import LOCALE

__all__ = {"_"}

locale_path = pt.Resources.FOLDER_LOCALE
lang = Translations.load(locale_path, locales=[LOCALE])
lang.install()
_ = lang.gettext
"""
# Función identificadora

Cualquier texto dentro de la interfaz debe estar encapsulado por esta
función. El argumento debe ser el identificador del texto, el cual aparecerá
en los archivos de traducción respectivos de los recursos en
`resources/locale/`.

**Ejemplo de uso:**

>>> my_button: QPushButton = QPushButton()
    my_button.setText(_("MainWindow.HomeView.MyButton"))

Esto hará que el identificador "MainWindow.HomeView.MyButton" en los archivos
de traducción esté asociado al texto del botón `my_button`. Es recomendable
y se solicita encarecidamente que los identificadores sean lo más expresivos
y detallados posibles, de modo que cada elemento de la interfaz gráfica se
localize correctamente, sin que haya confusiones respecto al elemento
referenciado.
"""