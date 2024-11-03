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
from collections import defaultdict
from typing import Self
from typing import TypeAlias
from collections.abc import Iterator
from itertools import count
from utils import WtfError
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
            if not GRADE_MINIMUM <= obtained_grade <= GRADE_MAXIMUM:
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

    + `name`: el nombre asociado a la evaluación

    + `ponderation`: el porcentaje de importancia de la evaluación en el
    conjunto al que pertenece. Es nulo por defecto, de modo que pasa como
    argumento en el cálculo de media aritmética.

    + `extra_points`: décimas extra que se aplican a la calificación, en caso
    de que existan.

    + `extremist`: si la evaluación tiene requisitos de rendimiento propias,
    es decir, requiere de una nota mínima para aprobar el curso, se debe
    indicar a través de este atributo. Esto ocurre en ocasiones con algunos
    examenes llamados "reprobatorios" que exigen una nota mínima de 3.95
    por si propia cuenta para aprobar el ramo.
    """
    def __init__(self, id: int, name: str, ponderation: Optional[int]=None,
                 extra_points: int=0, extremist: Optional[float]=None,
                 **kwargs) -> None:
        try:
            self.grade: Grade = Grade(name, **kwargs)
            self.id = id
        except ValueError as error:
            log.error(f"There was an error while translating {kwargs} into"
                      f" a grade: \"{error}\". GradeSimple is not kept.")
            raise NonGradable
        except AttributeError as error:
            log.error(f"There was an error while assigning id={id} to {name}:"
                      f"\"{error}\". GradeSimple is kept, Grade is kept,"
                      f"but id is not.")
        self.ponderator = ponderation
        self.extra_points = extra_points
        self.extremist = extremist
    
    def _get_grade(self) -> float: ...
    def _set_grade(self, force: float) -> float: ...
    value = property(_get_grade, _set_grade)
        

class GradeGroup:
    """
    Calificación de grupo
    ---------------------
    Esta estructura busca agrupar evaluaciones que están asociadas a un mismo
    ponderador. Por lo general esta toma forma de controles que se realizan
    a lo largo del semestre. Pero es posible agrupar `GradeSimple` de modo que
    la nota final de este grupo se calcule como una ponderación de sus
    elementos. Esto aplica únicamente a aquellos elementos que tengan
    asignado un porcentaje.  

    Esta estructura, en conjunto con `GradeSimple` debería ser suficiente
    para modelar la gran mayoría de los cursos. Un curso en sí, es una
    estructura `GradeGroup` que contiene otros `GradeGroup` dentro de sí, los
    cuales interactúan con los `GradeSimple` definidos para el curso.
    """
    _ids: Iterator = count()
    def __init__(self, id: int, name: str, ponderation: Optional[int]=None,
                 extra_points: int=0, extremist: Optional[float]=None) -> None:
        # Para esta clase el método __init__ no tiene mucha magia
        # Toda la lógica mágica está contenido en los métodos
        self.name: str = name[:61] if len(name) > 60 else name
        self.ponderation = ponderation
        self.extra_points = extra_points
        self.extremist = extremist
        self.group_ponderated: dict[int, GradeSimple] = defaultdict()
        self.group_unponderated: dict[int, GradeSimple] = defaultdict()
        self.id = id
        self._table_level: int = 100
    
    def try_ponderation(self, request: int) -> int:
        if request is None or request < 1: return None
        if self._table_level < request:
            return self.try_ponderation(self._table_level)
        self._table_level -= request
        return request


    # Hablando de métodos... no los voy a definir por ahora xD
    def add_grade(self, name: str, **data) -> int|None:
        if name is None: return None
        ponderation = self.try_ponderation(data.get("ponderation"))
        creation = GradeSimple(next(self._ids), name, ponderation=ponderation,
                               **{key: data.get(key) for key in data.keys() \
                                  if key not in ("name", "ponderation")})
        if creation.ponderator is None:
            self.group_ponderated.__setitem__(creation.id, creation)
        else:
            self.group_unponderated.__setitem__(creation.id, creation)
        return creation.id

    def remove_grade(self, id: int) -> bool:
        if id in self.group_ponderated.keys():
            self.group_ponderated.__delitem__(id)
        else:
            self.group_unponderated.__delitem__(id)
        return True
        
    def edit_grade(self, id: int, **kwargs) -> bool:
        if id in self.group_ponderated.keys():
            reference = self.group_ponderated.get(id)
        elif id in self.group_unponderated.keys():
            reference = self.group_unpoderated.keys()
        else:
            raise WtfError("GradeGroup>edit_grade")
        for key in kwargs:
            if hasattr(reference, key):
                setattr(reference, key, kwargs.get(key))
        return True

    def edit_group(self, *args, **kwargs) -> None: ...
    
    def _get_grade(self) -> float: ...
    def _set_grade(self, force: float) -> float: ...
    value = property(_get_grade, _set_grade)


class GradeFormatted:
    """
    Calificación de formato complejo
    --------------------------------
    Estructura grupal que relaciona varias instancias de `Grade` a través de
    una conexión compleja que no puede ser definida por ponderadores ni
    combinaciones lineales. Esto incluye grupos dinámicos en que la nota y
    las evaluaciones que afectan a la calificación están condicionadas por
    expresiones no simples.

    Por ejemplo: supóngase el ramo **Magia Elemental I** que tiene dos
    interrogaciones y un examen. Estas evaluaciones forman el grupo "notas
    teóricas" cuya ponderación en la nota final es del 70%. Sin embargo,
    dentro de este grupo de notas teóricas la importancia está definida de
    la siguiente manera:

    >>> i1, i2, Ex = Interrogacion1, Interrogacion2, Examen
    >>> nota_teorica = (i1 + i2 + 2 * Ex - min(i1, i2, Ex)) / 3

    Es decir, `nota_teorica` es la media aritmética del examen, en conjunto
    con las siguiente dos notas de mayor valor, pudiendo incluir al mismo
    examen nuevamente. Luego de este cálculo, el valor de `nota_teorica`
    es ponderado para considerar su aporte a la nota final del curso.
    """
    def __init__(self, name: str, ponderation: Optional[int]=None,
                 *args, **kwargs) -> None: ...
    def add_single(self, *args, **kwargs) -> None: ...
    def math_represent(self, *args, **kwargs) -> None: ...
    def conditional_exprs(self, *args, **kwargs) -> None: ...
    def explicit_input(self, expr: str, *args, **kwargs): ...
    def _check_safe(self) -> None: ...
    def nosequehacer(self) -> True: ...
    
    def _get_grade(self) -> float: ...
    def _set_grade(self, force: float) -> float: ...
    value = property(_get_grade, _set_grade)


Evals: TypeAlias = GradeSimple | GradeGroup | GradeFormatted


class GradeTable:
    """
    Tabla de grados
    ---------------
    Cada curso tiene asociada una tabla de grados que contiene todas las
    sub-estructuras de calificaciones que el usuario defina. Esta clase
    se encarga de verificar una repartición ponderada coherente, así como
    de integrar las diferencias entre las sub-estructuras en el cálculo de
    nota final. Además, es la encargada de registrar los identificadores
    para cada evaluación existente.
    """
    _ids: Iterator = count()
    def __init__(self) -> None:
        self.ponderated_groups: dict[int, Evals] = defaultdict()
        self.unponderated_groups: dict[int, Evals] = defaultdict()
        self.unassigned: dict[int, Evals] = defaultdict()
        self._table_level: int = 100
    
    def try_ponderation(self, request: int) -> int:
        if request is None or request < 1: return None
        if self._table_level < request:
            return self.try_ponderation(self._table_level)
        self._table_level -= request
        return request

    def create_grade(self, requested_type: Evals, **data) -> bool:
        if data.get("name") is None: return False
        ponderation = self.try_ponderation(data.get("ponderation"))
        if requested_type == GradeSimple:
            creation = GradeSimple(next(self._ids), data.get("name"),
                                   ponderation=ponderation,
                                   **{key: data.get(key) for key in \
                                      data.keys() if \
                                      key not in ("name", "ponderation")})
        elif requested_type == GradeGroup:
            creation = GradeGroup(next(self._ids), data.get("name"),
                                  ponderation=ponderation,
                                  **{key: data.get(key) for key in data.keys()\
                                     if key not in ("name", "ponderation")})
        else:
            raise WtfError("GradeTable>create_grade on grades.py")
        if creation.ponderation is None:
            self.unponderated_groups.__setitem__(creation.id, creation)
        else:
            self.ponderated_groups.__setitem__(creation.id, creation)
        return True

    @classmethod
    def from_data(cls, data) -> Self:
        raise NotImplementedError