from typing import List
from PyQt6.QtWidgets import QApplication

from PyQt6.QtWidgets import QWidget

# explicitely import paths to load file's directory
from config import static_paths

class MainApp(QApplication):
    """
    PyQt6' application class that holds the modules and connects
    all the signals.
    """
    def __init__(self, argv: List[str]) -> None:
        super().__init__(argv)
        self.my_wdgt = QWidget()
        self.my_wdgt.show()