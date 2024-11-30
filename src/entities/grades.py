r"""
# Módulo de calificaciones

La nota mínima en la universidad es $1.0$, la nota de aprobación es $4.0$, y la
nota máxima es $7.0$. La exigencia refiere al porcentaje de correctitud que
debe tener una evaluación para alcanzar la nota de aprobación, de este modo,
en una prueba con $100$ preguntas al $60\%$ de exigencia, se deben tener
justamente $60$ respuestas correctas para alcanzar la nota $4.0$.

El formato de cálculo más simple implica crear dos rectas; una para el
segmento llamado "rojo" (bajo la nota de aprobación) entre $[1.0, 4.0)$, y
otra para el segmento llamado "azul" (sobre la nota de aprobación) entre
$[4.0, 7.0]$.

Luego, si se tiene $x$ porcentaje de respuestas correctas para una evaluación,
la nota será determinada según:

+ **Para rojos:** ($x < \text{exigencia}$)
$$
    y = \left(
    \frac{7.0 - 4.0}{\text{exigencia}}
    \right) x + 4.0
$$

+ **Para azules:** ($x \geq \text{exigencia}$)

$$
    y = \left(
    \frac{7.0 -4.0}{100.0 - \text{exigencia}}
    \right) x + 4.0 - \left(
    \frac{7.0 -4.0}{100.0 - \text{exigencia}}
    \right) \text{exigencia}
$$
"""
from typing import Optional
from collections import defaultdict
from typing import Self
from typing import TypeAlias
from collections.abc import Iterator
from itertools import count
from math import prod
from abc import ABC
from abc import abstractmethod
from typing import Protocol
from typing import overload
from collections.abc import Callable
import logging
class WtfError(Exception):
    """
    xd
    """

__all__ = {"Grade", "GradeSimple", "GradeGroup", "GradingFormula",
           "MathingGrades"}

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


