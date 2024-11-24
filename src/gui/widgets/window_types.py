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
import logging


class CardsWindow(QWidget):
    """
    # Ventana de navegación
    
    Ofrece un objeto central que sirve de contenedor para los elementos tipo
    *widget* que se deseen agregar, los cuales se navegan a través de las
    opciones presentes en un panel personalizable. 
    """
    def __init__(self, parent: QWidget|None=None,
                 flags: Qt.WindowType=Qt.WindowType.Window) -> None:
        super().__init__(parent, flags)
        self.setMinimumSize(150, 150)
        self.setLayout(QVBoxLayout(self))
        self._central_layout: QStackedLayout = QStackedLayout(self.layout())


if __name__ == "__main__":
    # exposition
    from PyQt6.QtWidgets import QApplication
    app = QApplication([])
    widget0 = CardsWindow()
    widget0.make_it_obvious()
    widget0.show()
    exit(app.exec())