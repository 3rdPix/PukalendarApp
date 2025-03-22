"""
# Tareas y eventos

En este módulo se definen las estructuras de eventos y tareas independientes
ó pertenecientes a un curso.
"""
from datetime import datetime
from dataclasses import dataclass
from collections import defaultdict
from itertools import count

__all__ = {"Task", "Event", "BulletTask"}

class Progression(int):
    def __new__(cls, value: int):
        if not (0 <= value <= 100):
            raise ValueError("Progression must be between 0 and 100.")
        return super().__new__(cls, value)

@dataclass
class Task:
    name: str = None
    expiration_datetime: datetime = None
    graded: bool = False
    description: str = ""
    # hacer de estas dos siguientes, propiedades
    completed: bool = False
    progress: Progression = Progression(0)


@dataclass
class Event:
    name: str = None
    graded: bool = False
    description: str = None
    scheduled_for: datetime = None


class TaskTable:
    """
    Definición de estructura de tareas
    """
    @classmethod
    def from_data(cls, data) -> None:
        raise NotImplementedError


class EventTable:
    """
    Definición de estructura de eventos
    """
    @classmethod
    def from_data(cls, data) -> None:
        raise NotImplementedError

@dataclass
class BulletTask:
    description: str = ""
    done: bool = False


class BulletTaskTable:
    """
    Definición de estructura de bullet task
    """
    id_generator = count()
    vault: dict[int, BulletTask] = defaultdict()

    def __init__(self):
        self.id_generator = count()
        self.vault: dict[int, BulletTask] = defaultdict()

    def create_bullet(self, description: str, done: bool) -> int:
        """
        Crea una tarea rápida con la descripción y retorna su identificador
        """
        new_bullet = BulletTask(description, done)
        bullet_id = next(self.id_generator)
        self.vault.__setitem__(bullet_id, new_bullet)
        return bullet_id

    def get_bullet(self, bullet_id: int) -> BulletTask|None:
        return self.vault.get(bullet_id)
    
    def get_all_bullets(self) -> list[BulletTask]:
        return self.vault.values()
    