class Grade(ABC):
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

    + `threshold`: porcentaje de respuestas correctas necesarias para obtener
    el mínimo grado de aprobación. Por defecto es 60.

    + `obtained_grade`: sobrescribe la nota calculada según `obtained_score`.
    Debe estar entre 1.0 y 7.0.

    + `add_base`: si se habilita, se le agrega un punto base (1.0) a la nota
    calculada según el puntaje obtenido.

    Esta estructura lleva nombre (puede ser definido por el usuario).
    """
    def _get_grade(self) -> float:
        if hasattr(self, "_obtained_grade"): return self._obtained_grade
        if hasattr(self, "_mathed_grade"): return self._mathed_grade
        return -1
    def _set_grade(self, forced_value: float) -> None:
        if not GRADE_MINIMUM <= forced_value <= GRADE_MAXIMUM:
            raise ValueError("Obtained grade not within valid range")
        self._obtained_grade = forced_value
    value = property(_get_grade, _set_grade)

    def assign_numbers(self, obtained_score: Optional[float]=None,
                       total_score: float=100.0,
                       threshold: int=DEFAULT_THRESHOLD,
                       obtained_grade: Optional[float]=None,
                       add_base: bool=False, **kwgs) -> None:
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
        

class MathingGrades:
    """
    Una colección de funciones para calcular la nota final de acuerdo con
    la función elegida por el usuario.
    """
    @staticmethod
    def arithmetic_mean(grades: list[Grade]) -> float:
        return sum(grade.value for grade in grades) / len(grades)

    @staticmethod
    def geometric_mean(grades: list[Grade]) -> float:
        return prod(grade.value for grade in grades) ** (1 / len(grades))

    @staticmethod
    def harmonic_mean(grades: list[Grade]) -> float:
        return len(grades) / sum(1 / grade.value for grade in grades)


class GradeSimple(Grade):
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
    def __init__(self, id: int, name: str) -> None:
        super().__init__()
        self.id: int = id
        self.name: str = name

    def define_relation(self, ponderator: Optional[int]=None,
                        extra_points: int=0,
                        extremist: Optional[float]=None, **kwgs) -> None:
        if ponderator is not None: self.ponderator = ponderator
        self.extra_points = extra_points
        if extremist is not None: self.extremist = extremist
    
    def _get_relative_value(self) -> float:
        concurrent: float = self.value
        if hasattr(self, "extra_points") \
           and not hasattr(self, "_obtained_grade"):
            concurrent += self.extra_points / 10
        if hasattr(self, "ponderator"):
            concurrent *= (self.ponderator / 100)
        return concurrent
    value_relative = property(_get_relative_value)
    """
    Es el valor que toma realmente la evaluación para el aporte final de
    la nota dentro del grupo al que pertenece. Si no tiene ponderador,
    retornará su valor natural y el contenedor es el encargado de integrar
    ese valor a la ecuación adecuada.
    """


class GradingFormula(Protocol):
    """
    # Fórmula de calificación
    Puede ser una predefinida en los contenedores correspondientes (por
    ejemplo en `MathingGrades`) ó una definida por el usuario a través de
    las clases correspondientes.
    """
    @overload
    def __call__(grades: list[Grade]) -> float: ...
    @overload
    def __call__(grades: list[Grade],
                 usr_def: Callable[[list[Grade]], float]) -> float: ...
    @overload
    def __call__(grades: dict[int, Grade],
                 usr_def: Callable[[list[Grade]], float]) -> float: ...


class GradeGroup(GradeSimple):
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
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
        self.id_handler: Iterator = count()
        self._total_ponderation: int = 100
        self.group_ponderated = dict[int, GradeSimple] = defaultdict()
        self.group_unponderated = dict[int, GradeSimple] = defaultdict()
        # Por defecto dejamos la media aritmética
        self.mathing_formula: GradingFormula = MathingGrades.arithmetic_mean
    
    
    def try_ponderation(self, request: int) -> int:
        """
        Asegura que la ponderación total de los elementos no supere el valor
        máximo del ramo (100%).
        """
        if request is None or request < 1: return None
        if self._total_ponderation < request:
            return self.try_ponderation(self._total_ponderation)
        approved = int(request)
        self._total_ponderation -= request
        return approved

    # Redefinimos el valor
    def _get_grade(self) -> float:
        if hasattr(self, "_obtained_grade"): return self._obtained_grade
        total_grade = 0
        for grade in self.group_ponderated.values():
            total_grade += grade.value_relative
        lonely_grades = list(self.group_unponderated.values())
        total_grade += self.mathing_formula.__call__(lonely_grades)
        # Agregamos un checkeo solo por si acaso
        if not GRADE_MINIMUM <= total_grade <= GRADE_MAXIMUM:
            log.error(f"Couldn't grade {self}:{total_grade}")
            raise ValueError
        self._mathed_grade = total_grade
        return total_grade
    def _set_grade(self, forced_value: float) -> None:
        if not GRADE_MINIMUM <= forced_value <= GRADE_MAXIMUM:
            raise ValueError("Obtained grade not within valid range")
        self._obtained_grade = forced_value
    value = property(_get_grade, _set_grade)

    def get_eval_from_id(self, id: int) -> object:
        # Si o si es de este nivel
        if id in self.group_ponderated.keys():
            return self.group_ponderated.get(id)
        elif id in self.group_unponderated.keys():
            return self.group_unponderated.get(id)
        else:
            log.error(f"Tried to find id:{id} at {self} but"
                      f" wasn't found on: {self.group_ponderated}"
                      f" or {self.group_unponderated}")
            raise KeyError("Id not here")

    def create_grade(self, locate: list[int], requested_type: object,
                     name: str) -> int|None:
        """
        Instancia una evaluación del tipo solicitado y retorna el `id` para
        referenciarle posteriormente.
        """
        # Si soy un group y me llega len 0 es porque yo tengo
        # que crearlo a mi nivel
        if len(locate) > 0:
            next_step: int = locate.pop(0)
            next_who: GradeGroup = self.get_eval_from_id(next_step)
            return next_who.create_grade(locate, requested_type, name)
        # si llego aquí significa que yo tengo que crearlo
        new: GradeSimple|GradeGroup = requested_type(
            next(self.id_handler), name)
        self.group_unponderated.__setitem__(new.id, new)
        return new.id

    def remove_grade(self, locate: list[int]) -> bool|None:
        """
        Elimina (por completo de la faz) una evaluación
        """
        if len(locate) > 1:
            next_step: int = locate.pop(0)
            next_who: GradeGroup = self.get_eval_from_id(next_step)
            return next_who.remove_grade(locate)
        who_to_kill: int = locate.pop(0)
        if who_to_kill in self.group_ponderated.keys():
            self.group_ponderated.__delitem__(who_to_kill)
        elif who_to_kill in self.group_unponderated.keys():
            self.group_unponderated.__delitem__(who_to_kill)
        else:
            log.error(f"Tried to delete id:{who_to_kill} but wasn't found on"
                      f" {self.group_ponderated} or {self.group_unponderated}")
            raise KeyError("Id not here")
        return True
        
    def edit_grade(self, locate: list[int], **kwargs) -> bool:
        """
        Editar ¿? qué significa esto
        """

    def assign_numbers(self, locate: list[int], **kwargs) -> None:
        this_level = locate.pop(0)
        if this_level in self.group_ponderated.keys():
            sub_location = self.group_ponderated.get(this_level)
            if isinstance(sub_location, GradeSimple):
                sub_location.assign_numbers(**kwargs)
            elif isinstance(sub_location, GradeGroup):
                sub_location.assign_numbers(locate, **kwargs)
            else:
                log.error(f"Trying to assign numbers to non Grade object "
                          f"at level {this_level}->{locate} which is"
                          f" {sub_location}. Payload is {kwargs}")
                raise TypeError
        elif this_level in self.group_unponderated.keys():
            sub_location = self.group_unponderated.get(this_level)
            if isinstance(sub_location, GradeSimple):
                sub_location.assign_numbers(**kwargs)
            elif isinstance(sub_location, GradeGroup):
                sub_location.assign_numbers(locate, **kwargs)
            else:
                log.error(f"Trying to assign numbers to non Grade object "
                          f"at level {this_level}->{locate} which is"
                          f" {sub_location}. Payload is {kwargs}")
                raise TypeError
        else:
            log.error(f"Asigning numbers to non-existing Grade on {this_level}"
                      f"->{locate}.")
            raise KeyError


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

    def create_grade(self, requested_type: Evals, locate: Optional[list]=None,
                     **data) -> bool|tuple[bool, int]:
        if data.get("name") is None: return False
        if locate is not None:
            location_copy = locate.copy()
            under_group: int = location_copy.pop(0)
            # buscarle
            group_0: GradeGroup = self.ponderated_groups.get(under_group)
            if group_0 is not None:
                ided = group_0.create_grade(location_copy,
                                            requested_type, data.get("name"))
                group_0.assign_numbers(location_copy, **data)
                return True, ided
            group_1: GradeGroup = self.unponderated_groups.get(under_group)
            if group_1 is not None:
                ided = group_1.create_grade(location_copy,
                                            requested_type, data.get("name"))
                group_1.assign_numbers(location_copy, **data)
                return True, ided
            group_2: GradeGroup = self.unassigned.get(under_group)
            if group_2 is not None:
                ided = group_2.create_grade(location_copy,
                                            requested_type, data.get("name"))
                group_2.assign_numbers(location_copy, **data)
                return True, ided
        ponderation = self.try_ponderation(data.get("ponderation"))
        if requested_type == GradeSimple:
            creation = GradeSimple(next(self._ids), data.get("name"))
            creation.assign_numbers(**{key: data.get(key) for key in \
                                      data.keys() if \
                                      key not in ("name", "ponderation")})
            creation.define_relation(ponderation, **data)
        elif requested_type == GradeGroup:
            creation = GradeGroup(next(self._ids), data.get("name"),
                                  ponderation=ponderation,
                                  **{key: data.get(key) for key in data.keys()\
                                     if key not in ("name", "ponderation")})
        else:
            raise WtfError("GradeTable>create_grade on grades.py")
        if creation.ponderator is None:
            self.unponderated_groups.__setitem__(creation.id, creation)
        else:
            self.ponderated_groups.__setitem__(creation.id, creation)
        return True, creation.id

    def assign_numbers(self, locate: list[int], **kwargs) -> None:
        this_level = locate.pop(0)
        if this_level in self.group_ponderated.keys():
            sub_location = self.group_ponderated.get(this_level)
            if isinstance(sub_location, GradeSimple):
                sub_location.assign_numbers(**kwargs)
            elif isinstance(sub_location, GradeGroup):
                sub_location.assign_numbers(locate, **kwargs)
            else:
                log.error(f"Trying to assign numbers to non Grade object "
                          f"at level {this_level}->{locate} which is"
                          f" {sub_location}. Payload is {kwargs}")
                raise TypeError
        elif this_level in self.group_unponderated.keys():
            sub_location = self.group_unponderated.get(this_level)
            if isinstance(sub_location, GradeSimple):
                sub_location.assign_numbers(**kwargs)
            elif isinstance(sub_location, GradeGroup):
                sub_location.assign_numbers(locate, **kwargs)
            else:
                log.error(f"Trying to assign numbers to non Grade object "
                          f"at level {this_level}->{locate} which is"
                          f" {sub_location}. Payload is {kwargs}")
                raise TypeError
        else:
            log.error(f"Asigning numbers to non-existing Grade on {this_level}"
                      f"->{locate}.")
            raise KeyError

    @classmethod
    def from_data(cls, data) -> Self:
        raise NotImplementedError