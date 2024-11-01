from dataclasses import dataclass
from typing import TypeAlias
from datetime import datetime
from datetime import timedelta
import logging
import grades

log = logging.getLogger("Courses")


CourseCode: TypeAlias = str
Module: TypeAlias = int
Campus: TypeAlias = int
PersonName: TypeAlias = str
GRADE_LOWEST: int = 1
GRADE_APPROVAL: int = 4
GRADE_HIGHEST: int = 7
GRADE_HIGHEST_BASE: int = 6


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


def calculate_grade(obtained_score: float, total_score: float,
                    exigency: int, add_base: bool) -> float:
    percentage = 100 * (obtained_score / total_score)
    slope_red = (GRADE_APPROVAL - GRADE_LOWEST) / exigency
    slope_blue = (GRADE_HIGHEST - GRADE_APPROVAL) / (100 - exigency)
    grade_red = (slope_red * percentage) + GRADE_LOWEST
    grade_blue = (slope_blue * percentage) - (slope_blue * exigency) + GRADE_APPROVAL
    if percentage >= exigency: return grade_blue
    return grade_red


class Grade: # Deprecate? No!
    """
    Nota
    ----
    Por si sola no tiene significado ni peso. Esta estructura se utiliza
    únicamente para guardar una calificación atómica que
    pueda ser expresada a través de estructuras con deiniciones de relación.
    """
    def __init__(self, obtained_score: float, total_score: float,
                    obtained_grade: float=-1, exigency: int=60) -> None:
        self.obtained_score = obtained_score
        self.total_score = total_score
        if obtained_grade == -1:
            self.obtained_grade = calculate_grade(
                obtained_score, total_score, exigency)
        else: self.obtained_grade = obtained_grade
        self.exigency = exigency


class SimpleGrade:
    """
    Calificación simple
    --------------------

    La estructura de notas más sencilla para un ramo está conformada
    por ponderaciones de calificaciones directas que pertenecen a esta
    clase. Esta estructura además acepta la posibilidad de integrar
    puntos adicionales en forma de \"décimas\" que son agregadas a la
    calificación.

    Un ejemplo de un ramo que utilice solo este tipo de calificación
    puede ser como el siguiente:

    **Lenguaje Rúnico II**
      - Interrogación 1 (40%): 7.0 * (0.4) = 2.8
      - Interrogación 2 (40%) (+2 dećimas): 6.0 * (0.4) + 0.2 = 2.6
      - Examen (20%): 5.0 * (0.2) = 1
      Nota final: 6.4
    
    En este escenario, cada evaluación (Interrogación 1, Interrogación 2, y
    Examen) es una estructura de tipo `SimpleGrade` con su propia ponderación.
    """
    def __init__(self, name: str, ponderator: int=-1, obtained_score: float=-1,
                 total_score: float=-1, obtained_grade: float=-1,
                 exigency: int=60, extra_points: int=0) -> None:
        self.name: str = name
        self.ponderator = ponderator if ponderator > 0 else None
        # Verificar sentido numérico
        condition_0: bool = obtained_score >= 0
        condition_1: bool = total_score > 0
        condition_2: bool = obtained_score <= total_score
        condition_3: bool = 1 <= exigency <= 99
        condition_4: bool = 0 <= extra_points <= 70
        if all([condition_0, condition_1, condition_2,
                condition_3, condition_4]):
            self.grade: Grade = Grade(obtained_score, total_score,
                                      obtained_grade=obtained_grade,
                                      exigency=exigency)


class GroupGrade:
    """
    Calificación de grupo
    ---------------------
    Esta estructura busca agrupar evaluaciones que están asociadas
    a un mismo ponderador. Por lo general esta toma forma de controles
    que se realizan a lo largo del semestre. La nota final de este grupo
    es calculada como la media aritmética entre todas las evaluaciones
    que contiene.

    Supongamos que en un ramo **Lenguaje Rúnico II** hay 4 controles a lo
    largo del semestre, y que la nota de controles se evalúa como el 20%
    de la nota final del curso. El aporte final de los controles se puede
    calcular de la siguiente forma:

      - Control 1:  7.0
      - Control 2:  2.0
      - Control 3:  5.0
      - Control 4:  5.5
      Promedio controles: (7.0 + 2.0 + 5.0 + 5.5) / 4 = 4.875
      Aporte a la nota final: 4.875 * (0.2) = 0.975

    Cada calificación es almacenada como una instancia de la clase
    `SimpleGrade` por lo que es posible asignarle a cada control un
    ponderador que tendrá efecto únicamente dentro de este grupo.
    La nota final será calculada en consideración de tales ponderadores,
    y las evaluaciones que no tienen ponderadores se agruparán para aportar
    con el porcentaje restante de la nota final del grupo.
    """

class SubCourse:
    """
    Estructura de califiaciones semejante a sub-grupo pero puede estar al
    mismo nivel de un ramo. Pensada a partir de laboratorios, con sus
    propios nombres, horarios, y ponderaciones, pero que siguen formando
    parte de un ramo padre
    """


class FormattedGroup:
    """
    Grupo de calificaciones con formato
    -----------------------------------
    Esta estructura relaciona `Grade` a través de una fórmula que puede
    ser dinámicamente definida por el usuario. Tiene el objetivo de aceptar
    combinaciones condicionales, en que las ponderaciones no son suficientes
    para modelar el comportamiento de los resultados.

    Un ejemplo con el ramo *Magia Elemental III* que tiene dos interrogaciones
    y un examen. Estas evaluaciones forma el grupo "notas teóricas", que
    tiene ponderación del 70% de la nota final como grupo, pero cada
    evaluación se relaciona de la siguiente forma:
    
    >>> i1, i2, Ex = interrogacion_1, interrogacion_2, Examen
    >>> nota_teorica = (i1 + i2 + 2 * Ex - min(i1, i2, Ex)) / 3
    
    Es decir, `nota_teorica` es la media aritmética de el examen, y las dos
    evaluaciones con nota mayor (pudiendo incluir al examen mismo de nuevo).
    Esta y otras estructuras complejas con fórmulas no comunes pueden ser
    definidas en esta clase.
    """

class GradeTable:
    """
    Tabla de grados
    --------------------
    Cada curso tiene asociada una tabla de grados que contiene todas las
    sub-estructuras de calificaciones que el usuario defina. Esta clase
    se encarga de verificar una repartición ponderada coherente, así como
    de integrar las diferencias entre las sub-estructuras en el cálculo de
    nota final.
    """
    
    @classmethod
    def from_data(cls, data) -> None:
        raise NotImplementedError


class Course:
    official_name: str
    official_nrc: NRC
    official_code: CourseCode
    official_professor: PersonName
    official_campus: Campus
    official_section: int
    official_modules: list[Module]
    user_alias: str
    user_color: HexColor
    user_dedicated_time: timedelta
    user_grades: GradeTable
    user_modules: list[Module]
    sessions_timer: SessionTimer = SessionTimer()
    course_on_session: bool

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