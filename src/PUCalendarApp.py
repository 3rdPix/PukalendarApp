from typing import List
from PyQt6.QtWidgets import QApplication
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

        #                           #
        #                           #
        #############################
        
        self.connect_signals()

        self.application_driver.drive()

    def pporqye():
        pass

    def connect_signals(self) -> None:
        self.my_wdgt.SG_window_close_event.connect(
            self.application_driver.closeEvent)
        self.my_wdgt.courses_view.new_class_dialog.SG_request_search.connect(
            self.application_driver.RQ_search_course)
        self.application_driver.SG_web_search_results.connect(
            self.my_wdgt.courses_view.new_class_dialog.RQ_show_search_result)
        self.my_wdgt.courses_view.new_class_dialog.SG_confirm_creation.connect(
            self.application_driver.RQ_create_course)
        self.application_driver.SG_update_courses.connect(
            self.my_wdgt.courses_view.RQ_update_courses)