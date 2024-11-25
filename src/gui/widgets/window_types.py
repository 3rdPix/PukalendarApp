from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QStackedLayout
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QEventLoop
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QWidget
from misc import SlidingStackedWidget
from misc import LineSeparator
from enum import Enum
import logging


class OrientationMode(Enum):
    HORIZONTAL: int = 0
    VERTICAL: int = 1

class CardsWindow(QWidget):
    """
    # Ventana de navegación
    
    Ofrece un objeto central que sirve de contenedor para los elementos tipo
    *widget* que se deseen agregar, los cuales se navegan a través de las
    opciones presentes en un panel personalizable. 
    """

    class NavigationBar(QWidget):
        """
        Área visual que contiene los botones para navegar entre los elementos
        de la ventana
        """
        def __init__(self, parent: QWidget|None=None,
                     flags: Qt.WindowType=Qt.WindowType.Widget,
                     mode: OrientationMode=OrientationMode.VERTICAL) -> None:
            super().__init__(parent, flags)
            self._items: list[] = list()


    def __init__(self, parent: QWidget|None=None,
                 flags: Qt.WindowType=Qt.WindowType.Window) -> None:
        super().__init__(parent, flags)
        self.setMinimumSize(150, 150)
        self.setLayout(QVBoxLayout(self))
        self._central_layout: SlidingStackedWidget = SlidingStackedWidget(self)
        self.layout().addWidget(self._central_layout)
        self.layout().addWidget(LineSeparator())


if __name__ == "__main__":
    # exposition
    from PyQt6.QtWidgets import QApplication
    app = QApplication([])
    widget0 = CardsWindow()
    widget0.show()
    exit(app.exec())