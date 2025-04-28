"""@private"""
from typing import List
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow
from gui.main_window import MainWindow
from controllers.driver import MainDriver
from inspect import getmembers
from logging import getLogger
from gui import PukalendarWidget
from PyQt6.QtCore import pyqtBoundSignal
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

log = getLogger("MainApp")

def __trsg__(cls: QWidget) -> None:
        for element_name, element in getmembers(
            cls, predicate=lambda x: isinstance(x, PukalendarWidget)):
            log.debug(f"Starting elevation for {element_name}")
            __trsg__(element)
            for name, attr in getmembers(element, predicate=lambda x: isinstance(x, pyqtBoundSignal)):
                if not name.startswith("SG"): continue
                log.debug(f"Handling {name} to {cls.objectName()}")
                setattr(cls, name, attr)

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
        self.main_window = MainWindow()
        self.application_driver = MainDriver()

        #                           #
        #                           #
        #############################
        
        __trsg__(self.main_window)
        self.connect_signals()
        self.application_driver.drive()

    def connect_signals(self) -> None:
        # esto se hará con introspección dinámica a futuro
        ## btw este es el futuro, y se hace con introspección dinámica xd
        ### also debería confesar que estoy arrepentido
        for signal_atr_name, signal in getmembers(
             self.main_window,
             predicate=lambda x: isinstance(x, pyqtBoundSignal)):
            if not signal_atr_name.startswith("SG_"): continue
            log.debug(f"Got member {signal_atr_name}")
            signal: pyqtSignal
            target_name = "RQ_" + signal_atr_name[3:]
            try:
                target_fun = getattr(self.application_driver, target_name)
                signal.connect(target_fun)
                log.debug(f"Successfully connected {signal_atr_name} into {target_name}")
            except AttributeError:
                log.error(f"Signal «{signal_atr_name}» exists but has no "
                          f"receiver in driver")

        self.application_driver.SG_show_SingleClassView.connect(
            self.main_window.courses_view.RQ_show_SingleClassView)
        self.application_driver.SG_window_setting.connect(
            self.main_window.RQ_window_setting)
        self.application_driver.SG_finished_loading.connect(
            self.main_window.RQ_finished_loading)
        self.application_driver.SG_update_time_infobox.connect(
            self.main_window.home_view.RQ_update_time_infobox)
        self.application_driver.SG_update_SingleClassView.connect(
            self.main_window.courses_view._single_class_view.RQ_update_SingleClassView)
        self.application_driver.SG_update_dedication_piechart.connect(
            self.main_window.home_view.RQ_update_dedication_piechart)
        self.application_driver.SG_update_courses.connect(
            self.main_window.courses_view.RQ_update_courses)
        self.application_driver.SG_web_search_results.connect(
            self.main_window.courses_view.new_class_dialog.RQ_web_search_result)
        self.application_driver.SG_show_error_bar.connect(
            self.main_window.RQ_show_error_bar)
        self.application_driver.SG_add_to_bullet_list.connect(
            self.main_window.courses_view._single_class_view.RQ_add_new_bullet)
        