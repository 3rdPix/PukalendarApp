from datetime import datetime
from dataclasses import dataclass

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
    description: str = None
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
    name: str = None
    done: bool = False


class BulletTaskTable:
    """
    Definición de estructura de bullet task
    """
    @classmethod
    def from_data(cls, data) -> None:
        raise NotImplementedError