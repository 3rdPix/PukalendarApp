"""
Cómo funcionan las notas?
-------------------------
No sé gracias, solo sé que nota 7 = promedio 7
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
La nota mínima en la universidad es 1.0, la exigencia te dice qué porcentaje
de \"correctitud\" debe tener para lograr la nota mínima de aprobación (4.0).
Por lo tanto el formato de cálculo más simple implica crear dos rectas, una
para el segmento \"rojo\" entre [1.0, 4.0) y el segmento \"azul\" [4.0, 7.0]
de modo que para un `x` porcentaje de correctitud, la nota `y` será:

Para rojos:
>>> y = ((4.0 - 1.0) / exigencia) * x + 1

Para azules:
>>> y = ((7.0 - 4.0) / (100.0 - exigencia)) * x + 4.0
    - ((7.0 - 4.0) / (100.0 - exigencia)) * exigencia

Esta ecuación debe ajustarse para aquellas calificaciones que tienen un punto
base, el cual se agrega luego de calcular la nota según el puntaje obtenido.
Las ecuaciones en este caso se transforman en:

Para rojos:
>>> y = (3.0 / exigencia) * x + 1

Para azules:
>>> y = ((6.0 - 3.0) / (100.0 - exigencia)) * x + 3.0
    - ((6.0 - 3.0) / (100.0 - exigencia)) * exigencia + 1
"""
from typing import Optional
import logging


log = logging.getLogger("Grading")
GRADE_MINIMUM: float = 1.0
GRADE_MAXIMUM: float = 7.0
GRADE_PASSING: float = 4.0
GRADE_MINIMUM_FOR_BASED: float = 0.0
GRADE_MAXIMUM_FOR_BASED: float = 6.0
GRADE_PASSING_FOR_BASED: float = 3.0
DEFAULT_THRESHOLD: int = 60


class NonGradable(ValueError):
    """
    Error referencial para identificar imposibilidad de crear
    una calificación con el input entregado.
    """


def calculate_blue(score: float,
                   threshold: int, add_base: bool) -> float:
    slope = (GRADE_MAXIMUM - GRADE_PASSING) / (100 - threshold)
    slope_based = ((GRADE_MAXIMUM_FOR_BASED - GRADE_PASSING_FOR_BASED) 
                   / (100 - threshold))
    if not add_base:
        grade = slope * score - slope * threshold + GRADE_PASSING
        return grade
    grade = (slope_based * score - slope_based * threshold
             + GRADE_PASSING_FOR_BASED + 1)
    return grade    


def calculate_red(score: float, threshold: int, add_base: bool) -> float:
    slope = (GRADE_PASSING - GRADE_MINIMUM) / threshold
    slope_based = (GRADE_PASSING_FOR_BASED - GRADE_MINIMUM_FOR_BASED) / threshold
    if not add_base:
        grade = slope * score + GRADE_MINIMUM
        return grade
    grade = slope_based * score + GRADE_MINIMUM_FOR_BASED
    return grade


def calculate_grade(obtained_score: float, total_score: float,
                    threshold: int, add_base: bool) -> float:
    percentage = 100 * (obtained_score / total_score)
    if percentage >= 60:
        return calculate_blue(percentage, threshold, add_base)
    else:
        return calculate_red(percentage, threshold, add_base)


class Grade:
    """
    Nota
    ----
    La unidad atómica de calificación. Por si sola no tiene sentido, es
    necesario unirla por medio de ponderaciones u ecuaciones a otras para
    formar algún promedio.

    + `obtained_score`: el puntaje obtenido de un total determinado, si no
    se especifica `total_score` se asume que se trata de un porcentaje de
    respuestas correctas.

    + `total_score`: el puntaje máximo obtenible. Por ejemplo, en una prueba
    de 80 preguntas de alternativa, el puntaje máximo obtenible es 80.

    + `exigency`: porcentaje de respuestas correctas necesarias para obtener
    el mínimo grado de aprobación. Por defecto es 60.

    + `obtained_grade`: sobrescribe la nota calculada según `obtained_score`.
    Debe estar entre 1.0 y 7.0.

    + `add_base`: si se habilita, se le agrega un punto base (1.0) a la nota
    calculada según el puntaje obtenido.

    Esta estructura lleva nombre (puede ser definido por el usuario). Acepta
    propiedad `enti` (id) definida una sola vez, esta debería ser asignada por
    la clase controladora del grupo al que la nota se agregue.
    """
    def __init__(self, name: str, obtained_score: Optional[float]=None,
                 total_score: float=100.0, threshold: int=DEFAULT_THRESHOLD,
                 obtained_grade: Optional[float]=None,
                 add_base: bool=False) -> None:
        self._defined_as: dict[str, str|float|bool|None] = {
            "name": name,
            "obtained_grade": obtained_grade,
            "total_score": total_score,
            "threshold:": threshold,
            "obtained_grade": obtained_grade,
            "add_base": add_base}
        self.name: str = name[:61] if len(name) > 60 else name
        if obtained_score is not None:
            condicion_1 = obtained_score >= 0
            condicion_2 = obtained_score <= total_score
            condicion_3 = total_score > 0
            condicion_4 = 0 < threshold < 100
            if not all([condicion_1, condicion_2, condicion_3, condicion_4]):
                raise ValueError("Conditions not met to calculate grade")
            self._mathed_grade = calculate_grade(obtained_score, total_score,
                                                 threshold, add_base)
        if obtained_grade:
            if not 1 <= obtained_grade <= 7:
                raise ValueError("Obtained grade not within valid range")
            self._obtained_grade = obtained_grade
        self._id: int = None

    def _get_id(self) -> int: return self._id
    def _set_id(self, id_candidate: int):
        if self._id is None:
            self._id = id_candidate
        raise AttributeError("Invalid id assignment")
    
    id = property(_get_id, _set_id)

    def _get_grade(self) -> float:
        if hasattr(self, "_obtained_grade"):
            return self._obtained_grade
        if hasattr(self, "_mathed_grade"):
            return self._mathed_grade
        return -1

    value = property(_get_grade)

class GradeSimple:
    """
    Calificación simple
    -------------------
    La estructura de notas más sencilla para un ramo está conformada por
    ponderaciones de caalificaciones directas que pertenecen a esta clase.
    Esta estructura además acepta la posibilidad de integrar puntos en
    forma de \"décimas\" que son agregadas a la nota.

    Un ejemplo de un ramo que utilice solo este tipo de calificación puede
    ser como el siguiente:

    **Lenguaje Rúnico II**
      - Interrogación 1 (40%): 7.0 * (0.4) = 2.8
      - Interrogación 2 (40%) (+2 dećimas): 6.0 * (0.4) + 0.2 = 2.6
      - Examen (20%): 5.0 * (0.2) = 1
      Nota final: 6.4
    
    En este escenario, cada evaluación (Interrogación 1, Interrogación 2, y
    Examen) es una estructura de tipo `GradeSimple` con su propia ponderación.
    """
    def __init__(self, id: int, name: str, ponderation: Optional[int]=None,
                 **kwargs) -> None:
        try:
            self.grade: Grade = Grade(name, **kwargs)
            self.grade.id = id
        except ValueError as error:
            log.error(f"There was an error while translating {kwargs} into"
                      f" a grade: \"{error}\". GradeSimple is not kept.")
            raise NonGradable
        except AttributeError as error:
            log.error(f"There was an error while assigning id={id} to {name}:"
                      f"\"{error}\". GradeSimple is kept, Grade is kept,"
                      f"but id is not.")