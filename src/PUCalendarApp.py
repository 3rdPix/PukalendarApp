from typing import List
from PyQt6.QtWidgets import QApplication

# Importar explícitamente el módulo de rutas para que las cargue
from config import static_paths

from gui.main_window import MainWindow
from controllers.driver import MainDriver

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
        self.application_driver = MainDriver()
        self.my_wdgt = MainWindow()
        print(self.primaryScreen())

        #                           #
        #                           #
        #############################
        
        self.connect_signals()

    def pporqye():
        pass

    def connect_signals(self) -> None:
        self.my_wdgt.windowIsClosing.connect(self.application_driver.closeEvent)