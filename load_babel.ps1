Write-Output "Extrayendo contenido desde src/"
pybabel extract -F src/config/babel.cfg -o resources/locale/messages.pot src/
if (!(Test-Path "resources/locale/es")) {
    Write-Output "Paquete de español no encontrado. Creando."
    pybabel init -i resources/locale/messages.pot -d resources/locale -l es
}
if (!(Test-Path "resources/locale/en")) {
    Write-Output "Paquete de inglés no encontrado. Creando."
    pybabel init -i resources/locale/messages.pot -d resources/locale -l en
}
if (!(Test-Path "resources/locale/fr")) {
    Write-Output "Paquete de francés no encontrado. Creando."
    pybabel init -i resources/locale/messages.pot -d resources/locale -l fr
}

Write-Output "Contenidos extraídos en las carpetas resources/locale/\$LANG. Actualizando..."
pybabel update -i resources/locale/messages.pot -d resources/locale

# Eliminar la línea `#, fuzzy` en archivos .po
Get-ChildItem -Path "resources/locale" -Recurse -Filter "*.po" | ForEach-Object {
    (Get-Content $_.FullName) -replace '^#, fuzzy$', '' | Set-Content $_.FullName
}

Write-Output "Debes agregar el contenido y luego ejecutar pybabel compile -d resources/locale"
