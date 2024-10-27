from datetime import datetime


class Progression(int):
    def __new__(cls, value: int):
        if not (0 <= value <= 100):
            raise ValueError("Progression must be between 0 and 100.")
        return super().__new__(cls, value)


class Task:
    name: str = None
    expiration_datetime: datetime = None
    graded: bool = False
    description: str = None
    completed: bool = False
    progress: Progression = Progression(0)


class TaskTable:
    """
    Definición de estructura de tareas
    """
    @classmethod
    def from_data(cls, data) -> None:
        raise NotImplementedError