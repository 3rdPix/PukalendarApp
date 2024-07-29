from typing import List
from PyQt6.QtWidgets import QApplication

from PyQt6.QtWidgets import QWidget

# Importar explícitamente el módulo de rutas para que las cargue
from config import static_paths

class MainApp(QApplication):
    """
    Aplicación de Qt que contiene todas la funcionalidad y conecta
    las señales del programa.
    """
    def __init__(self, argv: List[str]) -> None:
        super().__init__(argv)
        self.my_wdgt = QWidget()
        self.my_wdgt.show()