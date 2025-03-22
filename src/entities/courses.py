"""
# Cursos

Este módulo encapsula el comportamiento de los cursos. Estableciendo los
atributos que tienen y las funcionalidades asociadas a cada uno.
"""

from dataclasses import dataclass
from typing import TypeAlias
from datetime import datetime
from datetime import timedelta
import logging
from entities.grades import GradeTable
from collections import defaultdict
from json import dumps
from entities.tasks import BulletTaskTable
from threading import Lock

log = logging.getLogger("Courses")

__all__ = {"Course", "SessionTimer", "NRC", "StudySession"}

CourseCode: TypeAlias = str
Module: TypeAlias = int
Campus: TypeAlias = str
PersonName: TypeAlias = str
GRADE_LOWEST: int = 1
GRADE_APPROVAL: int = 4
GRADE_HIGHEST: int = 7
GRADE_HIGHEST_BASE: int = 6


class SessionTimer:
    _instance: object = None

    def __init__(self) -> None:
        self._on_session: bool = False
        self._session_start: datetime = None
        self._session_end: datetime = None
        self._session_duration: datetime = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def start_session(self) -> bool:
        """
        Intenta iniciar una sesión de estudio. Si tiene éxito, guarda el
        `datetime.now()` en `session_start` y actualiza el valor de estado
        `on_session`. Retorna `True` si tiene éxito, `False` en caso
        contrario.
        """
        if self._on_session: return False
        self._on_session = True
        self._session_start = datetime.now()
        return True
    
    def end_session(self) -> timedelta:
        """
        Intenta detener la sesión de estudio si el valor de estado
        `on_session` es coherente. Si tiene éxito, calcula y retorna
        el `timedelta` desde el inicio de la sesión. Retorna `False` en caso
        contrario.
        """
        if not self._on_session: return False
        self._session_end = datetime.now()
        self._session_duration = self._session_end - self._session_start
        self._on_session = False
        return self._session_duration

class NRC(int):
    """
    Clase particular de `int` que limita los valores a un rango válido
    basado en los valores posibles para los NRC de los cursos. Se asume
    que los valores están en el rango $[10000, 99999]$.
    """
    def __new__(cls, value: int):
        if not (10000 <= int(value) <= 99999):
            raise ValueError("NRC must be between 10000 and 99999.")
        return super().__new__(cls, value) 


class HexColor(str):
    def __init__(self, hex_value: str):
        if not self._is_valid_hex(hex_value):
            raise ValueError(f"Invalid hex color: {hex_value}")
        self.hex_value = hex_value
        super().__init__()

    def _is_valid_hex(self, hex_value: str) -> bool:
        if (isinstance(hex_value, str) and len(hex_value) == 7
           and hex_value[0] == '#'):
            hex_digits = hex_value[1:]
            return all(c in '0123456789ABCDEFabcdef' for c in hex_digits)
        return False

    def to_rgb(self):
        hex_value = self.hex_value.lstrip('#')
        return tuple(int(hex_value[i:i + 2], 16) for i in (0, 2, 4))

    def __str__(self):
        return self.hex_value
    
    def __repr__(self) -> str:
        return self.__str__()

@dataclass
class StudySession:
    date: datetime
    duration: timedelta = timedelta(0)

class Course:
    """
    La clase que define a un curso particular, guarda sus atributos y
    contiene referencia a el estado del mismo en relación con `SessionTimer`
    """
    _sessions_timer: SessionTimer = SessionTimer()
    course_on_session: bool = False

    def __init__(self, alias: str, color: str) -> None:
        self._establish_attr(alias, color)
    
    def _establish_attr(self, alias: str, color: str) -> None:
        self.user_alias = alias
        self.user_color = HexColor(color)
        self.user_dedicated_time = timedelta(0)
        self.user_grades = GradeTable()
        self.user_modules = list()
        self.user_sessions = list()
        self.bullet_table = BulletTaskTable()
        self.safespot = Lock()

    def _load_official_data(self, source: dict[str, str|int]) -> None:
        self.official_name = source.get("official_name")
        self.official_nrc = NRC(source.get("official_nrc"))
        self.official_code = CourseCode(source.get("official_code"))
        self.official_professor = PersonName(source.get("official_professor"))
        self.official_campus = Campus(source.get("official_campus"))
        self.official_section = source.get("official_section")
        # Recordar que estó está por definirse
        self.official_modules = source.get("official_modules")

    def _load_gradeTable(self, data=None) -> None:
        self.user_grades = GradeTable.from_data(data) if data else GradeTable()

    def _load_user_data(self, source: dict[str, str|int|list|set]) -> None:
        self.user_alias = source.get("user_alias")
        self.user_color = HexColor(source.get("user_color"))
        # deprecado
        # self.user_dedicated_time = source.get("user_dedicated_time")
        self.user_modules = source.get("user_modules")
        self.user_sessions = source.get("user_sessions")

    def restore_data(self, source: dict[str, str|int|list|set]) -> None:
        self._load_official_data(source)
        self._load_user_data(source)

    def start_session(self) -> datetime|None:
        """
        Crea una marca temporal que indica el inicio de la sesión de estudio.
        `SessionTimer` es bloqueado, de modo que no es posible iniciar otra
        sesión de estudio asociada a algún curso diferente, ni volver a iniciar
        una sesión de estudio en el curso que ya inició una.
        """
        if Course._sessions_timer.start_session():
            self._current_session = StudySession(datetime.now().date())
            self.course_on_session = True
            return Course._sessions_timer._session_start

    def stop_session(self) -> None:
        """
        Utiliza la marca temporal creada anteriormente para calcular el tiempo
        dedicado en la sesión de estudio. Agrega este valor al total de
        tiempo dedicado. Desbloquea `SessionTimer` para que pueda ser
        utilizado por otras instancias de `Course`.
        """
        if not self.course_on_session: return
        session_time: timedelta = Course._sessions_timer.end_session()
        if not isinstance(session_time, timedelta):
            log.error(f"Uncoordinated status of self.on_session with"
                      f" sessions timer on {self.official_name}."
                      f" Forcefully closing session.")
            self.course_on_session = False
            return

        self._current_session.duration = timedelta(
            seconds=session_time.total_seconds() // 1)
        self.user_sessions.append(self._current_session)
        # deprecado
        # self.user_dedicated_time += session_time
        self.course_on_session = False

    def get_dedicated_time(self) -> timedelta:
        """
        Retorna el tiempo total dedicato al curso sumando todas las sesiones
        de estudio
        """
        return sum((session.duration for session in self.user_sessions),
                   start=timedelta(0))
    
    def get_last_week_sessions(self) -> list[StudySession]:
        """
        Retorna una lista con todas las sesiones que han tenido lugar
        en la última semana
        """
        one_week_ago = datetime.now() - timedelta(weeks=1)
        return [session for session in self.user_sessions
                if session.date >= one_week_ago]
    
    def add_bullet_task(self, description: str, done: bool) -> int:
        """
        Crea una nueva tarea rápida y retorna el id
        """
        return self.bullet_table.create_bullet(description, done)