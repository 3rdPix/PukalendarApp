from enum import StrEnum, Enum, auto
from datetime import datetime
from typing import Literal
from config import PUCalendarAppPaths
from os.path import exists
import sqlite3

if not exists(PUCalendarAppPaths.Config.DATABASE):
  database_connection = sqlite3.connect(PUCalendarAppPaths.Config.DATABASE)
  database_cursor = database_connection.cursor()
  schema_path = PUCalendarAppPaths.Config.DATABASE_SCHEMA
  with open(schema_path, 'r', encoding='utf-8') as raw_file:
    creation_script = raw_file.read()
  database_cursor.executescript(creation_script)
  # database_connection.commit()
  entries_path = PUCalendarAppPaths.Config.DATABASE_DEFAULT_ENTRIES
  with open(entries_path, 'r', encoding="utf-8") as raw_file:
    entries_script = raw_file.read()
  database_cursor.executescript(entries_script)
  database_connection.commit()
  database_connection.close()

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

class CourseAlreadyExists(Exception):
  def __init__(self, *args: object) -> None:
    self.alias, self.color = args
    super().__init__()

weekDay = Literal["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"]
gradeType = Literal["Hoja", "Ponderado", "Media_Simple", "Media_Geométrica",
                    "Media_Harmónica", "Granulado", "Fórmula_personalizada"]
calcType = Literal["Exigencia_Lineal", "Puntaje_Directo", "Fórmula_Granulada"]
completionStatus = Literal["Pendiente", "Cancelado", "Asistido", "Prioritario"]
class DatabaseManager:
  def __init__(self) -> None:
    self.database_connection = sqlite3.connect(
      PUCalendarAppPaths.Config.DATABASE)
    self.database_cursor = self.database_connection.cursor()

  def create_course(self, sigla: str, nombre: str, creditos: int, periodo: int,
                    nrc: int, seccion: int, alias: str, color: str,
                    profesor: str|None=None, campus: str|None=None,
                    schedule: list[tuple[str, str, str, str]]|None=None
                    ) -> int:
    with self.database_connection:
      self.database_cursor.execute(
        """
        INSERT OR IGNORE INTO Cursos_Maestros (sigla, nombre, creditos)
        VALUES (?, ?, ?);
        """,
        (sigla, nombre, creditos))
      self.database_cursor.execute(
        """
        SELECT curso_maestro_id FROM Cursos_Maestros WHERE sigla = ?;
        """,
        (sigla,))
      master_id: int = self.database_cursor.fetchone()[0]

      self.database_cursor.execute(
        """
        SELECT alias, color FROM Inscripciones
        WHERE nrc = ? AND periodo = ?;
        """,
        (nrc, periodo))
      existing = self.database_cursor.fetchone()
      if existing is not None:
          raise CourseAlreadyExists(*existing)
      self.database_cursor.execute(
        """
        INSERT INTO Inscripciones (
        curso_maestro_id, periodo, nrc, profesor, campus, seccion,
        alias, color)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """,
        (master_id, periodo, nrc, profesor, campus, seccion, alias, color))
      inscription_rowid = self.database_cursor.lastrowid
      if inscription_rowid is None:
        raise RuntimeError("Couldn't save inscription")
      for module in schedule:
        dia_semana, numero_modulo, sala, instance_name = module
        print("Buscando", dia_semana, numero_modulo)
        self.database_cursor.execute(
          """
          SELECT hora_inicio, hora_fin FROM Modulos_Oficiales
          WHERE dia_semana = ? AND numero_modulo = ? AND valido = 1;
          """,
          (dia_semana, numero_modulo))
        result = self.database_cursor.fetchone()
        print(result)
        hora_inicio, hora_fin = result
        self.database_cursor.execute(
          """
          INSERT INTO Modulos_Horarios (inscripcion_id, dia_semana, hora_inicio,
          hora_fin, sala, nombre) VALUES (?, ?, ?, ?, ?, ?);
          """,
          (inscription_rowid, dia_semana, hora_inicio, hora_fin, sala, instance_name))
      return inscription_rowid

  def create_hour_module(self, inscripcion_id: int, dia_semana: weekDay,
                         hora_inicio: str, hora_fin: str,
                         sala: str|None=None
                         ) -> None:
    with self.database_connection:
      self.database_cursor.execute(
        """
        INSERT INTO Modulos_Horarios (inscripcion_id, dia_semana, hora_inicio,
        hora_fin, sala)
        VALUES (?, ?, ?, ?, ?);
        """,
        (inscripcion_id, dia_semana, hora_inicio, hora_fin, sala))
      
  def create_study_session(self, inscripcion_id: int, fecha_inicio: datetime,
                           fecha_fin: datetime, objetivo: str='',
                           es_manual: bool=False
                           ) -> None:
    with self.database_connection:
      self.database_cursor.execute(
        """
        INSERT INTO Sesiones_Estudio (inscripcion_id, fecha_inicio, fecha_fin,
        objetivo, es_manual)
        VALUES (?, ?, ?, ?, ?);
        """,
        (inscripcion_id, fecha_inicio, fecha_fin, objetivo, es_manual))