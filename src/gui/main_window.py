from qfluentwidgets import MSFluentWindow
from config.static_paths import ApplicationPaths
from config.static_paths import PathKey
from PyQt6.QtGui import QIcon
from utils.i18n import _
from config.text_keys import TextKey

class MainWindow(MSFluentWindow):
    """
    Clase de la ventana principal de la aplicación sobre la
    que se despliegan todas las vistas y sub-widgets
    """


    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._init_self()
    
    def _init_self(self) -> None:
        """
        Carga los contenidos propios de la ventana principal
        """
        self.setWindowIcon(QIcon(ApplicationPaths.get_path(
            PathKey.APPLICATION_ICON)))
        try:
            with open(ApplicationPaths.get_path(PathKey.QSS_MAIN_WINDOW),
                       'r', encoding='utf-8') as raw_file:
                self.setStyleSheet(raw_file.read())
        except FileNotFoundError:
            print(f'[ERROR] loading {ApplicationPaths.get_path(PathKey.QSS_MAIN_WINDOW)}')
        self.setWindowTitle(_(TextKey.WINDOW_TITLE))