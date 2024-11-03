echo "Extrayendo contenido desde src/"
pybabel extract -F src/config/babel.cfg -o resources/locale/messages.pot src/
if [ ! -d "resources/locale/es" ]; then
    echo "Paquete de español no encontrado. Creando."
    pybabel init -i resources/locale/messages.pot -d resources/locale -l es
fi
if [ ! -d "resources/locale/en" ]; then
    echo "Paquete de inglés no encontrado. Creando."
    pybabel init -i resources/locale/messages.pot -d resources/locale -l en
fi
if [ ! -d "resources/locale/fr" ]; then
    echo "Paquete de francés no encontrado. Creando."
    pybabel init -i resources/locale/messages.pot -d resources/locale -l fr
fi
echo "Contenidos extraídos en las carpetas resources/locale/\$LANG. Actualizando..."
pybabel update -i resources/locale/messages.pot -d resources/locale
find resources/locale/ -name "*.po" -exec sed -i '/^#, fuzzy$/d' {} +
echo "Debes agregar el contenido y luego ejecutar pybabel compile -d resources/locale"