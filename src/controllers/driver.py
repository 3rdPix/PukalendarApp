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
from entities.tasks import BulletTask
import pickle
from collections import defaultdict
from entities import StudySession
from datetime import datetime
from utils.i18n import _


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
    SG_show_error_bar = pyqtSignal(str, str)
    SG_add_to_bullet_list = pyqtSignal(str, int)

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
            with open(pt.Config.USER_COURSES, "r") as raw_file:
                courses_list: list[str] = raw_file.readlines()
        except (FileNotFoundError, pickle.UnpicklingError, EOFError):
            with open(pt.Config.USER_COURSES, "w") as raw_file:
                pass
            log.warning(f"Failed to load {pt.Config.USER_COURSES}. Creating"
                        f" empty list...")
            courses_list = []
        log.debug(f"Courses files found. Attempting to build from that...")
        for course_string in courses_list:
            separated_data = course_string.split(';')
            # orden bastante arbitrario
            # off_nrc; off_name; off_code; off_prof; off_camp; off_section
            # off_modules; Ualias; Ucolor; Umodules
            single_dict = defaultdict()
            single_dict.__setitem__("official_nrc", separated_data[0])
            single_dict.__setitem__("official_name", separated_data[1])
            single_dict.__setitem__("official_code", separated_data[2])
            single_dict.__setitem__("official_professor", separated_data[3])
            single_dict.__setitem__("official_campus", separated_data[4])
            single_dict.__setitem__("official_section", separated_data[5])
            single_dict.__setitem__("official_modules", separated_data[6])
            single_dict.__setitem__("user_alias", separated_data[7])
            single_dict.__setitem__("user_color", separated_data[8])
            single_dict.__setitem__("user_modules", separated_data[9])

            # Ahora recuperamos las sesiones
            container: list = list()
            target_file = (pt.Config.BASE_COURSE_SESSIONS
                           + separated_data[0]
                           + "_Sessions.csv")
            with open(target_file, 'r') as sessions_data:
                for line in sessions_data:
                    if not line: continue
                    date_as_string, seconds_as_string = line.split(';')
                    session_time = timedelta(seconds=float(seconds_as_string))
                    session_date = datetime.strptime(
                        date_as_string, "%Y-%m-%d").date()
                    new = StudySession(session_date, session_time)
                    container.append(new)
            single_dict.__setitem__("user_sessions", container)

            # recuperación de bullettasks
            point_bullet_path = (pt.Config.BASE_COURSE_BULLETS
                                 + str(separated_data[0])
                                 + "_BulletList.csv")
            bullets_container = list()
            try:
                with open(point_bullet_path, 'r') as bullets_data:
                    bullets_container: list[str] = bullets_data.readlines()
            except FileNotFoundError: pass
            
            log.info("All data from the course extracted. Attempting to "
                      "create object")
            
            current_course = Course('', '#000000')
            current_course.restore_data(single_dict)
            for bullet_task in bullets_container:
                if not bullet_task: continue
                description, done = bullet_task.split(';')
                done = done.strip()
                done = True if done == "True" else False
                current_course.add_bullet_task(description, done)

            
            self.courses[current_course.official_nrc] = current_course
            log.debug("Succesfully added course")
        if len(courses_list) > 0: self._udpate_timeinfobox(1)
        else: self._udpate_timeinfobox(0)
    
    def _udpate_timeinfobox(self, to: int, which: Optional[Course]=None,
                            starting_point: Optional[str]=None) -> None:
        match to:
            case 0:
                self.SG_update_time_infobox.emit(0, [])
            case 1:
                times_list = list()
                colors = list()
                percentages = calculate_relative_dedication(
                    self.courses.values())
                for each in self.courses.values():
                    each: Course
                    # trucheria para ahorrarnos los microsegundos
                    cheating = each.get_dedicated_time()
                    times_list.append(
                        [each.user_alias, cheating, each.user_color])
                    colors.append(each.user_color)
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
        # de momento se guarda elemento a elemento de  cada curso
        # es casi una copia del transformador de versiones
        with open(pt.Config.USER_COURSES, 'w') as blanking: pass
        for course in self.courses.values():
            official_name = course.official_name
            official_nrc = course.official_nrc
            official_code = course.official_code
            official_professor = course.official_professor
            official_campus = course.official_campus
            official_section = course.official_section
            official_modules = course.official_modules
            user_alias = course.user_alias
            user_color = course.user_color
            user_modules = course.user_modules

            single_entry = (""
                            + str(official_nrc) + ';'
                            + str(official_name) + ';'
                            + str(official_code) + ';'
                            + str(official_professor) + ';'
                            + str(official_campus) + ';'
                            + str(official_section) + ';'
                            + str(official_modules) + ';'
                            + str(user_alias) + ';'
                            + str(user_color) + ';'
                            + str(user_modules))
            
            with open(pt.Config.USER_COURSES, 'a') as courses_file:
                courses_file.write(single_entry)

            # sesiones
            point_session_path = (pt.Config.BASE_COURSE_SESSIONS
                                  + str(official_nrc)
                                  + "_Sessions.csv")
            with open(point_session_path, 'w') as blanking: pass
            for session in course.user_sessions:
                with open(point_session_path, 'a') as registry:
                    registry.write(
                        str(session.date)
                        + ';'
                        + str(session.duration.total_seconds() // 1)
                        + '\n')

            # bullettasks
            point_bullet_path = (pt.Config.BASE_COURSE_BULLETS
                                 + str(official_nrc)
                                 + "_BulletList.csv")
            with open(point_bullet_path, 'w') as blanking: pass
            for bullet_task in course.bullet_table.get_all_bullets():
                bullet_task: BulletTask
                line = bullet_task.description + ';' + str(bullet_task.done) + '\n'
                with open(point_bullet_path, 'a') as registry:
                    registry.write(line)
            

        # log.debug(f"Dumping courses into {pt.Config.USER_COURSES}")
        # with open(pt.Config.USER_COURSES, 'wb') as raw_file:
        #     pickle.dump(courses_list, raw_file)
        # Settings.setValue(Settings.Window.RECT, window_status)
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
        """"""
        # esta mandando el diccionario porque no sabe como interpretar
        # el objeto Course. Necesitamos dividir la información en paquetes
        # manejables por diferentes vistas ahora que separamos el tiempo
        # dedicado en sesiones de estudio. no hace daño dejarlo así como está
        # ahora pero tampoco mostrará la información adecuada.
        course_to_be_shown = self.courses.get(_with)
        self.SG_show_SingleClassView.emit(course_to_be_shown.__dict__)
        # also this es para que el driver recuerde a quién estamos viendo
        self.current_shown_course: Course = course_to_be_shown

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

    def RQ_bullettask_status_changed(self, bullet_id: int, checked: bool) -> None:
        # hay algo extraño con walrus acá? quizás tenga que ver con el
        # IF statement? no está claro pero no modifica el objeto
        # quizás no es referencia?
        # verificar
        #
        # if bullet := self.current_shown_course.bullet_table.get_bullet(bullet_id):
        #     bullet.done = checked
        #
        bullet = self.current_shown_course.bullet_table.get_bullet(bullet_id)
        if bullet is not None:
            log.debug(f"Checking bullet {bullet_id} as {checked}")
            bullet.done = checked
        else:
            log.warning("Tried to check an unexisting bullet")

    def RQ_SingleClass_accept_bullet(self, content: str) -> None:
        log.debug(f"User trying to add bullet with content\n\t{content}")
        # no puede estar vacío
        if content == '':
            self.SG_show_error_bar.emit(
                _("Driver.Error.Bullet.NoContent.Title"),
                _("Driver.Error.Bullet.NoContent.Content"))
            return
        elif ';' in content:
            self.SG_show_error_bar.emit(
                _("Driver.Error.Bullet.InvalidChar.Title"),
                _("Driver.Error.Bullet.InvalidChar.Content"))
            return
        bullet_id = self.current_shown_course.add_bullet_task(content, False)
        self.SG_add_to_bullet_list.emit(content, bullet_id)