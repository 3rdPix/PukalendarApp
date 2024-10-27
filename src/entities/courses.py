from typing import TypeAlias
from datetime import datetime
from datetime import timedelta

CourseCode: TypeAlias = str
Module: TypeAlias = int
Campus: TypeAlias = int
PersonName: TypeAlias = str


class SessionTimer:
    _instance: object = None
    on_session: bool = False
    session_start: datetime = None
    session_end: datetime = None
    session_duration: timedelta = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def start_session(self) -> bool:
        if self.on_session: return False
        self.on_session = True
        self.session_start = datetime.now()
        return True
    
    def end_session(self) -> timedelta:
        if not self.on_session: return False
        self.session_end = datetime.now()
        self.session_duration = self.session_start - self.session_end
        self.on_session = False
        return self.session_duration

class NRC(int):
    def __new__(cls, value: int):
        if not (10000 <= value <= 99999):
            raise ValueError("NRC must be between 10000 and 99999.")
        return super().__new__(cls, value) 


class HexColor:
    def __init__(self, hex_value: str):
        if not self._is_valid_hex(hex_value):
            raise ValueError(f"Invalid hex color: {hex_value}")
        self.hex_value = hex_value

    def _is_valid_hex(self, hex_value: str) -> bool:
        if isinstance(hex_value, str) and len(hex_value) == 7 and hex_value[0] == '#':
            hex_digits = hex_value[1:]
            return all(c in '0123456789ABCDEFabcdef' for c in hex_digits)
        return False

    def to_rgb(self):
        hex_value = self.hex_value.lstrip('#')
        return tuple(int(hex_value[i:i + 2], 16) for i in (0, 2, 4))

    def __str__(self):
        return self.hex_value


class GradeTable:
    """
    Definición de estructura de grados
    """
    @classmethod
    def from_data(cls, data) -> None:
        raise NotImplementedError


class Course:
    official_name: str = None
    official_nrc: NRC = None
    official_code: CourseCode = None
    official_professor: PersonName = None
    official_campus: Campus = None
    official_section: int = None
    official_modules: list[Module] = None
    user_alias: str = None
    user_color: HexColor = None
    user_dedicated_time: timedelta = None
    user_grades: GradeTable = None
    user_modules: list[Module] = None
    sessions_timer: SessionTimer = SessionTimer()
    course_on_session: bool = False

    def __init__(self, alias: str, color: str) -> None:
        self.user_alias = alias
        self.user_color = HexColor(color)
        self.user_dedicated_time = 0
        self.user_grades = GradeTable()
        self.user_modules = list()

    def load_official_data(self, source: dict[str, str|int]) -> None:
        self.official_name = source.get("official_name")
        self.official_nrc = source.get("official_nrc")
        self.official_code = source.get("official_code")
        self.official_professor = source.get("official_professor")
        self.official_campus = source.get("official_campus")
        self.official_section = source.get("official_section")
        self.official_modules = source.get("official_modules")

    def load_gradeTable(self, data=None) -> None:
        self.user_grades = GradeTable.from_data(data) if data else GradeTable()

    def load_user_data(self, source: dict[str, str|int|list]) -> None:
        self.user_alias = source.get("user_alias")
        self.user_color = source.get("user_color")
        self.user_dedicated_time = source.get("user_dedicated_time")
        self.user_modules = source.get("user_modules")

    def start_session(self) -> None:
        if Course.sessions_timer.start_session():
            self.course_on_session = True
    
    def stop_session(self) -> None:
        session_time: timedelta = Course.sessions_timer.end_session()
        self.user_dedicated_time += session_time