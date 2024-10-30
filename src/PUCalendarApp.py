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
        self.main_window = MainWindow()

        #                           #
        #                           #
        #############################
        
        self.connect_signals()

        self.application_driver.drive()

    def pporqye():
        pass

    def connect_signals(self) -> None:
        self.main_window.SG_window_close_event.connect(
            self.application_driver.closeEvent)
        self.main_window.courses_view.new_class_dialog.SG_request_search.connect(
            self.application_driver.RQ_search_course)
        self.application_driver.SG_web_search_results.connect(
            self.main_window.courses_view.new_class_dialog.RQ_show_search_result)
        self.main_window.courses_view.new_class_dialog.SG_confirm_creation.connect(
            self.application_driver.RQ_create_course)
        self.application_driver.SG_update_courses.connect(
            self.main_window.courses_view.RQ_update_courses)
        self.main_window.courses_view._all_classes_view.SG_request_SingleClassView.connect(
            self.application_driver.RQ_load_SingleClassView_data)
        self.application_driver.SG_show_SingleClassView.connect(
            self.main_window.courses_view.RQ_show_SingleClassView)
        self.application_driver.SG_window_setting.connect(
            self.main_window.RQ_load_settings)
        self.application_driver.SG_finished_loading.connect(
            self.main_window.RQ_splash_finish)