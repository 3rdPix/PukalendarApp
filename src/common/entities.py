from enum import Enum
from enum import auto
from dataclasses import dataclass
from datetime import datetime

class SchemaKeys:
  class Cursos_Maestros(Enum):
    curso_maestro_id = auto()
    sigla = auto()
    nombre = auto()
    creditos = auto()
  
  class Inscripciones(Enum):
    inscripcion_id = auto()
    curso_maestro_id = auto()
    periodo = auto()
    nrc = auto()
    profesor = auto()
    campus = auto()
    seccion = auto()
    alias = auto()
    color = auto()
    nota_final = auto()

  class Modulos_Horarios(Enum):
    modulo_id = auto()
    inscripcion_id = auto()
    dia_semana = auto()
    hora_inicio = auto()
    hora_fin = auto()
    sala = auto()
    nombre = auto()
  
  class Calificaciones_Estructura(Enum):
    estructura_id = auto()
    inscripcion_id = auto()
    padre_id = auto()
    nombre = auto()
    tipo_estructura = auto()
    ponderacion = auto()
    es_eliminable = auto()
    es_extremista = auto()
    expresion_calculo = auto()
  
  class Metodo_Calculo_Nota(Enum):
    metodo_id = auto()
    estructura_id = auto()
    tipo_metodo = auto()
    exigencia_porcentaje = auto()
    puntaje_maximo_esperado = auto()
    puntaje_total_posible = auto()

  class Actividades(Enum):
    actividad_id = auto()
    inscripcion_id = auto()
    estructura_id_asociada = auto()
    tipo = auto()
    nombre = auto()
    descripcion = auto()
    tiene_calificacion = auto()
    es_horario_fijo = auto()
    fecha_arbitraria = auto()
    duracion_minutos = auto()

  class Actividades_Modulos(Enum):
    actividad_modulo_id = auto()
    actividad_id = auto()
    modulo_id = auto()
    fecha_instancia = auto()
    estado = auto()

  class Calificaciones_Valores(Enum):
    valor_id = auto()
    estructura_id = auto()
    actividad_id = auto()
    puntaje_obtenido = auto()
    nota_calculada = auto()
    nota_manual_usuario = auto()
    usar_nota_manual = auto()
    puntos_extra = auto()
    puntaje_maximo = auto()

  class Sesiones_Estudio(Enum):
    sesion_id = auto()
    inscripcion_id = auto()
    fecha_inicio = auto()
    fecha_fin = auto()
    objetivo = auto()
    es_manual = auto()

  class Tareas_Pendientes(Enum):
    tarea_id = auto()
    padre_tarea_id = auto()
    inscripcion_id = auto()
    actividad_id = auto()
    nombre = auto()
    descripcion = auto()
    fecha_limite = auto()
    porcentaje_copletado = auto()
    estado = auto()
    es_recurrente = auto()
    fecha_fin_recurrencia = auto()
    fecha_creacion = auto()

  class Modulos_Oficiales(Enum):
    modulo_id = auto()
    dia_semana = auto()
    hora_inicio = auto()
    hora_fin = auto()
    numero_modulo = auto()
    valido = auto()

  class Semestres(Enum):
    semestre_id = auto()
    anio = auto()
    etapa = auto()
    fecha_inicio = auto()
    fecha_fin = auto()

@dataclass
class InformacionCurso:
  sigla: str
  nombre: str
  creditos: int
  nrc: str
  profesor: str
  campus: str
  seccion: int
  periodo: str

@dataclass
class ResultadoBuscacurso(InformacionCurso):
  modulos: list[list[str]]

@dataclass
class CursoAplicacion(InformacionCurso):
  identificador: int
  alias: str
  color: str

@dataclass
class StudySession:
  inscripcion_id: int
  fecha_inicio: datetime
  fecha_fin: datetime
  objetivo: str = ''
  es_manual: bool = False