from typing import List
from PyQt6.QtWidgets import QApplication

# Importar explícitamente el módulo de rutas para que las cargue
from config import static_paths

from gui.main_window import MainWindow

class MainApp(QApplication):
    """
    Aplicación de Qt que contiene todas la funcionalidad y conecta
    las señales del programa.
    """
    def __init__(self, argv: List[str]) -> None:
        super().__init__(argv)


        ############################
        #      ZONA DE BORRADO     #
        #                          #

        self.my_wdgt = MainWindow()

        #                           #
        #                           #
        #############################
