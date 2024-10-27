"""
Este es el módulo de entrada para la aplicación. El programa no
funcionará si otro módulo es utilizado como punto de entrada.
Además, se detendrá la ejecución si este módulo es importado
por otro.
"""
import sys


if __name__ != '__main__':
    print('''
ERROR: main.py is not being used as the entrance point.
Please start the app using this module found in src/main.py
''')
    sys.exit()

# El primer paso es añadir src/ al PATH del sistema para
# importar los módulos consistentemente
from os.path import abspath
from os.path import dirname
from os.path import join
import logging

logging.basicConfig()

src_dir = abspath(dirname(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Ahora los módulos son correctamente encontrados a partir de src/
from PUCalendarApp import MainApp

# Inicializar la aplicación y ejecutar
my_app = MainApp(sys.argv)
sys.exit(my_app.exec())