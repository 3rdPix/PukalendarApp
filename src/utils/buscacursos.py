r"""
# Scrapper

Este módulo provee el catálogo de cursos de acuerdo a un patrón de búsqueda
especificado por el usuario. Para lograr esto, se realiza extracción de
contenido del sitio [Buscacursos](http://buscacursos.uc.cl).
"""
import requests
import datetime
from bs4 import BeautifulSoup, ResultSet
from common.entities import ResultadoBuscacurso


__all__ = {"search_for_puclasses"}

def get_year_and_value() -> tuple[str, str]:
    current_month = datetime.datetime.now().month
    current_year = str(datetime.datetime.now().year)

    if current_month >= 12 or current_month <= 6:
        return (current_year, '1')
    else:
        return (current_year, '2')


def _extract_course_data(html_snippet: str) -> list[ResultadoBuscacurso]:
    """
    Parsear HTML del sitio para leer resultados
    """
    soup = BeautifulSoup(html_snippet, 'html.parser')
    rows: ResultSet = soup.find_all(class_=["resultadosRowPar", "resultadosRowImpar"])

    course_list: list[ResultadoBuscacurso] = []
    year, semester = get_year_and_value()
    periodo = str(year)[-2:] + semester
    for row in rows:
        columns = row.find_all('td')
        try:
            profesor = columns[10].find_all('a')[0].get_text().strip()
        except IndexError:
            profesor = "No asignado"
        
        horarios: list[list[str]] = list()
        # Extract dates from the table
        table_rows = row.find_all('tr')
        for table_row in table_rows:
            date_columns = table_row.find_all('td')
            if len(date_columns) == 3:
                date_info = [date_columns[0].get_text().strip(),
                             date_columns[1].get_text().strip(),
                             date_columns[2].get_text().strip()]
                horarios.append(date_info)

        curso = ResultadoBuscacurso(
            sigla=columns[1].get_text().strip(),
            nombre=columns[9].get_text().strip(),
            creditos=int(columns[12].get_text().strip()),
            nrc=columns[0].get_text().strip(),
            profesor=profesor,
            campus=columns[11].get_text().strip(),
            seccion=int(columns[4].get_text().strip()),
            modulos=horarios,
            periodo=periodo)

        course_list.append(curso)
        
    return course_list


def search_for_puclasses(search_pattern: str) -> list[ResultadoBuscacurso]:
    """
    # Busca cursos que coincidan con el texto
    
    `search_pattern: str`: intento de sigla ó nombre
    
    Retorna una lista con todos los cursos que coincidan con el patrón
    de búsqueda, en que cada curso es un diccionario.
    """
    name_url = ("https://buscacursos.uc.cl/?cxml_semestre={}-{}&cxml_sigla"
                "=&cxml_nrc=&cxml_nombre={}&cxml_categoria=TODOS&cxml_area"
                "_fg=TODOS&cxml_formato_cur=TODOS&cxml_profesor=&cxml_camp"
                "us=TODOS&cxml_unidad_academica=TODOS&cxml_horario_tipo_bu"
                "squeda=si_tenga&cxml_horario_tipo_busqueda_actividad=TODOS")
    nrc_url = ("https://buscacursos.uc.cl/?cxml_semestre={}-{}&cxml_sigla="
               "{}&cxml_nrc=&cxml_nombre=&cxml_categoria=TODOS&cxml_area_f"
               "g=TODOS&cxml_formato_cur=TODOS&cxml_profesor=&cxml_campus="
               "TODOS&cxml_unidad_academica=TODOS&cxml_horario_tipo_busque"
               "da=si_tenga&cxml_horario_tipo_busqueda_actividad=TODOS")
    year, semester = get_year_and_value()
    name_response = requests.get(
        name_url.format(year, semester, search_pattern)).text
    nrc_response = requests.get(
        nrc_url.format(year, semester, search_pattern)).text
    courses_with_matching_name = _extract_course_data(name_response)
    courses_with_matching_nrc = _extract_course_data(nrc_response)
    return courses_with_matching_name + courses_with_matching_nrc