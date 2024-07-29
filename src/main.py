"""
This is the entrance module for the application. The app will likely
not work if another module is used as the entrance point. The program
will stop if it reaches this module from another one.
"""
import sys


if __name__ != '__main__':
    print('''
ERROR: main.py is not being used as the entrance point.
Please start the app using this module found in src/main.py
''')
    sys.exit()

# First step is to add src/ to PATH to search for project modules
from os.path import abspath
from os.path import dirname
from os.path import join

src_dir = abspath(dirname(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Modules are correctly found relative to src/
from PUCalendarApp import MainApp

# Initialize and run
my_app = MainApp(sys.argv)
sys.exit(my_app.exec())