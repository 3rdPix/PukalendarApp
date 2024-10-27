import requests
import datetime
from bs4 import BeautifulSoup


def get_year_and_value() -> tuple[str, str]:
    current_month = datetime.datetime.now().month
    current_year = str(datetime.datetime.now().year)

    if current_month >= 12 or current_month <= 6:
        return (current_year, '1')
    else:
        return (current_year, '2')


def _extract_course_data(html_snippet: str) -> list:
    """
    Parse HTML from buscacursos.uc.cl to read results of the search
    """
    soup = BeautifulSoup(html_snippet, 'html.parser')
    rows = soup.find_all(class_=["resultadosRowPar", "resultadosRowImpar"])

    course_list = []

    for row in rows:
        columns = row.find_all('td')
        course_dict = {
            'official_nrc': columns[0].get_text().strip(),
            'official_code': columns[1].get_text().strip(),
            'official_name': columns[9].get_text().strip(),
            'official_campus': columns[11].get_text().strip(),
            'official_section': columns[4].get_text().strip(),  
            'official_modules': []}

        try:
            course_dict['professor'] = \
                columns[10].find_all('a')[0].get_text().strip()
        except IndexError:
            course_dict['professor'] = 'Ninguno'

        # Extract dates from the table
        table_rows = row.find_all('tr')
        for table_row in table_rows:
            date_columns = table_row.find_all('td')
            if len(date_columns) == 3:
                date_info = [date_columns[0].get_text().strip(),
                             date_columns[1].get_text().strip(),
                             date_columns[2].get_text().strip()]
                course_dict['dates'].append(date_info)

        course_list.append(course_dict)
        
    return course_list


def search_for_puclasses(search_pattern: str) -> list[dict] | None:
    """
    Searches for courses that match the pattern
    -------------------------------------------
    `search_pattern: str`: any nrc-like or name-like
    `year: str`: as string, for example, `"2024"`
    `semester: str`: as string. Only "1" or "2".
    -------------------------------------------
    Returns a list with all courses matching the pattern in the form of 
    dictionaries.
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