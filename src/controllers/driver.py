from datetime import timedelta
from PyQt6.QtCore import pyqtBoundSignal
from typing import Optional
from PyQt6.QtCore import QRect
from PyQt6.QtCore import QObject
from config import PUCalendarAppPaths as pt
from config import Settings
from entities.courses import Course
from PyQt6.QtCore import pyqtSignal
from utils import search_for_puclasses
from entities.courses import NRC
from entities import Course
from typing import Any
from collections.abc import Callable
from PyQt6.QtCore import QThread
from controllers.data_interacter import calculate_relative_dedication
import inspect
from inspect import getmembers
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
    SG_update_time_infobox = pyqtSignal(int, list)
    SG_update_SingleClassView = pyqtSignal(dict)
    SG_update_dedication_piechart = pyqtSignal(list, list)

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
        if len(courses_list) > 0: self._udpate_timeinfobox(1)
        else: self._udpate_timeinfobox(0)
    
    def _udpate_timeinfobox(self, to: int, which: Optional[Course]=None,
                            starting_point: Optional[str]=None) -> None:
        match to:
            case 0:
                self.SG_update_time_infobox.emit(0, [])
            case 1:
                times_list = list()
                actually_times = list()
                colors = list()
                for each in self.courses.values():
                    each: Course
                    # trucheria para ahorrarnos los microsegundos
                    cheating = timedelta(seconds=round(each.user_dedicated_time.total_seconds()))
                    times_list.append([each.user_alias, cheating, each.user_color])
                    actually_times.append(each.user_dedicated_time)
                    colors.append(each.user_color)
                percentages = calculate_relative_dedication(actually_times)
                self.SG_update_time_infobox.emit(1, times_list)
                # probablemente no es el mejor sitio para dejar la emisión
                self.SG_update_dedication_piechart.emit(percentages, colors)
            case 2:
                alias_text = which.user_alias
                color_text = which.user_color
                start_text = str(starting_point)
                self.SG_update_time_infobox.emit(
                    2, [alias_text, color_text, start_text])

    def RQ_MainWindow_closeEvent(self, window_status: QRect) -> None:
        courses_list: list[Course] = list(self.courses.values())
        # De momento solo cerraremos a la fuerza el tiempo de la sesión
        for each in courses_list:
            each: Course
            if each.course_on_session:
                each.stop_session()
                break
        log.debug(f"Dumping courses into {pt.Config.USER_COURSES}")
        with open(pt.Config.USER_COURSES, 'wb') as raw_file:
            pickle.dump(courses_list, raw_file)
        Settings.setValue(Settings.Window.RECT, window_status)
        # print(courses_list[0].dump_course())


    def RQ_NewClassDialog_search(self, search_pattern: str) -> None:
        class SearchThread(QThread):
            def run(self, _caller: QObject, pattern: str,
                    dest: pyqtBoundSignal) -> None:
                results = search_for_puclasses(pattern)
                _caller.web_search_results = results
                dest.emit(results)
        enw = SearchThread()
        enw.run(self, search_pattern, self.SG_web_search_results)

    def RQ_NewClassDialog_create(self, index_ref: int, alias: str, color: str) -> None:
        official_info = self.web_search_results[index_ref]
        course = Course(alias, color)
        course._load_official_data(official_info)
        identifier = course.official_nrc
        self.courses[identifier] = course
        self.web_search_results = None
        self._udpate_timeinfobox(1)
        log.debug(f"Successfully addded {identifier} to Courses")

    def RQ_CoursesView_showSingleClass(self, _with: str) -> None:
        self.SG_show_SingleClassView.emit(self.courses.get(_with).__dict__)

    def RQ_SingleClass_start_timer(self, course_id: int) -> None:
        log.debug(f"Received id:{course_id} to search on {self.courses}")
        which: Course = self.courses.get(course_id)
        log.debug(f"Got {which}")
        if starting_point := which.start_session():
            # Datos para timeinfobox
            self._udpate_timeinfobox(2, which, starting_point)
        else:
            log(f"Can't initiate session for {course_id} because other"
                f" course is on session.")
    
    def RQ_SingleClass_stop_timer(self, course_id: int) -> None:
        which: Course = self.courses.get(course_id)
        which.stop_session()
        # Datos para timeinfobox
        self._udpate_timeinfobox(1)
        self.SG_update_SingleClassView.emit(which.__dict__)

    def RQ_CoursesView_delete(self, nrc: NRC) -> None:
        log.info(f"Deleting course:{nrc}")
        if element := self.courses.get(nrc):
            element: Course
            element.stop_session()
            del self.courses[nrc]
            self._udpate_timeinfobox(1)
        else:
            log.warning(f"Couldn't delete course:{nrc} as it doesn't exists")