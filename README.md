# Pukalendar

[![Static Badge](https://img.shields.io/badge/Framework-brightgreen?style=for-the-badge&logo=qt&logoSize=auto&labelColor=blue)](https://pypi.org/project/PyQt6/)
[![Static Badge](https://img.shields.io/badge/Qt_for_python-green?style=for-the-badge&logo=Google%20Docs&logoColor=white&logoSize=big&labelColor=blue)](https://doc.qt.io/qtforpython-6/)
[![Static Badge](https://img.shields.io/badge/PEP8-coding_style-yellow?style=for-the-badge&logo=python&logoColor=yellow&logoSize=big&labelColor=blue)](https://pep8.org/)

![Static Badge](https://img.shields.io/badge/Windows-blue?style=flat-square&logo=windows&labelColor=blue)
![Static Badge](https://img.shields.io/badge/Linux-lightgray?style=flat-square&logo=linux&logoColor=black&logoSize=big)
![Static Badge](https://img.shields.io/badge/MacOS-blue?logo=apple)

[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-lightgrey.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

## Descripción

Pukalendar es un programa que busca facilitar la vida universitaria al proveer múltiples herramientas de utilidad para llevar un buen registro de las actividades universitarias tales como eventos, tareas, evaluaciones, etc. Además, permite mantener un historial de cursos inscritos a través del cual se puede obtener información variada de los mismos.

La aplicación también cuenta con un robusto sistema de seguimiento de calificaciones que permite modelar los requisitos de la gran mayoría de los cursos. Esto le entrega al estudiante información precisa respecto a las evaluaciones más relevantes, lo que le permite enfocarse en los estudios de forma más óptima.

También cuenta con un sistema de sesiones de estudio, a través del cual el estudiante puede conocer cuántas horas semanales dedica a cada curso, lo que ayuda a lograr un mejor balance de tiempo dedicado entre sus cursos inscritos.

Lamentablemente, esta aplicación se encuentra en fase de desarrollo, por lo que de momento no está disponible para el público general. Sin embargo, es posible utilizarla por medio de herramientas de desarrollo de _software_. Puedes dirigirte a la sección respectiva para conocer más detalles de cómo lanzar la aplicación en modo desarrollador. Si tienes cualquier consulta, siempre puedes dirigirte a la sección de [_issues_](https://github.com/3rdPix/PukalendarApp/issues) y publicar una entrada con tu duda.

# Desarrolladores

Esta aplicación de escritorio está desarrollada utilizando el framework *PyQt6*, y se apoya en paquetes externos para proporcionar una experiencia de usuario moderna y estilizada. La aplicación está diseñada para ofrecer una interfaz gráfica intuitiva y eficiente.

## Requisitos

La aplicación ha sido desarrollada con *Python 3.11.2*. Se recomienda usar esta versión de Python o versiones posteriores para garantizar la compatibilidad.

## Instalación

Para asegurar un correcto funcionamiento de la aplicación, sigue estos pasos:

1. **Crear un entorno virtual**: Esto es esencial para gestionar las dependencias y evitar conflictos con otros proyectos. Si no estás familiarizado con la creación de entornos virtuales en Python, consulta la [documentación oficial](https://docs.python.org/3/library/venv.html).

2. **Activar el entorno virtual**:
   - **En Windows**: Ejecuta `venv\Scripts\activate`
   - **En macOS y Linux**: Ejecuta `source venv/bin/activate`

3. **Instalar las dependencias**: Con el entorno virtual activado, instala los paquetes necesarios utilizando el archivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

El archivo principal para ejecutar la aplicación es `main.py`, ubicado en el directorio `src/`. Este archivo es el punto de entrada principal para la aplicación. Asegúrate de ejecutar solo este módulo para evitar problemas de importación y funcionamiento. Puedes ejecutar la aplicación con el siguiente comando:

```bash
python src/main.py
```

## Cómo Contribuir

### Reportar Problemas

Si encuentras un error o tienes una sugerencia, por favor, sigue estos pasos:

1. **Verifica** si el problema ya ha sido reportado en el [issue tracker](https://github.com/3rdPix/PUCalendarApp/issues). Si es así, puedes agregar tus comentarios o proporcionar información adicional.
2. **Crea un nuevo issue** si no has encontrado una solución similar. Proporciona una descripción clara del problema, los pasos para reproducirlo y cualquier otro detalle relevante.

### Solicitar Nuevas Funcionalidades

Si tienes una idea para una nueva característica:

1. **Consulta los issues existentes** para asegurarte de que tu propuesta no esté ya en discusión.
2. **Abre un nuevo issue** con una descripción detallada de la funcionalidad que te gustaría agregar, junto con razones de por qué sería útil.

### Contribuir Código

Para contribuir código, sigue estos pasos:

1. **Fork** el repositorio y **clona** tu fork a tu máquina local.
2. **Crea una rama** para tu cambio:
   ```bash
   git checkout -b nombre-de-tu-rama
   ```
3. **Haz tus cambios** y realiza pruebas para asegurarte de que todo funciona correctamente.
4. **Haz *commit* de tus cambios** con mensajes claros y descriptivos:
   ```bash
   git add .
   git commit -m "Descripción clara de los cambios"
   ```
5. **Añade** tus cambios a tu fork:
   ```bash
   git push origin nombre-de-tu-rama
   ```
6. **Crea un Pull Request** desde tu fork hacia el repositorio original. Asegúrate de proporcionar una descripción detallada de los cambios y por qué deberían ser incluidos.

El estilo de código debe seguir el formato estándar de desarrollo para los proyectos de *python*, cuya guía de referencia se encuentra en el sitio oficial del formato [PEP8](https://pep8.org/).

La totalidad del código, incluyendo nombres de variables, módulos, clases y demases, debe estar en **inglés**. Por su parte, la documentación (es decir, comentarios, y descripciones de funciones y clases) debe estar en **español**.

Además, y sin excepción, todo el código escrito debe estar en [**utf-8**](https://en.wikipedia.org/wiki/UTF-8).

## Licencia

En concordancia con las exigencias del framework, esta aplicación está bajo la *GNU General Public License v3*, consulta el archivo [LICENSE](LICENSE) para más detalles.