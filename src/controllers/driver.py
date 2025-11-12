from PyQt6.QtCore import pyqtBoundSignal
from typing import Optional
from PyQt6.QtCore import QRect
from PyQt6.QtCore import QObject
from config import Settings
from entities.courses import Course
from PyQt6.QtCore import pyqtSignal
from utils import search_for_puclasses
from entities.courses import NRC
from entities import Course
from typing import Any
from PyQt6.QtCore import QThread
import logging
from utils.i18n import _
from controllers.database_handler import DatabaseManager
from common.entities import CursoAplicacion
from common.entities import ResultadoBuscacurso
from typing import Any
from controllers.study_session import SessionController
from datetime import timedelta


log = logging.getLogger("Driver")


class CoursesDict(dict[int, CursoAplicacion]):
    def __init__(self, signal: pyqtBoundSignal,
                 initial_dict: dict[int, CursoAplicacion]) -> None:
        super().__init__(initial_dict)
        self.pipe = signal

    def notify(self) -> None:
        self.pipe.emit([course for course in self.values()])
    
    def __setitem__(self, key: Any, value: Any) -> None:
        super().__setitem__(key, value)
        self.notify()
    
    def __delitem__(self, key: Any) -> None:
        super().__delitem__(key)
        self.notify()

    def update(self, *args: Any, **kwargs: Any) -> None:
        super().update(*args, **kwargs)
        self.notify()

    def clear(self) -> None:
        super().clear()
        self.notify()

class MainDriver(QObject):
    SG_update_courses = pyqtSignal(list)
    SG_web_search_results = pyqtSignal(list)
    SG_show_SingleClassView = pyqtSignal(CursoAplicacion)
    SG_window_setting = pyqtSignal(QRect)
    SG_show_main_window = pyqtSignal()
    SG_finished_loading = pyqtSignal()
    SG_update_time_infobox = pyqtSignal(int, list)
    SG_update_SingleClassView = pyqtSignal(dict)
    SG_update_dedication_piechart = pyqtSignal(list, list)
    SG_show_error_bar = pyqtSignal(str, str)
    SG_add_to_bullet_list = pyqtSignal(str, int)
    SG_pause_study_session = pyqtSignal()
    SG_update_current_session_time = pyqtSignal(timedelta)

    def __init__(self) -> None:
        super().__init__()
        self.web_search_results: list[ResultadoBuscacurso]|None = None
        self.database_handle = DatabaseManager()
        self.study_session_manager = SessionController(self)

    def drive(self) -> None:
        # Corre la aplicación
        self.load_settings()
        self.load_courses()
        self.SG_finished_loading.emit()

    def load_settings(self) -> None:
        self.SG_window_setting.emit(Settings.value(Settings.Window.RECT))

    def load_courses(self) -> None:
        self.courses = CoursesDict(self.SG_update_courses,
                                   self.database_handle.obtener_cursos_activos())
        self.courses.update()
    
    def _udpate_timeinfobox(self, to: int, which: Optional[Course]=None,
                            starting_point: Optional[str]=None) -> None:
        # TODO: cargar la información desde db
        pass

    def RQ_MainWindow_closeEvent(self, window_status: QRect) -> None:
        pass

    def RQ_NewClassDialog_search(self, search_pattern: str) -> None:
        class SearchThread(QThread):
            resultados_listos = pyqtSignal(list)
            def __init__(self, pattern: str) -> None:
                super().__init__()
                self.pattern = pattern
            def run(self) -> None:
                self.resultados_listos.emit(search_for_puclasses(self.pattern))

        self.enw = SearchThread(search_pattern)
        self.enw.resultados_listos.connect(self.receive_buscacursos_results)
        self.enw.finished.connect(self.enw.deleteLater)
        self.enw.start()
    
    def receive_buscacursos_results(self, resultados: list[ResultadoBuscacurso]
                                    ) -> None:
        self.web_search_results = resultados
        self.SG_web_search_results.emit(resultados)
        del self.enw

    def RQ_NewClassDialog_create(self, index_ref: int, alias: str, color: str) -> None:
        if self.web_search_results is None: return
        official_info = self.web_search_results[index_ref]
        single_to_three: dict[str, str] = {
            'L': "Lun", 'M': "Mar", 'W': "Mie",
            'J': "Jue", 'V': "Vie", 'S': "Sab"}
        scheduled: list[tuple[str, int, str, str]] = list()
        # [['L-W-V:4', 'CLAS', 'M2'], ['L:5', 'AYU', 'BC21'], ['L:6', 'LAB', 'SIN SALA']]
        for instance_type in official_info.modulos:
            times, name, place = instance_type
            days, modules = times.split(':')
            days_separated = days.split('-')
            modules_separated = modules.split(',')
            for day in days_separated:
                for module in modules_separated:
                    dia_semana = single_to_three[day]
                    numero_modulo = module
                    sala = place
                    nombre = name
                    scheduled.append((dia_semana, int(numero_modulo), sala, nombre))
        identifier = self.database_handle.create_course(
            desde=official_info, alias=alias, color=color, scheduled=scheduled)
        nuevo_curso = CursoAplicacion(
            sigla=official_info.sigla,
            nombre=official_info.nombre,
            creditos=official_info.creditos,
            nrc=official_info.nrc,
            profesor=official_info.profesor,
            campus=official_info.campus,
            seccion=official_info.seccion,
            periodo=official_info.periodo,
            identificador=identifier,
            alias=alias,
            color=color)
        self.courses[nuevo_curso.identificador] = nuevo_curso

    def RQ_CoursesView_showSingleClass(self, _with: int) -> None:
        course_to_be_shown = self.courses.get(_with)
        self.current_shown_course = course_to_be_shown
        self.SG_show_SingleClassView.emit(course_to_be_shown)

    def RQ_SingleClass_start_timer(self, course_id: int) -> None:
        self.study_session_manager.start_session(course_id)
    
    def RQ_SingleClass_stop_timer(self) -> None:
        session = self.study_session_manager.stop_session()
        self.database_handle.create_study_session(session)

    def RQ_CoursesView_delete(self, nrc: NRC) -> None:
        raise NotImplemented
        log.info(f"Deleting course:{nrc}")
        if element := self.courses.get(nrc):
            element: Course
            element.stop_session()
            del self.courses[nrc]
            self._udpate_timeinfobox(1)
        else:
            log.warning(f"Couldn't delete course:{nrc} as it doesn't exists")

    def RQ_bullettask_status_changed(self, bullet_id: int, checked: bool) -> None:
        raise NotImplemented
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
        raise NotImplemented
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