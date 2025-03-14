
from datetime import timedelta
from entities import Course


def calculate_relative_dedication(courses: list[Course]) -> list[int]:
    """
    Toma la cantidad de horas dedicadas a cada curso y calcula el porcentaje
    de horas totales a la que corresponde.
    """
    # timedelta de cada cuurso
    hours_per_course: list[timedelta] = [
        course.get_dedicated_time() for course in courses]
    total_hours: timedelta = timedelta(0)
    for time_section in hours_per_course:
        total_hours += time_section
    if total_hours.seconds == 0: return [0 for _ in range(len(courses))]
    return [round(100 * dedicated_hours / total_hours)
            for dedicated_hours in hours_per_course]