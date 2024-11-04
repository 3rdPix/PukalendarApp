from PyQt6.QtCore import QRect
from PyQt6.QtCore import QObject
from config import PUCalendarAppPaths as pt
from config import Settings
from entities.courses import Course
from PyQt6.QtCore import pyqtSignal
from utils import search_for_puclasses
from entities import Course
from typing import Any
from collections.abc import Callable
import logging
import pickle


log = logging.getLogger("Driver")

class CoursesSet(dict):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.subscribers: set[tuple[pyqtSignal, Callable]] = set()

    def notify(self) -> None:
        (signal.emit(packager(self)) for signal, packager in self.subscribers)

    def add_subscriber(self, signal: pyqtSignal, packager: Callable) -> None:
        self.subscribers.add((signal, packager))
    
    def __setitem__(self, key: Any, value: Any) -> None:
        super().__setitem__(key, value)
        self.notify()
    
    def __delitem__(self, key: Any) -> None:
        super().__delitem__(key)
        self.notify()

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)
        self.notify()

    def clear(self) -> None:
        super().clear()
        self.notify()

class CoursesDict(dict):
    def __init__(self, signal: pyqtSignal, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.pipe: pyqtSignal = signal

    def notify(self) -> None:
        self.pipe.emit([course.__dict__ for course in self.values()])
    
    def __setitem__(self, key: Any, value: Any) -> None:
        super().__setitem__(key, value)
        self.notify()
    
    def __delitem__(self, key: Any) -> None:
        super().__delitem__(key)
        self.notify()

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)
        self.notify()

    def clear(self) -> None:
        super().clear()
        self.notify()

class MainDriver(QObject):
    SG_update_courses = pyqtSignal(list)
    SG_web_search_results = pyqtSignal(list)
    SG_show_SingleClassView = pyqtSignal(dict)
    SG_window_setting = pyqtSignal(QRect)
    SG_show_main_window = pyqtSignal()
    SG_finished_loading = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.web_search_results = None

    def drive(self) -> None:
        # Corre la aplicación
        self.load_settings()
        self.load_courses()
        self.SG_finished_loading.emit()

    def load_settings(self) -> None:
        self.SG_window_setting.emit(Settings.value(Settings.Window.RECT))

    def load_courses(self) -> None:
        self.courses: CoursesDict[str, Course] = CoursesDict(
            self.SG_update_courses)
        log.debug("Trying to load courses from file")
        try:
            with open(pt.Config.USER_COURSES, "rb") as raw_file:
                courses_list: list[Course] = pickle.load(raw_file)
            log.debug(f"Succesfully loaded {pt.Config.USER_COURSES}")
        except (FileNotFoundError, pickle.UnpicklingError, EOFError):
            with open(pt.Config.USER_COURSES, "wb") as raw_file:
                courses_list: list[Course] = list()
                pickle.dump(courses_list, raw_file)
            log.warning(f"Failed to load {pt.Config.USER_COURSES}. Creating"
                        f" empty list...")
        for course in courses_list:
            self.courses[course.official_nrc] = course

    def closeEvent(self, window_status: QRect) -> None:
        courses_list: list[Course] = list(self.courses.values())
        log.debug(f"Dumping courses into {pt.Config.USER_COURSES}")
        with open(pt.Config.USER_COURSES, 'wb') as raw_file:
            pickle.dump(courses_list, raw_file)
        Settings.setValue(Settings.Window.RECT, window_status)

    def RQ_search_course(self, search_pattern: str) -> None:
        self.web_search_results = search_for_puclasses(search_pattern)
        self.SG_web_search_results.emit(self.web_search_results)

    def RQ_create_course(self, index_ref: int, alias: str, color: str) -> None:
        official_info = self.web_search_results[index_ref]
        course = Course(alias, color)
        course.load_official_data(official_info)
        identifier = course.official_nrc
        self.courses[identifier] = course
        self.web_search_results = None
        log.debug(f"Successfully addded {identifier} to Courses")

    def RQ_load_SingleClassView_data(self, _with: str) -> None:
        self.SG_show_SingleClassView.emit(self.courses.get(_with).__dict__)

    def RQ_start_timer(self, course_id: int) -> None:
        log.debug(f"Received id:{course_id} to search on {self.courses}")
        which: Course = self.courses.get(course_id)
        log.debug(f"Got {which}")
        which.start_session()
    
    def RQ_stop_timer(self, course_id: int) -> None:
        which: Course = self.courses.get(course_id)
        which.stop_session()